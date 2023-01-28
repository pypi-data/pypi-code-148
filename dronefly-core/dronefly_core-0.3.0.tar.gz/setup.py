# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['core',
 'core.clients',
 'core.commands',
 'core.formatters',
 'core.models',
 'core.parsers',
 'core.query',
 'core.utils']

package_data = \
{'': ['*']}

install_requires = \
['dateparser>=1.1.1,<2.0.0',
 'inflect>=5.3.0,<6.0.0',
 'pyinaturalist>=0.17.0,<0.18.0',
 'rich>=10.9,<14']

setup_kwargs = {
    'name': 'dronefly-core',
    'version': '0.3.0',
    'description': 'Core dronefly components',
    'long_description': "[![Red cogs](https://img.shields.io/badge/Red--DiscordBot-cogs-red.svg)](https://github.com/Cog-Creators/Red-DiscordBot/tree/V3/develop)\n[![discord.py](https://img.shields.io/badge/discord-py-blue.svg)](https://github.com/Rapptz/discord.py)\n[![ReadTheDocs](https://img.shields.io/readthedocs/dronefly/latest?label=documentation)](https://dronefly.readthedocs.io)\n\n# Dronefly core\n\nThis branch contains an incomplete rewrite of Dronefly bot's core components,\nand as such is not yet suitable for production use. Please use dronefly's main\nbranch instead, which includes the stable version of Dronefly core.\n\n# Dronefly bot\n\nDronefly is a bot for naturalists that gives users access to\n[iNaturalist](https://www.inaturalist.org) on [Discord](https://discord.com)\nchat.\n\n",
    'author': 'Ben Armstrong',
    'author_email': 'synrg@debian.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.10',
}


setup(**setup_kwargs)
