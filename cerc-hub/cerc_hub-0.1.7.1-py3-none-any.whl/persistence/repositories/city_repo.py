"""
City repository with database CRUD operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""

from hub.city_model_structure.city import City
from hub.persistence import BaseRepo
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from hub.persistence.models import City as DBCity
import pickle
import requests
from urllib3.exceptions import HTTPError
from typing import Union, Dict
from hub.hub_logger import logger
import datetime


class CityRepo(BaseRepo):
  _instance = None

  def __init__(self, db_name: str, dotenv_path: str, app_env: str):
    super().__init__(db_name, dotenv_path, app_env)

  def __new__(cls, db_name, dotenv_path, app_env):
    """
    Implemented for a singleton pattern
    """
    if cls._instance is None:
      cls._instance = super(CityRepo, cls).__new__(cls)
    return cls._instance

  def insert(self, city: City, user_id: int) -> Union[City, Dict]:
    db_city = DBCity(pickle.dumps(city), city.name, city.srs_name, city.country_code, city.lower_corner,
                     city.upper_corner, user_id)
    db_city.climate_reference_city = city.climate_reference_city
    db_city.longitude = city.longitude
    db_city.latitude = city.latitude
    db_city.time_zone = city.time_zone

    try:
      # Retrieve hub project latest release
      response = requests.get("https://rs-loy-gitlab.concordia.ca/api/v4/projects/2/repository/branches/master",
                              headers={"PRIVATE-TOKEN": self.config.hub_token})
      recent_commit = response.json()["commit"]["id"]
      logger.info(f'Current commit of hub is {recent_commit}')
      exiting_city = self._get_by_hub_version(recent_commit, city.name)

      # Do not persist the same city for the same version of Hub
      if exiting_city is None:
        db_city.hub_release = recent_commit
        cities = self.get_by_name(city.name)
        # update version for the same city but different hub versions

        if len(cities) == 0:
          db_city.city_version = 0
        else:
          db_city.city_version = cities[-1].city_version + 1

        # Persist city
        self.session.add(db_city)
        self.session.flush()
        self.session.commit()
        return db_city
      else:
        return {'message': f'Same version of {city.name} exist'}
    except SQLAlchemyError as err:
      logger.error(f'Error while adding city: {err}')
    except HTTPError as err:
      logger.error(f'Error retrieving Hub latest release: {err}')

  def get_by_id(self, city_id: int) -> DBCity:
    """
    Fetch a City based on the id
    :param city_id: the city id
    :return: a city
    """
    try:
      return self.session.execute(select(DBCity).where(DBCity.id == city_id)).first()[0]
    except SQLAlchemyError as err:
      logger.error(f'Error while fetching city: {err}')

  def _get_by_hub_version(self, hub_commit: str, city_name: str) -> City:
    """
    Fetch a City based on the name and hub project recent commit
    :param hub_commit: the latest hub commit
    :param city_name: the name of the city
    :return: a city
    """
    try:
      return self.session.execute(select(DBCity)
                                  .where(DBCity.hub_release == hub_commit, DBCity.name == city_name)).first()
    except SQLAlchemyError as err:
      logger.error(f'Error while fetching city: {err}')

  def update(self, city_id: int, city: City):
    """
    Updates a city
    :param city_id: the id of the city to be updated
    :param city: the city object
    :return:
    """
    try:
      self.session.query(DBCity).filter(DBCity.id == city_id) \
        .update({
          'name': city.name, 'srs_name': city.srs_name, 'country_code': city.country_code, 'longitude': city.longitude,
          'latitude': city.latitude, 'time_zone': city.time_zone, 'lower_corner': city.lower_corner.tolist(),
          'upper_corner': city.upper_corner.tolist(), 'climate_reference_city': city.climate_reference_city,
          'updated': datetime.datetime.utcnow()
        })

      self.session.commit()
    except SQLAlchemyError as err:
      logger.error(f'Error while updating city: {err}')

  def get_by_name(self, city_name: str) -> [DBCity]:
    """
    Fetch city based on the name
    :param city_name: the name of the building
    :return: [ModelCity] with the provided name
    """
    try:
      result_set = self.session.execute(select(DBCity).where(DBCity.name == city_name))
      return [building[0] for building in result_set]
    except SQLAlchemyError as err:
      logger.error(f'Error while fetching city by name: {err}')

  def get_by_user(self, user_id: int) -> [DBCity]:
      """
      Fetch city based on the user who created it
      :param user_id: the id of the user
      :return: [ModelCity] with the provided name
      """
      try:
        result_set = self.session.execute(select(DBCity).where(DBCity.user_id == user_id))
        return [building[0] for building in result_set]
      except SQLAlchemyError as err:
        logger.error(f'Error while fetching city by name: {err}')

  def delete_city(self, city_id: int):
    """
    Deletes a City with the id
    :param city_id: the city id
    :return: a city
    """
    try:
      self.session.query(DBCity).filter(DBCity.id == city_id).delete()
      self.session.commit()
    except SQLAlchemyError as err:
      logger.error(f'Error while fetching city: {err}')
