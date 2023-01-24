from requests import Request
from owslib.wfs import WebFeatureService
import osmnx as ox
import geopandas as gpd


class WFS:
    def __init__(self, wfs_url, version="1.0.0"):
        """Connection object for a specified WFS service"""

        # WFS end point
        self.wfs_url = wfs_url

        # Initialize
        self.wfs = WebFeatureService(url=self.wfs_url, version=version)

        # Meta data
        self.meta_data = self.init_layer_info()

        # Area of interest
        self.area = None

    def init_layer_info(self):
        """Retrieve meta data information for all available layers"""
        meta_data = {}
        for layer, meta in self.wfs.items():
            meta_data[meta.id] = dict(crsOptions=meta.crsOptions,
                                      boundingBox=meta.boundingBox,
                                      boundingBoxWGS84=meta.boundingBoxWGS84,
                                      title=meta.title,
                                      id=meta.id,
                                      crs_code=meta.crsOptions[0].code,
                                      abstract=meta.abstract,
                                      keywords=meta.keywords,
                                      styles=meta.styles
                                      )
        return meta_data

    def get_layers(self):
        """Return all available layers at the WFS endpoint"""
        self.layers = list(self.wfs.contents)
        return self.layers

    def get_layer_info(self, layer_id=None):
        """Get metadata information for all layers or for a specific WFS layer"""
        if layer_id is not None:
            return self.meta_data[layer_id]
        else:
            return self.meta_data

    def get_functions(self):
        """Get all available functions in the WFS"""
        return [operation.name for operation in self.wfs.operations]

    def get_wfs_version(self):
        """Get the version of the WFS"""
        return self.wfs.version

    def get_default_epsg_code(self, layer_id):
        """Get default EPSG code of the specified layer"""
        return self.meta_data[layer_id]['crs_code']

    def get_epsg_options(self, layer_id):
        """Get available projections (EPSG codes) that can be used to fetch the data"""
        return self.meta_data[layer_id]['crsOptions']

    def get_epsg_specification(self, epsg_code, layer_id):
        """Get epsg specification for given EPSG number"""
        for spec in self.get_epsg_options(layer_id):
            if str(epsg_code) in spec.getcodeurn():
                return spec
        print("Could not find EPSG specification for %s. Using the default EPSG:%s." % (
        epsg_code, self.get_default_epsg_code(layer_id)))
        return self.get_epsg_specification(self.get_default_epsg_code(layer_id), layer_id)

    def get_wfs_bbox(self, xmin, ymin, xmax, ymax, epsg):
        """Get bounding box following WFS standard definition"""
        bbox = f"{xmin:.2f},{ymin:.2f},{xmax:.2f},{ymax:.2f},EPSG:{epsg}"
        return bbox

    def get_gdf_from_place(self, place_name):
        """Returns GeoDataFrame for a given place name using Nominatim.
        Check available place names from https://nominatim.openstreetmap.org/
        """
        data = ox.geocoder.geocode_to_gdf(place_name)
        assert len(
            data) > 0, "Could not find geometry for the location %s.\nCheck your search query from https://nominatim.openstreetmap.org/" % place_name

        # Update the area of interest
        self.area = data

        return data

    def get_bounds_from_gdf(self, gdf):
        """Extracts total bounds from the input GeoDataFrame"""
        return gdf.total_bounds

    def get_bbox_from_place(self, place_name):
        """
        Returns a bounding box for a given place name using Nominatim.
        Check available place names from https://nominatim.openstreetmap.org/
        """
        # Get data from OSM
        data = self.get_gdf_from_place(place_name=place_name)
        return data.geometry.total_bounds

    def get_poly_from_place(self, place_name):
        """
        Returns a Polygon for a given place name using Nominatim.
        Check available place names from https://nominatim.openstreetmap.org/
        """
        data = self.get_gdf_from_place(place_name=place_name)
        return data['geometry'].values[0]

    def get_wfs_with_requests(self, layer_id, bounding_box, max_features, epsg_spec):
        """
        Retrieves data directly to Geopandas using requests (used by default). Sometimes if 'json' format
        is not available, this does not work. Then 'get_wfs_with_fiona' is used instead.
        """
        # Get query
        q = self.prepare_get_query(layer_id=layer_id,
                                   bounding_box=bounding_box,
                                   max_features=max_features,
                                   epsg_spec=epsg_spec,
                                   output_format="json"
                                   )

        # Retrieve the data
        print(
            f"======================================\nDownloading data for: {layer_id}\n======================================\n")
        data = gpd.read_file(q)
        return data

    def get_wfs_with_fiona(self, layer_id, bounding_box, epsg_spec):
        """
        Retrieves data using fiona.
        """
        import fiona
        response = self.wfs.getfeature(typename=[layer_id], bbox=bounding_box, srsname=epsg_spec)
        b = bytes(response.read())
        with fiona.BytesCollection(b) as f:
            crs = f.crs
            gdf = gpd.GeoDataFrame.from_features(f, crs=crs)
        return gdf

    def prepare_wfs_bounding_box(self, bounding_box=None, epsg=None):
        """Prepare bounding box for WFS request"""
        assert isinstance(epsg, int), "'epsg' code should be an integer number. Found: %s" % type(epsg)
        return self.get_wfs_bbox(*self.get_bounds_from_gdf(bounding_box), epsg)

    def prepare_get_query(self, layer_id, bounding_box, max_features, epsg_spec, output_format):
        """Prepare requests query for WFS"""
        # Prepare basic call parameters
        params = dict(service='WFS',
                      version=self.get_wfs_version(),
                      request='GetFeature',
                      typeName=layer_id,
                      srsName=epsg_spec,
                      maxFeatures=max_features,
                      outputFormat=output_format
                      )

        # Add bounding box to parameters if specified
        if bounding_box is not None:
            params['BBOX'] = bounding_box

        # Prepare the query
        q = Request('GET', self.wfs_url, params=params).prepare().url

        return q

    def load_wfs(self, layer_id, bounding_box=None, max_features=1000000, epsg=None):
        """
        Download specified WFS layer.

        Params
        ------

        layer_id : str
           ID for the layer that will be downloaded from the WFS. Use .get_layers() function to find out all available ones.
        bounding_box : GeoDataFrame | shapely Polygon | shapely box | (xmin, ymin, xmax, ymax) -coordinate tuple
           Bounding box that can be used to limit the area from where the data is retrieved.
        max_features : int
           Maximum number of features that will be retrieved from the WFS.
        epsg : int
           The CRS how the data should be fetched.

        """

        # Get EPSG specification
        if epsg is None:
            epsg = self.get_default_epsg_code(layer_id)
        epsg_spec = self.get_epsg_specification(epsg, layer_id)

        # Prepare bounding box if it is specified
        if bounding_box is not None:
            # Ensure that the CRS of bounding box matches with the WFS layer
            if isinstance(bounding_box, gpd.GeoDataFrame):
                bounding_box = bounding_box.to_crs(epsg=epsg)
            bounding_box = self.prepare_wfs_bounding_box(bounding_box, epsg)

        # Retrieve the data
        try:
            data = self.get_wfs_with_requests(layer_id=layer_id,
                                              bounding_box=bounding_box,
                                              epsg_spec=epsg_spec,
                                              max_features=max_features)
        except:
            data = self.get_wfs_with_fiona(layer_id=layer_id,
                                           epsg_spec=epsg_spec,
                                           bounding_box=bounding_box
                                           )

        # Error if data could not been fetched
        assert len(data) > 0, "Did not find any data with given criteria:\n %s" % q
        return data