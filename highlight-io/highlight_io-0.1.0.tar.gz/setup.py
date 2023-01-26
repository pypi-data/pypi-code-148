# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['highlight_io']

package_data = \
{'': ['*']}

install_requires = \
['opentelemetry-api>=1.15.0,<2.0.0',
 'opentelemetry-proto>=1.15.0,<2.0.0',
 'opentelemetry-sdk>=1.15.0,<2.0.0']

setup_kwargs = {
    'name': 'highlight-io',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Vadim Korolik',
    'author_email': 'vadim@highlight.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
