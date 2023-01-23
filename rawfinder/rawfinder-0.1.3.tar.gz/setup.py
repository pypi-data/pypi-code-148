# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rawfinder']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['rawfinder = rawfinder.core:main']}

setup_kwargs = {
    'name': 'rawfinder',
    'version': '0.1.3',
    'description': 'Raw Finder',
    'long_description': '# RawFinder - Find a corresponded raw file\n\n## What is it?\n\nThis script find a corresponded raw files for jpeg files in a directory.\n\n## How to install\n\n```bash\n$ pip install rawfinder\n```\n\n## How to use\n```bash\n$ rawfinder -h\n\nusage: rawfinder [-h] [-d DST] [jpeg] [raw]\n\nFind correspond raw files\n\npositional arguments:\n  jpeg               directory with jpeg files\n  raw                directory with source RAW files\n\noptions:\n  -h, --help         show this help message and exit\n  -d DST, --dst DST  destination dir\n```\n\n## Example\n\nFind raw files in ~/Pictures/raw folder for jpeg files in current\nfolder, copy them to `raw` folder inside current folder (name by\ndefault):\n\n```bash\n$ rawfinder . ~/Pictures/raw -dst ./raw\n```\n\n# Development\n\n## Install\n\n```bash\n$ poetry install\n```\n\n## Tests\n\n```bash\n$ poetry run make test\n```\n\n## Linters\n\n```bash\n$ poetry run make format\n```\n',
    'author': 'Vitalii Shishorin',
    'author_email': 'moskrc@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/moskrc/rawfinder',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
