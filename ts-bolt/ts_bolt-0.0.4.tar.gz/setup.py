# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ts_bolt',
 'ts_bolt.datamodules',
 'ts_bolt.datasets',
 'ts_bolt.datasets.downloaders']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'cloudpathlib>=0.12.1,<0.13.0',
 'gluonts>=0.11.7,<0.12.0',
 'loguru>=0.6.0,<0.7.0',
 'pandas==1.5.2',
 'pydantic>=1.10.4,<2.0.0',
 'pytorch-lightning>=1.8.6,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'strenum>=0.4.9,<0.5.0',
 'torch>=1.13.1,<2.0.0']

entry_points = \
{'console_scripts': ['bolt = ts_bolt.cli:bolt']}

setup_kwargs = {
    'name': 'ts-bolt',
    'version': '0.0.4',
    'description': 'The Lightning Bolt for Time Series Data and Models',
    'long_description': 'None',
    'author': 'LM',
    'author_email': 'hi@leima.is',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
