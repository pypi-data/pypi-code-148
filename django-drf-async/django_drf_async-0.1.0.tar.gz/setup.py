# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_drf_async', 'django_drf_async.services']

package_data = \
{'': ['*']}

install_requires = \
['django>=4.1.5,<5.0.0', 'djangorestframework>=3.14.0,<4.0.0']

setup_kwargs = {
    'name': 'django-drf-async',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'godd0t',
    'author_email': 'lirrishala@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
