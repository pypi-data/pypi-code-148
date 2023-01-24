# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tootlogger']

package_data = \
{'': ['*'], 'tootlogger': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'html2text>=2020.1.16,<2021.0.0',
 'mastodon.py>=1.6,<2.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['tootlogger = tootlogger.cli:main']}

setup_kwargs = {
    'name': 'tootlogger',
    'version': '0.4.4',
    'description': 'Log your Mastodon toots to DayOne',
    'long_description': '# tootlogger\n\n## Journal your toots to DayOne\n\nTake all your toots and make a [DayOne](https://dayoneapp.com/) journal entry.\n\nThis saves the last seen toot id so subsequent runs will only show all the toots since then.\nIf you miss a day of running this it, it will back fill up to the pagination limit.\n\n## Install\n\n1. Ensure you have at least Python 3.7 on your Mac\n    - [homebrew](https://brew.sh/) makes this easy with `brew install python`\n1. Install the [DayOne Command Line Interface](http://help.dayoneapp.com/tips-and-tutorials/command-line-interface-cli)\n1. Install tootlogger with `python3 -m pip install tootlogger`\n\n## Setup\n\nYou will need to manually generate your access token and create a config file\n\n1. Log into your mastodon instance\n1. go to `/settings/applications` and create the new app\n    - `read` is the only checkbox needed\n1. Note down the `access_token`\n1. Repeat this for all accounts you want to log\n1. Create a config file like the example below (or in this repo) in one of two places\n    1. `$HOME/.tootlogger.toml`\n    1. `tootlogger.toml` in the local directory you run the command from\n\n### Config file\n\n```toml\n["account_name"]\ninstance = "https://mastodon.social"\naccess_token = "really big string"\n["cool account @ hachyderm.io"]\ninstance = "https://hachyderm.io"\naccess_token = "different big string"\n```\n\n## Usage\n\n1. run `tootlogger` to log all of your toots to DayOne\n1. Set up `tootlogger` to run daily or whenever you toot enough\n',
    'author': 'Amelia Aronsohn',
    'author_email': 'squirrel@wearing.black',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/onlyhavecans/tootlogger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
