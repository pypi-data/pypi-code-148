# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camply',
 'camply.config',
 'camply.containers',
 'camply.notifications',
 'camply.providers',
 'camply.providers.going_to_camp',
 'camply.providers.recreation_dot_gov',
 'camply.providers.xanterra',
 'camply.search',
 'camply.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1,<7.0',
 'click>=8.0.1',
 'pandas>=1.3,<1.4',
 'pydantic>=1.2,<2.0',
 'python-dotenv>=0.10.4',
 'pytz>=2019.1',
 'requests>=2.26.0',
 'rich>=10.0.0',
 'tenacity>=5.1.0']

extras_require = \
{'all': ['twilio>=7.14.0'], 'twilio': ['twilio>=7.14.0']}

entry_points = \
{'console_scripts': ['camply = camply.cli:cli']}

setup_kwargs = {
    'name': 'camply',
    'version': '0.9.0',
    'description': 'camply, the campsite finder 🏕',
    'long_description': '<div align="center">\n<a href="https://github.com/juftin/camply">\n  <img src="https://raw.githubusercontent.com/juftin/camply/main/docs/_static/camply.svg"\n    width="400" height="400" alt="camply">\n</a>\n</div>\n\n`camply`, the campsite finder ⛺️, is a tool to help you book a campground online. Finding\nreservations at sold out campgrounds can be tough. That\'s where camply comes in. It searches the\nAPIs of booking services like https://recreation.gov (which indexes thousands of campgrounds across\nthe USA) to continuously check for cancellations and availabilities to pop up. Once a campsite\nbecomes available, camply sends you a notification to book your spot!\n\n___________\n___________\n\n[![PyPI](https://img.shields.io/pypi/v/camply?color=blue&label=⛺️camply)](https://github.com/juftin/camply)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/camply)](https://pypi.python.org/pypi/camply/)\n[![Docker Image Version](https://img.shields.io/docker/v/juftin/camply?color=blue&label=docker&logo=docker)](https://hub.docker.com/r/juftin/camply)\n[![Testing Status](https://github.com/juftin/camply/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/juftin/camply/actions/workflows/tests.yaml)\n[![GitHub License](https://img.shields.io/github/license/juftin/camply?color=blue&label=License)](https://github.com/juftin/camply/blob/main/LICENSE)\n[![Black Codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)]()\n[![Discord Chat](https://img.shields.io/static/v1?label=chat&message=discord&color=blue&logo=discord)](https://discord.gg/qZDr78kKvB)\n[![Gitmoji](https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg)](https://gitmoji.dev)\n\n## [Check Out The Docs](https://juftin.com/camply/)\n\n## Installing\n\nInstall camply via pip:\n\n```\npip install camply\n```\n\n## Documentation\n\nHead over to the [camply documentation](https://juftin.com/camply/) to see what you can do!\n\n```commandline\ncamply --help\n\nUsage: camply [OPTIONS] COMMAND [ARGS]...\n\n  Welcome to camply, the campsite finder.\n\n  Finding reservations at sold out campgrounds can be tough. That\'s where\n  camply comes in. It searches the APIs of booking services like\n  https://recreation.gov (which indexes thousands of campgrounds across the\n  USA) to continuously check for cancellations and availabilities to pop up.\n  Once a campsite becomes available, camply sends you a notification to book\n  your spot!\n\n  visit the camply documentation at https://github.com/juftin/camply\n\nOptions:\n  --version             Show the version and exit.\n  --provider TEXT       Camping Search Provider. Options available are\n                        \'Yellowstone\' and \'RecreationDotGov\'. Defaults to\n                        \'RecreationDotGov\', not case-sensitive.\n  --debug / --no-debug  Enable extra debugging output\n  --help                Show this message and exit.\n\nCommands:\n  campgrounds       Search for Campgrounds (inside of Recreation Areas)...\n  campsites         Find available Campsites using search criteria\n  configure         Set up camply configuration file with an interactive...\n  recreation-areas  Search for Recreation Areas and list them\n```\n\n## Contributing\n\nCamply doesn\'t support your favorite campsite booking provider yet? Consider\n[contributing](https://juftin.com/camply/contributing/) 😉.\n\n\n## Table of Contents\n\n- [Installation](docs/installation.md)\n    * [PyPI](docs/installation.md#pypi)\n    * [Docker](docs/installation.md#docker)\n- [Providers](docs/providers.md)\n    * [RecreationDotGov](docs/providers.md#recreationgov)\n    * [Yellowstone](docs/providers.md#yellowstone)\n    * [GoingToCamp](docs/providers.md#goingtocamp)\n    * [RecDotGov Tours + Tickets + Timed Entry](docs/providers.md#recreationgov-tickets-tours--timed-entry)\n- [Command Line Usage](docs/command_line_usage.md)\n    * [campsites](docs/command_line_usage.md#campsites)\n    * [recreation-areas](docs/command_line_usage.md#recreation-areas)\n    * [campgrounds](docs/command_line_usage.md#campgrounds)\n    * [configure](docs/command_line_usage.md#configure)\n    * [Examples](docs/command_line_usage.md#examples)\n        + [Searching for a Campsite](docs/command_line_usage.md#searching-for-a-campsite)\n        + [Searching for a Campsite by Campground ID](docs/command_line_usage.md#searching-for-a-campsite-by-campground-id)\n        + [Searching for a Specific Campsite by ID](docs/command_line_usage.md#searching-for-a-specific-campsite-by-id)\n        + [Continuously Searching for A Campsite](docs/command_line_usage.md#continuously-searching-for-a-campsite)\n        + [Continue Looking After The First Match Is Found](docs/command_line_usage.md#continue-looking-after-the-first-match-is-found)\n        + [Send a Push Notification](docs/command_line_usage.md#send-a-push-notification)\n        + [Send a Text Message](docs/command_line_usage.md#send-a-text-message)\n        + [Send a Notification to Different Services](docs/command_line_usage.md#send-a-notification-to-different-services)\n        + [Look for Weekend Campsite Availabilities](docs/command_line_usage.md#look-for-weekend-campsite-availabilities)\n        + [Look for Consecutive Nights at the Same Campsite](docs/command_line_usage.md#look-for-consecutive-nights-at-the-same-campsite)\n        + [Look for a Campsite Inside of Yellowstone](docs/command_line_usage.md#look-for-a-campsite-inside-of-yellowstone)\n        + [Look for a Campsite from GoingToCamp](docs/command_line_usage.md#look-for-a-campsite-from-goingtocamp)\n        + [Searching GoingToCamp Using Equipment](docs/command_line_usage.md#searching-goingtocamp-using-equipment)\n        + [Look for a Campsite Across Multiple Recreation areas](docs/command_line_usage.md#look-for-a-campsite-across-multiple-recreation-areas)\n        + [Using a YAML Configuration file to search for campsites](docs/command_line_usage.md#using-a-yaml-configuration-file-to-search-for-campsites)\n        + [Searching for a Campsite That Fits Your Equipment](docs/command_line_usage.md#searching-for-a-campsite-that-fits-your-equipment)\n        + [Saving the Results of a Search](docs/command_line_usage.md#saving-the-results-of-a-search)\n        + [Search for Recreation Areas by Query String](docs/command_line_usage.md#search-for-recreation-areas-by-query-string)\n        + [Look for Specific Campgrounds Within a Recreation Area](docs/command_line_usage.md#look-for-specific-campgrounds-within-a-recreation-area)\n        + [Look for Specific Campgrounds by Query String](docs/command_line_usage.md#look-for-specific-campgrounds-by-query-string)\n        + [Searching for Tickets and Timed Entries](docs/ccommand_line_usage.md#searching-for-tickets-and-timed-entries)\n            - [Tickets + Tours](docs/ccommand_line_usage.md#tickets-tours)\n            - [Timed Entry](docs/ccommand_line_usage.md#timed-entry)\n            - [Using the Daily Providers](command_line_usage.md#using-the-daily-providers)\n- [Finding Recreation Areas IDs and Campground IDs To Search Without Using the Command Line](docs/command_line_usage.md#finding-recreation-areas-ids-and-campground-ids-to-search-without-using-the-command-line)\n- [Object-Oriented Usage (Python)](docs/python.md)\n    * [Search for a Recreation.gov Campsite](docs/python.md#search-for-a-recreationgov-campsite)\n    * [Continuously Search for Recreation.gov Campsites](docs/python.md#continuously-search-for-recreationgov-campsites)\n- [Running in Docker](docs/docker.md)\n- [Dependencies](docs/dependencies.md)\n- [Contributing](docs/contributing.md)\n\n<br/>\n\nRecreation data provided by [**Recreation.gov**](https://ridb.recreation.gov/)\n\n___________\n___________\n\n<br/>\n\n[<p align="center" ><img src="https://raw.githubusercontent.com/juftin/juftin/main/static/juftin.png" width="120" height="120"  alt="juftin logo"> </p>](https://github.com/juftin)\n',
    'author': 'Justin Flannery',
    'author_email': 'juftin@juftin.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/juftin/camply',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
