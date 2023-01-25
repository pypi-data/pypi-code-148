# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysupladevice']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pysupladevice',
    'version': '0.1.3',
    'description': '',
    'long_description': 'Python SUPLA device library\n===========================\n\nA python library allowing you to write a script that acts as a SUPLA device, such as a sensor or a\nlight switch.\n\nCurrently supports the following kinds of channel:\n * Relay/switch\n * Temperature sensor\n * Humidity sensor\n\nNote: I am not affiliated with SUPLA or Zamel -- this is not an "official" library.\n',
    'author': 'djungelorm',
    'author_email': 'djungelorm@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
