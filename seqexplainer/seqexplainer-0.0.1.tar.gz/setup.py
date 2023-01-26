# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seqexplainer']

package_data = \
{'': ['*']}

install_requires = \
['captum>=0.5.0,<0.6.0',
 'logomaker>=0.8,<0.9',
 'matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.21.5,<2.0.0',
 'torch>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'seqexplainer',
    'version': '0.0.1',
    'description': 'A tool for interpreting sequence input genomics PyTorch models',
    'long_description': None,
    'author': 'adamklie',
    'author_email': 'aklie@ucsd.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
