# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mtworker', 'mtworker.cmds', 'mtworker.tasks']

package_data = \
{'': ['*']}

install_requires = \
['celery[redis]>=5.2.7,<6.0.0',
 'httpx>=0.23.3,<0.24.0',
 'playwright>=1.29.1,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'mtworker',
    'version': '0.1.8',
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
