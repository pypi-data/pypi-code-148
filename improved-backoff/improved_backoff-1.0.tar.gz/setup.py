# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['improved_backoff']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'improved-backoff',
    'version': '1.0',
    'description': 'Fork of a popular backoff library with a few fixed bugs',
    'long_description': 'improved\\_backoff\n=================\n\n[![image](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370)\n[![image](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380)\n[![image](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390)\n[![image](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100)\n\n[![image](https://github.com/Kirusi/improved_backoff/workflows/tests/badge.svg)](https://github.com/Kirusi/improved_backoff/actions/workflows/tests.yml)\n[![image](https://kirusi.github.io/improved_backoff/coverage.svg)](https://github.com/Kirusi/improved_backoff/actions/workflows/coverage.yml)\n[![image](https://img.shields.io/pypi/v/improved_backoff.svg)](https://pypi.python.org/pypi/improved_backoff)\n[![image](https://img.shields.io/github/license/kirusi/improved_backoff)](https://github.com/kirusi/improved_backoff/blob/master/LICENSE)\n\n**Function decoration for backoff and retry**\n\nThis is a fork of an excellent Python library\n[backoff](https://github.com/litl/backoff). The library was forked from\nversion 2.2.1 (October 5, 2022) This version includes 2 PRs proposed in\nthe original repo:\n\n-   [Correct check for max\\_time\n    parameter](https://github.com/litl/backoff/pull/130)\n-   [Using \\"timeit\\" module for time\n    management](https://github.com/litl/backoff/pull/185)\n\nIn order to use this module import it under `backoff` alias and use it\nthe same way as the original module\n\n```python\nimport improved_backoff as backoff\n\n@backoff.on_exception(backoff.expo, requests.exceptions.RequestException)\ndef get_url(url):\n    return requests.get(url)\n```\n',
    'author': 'Kirusi Msafiri',
    'author_email': 'kirusi.msafiri@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Kirusi/improved_backoff',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
