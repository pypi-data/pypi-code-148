# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webint_auth', 'webint_auth.templates']

package_data = \
{'': ['*']}

install_requires = \
['indieauth>=0.0', 'webint>=0.0']

entry_points = \
{'webapps': ['auth = webint_auth:app']}

setup_kwargs = {
    'name': 'webint-auth',
    'version': '0.0.7',
    'description': 'manage website owner authentication',
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
