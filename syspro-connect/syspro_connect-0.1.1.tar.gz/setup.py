# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['syspro_connect']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.3,<2.0.0',
 'pyodbc>=4.0.35,<5.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'sqlalchemy>=1.4.46,<2.0.0']

setup_kwargs = {
    'name': 'syspro-connect',
    'version': '0.1.1',
    'description': '',
    'long_description': '# TODO',
    'author': 'w-ejt',
    'author_email': '97180065+w-ejt@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
