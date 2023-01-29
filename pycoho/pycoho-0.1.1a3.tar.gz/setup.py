# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycoho']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pycoho',
    'version': '0.1.1a3',
    'description': 'A Python wrapper for the UK Companies House API',
    'long_description': '# pycoho\nA Python wrapper for the UK Companies House API\n',
    'author': 'Armand Rego',
    'author_email': 'armand@weirdsheeplabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/regoawt/pycoho',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
