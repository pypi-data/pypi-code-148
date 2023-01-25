# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['demo_package', 'mtworker', 'mtworker.tasks']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mtworker',
    'version': '0.1.3',
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
