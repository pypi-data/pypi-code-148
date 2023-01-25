"""
DBFactory performs read related operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project CoderPeter Yefi peteryefi@gmail.com
"""
from hub.persistence import CityRepo
from hub.persistence import HeatPumpSimulationRepo


class DBFactory:
  """
  DBFactory class
  """

  def __init__(self, db_name, app_env, dotenv_path):
    self._city_repo = CityRepo(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)
    self._hp_simulation_repo = HeatPumpSimulationRepo(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)

  def get_city(self, city_id):
    """
    Retrieve a single city from postgres
    :param city_id: the id of the city to get
    """
    return self._city_repo.get_by_id(city_id)

  def get_city_by_name(self, city_name):
    """
    Retrieve a single city from postgres
    :param city_name: the name of the city to get
    """
    return self._city_repo.get_by_name(city_name)

  def get_city_by_user(self, user_id):
    """
    Retrieve cities created by user
    :param user_id: the id of the user
    """
    return self._city_repo.get_by_user(user_id)

  def get_hp_simulation(self, hp_sim_id: int):
    """
    Retrieve a single heat pump simulation from postgres
    :param hp_sim_id: the id of the heat pump to get
    """
    return self._hp_simulation_repo.get_by_id(hp_sim_id)

  def get_hp_simulation_by_city(self, city_id: int):
    """
    Retrieve a single city from postgres
    :param city_id: the id of the city
    """
    return self._hp_simulation_repo.get_by_city(city_id)
