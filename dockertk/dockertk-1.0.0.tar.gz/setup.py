# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dockertk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dockertk',
    'version': '1.0.0',
    'description': '',
    'long_description': '',
    'author': 'wayfaring-stranger',
    'author_email': 'zw6p226m@duck.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
