# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['containers_sugar']

package_data = \
{'': ['*']}

install_requires = \
['docker-compose>=1.29.2,<2.0.0',
 'podman-compose>=1.0.3,<2.0.0',
 'pyyaml<6.0',
 'sh>=1.14.3,<2.0.0',
 'types-pyyaml>=6.0.12.3,<7.0.0.0']

entry_points = \
{'console_scripts': ['containers-sugar = containers_sugar.__main__:app']}

setup_kwargs = {
    'name': 'containers-sugar',
    'version': '1.0.3',
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
