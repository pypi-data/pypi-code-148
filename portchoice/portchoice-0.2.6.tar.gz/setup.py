# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['portchoice']

package_data = \
{'': ['*']}

install_requires = \
['numdifftools>=0.9.40,<0.10.0', 'pandas>=1.4.2,<2.0.0', 'pyDOE2>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'portchoice',
    'version': '0.2.6',
    'description': 'Modules to design and estimate portfolio choice models',
    'long_description': 'None',
    'author': 'Jose Ignacio Hernandez',
    'author_email': 'j.i.hernandez@tudelft.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
