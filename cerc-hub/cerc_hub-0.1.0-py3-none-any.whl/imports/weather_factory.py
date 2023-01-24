"""
WeatherFactory retrieve the specific weather module for the given source format
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
from pathlib import Path
from imports.weather.xls_weather_parameters import XlsWeatherParameters
from imports.weather.epw_weather_parameters import EpwWeatherParameters


class WeatherFactory:
  """
  WeatherFactory class
  """

  def __init__(self, handler, city, base_path=None, file_name=None):
    if base_path is None:
      base_path = Path(Path(__file__).parent.parent / 'data/weather')
    self._handler = '_' + handler.lower().replace(' ', '_')
    self._city = city
    self._base_path = base_path
    self._file_name = file_name

  def _epw(self):
    """
    Enrich the city with energy plus weather file
    """
    # EnergyPlus Weather
    # to download files: https://energyplus.net/weather
    # description of the format: https://energyplus.net/sites/default/files/pdfs_v8.3.0/AuxiliaryPrograms.pdf
    _path = Path(self._base_path / 'epw').resolve()
    return EpwWeatherParameters(self._city, _path, self._file_name)

  def _xls(self):
    """
    Enrich the city with ISO_52016_1_BESTEST_ClimData_2016.08.24 weather file
    """
    name = 'ISO_52016_1_BESTEST_ClimData_2016.08.24'
    return XlsWeatherParameters(self._city, self._base_path, name)

  def enrich(self):
    """
    Enrich the city given to the class using the given weather handler
    :return: None
    """
    getattr(self, self._handler, lambda: None)()
