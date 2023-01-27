# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['platzky',
 'platzky.blog',
 'platzky.db',
 'platzky.plugins.redirections',
 'platzky.plugins.sendmail',
 'platzky.seo']

package_data = \
{'': ['*'], 'platzky': ['static/*', 'templates/*']}

install_requires = \
['Flask-Babel>=2.0.0,<3.0.0',
 'Flask-Minify>=0.39,<0.40',
 'Flask-WTF>=1.0.1,<2.0.0',
 'Flask>=2.2.2,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'aiohttp>=3.8.3,<4.0.0',
 'google-cloud-storage>=2.5.0,<3.0.0',
 'gql>=3.4.0,<4.0.0',
 'humanize>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'platzky',
    'version': '0.1.19',
    'description': 'Another blog in python',
    'long_description': '![Github Actions](https://github.com/platzky/platzky/actions/workflows/tests.yml/badge.svg?event=push&branch=main)\n[![Coverage Status](https://coveralls.io/repos/github/platzky/platzky/badge.svg?branch=main)](https://coveralls.io/github/platzky/platzky?branch=main)\n\n# platzky\n\nBlog engine in python\n\n# How to run?\n\n1. Install platzky with your favorite dependency management tool (`pip install platzky`)\n2. run `flask --app "platzky:create_app(PATH_TO_YOUR_CONFIG_FILE)" run`\n\n## Configuration\n\nFor details check `config.yml.tpl` file.\n\n\n# API\n`platzky.config.from_file(path_to_config)` - creates _platzky_ config from file (see __config.yml.tpl__)\n`platzky.create_app_from_config(config)` - creates _platzky_ application.\n`platzky.sendmail(receiver_email, subject, message)`- sends email from configured account\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
