# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['service', 'service.ext', 'service.log']

package_data = \
{'': ['*']}

modules = \
['README', '.gitignore', 'pyproject']
install_requires = \
['APScheduler>=3.9.1,<4.0.0',
 'PyJWT>=2.6.0,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'Pygments>=2.12.0,<3.0.0',
 'asgi-lifespan>=1.0.1,<2.0.0',
 'cryptography>=39.0.0,<40.0.0',
 'ddtrace>=1.6.3,<2.0.0',
 'dep-spec==2.3.29',
 'fastapi-utils>=0.2.1,<0.3.0',
 'fire>=0.4.0,<0.5.0',
 'flake8-bandit>=3.0.0,<4.0.0',
 'flake8-docstrings>=1.6.0,<2.0.0',
 'flake8==3.9.0',
 'flakehell>=0.9.0,<0.10.0',
 'httpx>=0.23.0,<0.24.0',
 'logging-json>=0.2.1,<0.3.0',
 'orjson>=3.8.1,<4.0.0',
 'pytest-asyncio>=0.19.0,<0.20.0',
 'pytest-httpx>=0.21.0,<0.22.0',
 'pytest>=7.1.2,<8.0.0',
 'python-i18n>=0.3.9,<0.4.0',
 'requests>=2.28.1,<3.0.0',
 'respx>=0.20.1,<0.21.0',
 'sentry-sdk>=1.9.5,<2.0.0',
 'ujson>=5.5.0,<6.0.0']

setup_kwargs = {
    'name': 'dep-service',
    'version': '2.11.0',
    'description': '',
    'long_description': None,
    'author': 'everhide',
    'author_email': 'i.tolkachnikov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<=3.11',
}


setup(**setup_kwargs)
