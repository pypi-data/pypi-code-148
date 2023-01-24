# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dash',
 'dash.categories',
 'dash.categories.migrations',
 'dash.dashblocks',
 'dash.dashblocks.migrations',
 'dash.dashblocks.templatetags',
 'dash.orgs',
 'dash.orgs.management',
 'dash.orgs.management.commands',
 'dash.orgs.migrations',
 'dash.orgs.templatetags',
 'dash.stories',
 'dash.stories.migrations',
 'dash.tags',
 'dash.tags.migrations',
 'dash.users',
 'dash.utils',
 'dash.utils.management',
 'dash.utils.management.commands',
 'dash.utils.templatetags']

package_data = \
{'': ['*'],
 'dash.categories': ['templates/categories/*'],
 'dash.dashblocks': ['static/css/*',
                     'static/css/font/*',
                     'static/js/*',
                     'templates/dashblocks/*'],
 'dash.orgs': ['templates/*', 'templates/orgs/*', 'templates/orgs/email/*'],
 'dash.stories': ['templates/stories/*']}

install_requires = \
['Django>=4.0,<5.0',
 'Pillow>=9.4.0,<10.0.0',
 'celery>=5.1,<6.0',
 'django-compressor>=4.0,<5.0',
 'django-hamlpy>=1.4.4,<2.0.0',
 'django-redis>=5.2.0,<6.0.0',
 'django-timezone-field>=4.1.1,<5.0.0',
 'isort[pyproject]>=5.10.1,<6.0.0',
 'phonenumbers>=8.12.16,<9.0.0',
 'psycopg2-binary>=2.9.1,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'rapidpro-python>=2.9.0,<3.0.0',
 'smartmin>=4.2.1,<5.0.0',
 'sorl-thumbnail>=12.9.0,<13.0.0']

setup_kwargs = {
    'name': 'rapidpro-dash',
    'version': '1.10.2',
    'description': 'Support library for RapidPro dashboards',
    'long_description': 'None',
    'author': 'Nyaruka Ltd',
    'author_email': 'code@nyaruka.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
