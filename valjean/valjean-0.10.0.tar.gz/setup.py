# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['valjean',
 'valjean.cambronne',
 'valjean.cambronne.commands',
 'valjean.cosette',
 'valjean.cosette.backends',
 'valjean.eponine',
 'valjean.eponine.apollo3',
 'valjean.eponine.tripoli4',
 'valjean.eponine.tripoli4.resources',
 'valjean.eponine.tripoli4.resources.depletion',
 'valjean.gavroche',
 'valjean.gavroche.diagnostics',
 'valjean.gavroche.stat_tests',
 'valjean.javert',
 'valjean.javert.resources',
 'valjean.javert.resources.rst']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3,<4.0', 'pyparsing>=3.0,<4.0', 'toml>=0.10,<0.11']

extras_require = \
{':(python_full_version >= "3.6.2" and python_full_version < "3.7.0") and (extra == "dev")': ['hypothesis[numpy]>=6.31,<7.0'],
 ':(python_full_version >= "3.6.2" and python_version < "3.8") and (extra == "dev")': ['Sphinx>=4.0,<4.1',
                                                                                       'flake8>=4.0,<4.1'],
 ':(python_version >= "3.7" and python_version < "4.0") and (extra == "dev")': ['hypothesis[numpy]>=6.55,<7.0'],
 ':(python_version >= "3.8") and (extra == "dev")': ['Sphinx>=5.0,<5.2',
                                                     'flake8>=5.0,<6.0'],
 ':extra == "dev"': ['pytest>=6.2,<7.0',
                     'pytest-cov>=3.0,<4.0',
                     'pytest-mpl>=0.13,<0.14',
                     'pytest-timeout>=2.0,<3.0',
                     'rstcheck>=3.3,<4.0',
                     'sphinx-rtd-theme>=1.0,<2.0',
                     'pylint>=2.12,<3.0',
                     'nbsphinx>=0.8,<0.9',
                     'jupyter-client>=7.1,<8.0',
                     'ipykernel>=5.5,<6.0',
                     'ipython!=8.7.0'],
 ':python_full_version >= "3.6.2" and python_full_version < "3.7.0"': ['numpy>=1.19,<2.0',
                                                                       'scipy>=1.5,<2.0',
                                                                       'h5py>=3.1,<3.2'],
 ':python_version >= "3.7" and python_version < "4.0"': ['numpy>=1.20,<2.0',
                                                         'scipy>=1.6,<2.0',
                                                         'h5py>=3.2,<4.0'],
 'graphviz': ['pydot>=1.4.2,<2.0.0']}

entry_points = \
{'console_scripts': ['valjean = valjean.cambronne.main:main']}

setup_kwargs = {
    'name': 'valjean',
    'version': '0.10.0',
    'description': "VALidation, Journal d'Évolution et ANalyse",
    'long_description': '# Valjean #\n\nQuick installation guide:\n\n*valjean* needs at least python3.6 (deprecated on December 23, 2021).\n\n## Installation using *pip* ##\n\n### Setup a virtual environment ###\n\n```\npython3 -m venv MY_VIRTUAL_ENV\nsource MY_VIRTUAL_ENV/bin/activate\npip install -U pip\n```\n\n### Installation from git ###\n\n```\ngit clone https://github.com/valjean-framework/valjean.git\npip install ./valjean  # or pip install path/to/valjean\n```\n\n### Installation from archive ###\n\nThe pip archive can be downloaded from the *Fichiers*/*Files* area of Tuleap.\n\n```\npip install valjean-VERSION.tar.gz\n```\n\n\n## Installation using *conda* ##\n\n1. Download and install *conda*.\n2. Download the *valjean-conda* archive from the *Fichiers*/*Files* area of\n   Tuleap.\n3. Install *valjean*:\n\n```\nsource MY_CONDA/bin/activate\nconda create -n MY_ENV python=PY_VERSION\nconda activate MY_ENV\nconda install -c file://PATH/TO/valjean-VERSION.tar.bz2 --use-local valjean\n```\n\nThe python version of *conda* should be the same as the one used to build the\n*valjean* archive.\n\nThis installation is not foreseen for development.\n\n\n## Documentation ##\n\nThe documentation can be found online: https://valjean.readthedocs.io/en/latest/\n\nIt can also be downloaded from the *Fichiers*/*Files* area of Tuleap.\n\n```\ntar xzf valjean-doc-*.tar.gz\n```\n\nYou can also consult the source files for the documentation in the ``doc/src``\ndirectory.\n',
    'author': 'valjean developers',
    'author_email': 'None',
    'maintainer': 'valjean developers',
    'maintainer_email': 'valjean-support@cea.fr',
    'url': 'https://github.com/valjean-framework/valjean',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
