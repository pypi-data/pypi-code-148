# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['grai_source_snowflake']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'grai-client>=0.2.0,<0.3.0',
 'grai-schemas>=0.1.5,<0.2.0',
 'multimethod>=1.8,<2.0',
 'pydantic>=1.9.1,<2.0.0',
 'snowflake-connector-python>=2.8.3,<3.0.0']

setup_kwargs = {
    'name': 'grai-source-snowflake',
    'version': '0.0.7',
    'description': '',
    'long_description': 'None',
    'author': 'Tony Lewis',
    'author_email': 'tony@grai.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
