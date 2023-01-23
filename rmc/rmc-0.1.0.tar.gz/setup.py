# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rmc', 'rmc.exporters']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0,<9.0', 'rmscene>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['rmc = rmc.cli:cli']}

setup_kwargs = {
    'name': 'rmc',
    'version': '0.1.0',
    'description': 'Convert to/from v6 .rm files from the reMarkable tablet',
    'long_description': 'None',
    'author': 'Rick Lupton',
    'author_email': 'mail@ricklupton.name',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
