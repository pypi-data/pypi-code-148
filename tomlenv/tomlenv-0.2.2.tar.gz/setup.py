# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tomlenv']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tomlenv',
    'version': '0.2.2',
    'description': 'Environment Wrapped TOML',
    'long_description': '# TOMLenv\n![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/joaonsantos/tomlenv/python-publish.yml)\n![PyPI - Version](https://img.shields.io/pypi/v/tomlenv)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tomlenv)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/tomlenv)\n![License](https://img.shields.io/github/license/joaonsantos/tomlenv)\n\nEnvironment wrapped TOML. \n\nPackage available in [PyPI](https://pypi.org/project/tomlenv/).\n\n## Getting Started\n\n### Install the library\n\nUsing pip:\n```sh\n$ pip install tomlenv\n```\n\nUsing pipenv:\n```sh\n$ pipenv install tomlenv\n```\n\nUsing poetry:\n```sh\n$ poetry add tomlenv\n```\n\n### Basic Usage\n\nTomlenv takes advantage of modern Python features such as `dataclasses` and\n`tomllib` to create a simple yet powerful configuration library.\n\nBy default, tomlenv looks for a `config.toml` file in your project root:\n```toml\ntoken = "dev"\ndebug = false\n```\n\nAssuming this environment variable is set:\n```sh\nTOMLENV_DEBUG=true\n```\n\nCreate your configuration dataclass and parse config and env into it:\n```python\nimport tomlenv\nfrom dataclasses import dataclass\n\n@dataclass\nclass Config:\n    token: str = \'\'\n    debug: bool = False\n\nconfig = Config()\nparser = tomlenv.Parser()\n\nparser.load(config)\n\n# You can now access the fields of your fully typed config Class\n# that contains values from a TOML config file and the environment.\n\n# For example:\n\ntoken = config.token\ndebug = config.debug\nprint(token) # prints "dev"\nprint(debug) # prints True\n```\n\n## Configuration\n\nTo configure the location of your toml file, set `TOMLENV_CONF_FILEPATH`.\n\nFor example if your config file is in `configs/config.toml` relative to the project root, then set `TOMLENV_CONF_FILEPATH=configs/config.toml`\n\n## Tests\n\nThis project uses [Poetry](https://python-poetry.org/) and [GNU Make](https://www.gnu.org/software/make/).\n\nRun tests from the project root with:\n```sh\n$ make test\n```\n\nTo get a coverage report:\n```sh\n$ make cov\n```\n\n## Issues\n\nFeel free to send issues or suggestions to https://github.com/joaonsantos/tomlenv/issues.\n',
    'author': 'João Santos',
    'author_email': 'joaopns05@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/joaonsantos/tomlenv',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
