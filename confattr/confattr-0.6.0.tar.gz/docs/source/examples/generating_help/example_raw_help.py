#!../../../../venv/bin/python3

import typing

from confattr import ConfigFile
from argparse import RawTextHelpFormatter

if typing.TYPE_CHECKING:
	from . import example
else:
	import example

config_file = ConfigFile(appname=__package__, formatter_class=RawTextHelpFormatter)
print(config_file.get_help())
