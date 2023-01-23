# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dadeschools']
entry_points = \
{'console_scripts': ['dadeschools = dadeschools:main']}

setup_kwargs = {
    'name': 'dadeschools',
    'version': '1.6',
    'description': 'The Ultimate Dadeschools CLI',
    'long_description': "# dadeschools\n\n## Installation\n`pip install dadeschools`\n\n## Usage\nRun 'dadeschools' in the terminal\n\n`dadeschools`\n\nThen enter your ID number to get grades from dadeschools.net\n",
    'author': 'BananaApache',
    'author_email': 'daniel.miami2005@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
