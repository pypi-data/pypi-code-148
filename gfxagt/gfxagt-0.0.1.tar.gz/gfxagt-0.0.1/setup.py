# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['gfxagt']
setup_kwargs = {
    'name': 'gfxagt',
    'version': '0.0.1',
    'description': 'a GUI agent',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/gfxagt',
    'py_modules': modules,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
