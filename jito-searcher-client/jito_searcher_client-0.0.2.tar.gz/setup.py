# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['searcher', 'searcher.generated']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'grpcio>=1.51.1,<2.0.0',
 'protobuf>=4.21.12,<5.0.0',
 'solana>=0.29.0,<0.30.0',
 'solders>=0.14.2,<0.15.0']

setup_kwargs = {
    'name': 'jito-searcher-client',
    'version': '0.0.2',
    'description': 'Jito Labs Python Searcher Client',
    'long_description': "# About\nThis library contains tooling to interact with Jito Lab's Block Engine as a searcher.\n\n# Tooling\n\nInstall pip\n```bash\n$ curl -sSL https://bootstrap.pypa.io/get-pip.py | python 3 -\n```\n\nInstall poetry\n```bash\n$ curl -sSL https://install.python-poetry.org | python3 -\n```\n\nSetup environment and build protobufs\n```bash\n$ poetry install\n$ poetry protoc\n$ poetry shell\n```\n\nPublishing package\n```bash\n$ poetry protoc\n$ poetry build\n$ poetry publish\n```\n",
    'author': 'Jito Labs',
    'author_email': 'support@jito.wtf',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
