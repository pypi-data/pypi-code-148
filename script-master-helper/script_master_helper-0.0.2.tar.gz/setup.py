# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['script_master_helper',
 'script_master_helper.executor',
 'script_master_helper.executor.client',
 'script_master_helper.workplanner',
 'script_master_helper.workplanner.client']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp', 'asyncio', 'pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'script-master-helper',
    'version': '0.0.2',
    'description': '',
    'long_description': '',
    'author': 'Pavel Maksimov',
    'author_email': 'vur21@ya.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pavelmaksimov/script-master-helper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
