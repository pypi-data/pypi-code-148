# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arena_integrations', 'arena_integrations.tests']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26,<2.0', 'pyspark>=3.3,<4.0']

setup_kwargs = {
    'name': 'arena-integrations',
    'version': '0.0.7',
    'description': '',
    'long_description': 'None',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
