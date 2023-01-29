# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['process_executor',
 'process_executor.git_tools',
 'process_executor.venv_tools']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'better-exceptions==0.3.3',
 'confz==1.8.1',
 'fastapi>=0.88,<0.89',
 'loguru>=0.6.0,<0.7.0',
 'orjson>=3.8.4,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'script-master-helper>=0.0.2,<0.0.3',
 'typer>=0.7.0,<0.8.0',
 'uvicorn[standart]>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['process-executor = process_executor.cli:cli',
                     'script-master-executor = process_executor.cli:cli']}

setup_kwargs = {
    'name': 'process-executor',
    'version': '0.0.1',
    'description': '',
    'long_description': '# Python Process Ececutor\n\nЭта микросервис запускающий bash скрипты.\\\nСкрипты беруться только из Git.\\\nСкрипты выполняются в своем виртуальном окружении.\n\nПример конфига для процесса\n```\n{\n  "workplan_id": "821e40ee-d3c9-41da-85d2-d12d5183998a",\n  "name": "1",\n  "command": [\n    "{executable}", "./scripts/yandex_direct_export_to_file.py", "--body_filepath", "./scripts/body-clients.json", "--filepath", "clients.tsv", "--resource", "clients", "--token", ""\n  ],\n  "git": {\n    "url": "https://github.com/pavelmaksimov/tapi-yandex-direct"\n  },\n  "venv": {\n    "version": "3.7",\n    "requirements": [\n      "tapi_yandex_direct"\n    ]\n  },\n  "time_limit": 100,\n  "expires_utc": "2023-01-16T15:15:54.818Z",\n  "save_stdout": false,\n  "save_stderr": true\n}\n```\n\n\n\n\n## Run\nSet environment variable `PROCESS_EXECUTOR_HOME`\n\n    process_executor --help\n    process_executor',
    'author': 'Pavel Maksimov',
    'author_email': 'vur21@ya.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pavelmaksimov/process-executor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
