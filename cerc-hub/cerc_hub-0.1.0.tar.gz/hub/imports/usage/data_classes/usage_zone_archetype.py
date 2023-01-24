"""
UsageZoneArchetype stores usage information by usage type
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

from typing import List
from imports.usage.data_classes.hft_internal_gains_archetype import HftInternalGainsArchetype


class UsageZoneArchetype:
  """
  UsageZoneArchetype class
  """
  def __init__(self, usage=None, internal_gains=None, hours_day=None, days_year=None,
               electrical_app_average_consumption_sqm_year=None, mechanical_air_change=None, occupancy=None,
               lighting=None, appliances=None):
    self._usage = usage
    self._internal_gains = internal_gains
    self._hours_day = hours_day
    self._days_year = days_year
    self._electrical_app_average_consumption_sqm_year = electrical_app_average_consumption_sqm_year
    self._mechanical_air_change = mechanical_air_change
    self._occupancy = occupancy
    self._lighting = lighting
    self._appliances = appliances

  @property
  def internal_gains(self) -> List[HftInternalGainsArchetype]:
    """
    Get usage zone internal gains from not detailed heating source in W/m2
    :return: [InternalGain]
    """
    return self._internal_gains

  @property
  def hours_day(self):
    """
    Get usage zone usage hours per day
    :return: float
    """
    return self._hours_day

  @property
  def days_year(self):
    """
    Get usage zone usage days per year
    :return: float
    """
    return self._days_year

  @property
  def mechanical_air_change(self):
    """
    Set usage zone mechanical air change in air change per hour (ACH)
    :return: float
    """
    return self._mechanical_air_change

  @property
  def usage(self):
    """
    Get usage zone usage
    :return: str
    """
    return self._usage

  @property
  def electrical_app_average_consumption_sqm_year(self):
    """
    Get average consumption of electrical appliances in Joules per m2 and year (J/m2yr)
    :return: float
    """
    return self._electrical_app_average_consumption_sqm_year

  @property
  def occupancy(self):
    """
    Get occupancy data
    :return: Occupancy
    """
    return self._occupancy

  @property
  def lighting(self):
    """
    Get lighting data
    :return: Lighting
    """
    return self._lighting

  @property
  def appliances(self):
    """
    Get appliances data
    :return: Appliances
    """
    return self._appliances
