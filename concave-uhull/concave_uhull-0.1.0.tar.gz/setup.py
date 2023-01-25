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
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'Luan',
    'author_email': 'luan.moraes@loggi.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
