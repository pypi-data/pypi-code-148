# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mpbroker', 'mpbroker.config', 'mpbroker.models']

package_data = \
{'': ['*'], 'mpbroker': ['example/*']}

install_requires = \
['natsort==8.2.0',
 'pycouchdb==1.14.2',
 'pydantic==1.10.4',
 'pymediainfo==6.0.1',
 'requests==2.28.2',
 'rich==12.6.0',
 'tomli==2.0.1',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['mpb = mpbroker.main:app']}

setup_kwargs = {
    'name': 'mpbroker',
    'version': '0.14.0',
    'description': 'Media Player Broker',
    'long_description': "# README\n\nMedia Player Broker (mpb) is an application that helps you play and track media you have watched over disparet locations. mpb keeps track of what you have played at Location A so when you are at Location B you can see what you have watched from either location to avoid digging through history command output over SSH.\n\nmpb is not a player itself but it can be configured to launch your player of choice to view media.\n\n\n### New\n\n- upgrade packages (typer, pycouchdb, pydantic, rich, pymediainfo, natsort)\n- added `--no-confirm` flag to ingest to enable running ingest via cron/scheduled jobs\n\n\n### NOTICE\n\n- BREAKING: version 0.14.0 corrected the spelling error (injest ─⏵ ingest) which requires a change to your `user_config.toml` file (change `[injest]` to `[ingest]`)\n- this app uses tomli for toml parsing, python 3.11 has tomllib included which we will move to at some point in the near future. We realize this could be a large burden on users so we have delayed this task until python 3.11 is more widely used.\n\n\n### The Need\n\nRather than living in the cloud I have my videos duplicated at various locations. I needed something that remembers what episode of MacGyver I had watched in one location so when I was in another location I could continue watching the next episode without digging through `history` output or keeping track of what was played where.\n\nmpb consists of a CLI application (the client) and a database (couchdb). From the client you `ingest` your media metadata. This extracts the file names from file paths and stores the data in the database. After ingesting, you can `list` your media which shows you the media Item, whether it has been watched or not along with a Rating, Notes, and the Sources the item is available at. You can then use the `play` command along with the Item to watch the Item. After playback is completed you are prompted to mark the item as played/watched, Rate it and add Notes - all of which are used in the `list` command to show what you have already watched and what is new.\n\nmpb can also be used by multiple 'users' - you can share a 'user' so your wife can see what you have watched or you can keep separate users so your wife sees what she has watched and you know what you have watched.\n\n\n### Install\n\nWe recommend using [pipx](https://github.com/pypa/pipx) to install mpbroker: `pipx install mpbroker`. You can also install via pip: `pip install --user mpbroker`.\n\nmpbroker uses a config file to store your setup. This file contains information such as your media player, the database url, and types of data to ingest. You can grab the sample config file from  [mpbroker/example/user_config.toml](https://gitlab.com/drad/mpbroker/-/blob/master/mpbroker/example/user_config.toml) and place it in a config location. mpbroker searches the following locations for the config file (in order of precedence):\n\n- $MPB_CONFIG_HOME: set this environment variable to any path you like and place the mpbroker `user_config.toml` file in this location\n- $XDG_CONFIG_HOME/mpbroker\n- $APPDATA/mpbroker\n- $HOME/.config/mpbroker\n\n\n### Configure\n\n#### Notices\n\n- an example `user_config.toml` file can be found in the [project example directory](https://gitlab.com/drad/mpbroker/-/tree/master/mpbroker/example)\n- if you do not want to use the standard locations and do not want to set a `MPB_CONFIG_HOME` envvar you can set `MPB_CONFIG_HOME` on the command line before calling mpb such as `MPB_CONFIG_HOME=/opt/tmp mpb list 'The_Matrix'`\n\nTo set up MPB you need to:\n- create your `user_config.toml` file (see above for locations of this file)\n- configure your user_config.toml file (at a minimum you will need to set/change the `database.db_uri` value)\n- ensure your mpb database is available\n  + use the `db-init` command to initialize your db if it is a new instance!\n\nIf you are testing mpb or do not have a database you can use docker-compose to start a local database with `docker-compose up` from the [project's docker-compose.yml file](https://gitlab.com/drad/mpbroker). If you use the local database your `database.db_uri` would be: `http://localhost:5984` (add your username and password if needed).\n\n\n### Using MPB\n\nmpb has built in help (`mpb --help`) which should give you enough info to get going.\n\nA Quick Start:\n\n- you will likely want to `ingest` some media\n- next you can use `list` to view/find an item to play\n- finally you can `play` an item\n\n#### Paging Output\n\nmpb has pager support, to enable it set the 'use_pager' config option in the user_config.toml file. By default this is not enabled as most pagers drop color support. If you would like pager support and want color to remain in the output you can set the following in your `~/.bashrc` (or equivalent) file:\n\n```\nexport LESS='--quit-if-one-screen --ignore-case --status-column --LONG-PROMPT --RAW-CONTROL-CHARS --HILITE-UNREAD --tabs=4 --no-init --window=-4'\n```\n\nTip: using a pager allows showing one 'page' (screen) of results at a time; however, most pagers (less) also allow searching within the results easily and quickly. We recommend setting the `--RAW-CONTROL-CHARS` and using `less` with mpbroker.\n\n\n### Ingestion\n\nIngestion is the process of loading media metadata into your mpbroker database.\n\n#### Extract Metadata\n\nExtracting metadata on ingestion increases the ingestion time but adds the following data to each ingested media item:\n\n    file_size: # filesize in human readable format (569 MiB, 1.1 GiB)\n    file_type: # file type (video/H265)\n    file_format: # file format (Matroska)\n    encoding: # encoding (x265)\n    duration: # duration in human readable format (1 h 52 min, 2 h 48 min)\n    resolution: # resulution in width x height format (720 x 480)\n    aspect_ratio: # display aspect ratio (16:9)\n    audio_format:  audio format (AAC)\n    audio_sampling: audio sample rate (48000)\n\nTo extract metadata you will need to install [MediaInfo](https://mediaarea.net/en/MediaInfo) which should be available in the repo of most distributions:\n\n- arch: `mediainfo`\n- debian: `mediainfo`\n\n#### Ingestion Time Details\n\n- ~500 videos\n    + with metadata extraction: 6.05s\n    + without metadata extraction: 99.05s\n- 2785 videos\n    + with metadata extraction: 596.53s\n    + without metadata extraction: 72.75s\n",
    'author': 'drad',
    'author_email': 'sa@adercon.com',
    'maintainer': 'drad',
    'maintainer_email': 'sa@adercon.com',
    'url': 'https://gitlab.com/drad/mpbroker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
