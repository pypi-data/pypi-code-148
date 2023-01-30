"""
Heat pump simulation repository with database CRUD operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""

from hub.persistence import BaseRepo, CityRepo
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from hub.persistence.models import HeatPumpSimulation
from typing import Union, Dict
from hub.hub_logger import logger


class HeatPumpSimulationRepo(BaseRepo):
  _instance = None

  def __init__(self, db_name, dotenv_path, app_env):
    super().__init__(db_name, dotenv_path, app_env)
    self._city_repo = CityRepo(db_name, dotenv_path, app_env)

  def __new__(cls, db_name, dotenv_path, app_env):
    """
    Implemented for a singleton pattern
    """
    if cls._instance is None:
      cls._instance = super(HeatPumpSimulationRepo, cls).__new__(cls)
    return cls._instance

  def insert(self, hp_sim_data: Dict, city_id: int) -> Union[HeatPumpSimulation, Dict]:
    """
    Inserts the results of heat pump simulation
    :param hp_sim_data: dictionary with heatpump the simulation inputs and output
    :param city_id: the city that was used in running the simulation
    :return: HeatPumpSimulation
    """

    city = self._city_repo.get_by_id(city_id)
    if city is None:
      return {'message': 'city not found in database'}

    try:
      hp_simulation = HeatPumpSimulation(city_id, hp_sim_data["HourlyElectricityDemand"],
                                         hp_sim_data["DailyElectricityDemand"], hp_sim_data["MonthlyElectricityDemand"],
                                         hp_sim_data["DailyFossilFuelConsumption"],
                                         hp_sim_data["MonthlyFossilFuelConsumption"])
      hp_simulation.city_id = city_id
      hp_simulation.end_year = hp_sim_data["EndYear"]
      hp_simulation.start_year = hp_sim_data["StartYear"]
      hp_simulation.max_demand_storage_hour = hp_sim_data["HoursOfStorageAtMaxDemand"]
      hp_simulation.max_hp_energy_input = hp_sim_data["MaximumHPEnergyInput"]
      hp_simulation.building_supply_temp = hp_sim_data["BuildingSuppTemp"]
      hp_simulation.temp_difference = hp_sim_data["TemperatureDifference"]
      hp_simulation.fuel_lhv = hp_sim_data["FuelLHV"]
      hp_simulation.fuel_price = hp_sim_data["FuelPrice"]
      hp_simulation.fuel_efficiency = hp_sim_data["FuelEF"]
      hp_simulation.fuel_density = hp_sim_data["FuelDensity"]
      hp_simulation.hp_supply_temp = hp_sim_data["HPSupTemp"]
      hp_simulation.simulation_type = hp_sim_data["SimulationType"]
      hp_simulation.heat_pump_model = hp_sim_data["HeatPumpModel"]
      hp_simulation.heat_pump_type = hp_sim_data["HeatPumpType"]

      # Persist heat pump simulation data
      self.session.add(hp_simulation)
      self.session.flush()
      self.session.commit()
      return hp_simulation
    except SQLAlchemyError as err:
      logger.error(f'Error while saving heat pump simulation data: {err}')
    except KeyError as err:
      logger.error(f'A required field is missing in your heat pump simulation dictionary: {err}')

  def get_by_id(self, hp_simulation_id: int) -> HeatPumpSimulation:
    """
    Fetches heat pump simulation data
    :param hp_simulation_id: the city id
    :return: a HeatPumpSimulation
    """
    try:
      return self.session.execute(select(HeatPumpSimulation).where(HeatPumpSimulation.id == hp_simulation_id)).first()[
        0]
    except SQLAlchemyError as err:
      logger.error(f'Error while fetching city: {err}')

  def get_by_city(self, city_id: int) -> [HeatPumpSimulation]:
    """
    Fetch heat pump simulation results by city
    :param city_id: the name of the building
    :return: [HeatPumpSimulation] with the provided name
    """
    try:
      result_set = self.session.execute(select(HeatPumpSimulation).where(HeatPumpSimulation.city_id == city_id))
      return [sim_data[0] for sim_data in result_set]
    except SQLAlchemyError as err:
      logger.error(f'Error while fetching city by name: {err}')

  def delete_hp_simulation(self, hp_simulation_id: int):
    """
    Deletes a heat pump simulation results
    :param hp_simulation_id: the heat pump simulation results id
    :return:
    """
    try:
      self.session.query(HeatPumpSimulation).filter(HeatPumpSimulation.id == hp_simulation_id).delete()
      self.session.commit()
    except SQLAlchemyError as err:
      logger.error(f'Error while fetching city: {err}')
