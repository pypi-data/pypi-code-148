# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['corpus_x', 'corpus_x.utils']

package_data = \
{'': ['*'],
 'corpus_x': ['sql/analysis/*',
              'sql/base/*',
              'sql/codes/*',
              'sql/codes/events/*',
              'sql/decisions/*',
              'sql/decisions/inclusions/*',
              'sql/statutes/*',
              'sql/statutes/references/*']}

install_requires = \
['corpus-base>=0.1.10,<0.2.0', 'statute-trees>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'corpus-x',
    'version': '0.0.2',
    'description': 'Add codification and statute tables to pre-existing corpus-base database.',
    'long_description': '# corpus-x\n\n![Github CI](https://github.com/justmars/corpus-x/actions/workflows/main.yml/badge.svg)\n\nCreate the `x.db` sqlite database for lawdata; utilized in the [LawSQL dataset](https://lawsql.com).\n\n## Documentation\n\nSee [documentation](https://justmars.github.io/corpus-x), building on top of [corpus-base](https://justmars.github.io/corpus-base)\n\n## Development\n\nCheckout code, create a new virtual environment:\n\n```sh\npoetry add corpus-x # python -m pip install corpus-x\npoetry update # install dependencies\npoetry shell\n```\n\nRun tests:\n\n```sh\npytest\n```\n',
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
