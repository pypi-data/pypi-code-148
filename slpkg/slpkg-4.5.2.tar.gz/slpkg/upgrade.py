#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.blacklist import Blacklist
from slpkg.dependencies import Requires
from slpkg.configs import Configs


class Upgrade(Configs, Utilities):
    """ Upgrade the installed packages. """

    def __init__(self, file_pattern):
        super(Configs, self).__init__()
        super(Utilities, self).__init__()
        self.file_pattern = file_pattern

    def packages(self):
        """ Compares version of packages and returns the maximum. """
        repo_packages = SBoQueries('').sbos()
        black = Blacklist().get()
        upgrade, requires = [], []

        installed = self.all_installed(self.file_pattern)

        for pkg in installed:
            inst_pkg_name = self.split_installed_pkg(pkg)[0]

            if inst_pkg_name not in black and inst_pkg_name in repo_packages:

                if self.is_repo_version_bigger(inst_pkg_name, self.file_pattern):
                    requires += Requires(inst_pkg_name).resolve()
                    upgrade.append(inst_pkg_name)

        # Clean the packages if they are dependencies
        for pkg in upgrade:
            if pkg not in requires:
                yield pkg
