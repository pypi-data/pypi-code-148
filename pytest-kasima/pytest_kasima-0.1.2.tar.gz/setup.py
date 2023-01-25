# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_kasima']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.1,<8.0.0']

entry_points = \
{'pytest11': ['k4sima = pytest_kasima']}

setup_kwargs = {
    'name': 'pytest-kasima',
    'version': '0.1.2',
    'description': '',
    'long_description': '[![PyPI version](https://badge.fury.io/py/pytest_kasima.svg)](https://badge.fury.io/py/pytest_kasima)\n[![Python Versions](https://img.shields.io/pypi/pyversions/pytest_kasima.svg)](https://pypi.org/project/pytest_kasima)\n\n# pytest-kasima\n\n## install\n\n```\npip install pytest-kasima\n```\n\n## usage\n\nDisplay horizontal lines above and below the captured standard output for easy viewing.\n\n### options\n\n- `--kasima-skip` - disable\n',
    'author': 'k4sima_0',
    'author_email': '44926913+k4sima@users.noreply.github.com',
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
