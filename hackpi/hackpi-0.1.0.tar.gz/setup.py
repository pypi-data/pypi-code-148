# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hackpi']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.89.1,<0.90.0',
 'pydantic>=1.10.4,<2.0.0',
 'sqlalchemy>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'hackpi',
    'version': '0.1.0',
    'description': 'HackPi - is a library for the FastAPI framework that adds additional functionality that simplifies development.',
    'long_description': '',
    'author': 'thenesterov',
    'author_email': 'thenesterov@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/thenesterov/hackpi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
