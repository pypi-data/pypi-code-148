BANNER = """
*---------------------------------------------------------------*
*                      Alvon Analysis ONVIF                     *
* Copyright (c) 2023, Transline Tech, Ltd. All rights reserved. *
*---------------------------------------------------------------*
"""
print(BANNER)
from alvonOnvif.CameraClient import Camera
from alvonOnvif.StreamHandler import Stream
from alvonOnvif.OnvifUtils import ExtrasHelper, CreateLogger, AlertLogger
