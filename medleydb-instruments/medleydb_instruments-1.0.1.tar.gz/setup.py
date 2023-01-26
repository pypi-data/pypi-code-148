# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['medleydb_instruments']

package_data = \
{'': ['*'],
 'medleydb_instruments': ['resources/annotations/*', 'resources/metadata/*']}

install_requires = \
['pandas>=1.0.0,<2']

setup_kwargs = {
    'name': 'medleydb-instruments',
    'version': '1.0.1',
    'description': 'A tool to query MedleyDB annotations and metadata.',
    'long_description': '# 🎷 medleydb-instruments\n[![Supported Python Versions](https://img.shields.io/pypi/pyversions/medleydb-instruments)](https://pypi.org/project/medleydb-instruments/)\n [![PyPI version](https://badge.fury.io/py/medleydb-instruments.svg)](https://badge.fury.io/py/medleydb-instruments)\n [![Linter Actions Status](https://github.com/Seon82/medleydb_instruments/actions/workflows/lint.yml//badge.svg?branch=master)](https://github.com/Seon82/medleydb_instruments/actions)\n\n`medleydb-instruments` is a tool used to seemlessly query MedleyDB annotations and instrument metadata.\n\nThe [MedleyDB 1.0 and 2.0](https://medleydb.weebly.com/) datasets don\'t provide annotations or metadata, only raw audio files. The authors provide [an official github repo](https://github.com/marl/medleydb) containing metadata, but it is painful to install and can be quite complex to use. \n\n## Installing\nInstall with `pip` or your favorite PyPI package manager.\n\n```python -m pip install medleydb-instruments```\n\n## Example\n```python\nimport medleydb_instruments as mdb\n\ntrack = mdb.MultiTrack("AcDc_BackInBlack")\n# Get a list of instruments present in the track\ninstrument_list = track.instruments\n# Determine if the recording has bleed\nhas_bleed = track.has_bleed\n# Get a dataframe of instrument activations\nactivations_df = track.activations\n```\n\n',
    'author': 'Dylan Sechet',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Seon82/medleydb_instruments',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
