# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['unclick']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.0,<9.0.0']

setup_kwargs = {
    'name': 'unclick',
    'version': '0.1.0b1',
    'description': 'A reverse parser for the click CLI library',
    'long_description': '# unclick\n\n![Versions](https://img.shields.io/badge/python-3.8+-blue)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Test](https://github.com/albireox/unclick/actions/workflows/test.yml/badge.svg)](https://github.com/albireox/unclick/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/albireox/unclick/branch/main/graph/badge.svg)](https://codecov.io/gh/albireox/unclick)\n\nA reverse parser for [click](https://click.palletsprojects.com).\n',
    'author': 'José Sánchez-Gallego',
    'author_email': 'gallegoj@uw.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
