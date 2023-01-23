import os
import psycopg2
from osgeo import ogr, osr

def get_req_bduni(req, dirout, layer, keep_exists=False):
    """requete une couche de la BDUni"""

    if ("BDUNI_PASSWORD" not in os.environ):
        raise RuntimeError("Please set environnment varible BDUNI_PASSWORD")

    password=os.getenv("BDUNI_PASSWORD", "")

    conn = psycopg2.connect(
        host="babylone3.ign.fr",
        port=5432,
        dbname="bduni_france_consultation",
        user="invite",
        password=password
    )

    cur = conn.cursor()

    layer_name = layer + ".json"
    json_th = os.path.join(dirout, layer_name)

    if keep_exists:
        if os.path.exists(json_th):
            statinfo = os.stat(json_th)
            if statinfo.st_size != 100:
                return json_th

    cur.execute(req)
    ths = cur.fetchall()
    drv = ogr.GetDriverByName("GeoJSON")
    ds = drv.CreateDataSource(json_th)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(2154)
    lay = ds.CreateLayer(layer, srs, ogr.wkbMultiPolygon)
    for th in ths:
        feat = ogr.Feature(lay.GetLayerDefn())
        poly = ogr.CreateGeometryFromWkt(th[0])
        feat.SetGeometry(poly)
        lay.CreateFeature(feat)
        feat = None
    lay = srs = ds = drv = None

    conn.commit()
    cur.close()
    del cur
    conn.close()
    return json_th


##########################################################################


def get_req_bduni_bat(poly, param_hmin, dir_out):
    """requete le bâti de la BDUni"""

    geom_chantier = "ST_GeomFromText('" + poly.ExportToWkt() + "')"

    cmd_sql = f"""
        SELECT st_astext(geometrie) AS geom
        FROM batiment 
        WHERE NOT gcms_detruit 
        AND hauteur>{param_hmin} 
        AND ST_Intersects(geometrie, {geom_chantier})
        UNION
        SELECT st_astext(geometrie) AS geom
        FROM reservoir
        WHERE NOT gcms_detruit
        AND hauteur>{param_hmin}
        AND ST_Intersects(geometrie, {geom_chantier})
    """

    return get_req_bduni(cmd_sql, dir_out, "bati")


##########################################################################


def get_req_bduni_eolienne(poly, buffer, dir_out):
    """requete les eoliennes de la BDUni"""

    geom_chantier = "ST_GeomFromText('" + poly.ExportToWkt() + "')"

    cmd_sql = f"""
        SELECT st_astext(st_buffer(geometrie, '{buffer}')) FROM construction_ponctuelle WHERE NOT gcms_detruit AND nature='Eolienne' AND ST_Intersects(geometrie, {geom_chantier})
    """

    return get_req_bduni(cmd_sql, dir_out, "eolienne")


##########################################################################


def get_req_bduni_ligne_electrique(poly, buffer, dir_out):
    """requete les eoliennes de la BDUni"""

    geom_chantier = "ST_GeomFromText('" + poly.ExportToWkt() + "')"

    cmd_sql = f"""
        SELECT st_astext(st_buffer(geometrie, '{buffer}')) FROM ligne_electrique WHERE NOT gcms_detruit AND ST_Intersects(geometrie, {geom_chantier})
    """

    return get_req_bduni(cmd_sql, dir_out, "ligne_electrique")
