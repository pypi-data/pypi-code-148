"""
HftUsageParameters model the usage properties
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import sys

from imports.geometry.helpers.geometry_helper import GeometryHelper
from imports.usage.hft_usage_interface import HftUsageInterface
from imports.usage.helpers.usage_helper import UsageHelper


class HftUsageParameters(HftUsageInterface):
  """
  HftUsageParameters class
  """
  def __init__(self, city, base_path):
    super().__init__(base_path, 'de_library.xml')
    self._city = city

  def enrich_buildings(self):
    """
    Returns the city with the usage parameters assigned to the buildings
    :return:
    """
    city = self._city
    for building in city.buildings:
      usage = GeometryHelper().libs_usage_from_libs_function(building.function)
      try:
        archetype = self._search_archetype(usage)
      except KeyError:
        sys.stderr.write(f'Building {building.name} has unknown archetype for building function:'
                         f' {building.function}, that assigns building usage as '
                         f'{GeometryHelper().libs_usage_from_libs_function(building.function)}\n')
        return

      for internal_zone in building.internal_zones:
          libs_usage = GeometryHelper().libs_usage_from_libs_function(building.function)
          usage_zone = self._assign_values(UsageHelper().hft_from_libs_usage(libs_usage), archetype)
          usage_zone.percentage = 1
          internal_zone.usage_zones = [usage_zone]
