# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lm_backend', 'lm_backend.api']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy-Utils>=0.37.8,<0.38.0',
 'SQLAlchemy>=1.4.29,<2.0.0',
 'armasec>=0.11,<0.12',
 'asyncpg>=0.24.0,<0.25.0',
 'aws-psycopg2>=1.2.1,<2.0.0',
 'databases[postgresql]>=0.5.3,<0.6.0',
 'fastapi>=0.68.0,<0.69.0',
 'loguru>=0.5.3,<0.6.0',
 'py-buzz>=3.2.1,<4.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'sentry-sdk>=1.3.1,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'uvicorn>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'license-manager-backend',
    'version': '2.2.18',
    'description': 'Provides an API for managing license data',
    'long_description': '# License-manager Backend',
    'author': 'OmniVector Solutions',
    'author_email': 'info@omnivector.solutions',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/omnivector-solutions/license-manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
