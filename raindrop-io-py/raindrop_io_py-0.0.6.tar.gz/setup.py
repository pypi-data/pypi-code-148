# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raindropiopy',
 'raindropiopy.api',
 'raindropiopy.cli',
 'raindropiopy.cli.commands',
 'raindropiopy.cli.models']

package_data = \
{'': ['*']}

install_requires = \
['humanize>=4.4.0,<5.0.0',
 'jashin>=0.0.7,<0.0.8',
 'prompt-toolkit>=3.0.36,<4.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests-oauthlib>=1.3.1,<2.0.0',
 'rich>=13.2.0,<14.0.0',
 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['raindrop-io-py = raindropiopy.cli.cli:main']}

setup_kwargs = {
    'name': 'raindrop-io-py',
    'version': '0.0.6',
    'description': 'API and terminal-based CLI for Raindrop.io bookmark manager',
    'long_description': '\n# Raindrop-io-py\n\n[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)\n[![Python Version](https://img.shields.io/badge/python-3.10+-green)](https://www.python.org/)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)\n\nPython wrapper for the [Raindrop.io](https://raindrop.io) Bookmark Manager as well as a simple command-line interface to perform common operations.\n\n\n## Background & Acknowledgments\n\nI needed a few additions to an existing API for the Raindrop Bookmark Manager and desired a simple terminal-based UI for interactive work with Raindrop itself. Thus, this is a _fork_ of [python-raindropio](https://github.com/atsuoishimoto/python-raindropio) from [Atsuo Ishimoto](https://github.com/atsuoishimoto) ...thanks Atsuo!\n\n\n## Status\n\nAs the API layer is based on a fork of an existing package, it\'s reasonably stable. However, the command-line interface (CLI) is brand new (and lacking tests, ie. "works for me!" ;-).\n\n## Requirements\n\nRequires Python 3.10 or later (well, at least I\'m developing against 3.10.9).\n\n## Install\n\n```shell\n[.venv] python -m pip install raindrop-io-py\n```\n\n## Setup\n\nTo use this package, besides your own account on [Raindrop](https://raindrop.io), you\'ll need to create an _integration app_ on the Raindrop.io site from which you can create API token(s). \n\n- Go to [app.draindrop.api/settings/integrations](https://app.raindrop.io/settings/integrations) and select `+ create new app`.\n\n- Give it a descriptive name and then select the app you just created. \n\n- Select `Create test token` and copy the token provided. Note that the basis for calling it a "test" token is that it only gives you access to bookmarks within _your own account_. Raindrop allows you to use their API against other people\'s environments using oAuth (see untested/unsupported flask_oauth file in /examples)\n\n- Save your token into your environment (we use python-dotenv so a simple .env/.envrc file your information should suffice), for example:\n\n```\n# in a .env file:\nRAINDROP_TOKEN=01234567890-abcdefghf-aSample-API-Token-01234567890-abcdefghf\n\n# Or for bash:\nexport RAINDROP_TOKEN=01234567890-abcdefghf-aSample-API-Token-01234567890-abcdefghf\n\n# Or for fish:\nset -gx RAINDROP_TOKEN 01234567890-abcdefghf-aSample-API-Token-01234567890-abcdefghf\n\n# ...\n```\n\n## API Usage & Examples\n\nA full suite of examples are provided in the `examples` directory, here are a few to give you some idea of the usage model:\n\n### Create a New Raindrop Bookmark to a URL\n\n```python\nimport os\nimport sys\n\nfrom dotenv import load_dotenv\n\nfrom raindropiopy.api import API, Raindrop\n\nload_dotenv()\n\nwith API(os.environ["RAINDROP_TOKEN"]) as api:\n    link, title = "https://www.python.org/", "Our Benevolent Dictator\'s Creation"\n    print(f"Creating Raindrop to: \'{link}\' with title: \'{title}\'...", flush=True, end="")\n    raindrop = Raindrop.create_link(api, link=link, title=title, tags=["abc", "def"])\n    print(f"Done, id={raindrop.id}")\n```\n\n(after this has executed, go to your Raindrop.io environment (site or app) and you should see this Raindrop to python.org available)\n\n### Create a New Raindrop Collection\n\n```python\nimport os\nimport sys\nfrom datetime import datetime\nfrom getpass import getuser\n\nfrom dotenv import load_dotenv\n\nfrom raindropiopy.api import API, Collection\n\nload_dotenv()\n\nwith API(os.environ["RAINDROP_TOKEN"]) as api:\n    title = f"TEST Collection ({getuser()}@{datetime.now():%Y-%m-%dT%H:%M:%S})"\n    print(f"Creating collection: \'{title}\'...", flush=True, end="")\n    collection = Collection.create(api, title=title)\n    print(f"Done, {collection.id=}.")\n```\n\n(after this has executed, go to your Raindrop.io environment (site or app) and you should see this collection available)\n\n### Display All Bookmarks from the *Unsorted* Raindrop Collection\n\n```python\nimport os\nfrom dotenv import load_dotenv\n\nfrom raindropiopy.api import API, CollectionRef, Raindrop\n\nload_dotenv()\n\n\nwith API(os.environ["RAINDROP_TOKEN"]) as api:\n    page = 0\n    while (items := Raindrop.search(api, collection=CollectionRef.Unsorted, page=page)):\n        for item in items:\n            print(item.title)\n        page += 1\n```\n\n## Command-Line Interface Usage\n\n```shell\n[.venv] % raindropiopy\n```\nNote: remember to setup RAINDROP_TOKEN in your environment!\n\n## Acknowledgments\n\n- [python-raindropio](https://github.com/atsuoishimoto/python-raindropio) from [Atsuo Ishimoto](https://github.com/atsuoishimoto).\n\n\n## License\n\nThe project is licensed under the MIT License.\n',
    'author': 'Peter Borocz',
    'author_email': 'peter.borocz+raindrop-io-py@google.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/PBorocz/raindrop-io-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
