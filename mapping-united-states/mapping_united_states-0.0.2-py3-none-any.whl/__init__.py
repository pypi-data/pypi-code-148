import csv
import datetime
import os
from time import sleep
from typing import Optional
from zipfile import ZipFile

import geopandas as gpd
import pandas as pd

import requests


class CensusData:
    def __init__(self, census_year: int = 2022, cache_directory: Optional[str] = './caching/',
                 delay_between_requests_in_seconds: Optional[int] = 3):
        self.last_request = datetime.datetime.now() - datetime.timedelta(hours=1)
        self.census_year = census_year
        self.cache_directory = cache_directory
        self.delay_between_requests_in_seconds = delay_between_requests_in_seconds

    def get_counties_by_fips_code(self, fips_code: str) -> []:
        request_name = f'{self.census_year}_gaz_counties_{fips_code}.txt'
        filename = self.__get_cache_full_path('COUNTY', request_name)

        if not os.path.exists(filename):
            url = f'https://www2.census.gov/geo/docs/maps-data/data/gazetteer/{self.census_year}_Gazetteer/{request_name}'
            self.__download_file(
                url,
                filename
            )

        ret = []

        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:
                ret.append(row)

        return ret

    def get_states_info(self) -> {}:
        filename = self.__get_cache_full_path('STATE', 'state.psv')

        if not os.path.exists(filename):
            self.__download_file(
                'https://www2.census.gov/geo/docs/reference/state.txt',
                filename
            )

        ret = {}

        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='|')

            for row in reader:
                ret[row['STUSAB']] = row

        return ret

    def get_primary_roads(self) -> gpd.GeoDataFrame:
        return self.__default_shapes_download(
            'PRIMARYROADS',
            f'tl_{self.census_year}_us_primaryroads'
        )

    def get_states(self) -> gpd.GeoDataFrame:
        return self.__default_shapes_download(
            'STATE',
            f'tl_{self.census_year}_us_state'
        )

    def get_primary_and_secondary_roads_in_state(self, fips_code: str) -> gpd.GeoDataFrame:
        return self.__default_shapes_download(
            'PRISECROADS',
            f'tl_{self.census_year}_{fips_code}_prisecroads'
        )

    def get_area_water_for_county(self, county_geoid: str) -> gpd.GeoDataFrame:
        return self.__default_shapes_download(
            'AREAWATER',
            f'tl_{self.census_year}_{county_geoid}_areawater'
        )

    def get_places_in_state(self, fips_code: str) -> gpd.GeoDataFrame:
        return self.__default_shapes_download(
            'PLACE',
            f'tl_{self.census_year}_{fips_code}_place'
        )

    def get_counties(self) -> gpd.GeoDataFrame:
        return self.__default_shapes_download(
            'COUNTY',
            f'tl_{self.census_year}_us_county'
        )

    def get_rail_roads(self) -> gpd.GeoDataFrame:
        return self.__default_shapes_download(
            'RAILS',
            f'tl_{self.census_year}_us_rails'
        )

    def get_roads_for_county(self, county_geoid: str) -> gpd.GeoDataFrame:
        return self.__default_shapes_download(
            'ROADS',
            f'tl_{self.census_year}_{county_geoid}_roads'
        )

    def __generate_tiger_url(self, resource: str, filename: str) -> str:
        return f'https://www2.census.gov/geo/tiger/TIGER{self.census_year}/{resource}/{filename}'

    def __default_shapes_download(self, resource: str, base_filename: str):
        url_filename = f'{base_filename}.zip'
        filename = self.__get_cache_full_path(resource, f'{base_filename}.shp')
        temp_path = self.__get_cache_full_path(resource, url_filename)
        url = self.__generate_tiger_url(resource, url_filename)

        return self.__cache_zip_shapes_file(
            filename,
            temp_path,
            url
        )

    def __get_cache_full_path(self, cache_folder, filename):
        cache_directory = os.path.join(self.cache_directory, cache_folder, filename)
        if not os.path.exists(cache_directory):
            os.makedirs(cache_directory)

        location = os.path.join(cache_directory, filename)

        return location

    def __cache_zip_shapes_file(self, cache_file: str, temp_path: str, url: str) -> gpd.GeoDataFrame:
        if not os.path.exists(cache_file):
            if not os.path.exists(temp_path):
                self.__download_file(url, temp_path)

            with ZipFile(temp_path, 'r') as zObject:
                zObject.extractall(path=os.path.dirname(cache_file))

            os.remove(temp_path)

        return gpd.read_file(cache_file)

    def __download_file(self, url: str, filename: str):
        seconds = (datetime.datetime.now() - self.last_request).total_seconds()

        if seconds < self.delay_between_requests_in_seconds:
            wait_time = self.delay_between_requests_in_seconds - seconds
            sleep(wait_time)

        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        self.last_request = datetime.datetime.now()
