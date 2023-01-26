# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['medleydb_instruments']

package_data = \
{'': ['*'],
 'medleydb_instruments': ['resources/annotations/*', 'resources/metadata/*']}

install_requires = \
['pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'medleydb-instruments',
    'version': '1.0.0',
    'description': 'A tool to query MedleyDB annotations and metadata.',
    'long_description': '# medleydb_instruments\n[![Linter Actions Status](https://github.com/Seon82/medleydb_instruments/actions/workflows/lint.yml//badge.svg?branch=master)](https://github.com/Seon82/medleydb_instruments/actions)\n\n`medleydb_instruments` is a tool to seemlessly query MedleyDB annotations and instrument metadata.\n\nThe [MedleyDB 1.0 and 2.0](https://medleydb.weebly.com/) datasets don\'t provide annotations or metadata, only raw audio files. The authors provide [an official github repo](https://github.com/marl/medleydb) containing metadata, but it is painful to install and can be quite complex to use. \n\n## Installation\nSimply run: `pip install medleydb_instruments`\n\n## Quickstart\n```python\nimport medleydb_instruments as mdb\n\ntrack = mdb.MultiTrack("AcDc_BackInBlack")\n# Get a list of instruments present in the track\ninstrument_list = track.instruments\n# Determine if the recording has bleed\nhas_bleed = track.has_bleed\n# Get a dataframe of instrument activations\nactivations_df = track.activations\n```\n\n',
    'author': 'Dylan Sechet',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Seon82/medleydb_instruments',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
