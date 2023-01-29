# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['local_tuya',
 'local_tuya.device',
 'local_tuya.domoticz',
 'local_tuya.domoticz.plugin',
 'local_tuya.domoticz.units',
 'local_tuya.protocol',
 'local_tuya.protocol.message',
 'local_tuya.protocol.message.handlers']

package_data = \
{'': ['*']}

install_requires = \
['concurrent-tasks>=1,<2', 'pycryptodomex>=3,<4', 'xmltodict>=0.13,<0.14']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=4,<5']}

setup_kwargs = {
    'name': 'local-tuya',
    'version': '0.1.0',
    'description': 'Interface to Tuya devices over LAN.',
    'long_description': '# local-tuya\nInterface to Tuya devices over LAN.\n',
    'author': 'Gabriel Pajot',
    'author_email': 'gab@les-cactus.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gpajot/local-tuya',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
