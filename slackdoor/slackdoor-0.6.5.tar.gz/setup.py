# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['door',
 'door.models',
 'door.models.files',
 'door.models.messages',
 'door.plugins',
 'door.plugins.commands',
 'door.plugins.examples',
 'door.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiorun>=2022,<2023',
 'case-insensitive-dictionary',
 'python-dotenv>=0,<1',
 'pytz',
 'sentry-sdk>=1,<2',
 'slack-bolt[async]>=1.15.2,<2.0.0',
 'slack-sdk>=3.19.2,<4.0.0']

entry_points = \
{'console_scripts': ['slackdoor = door.run:main']}

setup_kwargs = {
    'name': 'slackdoor',
    'version': '0.6.5',
    'description': 'An opinionated and powerful chatbot framework for Slack',
    'long_description': 'None',
    'author': 'Eddy G',
    'author_email': 'eddyg@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eddyg/slackdoor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
