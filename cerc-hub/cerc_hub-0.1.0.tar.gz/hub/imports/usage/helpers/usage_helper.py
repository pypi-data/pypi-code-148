"""
Usage helper
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import sys
import helpers.constants as cte


class UsageHelper:
  """
  Usage helper class
  """
  _usage_to_hft = {
    cte.RESIDENTIAL: 'residential',
    cte.SINGLE_FAMILY_HOUSE: 'Single family house',
    cte.MULTI_FAMILY_HOUSE: 'Multi-family house',
    cte.EDUCATION: 'education',
    cte.SCHOOL_WITHOUT_SHOWER: 'school without shower',
    cte.SCHOOL_WITH_SHOWER: 'school with shower',
    cte.RETAIL_SHOP_WITHOUT_REFRIGERATED_FOOD: 'retail',
    cte.RETAIL_SHOP_WITH_REFRIGERATED_FOOD: 'retail shop / refrigerated food',
    cte.HOTEL: 'hotel',
    cte.HOTEL_MEDIUM_CLASS: 'hotel (Medium-class)',
    cte.DORMITORY: 'dormitory',
    cte.INDUSTRY: 'industry',
    cte.RESTAURANT: 'restaurant',
    cte.HEALTH_CARE: 'health care',
    cte.RETIREMENT_HOME_OR_ORPHANAGE: 'Home for the aged or orphanage',
    cte.OFFICE_AND_ADMINISTRATION: 'office and administration',
    cte.EVENT_LOCATION: 'event location',
    cte.HALL: 'hall',
    cte.SPORTS_LOCATION: 'sport location',
    cte.LABOR: 'Labor',
    cte.GREEN_HOUSE: 'green house',
    cte.NON_HEATED: 'non-heated'}

  @staticmethod
  def hft_from_libs_usage(usage):
    """
    Get HfT usage from the given internal usage key
    :param usage: str
    :return: str
    """
    try:
      return UsageHelper._usage_to_hft[usage]
    except KeyError:
      sys.stderr.write('Error: keyword not found to translate from libs_usage to hft usage.\n')

  _usage_to_comnet = {
    cte.RESIDENTIAL: 'BA Multifamily',
    cte.SINGLE_FAMILY_HOUSE: 'BA Multifamily',
    cte.MULTI_FAMILY_HOUSE: 'BA Multifamily',
    cte.EDUCATION: 'BA School/University',
    cte.SCHOOL_WITHOUT_SHOWER: 'BA School/University',
    cte.SCHOOL_WITH_SHOWER: 'BA School/University',
    cte.RETAIL_SHOP_WITHOUT_REFRIGERATED_FOOD: 'BA Retail',
    cte.RETAIL_SHOP_WITH_REFRIGERATED_FOOD: 'BA Retail',
    cte.HOTEL: 'BA Hotel',
    cte.HOTEL_MEDIUM_CLASS: 'BA Hotel',
    cte.DORMITORY: 'BA Dormitory',
    cte.INDUSTRY: 'BA Manufacturing Facility',
    cte.RESTAURANT: 'BA Dining: Family',
    cte.HEALTH_CARE: 'BA Hospital',
    cte.RETIREMENT_HOME_OR_ORPHANAGE: 'BA Multifamily',
    cte.OFFICE_AND_ADMINISTRATION: 'BA Office',
    cte.EVENT_LOCATION: 'BA Convention Center',
    cte.HALL: 'BA Convention Center',
    cte.SPORTS_LOCATION: 'BA Sports Arena',
    cte.LABOR: 'BA Gymnasium',
    cte.GREEN_HOUSE: cte.GREEN_HOUSE,
    cte.NON_HEATED: cte.NON_HEATED
  }

  _comnet_schedules_key_to_comnet_schedules = {
    'C-1 Assembly': 'C-1 Assembly',
    'C-2 Public': 'C-2 Health',
    'C-3 Hotel Motel': 'C-3 Hotel',
    'C-4 Manufacturing': 'C-4 Manufacturing',
    'C-5 Office': 'C-5 Office',
    'C-6 Parking Garage': 'C-6 Parking',
    'C-7 Restaurant': 'C-7 Restaurant',
    'C-8 Retail': 'C-8 Retail',
    'C-9 Schools': 'C-9 School',
    'C-10 Warehouse': 'C-10 Warehouse',
    'C-11 Laboratory': 'C-11 Lab',
    'C-12 Residential': 'C-12 Residential',
    'C-13 Data Center': 'C-13 Data',
    'C-14 Gymnasium': 'C-14 Gymnasium'}

  _comnet_schedules_key_to_usage = {
    'C-1 Assembly': 'C-1 Assembly',
    'C-2 Public': 'C-2 Health',
    'C-3 Hotel Motel': 'C-3 Hotel',
    'C-4 Manufacturing': 'C-4 Manufacturing',
    'C-5 Office': 'C-5 Office',
    'C-6 Parking Garage': 'C-6 Parking',
    'C-7 Restaurant': 'C-7 Restaurant',
    'C-8 Retail': 'C-8 Retail',
    'C-9 Schools': 'C-9 School',
    'C-10 Warehouse': 'C-10 Warehouse',
    'C-11 Laboratory': 'C-11 Lab',
    'C-12 Residential': 'C-12 Residential',
    'C-13 Data Center': 'C-13 Data',
    'C-14 Gymnasium': 'C-14 Gymnasium'}

  @staticmethod
  def comnet_from_libs_usage(usage):
    """
    Get Comnet usage from the given internal usage key
    :param usage: str
    :return: str
    """
    try:
      return UsageHelper._usage_to_comnet[usage]
    except KeyError:
      sys.stderr.write('Error: keyword not found to translate from libs_usage to comnet usage.\n')

  @staticmethod
  def schedules_key(usage):
    """
    Get Comnet schedules key from the list found in the Comnet usage file
    :param usage: str
    :return: str
    """
    try:
      return UsageHelper._comnet_schedules_key_to_comnet_schedules[usage]
    except KeyError:
      sys.stderr.write('Error: Comnet keyword not found. An update of the Comnet files might have been '
                       'done changing the keywords.\n')
