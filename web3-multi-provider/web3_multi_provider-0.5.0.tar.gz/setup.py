# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['web3_multi_provider']

package_data = \
{'': ['*']}

install_requires = \
['web3>=5.22.0,<7']

setup_kwargs = {
    'name': 'web3-multi-provider',
    'version': '0.5.0',
    'description': 'Web3py provider that makes it easy to switch between different blockchain nodes to make sure application will be be online if main blockchain node will be unavailable.',
    'long_description': '# <img src="https://docs.lido.fi/img/logo.svg" alt="Lido" width="46"/>\u2003Web3 Multi Provider\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nProvider that switch to other working web3 rpc endpoint if smth is bad with active one.\n\n## Install\n\n```bash\n$ pip install web3-multi-provider\n```  \nor  \n```bash\n$ poetry add web3-multi-provider\n```  \n\n## Usage\n\n```py\nfrom web3 import Web3\nfrom web3_multi_provider import MultiProvider\n\nw3 = Web3(MultiProvider([  # RPC endpoints list\n    \'http://127.0.0.1:8000/\',\n    \'https://mainnet.infura.io/v3/...\',\n    \'wss://mainnet.infura.io/ws/v3/...\',\n]))\n\nlast_block = w3.eth.get_block(\'latest\')\n```\n\n## For developers\n\n1. `poetry install` - to install deps\n2. `pre-commit install` - to install pre-commit hooks\n\n## Tests\n\n```bash\npoetry run pytest tests\n```\n',
    'author': 'Raman',
    'author_email': 'raman.s@lido.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.10,<4',
}


setup(**setup_kwargs)
