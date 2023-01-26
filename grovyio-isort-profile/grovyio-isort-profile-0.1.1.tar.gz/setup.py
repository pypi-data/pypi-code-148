# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grovyio_isort_profile']

package_data = \
{'': ['*']}

entry_points = \
{'isort.profiles': ['grovyio = grovyio_isort_profile.grovyio_profile:PROFILE']}

setup_kwargs = {
    'name': 'grovyio-isort-profile',
    'version': '0.1.1',
    'description': '',
    'long_description': '## Usage\n\n### pyproject.toml\n\n```toml\n[tool.isort]\nprofile = "grovyio"\nsrc_paths = ["my_project", "tests"]\n```\n',
    'author': 'Jung, Byung Kwan',
    'author_email': 'bkjung@grovy.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
