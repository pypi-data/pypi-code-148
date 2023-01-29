# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['script_master_ui', 'script_master_ui.routers']

package_data = \
{'': ['*'],
 'script_master_ui': ['templates/*',
                      'templates/includes/*',
                      'templates/pages/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'confz>=1.8,<2.0',
 'fastapi>=0.88,<0.89',
 'pydantic>=1.9.0,<2.0.0',
 'script-master-helper>=0.0.2,<0.0.3',
 'typer>=0.7.0,<0.8.0',
 'uvicorn[standart]>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['script-master-ui = script_master_ui.cli:cli']}

setup_kwargs = {
    'name': 'script-master-ui',
    'version': '0.0.1',
    'description': '',
    'long_description': '# Script-Master UI\n\nВеб интерфейс для [Script-Master](https://github.com/pavelmaksimov/script-master).',
    'author': 'Pavel Maksimov',
    'author_email': 'vur21@ya.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pavelmaksimov/script-master-ui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
