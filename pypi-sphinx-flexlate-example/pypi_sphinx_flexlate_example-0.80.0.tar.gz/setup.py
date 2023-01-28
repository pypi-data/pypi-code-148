# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypi_sphinx_flexlate_example']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypi-sphinx-flexlate-example',
    'version': '0.80.0',
    'description': 'Example output for https://github.com/nickderobertis/copier-pypi-sphinx-flexlate',
    'long_description': '\n\n[![](https://codecov.io/gh/nickderobertis/pypi-sphinx-flexlate-example/branch/main/graph/badge.svg)](https://codecov.io/gh/nickderobertis/pypi-sphinx-flexlate-example)\n[![PyPI](https://img.shields.io/pypi/v/pypi-sphinx-flexlate-example)](https://pypi.org/project/pypi-sphinx-flexlate-example/)\n![PyPI - License](https://img.shields.io/pypi/l/pypi-sphinx-flexlate-example)\n[![Documentation](https://img.shields.io/badge/documentation-pass-green)](https://nickderobertis.github.io/pypi-sphinx-flexlate-example/)\n![Tests Run on Ubuntu Python Versions](https://img.shields.io/badge/Tests%20Ubuntu%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)\n![Tests Run on Macos Python Versions](https://img.shields.io/badge/Tests%20Macos%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)\n![Tests Run on Windows Python Versions](https://img.shields.io/badge/Tests%20Windows%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)\n[![Github Repo](https://img.shields.io/badge/repo-github-informational)](https://github.com/nickderobertis/pypi-sphinx-flexlate-example/)\n\n\n#  pypi-sphinx-flexlate-example\n\n## Overview\n\nExample output for https://github.com/nickderobertis/copier-pypi-sphinx-flexlate\n\n## Getting Started\n\nInstall `pypi-sphinx-flexlate-example`:\n\n```\npip install pypi-sphinx-flexlate-example\n```\n\nA simple example:\n\n```python\nimport pypi_sphinx_flexlate_example\n\n# Do something with pypi_sphinx_flexlate_example\n```\n\nSee a\n[more in-depth tutorial here.](\nhttps://nickderobertis.github.io/pypi-sphinx-flexlate-example/tutorial.html\n)\n\n## Links\n\nSee the\n[documentation here.](\nhttps://nickderobertis.github.io/pypi-sphinx-flexlate-example/\n)\n\n## Development Status\n\nThis project is currently in early-stage development. There may be\nbreaking changes often. While the major version is 0, minor version\nupgrades will often have breaking changes.\n\n## Developing\n\nSee the [development guide](\nhttps://github.com/nickderobertis/pypi-sphinx-flexlate-example/blob/main/DEVELOPING.md\n) for development details.\n\n## Author\n\nCreated by Nick DeRobertis. MIT License.\n\n',
    'author': 'Nick DeRobertis',
    'author_email': 'derobertis.nick@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
