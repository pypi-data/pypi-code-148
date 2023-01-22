# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gatekeep']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gatekeep',
    'version': '0.1.1',
    'description': 'A login systeme for low-security deployment',
    'long_description': None,
    'author': 'Liam',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
