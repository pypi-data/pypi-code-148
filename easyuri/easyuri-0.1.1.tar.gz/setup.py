# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['easyuri']
install_requires = \
['hstspreload>=2023.1.1,<2024.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'easyuri',
    'version': '0.1.1',
    'description': 'a smart interface on a dumb URL parser',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/projects/easyuri',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
