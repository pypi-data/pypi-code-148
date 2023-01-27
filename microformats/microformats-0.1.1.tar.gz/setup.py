# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mf']
install_requires = \
['easyuri>0.0.12',
 'lxml>=4.9.2,<5.0.0',
 'mf2py>=1.1.2,<2.0.0',
 'mf2util>=0.5.2,<0.6.0',
 'requests>=2.28.2,<3.0.0',
 'txtint>0.0.68']

entry_points = \
{'console_scripts': ['mf = mf:main']}

setup_kwargs = {
    'name': 'microformats',
    'version': '0.1.1',
    'description': 'tools for Microformats production, consumption and analysis',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
