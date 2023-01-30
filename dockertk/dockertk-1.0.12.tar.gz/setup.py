# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dockertk']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.1,<7.0']

setup_kwargs = {
    'name': 'dockertk',
    'version': '1.0.12',
    'description': '',
    'long_description': '',
    'author': 'wayfaring-stranger',
    'author_email': 'zw6p226m@duck.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
