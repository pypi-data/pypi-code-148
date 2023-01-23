# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynasty_dl']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'requests', 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['dynasty-dl = dynasty_dl.__main__:main']}

setup_kwargs = {
    'name': 'dynasty-dl',
    'version': '0.1.0',
    'description': 'Download manga from dynasty-scans.com.',
    'long_description': '# dynasty-dl\nDownload manga from dynasty-scans.com. Written in Python.\n',
    'author': 'Temujin Lampasa',
    'author_email': 'temujinlampasa@gmail.com',
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
