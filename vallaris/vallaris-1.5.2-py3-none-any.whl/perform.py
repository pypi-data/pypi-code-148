################# Vallaris Maps ##################
############## By : sattawat arab ###############
###### GIS Backend Engineer #########
########### i-bitz company limited ##############
##################### 2020 ######################

import time
import tempfile
import os
from os import listdir
from os.path import isfile, join
import json
import uuid
import urllib.request
from urllib.request import urlopen
from urllib.request import urlretrieve
import cgi
import requests
import tarfile
from geopandas import GeoSeries
from shapely.geometry import Polygon
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
from vallaris.utils import *
from IPython.display import display, Javascript, Markdown as md, HTML
from urllib.parse import urlencode
import zipfile
from IPython.display import IFrame
import rasterio
from rasterio.plot import show
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
from dotenv import load_dotenv
load_dotenv()


def setEnviron(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)

    try:
        msgBody = json.loads(parameter)
    except:
        msgBody = parameter

    try:
        GP_API_FEATURES_HOST = os.environ.get(
            'GP_API_FEATURES_HOST', 'https://v2k-dev.vallarismaps.com/core/api/features')
        url = GP_API_FEATURES_HOST.split("/")[-4]
        Api_Key = msgBody["API-Key"]
        VallarisServer = GP_API_FEATURES_HOST

        if 'APIKey' in os.environ:
            del os.environ['APIKey']

        if 'VallarisServer' in os.environ:
            del os.environ['VallarisServer']

        os.environ["APIKey"] = Api_Key
        os.environ["VallarisServer"] = VallarisServer

    except:
        Api_Key = os.environ["APIKey"]
        VallarisServer = os.environ["VallarisServer"]

    return [Api_Key, VallarisServer]


def InputValue(storage, parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        input_format = msgOption['process']['inputs']['input'][0]['input'][0]['format']
        input_value = msgOption['process']['inputs']['input'][0]['input'][0]['value']
        # return input
        if input_format == 'GeoJSON':
            dump_json = json.dumps(input_value)
            read_data = gpd.read_file(dump_json)
            return read_data

        elif input_format == 'vallaris':
            dataset_id = input_value
            VallarisServer = os.environ["VallarisServer"]
            Api_Key = os.environ["APIKey"]

            dataCollection = getData(dataset_id, VallarisServer, Api_Key)
            return dataCollection

        elif input_format == 'pipeline':
            msgOption = msgBody
            read_data = gpd.read_file(
                storage + '/' + str(input_value) + ".gpkg")
            return read_data

        else:
            msg = "Perform step  get data KeyError: input "+input_format+" incorrect"
            return msg

    except Exception as e:
        # print(e)
        msg = "Perform step  get data KeyError: input "+input_format+" incorrect"
        return msg


def OverlayValue(storage, parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        input_format = msgOption['process']['inputs']['input'][0]['input'][1]['format']
        input_value = msgOption['process']['inputs']['input'][0]['input'][1]['value']
        # return input
        if input_format == 'GeoJSON':
            dump_json = json.dumps(input_value)
            read_data = gpd.read_file(dump_json)
            return read_data

        elif input_format == 'vallaris':
            dataset_id = input_value
            VallarisServer = os.environ["VallarisServer"]
            Api_Key = os.environ["APIKey"]

            dataCollection = getData(dataset_id, VallarisServer, Api_Key)
            return dataCollection

        elif input_format == 'pipeline':
            msgOption = msgBody
            read_data = gpd.read_file(
                storage + '/' + str(input_value) + ".gpkg")
            return read_data

        else:
            msg = "Perform step  get data KeyError: input "+input_format+" incorrect"
            return msg

    except Exception as e:
        # print(e)
        msg = "Perform step  get data KeyError: input "+input_format+" incorrect"
        return msg


def FileValue(parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        input = msgOption['process']['inputs']['input'][0]['input'][0]['value']
        file = str(input) + ".gpkg"
        return file
    except Exception as e:
        print(e)
        file = False
        return file


def FormatValue(parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        format = msgOption['process']['inputs']['input'][0]['input'][0]['format']
        return format
    except Exception as e:
        print(e)
        format = False
        return format


def ParamValue(parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        param = msgOption['process']['inputs']['parameter'][0]['input']
        return param
    except Exception as e:
        print(e)
        param = False
        return param


def CollectionValue(storage, parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        collection = msgOption['process']['inputs']['input'][0]['input']
        dataset_id = collection[0]['value']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        dataCollection = getData(storage, dataset_id, VallarisServer, Api_Key)

        if dataCollection != "something wrong":
            input = dataCollection
            return input

        else:
            input = False
            return input
    except Exception as e:
        print(e)
        input = False
        return input


def ExportFeatures(parameter):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        collection = msgOption['id']
        dataset_id = collection
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        dataExport = getExport(dataset_id, VallarisServer, Api_Key)
        return dataExport

    except Exception as e:
        print(e)
        dataExport = False
        return dataExport


def CreateFeatures(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        collection = msgOption['id']
        dataset_id = collection
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]
        data = msgOption['data']
        dirpath = tempfile.mkdtemp()

        dataImport = getImport(dataset_id,
                               data, VallarisServer, Api_Key)
        shutil.rmtree(dirpath)

        if dataImport != "something wrong":
            return dataImport

        else:
            dataImport = False
            return dataImport

    except Exception as e:
        print(e)
        dataImport = False
        return dataImport


def UpdateFeatures(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        dataset_id = msgOption['collectionId']
        features_id = msgOption['featuresId']
        data = msgOption['data']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]
        dataEdit = editFeatures(dataset_id,
                                features_id, data,  VallarisServer, Api_Key)

        if dataEdit != "something wrong":
            return dataEdit

        else:
            dataEdit = False
            return dataEdit

    except Exception as e:
        print(e)
        dataEdit = False
        return dataEdit


def DeleteFeatures(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        dataset_id = msgOption['collectionId']
        features_id = msgOption['featuresId']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]
        dataDelete = delFeatures(
            dataset_id, features_id,  VallarisServer, Api_Key)

        if dataDelete != "something wrong":
            return dataDelete

        else:
            dataDelete = False
            return dataDelete

    except Exception as e:
        print(e)
        dataDelete = False
        return dataDelete


def CreateCollection(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        title = msgOption['title']
        description = msgOption['description']
        itemType = msgOption['itemType']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        dataNew = newCollection(
            title, description, itemType, VallarisServer, Api_Key)

        if dataNew != "something wrong":
            return dataNew

        else:
            dataNew = False
            return dataNew

    except Exception as e:
        print(e)
        dataNew = False
        return dataNew


def UpdateCollection(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        dataset_id = msgOption['id']
        title = msgOption['title']
        description = msgOption['description']
        itemType = msgOption['itemType']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        editImport = editCollection(
            dataset_id, title, description, itemType, VallarisServer, Api_Key)

        if editImport != "something wrong":
            return editImport

        else:
            editImport = False
            return editImport

    except Exception as e:
        print(e)
        dataImport = False
        return dataImport


def DeleteCollection(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        dataset_id = msgOption['id']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        deleteData = delCollection(dataset_id, VallarisServer, Api_Key)

        if deleteData != "something wrong":
            return deleteData

        else:
            deleteData = False
            return deleteData

    except Exception as e:
        print(e)
        deleteData = False
        return deleteData


def CreateVectorTile(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    try:
        msgOption = msgBody
        dataset_id = msgOption["data_filter"]['dataset_id']
        dataset_out = msgOption["data_filter"]['dataset_out']
        VallarisServer = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        tile = makeTile(dataset_id, dataset_out,
                        VallarisServer, Api_Key, parameter)

        if tile != "something wrong":
            return tile

        else:
            tile = False
            return tile

    except Exception as e:
        print(e)
        tile = False
        return tile


def ProcessSuccess(storage, parameter, msg, data):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    msgOption = msgBody
    _output = msgOption['process']['outputs'][0]['format']

    try:
        order = msgOption['process']['order']
    except:
        order = 1

    if "GeoJSON" in _output:
        _output = 'json'

    data.to_file(storage + '/' + str(_output) +
                 str(order) + ".gpkg", driver="GPKG")

    file_final_up = storage + '/' + str(_output) + str(order) + '.gpkg'
    out_msg = {
        "code": 200,
        "message": msg,
        "file": file_final_up
    }
    return json.dumps(out_msg)


def ProcessFail(storage, parameter, msg):
    try:
        msgBody = json.loads(parameter)["requestBody"]
    except:
        msgBody = parameter

    out_msg = {
        "code": 404,
        "message": msg,
        "file": "no data"
    }

    print("process failed")
    return json.dumps(out_msg)


def RenderFeatures(parameter, *args, **kwargs):
    opacity = kwargs.get('opacity', 0.4)
    color = kwargs.get('color', "#FF0000")
    HOST = os.environ["VallarisServer"]

    try:

        data_out2 = []
        try:
            geojson = parameter['data']
            geojson2 = geojson['geometry'].to_json()
            dump_json = json.loads(geojson2)
            data_ = {
                "id": str(parameter['name']),
                "data": dump_json,
                "layer_type": [parameter['layer_type']],
                "paint": {"opacity": opacity, "color": color},
            }
            data_out2.append(data_)

        except:
            crt = len(parameter)
            for i in range(0, crt):
                geojson = parameter[i]['data']
                geojson2 = geojson['geometry'].to_json()
                dump_json = json.loads(geojson2)
                data_ = {
                    "id": str(parameter[i]['name']),
                    "data": dump_json,
                    "layer_type": [parameter[i]['layer_type']],
                    "paint": {"opacity": opacity, "color": color},
                }
                data_out2.append(data_)

        parameter2 = {"features": data_out2}

        map_id = uuid.uuid4().hex
        map_id2 = '"'

        js_create = """
                <iframe id='"""+map_id+"""' " width="100%" height=336 src=""></iframe>
                <script>
                 var myinputstring = '{0}';    
                 var myurl = '{1}';
                document.getElementById("""+map_id2+map_id+map_id2+""").src = myurl
                function bake_storage(value) {{
                   value ?   localStorage.setItem('params', value) : localStorage.clear()
                }}

                bake_storage(myinputstring)
                </script>
            """

        def js_convert_str_html(p, url):
            js_convert = js_create.format(p, url)
            return HTML(js_convert)

        newurl = HOST + "/sandbox/render/iframe"
        mydict = {'params': parameter2, 'z': 5, 'p': 0, }

        jsobj = js_convert_str_html(json.dumps(mydict), newurl)
        # display(jsobj)

        return display(jsobj)

    except Exception as e:
        return 'error display :' + str(e)


def RenderCollection(parameter, *args, **kwargs):
    opacity = kwargs.get('opacity', 0.4)
    color = kwargs.get('color', "#FF0000")

    try:
        HOST = os.environ["VallarisServer"]
        data_out2 = []
        try:
            if parameter['layer_type'] == 'clusterPoint':
                _type = ['clusterPoint', 'clusterPointCount']
            else:
                _type = [parameter['layer_type']]

            Api_Key = os.environ["APIKey"]

            data_ = {"id": parameter['data'],
                     "api_key": Api_Key,
                     "paint":
                     {"opacity": float(opacity),
                      "color": color
                      },
                     "layer_type": _type

                     }
            data_out2.append(data_)

        except:
            crt = len(parameter)
            for i in range(0, crt):
                if parameter[i]['layer_type'] == 'clusterPoint':
                    _type = ['clusterPoint', 'clusterPointCount']
                else:
                    _type = [parameter[i]['layer_type']]

                data_ = {"id": parameter[i]['data'],
                         "api_key": Api_Key,
                         "paint":
                         {"opacity": float(opacity),
                          "color": color
                          },
                         "layer_type": _type
                         }

                data_out2.append(data_)

        data_items = {"collection": data_out2}

        params = json.dumps(data_items)

        mydict = {'params': params, 'z': 3, 'p': 0, 'host': HOST}

        qstr = urlencode(mydict)

        mapURL = '/sandbox/render/iframe?'

        url = HOST + mapURL + qstr

        out_iframe = IFrame(url, '100%', '336px')

        return out_iframe

    except Exception as e:
        return 'error display :' + str(e)


def RenderRaster(parameter, *args, **kwargs):
    opacity = kwargs.get('opacity', 1)
    option = kwargs.get('option', 'internal')

    if option == 'internal':
        SandboxFileserver = os.environ["SandboxFileserver"]
        LOGNAME = os.environ["LOGNAME"]
        url = SandboxFileserver + "/" + str(LOGNAME) + "/" + parameter['data']

    else:
        url = parameter['data']

    try:
        HOST = os.environ["VallarisServer"]
        data_items = {
            "coverage": [
                {
                    "id": "rasterHot",
                    "url": url,
                    "layer_name": parameter['layer_type'],
                    "VallarisServer": HOST,
                    "paint":{
                        "opacity": float(opacity)
                    }
                }
            ]
        }

        map_id = uuid.uuid4().hex
        map_id2 = '"'

        js_create = """
                 <iframe id='"""+map_id+"""' width="100%" height=336 src=""></iframe>
                <script>
                 var myinputstring = '{0}';    
                 var myurl = '{1}';
                document.getElementById("""+map_id2+map_id+map_id2+""").src = myurl
                function bake_storage(value) {{
                   value ?   localStorage.setItem('params', value) : localStorage.clear()
                }}

                bake_storage(myinputstring)
                </script>
            """

        def js_convert_str_html_raster(p, url):
            js_convert = js_create.format(p, url)
            return HTML(js_convert)

        mydict = {'params': data_items, 'z': 8, 'p': 0, }

        newurl = HOST + "/sandbox/render/iframe"

        jsobj = js_convert_str_html_raster(json.dumps(mydict), newurl)
        # display(jsobj)

        return display(jsobj)

    except Exception as e:
        return 'error display :' + str(e)


def RGBMap(parameter, *args, **kwargs):

    title = kwargs.get('title', "Maps")
    ylabel = kwargs.get('ylabel', "Row #")
    xlabel = kwargs.get('xlabel', "Column #")

    try:

        def normalize(array):
            '''
            normalize: normalize a numpy array so all value are between 0 and 1
            '''
            array_min, array_max = array.min(), array.max()
            return (array - array_min) / (array_max - array_min)

        # Open the file:
        raster = rasterio.open(parameter['data'])

        b1 = raster.read(parameter['band'][0])
        b2 = raster.read(parameter['band'][1])
        b3 = raster.read(parameter['band'][2])

        b1_norm = normalize(b1)
        b2_norm = normalize(b2)
        b3_norm = normalize(b3)

        nrg = np.dstack((b1_norm, b2_norm, b3_norm))

        fig, ax = plt.subplots(figsize=(12, 12))
        im = ax.imshow(nrg.squeeze())
        # ep.colorbar(im)
        ax.set(title=title)
        ax.set(xlabel=xlabel + '\n'+'\n' + '© Vallaris Maps')
        ax.set(ylabel=ylabel)

        return plt.show()

    except Exception as e:
        return 'error display :' + str(e)


def NDVIMap(parameter, *args, **kwargs):

    title = kwargs.get('title', "NDVI")
    ylabel = kwargs.get('ylabel', "Row #")
    xlabel = kwargs.get('xlabel', "Column #")

    try:

        # Open the file:
        raster = rasterio.open(parameter['data'])

        red = raster.read(parameter['red'])
        nir = raster.read(parameter['nir'])
        np.seterr(divide='ignore', invalid='ignore')
        c_map = kwargs.get('cmap', 'viridis')
        minn = kwargs.get('min', -1)
        maxx = kwargs.get('max', 1)

        # Calculate ndvi
        ndvi = (nir.astype(float)-red.astype(float)) / \
            (nir.astype(float)+red.astype(float))

        fig, ax = plt.subplots(figsize=(12, 12))
        im = ax.imshow(ndvi.squeeze(), cmap=c_map, vmin=minn, vmax=maxx)
        ep.colorbar(im)
        ax.set(title=title)
        ax.set(xlabel=xlabel + '\n'+'\n' + '© Vallaris Maps')
        ax.set(ylabel=ylabel)

        return plt.show()

    except Exception as e:
        return 'error display :' + str(e)


def RGBSave(parameter, *args, **kwargs):

    try:
        nodata = kwargs.get('nodata', -99)
        dtype = kwargs.get('dtype', "int8")

        # Open the file:
        raster = rasterio.open(parameter['input'])

        b1 = raster.read(parameter['band'][0])
        b2 = raster.read(parameter['band'][1])
        b3 = raster.read(parameter['band'][2])

        # Create the composite by stacking
        nrg = np.dstack((b1, b2, b3))

        ras_meta = raster.profile
        ras_meta['count'] = 3
        ras_meta['dtype'] = dtype
        ras_meta['nodata'] = nodata

        with rasterio.open(parameter['output'], 'w', **ras_meta) as dst:
            # If array is in (x, y, z) order (cols, rows, bands)
            dst.write(np.moveaxis(nrg, [0, 1, 2], [1, 2, 0]))

        return 'Succeed : ' + parameter['output']

    except Exception as e:
        return 'error to save :' + str(e)


def NDVISave(parameter, *args, **kwargs):
    nodata = kwargs.get('nodata', -99)
    dtype = kwargs.get('dtype', "float32")

    try:

        # Open the file:
        raster = rasterio.open(parameter['input'])

        red = raster.read(parameter['red'])
        nir = raster.read(parameter['nir'])
        np.seterr(divide='ignore', invalid='ignore')

        # Calculate ndvi
        ndvi = (nir.astype(float)-red.astype(float)) / \
            (nir.astype(float)+red.astype(float))

        ras_meta = raster.profile
        ras_meta['count'] = 1
        ras_meta['dtype'] = "float32"
        ras_meta['nodata'] = -99

        with rasterio.open(parameter['output'], 'w', **ras_meta) as dst:
            dst.write(ndvi, 1)

        return 'Succeed : ' + parameter['output']

    except Exception as e:
        return 'error to save :' + str(e)


def GrayMap(parameter, *args, **kwargs):

    title = kwargs.get('title', "Maps")
    ylabel = kwargs.get('ylabel', "Row #")
    xlabel = kwargs.get('xlabel', "Column #")
    minn = kwargs.get('min', "0")
    maxx = kwargs.get('max', "255")
    c_map = kwargs.get('cmap', "gray")

    try:

        # Open the file:
        raster = rasterio.open(parameter['data'])

        b1 = raster.read(parameter['band'])

        fig, ax = plt.subplots(figsize=(12, 12))
        im = ax.imshow(b1.squeeze(), cmap=c_map, vmin=minn, vmax=maxx)
        ep.colorbar(im)
        ax.set(title=title)
        ax.set(xlabel=xlabel + '\n'+'\n' + '© Vallaris Maps')
        ax.set(ylabel=ylabel)

        return plt.show()

    except Exception as e:
        # print(e)
        return 'error display :' + str(e)


def GraySave(parameter, *args, **kwargs):
    nodata = kwargs.get('nodata', -99)
    dtype = kwargs.get('dtype', "float32")

    try:

        # Open the file:
        raster = rasterio.open(parameter['input'])

        image = raster.read(parameter['band'])

        ras_meta = raster.profile
        ras_meta['count'] = 1
        ras_meta['dtype'] = "float32"
        ras_meta['nodata'] = -99

        with rasterio.open(parameter['output'], 'w', **ras_meta) as dst:
            dst.write(image, 1)

        return 'Succeed : ' + parameter['output']

    except Exception as e:
        print(e)
        return 'error to save : please check parameter'


def SearchData(satellite, *args, **kwargs):
    offset = kwargs.get('offset', 0)
    bbox = kwargs.get('bbox', False)
    datetime = kwargs.get('datetime', False)
    cloud_cover = kwargs.get('cloud_cover', False)
    path = kwargs.get('path', False)
    row = kwargs.get('row', False)
    relative_orbit_number = kwargs.get('relative_orbit_number', False)
    tile_number_field = kwargs.get('tile_number_field', False)

    try:

        payload = {
            "sortby": "-id",
            "limit": 10,
            "offset": offset
        }

        if bbox != False:
            payload['bbox'] = bbox

        if datetime != False:
            payload['datetime'] = datetime

        if satellite == 'Landsat8' or satellite == 'Landsat8':

            option = []
            if cloud_cover != False:

                cloud_ = {
                    "op": "<=",
                    "args": [
                        {
                            "property": "eo:cloud_cover"
                        },
                        cloud_cover
                    ]
                }
                option.append(cloud_)

            if path != False:

                path_ = {
                    "op": "=",
                    "args": [
                        {
                            "property": "landsat:wrs_path"
                        },
                        int(path)
                    ]
                }
                option.append(path_)

            if row != False:

                row_ = {
                    "op": "=",
                    "args": [
                        {
                            "property": "landsat:wrs_row"
                        },
                        int(row)
                    ]
                }
                option.append(row_)

            if cloud_cover != False or path != False or row != False:
                payload['filter'] = {"op": "and",
                                     "args": option
                                     }

        if satellite == 'Sentinel2':
            option = []

            if cloud_cover != False:

                cloud_ = {
                    "op": "<=",
                    "args": [
                        {
                            "property": "cloud_coverage"
                        },
                        cloud_cover
                    ]
                }
                option.append(cloud_)

            if relative_orbit_number != False:

                relative_orbit_number_ = {
                    "op": "=",
                    "args": [
                        {
                            "property": "relative_orbit_number"
                        },
                        relative_orbit_number
                    ]
                }
                option.append(relative_orbit_number_)

            if tile_number_field != False:

                tile_number_field_ = {
                    "op": "=",
                    "args": [
                        {
                            "property": "tile_number_field"
                        },
                        tile_number_field
                    ]
                }
                option.append(tile_number_field_)

            if cloud_cover != False or relative_orbit_number != False or tile_number_field != False:
                payload['filter'] = {"op": "and",
                                     "args": option
                                     }

        # print(payload)
        HOST = os.environ["VallarisServer"]
        url = HOST + "/core/api/stac/1.0/"+satellite+"/search"
        Api_Key = os.environ["APIKey"]

        payload = json.dumps(payload)
        headers = {
            'API-Key': Api_Key,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        # print(response.text)

        res_json = response.json()
        crt_res_json = len(res_json['features'])

        results = []

        for i in range(0, crt_res_json):
            results.append(res_json['features'][i]['id'])

        json_results = {
            "data": results,
            "context": res_json['context']
        }

        return json_results

    except Exception as e:
        return 'error :' + str(e)


def GetItem(satellite, collection):

    try:
        HOST = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]
        url = HOST + "/core/api/stac/1.0/"+satellite + \
            "/search?collections=" + str(collection)
        payload = {}
        headers = {
            'API-Key': Api_Key,
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        res_json = response.json()

        return res_json['features']

    except Exception as e:
        return 'error :' + str(e)


def ExportCoverage(collection, *args, **kwargs):

    try:
        satellite = kwargs.get('satellite', False)
        vallarisCoveage = kwargs.get('vallaris', True)
        Api_Key = os.environ["APIKey"]
        HOST = os.environ["VallarisServer"]

        print("start perform download")

        # get catalog id

        url = HOST + "/core/api/catalogue/1.0/catalogues"

        payload = {}
        headers = {
            'API-Key': Api_Key
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        res_json = response.json()
        # print(res_json['context']['matched'])

        matched = res_json['context']['matched'] + 1

        url = HOST + "/core/api/catalogue/1.0/catalogues?limit=" + str(matched)

        payload = {}
        headers = {
            'API-Key': Api_Key
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        res_json = response.json()
        # print(res_json['catalogues'])

        crt = len(res_json['catalogues'])

        arr = []
        for i in range(0, crt):

            data = res_json['catalogues'][i]['stac_id']
            if data == 'THEOS1':
                data2 = res_json['catalogues'][i]['id']
                arr.append(data2)

        if satellite != False:

            url = HOST + "/core/api/stac/1.0/"+satellite + \
                "/search?collections=" + str(collection)
            HOST = os.environ["VallarisServer"]
            Api_Key = os.environ["APIKey"]

            payload = {}
            headers = {
                'API-Key': Api_Key,
                'Content-Type': 'application/json'}

            response = requests.request(
                "GET", url, headers=headers, data=payload)
            res_json = response.json()

            url_dl = res_json['features'][0]['assets']['download']['href']

            # url = url_dl + "?api_key=" + str(Api_Key)

            print("start download")

            url = HOST + "/core/api/catalogue/1.0/download"

            payload = json.dumps({
                "url": url_dl,
                "catalogue_id": arr[0]
            })
            headers = {
                'API-Key': Api_Key,
                'Content-Type': 'application/json'
            }

            response = requests.request(
                "POST", url, headers=headers, data=payload)
            data = response.content

            d = response.headers['content-disposition']
            filename = re.findall("filename=(.+)", d)[0]

            with open(filename, 'wb') as s:
                s.write(data)

            print("runing download : " + filename)

            fileURL = filename.split(".")[-1]
            get_data = True

            print("runing download : " + filename)

        elif satellite == False and vallarisCoveage != False:

            url = HOST + "/core/api/coverages/1.0-beta/manager/" + \
                str(collection) + "?api_key=" + str(Api_Key)
            print("start download")

            remotefile = urlopen(url)
            blah = remotefile.info()['Content-Disposition']
            value, params = cgi.parse_header(blah)
            filename = params["filename"]
            urlretrieve(url, filename)
            print("runing download : " + str(filename))

            fileURL = filename.split(".")[-1]
            get_data = True

        else:

            get_data = False

        if get_data != False:

            if fileURL.split(".")[-1] == 'zip':
                newpath = filename
                new_folder = newpath.split(".")[0]

                if not os.path.exists(newpath):
                    os.makedirs(new_folder)

                with zipfile.ZipFile(newpath, 'r') as zip_ref:
                    zip_ref.extractall(new_folder)

            elif fileURL.split(".")[-1] == 'tar' or fileURL.split(".")[-1] == 'gz':
                newpath = filename
                new_folder = newpath.split(".")[0]

                if not os.path.exists(newpath):
                    os.makedirs(new_folder)
                # open file
                file = tarfile.open(newpath)

                # extracting file
                file.extractall(new_folder)
                file.close()

            elif fileURL.split(".")[-1] == 'tif' or fileURL.split(".")[-1] == 'tiff' or fileURL.split(".")[-1] == 'TIF':
                return "succeed store file : " + str(filename)

            else:
                pass
                return "error : fiile not support"
        else:
            return "error : get data failed"

        return "succeed store in folder : " + str(new_folder)

    except Exception as e:
        return 'error :' + str(e)


def BandStack(parameter):

    try:
        stack_band_paths = parameter['input']
        raster_out_path = parameter['output']

        stack_band_paths.sort()
        # Create image stack and apply nodata value for Landsat
        arr_st, meta = es.stack(
            stack_band_paths, out_path=raster_out_path)

        return 'Succeed : ' + parameter['output']

    except Exception as e:
        print(e)
        return 'error to save : please check parameter'


def CreateCoverage(parameter, *args, **kwargs):
    thumbnail = kwargs.get('thumbnail', [1, 2, 3])

    try:
        Api_Key = os.environ["APIKey"]
        file_in = parameter['data']
        file_get = file_in.split("/")[-1]

        shutil.copy(file_in, file_get)

        zip_id = uuid.uuid4().hex
        file_out = zip_id + ".zip"

        with zipfile.ZipFile(file_out, mode="w") as archive:
            archive.write(file_get)

        print("running create zipfile : " + file_out)

        HOST = os.environ["VallarisServer"]

        url = HOST + "/core/api/utilities/1.0/files"
        payload = {'authRequired': 'true',
                   'expiresIn': '1d1h1m1s'
                   }
        headers = {
            'API-Key': Api_Key
        }

        files = [('files', (file_out, open(file_out, 'rb'), 'application/zip'))]

        response = requests.request(
            "POST", url, headers=headers, data=payload, files=files)

        # print(response.json())
        data = response.json()
        file_import = data['files'][0]['id']
        collection = parameter['id']

        print("running import coverage")

        url = HOST + "/core/api/coverages/1.0-beta/manager/import/" + \
            str(collection)+"/jobs"
        payload = json.dumps({
            "option": {
                "type": "internalStorage",
                "config": {
                    "type": "file",
                    "file": {
                        "stack": True,
                        "merge": False,
                        "inputPath": file_import,
                        "fileName": ""
                    }
                },
                "thumbnail": {
                    "band": [
                        thumbnail[0],
                        thumbnail[1],
                        thumbnail[2]
                    ]
                },
                "mimeType": "tif"
            }
        })
        headers = {
            'API-Key': Api_Key,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        try:
            response_json = response.json()
            getjobID = response_json['jobID']
            # print(getjobID)
            print("start import coverage")

        except:
            return response.text

        while True:
            time.sleep(10)
            response_st = requests.request(
                "GET", f"{HOST}/core/api/coverages/1.0-beta/manager/import/{collection}/jobs/" + getjobID, headers=headers, data=payload)
            print(
                f'{str(response_st.json()["status"])} : {str(response_st.json()["progress"])} %')
            if str(response_st.json()["progress"]) == "100" and response_st.json()["status"] == "succeed":
                status = response_st.json()["status"]
                break

            if response_st.json()["status"] == "failed":
                status = response_st.json()["status"]
                break

        if os.path.exists(zip_id + ".zip"):
            os.remove(zip_id + ".zip")

        if status == "succeed":
            return 'Succeed : ' + HOST + "/management/studio/coverages/" + collection

        else:
            return 'error to create coverage : failed'

    except Exception as e:
        if os.path.exists(zip_id + ".zip"):
            os.remove(zip_id + ".zip")

        print(e)
        return 'error to create coverage : ' + str(e)


def CreateCoverageTile(parameter, *args, **kwargs):

    try:
        reverse = kwargs.get('reverse', 'false')
        get_class = kwargs.get('color', False)

        collection_in = parameter['dataset_id']
        collection_out = parameter['dataset_out']
        style = parameter['style']

        HOST = os.environ["VallarisServer"]
        Api_Key = os.environ["APIKey"]

        if style == 'gray':

            url = HOST + "/core/api/coverages/1.0-beta/manager/style/" + \
                str(collection_in)+"/jobs?type=gray"

        elif style == 'rgb':

            url = HOST + "/core/api/coverages/1.0-beta/manager/style/" + \
                str(collection_in)+"/jobs?type=rgb"

        elif style == 'classification':

            if get_class != False:

                crt_class = len(get_class)

                min_ = []
                max_ = []

                for i in range(0, crt_class):
                    min_.append(get_class[i]['min'])
                    max_.append(get_class[i]['max'])

                min_get = min(min_)
                max_get = max(max_)

                total = np.array([min_, max_])
                mean_get = np.mean(total)
                stDev_get = np.std(total)

                option = {
                    "type": "classification",
                    "band": 1,
                    "noData": -999,
                    "stats": [
                            {
                                "band1": {
                                    "maximum": max_get,
                                    "mean": mean_get,
                                    "minimum": min_get,
                                    "stDev": stDev_get
                                }
                            }
                    ],
                    "classes": crt_class,
                    "method": "EqualInterval",
                    "color": get_class,
                    "opacity": 100
                }

                # print(option)

            else:

                err = {
                    "error": 'no class for create style',
                    "class": [
                        {
                            "min": 0.0,
                            "max": 58.6,
                            "color": "#08488e"
                        },
                        {
                            "min": 58.6,
                            "max": 117.2,
                            "color": "#135fa7"
                        },
                        {
                            "min": 117.2,
                            "max": 175.8,
                            "color": "#2676b8"
                        }
                    ]
                }

                return err

            # url = HOST + "/core/api/coverages/1.0-beta/manager/style/"+str(collection_in)+"/jobs?type=classification&method=EqualInterval&classes=10&color=viridis&reverse=" + str(reverse)

        else:
            return 'error to create coverage tile : style not support'

        print("running create coverage tile")

        if style != 'classification':

            payload = ""
            headers = {
                'API-Key': Api_Key,
                'Content-Type': 'application/json'
            }

            response = requests.request(
                "POST", url, headers=headers, data=payload)

            # print(response)

            print("strat create coverage tile")

            response_json = response.json()
            # print(response_json)

            option = response_json['styleDefault']['option']

        option_style = {
            "option": option,
            "collection": {
                "input": collection_in,
                "output": collection_out
            }
        }

        # print(option_style)
        url = HOST + "/core/api/coverages/1.0-beta/manager/maketile/"+collection_in+"/jobs"
        payload = json.dumps(option_style)
        headers = {
            'API-Key': Api_Key,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)

        try:
            job_json = response.json()
            getjobID = job_json['jobID']
            # print(getjobID)
            print("start create coverage tile")
        except:
            return response.text

        while True:
            time.sleep(10)
            response_st = requests.request(
                "GET", f"{HOST}/core/api/coverages/1.0-beta/manager/maketile/{collection_in}/jobs/" + getjobID, headers=headers, data=payload)
            print(
                f'{str(response_st.json()["status"])} : {str(response_st.json()["progress"])} %')
            if str(response_st.json()["progress"]) == "100" and response_st.json()["status"] == "succeed":
                status = response_st.json()["status"]
                break

            if response_st.json()["status"] == "failed":
                status = response_st.json()["status"]
                break

        if status == "succeed":
            return 'Succeed : ' + HOST + "/management/studio/tiles-coverage/" + collection_out

        else:
            return 'error to create coverage : failed'

    except Exception as e:
        print(e)
        return 'error to create coverage : ' + str(e)
