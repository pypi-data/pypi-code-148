# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hitfactorpy_sqlalchemy',
 'hitfactorpy_sqlalchemy.cli',
 'hitfactorpy_sqlalchemy.migrations',
 'hitfactorpy_sqlalchemy.migrations.versions',
 'hitfactorpy_sqlalchemy.orm']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.9.2,<2.0.0',
 'asyncpg>=0.27.0,<0.28.0',
 'hitfactorpy>=0.0.4,<0.0.5',
 'inflection>=0.5.1,<0.6.0',
 'sqlalchemy-continuum>=1.3.14,<2.0.0',
 'sqlalchemy[asyncio,mypy]>=1.4,<2.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['hitfactorpy-sqlalchemy = hitfactorpy_sqlalchemy.cli:cli']}

setup_kwargs = {
    'name': 'hitfactorpy-sqlalchemy',
    'version': '0.0.1',
    'description': 'Manage practical match reports with SQLAlchemy',
    'long_description': '# hitfactorpy_sqlalchemy\n\n[![Main](https://github.com/cahna/hitfactorpy_sqlalchemy/actions/workflows/main.yaml/badge.svg)](https://github.com/cahna/hitfactorpy_sqlalchemy/actions/workflows/main.yaml)\n\nManage practical match reports with SQLAlchemy\n\n## Status\n\n**Work in progress...**\n\n## Usage\n\n1. Run migrations on a database to create tables and types:\n    ```console\n    $ hitfactorpy-sqlalchemy migrate up\n    ```\n2. Verify DB status:\n    ```console\n    $ hitfactorpy-sqlalchemy migrate check\n    ```\n3. Import a match report from a text file:\n    ```console\n    $ hitfactorpy-sqlalchemy import match-report ./report.txt\n    ```\n4. Bulk import match reports:\n    ```console\n    $ find reports/ -type f -name "*.txt" | xargs hitfactorpy-sqlalchemy import match-report\n    ```\n',
    'author': 'Conor Heine',
    'author_email': 'conor.heine@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
