# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['galaxywitness']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx',
 'astropy',
 'gudhi',
 'matplotlib',
 'numpy',
 'pandas',
 'plotly',
 'scikit-learn',
 'sphinx-rtd-theme',
 'tqdm']

setup_kwargs = {
    'name': 'galaxywitness',
    'version': '0.2.3.1',
    'description': 'Package for topological data analysis of the big data. It is attempt to study distribution of galaxies in the universe via TDA',
    'long_description': '# GalaxyWitness\n[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)\n[![CodeFactor](https://www.codefactor.io/repository/github/davidosx/galaxywitness/badge/master)](https://www.codefactor.io/repository/github/davidosx/galaxywitness/overview/master)\n[![Documentation Status](https://readthedocs.org/projects/galaxywitness/badge/?version=latest)](https://galaxywitness.readthedocs.io/en/latest/?badge=latest)\n\n\nPackage for topological data analysis of the big data. It is attempt to study distribution of galaxies in the universe via TDA. Based on [GUDHI](https://gudhi.inria.fr) and [Astropy](https://www.astropy.org)\n\n## Requirements\n1. Python 3.8+ and pip\n2. git (for development)\n\nOS X or Linux\n\n## Installation\nFor the best experience, use python virtual environment:\n```sh\npip3 install virtualenv\nvirtualenv env (or python3 -m virtualenv galaxy-witness)\n. ./env/bin/activate\n```\nInstall this package from PyPI via ```pip install galaxywitness```\n\n## Documentation\nYou can find our technical documentation here: [Docs](https://galaxywitness.rtfd.io)\n### For developers\n[Sphinx](https://www.sphinx-doc.org/en/master/index.html) generates documentation for delelopers from sources in <code>./docs</code> folder. HTML files of documentation are in <code>./docs/build/html</code> and you can open it with browser. \nIf you want to build documentation yourself:\n```sh\ncd docs\nmake html\n```\nor if you want to get .pdf with documentation:\n```sh\ncd docs\nmake latexpdf\n```\n\n## Usage\nTo run just type:\n```sh   \npython -m galaxywitness\n```\n\nIn runtime the program will request you to choose file with your data. This file have to be in folder ```./data```\n\nIf you want to finish a work with package and deactivate virtual environment just type:\n```sh\ndeactivate\n```\n\n## Development\nYou can use python virtual environment and install dependencies manually:\n### Create and activate a virtual environment\nThis will create a new virtual environment called "galaxy-witness":\n```sh\npip3 install virtualenv\nvirtualenv galaxy-witness (or python3 -m virtualenv galaxy-witness)\n. ./galaxy-witness/bin/activate\n``` \nThis will clone the repository "GalaxyWitness" on your local machine, install dependencies and install this package \'galaxywitness\':\n```sh\ngit clone https://github.com/davidosx/GalaxyWitness\ncd GalaxyWitness\npip install -r requirements.txt\npython setup.py install\n```\n\nOr poetry package manager:\n### Poetry\n```sh\ngit clone https://github.com/davidosx/GalaxyWitness\ncd GalaxyWitness\npoetry install\n```\n\n### Uninstalling\nFor uninstalling (include dependencies and an virtual environment):\n```sh\nrm -r GalaxyWitness\nrm -r galaxy-witness\n```\n\n\n',
    'author': 'David Miheev',
    'author_email': 'me@davidkorol.life',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
