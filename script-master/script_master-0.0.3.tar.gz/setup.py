# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['script_master', 'script_master.notebook']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aiopath>=0.6.11,<0.7.0',
 'asyncio>=3.4.3,<4.0.0',
 'better-exceptions>=0.3.3,<0.4.0',
 'confz==1.8.1',
 'fastapi>=0.88,<0.89',
 'jinja2>=3.1.2,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'orjson>=3.8.4,<4.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'script-master-helper>=0.0.1,<0.0.2',
 'typer>=0.7.0,<0.8.0',
 'uvicorn[standart]>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['script-master = script_master.cli:cli']}

setup_kwargs = {
    'name': 'script-master',
    'version': '0.0.3',
    'description': '',
    'long_description': '# Script-Master\n\nСервис, который по конфигам (формат YAML), \nсоздает задания запуска скриптов в сервисе [Process-Executor](https://github.com/pavelmaksimov/process-executor),\nсогласно плану запусков полученных от сервиса [Work-Planner](https://github.com/pavelmaksimov/work-planner).\n\n## Install\n    poetry add script-master\n\nor\n\n    pip install script-master\n\n## Run\n    script-master --help\n    script-master init # Создаст конфиг в текущий директории\n    script-master run # Пользоваться командой, запускать всегда в директории, в которой выполнен init\n\n## Интерфейс\nЕсть [интерфейс](https://github.com/pavelmaksimov/script-master-helper), он не обязателен. Для сервиса требуются только конфиги yaml, их иожно вручную создавать\nЗапускается отдельно/',
    'author': 'Pavel Maksimov',
    'author_email': 'vur21@ya.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pavelmaksimov/script-master',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
