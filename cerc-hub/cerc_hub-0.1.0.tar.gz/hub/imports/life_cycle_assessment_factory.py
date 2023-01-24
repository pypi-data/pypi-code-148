"""
ConstructionFactory (before PhysicsFactory) retrieve the specific construction module for the given region
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Atiya atiya.atiya@mail.concordia.ca
"""

from pathlib import Path
from imports.life_cycle_assessment.lca_fuel import LcaFuel
from imports.life_cycle_assessment.lca_vehicle import LcaVehicle
from imports.life_cycle_assessment.lca_machine import LcaMachine
from imports.life_cycle_assessment.lca_material import LcaMaterial


class LifeCycleAssessment:
  """
  Life cicle analize factory class
  """
  def __init__(self, handler, city, base_path=None):
    if base_path is None:
      base_path = Path(Path(__file__).parent.parent / 'data/life_cycle_assessment')
    self._handler = '_' + handler.lower().replace(' ', '_')
    self._city = city
    self._base_path = base_path

  def _fuel(self):
    """
    Enrich the city by adding the fuel carbon information
    """
    LcaFuel(self._city, self._base_path).enrich()

  def _vehicle(self):
    """
    Enrich the city by adding the vehicle carbon information
    """
    LcaVehicle(self._city, self._base_path).enrich()

  def _machine(self):
    """
    Enrich the city by adding the machine carbon information
    """
    LcaMachine(self._city, self._base_path).enrich()

  def _material(self):
    """
    Enrich the city by adding the material carbon information
    """
    LcaMaterial(self._city, self._base_path).enrich()

  def enrich(self):
    """
    Enrich the city given to the class using the class given handler
    :return: None
    """
    getattr(self, self._handler, lambda: None)()
