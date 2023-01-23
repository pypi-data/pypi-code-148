# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['theseptatimes']

package_data = \
{'': ['*']}

install_requires = \
['DateTime>=5.0,<6.0',
 'colorama>=0.4.6,<0.5.0',
 'requests>=2.28.2,<3.0.0',
 'thefuzz[speedup]>=0.19.0,<0.20.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['tst = theseptatimes.cli:main']}

setup_kwargs = {
    'name': 'theseptatimes',
    'version': '0.2.4',
    'description': 'A Python package to get data from the Septa API',
    'long_description': '<h2 align="center"> ━━━━━━  ❖  ━━━━━━ </h2>\n\n<!-- BADGES -->\n<div align="center">\n   <p></p>\n   \n   <img src="https://img.shields.io/github/stars/dotzenith/TheSeptaTimes?color=F8BD96&labelColor=302D41&style=for-the-badge">   \n\n   <img src="https://img.shields.io/github/forks/dotzenith/TheSeptaTimes?color=DDB6F2&labelColor=302D41&style=for-the-badge">   \n\n   <img src="https://img.shields.io/github/repo-size/dotzenith/TheSeptaTimes?color=ABE9B3&labelColor=302D41&style=for-the-badge">\n   \n   <img src="https://img.shields.io/github/commit-activity/y/dotzenith/TheSeptaTimes?color=96CDFB&labelColor=302D41&style=for-the-badge&label=COMMITS"/>\n   <br>\n</div>\n\n<p/>\n\n---\n\n### ❖ TheSeptaTimes\n\nTheSeptaTimes is a python package designed to make accessing info about Septa\'s regional rail network easier. I made this because I commute to college every day via septa, and checking the time for the next train via the app or the website simply takes too much time. I wanted something I could access from my terminal, and thus, TheSeptaTimes was born. \n\n  <img src="https://github.com/dotzenith/dotzenith/blob/main/assets/TheSeptaTimes/septa.gif" alt="septa gif">\n\n---\n\n### ❖ Installation\n\n> Install from pip\n\n```sh\npip3 install TheSeptaTimes\n```\n\n> Install from source\n- First, install [poetry](https://python-poetry.org/)\n\n```sh\ngit clone https://github.com/dotzenith/TheSeptaTimes.git\ncd TheSeptaTimes\npoetry build\npip3 install ./dist/theseptatimes-0.2.4.tar.gz\n```\n\n---\n\n### ❖ Usage\n\n```sh\nUsage: tst [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  arrivals  Find the next arrivals at a given train station\n  next      Search for the next train going from an origin to a destination\n  search    Search for a given station\n  train     Track a given train using it\'s number\n```\n\n> Fuzzy search for a train station\n```sh\ntst search admr\n```\n\n> Get times for the next two trains that go from a given train station to another\n```sh\ntst next \'30th Street Station\' \'North Philadelphia\'\n```\n\n> List the next 6 arrivals at a given train station\n```sh\ntst arrivals \'30th Street Station\' 6\n```\n\n> Take a look at any given train\'s schedule using the train number\n```sh\ntst train 9374\n```\n\n---\n\n### ❖ What\'s New? \n0.2.4 - Naming changes\n\n---\n\n<div align="center">\n\n   <img src="https://img.shields.io/static/v1.svg?label=License&message=MIT&color=F5E0DC&labelColor=302D41&style=for-the-badge">\n\n</div>\n\n',
    'author': 'dotzenith',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
