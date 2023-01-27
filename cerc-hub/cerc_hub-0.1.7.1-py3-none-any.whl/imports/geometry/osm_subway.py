"""
OsmSubway module parses osm files and import the metro location into the city model structure
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""

import sys
import xmltodict
from pyproj import Transformer
from hub.city_model_structure.city import City
from hub.city_model_structure.subway_entrance import SubwayEntrance


class OsmSubway:
  """
  Open street map subway
  """
  def __init__(self, path):
    self._city = None
    self._subway_entrances = []
    with open(path) as osm:
      self._osm = xmltodict.parse(osm.read(), force_list='tag')
      for node in self._osm['osm']['node']:
        if 'tag' not in node:
          continue
        for tag in node['tag']:
          if '@v' not in tag:
            continue
          if tag['@v'] == 'subway_entrance':
            subway_entrance = SubwayEntrance(node['@id'], node['@lat'], node['@lon'])
            self._subway_entrances.append(subway_entrance)

  @property
  def city(self) -> City:
    """
    Get a city with subway entrances
    """
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857")
    lower_corner = [sys.float_info.max, sys.float_info.max, 0]
    upper_corner = [sys.float_info.min, sys.float_info.min, 0]
    x = 0
    y = 1
    for subway_entrance in self._subway_entrances:
      coordinate = transformer.transform(subway_entrance.longitude, subway_entrance.latitude)
      if coordinate[x] >= upper_corner[x]:
        upper_corner[x] = coordinate[x]
      if coordinate[y] >= upper_corner[y]:
        upper_corner[y] = coordinate[y]
      if coordinate[x] < lower_corner[x]:
        lower_corner[x] = coordinate[x]
      if coordinate[y] < lower_corner[y]:
        lower_corner[y] = coordinate[y]

    city = City(lower_corner, upper_corner, 'unknown')
    for subway_entrance in self._subway_entrances:
      city.add_city_object(subway_entrance)
    return city
