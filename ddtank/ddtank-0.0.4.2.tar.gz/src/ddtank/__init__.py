__all__ = ['ddtask', 'status', 'initialize']

import win32api
import win32con
import win32gui
import win32ui
import time
import string
import cv2
import numpy as np
import re

from ctypes import windll
from threading import Thread

VkKeyScanA = windll.user32.VkKeyScanA
