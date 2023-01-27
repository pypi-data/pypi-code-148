# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['apispec_pydantic_plugin']

package_data = \
{'': ['*']}

install_requires = \
['apispec>=6.0.2,<7', 'pydantic>=1.10.4,<2']

setup_kwargs = {
    'name': 'apispec-pydantic-plugin',
    'version': '0.2.1',
    'description': '',
    'long_description': '',
    'author': 'Kevin Kirsche',
    'author_email': 'kevin.kirsche@one.verizon.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
