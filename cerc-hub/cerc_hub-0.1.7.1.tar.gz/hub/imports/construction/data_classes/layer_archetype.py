"""
LayerArchetype stores layer and materials information, complementing the BuildingArchetype class
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""


class LayerArchetype:
  """
  LayerArchetype class
  """
  def __init__(self, name, solar_absorptance, thermal_absorptance, visible_absorptance, thickness=None,
               conductivity=None, specific_heat=None, density=None,  no_mass=False, thermal_resistance=None):
    self._thickness = thickness
    self._conductivity = conductivity
    self._specific_heat = specific_heat
    self._density = density
    self._solar_absorptance = solar_absorptance
    self._thermal_absorptance = thermal_absorptance
    self._visible_absorptance = visible_absorptance
    self._no_mass = no_mass
    self._name = name
    self._thermal_resistance = thermal_resistance

  @property
  def thickness(self):
    """
    Get thickness in meters
    :return: float
    """
    return self._thickness

  @property
  def conductivity(self):
    """
    Get conductivity in W/mK
    :return: float
    """
    return self._conductivity

  @property
  def specific_heat(self):
    """
    Get specific heat in J/kgK
    :return: float
    """
    return self._specific_heat

  @property
  def density(self):
    """
    Get density in kg/m3
    :return: float
    """
    return self._density

  @property
  def solar_absorptance(self):
    """
    Get solar absorptance
    :return: float
    """
    return self._solar_absorptance

  @property
  def thermal_absorptance(self):
    """
    Get thermal absorptance
    :return: float
    """
    return self._thermal_absorptance

  @property
  def visible_absorptance(self):
    """
    Get visible absorptance
    :return: float
    """
    return self._visible_absorptance

  @property
  def no_mass(self) -> bool:
    """
    Get no mass flag
    :return: Boolean
    """
    return self._no_mass

  @property
  def name(self):
    """
    Get name
    :return: str
    """
    return self._name

  @property
  def thermal_resistance(self):
    """
    Get thermal resistance in m2K/W
    :return: float
    """
    return self._thermal_resistance
