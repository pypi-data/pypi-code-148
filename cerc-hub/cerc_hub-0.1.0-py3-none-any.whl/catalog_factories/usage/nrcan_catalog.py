"""
NRCAN usage catalog
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""

import json
import urllib.request
import xmltodict

import helpers.constants as cte
from catalog_factories.catalog import Catalog
from catalog_factories.data_models.usages.appliances import Appliances
from catalog_factories.data_models.usages.content import Content
from catalog_factories.data_models.usages.lighting import Lighting
from catalog_factories.data_models.usages.ocupancy import Occupancy
from catalog_factories.data_models.usages.schedule import Schedule
from catalog_factories.data_models.usages.thermal_control import ThermalControl
from catalog_factories.data_models.usages.usage import Usage
from catalog_factories.usage.usage_helper import UsageHelper


class NrcanCatalog(Catalog):
  def __init__(self, path):
    path = str(path / 'nrcan.xml')
    self._content = None
    self._schedules = {}
    with open(path) as xml:
      self._metadata = xmltodict.parse(xml.read())
    self._base_url = self._metadata['nrcan']['@base_url']
    self._load_schedules()
    self._content = Content(self._load_archetypes())

  def _calculate_hours_day(self, function):
    # todo: pilar need to check how to calculate this value
    return 24

  @staticmethod
  def _extract_schedule(raw):
    nrcan_schedule_type = raw['category']
    if 'Heating' in raw['name']:
      nrcan_schedule_type = f'{nrcan_schedule_type} Heating'
    elif 'Cooling' in raw['name']:
      nrcan_schedule_type = f'{nrcan_schedule_type} Cooling'
    if nrcan_schedule_type not in UsageHelper().nrcan_schedule_type_to_hub_schedule_type:
      return None
    hub_type = UsageHelper().nrcan_schedule_type_to_hub_schedule_type[nrcan_schedule_type]
    data_type = UsageHelper().nrcan_data_type_to_hub_data_type[raw['units']]
    time_step = UsageHelper().nrcan_time_to_hub_time[raw['type']]
    # nrcan only uses yearly range for the schedules
    time_range = cte.YEAR
    day_types = UsageHelper().nrcan_day_type_to_hub_days[raw['day_types']]
    return Schedule(hub_type, raw['values'], data_type, time_step, time_range, day_types)

  def _load_schedules(self):
    usage = self._metadata['nrcan']['standards']['usage']
    url = f'{self._base_url}{usage["schedules_location"]}'
    with urllib.request.urlopen(url) as json_file:
      schedules_type = json.load(json_file)
    for schedule_type in schedules_type['tables']['schedules']['table']:
      schedule = NrcanCatalog._extract_schedule(schedule_type)
      if schedule is not None:
        self._schedules[schedule_type['name']] = schedule

  def _get_schedule(self, name):
    if name in self._schedules:
      return self._schedules[name]

  def _load_archetypes(self):
    usages = []
    usage = self._metadata['nrcan']['standards']['usage']
    url = f'{self._base_url}{usage["space_types_location"]}'
    with urllib.request.urlopen(url) as json_file:
      space_types = json.load(json_file)['tables']['space_types']['table']
    space_types = [st for st in space_types if st['building_type'] == 'Space Function']
    for space_type in space_types:
      usage_type = space_type['space_type']
      mechanical_air_change = space_type['ventilation_air_changes']
      ventilation_rate = space_type['ventilation_per_area']
      if ventilation_rate == 0:
        ventilation_rate = space_type['ventilation_per_person']
      hours_day = self._calculate_hours_day(usage_type)
      days_year = 365
      occupancy_schedule_name = space_type['occupancy_schedule']
      lighting_schedule_name = space_type['lighting_schedule']
      appliance_schedule_name = space_type['electric_equipment_schedule']
      # thermal control
      heating_setpoint_schedule_name = space_type['heating_setpoint_schedule']
      cooling_setpoint_schedule_name = space_type['cooling_setpoint_schedule']
      occupancy_schedule = self._get_schedule(occupancy_schedule_name)
      lighting_schedule = self._get_schedule(lighting_schedule_name)
      appliance_schedule = self._get_schedule(appliance_schedule_name)
      heating_schedule = self._get_schedule(heating_setpoint_schedule_name)
      cooling_schedule = self._get_schedule(cooling_setpoint_schedule_name)

      occupancy_density = space_type['occupancy_per_area']
      lighting_density = space_type['lighting_per_area']
      lighting_radiative_fraction = space_type['lighting_fraction_radiant']
      if lighting_radiative_fraction is not None:
        lighting_convective_fraction = 1 - lighting_radiative_fraction
      lighting_latent_fraction = 0
      appliances_density = space_type['electric_equipment_per_area']
      appliances_radiative_fraction = space_type['electric_equipment_fraction_radiant']
      if appliances_radiative_fraction is not None:
        appliances_convective_fraction = 1 - appliances_radiative_fraction
      appliances_latent_fraction = space_type['electric_equipment_fraction_latent']

      occupancy = Occupancy(occupancy_density, 0, 0, 0, occupancy_schedule)
      lighting = Lighting(lighting_density,
                          lighting_convective_fraction,
                          lighting_radiative_fraction,
                          lighting_latent_fraction,
                          lighting_schedule)
      appliances = Appliances(appliances_density,
                              appliances_convective_fraction,
                              appliances_radiative_fraction,
                              appliances_latent_fraction,
                              appliance_schedule)
      if heating_schedule is not None:
        thermal_control = ThermalControl(max(heating_schedule.values),
                                         min(heating_schedule.values),
                                         min(cooling_schedule.values),
                                         None,
                                         heating_schedule,
                                         cooling_schedule)
      else:
        thermal_control = ThermalControl(None,
                                         None,
                                         None,
                                         None,
                                         None,
                                         None)
      usages.append(Usage(usage_type,
                          hours_day,
                          days_year,
                          mechanical_air_change,
                          ventilation_rate,
                          occupancy,
                          lighting,
                          appliances,
                          thermal_control))
    return usages

  def names(self, category=None):
    """
    Get the catalog elements names
    :parm: for usage catalog category filter does nothing as there is only one category (usages)
    """
    _names = {'usages': []}
    for usage in self._content.usages:
      _names['usages'].append(usage.usage)
    return _names

  def entries(self, category=None):
    """
    Get the catalog elements
    :parm: for usage catalog category filter does nothing as there is only one category (usages)
    """
    return self._content

  def get_entry(self, name):
    """
    Get one catalog element by names
    :parm: entry name
    """
    for usage in self._content.usages:
      if usage.usage.lower() == name.lower():
        return usage
    raise IndexError(f"{name} doesn't exists in the catalog")
