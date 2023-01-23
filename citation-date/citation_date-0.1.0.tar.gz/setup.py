# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['citation_date', 'citation_date.base']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8,<3.0', 'types-python-dateutil>=2.8.19,<3.0.0']

setup_kwargs = {
    'name': 'citation-date',
    'version': '0.1.0',
    'description': 'Regex date formula and decoder - Philippine Supreme Court Decisions',
    'long_description': '# citation-date\n\n![Github CI](https://github.com/justmars/citation-date/actions/workflows/main.yml/badge.svg)\n\nRegex date formula and decoder, eventually used by the dataset employed in [LawSQL](https://lawsql.com).\n\n## Documentation\n\nSee [documentation](https://justmars.github.io/citation-date).\n\n## Development\n\nCheckout code, create a new virtual environment:\n\n```sh\npoetry add citation-date # python -m pip install citation-date\npoetry update # install dependencies\npoetry shell\n```\n\nRun tests:\n\n```sh\npytest\n```\n',
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
