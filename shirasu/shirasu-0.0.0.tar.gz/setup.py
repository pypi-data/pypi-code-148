# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shirasu', 'shirasu.internal']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'ujson>=5.7.0,<6.0.0', 'websockets>=10.4,<11.0']

setup_kwargs = {
    'name': 'shirasu',
    'version': '0.0.0',
    'description': 'A developer-friendly bot framework based on OneBot',
    'long_description': '# Shirasu\n\nA developer-friendly bot framework based on OneBot.\n\nDeveloping. WIP.\n',
    'author': 'kifuan',
    'author_email': 'kifuan@foxmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
