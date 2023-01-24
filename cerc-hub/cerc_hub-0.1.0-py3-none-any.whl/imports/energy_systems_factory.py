"""
EnergySystemsFactory retrieve the energy system module for the given region
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete pilar.monsalvete@concordi.
Code contributors: Peter Yefi peteryefi@gmail.com
"""
from pathlib import Path
from imports.energy_systems.air_source_hp_parameters import AirSourceHeatPumpParameters
from imports.energy_systems.water_to_water_hp_parameters import WaterToWaterHPParameters


class EnergySystemsFactory:
  """
  EnergySystemsFactory class
  """

  def __init__(self, handler, city, base_path=None):
    if base_path is None:
      base_path = Path(Path(__file__).parent.parent / 'data/energy_systems')
    self._handler = '_' + handler.lower().replace(' ', '_')
    self._city = city
    self._base_path = base_path

  def _air_source_hp(self):
    """
    Enrich the city by using xlsx heat pump information
    """
    AirSourceHeatPumpParameters(self._city, self._base_path).enrich_city()

  def _water_to_water_hp(self):
    """
    Enrich the city by using water to water heat pump information
    """
    WaterToWaterHPParameters(self._city, self._base_path).enrich_city()

  def enrich(self):
    """
    Enrich the city given to the class using the class given handler
    :return: None
    """
    getattr(self, self._handler, lambda: None)()
