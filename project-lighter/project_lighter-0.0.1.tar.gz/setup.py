# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lighter',
 'lighter.callbacks',
 'lighter.contrib',
 'lighter.contrib.models',
 'lighter.contrib.optimizer',
 'lighter.contrib.transforms',
 'lighter.contrib.utils',
 'lighter.utils']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.5.0,<0.6.0',
 'lightly>=1.2.43,<2.0.0',
 'loguru>=0.6.0,<0.7.0',
 'monai-weekly>=1.2.dev2304,<2.0',
 'pandas>=1.5.3,<2.0.0',
 'py>=1.11.0,<2.0.0',
 'pytorch-lightning>=1.9.0,<2.0.0',
 'tensorboard>=2.11.2,<3.0.0',
 'torch>=1.13.1,<2.0.0',
 'torchmetrics>=0.11.0,<0.12.0',
 'torchvision>=0.14.1,<0.15.0']

entry_points = \
{'console_scripts': ['lighter = lighter.utils.cli:interface']}

setup_kwargs = {
    'name': 'project-lighter',
    'version': '0.0.1',
    'description': 'YAML-based automated rapid prototyping framework for deep learning experiments',
    'long_description': '# Lighter\n[![build](https://github.com/project-lighter/lighter/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/project-lighter/lighter/actions/workflows/build.yml) ![Coverage](./assets/images/coverage.svg)\n\n\n## Setup\n\nRun the following commands to develop with the repository and add the package in develop mode to your environment\n\n````\nmake setup\nmake install \n````\n\nTo setup the pre-commit hook to format code before commit,\n````\nmake pre-commit-install\n````\n',
    'author': 'Ibrahim Hadzic',
    'author_email': 'ibrahimhadzic45@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lighter/lighter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
