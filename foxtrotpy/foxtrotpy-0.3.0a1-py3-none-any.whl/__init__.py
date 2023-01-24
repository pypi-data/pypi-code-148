import sys
import os

import pkg_resources

#NOTE: hack to make protobuf imports work properly
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(FILE_DIR, "protos"))

try:
    vers = pkg_resources.get_distribution("foxtrotpy").version
except pkg_resources.DistributionNotFound:
    vers = "unknown"

__version__ = vers


