# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mtworker', 'mtworker.tasks', 'my_package2']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mtworker',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Example Package\n',
    'author': 'a',
    'author_email': 'a@a.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
