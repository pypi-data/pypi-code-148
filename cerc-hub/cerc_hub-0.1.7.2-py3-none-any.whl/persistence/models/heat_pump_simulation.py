"""
Model representation of the results of heat pump simulation
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""

from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy import Enum, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from hub.persistence.db_config import Base
import enum
import datetime


class SimulationTypes(enum.Enum):
  Parallel = 'PARALLEL'
  Series = 'SERIES'


class HeatPumpTypes(enum.Enum):
  Air = 'Air Source'
  Water = 'Water to Water'


class HeatPumpSimulation(Base):
  """A model representation of a building

        Attributes:
            city_id,  A reference to the city which was used to run this simulation.
            hourly_electricity_demand, A JSON object that has hours and their electricity demand
            daily_electricity_demand, A JSON object that has days and their electricity demand
            monthly_electricity_demand, A JSON object that has months and their electricity demand
            daily_fossil_fuel_consumption, A JSON object that has days and fossil fuel consumption
            monthly_fossil_fuel_consumption, A JSON object that has months and fossil fuel consumption
            heat_pump_type, Water or air heat pump
            simulation_type, The type of heat pump simulation (parallel or series)
            heat_pump_model, The model of the heat pump (either water to water or air source)
            start year, HP simulation start year
            end year, HP simulation end year
            max_hp_energy_input, Maximum heat pump energy input
            max_demand_storage_hour, Hours of storage at maximum demand
            building_supply_temp, building supply temperature
            temp_difference, Difference in HP and building supply temperatures
            fuel_lhv, The lower heating value of fuel
            fuel_price, The price of fuel
            fuel_efficiency, the efficiency of fuel
            fuel_density, the density of fuel
            hp_supply_temp, supply temperature of heat pump


    """
  __tablename__ = "heat_pump_simulation"
  id = Column(Integer, Sequence('hp_simulation_id_seq'), primary_key=True)
  city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
  daily_electricity_demand = Column(JSONB, nullable=False)
  hourly_electricity_demand = Column(JSONB, nullable=False)
  daily_fossil_fuel_consumption = Column(JSONB, nullable=False)
  monthly_fossil_fuel_consumption = Column(JSONB, nullable=False)
  monthly_electricity_demand = Column(JSONB, nullable=False)
  heat_pump_type = Column(Enum(HeatPumpTypes), nullable=False)
  simulation_type = Column(Enum(SimulationTypes), nullable=False)
  heat_pump_model = Column(String, nullable=False)
  start_year = Column(Integer, nullable=False)
  end_year = Column(Integer, nullable=False)
  max_hp_energy_input = Column(Float, nullable=False)
  max_demand_storage_hour = Column(Float, nullable=False)
  building_supply_temp = Column(Float, nullable=False)
  temp_difference = Column(Float, nullable=False)
  fuel_lhv = Column(Float, nullable=False)
  fuel_price = Column(Float, nullable=False)
  fuel_efficiency = Column(Float, nullable=False)
  fuel_density = Column(Float, nullable=False)
  hp_supply_temp = Column(Float, nullable=False)
  created = Column(DateTime, default=datetime.datetime.utcnow)

  def __init__(self, city_id, hourly_elec_demand, daily_elec_demand, monthly_elec_demand, daily_fossil, monthly_fossil):
    self.city_id = city_id
    self.hourly_electricity_demand = hourly_elec_demand
    self.daily_electricity_demand = daily_elec_demand
    self.monthly_electricity_demand = monthly_elec_demand
    self.daily_fossil_fuel_consumption = daily_fossil
    self.monthly_fossil_fuel_consumption = monthly_fossil
