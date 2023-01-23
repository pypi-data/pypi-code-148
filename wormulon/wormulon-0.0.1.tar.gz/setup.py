# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wormulon']

package_data = \
{'': ['*']}

install_requires = \
['paramiko>=2.11.0,<3.0.0']

setup_kwargs = {
    'name': 'wormulon',
    'version': '0.0.1',
    'description': '',
    'long_description': 'None',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
