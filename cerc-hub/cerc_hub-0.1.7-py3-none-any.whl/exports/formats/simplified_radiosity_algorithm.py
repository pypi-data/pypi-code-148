"""
Simplified Radiosity Algorithm
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guillermo.GutierrezMorote@concordia.ca
"""
import xmltodict


class SimplifiedRadiosityAlgorithm:
  """
  Export to SRA format
  """
  def __init__(self, city, file_name, target_buildings=None, begin_month=1, begin_day=1, end_month=12, end_day=31):
    self._file_name = file_name
    self._begin_month = begin_month
    self._begin_day = begin_day
    self._end_month = end_month
    self._end_day = end_day
    self._city = city
    self._target_buildings = target_buildings
    self._export()

  def _correct_point(self, point):
    # correct the x, y, z values into the reference frame set by city lower_corner
    x = point[0] - self._city.lower_corner[0]
    y = point[1] - self._city.lower_corner[1]
    z = point[2] - self._city.lower_corner[2]
    return [x, y, z]

  def _export(self):
    buildings = []
    for building_index, building in enumerate(self._city.buildings):
      if self._target_buildings is None:
        simulate = 'true'
      else:
        simulate = 'false'
        for target_building in self._target_buildings:
          if building.name == target_building.name:
            simulate = 'true'
      building_dict = {
        '@Name': f'{building.name}',
        '@id': f'{building_index}',
        '@key': f'{building.name}',
        '@Simulate': f'{simulate}'
      }
      walls, roofs, floors = [], [], []
      for surface in building.surfaces:
        surface_dict = {
          '@id': f'{surface.id}',
          '@ShortWaveReflectance': f'{surface.short_wave_reflectance}'
        }
        for point_index, point in enumerate(surface.perimeter_polygon.coordinates):
          point = self._correct_point(point)
          surface_dict[f'V{point_index}'] = {
            '@x': f'{point[0]}',
            '@y': f'{point[1]}',
            '@z': f'{point[2]}'
          }
        if surface.type == 'Wall':
          walls.append(surface_dict)
        elif surface.type == 'Roof':
          roofs.append(surface_dict)
        else:
          floors.append(surface_dict)
      building_dict['Wall'] = walls
      building_dict['Roof'] = roofs
      building_dict['Floor'] = floors
      buildings.append(building_dict)
    sra = {
      'CitySim': {
        '@name': f'{self._file_name.name}',
        'Simulation': {
          '@beginMonth': f'{self._begin_month}',
          '@beginDay': f'{self._begin_day}',
          '@endMonth': f'{self._end_month}',
          '@endDay': f'{self._end_day}',
        },
        'Climate': {
          '@location': f'{self._city.climate_file}',
          '@city': f'{self._city.climate_reference_city}'
        },
        'District': {
          'FarFieldObstructions': None,
          'Building': buildings
        }
      }
    }
    with open(self._file_name, "w") as file:
      file.write(xmltodict.unparse(sra, pretty=True, short_empty_elements=True))
