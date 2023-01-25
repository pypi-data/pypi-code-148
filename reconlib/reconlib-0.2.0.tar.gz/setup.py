# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reconlib',
 'reconlib.core',
 'reconlib.crtsh',
 'reconlib.hackertarget',
 'reconlib.utils']

package_data = \
{'': ['*']}

install_requires = \
['pytest-mock>=3.10.0,<4.0.0', 'pytest>=7.2.1,<8.0.0']

setup_kwargs = {
    'name': 'reconlib',
    'version': '0.2.0',
    'description': 'A collection of modules and helpers for active and passive reconnaissance of remote hosts',
    'long_description': None,
    'author': 'eonraider',
    'author_email': 'livewire_voodoo@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
