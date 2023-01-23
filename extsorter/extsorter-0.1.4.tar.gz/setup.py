# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['extsorter']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['extsorter = extsorter.core:sort']}

setup_kwargs = {
    'name': 'extsorter',
    'version': '0.1.4',
    'description': 'File Sorter',
    'long_description': '# ExtSorter - A simple file sorter\n\n## What is it?\n\nSometimes you have a folder with a lot of files, and you want\nto sort them into folders. This is where ExtSorter comes in.\nIt will sort your files into folders based on the file extension.\n\n## How to install\n\n```bash\n$ pip install extsorter\n```\n\n## How to use\n```bash\n$ extsorter -h\n\nusage: extsorter [-h] [-d DST] [src]\n\nSort files by extension\n\npositional arguments:\n  src                source dir\n\noptions:\n  -h, --help         show this help message and exit\n  -d DST, --dst DST  destination dir\n```\n\n## Example\n\nSort files in current directory to a folder called `sorted` (name by default):\n\n```bash\n$ extsorter\n```\n\nSort files in `~/Downloads` to `~/Downloads/old`:\n\n```bash\n$ extsorter ~/Downloads -d ~/Downloads/old\n```\n\n# Development\n\n## Install\n\n```bash\n$ poetry install\n```\n\n## Tests\n\n```bash\n$ poetry run make test\n```\n\n## Linters\n\n```bash\n$ poetry run make format\n```\n',
    'author': 'Vitalii Shishorin',
    'author_email': 'moskrc@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/moskrc/filesorter',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
