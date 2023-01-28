# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypi_poetry_project']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypi-poetry-project',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'antoniotoineto',
    'author_email': 'netocaastro10@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
