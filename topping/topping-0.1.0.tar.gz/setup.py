# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['topping']

package_data = \
{'': ['*']}

install_requires = \
['rich>=13.2.0,<14.0.0']

setup_kwargs = {
    'name': 'topping',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'jenz',
    'author_email': '2025.jenz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
