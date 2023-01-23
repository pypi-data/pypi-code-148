# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['asjs']
setup_kwargs = {
    'name': 'asjs',
    'version': '0.1.0',
    'description': 'Python module for implement object with syntax from JavaScript',
    'long_description': None,
    'author': 'Alexander Podstrechnyy',
    'author_email': 'tankalxat34@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
