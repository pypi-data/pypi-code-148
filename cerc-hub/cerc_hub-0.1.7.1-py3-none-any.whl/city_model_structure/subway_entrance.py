"""
Subway entrance module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
from hub.city_model_structure.city_object import CityObject


class SubwayEntrance(CityObject):
  """
  SubwayEntrance(CityObject) class
  """
  def __init__(self, name, latitude, longitude):
    super().__init__(name, 0)
    self._name = name
    self._latitude = latitude
    self._longitude = longitude
    self._type = 'subway_entrance'

  @property
  def latitude(self):
    # todo: to be defined the spacial point and the units
    """
    Get latitude
    :return: float
    """
    return self._latitude

  @property
  def longitude(self):
    # todo: to be defined the spacial point and the units
    """
    Get longitude
    :return: float
    """
    return self._longitude

  @property
  def name(self):
    """
    Get name
    :return: str
    """
    return self._name
