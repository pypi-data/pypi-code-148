#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs
from slpkg.views.ascii import Ascii
from slpkg.queries import SBoQueries
from slpkg.models.models import SBoTable
from slpkg.models.models import session as Session


class Dependees:
    """ Show which packages depend. """

    def __init__(self, packages: list, flags: list):
        self.packages = packages
        self.flags = flags
        self.flag_full_reverse = '--full-reverse'
        self.flag_pkg_version = '--pkg-version'
        self.configs = Configs
        self.session = Session
        self.ascii = Ascii()
        self.llc = self.ascii.lower_left_corner
        self.hl = self.ascii.horizontal_line
        self.var = self.ascii.vertical_and_right
        self.colors = self.configs.colour
        self.color = self.colors()
        self.bold = self.color['bold']
        self.violet = self.color['violet']
        self.cyan = self.color['cyan']
        self.grey = self.color['grey']
        self.yellow = self.color['yellow']
        self.byellow = f'{self.bold}{self.yellow}'
        self.endc = self.color['endc']

    def slackbuilds(self):
        """ Collecting the dependees. """
        print(f"The list below shows the "
              f"packages that dependees on '{', '.join([p for p in self.packages])}':\n")

        for pkg in self.packages:
            dependees = list(self.find_requires(pkg))

            package = f'{self.byellow}{pkg}{self.endc}'

            if self.flag_pkg_version in self.flags:
                package = f'{self.byellow}{pkg}-{SBoQueries(pkg).version()}{self.endc}'

            print(package)

            print(f' {self.llc}{self.hl}', end='')

            if not dependees:
                print(f'{self.cyan} No dependees{self.endc}')

            sp = ' ' * 4
            for i, dep in enumerate(dependees, start=1):
                dependency = f'{self.cyan}{dep[0]}{self.endc}'

                if self.flag_pkg_version in self.flags:
                    dependency = (f'{self.cyan}{dep[0]}{self.endc}-{self.yellow}'
                                  f'{SBoQueries(dep[0]).version()}{self.endc}')

                if i == 1:
                    print(f' {dependency}')
                else:
                    print(f'{sp}{dependency}')

                if self.flag_full_reverse in self.flags:
                    if i == len(dependees):
                        print(" " * 4 + f' {self.llc}{self.hl} {self.violet}{dep[1]}{self.endc}')
                    else:
                        print(" " * 4 + f' {self.var}{self.hl} {self.violet}{dep[1]}{self.endc}')

            print(f'\n{self.grey}{len(dependees)} dependees for {pkg}{self.endc}\n')

    def find_requires(self, sbo):
        """ Find requires that slackbuild dependees. """
        requires = self.session.query(SBoTable.name, SBoTable.requires).all()
        for req in requires:
            if [r for r in req[1].split() if r == sbo]:
                yield req
