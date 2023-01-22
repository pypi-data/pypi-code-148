# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rshanker779_common', 'rshanker779_common.mixins']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2', 'snakeviz>=2.1.1']

setup_kwargs = {
    'name': 'rshanker779-common',
    'version': '1.0.1a1',
    'description': '',
    'long_description': '[![PyPI version](https://badge.fury.io/py/rshanker779-common.svg)](https://badge.fury.io/py/rshanker779-common)\n\n[![Build Status](https://travis-ci.com/rshanker779/rshanker779_common.svg?branch=master)](https://travis-ci.com/rshanker779/rshanker779_common)\n\n[![Coverage Status](https://coveralls.io/repos/github/rshanker779/rshanker779_common/badge.svg?branch=master)](https://coveralls.io/github/rshanker779/rshanker779_common?branch=master)\n\nCommon utilities for my projects\n',
    'author': 'Rohan Shanker',
    'author_email': 'rshanker779@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
