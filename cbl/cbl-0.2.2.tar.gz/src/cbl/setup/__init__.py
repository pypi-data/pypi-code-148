# (C) 2023 A. Voß setup@codebasedlearning.dev, a.voss@fh-aachen.de

import os
import sys

# enables relative local imports
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# select visible/importable
from package_impl import about_package, PackageInfo
from platform_impl import about_platform, PlatformInfo
from python_impl import about_python, PythonInfo
