# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['warp10']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.2.0,<3.0.0',
 'numpy>=1.22.2,<2.0.0',
 'replit>=3.2.4,<4.0.0',
 'sanic>=22.6.2,<23.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'warp10',
    'version': '0.1.1',
    'description': 'SPA Framework',
    'long_description': None,
    'author': 'Zeb',
    'author_email': 'zceboys@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.11',
}


setup(**setup_kwargs)
