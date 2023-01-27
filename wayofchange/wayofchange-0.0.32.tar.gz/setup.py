# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wayofchange']

package_data = \
{'': ['*'], 'wayofchange': ['wayOfChange.egg-info/*']}

setup_kwargs = {
    'name': 'wayofchange',
    'version': '0.0.32',
    'description': '',
    'long_description': 'Read me now',
    'author': 'Edrihan Levesque',
    'author_email': 'edrihan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
