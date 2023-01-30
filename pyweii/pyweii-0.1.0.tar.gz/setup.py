# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyweii']

package_data = \
{'': ['*']}

install_requires = \
['evdev>=1.6.1,<2.0.0']

entry_points = \
{'console_scripts': ['weii = pyweii.cli:cli']}

setup_kwargs = {
    'name': 'pyweii',
    'version': '0.1.0',
    'description': 'A utility to measure weight using the Wii Balance Board.',
    'long_description': 'Weii\n====\n\nWeii (pronounced "weigh") is a small script that connects to a Wii Balance Board, reads a weight measurement, and disconnects.\nWeii is the new, redesigned spiritual successor to [gr8w8upd8m8](https://github.com/skorokithakis/gr8w8upd8m8).\n',
    'author': 'Stavros Korokithakis',
    'author_email': 'hi@stavros.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/stavros/weii',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
