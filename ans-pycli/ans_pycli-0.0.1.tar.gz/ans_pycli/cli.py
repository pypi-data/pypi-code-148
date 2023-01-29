import argparse
from os import environ
from ans_pycli.helpers import set_val

from .commands import (
    DevCommand, mixins
)

is_debug = environ.get("DEBUG", "false").lower() in ["true", "1"]
if is_debug:
    print("DEBUG MODE ENABLED")


class CLI(mixins.HasSubparsers):
    _DEBUG: bool = None
    _description: str = None

    _subparsers: mixins.SubparsersDictType = {
        "commands": [
            DevCommand(),
        ],
    }

    def __init__(self, description: str = None, DEBUG: bool = None):
        set_val(self, "_description", description,
                "PyCli is a CLI for your Python project", _type=str)
        set_val(self, "_DEBUG", DEBUG, is_debug, _type=bool)

        self.parser = argparse.ArgumentParser(description=self._description)
        self._init_subparsers(self.parser)

        self.parser.add_argument(
            "args", nargs="*", help="Arguments for the command")

    def run(self):
        args = self.parser.parse_args()
        res = args.func()
        if self._DEBUG:
            print('Args: \n', args)
            print('Result: \n', res)


def cli():
    CLI().run()
