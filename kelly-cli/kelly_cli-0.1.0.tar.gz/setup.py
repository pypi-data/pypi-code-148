# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kelly_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'pybet>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['kelly = kelly_cli.kelly:kelly',
                     'test_kelly = tests.test_kelly:runner']}

setup_kwargs = {
    'name': 'kelly-cli',
    'version': '0.1.0',
    'description': 'A command line tool for calculating the Kelly Criterion betting stake for given odds and bank size',
    'long_description': 'This is a simple command line tool to allow the user to calculate the optimal stake at given market odds for a given true odds and a given bank size, as determined by the [Kelly Criterion](https://en.wikipedia.org/wiki/Kelly_criterion)\n\nInstall as follows:\n\n`pip install kelly-cli`\n\nthen run `kelly --help` at the command line for full instructions.\n',
    'author': 'peaky76',
    'author_email': 'robertjamespeacock@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
