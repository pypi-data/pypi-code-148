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
    'version': '0.0.8',
    'description': 'API and terminal-based CLI for Raindrop.io bookmark manager',
    'long_description': '#+options: toc:nil ^:nil\n#+attr_html: :style width: 100px\n#+toc: headlines 2\n\n#+begin_export html\n<div align="center">\n  <a href="https://choosealicense.com/licenses/mit/">\n    <img alt="MIT License"\n         src="https://img.shields.io/badge/License-MIT-green.svg" />\n  </a>\n\n  <a href="https://www.python.org/">\n    <img alt="Python Version"\n         src="https://img.shields.io/badge/python-3.10+-green" />\n  </a>\n\n  <a href="https://github.com/pre-commit/pre-commit">\n    <img alt="pre-commit"\n       src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit" />\n  </a>\n</div>\n#+end_export\n\n* Raindrop-IO-py\n  Python wrapper for the API to the [[https://raindrop.io][Raindrop.io]] Bookmark Manager as well as a simple command-line interface to perform common operations.\n** Background\n   I wanted to use an existing API for the Raindrop Bookmark Manager ([[https://github.com/atsuoishimoto/python-raindropio][python-raindropio]]) to perform some bulk operations through a simple command-line interface. However, the API available was incomplete and didn\'t contain any interface. Thus, this is a _fork_ and significant extension of [[https://github.com/atsuoishimoto/python-raindropio][python-raindropio]] (thanks [[https://github.com/atsuoishimoto][Atsuo Ishimoto]]!).\n\n   This package includes:\n   - An API providing access to the Raindrop environment (for instance, create, update, delete link/file-based Raindrops; create, update delete Raindrop collections, tags etc.\n   - A terminal-based user-interface that both tests the API as well as providing (me) a fast, simple interface to my Raindrop collections.\n** Status\n   As the API layer is based on a fork of an existing package, it\'s reasonably stable. However, the command-line interface (CLI) is brand new (and lacking tests, ie. "works for me!" ;-).\n** Requirements\n   Requires Python 3.10 or later (well, at least I\'m developing against 3.10.9).\n** Install\n #+BEGIN_SRC shell\n [.venv] python -m pip install raindrop-io-py\n #+END_SRC\n** Setup\n    To use this package, besides your own account on [[https://raindrop.io][Raindrop]], you\'ll need to create an ~integration app~ on the Raindrop.io site from which you can create API token(s).\n\n    - Go to [[https://app.raindrop.io/settings/integrations][https://app.draindrop.api/settings/integrations]] and select ~+ create new app~.\n\n    - Give it a descriptive name and then select the app you just created.\n\n    - Select ~Create test token~ and copy the token provided. Note that the basis for calling it a "test" token is that it only gives you access to bookmarks within _your own account_. Raindrop allows you to use their API against other people\'s environments using oAuth (see untested/unsupported flask_oauth file in /examples)\n\n    - Save your token into your environment (we use python-dotenv so a simple .env/.envrc file containing your token should suffice), for example:\n\n #+BEGIN_SRC shell\n   # If you use direnv or it\'s equivalent, place something like this in a .env file:\n   RAINDROP_TOKEN=01234567890-abcdefghf-aSample-API-Token-01234567890-abcdefghf\n\n   # Or for bash:\n   export RAINDROP_TOKEN=01234567890-abcdefghf-aSample-API-Token-01234567890-abcdefghf\n\n   # Or for fish:\n   set -gx RAINDROP_TOKEN 01234567890-abcdefghf-aSample-API-Token-01234567890-abcdefghf\n\n   # etc...\n #+END_SRC\n** API Usage & Examples\n   A full suite of examples are provided in the `examples` directory, here are a few to give you some idea of the usage model:\n*** Create a New Raindrop Bookmark to a URL\n#+BEGIN_SRC python\n  import os\n  import sys\n\n  from dotenv import load_dotenv\n\n  from raindropiopy.api import API, Raindrop\n\n  load_dotenv()\n\n  with API(os.environ["RAINDROP_TOKEN"]) as api:\n      link, title = "https://www.python.org/", "Our Benevolent Dictator\'s Creation"\n      print(f"Creating Raindrop to: \'{link}\' with title: \'{title}\'...", flush=True, end="")\n      raindrop = Raindrop.create_link(api, link=link, title=title, tags=["abc", "def"])\n      print(f"Done, id={raindrop.id}")\n\n#+END_SRC\n    (after this has executed, go to your Raindrop.io environment (site or app) and you should see this Raindrop to python.org available)\n*** Create a New Raindrop Collection\n#+BEGIN_SRC python\n  import os\n  import sys\n  from datetime import datetime\n  from getpass import getuser\n\n  from dotenv import load_dotenv\n\n  from raindropiopy.api import API, Collection\n\n  load_dotenv()\n\n  with API(os.environ["RAINDROP_TOKEN"]) as api:\n      title = f"TEST Collection ({getuser()}@{datetime.now():%Y-%m-%dT%H:%M:%S})"\n      print(f"Creating collection: \'{title}\'...", flush=True, end="")\n      collection = Collection.create(api, title=title)\n      print(f"Done, {collection.id=}.")\n#+END_SRC\n    (after this has executed, go to your Raindrop.io environment (site or app) and you should see this collection available)\n*** Display All Bookmarks from the *Unsorted* Raindrop Collection\n#+BEGIN_SRC python\n  import os\n  from dotenv import load_dotenv\n\n  from raindropiopy.api import API, CollectionRef, Raindrop\n\n  load_dotenv()\n\n  with API(os.environ["RAINDROP_TOKEN"]) as api:\n      page = 0\n      while (items := Raindrop.search(api, collection=CollectionRef.Unsorted, page=page)):\n          for item in items:\n              print(item.title)\n          page += 1\n#+END_SRC\n** Command-Line Interface Usage\n #+BEGIN_SRC shell\n   [.venv] % raindropiopy\n #+END_SRC\n Note: remember to setup RAINDROP_TOKEN in your environment!\n** Acknowledgments\n   - [[https://github.com/atsuoishimoto/python-raindropio][python-raindropio]] from [[https://github.com/atsuoishimoto][Atsuo Ishimoto]].\n** License\n   The project is licensed under the MIT License.\n** Release History\n*** Unreleased\n*** v0.0.8 - 2023-01-25\n    - CHANGED: Added simple version method in root package (~from raindropiopy import version;print(version())~)\n*** v0.0.7 - 2023-01-25\n    - CHANGED: Added simple version method in root package (~from raindropiopy import version;print(version())~)\n    - CHANGED: Moved from keeping README in markdown to org file format. Incorporated package\'s ChangeLog into README as well (at the bottom).\n    - CHANGED: Added new manage.py release automation capability (internal only, nothing public-facing).\n*** v0.0.6 - 2023-01-22\n    - FIXED: CLI autocomplete now works again after adding support for "single-letter" command-shortcuts.\n    - ADDED: A set of missing attributes to the Raindrop API model type, eg. file, cache etc. Only attribute still missing is `highlights`.\n*** v0.0.5 - 2023-01-21\n    - ADDED: Support use of [[https://github.com/jendrikseipp/vulture][Vulture]] for dead-code analysis (not in pre-commit through due to conflict with ruff\'s McCabe complexity metric)\n    - CHANGED: Moved internal module name to match that of package name. Since we couldn\'t use raindroppy as a package name on PyPI due to similarities with existing packages (one of which was for a *crypto* package), we renamed this package to raindrop-io-py. In concert, the internal module is now ~raindropiopy~:\n #+BEGIN_SRC python\n   from raindroiopy.api import API\n #+END_SRC\n    - FIXED: Sample file upload specification in examples/create_raindrop_file.py is now correct.\n',
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
