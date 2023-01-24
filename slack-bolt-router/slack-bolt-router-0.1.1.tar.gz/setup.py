# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slack_bolt_router']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'slack-bolt-router',
    'version': '0.1.1',
    'description': 'Slack Bolt Router',
    'long_description': '## slack-bolt-router\n\n[![Python Versions](https://badgen.net/pypi/python/slack-bolt-router)](https://pypi.org/project/slack-bolt-router/)\n[![Slack-Bolt Version](https://badgen.net/badge/icon/%5E1.10.0?icon=slack&label=slack-bolt)]()\n[![Release](https://badgen.net/github/release/dmytrohoi/slack-bolt-router)](https://github.com/dmytrohoi/slack-bolt-router/releases)\n[![License](https://badgen.net/github/license/dmytrohoi/slack-bolt-router)](https://github.com/dmytrohoi/slack-bolt-router/blob/master/LICENSE)\n\n### Description\n\nThe slack-bolt-router package it is a helper utility that can collect and add\nroutes for the Slack Application.\n\nCurrent compatible slack-bolt version is __1.10.0__.\n\n_NOTE: This package may be affected by major updates to the Slack-bolt library,\nand may not contain additional routes from a future release._\n\n### Usage\n\nInstall from pip:\n\n``` sh\npython3 -m pip install slack-bolt-router\n```\n\nImport router to file with your handler functions:\n\n```python\nfrom slack_bolt_router import Router\n```\n\nStart to use routers in your bot application:\n```python\nrouter = Router()\n\n@router.register(type="view")\ndef example_submit(ack):\n    ack()\n\nrouter.apply_to(app)\n```\n\n__[Examples of usage](https://github.com/dmytrohoi/slack-bolt-router/blob/master/examples)__\n\n### Contribution\n\n1. Clone repo\n2. Run `poetry install`\n3. Make some changes and commit to new branch\n4. Create pull request and add some information about changes in PR\n5. Add project author to PR Reviewers\n\n### Author\n\n_You can sponsorship this project by links in github repo._\n\nAuthor personal website: https://hoid.dev\n\n(c) Dmytro Hoi <code@dmytrohoi.com>, 2021 | MIT License\n',
    'author': 'Dmytro Hoi',
    'author_email': 'code@dmytrohoi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://dmytrohoi.github.io/slack-bolt-router/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
