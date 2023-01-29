# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trabalho_final']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'trabalho-final',
    'version': '0.1.0',
    'description': 'Trabalho individual e final',
    'long_description': '',
    'author': 'anacarolinarodrigues',
    'author_email': 'anacarolinarodrigues480@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
