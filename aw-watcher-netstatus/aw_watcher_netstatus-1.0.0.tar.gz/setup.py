# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aw_watcher_netstatus']

package_data = \
{'': ['*']}

install_requires = \
['aw-client>=0.5.11,<0.6.0', 'aw-core>=0.5.11,<0.6.0']

entry_points = \
{'console_scripts': ['aw-watcher-netstatus = aw_watcher_netstatus:main']}

setup_kwargs = {
    'name': 'aw-watcher-netstatus',
    'version': '1.0.0',
    'description': 'An ActivityWatch monitor for observing the network connection status.',
    'long_description': '# `aw-watcher-netstatus`\n\nAn [ActivityWatch](https://activitywatch.net/) monitor for observing the network connection status.\n\n## Purpose\n\n> On the internet, Wonderland is recursive, with rabbit holes opening up to yet more rabbit holes; you never stop falling.\n>\n> —[Henrik Karlsson](https://escapingflatland.substack.com/p/search-query)\n\nLibrar𝘪𝘦𝘴 of Alexandria, brimming with knowledge, promise, culture; an unrelenting, expanding periphery; innumerable collections of untold riches; a source of wonder and awe—all a single keypress away. It\'s suffocating.\n\n\n# Installation\n\n1. Install the module with `pip`. This will add `aw-watcher-netstatus` to your `$PATH`.\n\n    ```\n    pip install aw-watcher-netstatus\n    ```\n\n2. `aw-qt` can now find the module; to start it by default add `aw-watcher-netstatus` to the `aw-qt.toml` configuration file (find the location [here](https://docs.activitywatch.net/en/latest/directories.html)), e.g.\n    ```\n    $ cat  $AW_DIRECTORY/aw-qt/aw-qt.toml\n\n    [aw-qt]\n    autostart_modules = ["aw-server", "aw-watcher-afk", "aw-watcher-window", "aw-watcher-netstatus"]\n    ```\n\n# Development\n\n1. Prerequisites: Clone the repository. Install [Poetry](https://python-poetry.org/).\n2. Run `poetry install` in the root of the directory. \n3. Start the ActivityWatch server in development mode:\n\n    ```\n    $ AW_PATH/aw-server --testing --verbose\n    ```\n\n4. Run `aw-watcher-netstatus` in development mode, this will connect to `localhost:8080` by default.\n\n    ```\n    $ poetry run aw-watcher-netstatus --testing -v\n    ```\n\n5. Open a socket at that port; observe the logs produced by `aw-watcher-netstatus`, view the timeline at `localhost:5666`.\n\n    ```\n    nc -l -k 8080\n    ```\n\n\n',
    'author': 'Sameer Ismail',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sameersismail/aw-watcher-netstatus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
