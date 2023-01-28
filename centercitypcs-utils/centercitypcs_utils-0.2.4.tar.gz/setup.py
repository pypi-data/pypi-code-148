# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['centercitypcs_utils']

package_data = \
{'': ['*']}

install_requires = \
['cx-oracle>=8.0.1,<9.0.0',
 'gspread>=5.7.2,<6.0.0',
 'gspread_dataframe>=3.1.0,<4.0.0',
 'pandas>=1.1.2,<2.0.0',
 'records>=0.5.3,<0.6.0',
 'sqlalchemy>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'centercitypcs-utils',
    'version': '0.2.4',
    'description': '',
    'long_description': 'None',
    'author': 'Scott Burns',
    'author_email': 'sburns@centercitypcs.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
