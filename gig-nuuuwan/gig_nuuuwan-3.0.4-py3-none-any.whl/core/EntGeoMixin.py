import os

import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon
from utils import WWW

from gig.core._common import URL_BASE
from gig.core.EntType import EntType


class EntGeoMixin:
    @property
    def url_remote_geo_data_path(self):
        id = self.id
        ent_type = EntType.from_id(id)
        return os.path.join(
            URL_BASE,
            f'geo/{ent_type.name}/{id}.json',
        )

    def raw_geo(self):
        return WWW(self.url_remote_geo_data_path).readJSON()

    def geo(self):
        polygon_list = list(
            map(
                lambda polygon_data: Polygon(polygon_data),
                self.raw_geo(),
            )
        )
        multipolygon = MultiPolygon(polygon_list)
        return gpd.GeoDataFrame(
            index=[0], crs='epsg:4326', geometry=[multipolygon]
        )
