# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_filterset']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy[asyncio,mypy]>=1.4,<2', 'greenlet>=1.1.2']

setup_kwargs = {
    'name': 'sqlalchemy-filterset',
    'version': '1.0.0',
    'description': '',
    'long_description': 'None',
    'author': 'Arseny Sysolyatin',
    'author_email': 'as@idaproject.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
