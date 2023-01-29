# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['my_test_project']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'my-test-project',
    'version': '0.1.0',
    'description': 'This is my first test project on PyPI.org',
    'long_description': '',
    'author': 'Mahad',
    'author_email': 'mahadahmed99@yahoo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
