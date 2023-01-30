# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot',
 'nonebot.adapters.console',
 'nonebot.adapters.console.frontend',
 'nonebot.adapters.console.frontend.components',
 'nonebot.adapters.console.frontend.components.chatroom',
 'nonebot.adapters.console.frontend.components.general',
 'nonebot.adapters.console.frontend.components.log',
 'nonebot.adapters.console.frontend.router',
 'nonebot.adapters.console.frontend.storage',
 'nonebot.adapters.console.frontend.views']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-beta.1,<3.0.0', 'textual>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'nonebot-adapter-console',
    'version': '0.3.1',
    'description': 'console adapter for nonebot2',
    'long_description': '<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" alt="nonebot-adapter-console"></a>\n</p>\n\n<div align="center">\n\n# NoneBot-Adapter-Console\n\n_✨ Console 适配 ✨_\n\n</div>\n',
    'author': 'MelodyKnit',
    'author_email': 'yanximelody@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
