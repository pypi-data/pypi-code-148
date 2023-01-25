"""
DBFactory performs database create, delete and update operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project CoderPeter Yefi peteryefi@gmail.com
"""
from hub.persistence import CityRepo
from hub.persistence import HeatPumpSimulationRepo
from typing import Dict
from hub.city_model_structure.city import City


class DBFactory:
  """
  DBFactory class
  """

  def __init__(self, db_name, dotenv_path, app_env):
    self._city_repo = CityRepo(db_name=db_name, dotenv_path=dotenv_path, app_env=app_env)
    self._hp_simulation_repo = HeatPumpSimulationRepo(db_name=db_name, dotenv_path=dotenv_path, app_env=app_env)

  def persist_city(self, user_id: int, city: City):
    """
    Persist city into postgres database
    """
    return self._city_repo.insert(city, user_id)

  def update_city(self, city_id, city):
    """
   Update an existing city in postgres database
   :param city_id: the id of the city to update
   :param city: the updated city object
    """
    return self._city_repo.update(city_id, city)

  def delete_city(self, city_id):
    """
    Deletes a single city from postgres
    :param city_id: the id of the city to get
    """
    self._city_repo.delete_city(city_id)

  def persist_hp_simulation(self, hp_simulation_data: Dict, city_id: int):
    """
    Persist heat pump simulation results
    :param hp_simulation_data: the simulation results
    :param city_id: the city object used in running the simulation
    :return: HeatPumpSimulation object
    """
    return self._hp_simulation_repo.insert(hp_simulation_data, city_id)

  def delete_hp_simulation(self, hp_sim_id):
    """
    Deletes a single heat pump simulation from postgres
    :param hp_sim_id: the id of the heat pump simulation to get
    """
    self._hp_simulation_repo.delete_hp_simulation(hp_sim_id)
