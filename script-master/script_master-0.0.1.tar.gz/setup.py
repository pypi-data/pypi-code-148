# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['script_master', 'script_master.notebook']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aiopath>=0.6.11,<0.7.0',
 'asyncio>=3.4.3,<4.0.0',
 'better-exceptions>=0.3.3,<0.4.0',
 'confz==1.8.1',
 'fastapi>=0.88,<0.89',
 'jinja2>=3.1.2,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'orjson>=3.8.4,<4.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'typer>=0.7.0,<0.8.0',
 'uvicorn[standart]>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['script-master = script_master.cli:cli']}

setup_kwargs = {
    'name': 'script-master',
    'version': '0.0.1',
    'description': '',
    'long_description': 'None',
    'author': 'Pavel Maksimov',
    'author_email': 'vur21@ya.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pavelmaksimov/script-master',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
