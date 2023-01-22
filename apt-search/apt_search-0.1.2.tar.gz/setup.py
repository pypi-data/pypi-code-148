# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apt_search']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'httpx>=0.23.3,<0.24.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['apt-search = apt_search.main:app']}

setup_kwargs = {
    'name': 'apt-search',
    'version': '0.1.2',
    'description': 'Search Ubuntu packages.',
    'long_description': '# apt-search\n\n*Search Ubuntu packages.*\n\n## Installation\n\nUse `pip` or `pipx` for installation:\n\n```bash\npip install --user apt-search\n# or\npipx install apt-search\n```\n\n## Usage\n\nJust execute the `apt-search` command with the filename you are looking for:\n\n```bash\napt-search --help\n# Usage: main.py [OPTIONS] FILENAME\n#\n# Arguments:\n#   FILENAME  [required]\n#\n# Options:\n#   --suite TEXT                    [default: jammy]\n#   --arch TEXT                     [default: any]\n#   --help                          Show this message and exit.\n```\n',
    'author': 'David Härer',
    'author_email': 'david@familie-haerer.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/DavidHeresy/apt-search',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
