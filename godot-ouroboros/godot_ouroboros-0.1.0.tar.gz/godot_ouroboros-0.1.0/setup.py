# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['godot_ouroboros']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.21.1,<0.22.0']

entry_points = \
{'console_scripts': ['publish = publish:main']}

setup_kwargs = {
    'name': 'godot-ouroboros',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Jonathan Crum',
    'author_email': 'jcrum@theobogroup.com',
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
