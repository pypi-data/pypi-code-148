# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['monthify']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'cachetools>=5.2.1,<6.0.0',
 'loguru>=0.6.0,<0.7.0',
 'rich>=13.1.0,<14.0.0',
 'spotipy>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['monthify = monthify.main:run']}

setup_kwargs = {
    'name': 'monthify',
    'version': '0.2.1',
    'description': 'Sorts liked spotify tracks into playlists by the month they were liked.',
    'long_description': '# Monthify\nA python script that sorts liked spotify tracks into playlists by the month they were liked.\nInspired by an [IFTTT applet](https://ifttt.com/applets/rC5QtGu6-add-saved-songs-to-a-monthly-playlist) by user [t00r](https://ifttt.com/p/t00r)\n\n## Required\n- Python 3.10+\n- A spotify account\n- [Spotify Client_id and Client_secret](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/)\n\n\n## Install\n```\npip install monthify\n```\n\n## Usage\n```\nmonthify --client-id=CLIENT_ID --client-secret=CLIENT_SECRET\n```\n\n## Building\n### Required\n- [Poetry](https://python-poetry.org)\n\n```\ngit clone https://github.com/madstone0-0/monthify.git\ncd monthify\npoetry install\npoetry build\n```',
    'author': 'Madiba Hudson-Quansah',
    'author_email': 'mhquansah@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
