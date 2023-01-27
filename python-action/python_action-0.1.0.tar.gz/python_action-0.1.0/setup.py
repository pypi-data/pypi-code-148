# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_action']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-action',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'mateusbrandao',
    'author_email': 'mateus.brandaoteixeira@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
