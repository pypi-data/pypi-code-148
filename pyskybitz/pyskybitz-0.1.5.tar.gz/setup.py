# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyskybitz', 'pyskybitz.models', 'pyskybitz.services']

package_data = \
{'': ['*']}

install_requires = \
['Inject>=4.3.1,<5.0.0',
 'lxml>=4.9.2,<5.0.0',
 'pydantic==1.10.4',
 'requests>=2.28.1,<3.0.0',
 'six==1.16.0']

setup_kwargs = {
    'name': 'pyskybitz',
    'version': '0.1.5',
    'description': 'Python client to work with SkyBitz API',
    'long_description': None,
    'author': 'Jasurbek Nurboyev',
    'author_email': 'jasurbeknurboyev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
