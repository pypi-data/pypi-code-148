#!/usr/bin/env python
#
# This file is part of the magnum.np distribution
# (https://gitlab.com/magnum.np/magnum.np).
# Copyright (c) 2023 magnum.np team.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from distutils.core import setup

setup(name='magnumnp',
      version='v1.0.1',
      description='magnum.np finite-difference package for the solution of micromagnetic problems',
      author='Florian Bruckner',
      author_email='florian.bruckner@univie.ac.at',
      url='http://gitlab.com/magnum.np/magnum.np',
      packages=['magnumnp', 'magnumnp.common', 'magnumnp.field_terms', 'magnumnp.loggers', 'magnumnp.solvers', 'magnumnp.utils'],
      install_requires = [
            'torch',
            'numpy',
            'scipy',
            'setproctitle',
            'pyvista',
            'xitorch'
            ]
     )
