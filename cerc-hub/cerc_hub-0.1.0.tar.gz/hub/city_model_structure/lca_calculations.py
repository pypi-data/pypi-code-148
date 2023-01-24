"""
LifeCycleAssessment retrieve the specific Life Cycle Assessment module for the given region
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Atiya atiya.atiya@mail.concordia.ca
"""
from city_model_structure.machine import Machine


class LcaCalculations:
  """
  LCA Calculations class
  """
  def emission_disposal_machines(self, ):
    return Machine.work_efficiency * Machine.energy_consumption_rate * Machine.carbon_emission_factor

  def emission_transportation(self, weight, distance ):
    return weight * distance * Machine.energy_consumption_rate * Machine.carbon_emission_factor



