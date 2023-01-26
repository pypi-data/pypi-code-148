# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roll_the_dice']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['dice = roll_the_dice.cli:app']}

setup_kwargs = {
    'name': 'roll-the-dice',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Guilherme',
    'author_email': 'marquesguilherme3@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
