# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modernrpc', 'modernrpc.auth', 'modernrpc.conf', 'modernrpc.handlers']

package_data = \
{'': ['*'],
 'modernrpc': ['templates/modernrpc/bootstrap4/*',
               'templates/modernrpc/default/*']}

install_requires = \
['django>=2.1']

extras_require = \
{'docutils': ['docutils'], 'markdown': ['markdown']}

setup_kwargs = {
    'name': 'django-modern-rpc',
    'version': '1.0.1',
    'description': 'Simple and powerful RPC server for your Django project',
    'long_description': '# django-modern-rpc\n\n[![Downloads](https://static.pepy.tech/personalized-badge/django-modern-rpc?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)](https://pepy.tech/project/django-modern-rpc)\n[![Tests](https://github.com/alorence/django-modern-rpc/actions/workflows/default.yml/badge.svg)](https://github.com/alorence/django-modern-rpc/actions/workflows/default.yml)\n[![Documentation Status](https://readthedocs.org/projects/django-modern-rpc/badge/?version=latest)](https://django-modern-rpc.readthedocs.io/en/latest/?badge=main)\n[![Link to demo](https://img.shields.io/badge/demo-online-informational.svg)](https://modernrpc.onrender.com)\n\nExpose global python functions through XML-RPC and/or JSON-RPC server using Django toolbox.\n\n## Main features\n\n- XML-RPC and JSON-RPC 2.0 support (JSON-RPC 1.0 is NOT supported)\n- HTTP Basic Auth & custom authentication methods\n- Multiple entry-points: group your RPC methods under different paths to apply\nspecific rules, authentication, protocol support, etc.\n- API docs generation (based on docstring)\n\n## Requirements\n\nThe following Django / Python version are supported, according to Django requirements (see\n[here](https://docs.djangoproject.com/fr/2.2/faq/install/#faq-python-version-support) and\n[here](https://docs.djangoproject.com/fr/4.1/faq/install/#faq-python-version-support))\n\n| 🠗 Django \\ Python 🠖 | 3.5 | 3.6 | 3.7 | 3.8 | 3.9 | 3.10 | 3.11 |\n|---------------------|:---:|:---:|:---:|:---:|:---:|:----:|:----:|\n| 2.1                 | ✔️️  | ✔️️  | ✔️️  | ❌  | ❌  |  ❌  |  ❌  |\n| 2.2                 | ✔️️  | ✔️️  | ✔️️  | ✔️️  | ✔️️  |  ❌  |  ❌  |\n| 3.0                 | ❌  | ✔️️  | ✔️️  | ✔️️  | ✔️️  |  ❌  |  ❌  |\n| 3.1                 | ❌  | ✔️️  | ✔️️  | ✔️️  | ✔️️  |  ❌  |  ❌  |\n| 3.2                 | ❌  | ✔️️  | ✔️️  | ✔️️  | ✔️️  |  ✔️️  |  ❌  |\n| 4.0                 | ❌  | ❌  | ❌  | ✔️️  | ✔️️  |  ✔️️  |  ❌  |\n| 4.1                 | ❌  | ❌  | ❌  | ✔️️  | ✔️️  |  ✔️️  |  ✔️️  |\n\n## Setup\n\nA [quick start](https://django-modern-rpc.readthedocs.io/en/latest/basics/quickstart.html) is available as part\nof the documentation to help setting up you project.\n\n## Code quality\n\nContinuous integration and code analysis is performed automatically to ensure a decent code quality. Project health\nis publicly available on following apps:\n\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/37607e2ecaf549b890fc6defca88c7f8)](https://www.codacy.com/gh/alorence/django-modern-rpc/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=alorence/django-modern-rpc&amp;utm_campaign=Badge_Grade)\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/37607e2ecaf549b890fc6defca88c7f8)](https://www.codacy.com/gh/alorence/django-modern-rpc/dashboard?utm_source=github.com&utm_medium=referral&utm_content=alorence/django-modern-rpc&utm_campaign=Badge_Coverage)\n[![Coveralls Status](https://coveralls.io/repos/github/alorence/django-modern-rpc/badge.svg)](https://coveralls.io/github/alorence/django-modern-rpc)\n',
    'author': 'Antoine Lorence',
    'author_email': 'antoine.lorence@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alorence/django-modern-rpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
