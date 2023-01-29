# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lory']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lory',
    'version': '0.0.1',
    'description': 'An integration testing framework written in Python :)',
    'long_description': '# lory\n\nAn integration testing framework written in Python :)\n\n# NotImplementedYet\n',
    'author': 'Vitaman02',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
