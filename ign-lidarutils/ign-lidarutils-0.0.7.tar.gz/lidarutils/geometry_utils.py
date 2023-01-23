""" fonctions utiles autour de la géométrie """

from geojson import Polygon
from osgeo import ogr

##########################################################################


class Bbox:
    """Défini une enveloppe"""

    def __init__(self, xmin=0.0, xmax=0.0, ymin=0.0, ymax=0.0):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def is_empty(self):
        """test si l'enveloppe est vide"""
        return (
            self.xmin == 0.0
            and self.ymin == 0.0
            and self.xmax == 0.0
            and self.ymax == 0.0
        )

    def to_string(self):
        """exporte une chaine de carractère"""
        return (
            "["
            + str(self.xmin)
            + ","
            + str(self.xmax)
            + ","
            + str(self.ymin)
            + ","
            + str(self.ymax)
            + "]"
        )

    def to_polygon_geojson(self):
        """exporte en polygone geojson"""
        poly = Polygon(
            [
                [
                    [float(self.xmin), float(self.ymin)],
                    [float(self.xmax), float(self.ymin)],
                    [float(self.xmax), float(self.ymax)],
                    [float(self.xmin), float(self.ymax)],
                    [float(self.xmin), float(self.ymin)],
                ]
            ]
        )
        return poly

    def to_ring_ogr(self):
        """conversion en ring ogr"""
        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint(self.xmin, self.ymin)
        ring.AddPoint(self.xmin, self.ymax)
        ring.AddPoint(self.xmax, self.ymax)
        ring.AddPoint(self.xmax, self.ymin)
        ring.AddPoint(self.xmin, self.ymin)
        return ring

    def expand(self, val):
        """extension de l'emprise"""
        self.xmin -= val
        self.ymin -= val
        self.xmax += val
        self.ymax += val



##########################################################################
##########################################################################


def build_poly_ogr(rings):
    """construction d'un polygone ogr a partir de rings"""
    poly = ogr.Geometry(ogr.wkbPolygon)
    for ring in rings:
        poly.AddGeometry(ring)
    return poly
