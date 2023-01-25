# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py3gpp']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.0,<2.0.0']

setup_kwargs = {
    'name': 'py3gpp',
    'version': '0.1.2',
    'description': 'functions for 5G NR signal processing',
    'long_description': "[![CI](https://github.com/catkira/py3gpp/actions/workflows/lint_and_test.yml/badge.svg)](https://github.com/catkira/py3gpp/actions/workflows/lint_and_test.yml)\n[![Pylint](https://catkira.github.io/py3gpp/pylint.svg)](https://github.com/catkira/py3gpp/actions/workflows/python-package.yml)\n[![PyPI version](https://badge.fury.io/py/py3gpp.svg)](https://badge.fury.io/py/py3gpp)\n[![Downloads](https://pepy.tech/badge/py3gpp)](https://pepy.tech/project/py3gpp)\n\n# Summary\nThis python package aims to replace the Matlab 5G Toolbox in Python. The call syntax of functions is the same as in matlab where possible. There are some differences, because matlab allows to continuously index a multidimensional array in one axis. In python this is not possible, therefore the result of functions like nrPBCHIndices() is also multidimensional here to make it compatible with Python.\n\n# Installation\n'python3 -m pip install py3gpp'\nor\nclone this repo and then do 'python3 -m pip install -e .'\n\n# Getting started\nrun 'examples/test_py3gpp.ipynb'\n\nThe example data is ideal data generated with Matlab, but the code has been tested with real data that has CFO, SFO and noise.\n\n# Documentation\nSee Matlab documentation of equivalent function\n",
    'author': 'Benjamin Menküc',
    'author_email': 'benjamin@menkuec.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/catkira/py3gpp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
