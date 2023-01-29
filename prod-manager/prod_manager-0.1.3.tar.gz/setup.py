# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prodmanager']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'prod-manager',
    'version': '0.1.3',
    'description': 'Interact with a ProdManager instance',
    'long_description': '# ProdManager API\n\n`prod-manager` is a Python package providing access to the [ProdManager][prodmanager] API.\n\n## Features\n\n`prod-manager` enables you to:\n\n- write Pythonic code to manage your [ProdManager][prodmanager] resources.\n- pass arbitrary parameters to the [ProdManager][prodmanager] API. Simply follow [ProdManager][prodmanager]’s docs on what parameters are available.\n- access arbitrary endpoints as soon as they are available on [ProdManager][prodmanager], by using lower-level API methods.\n- use persistent requests sessions for authentication, proxy and certificate handling.\n- flexible handling of paginated responses, including lazy iterators.\n\n## Installation\n\n`prod-manager` is compatible with Python 3.7+.\n\nUse `pip` to install the latest stable version of `prod-manager`:\n\n```bash\n$ pip install --upgrade prod-manager\n```\n\nThe current development version is available on GitLab.com, and can be installed directly from the git repository:\n\n```bash\n$ pip install git+https://gitlab.com/prod-manager/prod-manager-api.git\n```\n\n## Bug reports\n\nPlease report bugs and feature requests at <https://gitlab.com/prod-manager/prod-manager-api/-/issues>.\n\n## Documentation\n\nThe full documentation for CLI and API is available on [GitLab Pages][documentation-url].\n\n### Build the docs\n\nWe use `mkdocs` to manage our environment and build the documentation :\n\n```bash\n$ poetry install --only docs\n$ mkdocs build\n```\n\n## Contributing\n\nFor guidelines for contributing to `prod-manager`, refer to [CONTRIBUTING.md](./CONTRIBUTING.md).\n\n\n<!-- Links -->\n[documentation-url]: https://prod-manager-api.tiwabbit.fr\n[prodmanager]: https://gitlab.com/prod-manager/prod-manager',
    'author': 'Lunik',
    'author_email': 'lunik@tiwabbit.fr',
    'maintainer': 'Lunik',
    'maintainer_email': 'lunik@tiwabbit.fr',
    'url': 'https://gitlab.com/prod-manager/prod-manager-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
