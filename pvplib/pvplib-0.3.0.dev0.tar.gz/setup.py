# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pvplib']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.23.5,<2.0.0',
 'scipy<=1.9',
 'statsmodels>=0.13.5,<0.14.0']

setup_kwargs = {
    'name': 'pvplib',
    'version': '0.3.0.dev0',
    'description': 'Library to compute PVPs per https://arxiv.org/pdf/1804.05021.pdf',
    'long_description': None,
    'author': 'anonymous',
    'author_email': 'chisub7893@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
