# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ibkrbox']

package_data = \
{'': ['*']}

install_requires = \
['click-log>=0.4.0,<0.5.0',
 'click>=8.1.3,<9.0.0',
 'ib-insync>=0.9.71,<0.10.0',
 'pandas>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['ibkrbox = ibkrbox.cli:cli']}

setup_kwargs = {
    'name': 'ibkrbox',
    'version': '0.4.0',
    'description': 'box spread utility for interactive brokers',
    'long_description': '# ibkrbox\nConstructs a Box Spread combo order for SPX or ES futures option, only required arguments are amount you want to lend or borrow , and for how many months.\n\nThis utility will automatically look up current treasury rates, and add .30 to get the yield rate. This will be used to calculate limit price. rate or limit price can be overridden as needed.\n\nIt can also automatically calculate the right strikes and spread, with approximate expiry for given duration. All of these can be overridden as needed.\n\nThis utility is easy to install and use with existing IBKR TWS or gateway session. Just make sure to enable API access in the GUI of IBKR TWS or gateway.\n\n## Installation\n```code\npip install ibkrbox\n```\n\n## Usage\n\n```code\nibkrbox -h\n```\n<img width="629" alt="image" src="https://user-images.githubusercontent.com/998264/200383898-c9433221-0107-4366-9b06-60179233f5c1.png">\n\n\n### 1. construct a combo SPX Box Spread lending for 50K, duration 4 months, and display ("--show" option ensures it will not be executed)\n```code\nibkrbox -a 50000 -m 4 --show\n```\n<img width="795" alt="image" src="https://user-images.githubusercontent.com/998264/200384213-06b1e995-6cfb-4c68-a022-53385b3e494f.png">\n\n\n### 2. construct a combo SPX Box Spread borrowing for 50K, duration 4 months, and display.\n```code\nibkrbox -a 50000 -m 4 --show --short\n```\n',
    'author': 'asemx',
    'author_email': '998264+asemx@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/asemx/ibkrbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
