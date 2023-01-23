""" Extraction du RGE Alti  des flux GPP sur une bbox """

import os
import requests

import lidarutils.geometry_utils as gu

""" 
    La pyramide issue du GPP n'est pas la plus fine
    Le MNT résultant ne sera donc pas à la meilleure qualité
"""

##########################################################################

def get_rge_alti_from_gpp(bbox: gu.Bbox, dtm_rge_path: str, layer_str: str , epsg : int):
    """extraction du RGE Alti sur la bbox"""

    # les types de layer
    layers = [
        {'name':'DTM', 'url':'ELEVATION.ELEVATIONGRIDCOVERAGE.HIGHRES'},
        {'name':'SRC', 'url':'ELEVATIONGRIDCOVERAGE.HIGHRES.QUALITY'}
    ]

    layer_url = None
    for lay in layers:
        if lay['name']==layer_str:
            layer_url = lay['url']
    assert layer_url is not None

    URL_GPP = "https://wxs.ign.fr/altimetrie/geoportail/r/wms?"
    URL_FORMAT = "&EXCEPTIONS=text/xml&FORMAT=image/geotiff&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&STYLES="
    URL_EPSG = "&CRS=EPSG:" + str(epsg)
    URL_BBOX = "&BBOX=" + str(bbox.xmin) + "," + str(bbox.ymin) + "," + str(bbox.xmax) + "," + str(bbox.ymax)
    URL_SIZE = "&WIDTH=" + str(int(bbox.xmax-bbox.xmin)) + "&HEIGHT=" + str(int(bbox.ymax-bbox.ymin))

    #for layer in layers:
    URL = URL_GPP + "LAYERS=" + layer_url + URL_FORMAT + URL_EPSG + URL_BBOX + URL_SIZE
    req = requests.get(URL, allow_redirects=True)
    open(dtm_rge_path, 'wb').write(req.content)


##########################################################################
