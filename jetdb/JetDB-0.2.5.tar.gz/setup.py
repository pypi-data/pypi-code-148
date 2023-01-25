# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jetdb']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jetdb',
    'version': '0.2.5',
    'description': 'This module is designed for everyone to have an easier time handling txt files. JSON file handling will be added soon.',
    'long_description': None,
    'author': 'Srijeet Aditya',
    'author_email': 'adityasrijeet12355@egmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
