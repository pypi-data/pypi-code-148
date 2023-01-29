# Copyright (C) 2023 Jan Tschada (gisfromscratch@live.de)
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
import requests

from .client import GeoRapidClient
from .formats import OutFormat



def aggregate(client: GeoRapidClient, date: datetime = datetime(2022, 2, 24), format = OutFormat.GEOJSON):
    """
    Aggregates the armed conflict events using a spatial grid and returns the features as hexagonal bins.
    You must define a specific date intersecting the valid date extent.
    The underlying event database collects data since 2020-01-01. 
    The format can be GeoJSON or Esri JSON.
    """
    endpoint = '{0}/aggregate'.format(client.url)
    params = {
        'format': str(format)
    }
    if date:
        params['date'] = datetime.strftime(date, '%Y-%m-%d')

    response = requests.request('GET', endpoint, headers=client.auth_headers, params=params)
    response.raise_for_status()
    return response.json()

def cluster(client: GeoRapidClient, date: datetime = datetime(2022, 2, 24), format = OutFormat.GEOJSON):
    """
    Creates spatial clusters using the armed conflict events and returns the features as cluster polygons. 
    You must define a specific date intersecting the valid date extent.
    The underlying event database collects data since 2020-01-01. 
    The format can be GeoJSON or Esri JSON.
    """
    endpoint = '{0}/cluster'.format(client.url)
    params = {
        'format': str(format)
    }
    if date:
        params['date'] = datetime.strftime(date, '%Y-%m-%d')

    response = requests.request('GET', endpoint, headers=client.auth_headers, params=params)
    response.raise_for_status()
    return response.json()

def count(client: GeoRapidClient):
    """
    Returns the number of armed conflict events as a JSON result.
    """
    endpoint = '{0}/count'.format(client.url)
    response = requests.request('GET', endpoint, headers=client.auth_headers)
    response.raise_for_status()
    return response.json()

def date_extent(client: GeoRapidClient):
    """
    Returns the valid date extent (start and end date) of the armed conflict events as a JSON result.
    """
    endpoint = '{0}/dateExtent'.format(client.url)
    response = requests.request('GET', endpoint, headers=client.auth_headers)
    response.raise_for_status()
    return response.json()

def extent(client: GeoRapidClient):
    """
    Returns the valid spatial extent (xmin, ymin, xmax, ymax) of the armed conflict events as a JSON result.
    """
    endpoint = '{0}/extent'.format(client.url)
    response = requests.request('GET', endpoint, headers=client.auth_headers)
    response.raise_for_status()
    return response.json()

def query(client: GeoRapidClient, date: datetime = datetime(2022, 2, 24), format = OutFormat.GEOJSON):
    """
    Queries the armed conflict events and returns the events as features.
    You must define a specific date intersecting the valid date extent.
    The underlying event database collects data since 2020-01-01.
    The format can be GeoJSON or Esri JSON.
    """
    endpoint = '{0}/query'.format(client.url)
    params = {
        'format': str(format)
    }
    if date:
        params['date'] = datetime.strftime(date, '%Y-%m-%d')

    response = requests.request('GET', endpoint, headers=client.auth_headers, params=params)
    response.raise_for_status()
    return response.json()