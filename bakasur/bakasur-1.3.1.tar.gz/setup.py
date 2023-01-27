# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bakasur']

package_data = \
{'': ['*']}

install_requires = \
['datapane>=0.14.0,<0.15.0',
 'fake-useragent>=1.1.1,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.4.4,<13.0.0',
 'typer[all]>=0.4.2,<0.5.0']

entry_points = \
{'console_scripts': ['bakasur = bakasur.main:app']}

setup_kwargs = {
    'name': 'bakasur',
    'version': '1.3.1',
    'description': 'Bakasur is your friendly demon that helps you analyse your Thuisbezorgd order history and visualise patterns.',
    'long_description': '# Bakasur\n[![PyPI version](https://badge.fury.io/py/bakasur.svg)](https://badge.fury.io/py/bakasur)\n***\n[Bakasur](https://github.com/d-kold/bakasur) (_/buh-KAA-soor/_) is your friendly demon who helps you analyse your Thuisbezorgd order history and visualise it. \n\n![Dashboard](img/dashboard.png)\n\n![Terminal](img/terminal.png)\n\n\n### Disclaimer\n***\nThis tool requires you to log in using your Thuisbezorgd credentials. Upon correct input, you will recieve \na email with a verification code from Thuisbezorgd. Once the details are added, `bakasur` will create a `thuisbezorgd_token.json`\nfile in your current working directory which will store the `authToken` and `refreshToken` received from the login request. \nThese tokens will help in authenticating the Thuisbezorgd API in the subsequent runs of this tool. \nIf you are concerned about the security of the tokens they are on your local filesystem and you can also review\nthe code to check that there are no evil intentions here. **Your username and password are not stored.**\n\n\n### How to use this tool\n***\nThis tool uses a number of packages such as `typer`, `rich`, `datapane`. To avoid any conflicts with your current installed\nsite-packages, it is preferable to create a virtual environment and then install this tool.\n\n- Create a virtual environment `virtualenv venv` and activate it `source venv/bin/activate`\n- Install Bakasur using `pip install bakasur`\n- Once it is installed you can now type in `bakasur` in your terminal and get started\n\n### Tool specifics\n***\nWhen you first log in to Thuisbezorgd using `bakasur` it creates a sqlite database in your current working directory `thuisbezrgd.db`. \nThe database stores all your orders and their details in tables `orders` and `items` respectively. During subsequent runs\nof the tool, your most recent orders are inserted into the database \n\nRequires:\n- Python v3.7.1+ \n- Thuisbezorgd account (duh!)\n\n### Contribution\n***\nGive this tool a try and if you find any bugs or issues with it then feel free to open an issue or start a discussion.\nFeature requests, Bug fixes are most welcome.\n\n### License\n***\n[MIT License](https://github.com/d-kold/bakasur/blob/0d2317c116180b2e33d14e833c25352ff5a8e032/LICENSE.md)\n\n### Important\n***\nThis tool is intended for personal use. A fun hobby project for demo. I am not responsible if you tweak the code and violate \nany Thuisbezorgd Terms and Conditions. \n\n[d-kold](https://github.com/d-kold)',
    'author': 'Devendra Kulkarni',
    'author_email': 'kulkarnidevendra21@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11.0',
}


setup(**setup_kwargs)
