# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djangocms_themata',
 'djangocms_themata.management.commands',
 'djangocms_themata.migrations',
 'djangocms_themata.templatetags']

package_data = \
{'': ['*'], 'djangocms_themata': ['templates/*', 'templates/themata/*']}

install_requires = \
['Django>=3.2,<4.0',
 'django-cms>=3.9.0,<4.0.0',
 'djangocms-bootstrap>=1.1.2,<2.0.0',
 'djangocms-page-meta>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'djangocms-themata',
    'version': '0.1.0',
    'description': 'A set of themes for Django CMS projects.',
    'long_description': 'None',
    'author': 'Robert Turnbull',
    'author_email': 'robert.turnbull@unimelb.edu.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
