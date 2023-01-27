# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ruuvibot']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ruuvibot',
    'version': '0.1.0',
    'description': 'Telegram bot to read ruuvitag data and log data to database',
    'long_description': 'None',
    'author': 'Rami Rahikkala',
    'author_email': 'rami.rahikkala@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
