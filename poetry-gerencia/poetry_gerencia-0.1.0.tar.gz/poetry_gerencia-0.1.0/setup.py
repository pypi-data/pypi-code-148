# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_gerencia']

package_data = \
{'': ['*']}

install_requires = \
['pyglet>=2.0.3,<3.0.0']

setup_kwargs = {
    'name': 'poetry-gerencia',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Eduardo Gurgel',
    'author_email': '51385738+EduardoGurgel@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
