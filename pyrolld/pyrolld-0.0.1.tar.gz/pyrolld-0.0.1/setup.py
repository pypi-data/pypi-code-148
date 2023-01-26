# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rolld']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyrolld',
    'version': '0.0.1',
    'description': 'A package to generate color sequences from videos and images',
    'long_description': '# pyrolld\n\nA package to generate color sequences from videos and images\n',
    'author': 'Vitaman02',
    'author_email': 'filip1253@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
