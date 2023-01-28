from ogc_reader import web_map_service_111
from wms.wms_111 import WebMapService111

url = "https://geoservidorperu.minam.gob.pe/arcgis/services/ServicioBase/MapServer/WMSServer?"

wms: WebMapService111 = web_map_service_111(url)

layers = list(wms.contents)
