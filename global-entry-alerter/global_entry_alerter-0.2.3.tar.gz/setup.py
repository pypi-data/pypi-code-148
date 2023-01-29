# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['global_entry_alerter',
 'global_entry_alerter.clients',
 'global_entry_alerter.clients.scheduler',
 'global_entry_alerter.clients.twilio']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.12.0,<23.0.0',
 'flake8>=6.0.0,<7.0.0',
 'pre-commit>=3.0.1,<4.0.0',
 'requests>=2.28.2,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'twilio>=7.16.2,<8.0.0']

entry_points = \
{'console_scripts': ['global-entry-alerter = global_entry_alerter:run',
                     'vital-tracker = vital_tracker:run']}

setup_kwargs = {
    'name': 'global-entry-alerter',
    'version': '0.2.3',
    'description': 'A bot that helps you find an open Global Entry interview appointment',
    'long_description': '# Global Entry Alerter\nA bot that helps you find an open Global Entry interview appointment.\n\n[![PyPI version](https://badge.fury.io/py/global-entry-alerter.svg)](https://badge.fury.io/py/global-entry-alerter)\n\n## Problem\nBooking an appointment for a [Global Entry](https://www.cbp.gov/travel/trusted-traveler-programs/global-entry) interview is hard, especially in cities with high demand like SF or NYC. \n\nIf you check for open appointments, there is typically nothing available for weeks, sometimes even months. \nHowever, appointments _are_ actually constantly opening up, they just get booked very quickly.\n\nThis project polls the DHS Scheduler API for open Global Entry appointments, notifying you whenever a new one opens up.\nIf the new appointment is convenient for you, book it immediately — otherwise it will be gone within a few minutes.\n\nThis project is not affiliated with U.S. Customs and Border Protection or the U.S. Department of Homeland Security.\n\n\n### Example Usage\n<img src="https://github.com/grahamplace/global-entry-alerter/blob/main/example.png?raw=true" alt="example of messages sent by bot" width="30%"/>\n\n## Requirements\n1. A Twilio account with the ability to send programmable SMS. See [here](https://www.twilio.com/docs/sms/quickstart/python).\n2. Python 3 & [Poetry](https://python-poetry.org/docs/)\n\n## Usage\nConfigure your settings in a `config.toml`, set env vars, and leave the `global-entry-alerter` running for as long as needed.\n\nOnce the script sends an alert about a particular appointment, it will keep that appointment in memory and won\'t notify you of it again. If you restart the script, it may re-send previously-seen appointments.\n\n### Installation\n```bash\n$ pip install global-entry-alerter\n```\n\n### Running\nTo run the project:\n1. Create your own `config.toml` (see [example_config.toml](https://github.com/grahamplace/global-entry-alerter/blob/main/example_config.toml))\n2. Configure your settings (see Configuration below)\n3. Set the following env variables using your Twilio account:\n   - `TWILIO_AUTH_TOKEN`\n   - `TWILIO_ACCOUNT_SID`\n   - `TWILIO_PHONE_NUMBER`\n4. `global-entry-alerter --config ~/path_to_your/config.toml`\n\n\n### Configuration\nThe project uses a `.toml` configuration file for all settings.\n\nSee [example_config.toml](https://github.com/grahamplace/global-entry-alerter/blob/main/example_config.toml) as a reference for your own `config.toml`\n\n| Setting                  | Description                                                                                                                                                                                                                                                           |                     Example Value |\n|:-------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------:|\n| `fetching.lookahead_weeks` | How many weeks from today to check for open appointments. E.g. if you want an appointment in the next month, use 4 weeks                                                                                                                                              |                                 4 |\n| `fetching.wait_seconds`    | The interval between checks for open appointments. It is best to use a value <= 60                                                                                                                                                                                    |                                10 |\n| `fetching.locations`       | Which Global Entry interview locations to check. Accepts many locations for use cases where multiple locations are feasible (e.g. EWR or JFK if you live in NYC). See [here](https://github.com/oliversong/goes-notifier#goes-center-codes) for the full set of codes | `[{ name = "JFK", code = 5140 }]` |\n| `sending.to_numbers`       | The phone numbers to send alerts to. Include +1 (or whatever country code)                                                                                                                                                                                            |                  `["+11231231234"]` |\n\n\n## Development\n\n### Pre-commit hooks\nThis project uses [pre-commit](https://pre-commit.com) to enforce linting on all commits. Install it with:\n```bash\n$ poetry run pre-commit install\n```\n\n### Formatting\nThis project uses [black](https://github.com/psf/black) and [flake8](https://flake8.pycqa.org/en/latest/) to enforce a consistent style.\nTo format the project according to the rules, run:\n```bash\nmake format\n```\n\n### Test Mode\nRunning in test mode will fetch appointments using the settings in `config.toml`, but will not actually send alerts.\nUse this when developing to avoid incurring Twilio costs:\n```bash\npoetry run global-entry-alerter --test \n```\n\n',
    'author': 'Graham Place',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4',
}


setup(**setup_kwargs)
