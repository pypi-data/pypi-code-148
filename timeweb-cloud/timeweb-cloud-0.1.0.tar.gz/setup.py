# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['timeweb',
 'timeweb.errors',
 'timeweb.schemas',
 'timeweb.schemas.account',
 'timeweb.sync_api']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0', 'pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'timeweb-cloud',
    'version': '0.1.0',
    'description': 'Timeweb Cloud API wrapper',
    'long_description': '# timeweb-cloud\nAPI Timeweb Cloud позволяет вам управлять ресурсами в облаке программным способом с использованием обычных HTTP-запросов.\n\nМножество функции, которые доступны в панели управления Timeweb Cloud, также доступны через API, что позволяет вам автоматизировать ваши собственные сценарии.\n\nЭта библиотека позволяет вам легко использовать API Timeweb Cloud в вашем приложении на Python.\n\n[Документация API](https://timeweb.cloud/api-docs)',
    'author': 'Maxim Mosin',
    'author_email': 'max@mosin.pw',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LulzLoL231/timeweb-cloud',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
