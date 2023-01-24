# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clean_ioc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'clean-ioc',
    'version': '0.0.1',
    'description': 'An IOC Container for Python 3.10+',
    'long_description': '# clean_ioc\nA simple dependency injection library for python\n\n## TODO: Add more here',
    'author': 'Peter Daly',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/peter-daly/clean_ioc',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
