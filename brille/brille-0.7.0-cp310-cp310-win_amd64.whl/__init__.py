# Copyright © 2020 Greg Tucker <greg.tucker@stfc.ac.uk>
#
# This file is part of brille.
#
# brille is free software: you can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# brille is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with brille. If not, see <https://www.gnu.org/licenses/>.

"""Python module :py:mod:`brille`
=================================

This module provides access to the C++ brille library which can be used to
interact with spacegroup and pointgroup symmetry operations, to determine the
first Brillouin zone for a given real space crystallographic lattice, to
find *an* irreducible polyhedron from the first Brillouin zone and the
pointgroup operations of a spacegroup, to construct polyhedron-filling connected
point networks, and to perform linear-interpolation of user-provided data for
any reciprocal space point at a symmetry-equivalent position within the
connected point network.

.. currentmodule:: brille

.. autosummary::
    :toctree: _generate
"""


# start delvewheel patch
def _delvewheel_init_patch_1_2_0():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'brille.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    if not is_pyinstaller or os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_init_patch_1_2_0()
del _delvewheel_init_patch_1_2_0
# end delvewheel patch


from .bound import *
from .lattice import Lattice
from . import utils

try:
    from . import plotting
except ModuleNotFoundError:
    # Build servers don't have Matplotlib installed; plotting not tested
    pass