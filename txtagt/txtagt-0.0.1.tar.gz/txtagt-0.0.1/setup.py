# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['txtagt']
setup_kwargs = {
    'name': 'txtagt',
    'version': '0.0.1',
    'description': 'a txt agent',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/txtagt',
    'py_modules': modules,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
