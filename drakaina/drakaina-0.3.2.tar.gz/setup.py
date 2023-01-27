# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drakaina',
 'drakaina.client',
 'drakaina.contrib',
 'drakaina.contrib.django',
 'drakaina.contrib.jwt',
 'drakaina.middlewares',
 'drakaina.middlewares.openapi']

package_data = \
{'': ['*']}

extras_require = \
{'msgpack': ['msgpack>=1.0.4,<2.0.0'],
 'orjson': ['orjson>=3.8.5,<4.0.0'],
 'ujson': ['ujson>=5.7.0,<6.0.0']}

setup_kwargs = {
    'name': 'drakaina',
    'version': '0.3.2',
    'description': 'Module for simple RPC server implementation',
    'long_description': '# drakaina\n\n❗ WIP\n\nModule for simple RPC server implementation\n\n![license: Apache License 2.0](https://img.shields.io/badge/license-Apache%202-blue) ![Python: >=3.7](https://img.shields.io/badge/python-%3E=3.7-blue) ![Code style: black](https://img.shields.io/badge/code%20style-black-black)\n\n## Quick use\n\n```python\nfrom drakaina import remote_procedure\nfrom drakaina.rpc_protocols import JsonRPCv2\n\n\n@remote_procedure\ndef my_method():\n    return "Hello Bro! ✋️"\n\n\nJsonRPCv2().handle({"jsonrpc": "2.0", "method": "my_method", "id": 1})\n```\n\n## Installation\n\n```shell\npip install drakaina\n```\n',
    'author': 'Aleksey Terentyev',
    'author_email': 'terentyev.a@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/tau_lex/drakaina',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
