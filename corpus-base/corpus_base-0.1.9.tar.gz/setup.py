# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['corpus_base', 'corpus_base.utils']

package_data = \
{'': ['*'], 'corpus_base': ['templates/*']}

install_requires = \
['citation-utils>=0.2.3,<0.3.0',
 'corpus-pax>=0.1.12,<0.2.0',
 'markdownify>=0.11.6,<0.12.0',
 'unidecode>=1.3.6,<2.0.0']

setup_kwargs = {
    'name': 'corpus-base',
    'version': '0.1.9',
    'description': 'Add justice, decision, citation, voting, opinion, and segment tables to database.',
    'long_description': '# corpus-base\n\n![Github CI](https://github.com/justmars/corpus-base/actions/workflows/main.yml/badge.svg)\n\nAdd justice, decision, citation, voting, opinion, and segment tables to database; utilized in the [LawSQL dataset](https://lawsql.com).\n\n## Documentation\n\nSee [documentation](https://justmars.github.io/corpus-base), building on top of [corpus-pax](https://justmars.github.io/corpus-pax)\n\n## Development\n\nCheckout code, create a new virtual environment:\n\n```sh\npoetry add corpus-base # python -m pip install corpus-base\npoetry update # install dependencies\npoetry shell\n```\n\nRun tests:\n\n```sh\npytest\n```\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://lawdata.xyz',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
