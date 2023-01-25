"""
Level of detail module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""


class LevelOfDetail:
  """
  Level of detail for the city class
  """
  def __init__(self):
    self._geometry = None
    self._construction = None
    self._usage = None

  @property
  def geometry(self):
    """
    Get the city minimal geometry level of detail from 0 to 4
    :return: int
    """
    return self._geometry

  @geometry.setter
  def geometry(self, value):
    """
    Set the city minimal geometry level of detail from 0 to 4
    """
    self._geometry = value

  @property
  def construction(self):
    """
    Get the city minimal construction level of detail, 1 or 2
    :return: int
    """
    return self._construction

  @construction.setter
  def construction(self, value):
    """
    Set the city minimal construction level of detail, 1 or 2
    """
    self._construction = value

  @property
  def usage(self):
    """
    Get the city minimal usage level of detail, 1 or 2
    :return: int
    """
    return self._usage

  @usage.setter
  def usage(self, value):
    """
    Set the city minimal usage level of detail, 1 or 2
    """
    self._usage = value
