# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypi_sphinx_flexlate_example']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypi-sphinx-flexlate-example',
    'version': '0.74.0',
    'description': 'Example output for https://github.com/nickderobertis/copier-pypi-sphinx-flexlate',
    'long_description': '\n\n[![](https://codecov.io/gh/nickderobertis/pypi-sphinx-flexlate-example/branch/main/graph/badge.svg)](https://codecov.io/gh/nickderobertis/pypi-sphinx-flexlate-example)\n[![PyPI](https://img.shields.io/pypi/v/pypi-sphinx-flexlate-example)](https://pypi.org/project/pypi-sphinx-flexlate-example/)\n![PyPI - License](https://img.shields.io/pypi/l/pypi-sphinx-flexlate-example)\n[![Documentation](https://img.shields.io/badge/documentation-pass-green)](https://nickderobertis.github.io/pypi-sphinx-flexlate-example/)\n![Tests Run on Ubuntu Python Versions](https://img.shields.io/badge/Tests%20Ubuntu%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)\n![Tests Run on Macos Python Versions](https://img.shields.io/badge/Tests%20Macos%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)\n![Tests Run on Windows Python Versions](https://img.shields.io/badge/Tests%20Windows%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)\n[![Github Repo](https://img.shields.io/badge/repo-github-informational)](https://github.com/nickderobertis/pypi-sphinx-flexlate-example/)\n\n\n#  pypi-sphinx-flexlate-example\n\n## Overview\n\nExample output for https://github.com/nickderobertis/copier-pypi-sphinx-flexlate\n\n## Getting Started\n\nInstall `pypi-sphinx-flexlate-example`:\n\n```\npip install pypi-sphinx-flexlate-example\n```\n\nA simple example:\n\n```python\nimport pypi_sphinx_flexlate_example\n\n# Do something with pypi_sphinx_flexlate_example\n```\n\nSee a\n[more in-depth tutorial here.](\nhttps://nickderobertis.github.io/pypi-sphinx-flexlate-example/tutorial.html\n)\n\n## Links\n\nSee the\n[documentation here.](\nhttps://nickderobertis.github.io/pypi-sphinx-flexlate-example/\n)\n\n## Development Status\n\nThis project is currently in early-stage development. There may be\nbreaking changes often. While the major version is 0, minor version\nupgrades will often have breaking changes.\n\n## Developing\n\n### Initial Setup\n\nFirst, you need a couple global dependencies installed, see their documentation for details:\n- [direnv](https://direnv.net/docs/installation.html)\n- [asdf](https://asdf-vm.com/guide/getting-started.html)\n\nNote that these tools require a UNIX-style shell, such as bash or zsh. If\nyou are on Windows, you can use WSL or Git Bash. If you are using Pycharm,\nyou can configure the built-in terminal to use Git Bash.\n\nThen clone the repo and run `direnv allow`. This will take a while on the first time\nto install the remaining dependencies.\n\n### Day to Day Development\n\nMake your changes and then run `just` to run formatting,\nlinting, and tests.\n\nDevelop documentation by running `just docs` to start up a dev server.\n\nTo run tests only, run `just test`. You can pass additional arguments to pytest,\ne.g. `just test -k test_something`.\n\nPrior to committing, you can run `just` with no arguments to run all the checks.\n\n#### Conventional Commits & Semantic Release\n\nThis project uses [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)\nto power [semantic release](https://semantic-release.gitbook.io/semantic-release/). This means\nthat when you commit, you should use the following format:\n\n```\n<type>[optional scope]: <description>\n```\n\nFor example, `feat: Add new feature` or `fix: Fix bug`.\n\nWhen creating a PR, please name the PR in this way as well so that the squashed\ncommit from the PR will have a conventional commit message.\n\n#### Pre-commit Hooks\n\nThis project uses Husky and Lint-staged to run pre-commit hooks. This means that\nwhen you commit, it will run `just format` and `just strip` on the files\nyou edited, and also check that your commit message is a conventional commit.\n\nIf you are not able to commit, it is likely because your commit message is not\nin the conventional commit format.\n\n## Author\n\nCreated by Nick DeRobertis. MIT License.\n\n',
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
