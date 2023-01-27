import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))  # enables relative local imports

import dataclasses

#import info
from info_impl import *


@dataclasses.dataclass
class PackageInfo:
    full_name: str
    version: str


def package_info2() -> PackageInfo:
    return PackageInfo("cbl_test_package.info", "2.0.2")  # "1.0.1"

