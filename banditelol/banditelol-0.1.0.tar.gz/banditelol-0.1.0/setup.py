# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['banditelol']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'banditelol',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Adit RP',
    'author_email': 'aditya.putra@pitik.id',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
