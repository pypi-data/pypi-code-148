# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlpyd']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'sqlite-utils>=3.30,<4.0']

setup_kwargs = {
    'name': 'sqlpyd',
    'version': '0.1.4',
    'description': 'Validate raw content with pydantic for consumption by sqlite-utils.',
    'long_description': '# sqlpyd\n\n![Github CI](https://github.com/justmars/sqlpyd/actions/workflows/main.yml/badge.svg)\n\nValidate raw content with pydantic for consumption by sqlite-utils.; utilized in the [LawSQL dataset](https://lawsql.com).\n\n## Documentation\n\nSee [documentation](https://justmars.github.io/sqlpyd).\n\n## Development\n\nCheckout code, create a new virtual environment:\n\n```sh\npoetry add sqlpyd # python -m pip install sqlpyd\npoetry update # install dependencies\npoetry shell\n```\n\nRun tests:\n\n```sh\npytest\n```\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://lawsql.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
