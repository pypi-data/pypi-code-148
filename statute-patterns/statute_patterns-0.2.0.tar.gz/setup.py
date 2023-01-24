# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statute_patterns', 'statute_patterns.components', 'statute_patterns.recipes']

package_data = \
{'': ['*']}

install_requires = \
['email-validator>=1.3.0,<2.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.21,<0.22',
 'python-slugify>=6.1.2,<7.0.0']

setup_kwargs = {
    'name': 'statute-patterns',
    'version': '0.2.0',
    'description': 'Philippine statutory law pattern matching and unit retrieval.',
    'long_description': '# statute-patterns\n\n![Github CI](https://github.com/justmars/statute-patterns/actions/workflows/main.yml/badge.svg)\n\nPhilippine statutory law pattern matching and unit retrieval; utilized in [LawSQL dataset](https://lawsql.com).\n\n## Documentation\n\nSee [documentation](https://justmars.github.io/statute-patterns).\n\n## Development\n\nCheckout code, create a new virtual environment:\n\n```sh\npoetry add statute-patterns # python -m pip install statute-patterns\npoetry update # install dependencies\npoetry shell\n```\n\nRun tests:\n\n```sh\npytest\n```\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://lawsql.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
