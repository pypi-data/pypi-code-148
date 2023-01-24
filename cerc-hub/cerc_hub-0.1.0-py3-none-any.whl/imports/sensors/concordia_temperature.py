"""
Concordia temperature
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
import pandas as pd
from imports.sensors.concordia_file_report import ConcordiaFileReport
from city_model_structure.iot.concordia_temperature_sensor import ConcordiaTemperatureSensor


class ConcordiaTemperature(ConcordiaFileReport):
  """
  Concordia temperature sensor class
  """
  def __init__(self, city, end_point, base_path):
    super().__init__(city, end_point, base_path, 'concordia_temperature_db.json')
    for city_object in city.city_objects:
      self._assign_sensor_to_object(city_object)

  def _assign_sensor_to_object(self, obj):
    for i in range(len(self._city_object)):
      if self._city_object[i] == obj.name and self._sensors[i] in self._sensor_point:
        building_measures = [self._measures["Date time"], self._measures[self._sensor_point[self._sensors[i]]]]
        building_headers = ["Date time", "Temperature"]
        building_energy_consumption = pd.concat(building_measures, keys=building_headers, axis=1)
        sensor = ConcordiaTemperatureSensor(self._sensors[i])
        sensor_exist = False
        for j in range(len(obj.sensors)):
          if obj.sensors[j].name is sensor.name:
            obj.sensors[j].add_period(building_energy_consumption)
            sensor_exist = True
            break
        if not sensor_exist:
          sensor.add_period(building_energy_consumption)
          obj.sensors.append(sensor)
