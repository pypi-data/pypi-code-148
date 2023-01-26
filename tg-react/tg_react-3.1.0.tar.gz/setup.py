# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tg_react', 'tg_react.api', 'tg_react.api.accounts']

package_data = \
{'': ['*'],
 'tg_react': ['locale/en/LC_MESSAGES/*',
              'locale/en_US/LC_MESSAGES/*',
              'locale/et/LC_MESSAGES/*',
              'locale/ru/LC_MESSAGES/*',
              'templates/tg_react_emails/*']}

install_requires = \
['django>=2.2,<4.2', 'djangorestframework>=3.9.2']

setup_kwargs = {
    'name': 'tg-react',
    'version': '3.1.0',
    'description': 'Helpers for react based applications running on django.',
    'long_description': '# tg-react\n\n![https://badge.fury.io/py/tg-react](https://badge.fury.io/py/tg-react.png)\n![Workflow status](https://github.com/thorgate/tg-react/actions/workflows/python-package.yml/badge.svg?branch=master)\n\nHelpers for react based applications running on django.\n\n## Documentation\n\nThe full documentation is at https://tg-react.readthedocs.org.\n\n## Quickstart\n\nInstall tg-react:\n\n```\npip install tg-react\n```\n\nThen use it in a project:\n\n```\nimport tg_react\n```\n\n## Features\n\n* TODO\n\n.. TODO: List features and link to documentation for more information\n\n## Changelog\n\nChanges are documented under `Github Releases <https://github.com/thorgate/tg-react/releases>`_.\n',
    'author': 'Thorgate',
    'author_email': 'code@thorgate.eu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/thorgate/tg-react',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
