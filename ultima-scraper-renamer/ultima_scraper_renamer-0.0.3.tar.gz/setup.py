# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ultima_scraper_renamer']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3.8.3,<4.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'ultima-scraper-api>=0.0.1.5,<0.0.2.0']

setup_kwargs = {
    'name': 'ultima-scraper-renamer',
    'version': '0.0.3',
    'description': '',
    'long_description': '',
    'author': 'DIGITALCRIMINALS',
    'author_email': '89371864+DIGITALCRIMINALS@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
