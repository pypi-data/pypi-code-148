# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['demo_package', 'mtworker', 'mtworker.tasks']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'mtworker',
    'version': '0.1.4',
    'description': '',
    'long_description': '# Example Package\n',
    'author': 'a',
    'author_email': 'a@a.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
