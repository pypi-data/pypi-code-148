# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rmscene']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rmscene',
    'version': '0.1.0',
    'description': 'Read v6 .rm files from the reMarkable tablet',
    'long_description': 'None',
    'author': 'Rick Lupton',
    'author_email': 'mail@ricklupton.name',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
