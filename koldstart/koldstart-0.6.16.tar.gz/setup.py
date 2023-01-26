# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['koldstart', 'koldstart.auth']

package_data = \
{'': ['*']}

install_requires = \
['auth0-python>=3.24.0,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'dill==0.3.5.1',
 'grpcio>=1.50.0,<2.0.0',
 'isolate-proto>=0.0.15,<0.0.16',
 'isolate==0.9.1',
 'requests>=2.28.1,<3.0.0',
 'typing-extensions==4.4']

entry_points = \
{'console_scripts': ['koldstart = koldstart.cli:cli']}

setup_kwargs = {
    'name': 'koldstart',
    'version': '0.6.16',
    'description': 'koldstart is an easy-to-use Serverless Python Framework',
    'long_description': '',
    'author': 'Features & Labels',
    'author_email': 'hello@fal.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
