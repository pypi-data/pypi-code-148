# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webint_owner', 'webint_owner.templates']

package_data = \
{'': ['*']}

install_requires = \
['webint>=0.0']

entry_points = \
{'webapps': ['owner = webint_owner:app']}

setup_kwargs = {
    'name': 'webint-owner',
    'version': '0.0.4',
    'description': 'manage website ownership',
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
