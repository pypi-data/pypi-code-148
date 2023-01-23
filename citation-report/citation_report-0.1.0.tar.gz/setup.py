# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['citation_report']

package_data = \
{'': ['*']}

install_requires = \
['citation-date>=0.1.0,<0.2.0', 'pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'citation-report',
    'version': '0.1.0',
    'description': 'Parse legal citations having the publisher format - i.e. SCRA, PHIL, OFFG - referring to Philippine Supreme Court decisions.',
    'long_description': 'None',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://lawsql.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
