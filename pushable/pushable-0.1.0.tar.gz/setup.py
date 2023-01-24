# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pushable']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pushable',
    'version': '0.1.0',
    'description': 'Convert iterators into pushable iterators',
    'long_description': None,
    'author': 'Stephen Leach',
    'author_email': 'sfkleach@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
