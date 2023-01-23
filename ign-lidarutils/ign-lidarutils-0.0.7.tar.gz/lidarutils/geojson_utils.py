""" fonctions utiles autour des GeoJSON """

import geojson
from shapely.geometry import shape

##########################################################################


def remove_small_area(fic_input, fic_output, surface):
    """
    Nettoyage des surfaces trop petites
    """

    with open(fic_input) as file:
        geo_json = geojson.load(file)

    keep = []
    features = geo_json["features"]
    for feature in features:
        geoj = feature["geometry"]
        geo = shape(geoj)
        if geo.area > float(surface):
            keep.append(feature)

    feature_collection = geojson.FeatureCollection(keep)

    with open(fic_output, "w") as file:
        geojson.dump(feature_collection, file)

    return len(keep)

##########################################################################

def merge(input_fics : [str], fic_output : str):
    """ merge des features dans le même fichier """

    features_out = []
    for json in input_fics:
        with open(json) as file:
            geo_json = geojson.load(file)
            features = geo_json["features"]
            for fea in features:
                features_out.append(fea)

    feature_collection = geojson.FeatureCollection(features_out)
    with open(fic_output, "w") as file:
        geojson.dump(feature_collection, file)

##########################################################################
