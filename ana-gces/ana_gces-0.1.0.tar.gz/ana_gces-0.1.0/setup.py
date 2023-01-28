# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ana_gces']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ana-gces',
    'version': '0.1.0',
    'description': 'Trabalho Final de GCES',
    'long_description': 'None',
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
