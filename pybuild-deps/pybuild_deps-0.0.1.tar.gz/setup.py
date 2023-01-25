# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pybuild_deps']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1']

entry_points = \
{'console_scripts': ['pybuild-deps = pybuild_deps.__main__:main']}

setup_kwargs = {
    'name': 'pybuild-deps',
    'version': '0.0.1',
    'description': 'A simple tool for detection of PEP-517 build dependencies.',
    'long_description': "# PyBuild Deps\n\n[![PyPI](https://img.shields.io/pypi/v/pybuild-deps.svg)][pypi status]\n[![Status](https://img.shields.io/pypi/status/pybuild-deps.svg)][pypi status]\n[![Python Version](https://img.shields.io/pypi/pyversions/pybuild-deps)][pypi status]\n[![License](https://img.shields.io/pypi/l/pybuild-deps)][license]\n\n[![Read the documentation at https://pybuild-deps.readthedocs.io/](https://img.shields.io/readthedocs/pybuild-deps/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/bruno-fs/pybuild-deps/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/bruno-fs/pybuild-deps/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi status]: https://pypi.org/project/pybuild-deps/\n[read the docs]: https://pybuild-deps.readthedocs.io/\n[tests]: https://github.com/bruno-fs/pybuild-deps/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/bruno-fs/pybuild-deps\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _PyBuild Deps_ via [pip] from [PyPI]:\n\n```console\n$ pip install pybuild-deps\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [GPL 3.0 license][license],\n_PyBuild Deps_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/bruno-fs/pybuild-deps/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/bruno-fs/pybuild-deps/blob/main/LICENSE\n[contributor guide]: https://github.com/bruno-fs/pybuild-deps/blob/main/CONTRIBUTING.md\n[command-line reference]: https://pybuild-deps.readthedocs.io/en/latest/usage.html\n",
    'author': 'Bruno Ciconelle',
    'author_email': 'fsouza.bruno@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bruno-fs/pybuild-deps',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
