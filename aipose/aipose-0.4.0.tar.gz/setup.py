# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aipose', 'aipose.webcam']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'matplotlib>=3.2.2',
 'numpy>=1.18.5,<1.24.0',
 'opencv-python>=4.1.1',
 'pandas>=1.1.4',
 'protobuf<4.21.3',
 'pydantic',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'scipy>=1.4.1',
 'seaborn>=0.11.0',
 'tensorboard>=2.4.1',
 'torch>=1.7.0,!=1.12.0',
 'torchvision>=0.8.1,!=0.13.0',
 'tqdm>=4.41.0',
 'types-requests>=2.28.11.8,<3.0.0.0']

entry_points = \
{'console_scripts': ['posewebcam = aipose.__main__:webcam']}

setup_kwargs = {
    'name': 'aipose',
    'version': '0.4.0',
    'description': 'Library to use pose estimation in your projects easily',
    'long_description': '# aipose\n\nLibrary to use pose estimation in your projects easily.\n\n[![PyPI version](https://badge.fury.io/py/aipose.svg)](https://badge.fury.io/py/aipose)\n',
    'author': 'Tlaloc-Es',
    'author_email': 'dev@tlaloc-es.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Tlaloc-Es/aipose',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
