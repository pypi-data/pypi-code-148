"""
ConstructionFactory (before PhysicsFactory) retrieve the specific construction module for the given region
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""
from pathlib import Path
from imports.construction.us_physics_parameters import UsPhysicsParameters


class ConstructionFactory:
  """
  PhysicsFactor class
  """
  def __init__(self, handler, city, base_path=None):
    if base_path is None:
      base_path = Path(Path(__file__).parent.parent / 'data/construction')
    self._handler = '_' + handler.lower().replace(' ', '_')
    self._city = city
    self._base_path = base_path

  def _nrel(self):
    """
    Enrich the city by using NREL information
    """
    UsPhysicsParameters(self._city, self._base_path).enrich_buildings()
    self._city.level_of_detail.construction = 2

  def enrich(self):
    """
    Enrich the city given to the class using the class given handler
    :return: None
    """
    getattr(self, self._handler, lambda: None)()

  def enrich_debug(self):
    """
    Enrich the city given to the class using the class given handler
    :return: None
    """
    UsPhysicsParameters(self._city, self._base_path).enrich_buildings()