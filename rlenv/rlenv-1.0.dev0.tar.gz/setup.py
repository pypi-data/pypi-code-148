#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Accenta Gym Environment

# Copyright (c) 2019-2022 Accenta (www.accenta.ai)

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


# SETUP VARIABLES #############################################################

from rlenv import get_version

VERSION = get_version()

AUTHOR_NAME = 'Jérémie DECOCK'
AUTHOR_EMAIL = 'jeremie.decock@accenta.ai'

PYPI_PACKAGE_NAME = 'rlenv'
PROJECT_SHORT_DESC = 'Accenta.AI Gym Environement'
PROJECT_WEB_SITE_URL = ''

# See :  http://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = ['Development Status :: 4 - Beta',
               'Intended Audience :: Developers',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development :: Libraries',
               'Topic :: Software Development :: Libraries :: Python Modules',
               'Topic :: Software Development :: Libraries :: Application Frameworks']

KEYWORDS = 'rlenv'

# You can either specify manually the list of packages to include in the
# distribution or use "setuptools.find_packages()" to include them
# automatically with a recursive search (from the root directory of the
# project).
PACKAGES = find_packages()
#PACKAGES = ['rlenv']


# The following list contains all dependencies that Python will try to
# install with this project
# E.g. INSTALL_REQUIRES = ['pyserial >= 2.6']
INSTALL_REQUIRES = [
    'coverage',
    'gym==0.26.2',
    'matplotlib==3.5.3',
    'numpy==1.21.6',
    'pandas==1.3.5',
    'pytest==7.1.3',
    'pyyaml==6.0',
    'scipy',
    'seaborn',
    'setuptools',
    'Sphinx',
    'sphinx-gallery',
    'sphinx-rtd-theme'
]


# E.g. SCRIPTS = ["examples/pyax12demo"]
SCRIPTS = []


# Entry point can be used to create plugins or to automatically generate
# system commands to call specific functions.
# Syntax: "name_of_the_command_to_make = package.module:function".
# E.g.:
#   ENTRY_POINTS = {
#     'console_scripts': [
#         'pyax12gui = pyax12.gui:run',
#     ],
#   }
ENTRY_POINTS = {}


README_FILE = 'README.rst'

def get_long_description():
    with open(README_FILE, 'r') as fd:
        desc = fd.read()
    return desc


###############################################################################

setup(author=AUTHOR_NAME,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR_NAME,
      maintainer_email=AUTHOR_EMAIL,

      name=PYPI_PACKAGE_NAME,
      description=PROJECT_SHORT_DESC,
      long_description=get_long_description(),
      url=PROJECT_WEB_SITE_URL,
      download_url=PROJECT_WEB_SITE_URL, # Where the package can be downloaded

      classifiers=CLASSIFIERS,
      keywords=KEYWORDS,

      packages=PACKAGES,
      include_package_data=True, # Use the MANIFEST.in file

      install_requires=INSTALL_REQUIRES,
      #platforms=['Linux'],
      #requires=[],

      scripts=SCRIPTS,
      entry_points=ENTRY_POINTS,

      version=VERSION)
