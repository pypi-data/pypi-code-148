"""
HftInternalGainsArchetype stores internal gains information, complementing the HftUsageZoneArchetype class
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""


class HftInternalGainsArchetype:
  """
  HftInternalGainsArchetype class
  """
  def __init__(self, internal_gains_type=None, average_internal_gain=None, convective_fraction=None, \
               radiative_fraction=None, latent_fraction=None):
    self._type = internal_gains_type
    self._average_internal_gain = average_internal_gain
    self._convective_fraction = convective_fraction
    self._radiative_fraction = radiative_fraction
    self._latent_fraction = latent_fraction

  @property
  def type(self):
    """
    Get internal gains type
    :return: string
    """
    return self._type

  @type.setter
  def type(self, value):
    """
    Set internal gains type
    :param value: string
    """
    self._type = value

  @property
  def average_internal_gain(self):
    """
    Get internal gains average internal gain in W/m2
    :return: float
    """
    return self._average_internal_gain

  @property
  def convective_fraction(self):
    """
    Get internal gains convective fraction
    :return: float
    """
    return self._convective_fraction

  @property
  def radiative_fraction(self):
    """
    Get internal gains radiative fraction
    :return: float
    """
    return self._radiative_fraction

  @property
  def latent_fraction(self):
    """
    Get internal gains latent fraction
    :return: float
    """
    return self._latent_fraction
