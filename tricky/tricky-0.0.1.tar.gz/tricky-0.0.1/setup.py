# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['__init__']
setup_kwargs = {
    'name': 'tricky',
    'version': '0.0.1',
    'description': 'A set of useful features to make working with your code easier.',
    'long_description': '# tricky',
    'author': 'Alexander Walther',
    'author_email': 'alexander.walther.engineering@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Walther-s-Engineering/tricky',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
