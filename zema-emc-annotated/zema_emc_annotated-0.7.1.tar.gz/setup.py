# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['zema_emc_annotated']

package_data = \
{'': ['*'], 'zema_emc_annotated': ['examples/*']}

install_requires = \
['h5py>=3.7.0,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pooch>=1.6.0,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

extras_require = \
{'docs': ['ipython>=8.8.0,<9.0.0',
          'myst-parser>=0.18.1,<0.19.0',
          'nbsphinx>=0.8.12,<0.9.0',
          'sphinx>=5.3.0,<6.0.0',
          'sphinx-rtd-theme>=1.1.1,<2.0.0']}

setup_kwargs = {
    'name': 'zema-emc-annotated',
    'version': '0.7.1',
    'description': 'API to the annotated ZeMA dataset about an electro-mechanical cylinder',
    'long_description': '# zema_emc_annotated\n\n[![pipeline status](https://gitlab1.ptb.de/m4d/zema_emc_annotated/badges/main/pipeline.svg)](https://gitlab1.ptb.de/m4d/zema_emc_annotated/-/commits/main)\n[![Documentation Status](https://readthedocs.org/projects/zema-emc-annotated/badge/?version=v0.7.1)](https://zema-emc-annotated.readthedocs.io/en/v0.7.1/)\n[![codecov](https://codecov.io/gh/PTB-M4D/zema_emc_annotated/branch/main/graph/badge.svg?token=HQZE3FXL7N)](https://app.codecov.io/gh/PTB-M4D/zema_emc_annotated?search=&displayType=list&trend=7%20days)\n[![Latest Release](https://img.shields.io/github/v/release/PTB-M4D/zema_emc_annotated?label=Latest%20Release)](https://github.com/PTB-M4D/zema_emc_annotated/releases/latest)\n[![DOI](https://zenodo.org/badge/591514193.svg)](https://doi.org/10.5281/zenodo.7556142)\n\nThis software provides a convenient API to access the [annotated ZeMA dataset about \nremaining useful life of an electro-mechanical cylinder on\nZenodo](https://doi.org/10.5281/zenodo.5185953). The code was written for _Python 3.10_.\n\n## Getting started\n\nThe [INSTALL guide](INSTALL.md) assists in installing the required packages. \nAfterwards please visit our\n[example page](https://zema-emc-annotated.readthedocs.io/en/latest/examples.html).\n\n## Documentation\n\nThe documentation can be found on\n[ReadTheDocs](https://zema-emc-annotated.readthedocs.io/en/v0.7.1/).\n\n## Disclaimer\n\nThis software is developed at Physikalisch-Technische Bundesanstalt (PTB). The software\nis made available "as is" free of cost. PTB assumes no responsibility whatsoever for\nits use by other parties, and makes no guarantees, expressed or implied, about its\nquality, reliability, safety, suitability or any other characteristic. In no event\nwill PTB be liable for any direct, indirect or consequential damage arising in\nconnection with the use of this software.\n\n## License\n\nzema_emc_annotated is distributed under the [MIT\nlicense](https://github.com/PTB-M4D/zema_emc_annotated/blob/main/LICENSE).\n',
    'author': 'Bjoern Ludwig',
    'author_email': 'bjoern.ludwig@ptb.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
