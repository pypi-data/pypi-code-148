"""
weather helper
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import math
import hub.helpers.constants as cte


class Weather:
  """
  Weather class
  """

  @staticmethod
  def sky_temperature(ambient_temperature):
    """
    Get sky temperature from ambient temperature in Celsius
    :return: float
    """
    # Swinbank - Source sky model approximation(1963) based on cloudiness statistics(32 %) in United States
    # ambient temperatures( in °C)
    # sky temperatures( in °C)
    values = []
    for temperature in ambient_temperature:
      value = 0.037536 * math.pow((temperature + cte.KELVIN), 1.5) \
              + 0.32 * (temperature + cte.KELVIN) - cte.KELVIN
      values.append(value)
    return values
