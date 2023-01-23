# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytrms', 'pytrms.clients', 'pytrms.testing']

package_data = \
{'': ['*'], 'pytrms': ['data/*']}

install_requires = \
['h5py>=3.6.0,<4.0.0',
 'pandas>=1.4.0,<2.0.0',
 'pyModbusTCP>=0.2.0,<0.3.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pytrms',
    'version': '0.2.2',
    'description': 'Python bundle for proton-transfer reaction mass-spectrometry (PTR-MS).',
    'long_description': 'None',
    'author': 'Moritz Koenemann',
    'author_email': 'moritz.koenemann@ionicon.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
