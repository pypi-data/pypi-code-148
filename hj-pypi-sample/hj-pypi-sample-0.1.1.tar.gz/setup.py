# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hj_pypi_sample']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['hj-pypi-sample = hj_pypi_sample:main']}

setup_kwargs = {
    'name': 'hj-pypi-sample',
    'version': '0.1.1',
    'description': 'Print hello',
    'long_description': '# Test\n\n',
    'author': 'Hojung Yun',
    'author_email': 'hojung_yun@yahoo.co.kr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://yahoo.com',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
