"""
ThermalBoundaryArchetype stores thermal boundaries information, complementing the BuildingArchetype class
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
from typing import List

from imports.construction.data_classes.layer_archetype import LayerArchetype
from imports.construction.data_classes.thermal_opening_archetype import ThermalOpeningArchetype


class ThermalBoundaryArchetype:
  """
  ThermalBoundaryArchetype class
  """
  def __init__(self, boundary_type, window_ratio, construction_name, layers, thermal_opening,
               outside_solar_absorptance=None, outside_thermal_absorptance=None, outside_visible_absorptance=None,
               overall_u_value=None, shortwave_reflectance=None, inside_emissivity=None, alpha_coefficient=None,
               radiative_coefficient=None):
    self._boundary_type = boundary_type
    self._outside_solar_absorptance = outside_solar_absorptance
    self._outside_thermal_absorptance = outside_thermal_absorptance
    self._outside_visible_absorptance = outside_visible_absorptance
    self._window_ratio = window_ratio
    self._construction_name = construction_name
    self._overall_u_value = overall_u_value
    self._layers = layers
    self._thermal_opening_archetype = thermal_opening
    self._shortwave_reflectance = shortwave_reflectance
    self._inside_emissivity = inside_emissivity
    self._alpha_coefficient = alpha_coefficient
    self._radiative_coefficient = radiative_coefficient

  @property
  def boundary_type(self):
    """
    Get type
    :return: str
    """
    return self._boundary_type

  @property
  def outside_solar_absorptance(self):
    """
    Get outside solar absorptance
    :return: float
    """
    return self._outside_solar_absorptance

  @property
  def outside_thermal_absorptance(self):
    """
    Get outside thermal absorptance
    :return: float
    """
    return self._outside_thermal_absorptance

  @property
  def outside_visible_absorptance(self):
    """
    Get outside visible absorptance
    :return: float
    """
    return self._outside_visible_absorptance

  @property
  def window_ratio(self):
    """
    Get window ratio
    :return: float
    """
    return self._window_ratio

  @property
  def construction_name(self):
    """
    Get construction name
    :return: str
    """
    return self._construction_name

  @property
  def layers(self) -> List[LayerArchetype]:
    """
    Get layers
    :return: [NrelLayerArchetype]
    """
    return self._layers

  @property
  def thermal_opening_archetype(self) -> ThermalOpeningArchetype:
    """
    Get thermal opening archetype
    :return: ThermalOpeningArchetype
    """
    return self._thermal_opening_archetype

  @property
  def overall_u_value(self):
    """
    Get overall U-value in W/m2K
    :return: float
    """
    return self._overall_u_value

  @property
  def shortwave_reflectance(self):
    """
    Get shortwave reflectance
    :return: float
    """
    return self._shortwave_reflectance

  @property
  def inside_emissivity(self):
    """
    Get emissivity inside
    :return: float
    """
    return self._inside_emissivity

  @property
  def alpha_coefficient(self):
    """
    Get alpha coefficient
    :return: float
    """
    return self._alpha_coefficient

  @property
  def radiative_coefficient(self):
    """
    Get radiative coefficient
    :return: float
    """
    return self._radiative_coefficient
