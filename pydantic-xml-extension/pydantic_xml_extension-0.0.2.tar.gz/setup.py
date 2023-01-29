# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_xml']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0', 'xmltodict>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'pydantic-xml-extension',
    'version': '0.0.2',
    'description': '',
    'long_description': '# Pydantic XML Extension\n\nAllows Pydantic models to render to XML.\n',
    'author': 'Patrick Withams',
    'author_email': 'pwithams@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
