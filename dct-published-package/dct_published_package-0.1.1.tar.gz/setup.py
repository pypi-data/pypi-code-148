# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dct_published_package']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dct-published-package',
    'version': '0.1.1',
    'description': '',
    'long_description': '### dct-published-package\n\nThis is a test to publish a Python package using Poetry.',
    'author': 'Mihai Vladu',
    'author_email': 'vladuomihai@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
