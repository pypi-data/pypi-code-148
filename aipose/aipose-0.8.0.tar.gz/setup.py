# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aipose', 'aipose.frame', 'aipose.stream']

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
    'version': '0.8.0',
    'description': 'Library to use pose estimation in your projects easily',
    'long_description': '# AIPOSE\n\n<div align="center">\n\n[![Downloads](https://static.pepy.tech/personalized-badge/aipose?period=month&units=international_system&left_color=grey&right_color=blue&left_text=PyPi%20Downloads)](https://pepy.tech/project/aipose)\n[![Stars](https://img.shields.io/github/stars/Tlaloc-Es/aipose?color=yellow&style=flat)](https://github.com/Tlaloc-Es/aipose/stargazers)\n\n</div>\n\n\n<p align="center">\n        <img src="./logo.png" width="200" height="240"/>\n    </p>\n\nLibrary to use pose estimation in your projects easily.\n## Instalation [![PyPI](https://img.shields.io/pypi/v/aipose.svg)](https://pypi.org/project/aipose/)\n\nYou can install `aipose` from [Pypi](https://pypi.org/project/aipose/). It\'s going to install the library itself and its prerequisites as well.\n\n```bash\npip install aipose\n```\n\nYou can install `aipose` from its source code.\n\n```bash\ngit clone https://github.com/Tlaloc-Es/aipose.git\ncd aipose\npip install -e .\n```\n\n## Run demo\n\nUse the following command to run a demo with your cam and YOLOv7 pose estimator,\n\n```bash\nposewebcam\n```\n\n## How to use\n\nYou can check the section notebooks in the repository to check the usage of the library or you can ask in the [Issues section](https://github.com/Tlaloc-Es/aipose/issues).\n\nThe examples are:\n\n* [How to draw key points in a video](https://github.com/Tlaloc-Es/aipose/blob/master/notebooks/video.ipynb)\n* [How to draw key points in a webcam](https://github.com/Tlaloc-Es/aipose/blob/master/notebooks/webcam.ipynb)\n* [How to draw key points in a picture](https://github.com/Tlaloc-Es/aipose/blob/master/notebooks/plot_keypoints.ipynb)\n* [How to capture a frame to apply your business logic](https://github.com/Tlaloc-Es/aipose/blob/master/notebooks/custom%20manager.ipynb)\n* [How to stop the video stream when anybody raises hands with YOLOv7](https://github.com/Tlaloc-Es/aipose/blob/master/notebooks/process_keypoints.ipynb)\n\n## References\n\n* https://github.com/RizwanMunawar/yolov7-pose-estimation\n\n## Support\n\nYou can do a donation with the following link.\n\n<a href="https://www.buymeacoffee.com/tlaloc" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>\n\nOr you can try to make a pull request with your improvements to the repo.\n\n## Source of videos and images\n\n* Video by Mikhail Nilov: https://www.pexels.com/video/a-woman-exercising-using-an-exercise-ball-6739975/',
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
