"""
Hft-based interface, it reads format defined within the CERC team (based on that one used in SimStadt and developed by
the IAF team at hft-Stuttgart)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import xmltodict
import copy
from city_model_structure.building_demand.usage_zone import UsageZone
from city_model_structure.building_demand.internal_gain import InternalGain
from city_model_structure.building_demand.occupancy import Occupancy
from city_model_structure.building_demand.appliances import Appliances
from city_model_structure.building_demand.thermal_control import ThermalControl
from city_model_structure.attributes.schedule import Schedule
import helpers.constants as cte
from imports.usage.helpers.usage_helper import UsageHelper


class HftUsageInterface:
  """
  HftUsageInterface abstract class
  """

  def __init__(self, base_path, usage_file='ca_library_reduced.xml'):
    path = str(base_path / usage_file)
    self._usage_archetypes = []
    with open(path) as xml:
      self._archetypes = xmltodict.parse(xml.read(), force_list=('zoneUsageVariant', 'zoneUsageType'))
    for zone_usage_type in self._archetypes['buildingUsageLibrary']['zoneUsageType']:
      usage = zone_usage_type['id']
      usage_archetype = self._parse_zone_usage_type(usage, zone_usage_type)
      self._usage_archetypes.append(usage_archetype)
      if 'zoneUsageVariant' in zone_usage_type:
        for usage_zone_variant in zone_usage_type['zoneUsageVariant']:
          usage = usage_zone_variant['id']
          usage_archetype_variant = self._parse_zone_usage_variant(usage, usage_archetype, usage_zone_variant)
          self._usage_archetypes.append(usage_archetype_variant)

  @staticmethod
  def _parse_zone_usage_type(usage, zone_usage_type):
    usage_zone_archetype = UsageZone()
    usage_zone_archetype.usage = usage

    if 'occupancy' in zone_usage_type:
      _occupancy = Occupancy()
      _occupancy.occupancy_density = zone_usage_type['occupancy']['occupancyDensity'] #todo: check units

      if 'internGains' in zone_usage_type['occupancy']:
        _internal_gain = InternalGain()
        _internal_gain.latent_fraction = zone_usage_type['occupancy']['internGains']['latentFraction']
        _internal_gain.convective_fraction = zone_usage_type['occupancy']['internGains']['convectiveFraction']
        _internal_gain.average_internal_gain = zone_usage_type['occupancy']['internGains']['averageInternGainPerSqm']
        _internal_gain.radiative_fraction = zone_usage_type['occupancy']['internGains']['radiantFraction']
        if 'load' in zone_usage_type['occupancy']['internGains']:
          _schedule = Schedule()
          _schedule.type = 'internal gains load'
          _schedule.time_range = cte.DAY
          _schedule.time_step = cte.HOUR
          _schedule.data_type = cte.ANY_NUMBER
          _schedule.day_types = [cte.MONDAY, cte.TUESDAY, cte.WEDNESDAY, cte.THURSDAY, cte.FRIDAY, cte.SATURDAY,
                                 cte.SUNDAY]
          _values = zone_usage_type['occupancy']['internGains']['load']['weekDayProfile']['values']
          while '  ' in _values:
            _values = _values.replace('  ', ' ')
          _values = _values.split()
          _values_float = []
          for _value in _values:
            _values_float.append(float(_value))
          _schedule.values = _values_float
          _internal_gain.schedules = [_schedule]

        usage_zone_archetype.internal_gains = [_internal_gain]

      usage_zone_archetype.hours_day = zone_usage_type['occupancy']['usageHoursPerDay']
      usage_zone_archetype.days_year = zone_usage_type['occupancy']['usageDaysPerYear']
      usage_zone_archetype.occupancy = _occupancy

    if 'endUses' in zone_usage_type:
      _thermal_control = ThermalControl()
      if 'space_heating' in zone_usage_type['endUses']:
        _thermal_control.mean_heating_set_point = \
          zone_usage_type['endUses']['space_heating']['heatingSetPointTemperature']
        _thermal_control.heating_set_back = zone_usage_type['endUses']['space_heating']['heatingSetBackTemperature']
        if 'schedule' in zone_usage_type['endUses']['space_heating']:
          _schedule = Schedule()
          _schedule.type = 'heating temperature'
          _schedule.time_range = cte.DAY
          _schedule.time_step = cte.HOUR
          _schedule.data_type = cte.ANY_NUMBER
          _schedule.day_types = [cte.MONDAY, cte.TUESDAY, cte.WEDNESDAY, cte.THURSDAY, cte.FRIDAY, cte.SATURDAY,
                                 cte.SUNDAY]
          _values = zone_usage_type['endUses']['space_heating']['schedule']['weekDayProfile']['values']
          while '  ' in _values:
            _values = _values.replace('  ', ' ')
          _values = _values.split()
          _values_float = []
          for _value in _values:
            _values_float.append(float(_value))
          _schedule.values = _values_float
          _thermal_control.heating_set_point_schedules = [_schedule]

      if 'space_cooling' in zone_usage_type['endUses']:
        _thermal_control.mean_cooling_set_point = \
          zone_usage_type['endUses']['space_cooling']['coolingSetPointTemperature']
        if 'schedule' in zone_usage_type['endUses']['space_cooling']:
          _schedule = Schedule()
          _schedule.type = 'cooling temperature'
          _schedule.time_range = cte.DAY
          _schedule.time_step = cte.HOUR
          _schedule.data_type = cte.ANY_NUMBER
          _schedule.day_types = [cte.MONDAY, cte.TUESDAY, cte.WEDNESDAY, cte.THURSDAY, cte.FRIDAY, cte.SATURDAY,
                                 cte.SUNDAY]
          _values = zone_usage_type['endUses']['space_cooling']['schedule']['weekDayProfile']['values']
          while '  ' in _values:
            _values = _values.replace('  ', ' ')
          _values = _values.split()
          _values_float = []
          for _value in _values:
            _values_float.append(float(_value))
          _schedule.values = _values_float
          _thermal_control.cooling_set_point_schedules = [_schedule]

      usage_zone_archetype.thermal_control = _thermal_control

      if 'ventilation' in zone_usage_type['endUses'] and zone_usage_type['endUses']['ventilation'] is not None:
        usage_zone_archetype.mechanical_air_change = \
          zone_usage_type['endUses']['ventilation']['mechanicalAirChangeRate']

      # todo: not used or assigned anywhere
      if 'domestic_hot_water' in zone_usage_type['endUses']:
        # liters to cubic meters
        dhw_average_volume_pers_day = float(
          zone_usage_type['endUses']['domestic_hot_water']['averageVolumePerPersAndDay']) / 1000
        dhw_preparation_temperature = zone_usage_type['endUses']['domestic_hot_water']['preparationTemperature']

      if 'all_electrical_appliances' in zone_usage_type['endUses']:
        if 'averageConsumptionPerSqmAndYear' in zone_usage_type['endUses']['all_electrical_appliances']:
          # kWh to J
          usage_zone_archetype.electrical_app_average_consumption_sqm_year = \
            float(zone_usage_type['endUses']['all_electrical_appliances']['averageConsumptionPerSqmAndYear']) \
            * cte.KILO_WATTS_HOUR_TO_JULES

    if 'appliance' in zone_usage_type:
      _appliances = Appliances()
      _appliances.density = zone_usage_type['appliance']['#text'] #todo: check units

      usage_zone_archetype.appliances = _appliances

    return usage_zone_archetype

  @staticmethod
  def _parse_zone_usage_variant(usage, usage_zone, usage_zone_variant):
    # the variants mimic the inheritance concept from OOP
    usage_zone_archetype = copy.deepcopy(usage_zone)
    usage_zone_archetype.usage = usage

    if 'occupancy' in usage_zone_variant:
      _occupancy = Occupancy()
      if 'occupancyDensity' in usage_zone_variant['occupancy']:
        _occupancy.occupancy_density = usage_zone_variant['occupancy']['occupancyDensity']  # todo: check units
      if 'usageHoursPerDay' in usage_zone_variant['occupancy']:
        usage_zone_archetype.hours_day = usage_zone_variant['occupancy']['usageHoursPerDay']
      if 'usageDaysPerYear' in usage_zone_variant['occupancy']:
        usage_zone_archetype.days_year = usage_zone_variant['occupancy']['usageDaysPerYear']
      usage_zone_archetype.occupancy = _occupancy

      if 'internGains' in usage_zone_variant['occupancy']:
        _internal_gain = InternalGain()
        if 'latentFraction' in usage_zone_variant['occupancy']['internGains']:
          _internal_gain.latent_fraction = usage_zone_variant['occupancy']['internGains']['latentFraction']
        if 'convectiveFraction' in usage_zone_variant['occupancy']['internGains']:
          _internal_gain.convective_fraction = usage_zone_variant['occupancy']['internGains']['convectiveFraction']
        if 'averageInternGainPerSqm' in usage_zone_variant['occupancy']['internGains']:
          _internal_gain.average_internal_gain = \
            usage_zone_variant['occupancy']['internGains']['averageInternGainPerSqm']
        if 'radiantFraction' in usage_zone_variant['occupancy']['internGains']:
          _internal_gain.radiative_fraction = usage_zone_variant['occupancy']['internGains']['radiantFraction']
        if 'load' in usage_zone_variant['occupancy']['internGains']:
          _schedule = Schedule()
          _schedule.type = 'internal gains load'
          _schedule.time_range = cte.DAY
          _schedule.time_step = cte.HOUR
          _schedule.data_type = cte.ANY_NUMBER
          _schedule.day_types = [cte.MONDAY, cte.TUESDAY, cte.WEDNESDAY, cte.THURSDAY, cte.FRIDAY, cte.SATURDAY,
                                 cte.SUNDAY]
          _values = usage_zone_variant['occupancy']['internGains']['load']['weekDayProfile']['values']
          while '  ' in _values:
            _values = _values.replace('  ', ' ')
          _values = _values.split()
          _values_float = []
          for _value in _values:
            _values_float.append(float(_value))
          _schedule.values = _values_float
          _internal_gain.schedules = [_schedule]

        usage_zone_archetype.internal_gains = [_internal_gain]

    if 'endUses' in usage_zone_variant:
      _thermal_control = ThermalControl()
      if 'space_heating' in usage_zone_variant['endUses']:
        if 'heatingSetPointTemperature' in usage_zone_variant['endUses']['space_heating']:
          _thermal_control.mean_heating_set_point = \
            usage_zone_variant['endUses']['space_heating']['heatingSetPointTemperature']
        if 'heatingSetBackTemperature' in usage_zone_variant['endUses']['space_heating']:
          _thermal_control.heating_set_back = usage_zone_variant['endUses']['space_heating']['heatingSetBackTemperature']
        if 'schedule' in usage_zone_variant['endUses']['space_heating']:
          _schedule = Schedule()
          _schedule.type = 'heating temperature'
          _schedule.time_range = cte.DAY
          _schedule.time_step = cte.HOUR
          _schedule.data_type = cte.ANY_NUMBER
          _schedule.day_types = [cte.MONDAY, cte.TUESDAY, cte.WEDNESDAY, cte.THURSDAY, cte.FRIDAY, cte.SATURDAY,
                                 cte.SUNDAY]
          _values = usage_zone_variant['endUses']['space_heating']['schedule']['weekDayProfile']['values']
          while '  ' in _values:
            _values = _values.replace('  ', ' ')
          _values = _values.split()
          _values_float = []
          for _value in _values:
            _values_float.append(float(_value))
          _schedule.values = _values_float
          _thermal_control.heating_set_point_schedules = [_schedule]

      if 'space_cooling' in usage_zone_variant['endUses'] and \
          usage_zone_variant['endUses']['space_cooling'] is not None:
        if 'coolingSetPointTemperature' in usage_zone_variant['endUses']['space_cooling']:
          _thermal_control.mean_cooling_set_point = \
            usage_zone_variant['endUses']['space_cooling']['coolingSetPointTemperature']
        if 'schedule' in usage_zone_variant['endUses']['space_cooling']:
          _schedule = Schedule()
          _schedule.type = 'cooling temperature'
          _schedule.time_range = cte.DAY
          _schedule.time_step = cte.HOUR
          _schedule.data_type = cte.ANY_NUMBER
          _schedule.day_types = [cte.MONDAY, cte.TUESDAY, cte.WEDNESDAY, cte.THURSDAY, cte.FRIDAY, cte.SATURDAY,
                                 cte.SUNDAY]
          _values = usage_zone_variant['endUses']['space_cooling']['schedule']['weekDayProfile']['values']
          while '  ' in _values:
            _values = _values.replace('  ', ' ')
          _values = _values.split()
          _values_float = []
          for _value in _values:
            _values_float.append(float(_value))
          _schedule.values = _values_float
          _thermal_control.cooling_set_point_schedules = [_schedule]

      usage_zone_archetype.thermal_control = _thermal_control

      if 'ventilation' in usage_zone_variant['endUses'] and usage_zone_variant['endUses']['ventilation'] is not None:
        usage_zone_archetype.mechanical_air_change = \
          usage_zone_variant['endUses']['ventilation']['mechanicalAirChangeRate']

    if 'appliance' in usage_zone_variant:
      _appliances = Appliances()
      _appliances.density = usage_zone_variant['appliance']['#text']   # todo: check units

      usage_zone_archetype.appliances = _appliances

    return usage_zone_archetype

  def _search_archetype(self, libs_usage):
    building_usage = UsageHelper().hft_from_libs_usage(libs_usage)
    for building_archetype in self._usage_archetypes:
      if building_archetype.usage == building_usage:
        return building_archetype
    return None

  @staticmethod
  def _assign_values(usage, archetype):
    usage_zone = UsageZone()
    usage_zone.usage = usage
    usage_zone.internal_gains = copy.deepcopy(archetype.internal_gains)
    usage_zone.mechanical_air_change = archetype.mechanical_air_change
    usage_zone.occupancy = copy.deepcopy(archetype.occupancy)
    usage_zone.appliances = copy.deepcopy(archetype.appliances)
    usage_zone.thermal_control = copy.deepcopy(archetype.thermal_control)
    usage_zone.days_year = archetype.days_year
    usage_zone.hours_day = archetype.hours_day
    return usage_zone
