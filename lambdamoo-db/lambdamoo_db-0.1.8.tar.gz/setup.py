# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lambdamoo_db']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.2.0,<23.0.0', 'cattrs>=22.2.0,<23.0.0', 'click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['moodb2flat = lambdamoo_db.cli:moodb2flat']}

setup_kwargs = {
    'name': 'lambdamoo-db',
    'version': '0.1.8',
    'description': 'Parser for LambdaMOO databases',
    'long_description': '# LambdaMOO database reader and exporter\n\nFill me in!\n\n## cli commands\n`moodb2flat DBFile Directory`',
    'author': 'Katelyn Gigante',
    'author_email': 'clockwork.singularity@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
