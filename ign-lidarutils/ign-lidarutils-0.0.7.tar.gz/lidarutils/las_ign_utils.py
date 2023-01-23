""" fonctions utiles sur la gestion des las IGN """

import json
import os
import tempfile
import pdal
from osgeo.osr import SpatialReference

import lidarutils.geometry_utils as gu
import lidarutils.pdal_pipeline as pdal_ign


class LasIGN:
    """classe représentant un fichier LAS format IGN"""

    def __init__(self, las):
        """constructeur"""

        """le fichier las"""
        self.file_las = las
        self.basename = os.path.basename(las)

        """  l'enveloppe du las """
        self._bbox = gu.Bbox()

        """  l'enveloppe du las a partir du nom du las - construit par appel de validate_name() """
        self._bbox_from_name = gu.Bbox()

        """  projection EPSG du las """
        self._proj = None

    def validate_name(self, return_string):
        """Renvoie False si le nom n'est pas valide.
        Rempli las.return_string avec une erreur lisible par l'utilisateur"""

        def try_string_to_int(string, return_string):
            """Return True si la chaine est un entier. Sinon, Retourne Flase
            et rempli l'objet return_string avec une erreur lisible par l'utilisateur"""
            try:
                int(string)
            except ValueError:
                return_string += "- La chaine " + string + " devrait être un entier." + "\n"
                return False
            return True

        las_name_infos = self.basename.split("_")
        if len(las_name_infos) != 6:
            return_string += "- Le nom de fichier n'est pas valide." + "\n"
            return False

        if las_name_infos[0] != "Semis":
            return_string += '- Le nom de fichier doit commencer par "Semis".' + "\n"
            return False

        # année
        if not try_string_to_int(las_name_infos[1], return_string):
            return False

        # XXXX
        if len(las_name_infos[2]) != 4:
            return_string += (
                "- La chaine "
                + las_name_infos[2]
                + " devrait contenir 4 carractères. (coordonnées X)"
                + "\n"
            )
            return False

        if not try_string_to_int(las_name_infos[2], return_string):
            return False

        x_min_name = int(las_name_infos[2])
        self._bbox_from_name.xmin = 1000 * float(x_min_name)
        self._bbox_from_name.xmax = 1000 * float(x_min_name + 1)

        # YYYY
        if len(las_name_infos[3]) != 4:
            return_string += (
                "- La chaine "
                + las_name_infos[3]
                + " devrait contenir 4 carractères. (coordonnées Y)"
                + "\n"
            )
            return False

        if not try_string_to_int(las_name_infos[3], return_string):
            return False

        y_max_name = int(las_name_infos[3])
        self._bbox_from_name.ymin = 1000 * float(y_max_name - 1)
        self._bbox_from_name.ymax = 1000 * float(y_max_name)

        # rien pour proj et refz pour le moment

        return True

    @property
    def bbox_from_name(self):
        """renvoie l'enveloppe calculée via le nom du LAS"""
        if self._bbox_from_name.is_empty():
            return_validate_name = ""
            self.validate_name(return_validate_name)
        return self._bbox_from_name

    @property
    def bbox(self):
        """renvoie l'enveloppe du LAS, par défaut celle du nom du LAS"""
        if not self._bbox.is_empty():
            return self._bbox
        if not self._bbox_from_name.is_empty():
            self._bbox = self._bbox_from_name
        if self._bbox.is_empty():
            # * permet de degrouper un tuple...
            self._bbox = gu.Bbox(*get_bbox(self.file_las))
        return self._bbox

    @property
    def projection(self):
        """renvoie la projection du las"""
        if self._proj is not None:
            return self._proj
        try:
            self._proj = get_projection(self.file_las)
        except OSError:
            self._proj = None
        return self._proj


def get_bbox(las: str):
    """Get XY bounding box of a cloud using pdal info --metadata

     Args:
         input_las (str): path to input LAS cloud.

     Returns:
         float: coordinates of bounding box : xmin, ymin, xmax, ymax
     """

    # Ecriture des metadonnees dans un fichier tmp
    tmp = tempfile.NamedTemporaryFile(suffix="_mtd_get_bbox")
    tmp.close()
    pdal_ign.run_pdal_info(las, tmp.name)

    with open(tmp.name) as mtd:
        metadata = json.load(mtd)["metadata"]
    os.remove(tmp.name)
    return metadata["minx"], metadata["maxx"], metadata["miny"], metadata["maxy"]

def get_projection(las: str):
    """Get the las projection"""
    tmp = tempfile.NamedTemporaryFile(suffix="_mtd_get_projection")
    tmp.close()
    pdal_ign.run_pdal_info(las, tmp.name)

    authority = None
    with open(tmp.name) as mtd:
        metadata = json.load(mtd)
        spatial_wkt = metadata["metadata"]["comp_spatialreference"]

        osr_crs = SpatialReference()
        osr_crs.ImportFromWkt(spatial_wkt)
        authority = osr_crs.GetAttrValue("AUTHORITY", 0)

    os.remove(tmp.name)
    if authority == 'EPSG':
        proj = osr_crs.GetAttrValue("AUTHORITY", 1)
        return int(proj)

    return None

def set_projection(input_las: str, output_las: str, epsg: int):
    """Add projection to a las"""
    pipeline = pdal.Reader.las(filename=input_las) | pdal.Writer.las(
        filename=output_las,
        a_srs='EPSG:'+str(epsg),
    )
    pipeline.execute()
