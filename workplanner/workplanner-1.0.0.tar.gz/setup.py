# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['workplanner']

package_data = \
{'': ['*']}

install_requires = \
['better-exceptions>=0.3.3,<0.4.0',
 'confz==1.8.1',
 'fastapi>=0.88,<0.89',
 'loguru>=0.6.0,<0.7.0',
 'orjson>=3.8.4,<4.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'sqlalchemy>=2.0b,<3.0',
 'typer>=0.7.0,<0.8.0',
 'uvicorn[standart]>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['script-master-workplanner = workplanner.cli:cli',
                     'workplanner = workplanner.cli:cli']}

setup_kwargs = {
    'name': 'workplanner',
    'version': '1.0.0',
    'description': 'Microservice for scheduling tasks by intervals',
    'long_description': '# Microservice for scheduling tasks\n\n## Install\n    poetry add workplanner\n\nor\n\n    pip install workplanner\n\n\n## Run\nSet environment variable `WORKPLANNER_HOME`.\\\nAfter run:\n\n    workplanner run --help\n    workplanner run\n\nDefault port 14444\n\n[Swagger](https://github.com/swagger-api/swagger-ui): \\\nhttp://127.0.0.1:14444/docs\n\n[Redoc](https://github.com/Redocly/redoc): \\\nhttp://127.0.0.1:14444/redoc\n',
    'author': 'Pavel Maksimov',
    'author_email': 'vur21@ya.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pavelmaksimov/work-planner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
