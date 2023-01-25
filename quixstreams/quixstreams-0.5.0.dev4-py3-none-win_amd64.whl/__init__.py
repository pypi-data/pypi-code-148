# The version will get automatically updated as part of setup
__version__ = "0.5.0.dev4"

import os
import sysconfig
import ctypes

from .native.Python.InteropHelpers.InteropUtils import InteropUtils

plat = sysconfig.get_platform()
lib_dir = os.path.join(os.path.dirname(__file__), "./native/" + plat + "/Quix.Sdk.Streaming.Interop/")
if plat.startswith("win"):
    allowed_extensions = [".dll"]
    lib_dll = "Quix.Sdk.Streaming.Interop.dll"
    for file in os.listdir(lib_dir):
        if file == lib_dll:
            continue
        allowed = False
        for ext in allowed_extensions:
            if file.endswith(ext):
                allowed = True
                break
        if not allowed:
            continue
        ctypes.cdll.LoadLibrary(lib_dir + file)
elif plat.startswith("macosx"):
    allowed_extensions = [".dylib"]
    lib_dll = "Quix.Sdk.Streaming.Interop.dylib"
    # TODO improve so not so hardcoded
    if plat.endswith("x86_64"):
        lib_dir = os.path.join(os.path.dirname(__file__), "../../macosx-10_12-x86_64/Quix.Sdk.Streaming.Interop/")
    if plat.endswith("arm64"):
        lib_dir = os.path.join(os.path.dirname(__file__), "../../macosx_11_0_arm64/Quix.Sdk.Streaming.Interop/")
elif plat.startswith("linux"):
    allowed_extensions = [".so"]
    lib_dll = "Quix.Sdk.Streaming.Interop.so"
else:
    raise Exception("Platform {} is not supported".format(plat))

lib = ctypes.cdll.LoadLibrary(lib_dir + lib_dll)
InteropUtils.set_lib(lib)


from .models import *
from .quixstreamingclient import QuixStreamingClient
from .streamreader import StreamReader
from .app import App, CancellationTokenSource, CancellationToken
from .kafkastreamingclient import KafkaStreamingClient
from .raw import RawMessage

from .outputtopic import OutputTopic

from .configuration import *
#from .inputtopic import InputTopic
#from .streamwriter import StreamWriter

#from .logging import Logging, LogLevel
#from .state import LocalFileStorage
