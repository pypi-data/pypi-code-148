# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['safe_ds',
 'safe_ds._util',
 'safe_ds.classification',
 'safe_ds.classification.metrics',
 'safe_ds.data',
 'safe_ds.exceptions',
 'safe_ds.plotting',
 'safe_ds.regression',
 'safe_ds.regression.metrics']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.3,<4.0.0',
 'pandas>=1.5.3,<2.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'seaborn>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'safe-ds',
    'version': '0.1.0',
    'description': 'The Safe-DS standard library.',
    'long_description': 'None',
    'author': 'Lars Reimann',
    'author_email': 'mail@larsreimann.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
