# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['riksdagenapi']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0', 'requests>=2.28.2,<3.0.0', 'rich>=13.3.0,<14.0.0']

setup_kwargs = {
    'name': 'riksdagenapi',
    'version': '0.0.4',
    'description': 'Libray for accessing the Riksdagen API',
    'long_description': '# Riksdagen API\nThis library makes it easy to get data from Riksdagen\n\n# Features\nIt currently only support getting documents by id and \n\nSee http://data.riksdagen.se/dokumentation/ for details.\n\n## What I learned from writing this\n* Writing this library I intentionally tried \n  using Test Driven Development. This proved to be \n  a valuable exercise!\n  \n## License\nGPLv3+',
    'author': 'Dennis Priskorn',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
