# Copyright (C) 2022 Jan Tschada (gisfromscratch@live.de)
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

from georapid.client import GeoRapidClient
from georapid.factory import EnvironmentClientFactory
from georapid.protests import aggregate as aggregate_protests, articles as articles_protests, hotspots as hotspots_protests
from georapid.fires import aggregate as aggregate_fires, articles as articles_fires, query as query_fires
from georapid.conflicts import aggregate as aggregate_conflicts, cluster as cluster_conflicts, count as count_conflicts, date_extent as date_extent_conflicts, extent as extent_conflicts, query as query_conflicts
from georapid.geodetic import create_points_along, create_buffers, create_buffers_from_points, create_points_from_direction, create_path_from_directions, create_wedges, to_azimuth
from georapid.joins import contains, covers, crosses, intersects, overlaps, touches, within
from georapid.geojson import GeoJSON
import unittest

from georapid.units import LinearUnit



class TestConnect(unittest.TestCase):

    def setUp(self) -> None:
        self._latitudes = [51.83864, 50.73438]
        self._longitudes = [12.24555, 7.09549]

    def test_create(self):
        client: GeoRapidClient = EnvironmentClientFactory.create_client()
        self.assertIsNotNone(client, "Client must be initialized!")

    def test_protests_aggregate(self):
        client: GeoRapidClient = EnvironmentClientFactory.create_client()
        geojson = aggregate_protests(client)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")

    def test_protests_articles(self):
        client: GeoRapidClient = EnvironmentClientFactory.create_client()
        json = articles_protests(client)
        self.assertIsNotNone(json, "JSON response must be initialized!")

    def test_host_protests_articles(self):
        host = "geoprotests.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        json = articles_protests(client)
        self.assertIsNotNone(json, "JSON response must be initialized!")

    def test_protests_hotspots(self):
        client: GeoRapidClient = EnvironmentClientFactory.create_client()
        geojson = hotspots_protests(client)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")

    def test_fires_aggregate(self):
        host = "geofires.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        geojson = aggregate_fires(client)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")

    def test_fires_articles(self):
        host = "geofires.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        json = articles_fires(client)
        self.assertIsNotNone(json, "JSON response must be initialized!")

    def test_fires_query(self):
        host = "geofires.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        geojson = query_fires(client)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")

    def test_joins_contains(self):
        host = "geojoins.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        lat = self._latitudes[0]
        lon = self._longitudes[0]
        delta = 0.1
        xmin, xmax, ymin, ymax = lon-delta, lon+delta, lat-delta, lat+delta
        left = { 
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[xmin, ymax], [xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]]
                },
                "properties": {
                    "id": "left_polygon"
                }
            }]
        }
        right = { 
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "properties": {
                    "id": "right_point"
                }
            }]
        }
        geojson = contains(client, left, right)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")
        self.assertTrue('features' in geojson, "GeoJSON response must have features!")
        features = geojson['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")
        self.assertEqual(1, len(features), "One result feature was expected!")

    def test_joins_covers(self):
        host = "geojoins.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        lat = self._latitudes[0]
        lon = self._longitudes[0]
        delta = 0.1
        xmin, xmax, ymin, ymax = lon-delta, lon+delta, lat-delta, lat+delta
        left = { 
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[xmin, ymax], [xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]]
                },
                "properties": {
                    "id": "left_polygon"
                }
            }]
        }
        right = { 
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "properties": {
                    "id": "right_point"
                }
            }]
        }
        geojson = covers(client, left, right)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")
        self.assertTrue('features' in geojson, "GeoJSON response must have features!")
        features = geojson['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")
        self.assertEqual(1, len(features), "One result feature was expected!")

    def test_joins_crosses(self):
        host = "geojoins.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        lat1_start = self._latitudes[0]
        lon1_start = self._longitudes[0]
        lat1_end = -lat1_start
        lon1_end = -lon1_start
        lat2_start = self._latitudes[1]
        lon2_start = self._longitudes[1]
        lat2_end = -lat2_start
        lon2_end = -lon2_start
        left = { 
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[lon1_start, lat1_start], [lon1_end, lat1_end]]
                },
                "properties": {
                    "id": "left_linestring"
                }
            }]
        }
        right = { 
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[lon2_start, lat2_start], [lon2_end, lat2_end]]
                },
                "properties": {
                    "id": "right_linestring"
                }
            }]
        }
        geojson = crosses(client, left, right)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")
        self.assertTrue('features' in geojson, "GeoJSON response must have features!")
        features = geojson['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")
        self.assertEqual(1, len(features), "One result feature was expected!")

    def test_joins_intersects(self):
        host = "geojoins.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        lat1_start = self._latitudes[0]
        lon1_start = self._longitudes[0]
        lat1_end = -lat1_start
        lon1_end = -lon1_start
        lat2_start = self._latitudes[1]
        lon2_start = self._longitudes[1]
        lat2_end = -lat2_start
        lon2_end = -lon2_start
        left = { 
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[lon1_start, lat1_start], [lon1_end, lat1_end]]
                },
                "properties": {
                    "id": "left_linestring"
                }
            }]
        }
        right = { 
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[lon2_start, lat2_start], [lon2_end, lat2_end]]
                },
                "properties": {
                    "id": "right_linestring"
                }
            }]
        }
        geojson = intersects(client, left, right)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")
        self.assertTrue('features' in geojson, "GeoJSON response must have features!")
        features = geojson['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")
        self.assertEqual(1, len(features), "One result feature was expected!")

    def test_joins_overlaps(self):
        host = "geojoins.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        lat1_start = self._latitudes[0]
        lon1_start = self._longitudes[0]
        lat1_end = self._latitudes[1]
        lon1_end = self._longitudes[1]
        lat2_start = self._latitudes[1]
        lon2_start = self._longitudes[1]
        lat2_end = self._latitudes[0]
        lon2_end = self._longitudes[0]
        left = { 
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[lon1_start, lat1_start], [lon1_end, lat1_end]]
                },
                "properties": {
                    "id": "left_linestring"
                }
            }]
        }
        right = { 
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[lon2_start, lat2_start], [lon2_end, lat2_end]]
                },
                "properties": {
                    "id": "right_linestring"
                }
            }]
        }
        geojson = overlaps(client, left, right)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")
        self.assertTrue('features' in geojson, "GeoJSON response must have features!")
        features = geojson['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")
        self.assertEqual(1, len(features), "One result feature was expected!")

    def test_joins_touches(self):
        host = "geojoins.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        lat1_start = self._latitudes[0]
        lon1_start = self._longitudes[0]
        lat1_end = 0
        lon1_end = 0
        lat2_start = self._latitudes[1]
        lon2_start = self._longitudes[1]
        lat2_end = 0
        lon2_end = 0
        left = { 
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[lon1_start, lat1_start], [lon1_end, lat1_end]]
                },
                "properties": {
                    "id": "left_linestring"
                }
            }]
        }
        right = { 
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[lon2_start, lat2_start], [lon2_end, lat2_end]]
                },
                "properties": {
                    "id": "right_linestring"
                }
            }]
        }
        geojson = touches(client, left, right)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")
        self.assertTrue('features' in geojson, "GeoJSON response must have features!")
        features = geojson['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")
        self.assertEqual(1, len(features), "One result feature was expected!")

    def test_joins_within(self):
        host = "geojoins.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        lat = self._latitudes[0]
        lon = self._longitudes[0]
        delta = 0.1
        xmin, xmax, ymin, ymax = lon-delta, lon+delta, lat-delta, lat+delta
        left = { 
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "properties": {
                    "id": "left_point"
                }
            }]
        }
        right = { 
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[xmin, ymax], [xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]]
                },
                "properties": {
                    "id": "right_polygon"
                }
            }]
        }
        geojson = within(client, left, right)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")
        self.assertTrue('features' in geojson, "GeoJSON response must have features!")
        features = geojson['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")
        self.assertEqual(1, len(features), "One result feature was expected!")

    def test_geojson_from_url(self):
        host = "geojoins.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        url = "https://stadtplan.bonn.de/geojson?Thema=14574"
        left = GeoJSON.from_url(url)
        lat = self._latitudes[1]
        lon = self._longitudes[1]
        right = { 
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "properties": {
                    "id": "right_point"
                }
            }]
        }
        geojson = contains(client, left, right)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")
        self.assertTrue('features' in geojson, "GeoJSON response must have features!")
        features = geojson['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")
        self.assertEqual(1, len(features), "One result feature was expected!")

    def test_along(self):
        host = "geodetic.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        distances = [0, 1.5, 3.75, 5]
        offsets = [0, -1.25, 1.75, 5]
        geojson = create_points_along(client, self._latitudes[0], self._longitudes[0], self._latitudes[1], self._longitudes[1], distances, offsets, LinearUnit.km)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")
        self.assertTrue('features' in geojson, "GeoJSON response must have features!")
        features = geojson['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")
        self.assertEqual(len(distances), len(features), "Number of features are wrong!")

    def test_buffer(self):
        host = "geodetic.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        distance = 23.5
        geojson = create_buffers(client, self._latitudes, self._longitudes, distance, LinearUnit.km)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")
        self.assertTrue('features' in geojson, "GeoJSON response must have features!")
        features = geojson['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")
        self.assertEqual(len(self._latitudes), len(features), "Number of features are wrong!")

    def test_buffer_points(self):
        host = "geodetic.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        distance = 23.5
        point_features = { 
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [self._longitudes[0], self._latitudes[0]]
                },
                "properties": {
                    "name": "Dessau"
                }
            }, {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [self._longitudes[1], self._latitudes[1]]
                },
                "properties": {
                    "name": "Bonn"
                }
            }]
        }
        geojson = create_buffers_from_points(client, point_features, distance, LinearUnit.km)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")
        self.assertTrue('features' in geojson, "GeoJSON response must have features!")
        features = geojson['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")
        self.assertEqual(len(point_features), len(features), "Number of features are wrong!")

    def test_direction(self):
        host = "geodetic.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        azimuth = 45
        distance = 23.5
        geojson = create_points_from_direction(client, self._latitudes, self._longitudes, azimuth, distance, LinearUnit.km)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")
        self.assertTrue('features' in geojson, "GeoJSON response must have features!")
        features = geojson['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")
        self.assertEqual(len(self._latitudes), len(features), "Number of features are wrong!")

    def test_path(self):
        host = "geodetic.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        azimuths = [0, 25.5, 95.25]
        distances = [5.5, 10.25, 25.75]
        geojson = create_path_from_directions(client, self._latitudes[0], self._longitudes[0], azimuths, distances, LinearUnit.km)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")
        self.assertTrue('features' in geojson, "GeoJSON response must have features!")
        features = geojson['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")
        self.assertEqual(1, len(features), "Only one path must be created!")

    def test_wedge(self):
        host = "geodetic.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        azimuth = 45
        azimuth_span = 20
        distance = 23.5
        geojson = create_wedges(client, self._latitudes, self._longitudes, azimuth, azimuth_span, distance, LinearUnit.km)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")
        self.assertTrue('features' in geojson, "GeoJSON response must have features!")
        features = geojson['features']
        self.assertTrue(isinstance(features, list), "GeoJSON features must be an instance of list!")
        self.assertEqual(len(self._latitudes), len(features), "Number of features are wrong!")

    def test_azimuth(self):
        host = "geodetic.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        azimuth = to_azimuth(client, "N")
        self.assertIsNotNone(azimuth, "The azimuth response must be initialized!")
        self.assertEqual(0, azimuth, "Azimuth of 0 was expected!")
        azimuth = to_azimuth(client, "S")
        self.assertIsNotNone(azimuth, "The azimuth response must be initialized!")
        self.assertEqual(180, azimuth, "Azimuth of 180 was expected!")

    def test_aggregate_conflicts(self):
        host = "geoconflicts.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        geojson = aggregate_conflicts(client)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")

    def test_cluster_conflicts(self):
        host = "geoconflicts.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        geojson = cluster_conflicts(client)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")
    
    def test_count_conflicts(self):
        host = "geoconflicts.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        count_result = count_conflicts(client)
        self.assertTrue('count' in count_result, "The count result must contain a 'count' property!")
        count = count_result['count']
        self.assertGreater(count, 0, "The conflict count must be greater than 0!")

    def test_date_extent_conflicts(self):
        host = "geoconflicts.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        date_extent_result = date_extent_conflicts(client)
        self.assertTrue('start' in date_extent_result, "The date extent result must contain a 'start' property!")
        start = date_extent_result['start']
        self.assertEquals(start, '2020-01-01', "The conflict start date must equal 2020-01-01!")

    def test_extent(self):
        host = "geoconflicts.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        extent_result = extent_conflicts(client)
        self.assertTrue('xmin' in extent_result, "The spatial extent result must contain a 'xmin' property!")
        xmin = extent_result['xmin']
        self.assertGreater(xmin, -181, "The conflict xmin must be greater than -181!")
        self.assertTrue('ymin' in extent_result, "The spatial extent result must contain a 'ymin' property!")
        ymin = extent_result['ymin']
        self.assertGreater(ymin, -91, "The conflict ymin must be greater than -91!")
        self.assertTrue('xmax' in extent_result, "The spatial extent result must contain a 'xmax' property!")
        xmax = extent_result['xmax']
        self.assertLess(xmax, 181, "The conflict xmax must be less than 181!")
        self.assertTrue('ymax' in extent_result, "The spatial extent result must contain a 'ymax' property!")
        ymax = extent_result['ymax']
        self.assertLess(ymax, 91, "The conflict ymax must be less than 91!")

    def test_query_conflicts(self):
        host = "geoconflicts.p.rapidapi.com"
        client: GeoRapidClient = EnvironmentClientFactory.create_client_with_host(host)
        geojson = query_conflicts(client)
        self.assertIsNotNone(geojson, "GeoJSON response must be initialized!")