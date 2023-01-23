# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['heatcontrol']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'schedule>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'heatcontrol',
    'version': '0.2.1',
    'description': '',
    'long_description': '',
    'author': 'Rami Rahikkala',
    'author_email': 'rami.rahikkala@vincit.fi',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
