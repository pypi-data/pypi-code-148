# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['excelr']
setup_kwargs = {
    'name': 'excelr',
    'version': '0.2.0',
    'description': '',
    'long_description': 'None',
    'author': 'Daniel Bradburn',
    'author_email': 'daniel@crunchrapps.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
