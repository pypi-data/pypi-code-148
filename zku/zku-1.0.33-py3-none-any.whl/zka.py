# -*- coding: utf-8 -*-
# Copyright (c) 2016-2021 Zymbit, Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# .. codeauthor:: Scott Miller <scott@zymbit.com>

"""Loader for the Zymkey App Library.

This module loads the C library `libzk_app_utils.so` for importation into the
main module of the Zymkey App Utils Library.

Notes
-----
The `zkalib` object must be set in this separate module and imported into the
main module in order for Sphinx autodoc to be able to mock the import. See
the relevant configuration in docs/conf.py:

    autodoc_mock_imports = [
        "zymkey.zka",
    ]

Attributes
----------
zkalib : CDLL
    The loaded Zymkey library path that will be imported by the main module.
"""

import os
import errno

from ctypes import cdll, CDLL

import distutils.sysconfig

from .exceptions import ZymkeyLibraryError
from .settings import ZYMKEY_LIBRARY_PATH

zkalib: CDLL
loaded_lib = None
_prefixes = []
for prefix in (distutils.sysconfig.get_python_lib(), ""):
    _zymkey_library_path = "{}{}".format(prefix, ZYMKEY_LIBRARY_PATH)
    if os.path.exists(_zymkey_library_path):
        loaded_lib = cdll.LoadLibrary(_zymkey_library_path)
        break
    else:
        _prefixes.append(os.path.dirname(_zymkey_library_path))
else:
    raise ZymkeyLibraryError(
        "unable to find {}, checked {}".format(
            os.path.basename(ZYMKEY_LIBRARY_PATH), _prefixes
        )
    )

zkalib = loaded_lib

__all__ = [
    "zkalib",
]
