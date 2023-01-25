# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_k4sima']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.1,<8.0.0']

entry_points = \
{'pytest11': ['k4sima = pytest_k4sima']}

setup_kwargs = {
    'name': 'pytest-kasima',
    'version': '0.1.1',
    'description': '',
    'long_description': '[![PyPI version](https://badge.fury.io/py/pytest_k4sima.svg)](https://badge.fury.io/py/pytest_k4sima)\n[![Python Versions](https://img.shields.io/pypi/pyversions/pytest_k4sima.svg)](https://pypi.org/project/pytest_k4sima)\n\n# pytest-k4sima\n\n## install\n\n```\npip install pytest-k4sima\n```\n\n## usage\n\nDisplay horizontal lines above and below the captured standard output for easy viewing.\n\n### options\n\n- `--kasima-skip` - disable\n',
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
