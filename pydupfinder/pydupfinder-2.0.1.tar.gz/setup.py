# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydupfinder']

package_data = \
{'': ['*']}

install_requires = \
['click-option-group>=0.5.5,<0.6.0', 'click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['pydupfinder = pydupfinder.pydupfinder:cli']}

setup_kwargs = {
    'name': 'pydupfinder',
    'version': '2.0.1',
    'description': '',
    'long_description': '# pydupfinder\n\n```Usage: pydupfinder [OPTIONS] PATH\n\n  Find duplicate files.\n\nOptions:\n  Limits: [mutually_exclusive]    Limits for found duplicates\n    -a, --at-least INTEGER RANGE  Find AT LEAST that many duplicates if there\n                                  are enough duplicates.  [x>=2]\n    -m, --max-size TEXT           Calculate checksums for AT MOST this total\n                                  size of files.\n  -r, --reset-cache               Remove database, caching checksums\n  --help                          Show this message and exit.\n```\n\n`max-size` limit allows one, for example, find duplicates in OneDrive without downloading everything.\n',
    'author': 'Alexey Vyskubov',
    'author_email': 'alexey@ocaml.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
