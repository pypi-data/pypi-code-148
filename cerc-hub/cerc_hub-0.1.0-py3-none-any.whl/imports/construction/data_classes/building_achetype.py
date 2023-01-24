"""
BuildingArchetype stores construction information by building archetypes
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
from typing import List
from imports.construction.data_classes.thermal_boundary_archetype import ThermalBoundaryArchetype


class BuildingArchetype:
  """
  BuildingArchetype class
  """
  def __init__(self, archetype_keys, average_storey_height, storeys_above_ground, effective_thermal_capacity,
               additional_thermal_bridge_u_value, indirectly_heated_area_ratio, infiltration_rate_system_off,
               infiltration_rate_system_on, thermal_boundary_archetypes):
    self._archetype_keys = archetype_keys
    self._average_storey_height = average_storey_height
    self._storeys_above_ground = storeys_above_ground
    self._effective_thermal_capacity = effective_thermal_capacity
    self._additional_thermal_bridge_u_value = additional_thermal_bridge_u_value
    self._indirectly_heated_area_ratio = indirectly_heated_area_ratio
    self._infiltration_rate_system_off = infiltration_rate_system_off
    self._infiltration_rate_system_on = infiltration_rate_system_on
    self._thermal_boundary_archetypes = thermal_boundary_archetypes

  @property
  def archetype_keys(self) -> {}:
    """
    Get keys that define the archetype
    :return: dictionary
    """
    return self._archetype_keys

  @property
  def average_storey_height(self):
    """
    Get archetype's building storey height in meters
    :return: float
    """
    return self._average_storey_height

  @property
  def storeys_above_ground(self):
    """
    Get archetype's building storey height in meters
    :return: float
    """
    return self._storeys_above_ground

  @property
  def effective_thermal_capacity(self):
    """
    Get archetype's effective thermal capacity in J/m2K
    :return: float
    """
    return self._effective_thermal_capacity

  @property
  def additional_thermal_bridge_u_value(self):
    """
    Get archetype's additional U value due to thermal bridges per area of shell in W/m2K
    :return: float
    """
    return self._additional_thermal_bridge_u_value

  @property
  def indirectly_heated_area_ratio(self):
    """
    Get archetype's indirectly heated area ratio
    :return: float
    """
    return self._indirectly_heated_area_ratio

  @property
  def infiltration_rate_system_off(self):
    """
    Get archetype's infiltration rate when conditioning systems OFF in air changes per hour (ACH)
    :return: float
    """
    return self._infiltration_rate_system_off

  @property
  def infiltration_rate_system_on(self):
    """
    Get archetype's infiltration rate when conditioning systems ON in air changes per hour (ACH)
    :return: float
    """
    return self._infiltration_rate_system_on

  @property
  def thermal_boundary_archetypes(self) -> List[ThermalBoundaryArchetype]:
    """
    Get thermal boundary archetypes associated to the building archetype
    :return: list of boundary archetypes
    """
    return self._thermal_boundary_archetypes
