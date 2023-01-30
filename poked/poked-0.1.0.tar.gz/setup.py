# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poked']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'gql>=3.4.0,<4.0.0',
 'pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'poked',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Kyle Kelley',
    'author_email': 'rgbkrk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
