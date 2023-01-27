# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ultima_scraper_api',
 'ultima_scraper_api.apis',
 'ultima_scraper_api.apis.fanhouse',
 'ultima_scraper_api.apis.fanhouse.classes',
 'ultima_scraper_api.apis.fanhouse.decorators',
 'ultima_scraper_api.apis.fansly',
 'ultima_scraper_api.apis.fansly.classes',
 'ultima_scraper_api.apis.fansly.decorators',
 'ultima_scraper_api.apis.onlyfans',
 'ultima_scraper_api.apis.onlyfans.classes',
 'ultima_scraper_api.apis.onlyfans.decorators',
 'ultima_scraper_api.classes',
 'ultima_scraper_api.database',
 'ultima_scraper_api.database.archived_databases.messages',
 'ultima_scraper_api.database.archived_databases.messages.alembic',
 'ultima_scraper_api.database.archived_databases.messages.alembic.versions',
 'ultima_scraper_api.database.archived_databases.posts',
 'ultima_scraper_api.database.archived_databases.posts.alembic',
 'ultima_scraper_api.database.archived_databases.posts.alembic.versions',
 'ultima_scraper_api.database.archived_databases.stories',
 'ultima_scraper_api.database.archived_databases.stories.alembic',
 'ultima_scraper_api.database.archived_databases.stories.alembic.versions',
 'ultima_scraper_api.database.databases',
 'ultima_scraper_api.database.databases.user_data',
 'ultima_scraper_api.database.databases.user_data.alembic',
 'ultima_scraper_api.database.databases.user_data.alembic.versions',
 'ultima_scraper_api.database.databases.user_data.models',
 'ultima_scraper_api.database.extras.db_upgrader',
 'ultima_scraper_api.docs.source',
 'ultima_scraper_api.helpers',
 'ultima_scraper_api.managers',
 'ultima_scraper_api.managers.job_manager',
 'ultima_scraper_api.managers.job_manager.jobs',
 'ultima_scraper_api.managers.metadata_manager',
 'ultima_scraper_api.managers.storage_managers']

package_data = \
{'': ['*'], 'ultima_scraper_api': ['docs/*']}

install_requires = \
['SQLAlchemy>=1.4.44,<2.0.0',
 'Sphinx>=5.3.0,<6.0.0',
 'aiofiles>=22.1.0,<23.0.0',
 'aiohttp-socks>=0.7.1,<0.8.0',
 'aiohttp>=3.8.3,<4.0.0',
 'alembic>=1.8.1,<2.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'dill>=0.3.6,<0.4.0',
 'mergedeep>=1.3.4,<2.0.0',
 'mypy>=0.991,<0.992',
 'orjson>=3.8.3,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-socks>=2.0.3,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'sphinx-autoapi>=2.0.0,<3.0.0',
 'sphinx-rtd-theme>=1.1.1,<2.0.0',
 'user-agent>=0.1.10,<0.2.0',
 'websockets>=10.4,<11.0']

setup_kwargs = {
    'name': 'ultima-scraper-api',
    'version': '0.0.1.5',
    'description': '',
    'long_description': 'None',
    'author': 'DIGITALCRIMINALS',
    'author_email': '89371864+DIGITALCRIMINALS@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
