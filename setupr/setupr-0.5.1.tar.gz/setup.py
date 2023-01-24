# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['setupr']

package_data = \
{'': ['*']}

install_requires = \
['click-help-colors>=0.9.1,<0.10.0',
 'click>=8.1.3,<9.0.0',
 'distro>=1.8.0,<2.0.0',
 'google-cloud-storage>=2.5.0,<3.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'plumbum>=1.7.2,<2.0.0',
 'protobuf>=4.21.6,<5.0.0',
 'python-gnupg>=0.5.0,<0.6.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.4.4,<14.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'semver>=2.10,<3',
 'sha256sum>=2022.6.11,<2023.0.0',
 'structlog>=22.1.0,<23.0.0']

entry_points = \
{'console_scripts': ['setupr = setupr.console:main']}

setup_kwargs = {
    'name': 'setupr',
    'version': '0.5.1',
    'description': 'Setupr ships the Worldr infrastructure.',
    'long_description': '# Setupr, ships the Worldr infrastructure…\n\n<img src="https://github.com/worldr/setupr/blob/main/docs/assets/logo.png" width=25% height=25% >\n\n[![PyPi status](https://img.shields.io/pypi/status/Setupr)](https://img.shields.io/pypi/status/Setupr)\n[![PyPi version](https://img.shields.io/pypi/v/setupr)](https://img.shields.io/pypi/v/setupr)\n[![PyPi python versions](https://img.shields.io/pypi/pyversions/Setupr)](https://img.shields.io/pypi/pyversions/Setupr)\n[![PyPi downloads](https://img.shields.io/pypi/dm/setupr)](https://img.shields.io/pypi/dm/Setupr)\n\n[![Release](https://img.shields.io/github/v/release/worldr/setupr)](https://img.shields.io/github/v/release/worldr/setupr)\n[![Build status](https://img.shields.io/github/actions/workflow/status/worldr/setupr/codeql.yml?branch=main)](https://img.shields.io/github/actions/workflow/status/worldr/setupr/codeql.yml?branch=main)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/worldr/setupr)](https://img.shields.io/github/commit-activity/m/worldr/setupr)\n[![Code style with black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports with isort](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)\n\n---\n\n## Documentation\n\n- [Installation](docs/installation.md)\n- [Usage](docs/usage.md)\n- [Development](docs/development.md)\n\n---\n\n## Quick install\n\n```bash\npython -venv worldr\nsource ./worldr/bin/activate\npip install -U setupr\nsetupr --help\n```\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).\n',
    'author': 'Dr Yann Golanski',
    'author_email': 'ygg@worldr.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/worldr/setupr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
