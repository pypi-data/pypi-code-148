# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['spotify_assistant']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.3,<2.0.0', 'spotipy>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'spotify-assistant',
    'version': '0.1.3',
    'description': "A package that makes spotify users' lives easier!",
    'long_description': '# spotify_assistant\n\nA Python package that enriches spotify users\' music experience by allowing them to explore their listening trends via REST APIs implemented for Spotify developers.\n\nThere is one similar Python package, [Spotipy](https://github.com/spotipy-dev/spotipy) that provides wrapper functions in Python for the Spotify API. This package contains a function for each possible API request, but does not combine any of these requests. Our aim is to create functions that combine multiple requests and provide additional insights for Spotify users.\n\n## Authors\n- Caroline Tang\n- Chester Wang\n- Jenit Jain\n- Julie Song\n\nThis package was originally created as part of the requirements of DSCI524 (Collaborative Software Development), a course in the Master of Data Science program at the University of British Columbia. All original members of this project abided by the [Code of Conduct](CONDUCT.md).\n\n## Installation\n\n```bash\n$ pip install spotify_assistant\n```\n\n## Usage\n\n```bash\nimport spotify_assistant\n\ncredentials = {clientId:\'xxxxxxxxxxxx\', clientSecret: \'xxxxxxxxxxxx\'}\nRandomUser = User(credentials)\nRandomUser.get_song_recommendations("Recommended Songs")\nRandomUser.get_users_playlists_songs()\nRandomUser.get_users_top_genres()\nspotify_assistant.User.get_new_releases_by_continent("Asia")\n\n```\n\n## Functions\n\n- `get_users_top_genres()`: Returns the top 5 genres of music that a user listens to and has saved in the "Your Music" library.\n- `get_song_recommendations(playlist_name, num_songs)`: Creates a playlist of recommended songs based on user’s top 3 artists.\n- `get_playlists_songs(playlists)`: Returns the songs saved in all the playlists, which are passed as a list to the function.\n- `get_new_releases_by_continent(continent, limit)`: Returns the new releases by continent\n\n## Contributing\n\nInterested in contributing? Check out the [contributing guidelines](CONTRIBUTING.md). Please note that this project is released with a [Code of Conduct](CONDUCT.md). By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`spotify_assistant` was created by Caroline Tang, Julie Song, Jenit Jain, Chester Wang. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`spotify_assistant` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Caroline Tang, Julie Song, Jenit Jain, Chester Wang',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
