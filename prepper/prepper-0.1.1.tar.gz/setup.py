# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prepper']

package_data = \
{'': ['*']}

install_requires = \
['aenum>=3.1.11,<4.0.0',
 'h5py>=3.8.0,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'numpy>=1.24.1,<2.0.0']

setup_kwargs = {
    'name': 'prepper',
    'version': '0.1.1',
    'description': 'Allows python objects to be stored and loaded from an HDF5 file',
    'long_description': '',
    'author': 'Varchas Gopalaswamy',
    'author_email': 'vgop@lle.rochester.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
