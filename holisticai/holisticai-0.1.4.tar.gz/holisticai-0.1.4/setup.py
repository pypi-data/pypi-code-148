# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['holisticai']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'holisticai',
    'version': '0.1.4',
    'description': '',
    'long_description': 'None',
    'author': 'GBadila',
    'author_email': 'gabriel.badila@holisticai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
