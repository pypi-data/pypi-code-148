# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ampel']

package_data = \
{'': ['*']}

install_requires = \
['ampel-core>=0.8.3,<0.9.0', 'ampel-ipython==0.7']

setup_kwargs = {
    'name': 'ampel',
    'version': '0.8.3a2',
    'description': 'Asynchronous and Modular Platform with Execution Layers',
    'long_description': 'None',
    'author': 'Valery Brinnel',
    'author_email': 'None',
    'maintainer': 'Jakob van Santen',
    'maintainer_email': 'jakob.van.santen@desy.de',
    'url': 'https://ampelproject.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
