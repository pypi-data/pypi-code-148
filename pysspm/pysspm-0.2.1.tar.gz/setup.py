# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysspm', 'pysspm.cli', 'pysspm.lib']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'pandas>=1.5.0,<2.0.0',
 'tabulate>=0.8.10,<0.9.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['sspm = pysspm.sspm:main']}

setup_kwargs = {
    'name': 'pysspm',
    'version': '0.2.1',
    'description': 'Simple Scientific Project Manager.',
    'long_description': 'None',
    'author': 'Aaron Ponti',
    'author_email': 'aaron.ponti@bsse.ethz.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aarpon/pysspm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
