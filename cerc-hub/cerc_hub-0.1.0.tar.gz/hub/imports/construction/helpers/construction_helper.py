"""
Construction helper
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import sys
from helpers import constants as cte


class ConstructionHelper:
  """
  Construction helper
  """
  # NREL
  _function_to_nrel = {
    cte.RESIDENTIAL: 'residential',
    cte.SINGLE_FAMILY_HOUSE: 'residential',
    cte.MULTI_FAMILY_HOUSE: 'residential',
    cte.ROW_HOSE: 'residential',
    cte.MID_RISE_APARTMENT: 'midrise apartment',
    cte.HIGH_RISE_APARTMENT: 'high-rise apartment',
    cte.SMALL_OFFICE: 'small office',
    cte.MEDIUM_OFFICE: 'medium office',
    cte.LARGE_OFFICE: 'large office',
    cte.PRIMARY_SCHOOL: 'primary school',
    cte.SECONDARY_SCHOOL: 'secondary school',
    cte.STAND_ALONE_RETAIL: 'stand-alone retail',
    cte.HOSPITAL: 'hospital',
    cte.OUT_PATIENT_HEALTH_CARE: 'outpatient healthcare',
    cte.STRIP_MALL: 'strip mall',
    cte.SUPERMARKET: 'supermarket',
    cte.WAREHOUSE: 'warehouse',
    cte.QUICK_SERVICE_RESTAURANT: 'quick service restaurant',
    cte.FULL_SERVICE_RESTAURANT: 'full service restaurant',
    cte.SMALL_HOTEL: 'small hotel',
    cte.LARGE_HOTEL: 'large hotel'
  }

  _nrel_standards = {
    'ASHRAE Std189': 1,
    'ASHRAE 90.1_2004': 2
  }
  _reference_city_to_nrel_climate_zone = {
    'Miami': 'ASHRAE_2004:1A',
    'Houston': 'ASHRAE_2004:2A',
    'Phoenix': 'ASHRAE_2004:2B',
    'Atlanta': 'ASHRAE_2004:3A',
    'Los Angeles': 'ASHRAE_2004:3B',
    'Las Vegas': 'ASHRAE_2004:3B',
    'San Francisco': 'ASHRAE_2004:3C',
    'Baltimore': 'ASHRAE_2004:4A',
    'Albuquerque': 'ASHRAE_2004:4B',
    'Seattle': 'ASHRAE_2004:4C',
    'Chicago': 'ASHRAE_2004:5A',
    'Boulder': 'ASHRAE_2004:5B',
    'Minneapolis': 'ASHRAE_2004:6A',
    'Helena': 'ASHRAE_2004:6B',
    'Duluth': 'ASHRAE_2004:7A',
    'Fairbanks': 'ASHRAE_2004:8A'
  }
  nrel_window_types = [cte.WINDOW, cte.DOOR, cte.SKYLIGHT]

  nrel_construction_types = {
    cte.WALL: 'exterior wall',
    cte.INTERIOR_WALL: 'interior wall',
    cte.GROUND_WALL: 'ground wall',
    cte.GROUND: 'exterior slab',
    cte.ATTIC_FLOOR: 'attic floor',
    cte.INTERIOR_SLAB: 'interior slab',
    cte.ROOF: 'roof'
  }

  @staticmethod
  def nrel_from_libs_function(function):
    """
    Get NREL function from the given internal function key
    :param function: str
    :return: str
    """
    try:
      return ConstructionHelper._function_to_nrel[function]
    except KeyError:
      sys.stderr.write('Error: keyword not found.\n')

  @staticmethod
  def yoc_to_nrel_standard(year_of_construction):
    """
    Year of construction to NREL standard
    :param year_of_construction: int
    :return: str
    """
    if int(year_of_construction) < 2009:
      standard = 'ASHRAE 90.1_2004'
    else:
      standard = 'ASHRAE 189.1_2009'
    return standard

  @staticmethod
  def city_to_reference_city(city):
    """
    City name to reference city
    :param city: str
    :return: str
    """
    # todo: Dummy function that needs to be implemented
    reference_city = 'Baltimore'
    if city is not None:
      reference_city = 'Baltimore'
    return reference_city

  @staticmethod
  def city_to_nrel_climate_zone(city):
    """
    City name to NREL climate zone
    :param city: str
    :return: str
    """
    reference_city = ConstructionHelper.city_to_reference_city(city)
    return ConstructionHelper._reference_city_to_nrel_climate_zone[reference_city]