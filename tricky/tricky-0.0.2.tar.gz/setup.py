# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tricky']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tricky',
    'version': '0.0.2',
    'description': 'A set of useful features to make working with your code easier.',
    'long_description': '# tricky',
    'author': 'Alexander Walther',
    'author_email': 'alexander.walther.engineering@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Walther-s-Engineering/tricky',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
