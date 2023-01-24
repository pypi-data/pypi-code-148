"""
ThermalOpeningArchetype stores thermal openings information, complementing the BuildingArchetype class
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""


class ThermalOpeningArchetype:
  """
  ThermalOpeningArchetype class
  """
  def __init__(self, conductivity=None, frame_ratio=None, g_value=None, thickness=None,
               back_side_solar_transmittance_at_normal_incidence=None,
               front_side_solar_transmittance_at_normal_incidence=None, overall_u_value=None,
               openable_ratio=None, inside_emissivity=None, alpha_coefficient=None, radiative_coefficient=None,
               construction_name=None):
    self._conductivity = conductivity
    self._frame_ratio = frame_ratio
    self._g_value = g_value
    self._thickness = thickness
    self._back_side_solar_transmittance_at_normal_incidence = back_side_solar_transmittance_at_normal_incidence
    self._front_side_solar_transmittance_at_normal_incidence = front_side_solar_transmittance_at_normal_incidence
    self._overall_u_value = overall_u_value
    self._openable_ratio = openable_ratio
    self._inside_emissivity = inside_emissivity
    self._alpha_coefficient = alpha_coefficient
    self._radiative_coefficient = radiative_coefficient
    self._construction_name = construction_name

  @property
  def conductivity(self):
    """
    Get conductivity in W/mK
    :return: float
    """
    return self._conductivity

  @property
  def frame_ratio(self):
    """
    Get frame ratio
    :return: float
    """
    return self._frame_ratio

  @property
  def g_value(self):
    """
    Get g-value, also called shgc
    :return: float
    """
    return self._g_value

  @property
  def thickness(self):
    """
    Get thickness in meters
    :return: float
    """
    return self._thickness

  @property
  def back_side_solar_transmittance_at_normal_incidence(self):
    """
    Get back side solar transmittance at normal incidence
    :return: float
    """
    return self._back_side_solar_transmittance_at_normal_incidence

  @property
  def front_side_solar_transmittance_at_normal_incidence(self):
    """
    Get front side solar transmittance at normal incidence
    :return: float
    """
    return self._front_side_solar_transmittance_at_normal_incidence

  @property
  def overall_u_value(self):
    """
    Get overall U-value in W/m2K
    :return: float
    """
    return self._overall_u_value

  @property
  def openable_ratio(self):
    """
    Get openable ratio
    :return: float
    """
    return self._openable_ratio

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

  @property
  def construction_name(self):
    """
    Get thermal opening construction name
    """
    return self._construction_name

  @construction_name.setter
  def construction_name(self, value):
    """
    Set thermal opening construction name
    """
    self._construction_name = value
