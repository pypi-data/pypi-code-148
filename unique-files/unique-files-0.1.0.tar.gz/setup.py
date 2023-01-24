# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unique_files', 'unique_files.scripts']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['unique_files = unique_files.scripts.unique_files:main']}

setup_kwargs = {
    'name': 'unique-files',
    'version': '0.1.0',
    'description': 'The command returns a list of unique files from two directories',
    'long_description': None,
    'author': 'Andrii Chernov',
    'author_email': 'andreych1998@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
