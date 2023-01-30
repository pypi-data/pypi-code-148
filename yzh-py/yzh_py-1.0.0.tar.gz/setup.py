#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (C) 云账户
# All rights reserved.

"""
Setup script for log service SDK.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from yzh_py import __version__

requirements = [
    'requests>=2.19.1',
    'pycryptodome==3.10.1',
]

long_description = """
Python SDK for 云账户 
"""

packages = [
    'yzh_py',
    'yzh_py.client',
    'yzh_py.client.api',
    'yzh_py.client.api.model',
]

setup(
    name='yzh_py',
    version=__version__,
    description='yunzhanghu service Python client SDK',
    author='yunzhanghu',
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=packages,
    long_description=long_description,
)
