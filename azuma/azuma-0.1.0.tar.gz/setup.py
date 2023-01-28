# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azuma', 'azuma.schemas']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.12,<1.0',
 'pydantic>=1.8,<2.0',
 'pyyaml>=6.0,<7.0',
 'regex>=2022']

setup_kwargs = {
    'name': 'azuma',
    'version': '0.1.0',
    'description': 'Yet another Sigma library for Python',
    'long_description': '# azuma\n\n[![PyPI version](https://badge.fury.io/py/azuma.svg)](https://badge.fury.io/py/azuma)\n[![Test](https://github.com/ninoseki/azuma/actions/workflows/test.yml/badge.svg)](https://github.com/ninoseki/azuma/actions/workflows/test.yml)\n\nYet another [Sigma](https://github.com/SigmaHQ/sigma) library for Python.\n\nNote: This is a forked version of [CybercentreCanada/pysigma](https://github.com/CybercentreCanada/pysigma). Most of the things in this library come from their hard work.\n\n## Docs\n\n- [Requirements](https://github.com/ninoseki/azuma/wiki/Requirements)\n- [Installation](https://github.com/ninoseki/azuma/wiki/Installation)\n- [Usage](https://github.com/ninoseki/azuma/wiki/Usage)\n- [Known limitations](https://github.com/ninoseki/azuma/wiki/Known-limitations)\n',
    'author': 'Manabu Niseki',
    'author_email': 'manabu.niseki@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ninoseki/azuma',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
