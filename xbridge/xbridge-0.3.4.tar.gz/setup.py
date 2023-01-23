# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xbridge']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'cryptography>=37.0.2,<38.0.0',
 'progress>=1.6,<2.0',
 'pyOpenSSL>=22.0.0,<23.0.0',
 'pycryptodome>=3.14.1,<4.0.0',
 'qrcode>=7.3.1,<8.0.0',
 'rsa>=4.8,<5.0',
 'rsocket>=0.3,<0.4',
 'websockets>=10.3,<11.0',
 'zeroconf>=0.38.5,<0.39.0']

entry_points = \
{'console_scripts': ['xbridge = xbridge.__main__:main']}

setup_kwargs = {
    'name': 'xbridge',
    'version': '0.3.4',
    'description': 'Discoverable service in local networking',
    'long_description': 'None',
    'author': 'yudingp',
    'author_email': 'yudingp@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
