# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['concave_uhull', 'concave_uhull.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0']

setup_kwargs = {
    'name': 'concave-uhull',
    'version': '0.1.1',
    'description': 'A simple (but not simpler) algorithm to obtain the concave hull using an alpha shape algorithm.',
    'long_description': '\n=================\nconcave_uhull*\n=================\n\nA simple (but not simpler) algorithm to obtain the concave hull using an alpha shape algorithm.\n\nInstallation\n============\n.. code:: bash\n\n  pip install concave_uhull\n\nNotes\n-----\n  * uhull! (Brazil) yeah! (expresses joy or celebration)\n',
    'author': 'Luan',
    'author_email': 'llvdmoraes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
