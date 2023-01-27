# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['recval', 'recval.metrics']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.56.4,<0.57.0',
 'numpy>=1.23.5,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'pytest-xdist>=3.1.0,<4.0.0',
 'strenum>=0.4.9,<0.5.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'recval',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': "Edoardo D'Amico",
    'author_email': 'damicoedoardo95@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
