import os
import sys

# enables relative local imports
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# select visible/importable
from info_impl import platform_info, PlatformInfo, package_info, PackageInfo

from importlib.metadata import version
#__version__ = version(__name__)
print(f"here init: {__name__}, {version(__name__)}")
