"""
Schedules helper
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import sys
import helpers.constants as cte


class SchedulesHelper:
  """
  Schedules helper
  """
  _usage_to_comnet = {
    cte.RESIDENTIAL: 'C-12 Residential',
    cte.INDUSTRY: 'C-10 Warehouse',
    cte.OFFICE_AND_ADMINISTRATION: 'C-5 Office',
    cte.HOTEL: 'C-3 Hotel',
    cte.HEALTH_CARE: 'C-2 Health',
    cte.RETAIL_SHOP_WITHOUT_REFRIGERATED_FOOD: 'C-8 Retail',
    cte.HALL: 'C-8 Retail',
    cte.RESTAURANT: 'C-7 Restaurant',
    cte.EDUCATION: 'C-9 School'
  }

  _comnet_to_data_type = {
    'Fraction': cte.FRACTION,
    'OnOff': cte.ON_OFF,
    'Temperature': cte.ANY_NUMBER
  }

  # usage
  _function_to_usage = {
    'full service restaurant': cte.RESTAURANT,
    'high-rise apartment': cte.RESIDENTIAL,
    'hospital': cte.HEALTH_CARE,
    'large hotel': cte.HOTEL,
    'large office': cte.OFFICE_AND_ADMINISTRATION,
    'medium office': cte.OFFICE_AND_ADMINISTRATION,
    'midrise apartment': cte.RESIDENTIAL,
    'outpatient healthcare': cte.HEALTH_CARE,
    'primary school': cte.EDUCATION,
    'quick service restaurant': cte.RESTAURANT,
    'secondary school': cte.EDUCATION,
    'small hotel': cte.HOTEL,
    'small office': cte.OFFICE_AND_ADMINISTRATION,
    'stand-alone-retail': cte.RETAIL_SHOP_WITHOUT_REFRIGERATED_FOOD,
    'strip mall': cte.HALL,
    'supermarket': cte.RETAIL_SHOP_WITH_REFRIGERATED_FOOD,
    'warehouse': cte.INDUSTRY,
    'residential': cte.RESIDENTIAL
  }

  @staticmethod
  def comnet_from_usage(usage):
    """
    Get Comnet usage from the given internal usage key
    :param usage: str
    :return: str
    """
    try:
      return SchedulesHelper._usage_to_comnet[usage]
    except KeyError:
      sys.stderr.write('Error: keyword not found.\n')

  @staticmethod
  def data_type_from_comnet(comnet_data_type):
    """
    Get data_type from the Comnet data type definitions
    :param comnet_data_type: str
    :return: str
    """
    try:
      return SchedulesHelper._comnet_to_data_type[comnet_data_type]
    except KeyError:
      raise ValueError(f"Error: comnet data type keyword not found.")

  @staticmethod
  def usage_from_function(building_function):
    """
    Get the internal usage for the given internal building function
    :param building_function: str
    :return: str
    """
    return SchedulesHelper._function_to_usage[building_function]
