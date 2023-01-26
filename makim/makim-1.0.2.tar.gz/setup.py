# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['makim']

package_data = \
{'': ['*']}

install_requires = \
['jinja2<3.0.3', 'pyyaml<6.0', 'sh>=1.14.3,<2.0.0']

entry_points = \
{'console_scripts': ['makim = makim.__main__:app']}

setup_kwargs = {
    'name': 'makim',
    'version': '1.0.2',
    'description': 'Simplify the usage of containers',
    'long_description': None,
    'author': 'Ivan Ogasawara',
    'author_email': 'ivan.ogasawara@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
