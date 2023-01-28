# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gracy']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0']

extras_require = \
{'rich': ['rich']}

setup_kwargs = {
    'name': 'gracy',
    'version': '0.1.0',
    'description': 'Gracefully manage your API interactions',
    'long_description': '<p align="center">\n    <img src="./img/logo-dark.png#gh-dark-mode-only">\n    <img src="./img/logo-light.png#gh-light-mode-only">\n</p>\n\n<h2 align="center">Gracefully manage your API interactions</h2>\n\n<p align="center">\n  <!-- CI --><a href="https://github.com/guilatrova/gracy/actions"><img alt="Actions Status" src="https://github.com/guilatrova/gracy/workflows/CI/badge.svg"></a>\n  <!-- PyPI --><a href="https://pypi.org/project/gracy/"><img alt="PyPI" src="https://img.shields.io/pypi/v/gracy"/></a>\n  <!-- Supported Python versions --><img src="https://badgen.net/pypi/python/gracy" />\n  <!-- Alternative Python versioning: <img alt="python version" src="https://img.shields.io/badge/python-3.9%20%7C%203.10-blue"> -->\n  <!-- LICENSE --><a href="https://github.com/guilatrova/gracy/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/guilatrova/gracy"/></a>\n  <!-- PyPI downloads --><a href="https://pepy.tech/project/gracy/"><img alt="Downloads" src="https://static.pepy.tech/personalized-badge/gracy?period=total&units=international_system&left_color=grey&right_color=blue&left_text=%F0%9F%A6%96%20Downloads"/></a>\n  <!-- Formatting --><a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"/></a>\n  <!-- Tryceratops --><a href="https://github.com/guilatrova/tryceratops"><img alt="try/except style: tryceratops" src="https://img.shields.io/badge/try%2Fexcept%20style-tryceratops%20%F0%9F%A6%96%E2%9C%A8-black" /></a>\n  <!-- Typing --><a href="https://github.com/python/mypy"><img alt="Types: mypy" src="https://img.shields.io/badge/types-mypy-blue.svg"/></a>\n  <!-- Follow handle --><a href="https://twitter.com/intent/user?screen_name=guilatrova"><img alt="Follow guilatrova" src="https://img.shields.io/twitter/follow/guilatrova?style=social"/></a>\n  <!-- Sponsor --><a href="https://github.com/sponsors/guilatrova"><img alt="Sponsor guilatrova" src="https://img.shields.io/github/sponsors/guilatrova?logo=GitHub%20Sponsors&style=social"/></a>\n</p>\n\nGracy helps you handle failures, logging, retries, and tracking for all your HTTP interactions.\n\n> "Don\'t repeat, simplify"\n\n---\n\n## Get started\n\n### Installation\n\n```\npip install gracy\n```\n\nOR\n\n```\npoetry add gracy\n```\n',
    'author': 'Guilherme Latrova',
    'author_email': 'hello@guilatrova.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/guilatrova/gracy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
