"""Connect to and download Open Geospatial Consortium (OCG) services.

Bulk querying and downloading of geometric data hosted on an OCG GeoServer, such as Web Feature Services (WFS) and Web Map Services (WMS).
"""

__all__ = ["get_wfs_data"]


import owslib, owslib.wms, owslib.wfs, requests, geopandas as gpd


def get_wfs_data(url: str, layer_name: str, projection: int = 2193) -> gpd.GeoDataFrame:
    """Query a Web Feature Service (WFS) and return all data from a layer.
    
    Returns a geopandas.GeoDataFrame of all atrribute and geometric data from a layer in a WFS service.
        
    Args:
        url: String of the OGC Service. E.g. https://data.wairoadc.govt.nz/geoserver/ows.
        layer_name: Name of the layer to download. E.g. 'geonode:ncs_cemetery_plots'.
        projection: Integer of the CRS that the data should be returned in.

    Returns:
        A geopandas.GeoDataFrame containing all geometric data in the requested projection, with any attribute data.
    
    Raises:
        ValueError: Raised if the given layer name is not a part of the WFS 
    """
    wfs = owslib.wfs.WebFeatureService(url, version="1.0.0") # other versions are 1.1.0 and 2.0.0

    if layer_name not in wfs.contents:
        raise ValueError(f"The layer '{layer_name}' is not available from {url}.\nPlease choose from the following available layers:\n{list(wfs.contents)}")

    params = {
        "service": "WFS",
        "version": "1.0.0",
        "request": "GetFeature",
        "typeName": layer_name,
        "outputFormat": "json",
        "srsName": f"EPSG:{projection}"
    }

    wfs_request_url = requests.Request('GET', url, params=params).prepare().url
    return gpd.read_file(wfs_request_url)