#  -*- coding: utf-8 -*-
"""

Author: Rafael R. L. Benevides
Date: 1/26/23

"""

from setuptools import Extension, setup


setup(ext_modules=[
    Extension('smet.utils', sources=['smet/utils.c']),
])
