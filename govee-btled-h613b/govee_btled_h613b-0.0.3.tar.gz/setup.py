# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['govee_btled_H613B']

package_data = \
{'': ['*']}

install_requires = \
['async-timeout>=4.0.1',
 'bleak-retry-connector>=2.3.0',
 'bleak>=0.19.0',
 'colour>=0.1.5']

setup_kwargs = {
    'name': 'govee-btled-h613b',
    'version': '0.0.3',
    'description': 'Control Govee LED BLE device H613B',
    'long_description': '# LED BLE\n\nControl Govee LED BLE device H613B\n\n## Installation\n\nInstall this via pip (or your favourite package manager):\n\n`pip install govee-btled-H613B`\n',
    'author': 'gilcu3',
    'author_email': 'gilcu3@github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gilcu3/govee-btled-H613B',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
