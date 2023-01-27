# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mastodonamnesia']

package_data = \
{'': ['*']}

install_requires = \
['aiocsv>=1.2.3,<2.0.0',
 'aiofiles>=0.8.0,<0.9.0',
 'arrow>=1.2.1,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'minimal-activitypub>=0.4.0,<0.5.0',
 'outdated>=0.2.1,<0.3.0',
 'rich>=13.0.0,<14.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'typing-extensions>=4.2.0,<5.0.0']

entry_points = \
{'console_scripts': ['mastodonamnesia = '
                     'mastodonamnesia.mastodon_amnesia:start']}

setup_kwargs = {
    'name': 'mastodonamnesia',
    'version': '2.2.2',
    'description': 'Renamed to Fedinesia. Use Fedinesia for future updates and bug fixes.',
    'long_description': 'MastodonAmnesia\n---------------\n\n!!! MastodonAmnesia has been renamed to **Fedinesia** which is available on PyPI.org !!!\n\n!!! MastodonAmnesia no longer receives fixes or new features !!!\n\nPlease update to Fedinesia\n==========================\n\nUse the links below for information and to update:\n\n - https://pypi.org/project/fedinesia/\n - https://codeberg.org/MarvinsMastodonTools/fedinesia\n',
    'author': 'marvin8',
    'author_email': 'marvin8@tuta.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/MarvinsMastodonTools/mastodonamnesia',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
