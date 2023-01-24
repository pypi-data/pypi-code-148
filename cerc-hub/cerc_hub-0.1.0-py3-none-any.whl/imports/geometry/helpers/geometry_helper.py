"""
Geometry helper
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import helpers.constants as cte
import numpy as np


class GeometryHelper:
  """
  Geometry helper
  """
  # function
  _pluto_to_function = {
    'A0': cte.SINGLE_FAMILY_HOUSE,
    'A1': cte.SINGLE_FAMILY_HOUSE,
    'A2': cte.SINGLE_FAMILY_HOUSE,
    'A3': cte.SINGLE_FAMILY_HOUSE,
    'A4': cte.SINGLE_FAMILY_HOUSE,
    'A5': cte.SINGLE_FAMILY_HOUSE,
    'A6': cte.SINGLE_FAMILY_HOUSE,
    'A7': cte.SINGLE_FAMILY_HOUSE,
    'A8': cte.SINGLE_FAMILY_HOUSE,
    'A9': cte.SINGLE_FAMILY_HOUSE,
    'B1': cte.MULTI_FAMILY_HOUSE,
    'B2': cte.MULTI_FAMILY_HOUSE,
    'B3': cte.MULTI_FAMILY_HOUSE,
    'B9': cte.MULTI_FAMILY_HOUSE,
    'C0': cte.RESIDENTIAL,
    'C1': cte.RESIDENTIAL,
    'C2': cte.RESIDENTIAL,
    'C3': cte.RESIDENTIAL,
    'C4': cte.RESIDENTIAL,
    'C5': cte.RESIDENTIAL,
    'C6': cte.RESIDENTIAL,
    'C7': cte.RESIDENTIAL,
    'C8': cte.RESIDENTIAL,
    'C9': cte.RESIDENTIAL,
    'D0': cte.RESIDENTIAL,
    'D1': cte.RESIDENTIAL,
    'D2': cte.RESIDENTIAL,
    'D3': cte.RESIDENTIAL,
    'D4': cte.RESIDENTIAL,
    'D5': cte.RESIDENTIAL,
    'D6': cte.RESIDENTIAL,
    'D7': cte.RESIDENTIAL,
    'D8': cte.RESIDENTIAL,
    'D9': cte.RESIDENTIAL,
    'E1': cte.WAREHOUSE,
    'E3': cte.WAREHOUSE,
    'E4': cte.WAREHOUSE,
    'E5': cte.WAREHOUSE,
    'E7': cte.WAREHOUSE,
    'E9': cte.WAREHOUSE,
    'F1': cte.WAREHOUSE,
    'F2': cte.WAREHOUSE,
    'F4': cte.WAREHOUSE,
    'F5': cte.WAREHOUSE,
    'F8': cte.WAREHOUSE,
    'F9': cte.WAREHOUSE,
    'G0': cte.SMALL_OFFICE,
    'G1': cte.SMALL_OFFICE,
    'G2': cte.SMALL_OFFICE,
    'G3': cte.SMALL_OFFICE,
    'G4': cte.SMALL_OFFICE,
    'G5': cte.SMALL_OFFICE,
    'G6': cte.SMALL_OFFICE,
    'G7': cte.SMALL_OFFICE,
    'G8': cte.SMALL_OFFICE,
    'G9': cte.SMALL_OFFICE,
    'H1': cte.HOTEL,
    'H2': cte.HOTEL,
    'H3': cte.HOTEL,
    'H4': cte.HOTEL,
    'H5': cte.HOTEL,
    'H6': cte.HOTEL,
    'H7': cte.HOTEL,
    'H8': cte.HOTEL,
    'H9': cte.HOTEL,
    'HB': cte.HOTEL,
    'HH': cte.HOTEL,
    'HR': cte.HOTEL,
    'HS': cte.HOTEL,
    'I1': cte.HOSPITAL,
    'I2': cte.OUT_PATIENT_HEALTH_CARE,
    'I3': cte.OUT_PATIENT_HEALTH_CARE,
    'I4': cte.RESIDENTIAL,
    'I5': cte.OUT_PATIENT_HEALTH_CARE,
    'I6': cte.OUT_PATIENT_HEALTH_CARE,
    'I7': cte.OUT_PATIENT_HEALTH_CARE,
    'I9': cte.OUT_PATIENT_HEALTH_CARE,
    'J1': cte.LARGE_OFFICE,
    'J2': cte.LARGE_OFFICE,
    'J3': cte.LARGE_OFFICE,
    'J4': cte.LARGE_OFFICE,
    'J5': cte.LARGE_OFFICE,
    'J6': cte.LARGE_OFFICE,
    'J7': cte.LARGE_OFFICE,
    'J8': cte.LARGE_OFFICE,
    'J9': cte.LARGE_OFFICE,
    'K1': cte.STRIP_MALL,
    'K2': cte.STRIP_MALL,
    'K3': cte.STRIP_MALL,
    'K4': cte.RESIDENTIAL,
    'K5': cte.RESTAURANT,
    'K6': cte.SUPERMARKET,
    'K7': cte.SUPERMARKET,
    'K8': cte.SUPERMARKET,
    'K9': cte.SUPERMARKET,
    'L1': cte.RESIDENTIAL,
    'L2': cte.RESIDENTIAL,
    'L3': cte.RESIDENTIAL,
    'L8': cte.RESIDENTIAL,
    'L9': cte.RESIDENTIAL,
    'M1': cte.LARGE_OFFICE,
    'M2': cte.LARGE_OFFICE,
    'M3': cte.LARGE_OFFICE,
    'M4': cte.LARGE_OFFICE,
    'M9': cte.LARGE_OFFICE,
    'N1': cte.RESIDENTIAL,
    'N2': cte.RESIDENTIAL,
    'N3': cte.RESIDENTIAL,
    'N4': cte.RESIDENTIAL,
    'N9': cte.RESIDENTIAL,
    'O1': cte.SMALL_OFFICE,
    'O2': cte.SMALL_OFFICE,
    'O3': cte.SMALL_OFFICE,
    'O4': cte.SMALL_OFFICE,
    'O5': cte.SMALL_OFFICE,
    'O6': cte.SMALL_OFFICE,
    'O7': cte.SMALL_OFFICE,
    'O8': cte.SMALL_OFFICE,
    'O9': cte.SMALL_OFFICE,
    'P1': cte.LARGE_OFFICE,
    'P2': cte.HOTEL,
    'P3': cte.SMALL_OFFICE,
    'P4': cte.SMALL_OFFICE,
    'P5': cte.SMALL_OFFICE,
    'P6': cte.SMALL_OFFICE,
    'P7': cte.LARGE_OFFICE,
    'P8': cte.LARGE_OFFICE,
    'P9': cte.SMALL_OFFICE,
    'Q0': cte.SMALL_OFFICE,
    'Q1': cte.SMALL_OFFICE,
    'Q2': cte.SMALL_OFFICE,
    'Q3': cte.SMALL_OFFICE,
    'Q4': cte.SMALL_OFFICE,
    'Q5': cte.SMALL_OFFICE,
    'Q6': cte.SMALL_OFFICE,
    'Q7': cte.SMALL_OFFICE,
    'Q8': cte.SMALL_OFFICE,
    'Q9': cte.SMALL_OFFICE,
    'R0': cte.RESIDENTIAL,
    'R1': cte.RESIDENTIAL,
    'R2': cte.RESIDENTIAL,
    'R3': cte.RESIDENTIAL,
    'R4': cte.RESIDENTIAL,
    'R5': cte.RESIDENTIAL,
    'R6': cte.RESIDENTIAL,
    'R7': cte.RESIDENTIAL,
    'R8': cte.RESIDENTIAL,
    'R9': cte.RESIDENTIAL,
    'RA': cte.RESIDENTIAL,
    'RB': cte.RESIDENTIAL,
    'RC': cte.RESIDENTIAL,
    'RD': cte.RESIDENTIAL,
    'RG': cte.RESIDENTIAL,
    'RH': cte.RESIDENTIAL,
    'RI': cte.RESIDENTIAL,
    'RK': cte.RESIDENTIAL,
    'RM': cte.RESIDENTIAL,
    'RR': cte.RESIDENTIAL,
    'RS': cte.RESIDENTIAL,
    'RW': cte.RESIDENTIAL,
    'RX': cte.RESIDENTIAL,
    'RZ': cte.RESIDENTIAL,
    'S0': cte.RESIDENTIAL,
    'S1': cte.RESIDENTIAL,
    'S2': cte.RESIDENTIAL,
    'S3': cte.RESIDENTIAL,
    'S4': cte.RESIDENTIAL,
    'S5': cte.RESIDENTIAL,
    'S9': cte.RESIDENTIAL,
    'U0': cte.WAREHOUSE,
    'U1': cte.WAREHOUSE,
    'U2': cte.WAREHOUSE,
    'U3': cte.WAREHOUSE,
    'U4': cte.WAREHOUSE,
    'U5': cte.WAREHOUSE,
    'U6': cte.WAREHOUSE,
    'U7': cte.WAREHOUSE,
    'U8': cte.WAREHOUSE,
    'U9': cte.WAREHOUSE,
    'W1': cte.PRIMARY_SCHOOL,
    'W2': cte.PRIMARY_SCHOOL,
    'W3': cte.SECONDARY_SCHOOL,
    'W4': cte.SECONDARY_SCHOOL,
    'W5': cte.SECONDARY_SCHOOL,
    'W6': cte.SECONDARY_SCHOOL,
    'W7': cte.SECONDARY_SCHOOL,
    'W8': cte.PRIMARY_SCHOOL,
    'W9': cte.SECONDARY_SCHOOL,
    'Y1': cte.LARGE_OFFICE,
    'Y2': cte.LARGE_OFFICE,
    'Y3': cte.LARGE_OFFICE,
    'Y4': cte.LARGE_OFFICE,
    'Y5': cte.LARGE_OFFICE,
    'Y6': cte.LARGE_OFFICE,
    'Y7': cte.LARGE_OFFICE,
    'Y8': cte.LARGE_OFFICE,
    'Y9': cte.LARGE_OFFICE,
    'Z1': cte.LARGE_OFFICE
  }
  _hft_to_function = {
    'residential': cte.RESIDENTIAL,
    'single family house': cte.SINGLE_FAMILY_HOUSE,
    'multifamily house': cte.MULTI_FAMILY_HOUSE,
    'hotel': cte.HOTEL,
    'hospital': cte.HOSPITAL,
    'outpatient': cte.OUT_PATIENT_HEALTH_CARE,
    'commercial': cte.SUPERMARKET,
    'strip mall': cte.STRIP_MALL,
    'warehouse': cte.WAREHOUSE,
    'primary school': cte.PRIMARY_SCHOOL,
    'secondary school': cte.SECONDARY_SCHOOL,
    'office': cte.MEDIUM_OFFICE,
    'large office': cte.LARGE_OFFICE
  }

  # usage
  _function_to_usage = {
    cte.RESIDENTIAL: cte.RESIDENTIAL,
    cte.SINGLE_FAMILY_HOUSE: cte.SINGLE_FAMILY_HOUSE,
    cte.MULTI_FAMILY_HOUSE: cte.MULTI_FAMILY_HOUSE,
    cte.ROW_HOSE: cte.RESIDENTIAL,
    cte.MID_RISE_APARTMENT: cte.RESIDENTIAL,
    cte.HIGH_RISE_APARTMENT: cte.RESIDENTIAL,
    cte.SMALL_OFFICE: cte.OFFICE_AND_ADMINISTRATION,
    cte.MEDIUM_OFFICE: cte.OFFICE_AND_ADMINISTRATION,
    cte.LARGE_OFFICE: cte.OFFICE_AND_ADMINISTRATION,
    cte.PRIMARY_SCHOOL: cte.EDUCATION,
    cte.SECONDARY_SCHOOL: cte.EDUCATION,
    cte.STAND_ALONE_RETAIL: cte.RETAIL_SHOP_WITHOUT_REFRIGERATED_FOOD,
    cte.HOSPITAL: cte.HEALTH_CARE,
    cte.OUT_PATIENT_HEALTH_CARE: cte.HEALTH_CARE,
    cte.STRIP_MALL: cte.RETAIL_SHOP_WITHOUT_REFRIGERATED_FOOD,
    cte.SUPERMARKET: cte.RETAIL_SHOP_WITH_REFRIGERATED_FOOD,
    cte.WAREHOUSE: cte.RETAIL_SHOP_WITHOUT_REFRIGERATED_FOOD,
    cte.QUICK_SERVICE_RESTAURANT: cte.RESTAURANT,
    cte.FULL_SERVICE_RESTAURANT: cte.RESTAURANT,
    cte.SMALL_HOTEL: cte.HOTEL,
    cte.LARGE_HOTEL: cte.HOTEL,
    cte.INDUSTRY:cte.INDUSTRY
  }

  @staticmethod
  def libs_function_from_hft(building_hft_function):
    """
    Get internal function from the given HfT function
    :param building_hft_function: str
    :return: str
    """
    return GeometryHelper._hft_to_function[building_hft_function]

  @staticmethod
  def libs_function_from_pluto(building_pluto_function):
    """
    Get internal function from the given pluto function
    :param building_pluto_function: str
    :return: str
    """
    return GeometryHelper._pluto_to_function[building_pluto_function]

  @staticmethod
  def libs_usage_from_libs_function(building_function):
    """
    Get the internal usage for the given internal building function
    :param building_function: str
    :return: str
    """
    return GeometryHelper._function_to_usage[building_function]

  @staticmethod
  def to_points_matrix(points):
    """
    Transform a point vector into a point matrix
    :param points: [x, y, z, x, y, z ...]
    :return: [[x,y,z],[x,y,z]...]
    """
    rows = points.size // 3
    points = points.reshape(rows, 3)
    return points

  @staticmethod
  def gml_surface_to_libs(surface):
    """
    Transform citygml surface names into hub names
    """
    if surface == 'WallSurface':
      return 'Wall'
    if surface == 'GroundSurface':
      return 'Ground'
    return 'Roof'

  @staticmethod
  def points_from_string(coordinates) -> np.ndarray:
    points = np.fromstring(coordinates, dtype=float, sep=' ')
    points = GeometryHelper.to_points_matrix(points)
    return points

  @staticmethod
  def remove_last_point_from_string(points):
    array = points.split(' ')
    res = " "
    return res.join(array[0:len(array) - 3])
