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
    'version': '0.5.1',
    'description': 'Library to use pose estimation in your projects easily',
    'long_description': '<center>\n    <h1>AIPOSE</h1>\n    <b> Library to use pose estimation in your projects easily.</b>\n    <br>\n    <a href="https://badge.fury.io/py/aipose"><img src="https://badge.fury.io/py/aipose.svg" alt="PyPI version" height="18"></a>\n</center>\n\n## Instalation\n\n```bash\npip install aipose\n```\n\n## Run demo\n\nUse the following command to run a dem with your cam and yolo-v7-pose-estimator:\n\n```bash\nposewebcam\n```\n\n## How to use\n\nYou can check the section notebooks in the repo in order to check the usage of the library or you can ask in the [Issues section](https://github.com/Tlaloc-Es/aipose/issues).\n\n## References\n* https://github.com/RizwanMunawar/yolov7-pose-estimation\n\n## Support\n\nYou can do a donation with the following link.\n\n<a href="https://www.buymeacoffee.com/tlaloc" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>\n\nOr you can try to make a pull request with your improvements to the repo.\n',
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
