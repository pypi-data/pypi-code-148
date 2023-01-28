# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flare_explorer']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'flare-explorer-python',
    'version': '0.1.1',
    'description': 'A lightweight library that works as a connector to the Flare explorer api',
    'long_description': '# Flare explorer python\n<a href="https://pypi.org/project/flare-explorer-python" target="_blank"><img src="https://img.shields.io/pypi/v/flare-explorer-python?color=%2334D058&label=pypi%20package" alt="Package version"></a>\n[![Linting and tests](https://github.com/james-ecd/flare-explorer-python/actions/workflows/tests-and-linting.yml/badge.svg?branch=main)](https://github.com/james-ecd/flare-explorer-python/actions/workflows/tests-and-linting.yml)\n[![codecov](https://codecov.io/gh/james-ecd/flare-explorer-python/branch/main/graph/badge.svg?token=XOBC0UK00V)](https://codecov.io/gh/james-ecd/flare-explorer-python)\n<a href="https://pypi.org/project/flare-explorer-python" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/flare-explorer-python.svg?color=%2334D058" alt="Supported Python versions">\n</a>\n[![Code Style](https://img.shields.io/badge/code_style-black-black)](https://black.readthedocs.io/en/stable/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nA lightweight library that works as a connector to the [Flare explorer api](https://flare-explorer.flare.network/graphiql)\n\nIf you came here looking for the flare network, then go [here](https://flare.network/). If you want to query flares blockchain using python then stick around.\n\n## Installation\nflare-explorer-python is available on PYPI. Install with pip or poetry:\n\n```\npip install flare-explorer-python\n```\n```\npoetry add flare-explorer-python\n```\n\n## Usage\n### Transactions\n``` python\nfrom flare_explorer.transaction import (\n    get_internal_transactions,\n    get_transaction,\n    get_transactions_from_address,\n)\n\ntransaction = get_transaction("transaction_hash")\n\ninternal_transactions, page_info = get_internal_transactions(\n    "transaction_hash",\n    previous_cursor="previous_page_last_cursor"\n)\n\ntransactions, page_info = get_transactions_from_address(\n    "address_hash",\n    previous_cursor="previous_page_last_cursor"\n)\n```\n\n### Addresses\n``` python\nfrom flare_explorer.address import get_address, get_addresses\n\naddress = get_address(\n    "address_hash",\n)\n\naddresses = get_addresses(\n    [\n        "address_hash_1",\n        "address_hash_2",\n    ]\n)\n```\n\n### Blocks\n``` python\nfrom flare_explorer.block import get_block\n\nblock = get_block(4463469)\n```\n\n### Token transfers\n``` python\nfrom flare_explorer.token_transfers import get_token_transfers\n\ntoken_transfers, page_info = get_token_transfers(\n    "token_contract_address_hash",\n    previous_cursor="previous_page_last_cursor"\n)\n```\n\n## Upcoming features\n- asyncio support\n- websocket support\n- fast mode (no pydantic serialization)\n\n## Testing / Contributing\nAny contributions or issue raising is welcomed. If you wish to contribute then:\n1. fork/clone this repo\n2. make changes on a branch taken from main\n3. sumbit a pull request against main\n\nPull requests will be blocked from merging automatically if:\n- less than 100% coverage\n- there are failing tests\n- linting rules have been violated.\n',
    'author': 'James Davis',
    'author_email': 'jamesecd@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/james-ecd/flare-explorer-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
