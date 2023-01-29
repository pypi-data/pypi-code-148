# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['copyright_cli', 'copyright_cli.cli_parsers', 'copyright_cli.internal']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.11.6,<0.12.0']

entry_points = \
{'console_scripts': ['copyright = copyright_cli.cli:main']}

setup_kwargs = {
    'name': 'copyright-cli',
    'version': '0.1.0rc2',
    'description': '',
    'long_description': 'None',
    'author': 'Nicholas Johnson',
    'author_email': 'nicholas.m.j@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
