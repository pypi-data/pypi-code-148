# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poepi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poepi',
    'version': '0.1.2',
    'description': 'Poepi package',
    'long_description': '',
    'author': 'vodovi',
    'author_email': 'vodovi4524@crtsec.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
