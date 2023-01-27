# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transmep']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8,<4.0',
 'arch>=5.2.0,<6.0.0',
 'captum>=0.5,<0.6',
 'click>=8.1,<9.0',
 'deap>=1.3.3,<2.0.0',
 'fair-esm>=1.0.2,<2.0.0',
 'fsspec>=2022.3,<2023.0',
 'kaleido==0.2.1',
 'numpy>=1.21,<2.0',
 'plotly>=5.7,<6.0',
 'questionary>=1.10,<2.0',
 'requests>=2.27,<3.0',
 'scikit-learn>=1.0,<2.0',
 'torch==1.12.1',
 'tqdm>=4.64,<5.0']

entry_points = \
{'console_scripts': ['transmep = transmep.cli:main']}

setup_kwargs = {
    'name': 'transmep',
    'version': '0.1.0',
    'description': 'Transfer learning for Mutation Effect Prediction',
    'long_description': 'None',
    'author': 'Tilman Hoffbauer',
    'author_email': 'tilman.hoffbauer@rwth-aachen.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
