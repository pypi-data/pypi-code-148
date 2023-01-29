# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gces_arthur']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gces-arthur',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Eduardo Gurgel',
    'author_email': '51385738+EduardoGurgel@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
