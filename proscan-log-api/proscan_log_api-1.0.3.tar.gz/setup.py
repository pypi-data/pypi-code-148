# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proscan_log_api']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.5,<2.0.0', 'pandas>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'proscan-log-api',
    'version': '1.0.3',
    'description': "Log API for PSI's PROSCAN",
    'long_description': "# log_API - PROSCAN LOG API\n\n#### Table of Contents\n- [Introduction](#introduction)\n- [Installation](#installation)\n- [Quick-start Guid](#quick-start-guide)\n- [Documentation](#documentation)\n- [Dependencies](#dependencies)\n- [Contribute](#contribute)\n- [Project Changes and Tagged Releases](#project-changes-and-tagged-releases)\n- [Developer Notes](#developer-notes)\n- [Contact](#contact)\n\n# Introduction\nThis project/package aims to provide a fully asynchronous client for PSIs REST DataAPI.\n\n# Installation\nInstall with pip\n```bash\npip install proscan_log_api\n```\n# Quick-start Guide\nHere are some simple examples to get you started:\n```python\n\n\n```\n\n\n# Documentation\nCurrent Features:\n* Fully asynchronous\n* 100% Test coverage\n* Search for channels\n* get data as pandas dataframe\n\n\nCheck out the wiki for more info!\n\n# Dependencies\n* [httpx](https://github.com/encode/httpx/)\n* [isodate](https://github.com/gweis/isodate/)\n* [pandas](https://pandas.pydata.org/)\n\n\n# Contribute\nTo contribute, simply clone the project.\nYou can uses ``` pip -r requirements.txt ``` or the Makefile to set up the project.\nAfter that you can make changes and create a pull request or if allowed merge your changes.\n\n\n# Project Changes and Tagged Releases\n* See the Changelog file for further information\n* Project releases are available in pypi (NOT YET)\n\n# Developer Notes\nCurrently None\n\n# Contact\nIf you have any questions pleas contract 'niklas.laufkoetter@psi.ch'\n",
    'author': 'Niklas Laufkoetter',
    'author_email': 'niklas.laufkoetter@psi.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
