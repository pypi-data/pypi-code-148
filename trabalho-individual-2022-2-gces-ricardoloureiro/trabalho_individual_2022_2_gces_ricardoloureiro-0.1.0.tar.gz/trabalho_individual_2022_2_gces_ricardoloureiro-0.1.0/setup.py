# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_trabalho']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'trabalho-individual-2022-2-gces-ricardoloureiro',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Ricardo Loureiro',
    'author_email': 'ricardoloureiro75@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
