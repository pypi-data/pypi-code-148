# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['desuko', 'desuko.modules']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'py-cord>=2.2.2,<3.0.0']

setup_kwargs = {
    'name': 'desuko',
    'version': '0.1.1',
    'description': 'An extensible Discord bot, written in Python & Pycord.',
    'long_description': '<p align="center">\n    <h1 align="center">Desuko</h1>\n    <p align="center">\n        <img src="https://cdn.jsdelivr.net/npm/twemoji@11.3.0/2/svg/26a0.svg" width="20" alt="" valign="top" /> <b>This repository is archived.</b> Please check out <a href="https://docs.pycord.dev/en/stable/ext/tasks/index.html">discord.ext.tasks</a> as a replacement. <img src="https://cdn.jsdelivr.net/npm/twemoji@11.3.0/2/svg/26a0.svg" width="20" alt="" valign="top" />\n    </p>\n    <p align="center">\n        <a href="https://pypi.org/project/desuko-discord/" target="_blank"><img src="https://raster.shields.io/pypi/v/desuko-discord.svg?style=flat&logo=python&logoColor=white" alt="PyPi release" /></a>\n        <a href="https://codeclimate.com/github/arichr/desuko-discord/maintainability"><img src="https://api.codeclimate.com/v1/badges/76f40b543de7e3645163/maintainability" alt="CodeClimate maintainability" /></a>\n        <br />\n        Desuko is an extensible Discord bot, written in Python & Pycord.\n    </p>\n    <p align="center">\n        <a href="https://arichr.github.io/gophient/" target="_blank"><img src="https://raster.shields.io/badge/read-documentation-47b649.svg?style=for-the-badge&logo=python&logoColor=white" alt="Read documentation" /></a>\n    </p>\n</p>\n\n**Features:**\n\n* **Hackable**: Desuko aims to keep the code clean and intuitive.\n* **Extensible**: Desuko can be extended by various modules.\n* **Fully configurable**: Everything can be configured via YAML.\n* **Async-friendly**: Desuko support asyncronious functions out of the box.\n\n## Getting started\n**First steps:**\n\n1. [Installation](https://arichr.github.io/desuko-discord/docs/getting_started/1_Installation/) - Install & run a basic version of Desuko.\n2. [Configuration](https://arichr.github.io/desuko-discord/docs/getting_started/2_Configuration/) - Configurate your Desuko using `desuko.yaml`.\n\n**Modules:**\n\n1. [Hello, Desuko!](https://arichr.github.io/desuko-discord/docs/modules/Development/HelloDesuko/) - "Hello, World!" module for Desuko\n2. [Handlers and subscribers](https://arichr.github.io/desuko-discord/docs/modules/Development/HandlersAndSubs/) - Handlers and subscribers usage for building event-driven bots\n',
    'author': 'Arisu Wonderland',
    'author_email': 'arisuchr@riseup.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/arichr/desuko-discord',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
