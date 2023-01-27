# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webint_data', 'webint_data.templates']

package_data = \
{'': ['*']}

install_requires = \
['webint>=0.0']

entry_points = \
{'webapps': ['data = webint_data:app']}

setup_kwargs = {
    'name': 'webint-data',
    'version': '0.0.45',
    'description': 'manage the data on your website',
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
