# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hashwd']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4,<2.0', 'pyperclip>=1.8,<2.0', 'requests>=2.24,<3.0']

setup_kwargs = {
    'name': 'hashwd',
    'version': '0.0.3',
    'description': 'A script to generate a strong, random password',
    'long_description': 'None',
    'author': 'Jordan Langland',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
