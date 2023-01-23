# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['checkedid', 'checkedid.models']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.1,<0.24.0', 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'checkedid',
    'version': '0.4.0',
    'description': 'CheckedID Python API client',
    'long_description': '# CheckedID Python API client\n\n[![PyPI](https://img.shields.io/pypi/v/checkedid.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/checkedid.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/checkedid)][python version]\n[![License](https://img.shields.io/pypi/l/checkedid)][license]\n\n[![Read the documentation at https://checkedid.readthedocs.io/](https://img.shields.io/readthedocs/checkedid-api-python-client/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/foarsitter/checkedid-api-python-client/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/foarsitter/checkedid-api-python-client/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/checkedid/\n[status]: https://pypi.org/project/checkedid/\n[python version]: https://pypi.org/project/checkedid\n[read the docs]: https://checkedid.readthedocs.io/\n[tests]: https://github.com/foarsitter/checkedid-api-python-client/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/foarsitter/checkedid-api-python-client\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- Typed API client for api.checkedid.eu\n\n## Requirements\n\n- Build with Pydantic and httpx, does currently not support async.\n\n## Installation\n\nYou can install _CheckedID Python API client_ via [pip] from [PyPI]:\n\n```console\n$ pip install checkedid\n```\n\n## Usage\n\n```py\nfrom checkedid import errors, models, Client\n\ntry:\n    client = Client(\'1001\')\n    dossier: models.ReportResponse = client.dossier(\'123456789\')\nexcept errors.CheckedIDNotFoundError as e:\n    print("Dossier does not exists")\n```\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_CheckedID Python API client_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/foarsitter/checkedid-api-python-client/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/foarsitter/checkedid-api-python-client/blob/main/LICENSE\n[contributor guide]: https://github.com/foarsitter/checkedid-api-python-client/blob/main/CONTRIBUTING.md\n',
    'author': 'Jelmer Draaijer',
    'author_email': 'jelmer.draaijer@dok.works.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/foarsitter/checkedid-api-python-client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
