# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_bdd_context']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-bdd-context',
    'version': '0.0.3',
    'description': 'Biblioteca com Context Manager para facilitar os testes de Behavior Driven Development (BDD)',
    'long_description': '# py-bdd-context\n\nLibrary with Context Manager to facilitate Behavior Driven Development (BDD) tests.\n\nThis library will help you organize your tests!\n\n## Using\nThere are examples of how to use the lib in the `examples` folder.\n\n\n## Installing\nhttps://pypi.org/project/py-bdd-context/\n```\npip install py-bdd-context\n```',
    'author': 'Imobanco',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/imobanco/py-bdd-context',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
