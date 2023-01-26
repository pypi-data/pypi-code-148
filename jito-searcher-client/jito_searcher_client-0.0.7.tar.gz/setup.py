# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jito_searcher_client', 'jito_searcher_client.generated']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'grpcio>=1.51.1,<2.0.0',
 'isort>=5.11.4,<6.0.0',
 'protobuf>=4.21.12,<5.0.0',
 'solana>=0.29.0,<0.30.0',
 'solders>=0.14.2,<0.15.0']

setup_kwargs = {
    'name': 'jito-searcher-client',
    'version': '0.0.7',
    'description': 'Jito Labs Python Searcher Client',
    'long_description': '# About\nThis library contains tooling to interact with Jito Lab\'s Block Engine as a searcher.\n\n# Downloading\n```bash\n$ pip install jito_searcher_client\n```\n\n# Keypair Authentication\nPlease request access to the block engine by creating a solana keypair and emailing the public key to support@jito.wtf.\n\n# Examples\n\n```python\nfrom jito_searcher_client import get_searcher_client\nfrom jito_searcher_client.generated.searcher_pb2 import ConnectedLeadersRequest\n\nfrom solders.keypair import Keypair\n\nKEYPAIR_PATH = "/path/to/authenticated/keypair.json"\nBLOCK_ENGINE_URL = "frankfurt.mainnet.block-engine.jito.wtf"\n\nwith open(KEYPAIR_PATH) as kp_path:\n    kp = Keypair.from_json(kp_path.read())\n\nclient = get_searcher_client(BLOCK_ENGINE_URL, kp)\nleaders = client.GetConnectedLeaders(ConnectedLeadersRequest())\nprint(f"{leaders=}")\n```\n\n# Development\n\nInstall pip\n```bash\n$ curl -sSL https://bootstrap.pypa.io/get-pip.py | python 3 -\n```\n\nInstall poetry\n```bash\n$ curl -sSL https://install.python-poetry.org | python3 -\n```\n\nSetup environment and build protobufs\n```bash\n$ poetry install\n$ poetry protoc\n$ poetry shell\n```\n\nPublishing package\n```bash\n$ poetry protoc && poetry build && poetry publish\n```\n',
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
