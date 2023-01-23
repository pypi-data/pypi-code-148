""" fonctions utiles de traitements d'images avec GDAL """

import os
import cv2
import numpy as np
from osgeo import gdal, ogr, osr


##########################################################################


def reproj_if_unamed_proj(image, code_epsg_out):
    """Assigne la projection si l'image n'en a pas"""

    gdal_image = gdal.Open(image)
    prj = gdal_image.GetProjection()
    if "unnamed" in prj:
        print("reprojection de l'image en " + str(code_epsg_out))
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(code_epsg_out)
        gdal_image.SetProjection(srs.ExportToWkt())
    gdal_image = None


##########################################################################


def apply_georef(fic_ok, fic_open_cv, fic_output, kernel, epsg):
    """Transfert du Georef (perdu avec la morpho math de OpenCV)"""

    f_geo = gdal.Open(fic_ok)
    src_ds = gdal.Open(fic_open_cv)
    driver = gdal.GetDriverByName("GTiff")

    # Open destination dataset
    dst_ds = driver.CreateCopy(fic_output, src_ds, 0)
    geo_tsf = f_geo.GetGeoTransform()
    if kernel % 2 == 0 and kernel != 0:
        geo_tsf = [
            geo_tsf[0] - geo_tsf[1],
            geo_tsf[1],
            geo_tsf[2],
            geo_tsf[3] - geo_tsf[5],
            geo_tsf[4],
            geo_tsf[5],
        ]
    dst_ds.SetGeoTransform(geo_tsf)

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(int(epsg))
    dst_wkt = srs.ExportToWkt()
    dst_ds.SetProjection(dst_wkt)
    dst_ds = None
    src_ds = None
    f_geo = None


##########################################################################


def get_ogr_driver_by_ext(file):
    _, file_extension = os.path.splitext(file)
    if file_extension == ".json" or file_extension == ".geojson":
        return "GeoJson"
    elif file_extension == ".shp":
        return "ESRI Shapefile"
    else:
        raise Exception("Extension de fichier vecteur non comprise")
        return 0


def gdal_polygonize(fic_mask, fic_output, epsg_out=None, field_name="value", value_to_polygonize=0):
    """Polygonisation des valeurs non-nulles d'un raster monobande."""

    src_ds = gdal.Open(fic_mask)
    srcband = src_ds.GetRasterBand(1)
    srcband2 = src_ds.GetRasterBand(1)

    srs = get_ogr_srs(epsg_out)
    ext_driver = get_ogr_driver_by_ext(fic_output)
    drv = ogr.GetDriverByName(ext_driver)

    if os.path.exists(fic_output):
        drv.DeleteDataSource(fic_output)

    dst_datasource = drv.CreateDataSource(fic_output)
    dst_layer = dst_datasource.CreateLayer(fic_output, srs)
    field_defn = ogr.FieldDefn(field_name, ogr.OFTString)
    dst_layer.CreateField(field_defn)

    gdal.Polygonize(srcband, srcband2, dst_layer, value_to_polygonize, ["8"], callback=None)


def simplify_geom(fic_input, fic_output, epsg_out=None, ratio=2):
    """Simplification de geometrie avec OGR"""

    srs = get_ogr_srs(epsg_out)
    ext_driver = get_ogr_driver_by_ext(fic_output)
    drv = ogr.GetDriverByName(ext_driver)

    if os.path.exists(fic_output):
        drv.DeleteDataSource(fic_output)
    dst_datasource = drv.CreateDataSource(fic_output)
    dst_layer = dst_datasource.CreateLayer(fic_output, srs, geom_type=ogr.wkbPolygon)
    feature_def = dst_layer.GetLayerDefn()

    shp = ogr.Open(fic_input, 0)
    lyr = shp.GetLayer()

    for i in range(0, lyr.GetFeatureCount()):
        feat = lyr.GetFeature(i)
        geom = feat.geometry()
        simple = geom.Simplify(ratio)

        dst_feature = ogr.Feature(feature_def)
        dst_feature.SetGeometry(simple)
        dst_layer.CreateFeature(dst_feature)
        dst_feature = None


def create_ogr_layer(fic_output, epsg_out=None, ogr_geom_type=None):
    """Regroupe les etapes necessaires a la creation d'un layer OGR"""

    ext_driver = get_ogr_driver_by_ext(fic_output)
    drv = ogr.GetDriverByName(ext_driver)
    if os.path.exists(fic_output):
        drv.DeleteDataSource(fic_output)
    outDataSource = drv.CreateDataSource(fic_output)

    srs = get_ogr_srs(epsg_out)
    if ogr_geom_type is not None:
        outLayer = outDataSource.CreateLayer(fic_output, srs, geom_type=ogr_geom_type)
    else:
        outLayer = outDataSource.CreateLayer(fic_output, srs)
    return outLayer


def get_ogr_srs(epsg):
    if epsg is not None:
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(int(epsg))
        return srs
    else:
        return None


def remove_shp(shp):
    """suppression des fichiers associes au shp"""

    basename = os.path.splitext(shp)[0]
    ext = [".shp", ".shx", ".dbf", ".prj"]
    file_list = [basename + extension for extension in ext]
    [os.remove(file) for file in file_list if os.path.exists(file)]


##########################################################################
def mophology_open_cv2(fic_input, fic_output, kernel):
    """MorphMath : Ouverture"""

    # lecture de l'image
    img = cv2.imread(fic_input, 0)

    np.invert(img)

    # définition du kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(kernel, kernel))

    # appel des morphos maths
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    # L'ouverture posant quelques soucis
    # (suppression de grosses surfaces fines)
    # il vaut surement mieux conserver la valeur de surface min...

    # ecriture de l'image
    np.invert(img)
    cv2.imwrite(fic_output, img)


def mophology_close_cv2(fic_input, fic_output, kernel):
    """MorphMath : Fermeture"""

    # lecture de l'image
    img = cv2.imread(fic_input, 0)

    np.invert(img)

    # définition du kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(kernel, kernel))

    # appel des morphos maths
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    # L'ouverture posant quelques soucis
    # (suppression de grosses surfaces fines)
    # il vaut surement mieux conserver la valeur de surface min...

    # ecriture de l'image
    np.invert(img)
    cv2.imwrite(fic_output, img)


def buffer_cv2(fic_input, fic_output, kernel, iteration):
    """MorphMath : Buffer"""

    # lecture de l'image
    img = cv2.imread(fic_input, 0)

    np.invert(img)

    # définition du kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(kernel, kernel))

    # appel des morphos maths
    # img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    dilation = cv2.dilate(img, kernel, iterations=iteration)

    # L'ouverture posant quelques soucis
    # (suppression de grosses surfaces fines)
    # il vaut surement mieux conserver la valeur de surface min...

    # ecriture de l'image
    np.invert(dilation)
    cv2.imwrite(fic_output, dilation)


##########################################################################


def gdal_sieve(src_filename, dst_filename, threshold):
    """Surcharge  SieveFilter() ... Removes small raster polygons
    Parametres
    ----------
       src_filename : str
       dst_filename : str
       threshold : int
    """
    src_ds = gdal.Open(src_filename)
    src_band = src_ds.GetRasterBand(1)

    dst_drv = gdal.GetDriverByName("GTiff")
    dst_ds = dst_drv.CreateCopy(dst_filename, src_ds, strict=0)
    dst_band = dst_ds.GetRasterBand(1)

    gdal.SieveFilter(src_band, None, dst_band, threshold)
    dst_ds = None
    src_ds = None


##########################################################################


def get_extent(ds):
    """Return list of corner coordinates from a gdal Dataset"""
    xmin, xpixel, _, ymax, _, ypixel = ds.GetGeoTransform()
    width, height = ds.RasterXSize, ds.RasterYSize
    xmax = xmin + width * xpixel
    ymin = ymax + height * ypixel

    return (xmin, ymax), (xmax, ymax), (xmax, ymin), (xmin, ymin)


def reproject_coords(coords, src_srs, tgt_srs):
    """Reproject a list of x,y coordinates."""
    trans_coords = []
    transform = osr.CoordinateTransformation(src_srs, tgt_srs)
    for x, y in coords:
        x, y, z = transform.TransformPoint(x, y)
        trans_coords.append([x, y])
    return trans_coords
