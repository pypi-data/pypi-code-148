# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webint_guests', 'webint_guests.templates']

package_data = \
{'': ['*']}

install_requires = \
['webint>=0.0']

entry_points = \
{'webapps': ['guests = webint_guests:app']}

setup_kwargs = {
    'name': 'webint-guests',
    'version': '0.0.2',
    'description': 'manage website guests',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
