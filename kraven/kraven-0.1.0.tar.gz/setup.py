# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kraven']

package_data = \
{'': ['*']}

install_requires = \
['furl>=2.1.3,<3.0.0',
 'glom>=23.1.1,<24.0.0',
 'gql[httpx,requests]>=3.4.0,<4.0.0',
 'httpx>=0.23.3,<0.24.0',
 'rich>=13.2.0,<14.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'kraven',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Kraven',
    'author': 'Jeremy Zabala',
    'author_email': 'jeremy.zbala@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<3.12',
}


setup(**setup_kwargs)
