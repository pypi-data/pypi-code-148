# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['corpus_pax']

package_data = \
{'': ['*'], 'corpus_pax': ['templates/*']}

install_requires = \
['email-validator>=1.3.0,<2.0.0',
 'httpx>=0.23.0,<0.24.0',
 'jinja2>=3.1.2,<4.0.0',
 'mkdocs-material>=9.0.6,<10.0.0',
 'mkdocs>=1.4.2,<2.0.0',
 'mkdocstrings[python]>=0.20.0,<0.21.0',
 'python-frontmatter>=1.0.0,<2.0.0',
 'sqlpyd>=0.1.4,<0.2.0']

setup_kwargs = {
    'name': 'corpus-pax',
    'version': '0.1.12',
    'description': 'Using Github API (to pull individuals, orgs, and article content), setup a local sqlite database, syncing images to Cloudflare.',
    'long_description': '# corpus-pax\n\n![Github CI](https://github.com/justmars/corpus-pax/actions/workflows/main.yml/badge.svg)\n\nUsing Github API (to pull individuals, orgs, and article content), setup a local sqlite database, syncing images to Cloudflarel utilized in the [LawSQL dataset](https://lawsql.com).\n\n## Documentation\n\nSee [documentation](https://justmars.github.io/corpus-pax).\n\n## Development\n\nCheckout code, create a new virtual environment:\n\n```sh\npoetry add corpus-pax # python -m pip install corpus-pax\npoetry update # install dependencies\npoetry shell\n```\n\nRun tests:\n\n```sh\npytest\n```\n',
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
