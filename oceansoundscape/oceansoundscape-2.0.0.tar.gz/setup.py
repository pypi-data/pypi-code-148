# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oceansoundscape',
 'oceansoundscape.raven',
 'oceansoundscape.spectrogram',
 'oceansoundscape.testdata',
 'oceansoundscape.tests',
 'oceansoundscape.tests.data']

package_data = \
{'': ['*']}

install_requires = \
['h5py>=3.8.0,<4.0.0',
 'librosa==0.9.1',
 'matplotlib>=3.6.3,<4.0.0',
 'numpy==1.23.5',
 'opencv-python-headless>=4.7.0,<5.0.0',
 'pandas>=1.5.3,<2.0.0',
 'scipy>=1.10.0,<2.0.0',
 'soundfile==0.10.3.post1']

setup_kwargs = {
    'name': 'oceansoundscape',
    'version': '2.0.0',
    'description': 'A python package for analyzing ocean acoustic data. ',
    'long_description': '[![MBARI](https://www.mbari.org/wp-content/uploads/2014/11/logo-mbari-3b.png)](http://www.mbari.org)\n\n[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)\n![Supported Platforms](https://img.shields.io/badge/Supported%20Platforms-Windows%20%7C%20macOS%20%7C%20Linux-green)\n![license-GPL](https://img.shields.io/badge/license-GPL-blue)\n\n# About\n\nA python package for analyzing ocean acoustic data. \n \nAuthor: Danelle Cline, [dcline@mbari.org](mailto:dcline@mbari.org)\n\n## Prerequisites\n \n- Python 3.8 or 3.9\n \n## Installation\n\n```pip install oceansoundscape```\n\n## Documentation\n\nFull documentation is available at [https://docs.mbari.org/oceansoundscape/](https://docs.mbari.org/oceansoundscape/)\n\n\n## Development\n\nThis project is developed using [poetry](https://python-poetry.org/).  To install poetry, follow the instructions [here](https://python-poetry.org/docs/#installation).  Once poetry is installed, you can install the project dependencies by running:\n\n```poetry install```\n\nTo run the tests, run:\n\n```poetry run pytest```\n\nSee the DEV.md for more information on development.',
    'author': 'danellecline',
    'author_email': 'dcline@mbari.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mbari-org/oceansoundscape',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.9',
}


setup(**setup_kwargs)
