#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tomli
from pathlib import Path

from slpkg.configs import Configs


class Blacklist(Configs):
    """ Reads and returns the blacklist. """

    def __init__(self):
        super(Configs, self).__init__()

    def get(self) -> list:
        """ Reads the blacklist file. """
        file = Path(self.etc_path, 'blacklist.toml')
        if file.is_file():
            with open(file, 'rb') as black:
                return tomli.load(black)['blacklist']['packages']
