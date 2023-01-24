"""
UsageFactory retrieve the specific usage module for the given region
This factory can only be called after calling the construction factory so the thermal zones are created.
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
from pathlib import Path
from imports.usage.hft_usage_parameters import HftUsageParameters
from imports.usage.comnet_usage_parameters import ComnetUsageParameters


class UsageFactory:
  """
  UsageFactory class
  """
  def __init__(self, handler, city, base_path=None):
    if base_path is None:
      base_path = Path(Path(__file__).parent.parent / 'data/usage')
    self._handler = '_' + handler.lower().replace(' ', '_')
    self._city = city
    self._base_path = base_path

  def _hft(self):
    """
    Enrich the city with HFT usage library
    """
    self._city.level_of_detail.usage = 2
    return HftUsageParameters(self._city, self._base_path).enrich_buildings()

  def _comnet(self):
    """
    Enrich the city with COMNET usage library
    """
    self._city.level_of_detail.usage = 2
    return ComnetUsageParameters(self._city, self._base_path).enrich_buildings()

  def enrich(self):
    """
    Enrich the city given to the class using the usage factory given handler
    :return: None
    """
    getattr(self, self._handler, lambda: None)()
