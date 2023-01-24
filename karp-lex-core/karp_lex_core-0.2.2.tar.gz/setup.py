# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['karp',
 'karp.lex_core',
 'karp.lex_core.dtos',
 'karp.lex_core.tests',
 'karp.lex_core.value_objects']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0', 'ulid-py>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'karp-lex-core',
    'version': '0.2.2',
    'description': 'The core of karp-lex',
    'long_description': '# karp-lex-core\nThe core for karp-lex\n\n',
    'author': 'Språkbanken at the University of Gothenburg',
    'author_email': 'sb-info@svenska.gu.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://spraakbanken.gu.se',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
