# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tipe']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tipe',
    'version': '0.1.4',
    'description': '',
    'long_description': '',
    'author': 'Denis Mishankov',
    'author_email': 'mishankov@mail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
