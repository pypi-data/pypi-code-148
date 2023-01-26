import os

import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon
from utils import WWW, JSONFile

from gig.core._common import URL_BASE
from gig.core.EntType import EntType


class EntGeoMixin:
    @property
    def raw_geo_file(self):
        raw_geo_path = os.path.join('/tmp', f'ent.{self.id}.raw_geo.json')
        return JSONFile(raw_geo_path)

    @property
    def url_remote_geo_data_path(self):
        id = self.id
        ent_type = EntType.from_id(id)
        return os.path.join(
            URL_BASE,
            f'geo/{ent_type.name}/{id}.json',
        )

    def get_raw_geo(self):
        raw_geo_file = self.raw_geo_file
        if raw_geo_file.exists:
            raw_geo = raw_geo_file.read()
        else:
            raw_geo = WWW(self.url_remote_geo_data_path).readJSON()
            raw_geo_file.write(raw_geo)
        return raw_geo

    def geo(self):
        polygon_list = list(
            map(
                lambda polygon_data: Polygon(polygon_data),
                self.get_raw_geo(),
            )
        )
        multipolygon = MultiPolygon(polygon_list)
        return gpd.GeoDataFrame(
            index=[0], crs='epsg:4326', geometry=[multipolygon]
        )
