# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statute_trees', 'statute_trees.utils']

package_data = \
{'': ['*']}

install_requires = \
['citation-utils>=0.2.3,<0.3.0', 'statute-patterns>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'statute-trees',
    'version': '0.1.0',
    'description': 'Tree-based Philippine Codifications, Statutes, and Documents, using a uniform node structure (i.e., leaves of a tree) identified by a given material path.',
    'long_description': '# statute-trees\n\n![Github CI](https://github.com/justmars/statute-trees/actions/workflows/main.yml/badge.svg)\n\n Tree-based Philippine Codifications, Statutes, and Documents, using a uniform node structure; utilized in the [LawSQL dataset](https://lawsql.com).\n\n## Documentation\n\nSee [documentation](https://justmars.github.io/statute-trees).\n\n## Development\n\nCheckout code, create a new virtual environment:\n\n```sh\npoetry add statute-trees # python -m pip install statute-trees\npoetry update # install dependencies\npoetry shell\n```\n\nRun tests:\n\n```sh\npytest\n```\n',
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
