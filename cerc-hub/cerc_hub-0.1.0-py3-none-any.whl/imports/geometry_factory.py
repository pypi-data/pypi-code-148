"""
GeometryFactory retrieve the specific geometric module to load the given format
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""

import geopandas
from city_model_structure.city import City
from imports.geometry.citygml import CityGml
from imports.geometry.obj import Obj
from imports.geometry.osm_subway import OsmSubway
from imports.geometry.rhino import Rhino
from imports.geometry.gpandas import GPandas
from imports.geometry.geojson import Geojson


class GeometryFactory:
  """
  GeometryFactory class
  """
  def __init__(self, file_type,
               path=None,
               data_frame=None,
               height_field=None,
               year_of_construction_field=None,
               function_field=None):
    self._file_type = '_' + file_type.lower()
    self._path = path
    self._data_frame = data_frame
    self._height_field = height_field
    self._year_of_construction_field = year_of_construction_field
    self._function_field = function_field

  @property
  def _citygml(self) -> City:
    """
    Enrich the city by using CityGML information as data source
    :return: City
    """
    return CityGml(self._path, self._height_field, self._year_of_construction_field, self._function_field).city

  @property
  def _obj(self) -> City:
    """
    Enrich the city by using OBJ information as data source
    :return: City
    """
    return Obj(self._path).city
    
  @property
  def _gpandas(self) -> City:
    """
    Enrich the city by using GeoPandas information as data source
    :return: City
    """
    if self._data_frame is None:
      self._data_frame = geopandas.read_file(self._path)
    return GPandas(self._data_frame).city

  @property
  def _geojson(self) -> City:
    """
    Enrich the city by using Geojson information as data source
    :return: City
    """
    return Geojson(self._path, self._height_field, self._year_of_construction_field, self._function_field).city

  @property
  def _osm_subway(self) -> City:
    """
    Enrich the city by using OpenStreetMap information as data source
    :return: City
    """
    return OsmSubway(self._path).city

  @property
  def _rhino(self) -> City:
    """
    Enrich the city by using Rhino information as data source
    :return: City
    """
    return Rhino(self._path).city

  @property
  def city(self) -> City:
    """
    Enrich the city given to the class using the class given handler
    :return: City
    """
    return getattr(self, self._file_type, lambda: None)

  @property
  def city_debug(self) -> City:
    """
    Enrich the city given to the class using the class given handler
    :return: City
    """
    return Geojson(self._path, self._height_field, self._year_of_construction_field, self._function_field).city
