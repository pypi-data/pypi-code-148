import os
import sys
from pyrogram import Client

from darmilibs.darmi.helper.adminHelpers import *
from darmilibs.darmi.helper.aiohttp_helper import*
from darmilibs.darmi.helper.basic import *
from darmilibs.darmi.helper.cmd import *
from darmilibs.darmi.helper.constants import *
from darmilibs.darmi.helper.data import *
from darmilibs.darmi.helper.inline import *
from darmilibs.darmi.helper.interval import *
from darmilibs.darmi.helper.parser import *
from darmilibs.darmi.helper.PyroHelpers import *
from darmilibs.darmi.helper.utility import *
from darmilibs.darmi.helper.what import *


def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Darmi"])

