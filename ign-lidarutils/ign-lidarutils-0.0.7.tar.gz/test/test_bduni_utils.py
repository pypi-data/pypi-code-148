
from lidarutils import bduni_utils
from lidarutils import geometry_utils
from lidarutils import las_ign_utils
import geopandas
import tempfile
import pytest
import os

def bduni_request_example():
    MIN_HEIGHT_REQUESTED_BUILDINGS = 0

    bbox = geometry_utils.Bbox(922950, 924050, 6306950, 6308050)
    rings = [bbox.to_ring_ogr()]
    poly = geometry_utils.build_poly_ogr(rings)
    with tempfile.TemporaryDirectory() as d:
        # Request the BDUni and save vectors to a temporary geojson.
        print(poly)
        _buildings_json = bduni_utils.get_req_bduni_bat(
            poly, MIN_HEIGHT_REQUESTED_BUILDINGS, d
        )
        print(_buildings_json)
        gdf = geopandas.read_file(_buildings_json)
        nb_instances = len(gdf)
        print(nb_instances)
        assert(nb_instances > 200)


def test_bduni_request_raise():
    with pytest.raises(RuntimeError):
        bduni_request_example()

# Define BDUNI_PASSSWORD env var and test this commented test
# def test_bduni_request_raise():
#     bduni_request_example()
