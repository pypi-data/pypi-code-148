# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['backup_podcasts']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.7.1,<0.8.0',
 'feedparser>=6.0.10,<7.0.0',
 'fire>=0.5.0,<0.6.0',
 'parfive>=2.0.2,<3.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'backup-podcasts',
    'version': '0.1.2',
    'description': 'Backup/archive all episodes of your podcast subscriptions locally.',
    'long_description': '# backup podcasts\n\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\nBackup/archive all your podcasts.\n\nInsallation:\n\n`pip install backup-podcasts`\n\nFeatures:\n\n* OPML import\n* RSS pagination\n* Backup metadata (RSS, shownotes, cover)\n* Graceful interruption behaviour (no half-downloaded files, even when killed)\n* File-system compatible filename sanization (format: `pubdate - title`)\n\nUsage:\n\n`python3 -m backup-podcasts --opml "path_to.opml" --destination "/target/backup/location"`\n\nDestination is optional, defaults to cwd.\n',
    'author': 'DreamFlasher',
    'author_email': '31695+dreamflasher@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dreamflasher/backup-podcasts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
