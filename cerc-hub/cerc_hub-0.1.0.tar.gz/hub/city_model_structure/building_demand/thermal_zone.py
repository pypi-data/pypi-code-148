"""
ThermalZone module
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import uuid
import copy
import numpy
from typing import List, Union, TypeVar
from city_model_structure.building_demand.occupancy import Occupancy
from city_model_structure.building_demand.appliances import Appliances
from city_model_structure.building_demand.lighting import Lighting
from city_model_structure.building_demand.internal_gain import InternalGain
from city_model_structure.building_demand.thermal_control import ThermalControl
from city_model_structure.attributes.schedule import Schedule
import helpers.constants as cte

ThermalBoundary = TypeVar('ThermalBoundary')
InternalZone = TypeVar('InternalZone')


class ThermalZone:
  """
  ThermalZone class
  """
  def __init__(self, thermal_boundaries, parent_internal_zone, volume, footprint_area, usage=None):
    self._id = None
    self._parent_internal_zone = parent_internal_zone
    self._footprint_area = footprint_area
    self._thermal_boundaries = thermal_boundaries
    self._additional_thermal_bridge_u_value = None
    self._effective_thermal_capacity = None
    self._indirectly_heated_area_ratio = None
    self._infiltration_rate_system_on = None
    self._infiltration_rate_system_off = None
    self._volume = volume
    self._ordinate_number = None
    self._view_factors_matrix = None
    self._total_floor_area = None
    self._usage = usage
    self._usage_from_parent = False
    if usage is None:
      self._usage_from_parent = True
    self._hours_day = None
    self._days_year = None
    self._mechanical_air_change = None
    self._occupancy = None
    self._lighting = None
    self._appliances = None
    self._internal_gains = None
    self._thermal_control = None
    self._usages = None

  @property
  def usage_zones(self):
    # example 70-office_30-residential
    if self._usage_from_parent:
      self._usages = copy.deepcopy(self._parent_internal_zone.usage_zones)
    else:
      values = self._usage.split('_')
      usages = []
      for value in values:
        usages.append(value.split('-'))
      self._usages = []
      for parent_usage in self._parent_internal_zone.usage_zones:
        for value in usages:
          if parent_usage.usage == value[1]:
            new_usage = copy.deepcopy(parent_usage)
            new_usage.percentage = float(value[0])/100
            self._usages.append(new_usage)
    return self._usages

  @property
  def id(self):
    """
    Get thermal zone id, a universally unique identifier randomly generated
    :return: str
    """
    if self._id is None:
      self._id = uuid.uuid4()
    return self._id

  @property
  def footprint_area(self) -> float:
    """
    Get thermal zone footprint area in m2
    :return: float
    """
    return self._footprint_area

  @property
  def thermal_boundaries(self) -> [ThermalBoundary]:
    """
    Get thermal boundaries bounding with the thermal zone
    :return: [ThermalBoundary]
    """
    return self._thermal_boundaries

  @property
  def additional_thermal_bridge_u_value(self) -> Union[None, float]:
    """
    Get thermal zone additional thermal bridge u value per footprint area W/m2K
    :return: None or float
    """
    return self._additional_thermal_bridge_u_value

  @additional_thermal_bridge_u_value.setter
  def additional_thermal_bridge_u_value(self, value):
    """
    Set thermal zone additional thermal bridge u value per footprint area W/m2K
    :param value: float
    """
    if value is not None:
      self._additional_thermal_bridge_u_value = float(value)

  @property
  def effective_thermal_capacity(self) -> Union[None, float]:
    """
    Get thermal zone effective thermal capacity in J/m2K
    :return: None or float
    """
    return self._effective_thermal_capacity

  @effective_thermal_capacity.setter
  def effective_thermal_capacity(self, value):
    """
    Set thermal zone effective thermal capacity in J/m2K
    :param value: float
    """
    if value is not None:
      self._effective_thermal_capacity = float(value)

  @property
  def indirectly_heated_area_ratio(self) -> Union[None, float]:
    """
    Get thermal zone indirectly heated area ratio
    :return: None or float
    """
    return self._indirectly_heated_area_ratio

  @indirectly_heated_area_ratio.setter
  def indirectly_heated_area_ratio(self, value):
    """
    Set thermal zone indirectly heated area ratio
    :param value: float
    """
    if value is not None:
      self._indirectly_heated_area_ratio = float(value)

  @property
  def infiltration_rate_system_on(self):
    """
    Get thermal zone infiltration rate system on in air changes per hour (ACH)
    :return: None or float
    """
    return self._infiltration_rate_system_on

  @infiltration_rate_system_on.setter
  def infiltration_rate_system_on(self, value):
    """
    Set thermal zone infiltration rate system on in air changes per hour (ACH)
    :param value: float
    """
    self._infiltration_rate_system_on = value

  @property
  def infiltration_rate_system_off(self):
    """
    Get thermal zone infiltration rate system off in air changes per hour (ACH)
    :return: None or float
    """
    return self._infiltration_rate_system_off

  @infiltration_rate_system_off.setter
  def infiltration_rate_system_off(self, value):
    """
    Set thermal zone infiltration rate system on in air changes per hour (ACH)
    :param value: float
    """
    self._infiltration_rate_system_off = value

  @property
  def volume(self):
    """
    Get thermal zone volume
    :return: float
    """
    return self._volume

  @property
  def ordinate_number(self) -> Union[None, int]:
    """
    Get the order in which the thermal_zones need to be enumerated
    :return: None or int
    """
    return self._ordinate_number

  @ordinate_number.setter
  def ordinate_number(self, value):
    """
    Set a specific order of the zones to be called
    :param value: int
    """
    if value is not None:
      self._ordinate_number = int(value)

  @property
  def view_factors_matrix(self):
    """
    Get thermal zone view factors matrix
    :return: [[float]]
    """
    return self._view_factors_matrix

  @view_factors_matrix.setter
  def view_factors_matrix(self, value):
    """
    Set thermal zone view factors matrix
    :param value: [[float]]
    """
    self._view_factors_matrix = value

  @property
  def usage(self) -> Union[None, str]:
    """
    Get thermal zone usage
    :return: None or str
    """
    if self._usage_from_parent:
      if self._parent_internal_zone.usage_zones is None:
        return None
      self._usage = ''
      for usage_zone in self._parent_internal_zone.usage_zones:
        self._usage += str(round(usage_zone.percentage * 100)) + '-' + usage_zone.usage + '_'
      self._usage = self._usage[:-1]
    return self._usage

  @staticmethod
  def _get_schedule_of_day(requested_day_type, schedules):
    for schedule in schedules:
      for day_type in schedule.day_types:
        if day_type == requested_day_type:
          return schedule
      return None

  @property
  def hours_day(self) -> Union[None, float]:
    """
    Get thermal zone usage hours per day
    :return: None or float
    """
    if self.usage_zones is None:
      return None
    if self._hours_day is None:
      self._hours_day = 0
      for usage_zone in self.usage_zones:
        self._hours_day += usage_zone.percentage * usage_zone.hours_day
    return self._hours_day

  @property
  def days_year(self) -> Union[None, float]:
    """
    Get thermal zone usage days per year
    :return: None or float
    """
    if self.usage_zones is None:
      return None
    if self._days_year is None:
      self._days_year = 0
      for usage_zone in self.usage_zones:
        self._days_year += usage_zone.percentage * usage_zone.days_year
    return self._days_year

  @property
  def mechanical_air_change(self) -> Union[None, float]:
    """
    Get thermal zone mechanical air change in air change per hour (ACH)
    :return: None or float
    """
    if self.usage_zones is None:
      return None
    if self._mechanical_air_change is None:
      self._mechanical_air_change = 0
      for usage_zone in self.usage_zones:
        if usage_zone.mechanical_air_change is None:
          return None
        self._mechanical_air_change += usage_zone.percentage * usage_zone.mechanical_air_change
    return self._mechanical_air_change

  @property
  def occupancy(self) -> Union[None, Occupancy]:
    """
    Get occupancy in the thermal zone
    :return: None or Occupancy
    """
    if self.usage_zones is None:
      return None

    if self._occupancy is None:
      self._occupancy = Occupancy()
      _occupancy_density = 0
      _convective_part = 0
      _radiative_part = 0
      _latent_part = 0
      for usage_zone in self.usage_zones:
        if usage_zone.occupancy is None:
          return None
        _occupancy_density += usage_zone.percentage * usage_zone.occupancy.occupancy_density
        if usage_zone.occupancy.sensible_convective_internal_gain is not None:
          _convective_part += usage_zone.percentage * usage_zone.occupancy.sensible_convective_internal_gain
          _radiative_part += usage_zone.percentage * usage_zone.occupancy.sensible_radiative_internal_gain
          _latent_part += usage_zone.percentage * usage_zone.occupancy.latent_internal_gain
      self._occupancy.occupancy_density = _occupancy_density
      self._occupancy.sensible_convective_internal_gain = _convective_part
      self._occupancy.sensible_radiative_internal_gain = _radiative_part
      self._occupancy.latent_internal_gain = _latent_part

      _occupancy_reference = self.usage_zones[0].occupancy
      if _occupancy_reference.occupancy_schedules is not None:
        _schedules = []
        for i_schedule in range(0, len(_occupancy_reference.occupancy_schedules)):
          schedule = copy.deepcopy(_occupancy_reference.occupancy_schedules[i_schedule])
          new_values = []
          for i_value in range(0, len(_occupancy_reference.occupancy_schedules[i_schedule].values)):
            _new_value = 0
            for usage_zone in self.usage_zones:
              _new_value += usage_zone.percentage * usage_zone.occupancy.occupancy_schedules[i_schedule].values[i_value]
            new_values.append(_new_value)
          schedule.values = new_values
          _schedules.append(schedule)
        self._occupancy.occupancy_schedules = _schedules
    return self._occupancy

  @property
  def lighting(self) -> Union[None, Lighting]:
    """
    Get lighting information
    :return: None or Lighting
    """
    if self.usage_zones is None:
      return None

    if self._lighting is None:
      self._lighting = Lighting()
      _lighting_density = 0
      _convective_part = 0
      _radiative_part = 0
      _latent_part = 0
      for usage_zone in self.usage_zones:
        if usage_zone.lighting is None:
          return None
        _lighting_density += usage_zone.percentage * usage_zone.lighting.density
        if usage_zone.lighting.convective_fraction is not None:
          _convective_part += usage_zone.percentage * usage_zone.lighting.density \
                               * usage_zone.lighting.convective_fraction
          _radiative_part += usage_zone.percentage * usage_zone.lighting.density \
                             * usage_zone.lighting.radiative_fraction
          _latent_part += usage_zone.percentage * usage_zone.lighting.density \
                          * usage_zone.lighting.latent_fraction
      self._lighting.density = _lighting_density
      if _lighting_density > 0:
        self._lighting.convective_fraction = _convective_part / _lighting_density
        self._lighting.radiative_fraction = _radiative_part / _lighting_density
        self._lighting.latent_fraction = _latent_part / _lighting_density
      else:
        self._lighting.convective_fraction = 0
        self._lighting.radiative_fraction = 0
        self._lighting.latent_fraction = 0

      _lighting_reference = self.usage_zones[0].lighting
      if _lighting_reference.schedules is not None:
        _schedules = []
        for i_schedule in range(0, len(_lighting_reference.schedules)):
          schedule = copy.deepcopy(_lighting_reference.schedules[i_schedule])
          new_values = []
          for i_value in range(0, len(_lighting_reference.schedules[i_schedule].values)):
            _new_value = 0
            for usage_zone in self.usage_zones:
              _new_value += usage_zone.percentage * usage_zone.lighting.schedules[i_schedule].values[i_value]
            new_values.append(_new_value)
          schedule.values = new_values
          _schedules.append(schedule)
        self._lighting.schedules = _schedules
    return self._lighting

  @property
  def appliances(self) -> Union[None, Appliances]:
    """
    Get appliances information
    :return: None or Appliances
    """
    if self.usage_zones is None:
      return None

    if self._appliances is None:
      self._appliances = Appliances()
      _appliances_density = 0
      _convective_part = 0
      _radiative_part = 0
      _latent_part = 0
      for usage_zone in self.usage_zones:
        if usage_zone.appliances is None:
          return None
        _appliances_density += usage_zone.percentage * usage_zone.appliances.density
        if usage_zone.appliances.convective_fraction is not None:
          _convective_part += usage_zone.percentage * usage_zone.appliances.density \
                              * usage_zone.appliances.convective_fraction
          _radiative_part += usage_zone.percentage * usage_zone.appliances.density \
                             * usage_zone.appliances.radiative_fraction
          _latent_part += usage_zone.percentage * usage_zone.appliances.density \
                          * usage_zone.appliances.latent_fraction
      self._appliances.density = _appliances_density
      if _appliances_density > 0:
        self._appliances.convective_fraction = _convective_part / _appliances_density
        self._appliances.radiative_fraction = _radiative_part / _appliances_density
        self._appliances.latent_fraction = _latent_part / _appliances_density
      else:
        self._appliances.convective_fraction = 0
        self._appliances.radiative_fraction = 0
        self._appliances.latent_fraction = 0

      _appliances_reference = self.usage_zones[0].appliances
      if _appliances_reference.schedules is not None:
        _schedules = []
        for i_schedule in range(0, len(_appliances_reference.schedules)):
          schedule = copy.deepcopy(_appliances_reference.schedules[i_schedule])
          new_values = []
          for i_value in range(0, len(_appliances_reference.schedules[i_schedule].values)):
            _new_value = 0
            for usage_zone in self.usage_zones:
              _new_value += usage_zone.percentage * usage_zone.appliances.schedules[i_schedule].values[i_value]
            new_values.append(_new_value)
          schedule.values = new_values
          _schedules.append(schedule)
        self._appliances.schedules = _schedules
    return self._appliances

  @property
  def internal_gains(self) -> Union[None, List[InternalGain]]:
    """
    Calculates and returns the list of all internal gains defined
    :return: [InternalGain]
    """
    if self.usage_zones is None:
      return None

    if self._internal_gains is None:
      _internal_gain = InternalGain()
      _days = [cte.MONDAY, cte.TUESDAY, cte.WEDNESDAY, cte.THURSDAY, cte.FRIDAY, cte.SATURDAY, cte.SUNDAY, cte.HOLIDAY]
      _average_internal_gain = 0
      _convective_fraction = 0
      _radiative_fraction = 0
      _latent_fraction = 0
      _schedules = None
      _base_schedule = Schedule()
      _base_schedule.type = cte.INTERNAL_GAINS
      _base_schedule.time_range = cte.DAY
      _base_schedule.time_step = cte.HOUR
      _base_schedule.data_type = cte.ANY_NUMBER
      _schedules_defined = True
      values = numpy.zeros([24, 8])
      for usage_zone in self.usage_zones:
        for internal_gain in usage_zone.internal_gains:
          _average_internal_gain += internal_gain.average_internal_gain * usage_zone.percentage
          _convective_fraction += internal_gain.average_internal_gain * usage_zone.percentage \
                                  * internal_gain.convective_fraction
          _radiative_fraction += internal_gain.average_internal_gain * usage_zone.percentage \
                                 * internal_gain.radiative_fraction
          _latent_fraction += internal_gain.average_internal_gain * usage_zone.percentage \
                              * internal_gain.latent_fraction
      for usage_zone in self.usage_zones:
        for internal_gain in usage_zone.internal_gains:
          if internal_gain.schedules is None:
            _schedules_defined = False
            break
          if len(internal_gain.schedules) == 0:
            _schedules_defined = False
            break
          for day, _schedule in enumerate(internal_gain.schedules):
            for v, value in enumerate(_schedule.values):
              values[v, day] += value * usage_zone.percentage

      if _schedules_defined:
        _schedules = []
        for day in range(0, len(_days)):
          _schedule = copy.deepcopy(_base_schedule)
          _schedule.day_types = [_days[day]]
          _schedule.values = values[:day]
          _schedules.append(_schedule)

      _internal_gain.convective_fraction = _convective_fraction / _average_internal_gain
      _internal_gain.radiative_fraction = _radiative_fraction / _average_internal_gain
      _internal_gain.latent_fraction = _latent_fraction / _average_internal_gain
      _internal_gain.average_internal_gain = _average_internal_gain
      _internal_gain.type = 'mean_value'
      _internal_gain.schedules = _schedules
      self._internal_gains = [_internal_gain]
    return self._internal_gains

  @property
  def thermal_control(self) -> Union[None, ThermalControl]:
    """
    Get thermal control of this thermal zone
    :return: None or ThermalControl
    """
    if self.usage_zones is None:
      return None

    if self._thermal_control is None:
      self._thermal_control = ThermalControl()
      _mean_heating_set_point = 0
      _heating_set_back = 0
      _mean_cooling_set_point = 0
      for usage_zone in self.usage_zones:
        _mean_heating_set_point += usage_zone.percentage * usage_zone.thermal_control.mean_heating_set_point
        _heating_set_back += usage_zone.percentage * usage_zone.thermal_control.heating_set_back
        _mean_cooling_set_point += usage_zone.percentage * usage_zone.thermal_control.mean_cooling_set_point
      self._thermal_control.mean_heating_set_point = _mean_heating_set_point
      self._thermal_control.heating_set_back = _heating_set_back
      self._thermal_control.mean_cooling_set_point = _mean_cooling_set_point

      _thermal_control_reference = self.usage_zones[0].thermal_control
      _types_reference = []
      if _thermal_control_reference.hvac_availability_schedules is not None:
        _types_reference.append([cte.HVAC_AVAILABILITY, _thermal_control_reference.hvac_availability_schedules])
      if _thermal_control_reference.heating_set_point_schedules is not None:
        _types_reference.append([cte.HEATING_SET_POINT, _thermal_control_reference.heating_set_point_schedules])
      if _thermal_control_reference.cooling_set_point_schedules is not None:
        _types_reference.append([cte.COOLING_SET_POINT, _thermal_control_reference.cooling_set_point_schedules])

      for i_type in range(0, len(_types_reference)):
        _schedules = []
        _schedule_type = _types_reference[i_type][1]
        for i_schedule in range(0, len(_schedule_type)):
          schedule = copy.deepcopy(_schedule_type[i_schedule])
          new_values = []
          for i_value in range(0, len(_schedule_type[i_schedule].values)):
            _new_value = 0
            for usage_zone in self.usage_zones:
              if _types_reference[i_type][0] == cte.HVAC_AVAILABILITY:
                _new_value += usage_zone.percentage * \
                              usage_zone.thermal_control.hvac_availability_schedules[i_schedule].values[i_value]
              elif _types_reference[i_type][0] == cte.HEATING_SET_POINT:
                _new_value += usage_zone.percentage * \
                              usage_zone.thermal_control.heating_set_point_schedules[i_schedule].values[i_value]
              elif _types_reference[i_type][0] == cte.COOLING_SET_POINT:
                _new_value += usage_zone.percentage * \
                              usage_zone.thermal_control.cooling_set_point_schedules[i_schedule].values[i_value]
            new_values.append(_new_value)
          schedule.values = new_values
          _schedules.append(schedule)
        if i_type == 0:
          self._thermal_control.hvac_availability_schedules = _schedules
        elif i_type == 1:
          self._thermal_control.heating_set_point_schedules = _schedules
        elif i_type == 2:
          self._thermal_control.cooling_set_point_schedules = _schedules

    return self._thermal_control

  @property
  def total_floor_area(self):
    """
    Get the total floor area of this thermal zone
    :return: float
    """
    return self._total_floor_area

  @total_floor_area.setter
  def total_floor_area(self, value):
    """
    Set the total floor area of this thermal zone
    :param value: float
    """
    self._total_floor_area = value
