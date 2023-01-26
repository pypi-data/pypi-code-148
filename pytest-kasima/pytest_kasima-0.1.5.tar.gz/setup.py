# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_kasima']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.1,<8.0.0']

extras_require = \
{'rich': ['rich']}

entry_points = \
{'pytest11': ['kasima = pytest_kasima']}

setup_kwargs = {
    'name': 'pytest-kasima',
    'version': '0.1.5',
    'description': 'Display horizontal lines above and below the captured standard output for easy viewing.',
    'long_description': "[![PyPI version](https://badge.fury.io/py/pytest-kasima.svg)](https://badge.fury.io/py/pytest-kasima)\n[![Python Versions](https://img.shields.io/pypi/pyversions/pytest-kasima.svg)](https://pypi.org/project/pytest-kasima)\n\n# pytest-kasima\n\n![normal](https://github.com/k4sima/pytest-kasima/blob/main/screenshots/normal.png?raw=true)\n\n## install\n\n```\npip install pytest-kasima\n```\n\nIf you're a fan of [rich library](https://github.com/Textualize/rich), can integrate\n\n![with_rich](https://github.com/k4sima/pytest-kasima/blob/main/screenshots/rich.png?raw=true)\n\n```\npip install pytest-kasima[rich]\n```\n\n## usage\n\nDisplay horizontal lines above and below the captured standard output for easy viewing.\n\n`--capture=no` or `-s` option is not required.\n\n### options\n\n- `--kasima-skip` - If you don't like this plugin, disable it :smiley:\n- `--kasima-rich-skip` - Skip the rich integration\n",
    'author': 'k4sima',
    'author_email': '44926913+k4sima@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/k4sima/pytest-kasima',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
