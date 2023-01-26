# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymolstyles', 'pymolstyles.external']

package_data = \
{'': ['*']}

install_requires = \
['morfeus-ml>=0.7.2,<0.8.0']

setup_kwargs = {
    'name': 'pymolstyles',
    'version': '1.0.1',
    'description': 'Scripts for small molecule visualization using PyMOL',
    'long_description': "!['pymolstyles logo'](./docs/img/pymolstyles.png)\n\n",
    'author': 'Attilio Chiavegatti',
    'author_email': 'attiliochiavegatti@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
