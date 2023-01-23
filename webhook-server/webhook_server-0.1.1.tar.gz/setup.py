# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webhook_server']

package_data = \
{'': ['*']}

install_requires = \
['Flask-BasicAuth>=0.2.0,<0.3.0',
 'Flask-HTTPAuth>=4.7.0,<5.0.0',
 'Flask>=2.2.2,<3.0.0']

setup_kwargs = {
    'name': 'webhook-server',
    'version': '0.1.1',
    'description': 'Create a webhook server with Flask to forward Datadog alerts to Telegram',
    'long_description': '# Datadog to Telegram webhook\nProvides a basic authenticated webhook to forward alerts from Datadog to Telegram\n## Requirements\n- A Datadog account\n- A Telegram account\n\n### Quickstart\n#### Datadog\nTODO\n#### Telegram\nTODO\n#### Webhook server\nTODO\n\n### Documentation\n\n### Contribute\nOpen to any PR/comments/issues\n\n## Licence\nCopyright 2023 DaisukiXCI\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n',
    'author': 'daisukixci',
    'author_email': 'daisuki@tuxtrooper.com',
    'maintainer': 'daisukixci',
    'maintainer_email': 'daisuki@tuxtrooper.com',
    'url': 'https://gitlab.com/daisukixci/webhook_server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
