# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['backup_podcasts']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.7.1,<0.8.0',
 'feedparser>=6.0.10,<7.0.0',
 'fire>=0.5.0,<0.6.0',
 'parfive>=2.0.2,<3.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'backup-podcasts',
    'version': '0.1.0',
    'description': 'Backup/archive all episodes of your podcast subscriptions locally.',
    'long_description': 'None',
    'author': 'DreamFlasher',
    'author_email': '31695+dreamflasher@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
