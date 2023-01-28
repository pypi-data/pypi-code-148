# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ruuvibot']

package_data = \
{'': ['*'], 'ruuvibot': ['dbdata/*']}

install_requires = \
['pexpect>=4.8.0,<5.0.0',
 'python-telegram-bot>=20.0,<21.0',
 'ruuvitag-sensor>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['ruuvibot = ruuvibot:main']}

setup_kwargs = {
    'name': 'ruuvibot',
    'version': '0.3.1',
    'description': 'Telegram bot to read ruuvitag data and log data to database',
    'long_description': 'None',
    'author': 'Rami Rahikkala',
    'author_email': 'rami.rahikkala@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
