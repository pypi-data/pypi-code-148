# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slack_wlan_status_updater']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['slack-wlan-status-updater = '
                     'slack_wlan_status_updater.__main__:main']}

setup_kwargs = {
    'name': 'slack-wlan-status-updater',
    'version': '0.1.0',
    'description': 'Update Slack status based on WLAN network',
    'long_description': None,
    'author': 'Martin Ueding',
    'author_email': 'mu@martin-ueding.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
