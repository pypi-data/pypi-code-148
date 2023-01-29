# read version from installed package
from importlib.metadata import version
from chembox.chembox import *
__version__ = version("chembox")