"""
SensorsFactory retrieve sensors information
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
from pathlib import Path


class SensorsFactory:
  """
  UsageFactory class
  """
  def __init__(self, handler, city, end_point, base_path=None):
    if base_path is None:
      base_path = Path(Path(__file__).parent.parent / 'data/sensors')
    self._handler = '_' + handler.lower().replace(' ', '_')
    self._city = city
    self._end_point = end_point
    self._base_path = base_path

  def _cec(self):
    """
    Enrich the city by using concordia energy consumption sensors as data source
    """
    raise NotImplementedError('need to be reimplemented')

  def _cgf(self):
    """
    Enrich the city by using concordia gas flow sensors as data source
    """
    raise NotImplementedError('need to be reimplemented')

  def _ct(self):
    """
    Enrich the city by using concordia temperature sensors as data source
    """
    raise NotImplementedError('need to be reimplemented')

  def enrich(self):
    """
    Enrich the city given to the class using the given sensor handler
    :return: None
    """
    getattr(self, self._handler, lambda: None)()
