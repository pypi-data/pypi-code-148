"""
ComnetUsageParameters model the usage properties
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import copy
import sys
from typing import Dict
import pandas as pd
import numpy

import helpers.constants as cte
from helpers.configuration_helper import ConfigurationHelper as ch
from imports.geometry.helpers.geometry_helper import GeometryHelper
from imports.usage.helpers.usage_helper import UsageHelper
from imports.usage.helpers.schedules_helper import SchedulesHelper
from city_model_structure.building_demand.usage_zone import UsageZone
from city_model_structure.building_demand.lighting import Lighting
from city_model_structure.building_demand.occupancy import Occupancy
from city_model_structure.building_demand.appliances import Appliances
from city_model_structure.building_demand.thermal_control import ThermalControl
from city_model_structure.attributes.schedule import Schedule
from city_model_structure.building_demand.internal_gain import InternalGain


class ComnetUsageParameters:
  """
  ComnetUsageParameters class
  """
  def __init__(self, city, base_path):
    self._city = city
    self._base_path = str(base_path / 'comnet_archetypes.xlsx')
    self._data = self._read_file()
    self._comnet_schedules_path = str(base_path / 'comnet_schedules_archetypes.xlsx')
    self._xls = pd.ExcelFile(self._comnet_schedules_path)

  def _read_file(self) -> Dict:
    """
    reads xlsx files containing usage information into a dictionary
    :return : Dict
    """
    number_usage_types = 33
    xl_file = pd.ExcelFile(self._base_path)
    file_data = pd.read_excel(xl_file, sheet_name="Modeling Data", usecols="A:AB", skiprows=[0, 1, 2],
                              nrows=number_usage_types)

    lighting_data = {}
    plug_loads_data = {}
    occupancy_data = {}
    ventilation_rate = {}
    water_heating = {}
    process_data = {}
    schedules_key = {}

    for j in range(0, number_usage_types):
      usage_parameters = file_data.iloc[j]
      usage_type = usage_parameters[0]
      lighting_data[usage_type] = usage_parameters[1:6].values.tolist()
      plug_loads_data[usage_type] = usage_parameters[8:13].values.tolist()
      occupancy_data[usage_type] = usage_parameters[17:20].values.tolist()
      ventilation_rate[usage_type] = usage_parameters[20:21].values.tolist()
      water_heating[usage_type] = usage_parameters[23:24].values.tolist()
      process_data[usage_type] = usage_parameters[24:26].values.tolist()
      schedules_key[usage_type] = usage_parameters[27:28].values.tolist()

    return {'lighting': lighting_data,
            'plug loads': plug_loads_data,
            'occupancy': occupancy_data,
            'ventilation rate': ventilation_rate,
            'water heating': water_heating,
            'process': process_data,
            'schedules_key': schedules_key}

  @staticmethod
  def _parse_usage_type(comnet_usage, data, schedules_data):
    _usage_zone = UsageZone()

    # lighting
    _lighting = Lighting()
    _lighting.latent_fraction = ch().comnet_lighting_latent
    _lighting.convective_fraction = ch().comnet_lighting_convective
    _lighting.radiative_fraction = ch().comnet_lighting_radiant
    _lighting.density = data['lighting'][comnet_usage][4]

    # plug loads
    _appliances = None
    if data['plug loads'][comnet_usage][0] != 'n.a.':
      _appliances = Appliances()
      _appliances.latent_fraction = ch().comnet_plugs_latent
      _appliances.convective_fraction = ch().comnet_plugs_convective
      _appliances.radiative_fraction = ch().comnet_plugs_radiant
      _appliances.density = data['plug loads'][comnet_usage][0]

    # occupancy
    _occupancy = Occupancy()
    value = data['occupancy'][comnet_usage][0]
    _occupancy.occupancy_density = 0
    if value != 0:
      _occupancy.occupancy_density = 1 / value

    _occupancy.sensible_convective_internal_gain = data['occupancy'][comnet_usage][1] \
                                                   * ch().comnet_occupancy_sensible_convective
    _occupancy.sensible_radiative_internal_gain = data['occupancy'][comnet_usage][1] \
                                                  * ch().comnet_occupancy_sensible_radiant
    _occupancy.latent_internal_gain = data['occupancy'][comnet_usage][2]

    _usage_zone.mechanical_air_change = data['ventilation rate'][comnet_usage][0]

    schedules_usage = UsageHelper.schedules_key(data['schedules_key'][comnet_usage][0])

    _extracted_data = pd.read_excel(schedules_data, sheet_name=schedules_usage, usecols="A:AA", skiprows=[0,  1, 2, 3],
                                    nrows=39)
    schedules = []
    number_of_schedule_types = 13
    schedules_per_schedule_type = 3
    day_types = dict({'week_day': 0, 'saturday': 1, 'sunday': 2})
    for schedule_types in range(0, number_of_schedule_types):
      name = ''
      data_type = ''
      for schedule_day in range(0, schedules_per_schedule_type):
        _schedule = Schedule()
        _schedule.time_step = cte.HOUR
        _schedule.time_range = cte.DAY
        row_cells = _extracted_data.iloc[schedules_per_schedule_type * schedule_types + schedule_day]
        if schedule_day == day_types['week_day']:
          name = row_cells[0]
          data_type = row_cells[1]
          _schedule.day_types = [cte.MONDAY, cte.TUESDAY, cte.WEDNESDAY, cte.THURSDAY, cte.FRIDAY]
        elif schedule_day == day_types['saturday']:
          _schedule.day_types = [cte.SATURDAY]
        else:
          _schedule.day_types = [cte.SUNDAY, cte.HOLIDAY]
        _schedule.type = name
        _schedule.data_type = SchedulesHelper.data_type_from_comnet(data_type)
        if _schedule.data_type == cte.ANY_NUMBER:
          values = []
          for cell in row_cells[schedules_per_schedule_type:].to_numpy():
            values.append((float(cell) - 32.) * 5 / 9)
          _schedule.values = values
        else:
          _schedule.values = row_cells[schedules_per_schedule_type:].to_numpy()
        schedules.append(_schedule)

    schedules_types = dict({'Occupancy': 0, 'Lights': 3, 'Receptacle': 6, 'Infiltration': 9, 'HVAC Avail': 12,
                            'ClgSetPt': 15, 'HtgSetPt': 18})

    _schedules = []
    for pointer in range(0, 3):
      _schedules.append(schedules[schedules_types['Occupancy']+pointer])
    _occupancy.occupancy_schedules = _schedules
    _schedules = []
    for pointer in range(0, 3):
      _schedules.append(schedules[schedules_types['Lights']+pointer])
    _lighting.schedules = _schedules
    _schedules = []
    for pointer in range(0, 3):
      _schedules.append(schedules[schedules_types['Receptacle']+pointer])
    _appliances.schedules = _schedules

    _usage_zone.occupancy = _occupancy
    _usage_zone.lighting = _lighting
    _usage_zone.appliances = _appliances

    _control = ThermalControl()
    _schedules = []
    for pointer in range(0, 3):
      _schedules.append(schedules[schedules_types['HtgSetPt']+pointer])
    _control.heating_set_point_schedules = _schedules
    _schedules = []
    for pointer in range(0, 3):
      _schedules.append(schedules[schedules_types['ClgSetPt']+pointer])
    _control.cooling_set_point_schedules = _schedules
    _schedules = []
    for pointer in range(0, 3):
      _schedules.append(schedules[schedules_types['HVAC Avail']+pointer])
    _control.hvac_availability_schedules = _schedules
    _usage_zone.thermal_control = _control

    return _usage_zone

  def _search_archetypes(self, libs_usage):
    for item in self._data['lighting']:
      comnet_usage = UsageHelper.comnet_from_libs_usage(libs_usage)
      if comnet_usage == item:
        usage_archetype = self._parse_usage_type(comnet_usage, self._data, self._xls)
        return usage_archetype
    return None

  def enrich_buildings(self):
    """
    Returns the city with the usage parameters assigned to the buildings
    :return:
    """
    city = self._city
    for building in city.buildings:
      usage = GeometryHelper.libs_usage_from_libs_function(building.function)
      try:
        archetype_usage = self._search_archetypes(usage)
      except KeyError:
        sys.stderr.write(f'Building {building.name} has unknown archetype for building function:'
                         f' {building.function}, that assigns building usage as '
                         f'{GeometryHelper.libs_usage_from_libs_function(building.function)}\n')
        return

      for internal_zone in building.internal_zones:
        if internal_zone.area is None:
          raise Exception('Internal zone area not defined, ACH cannot be calculated')
        if internal_zone.volume is None:
          raise Exception('Internal zone volume not defined, ACH cannot be calculated')
        if internal_zone.area <= 0:
          raise Exception('Internal zone area is zero, ACH cannot be calculated')
        if internal_zone.volume <= 0:
          raise Exception('Internal zone volume is zero, ACH cannot be calculated')
        volume_per_area = internal_zone.volume / internal_zone.area
        usage_zone = UsageZone()
        usage_zone.usage = usage
        self._assign_values_usage_zone(usage_zone, archetype_usage, volume_per_area)
        usage_zone.percentage = 1
        self._calculate_reduced_values_from_extended_library(usage_zone, archetype_usage)

        internal_zone.usage_zones = [usage_zone]

  @staticmethod
  def _assign_values_usage_zone(usage_zone, archetype, volume_per_area):
    # Due to the fact that python is not a typed language, the wrong object type is assigned to
    # usage_zone.occupancy when writing usage_zone.occupancy = archetype.occupancy.
    # Same happens for lighting and appliances. Therefore, this walk around has been done.
    usage_zone.mechanical_air_change = archetype.mechanical_air_change * cte.METERS_TO_FEET ** 2 \
                                       * cte.HOUR_TO_MINUTES / cte.METERS_TO_FEET ** 3 / volume_per_area
    _occupancy = Occupancy()
    _occupancy.occupancy_density = archetype.occupancy.occupancy_density * cte.METERS_TO_FEET**2
    _occupancy.sensible_radiative_internal_gain = archetype.occupancy.sensible_radiative_internal_gain \
                                                  * archetype.occupancy.occupancy_density \
                                                  * cte.METERS_TO_FEET**2 * cte.BTU_H_TO_WATTS
    _occupancy.latent_internal_gain = archetype.occupancy.latent_internal_gain \
                                      * archetype.occupancy.occupancy_density \
                                      * cte.METERS_TO_FEET**2 * cte.BTU_H_TO_WATTS
    _occupancy.sensible_convective_internal_gain = archetype.occupancy.sensible_convective_internal_gain \
                                                   * archetype.occupancy.occupancy_density \
                                                   * cte.METERS_TO_FEET**2 * cte.BTU_H_TO_WATTS
    _occupancy.occupancy_schedules = archetype.occupancy.occupancy_schedules
    usage_zone.occupancy = _occupancy
    _lighting = Lighting()
    _lighting.density = archetype.lighting.density / cte.METERS_TO_FEET ** 2
    _lighting.convective_fraction = archetype.lighting.convective_fraction
    _lighting.radiative_fraction = archetype.lighting.radiative_fraction
    _lighting.latent_fraction = archetype.lighting.latent_fraction
    _lighting.schedules = archetype.lighting.schedules
    usage_zone.lighting = _lighting
    _appliances = Appliances()
    _appliances.density = archetype.appliances.density / cte.METERS_TO_FEET ** 2
    _appliances.convective_fraction = archetype.appliances.convective_fraction
    _appliances.radiative_fraction = archetype.appliances.radiative_fraction
    _appliances.latent_fraction = archetype.appliances.latent_fraction
    _appliances.schedules = archetype.appliances.schedules
    usage_zone.appliances = _appliances
    _control = ThermalControl()
    _control.cooling_set_point_schedules = archetype.thermal_control.cooling_set_point_schedules
    _control.heating_set_point_schedules = archetype.thermal_control.heating_set_point_schedules
    _control.hvac_availability_schedules = archetype.thermal_control.hvac_availability_schedules
    usage_zone.thermal_control = _control

  @staticmethod
  def _calculate_reduced_values_from_extended_library(usage_zone, archetype):
    number_of_days_per_type = {'WD': 251, 'Sat': 52, 'Sun': 62}
    total = 0
    for schedule in archetype.thermal_control.hvac_availability_schedules:
      if schedule.day_types[0] == cte.SATURDAY:
        for value in schedule.values:
          total += value * number_of_days_per_type['Sat']
      elif schedule.day_types[0] == cte.SUNDAY:
        for value in schedule.values:
          total += value * number_of_days_per_type['Sun']
      else:
        for value in schedule.values:
          total += value * number_of_days_per_type['WD']

    usage_zone.hours_day = total / 365
    usage_zone.days_year = 365

  @staticmethod
  def _calculate_internal_gains(archetype):

    _DAYS = [cte.MONDAY, cte.TUESDAY, cte.WEDNESDAY, cte.THURSDAY, cte.FRIDAY, cte.SATURDAY, cte.SUNDAY, cte.HOLIDAY]
    _number_of_days_per_type = [51, 50, 50, 50, 50, 52, 52, 10]

    _mean_internal_gain = InternalGain()
    _mean_internal_gain.type = 'mean_value_of_internal_gains'
    _base_schedule = Schedule()
    _base_schedule.type = cte.INTERNAL_GAINS
    _base_schedule.time_range = cte.DAY
    _base_schedule.time_step = cte.HOUR
    _base_schedule.data_type = cte.FRACTION

    _latent_heat_gain = archetype.occupancy.latent_internal_gain
    _convective_heat_gain = archetype.occupancy.sensible_convective_internal_gain
    _radiative_heat_gain = archetype.occupancy.sensible_radiative_internal_gain
    _total_heat_gain = (_latent_heat_gain + _convective_heat_gain + _radiative_heat_gain)

    _schedule_values = numpy.zeros([24, 8])
    _sum = 0
    for day, _schedule in enumerate(archetype.occupancy.schedules):
      for v, value in enumerate(_schedule.values):
        _schedule_values[v, day] = value * _total_heat_gain
        _sum += value * _total_heat_gain * _number_of_days_per_type[day]

    _total_heat_gain += archetype.lighting.density + archetype.appliances.density
    _latent_heat_gain += archetype.lighting.latent_fraction * archetype.lighting.density\
                         + archetype.appliances.latent_fraction * archetype.appliances.density
    _radiative_heat_gain = archetype.lighting.radiative_fraction * archetype.lighting.density \
                           + archetype.appliances.radiative_fraction * archetype.appliances.density
    _convective_heat_gain = archetype.lighting.convective_fraction * archetype.lighting.density \
                           + archetype.appliances.convective_fraction * archetype.appliances.density

    for day, _schedule in enumerate(archetype.lighting.schedules):
      for v, value in enumerate(_schedule.values):
        _schedule_values[v, day] += value * archetype.lighting.density
        _sum += value * archetype.lighting.density * _number_of_days_per_type[day]

    for day, _schedule in enumerate(archetype.appliances.schedules):
      for v, value in enumerate(_schedule.values):
        _schedule_values[v, day] += value * archetype.appliances.density
        _sum += value * archetype.appliances.density * _number_of_days_per_type[day]

    _latent_fraction = _latent_heat_gain / _total_heat_gain
    _radiative_fraction = _radiative_heat_gain / _total_heat_gain
    _convective_fraction = _convective_heat_gain / _total_heat_gain
    _average_internal_gain = _sum / _total_heat_gain

    _schedules = []
    for day in range(0, len(_DAYS)):
      _schedule = copy.deepcopy(_base_schedule)
      _schedule.day_types = [_DAYS[day]]
      _schedule.values = _schedule_values[:day]
      _schedules.append(_schedule)

    _mean_internal_gain.average_internal_gain = _average_internal_gain
    _mean_internal_gain.latent_fraction = _latent_fraction
    _mean_internal_gain.convective_fraction = _convective_fraction
    _mean_internal_gain.radiative_fraction = _radiative_fraction
    _mean_internal_gain.schedules = _schedules

    return [_mean_internal_gain]
