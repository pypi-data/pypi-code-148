import copy
import logging
import hashlib
import dateutil
from json import JSONDecoder, JSONEncoder
import aiostream

import a2grunner.stdouts_redirects as stdout_redirects

import traceback
from RestrictedPython.PrintCollector import PrintCollector

# Other dependencies
from datetime import datetime, timedelta, date, timezone
from dateutil.relativedelta import *
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from exchangelib import OAuth2Credentials,Build,Version,Configuration, OAUTH2,Account,IMPERSONATION,Message,Mailbox,FileAttachment,HTMLBody
import bisect
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from time import strftime, strptime
import time
import math
import random
import shapely
import shapely.geometry
from shapely.strtree import STRtree
import io
import boto
import boto3
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as plotcm
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64
import numpy as np
from matplotlib import gridspec
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from fpdf import FPDF, HTMLMixin
import xlsxwriter
from pyproj import Proj
import pyproj
from scipy import spatial
from scipy.spatial import cKDTree
from sklearn.neighbors import KDTree
from pyclipper import PyclipperOffset, ET_CLOSEDPOLYGON, JT_ROUND
import pyclipper as pyclip
from bson.objectid import ObjectId
import pytz
import requests
import sys
import os
import asyncio
import psutil
from urllib.parse import quote
import pandas as pd
import os
from pathlib import Path
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
import pickle as pkl
import xgboost
from staticmap import StaticMap, CircleMarker, Line, IconMarker
from PIL import Image, ImageDraw, ImageFont, ImageOps
import matplotlib.ticker as ticker
from textwrap import wrap
from statistics import mean
import warnings
import copy
import dateutil.parser
import imgkit
import base64
import multiprocessing
import threading
import statistics
from joblib import Parallel, delayed
import aiohttp
import asyncio
import pdfkit
import pusher
import decimal
import msal
import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes
import matplotlib.patches as mpatches
from matplotlib.pyplot import Axes
from exchangelib import OAuth2Credentials,Build,Version,Configuration, OAUTH2,Account,IMPERSONATION,Message,Mailbox,FileAttachment,HTMLBody
from openpyxl import Workbook, load_workbook
from openpyxl.styles.protection import  Protection
from uuid import uuid4

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                '__type__' : 'datetime',
                'info': obj.isoformat()
            }
        else:
            return JSONEncoder.default(self, obj)


class DateTimeDecoder(json.JSONDecoder):
    def __init__(self, *args, **kargs):
        JSONDecoder.__init__(self, object_hook=self.dict_to_object,
                             *args, **kargs)
    def dict_to_object(self, d):
        if '__type__' not in d:
            return d

        type = d.pop('__type__')
        try:
            dateobj = dateutil.parser.parse(d['info'])
            return dateobj
        except:
            d['__type__'] = type
            return d

async def simulate_run(file_url: str, is_config: list, api_key: str, customer: str):
    def __create_stream_map(is_config: list, api_key: str, customer: str):
        stream_data = {}
        if not os.path.exists("a2grunnercache"):
            os.makedirs("a2grunnercache")

        try:
            for data_map in is_config:
                cache_key = hashlib.md5(json.dumps(data_map).encode("utf-8")).hexdigest()
                read_cache = False

                if 'cache_name' in data_map:
                    cache_key = data_map['cache_name']

                cache_file = f'a2grunnercache/{data_map["alias"]}{cache_key}.json'
                data_elements = None
                if 'cache' in data_map and data_map['cache'] == True:
                    try:
                        with open(cache_file, encoding='utf8') as json_file:
                            data_elements = json.load(json_file, cls=DateTimeDecoder)
                            stream_data[data_map['alias']] = data_elements
                            print(
                                f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')} - Retrieved {len(data_elements)} for {data_map['alias']} in file {cache_file}")
                            read_cache = True
                    except Exception as e:
                        print(
                            f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')} - Failed to read cache for {data_map['alias']} on file {cache_file}")

                if data_elements is None:
                    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                    params = {
                        'apiKey': api_key,
                        'customerName': customer
                    }

                    for key, value in data_map.items():
                        params[f'cfg[{key}]'] = value

                    r = requests.post("https://listen.a2g.io/v1/production/streamdata", data=params, headers=headers)
                    if r.status_code == 200:
                        data_elements = r.json()

                        for d in data_elements:
                            for k, v in d.items():
                                try:
                                    if isinstance(v, str):
                                        dv = dateutil.parser.parse(v)
                                        dt = dv.replace(tzinfo=None)
                                        d[k] = dt
                                except ValueError:
                                    continue

                        stream_data[data_map['alias']] = data_elements
                        print(
                            f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')} - Retrieved {len(data_elements)} values for {data_map['alias']}")

                        if 'cache' in data_map and data_map['cache'] == True and read_cache == False:
                            with open(cache_file, 'w', encoding='utf8') as json_file:
                                json.dump(data_elements, json_file, ensure_ascii=False, cls=DateTimeEncoder)
                                print(
                                    f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')} - Cached {len(data_elements)} values in file {cache_file} for {data_map['alias']}")

                    else:
                        stream_data[data_map['alias']] = []
                        print(
                            f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')} - Failed to retrieve info for {data_map['alias']}, error: {r.text}")
        except Exception as e:
            tb = traceback.format_exc()
            print("An error ocurred while the fx_runner was running " + str(e) + "\n" + tb)

        return stream_data

    print(f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')} - Preparing Run")
    print_str = ""
    try:
        user_fx = ""
        with open(file_url, encoding="UTF-8") as f:
            user_fx = f.read()

        print(f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')} - Read User FX from File {file_url}, Length: {len(user_fx)}")
        data_map = __create_stream_map(is_config, api_key, customer)

        print(f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')} - User Fx Running")

        _print_ = PrintCollector
        stdout_redirects.enable_proxy()
        string_io = stdout_redirects.redirect()

        loc = locals().copy()
        glob = globals().copy()

        # We build the data map
        query_map = {}
        profiles = []

        glob['query_manager'] = None
        glob['custom_payload'] = {}
        glob['stream_data'] = data_map
        glob['query_map'] = query_map
        glob['profiles'] = profiles
        glob['_print_'] = _print_
        glob['printed'] = []

        mlogger = logging.getLogger('matplotlib')
        mlogger.setLevel(logging.ERROR)

        exec(user_fx, glob, loc)

        if 'async def user_fx()' in user_fx:
            result_obj, printed = await loc['user_fx']()
        else:
            result_obj, printed = loc['user_fx']()

        printed = string_io.getvalue().strip()
        stdout_redirects.stop_redirect()

        print(f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')} - User Fx Finished")

        del glob
        del loc

        return result_obj, printed, True
    except Exception as e:
        tb = traceback.format_exc()
        printed = string_io.getvalue().strip()
        stdout_redirects.stop_redirect()
        print(f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')} - User Fx FAILED")
        print(f"{datetime.now().strftime('%d-%b-%Y %H:%M:%S')} - An error ocurred while the fx_runner was running {str(e)}\n{tb}")

    return [], printed, False