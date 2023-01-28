# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['berri_ai']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'berri-ai',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Team Berri',
    'author_email': 'clerkieai@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
