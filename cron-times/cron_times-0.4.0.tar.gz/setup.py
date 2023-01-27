# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cron_times', 'cron_times.providers']

package_data = \
{'': ['*'], 'cron_times': ['static/*', 'templates/*']}

install_requires = \
['croniter>=1.3.8,<2.0.0',
 'flask>=2.2.2,<3.0.0',
 'markdown2>=2.4.6,<3.0.0',
 'pypugjs>=5.9.12,<6.0.0',
 'ruamel-yaml>=0.17.21,<0.18.0']

extras_require = \
{'cli': ['click>=8.1.3,<9.0.0',
         'colorlog>=6.7.0,<7.0.0',
         'httpx>=0.23.3,<0.24.0',
         'tzlocal>=4.2,<5.0']}

entry_points = \
{'console_scripts': ['cron-times = cron_times.__main__:cli']}

setup_kwargs = {
    'name': 'cron-times',
    'version': '0.4.0',
    'description': 'Show schdueled jobs in a more readable way',
    'long_description': '# Timetable for cronjobs\n\n[![PyPI version](https://img.shields.io/pypi/v/cron-times)](https://pypi.org/project/cron-times/)\n\nShow schdueled jobs in a more readable way.\n\n![screenshot](./screenshot.png)\n\n*features*\n\n* Easy configure - Setup job list in YAML format\n* Timezone supported - Able to configure server timezone and show the time in local time\n* Quick filtering - Allow customized label and quick lookup\n\n\n## Usage\n\n1. Install\n\n   ```bash\n   # basic\n   pip install cron-times\n\n   # with extra features\n   pip install \'cron-times[cli]\'\n   ```\n\n2. Create task definition files\n\n   Task definition are YAML files placed under `tasks/` folder in current working directory.\n\n   An example task:\n\n   ```yaml\n   - name: task name\n     schedule: "0 10 * * *"\n     timezone: Asia/Taipei  # tzdata format; Would use UTC if not provided\n     description: In the description, you *can* use `markdown`\n     labels:\n       - sample-label\n       - another-label\n   ```\n\n   All `*.yaml` files would be loaded on initialization time.\n   We could use scripts to pull the defines from other places before flask started.\n\n3. Run the app for testing\n\n   ```bash\n   flask --app cron_times run\n   ```\n\n### Built-in providers\n\nThis tool comes with few builtin providers. The providers read cronjobs from the following places and build into task definition file:\n\n* `crontab`: Read crontab on local machine\n* `dbt`: Query scheduled jobs from [dbt cloud](https://www.getdbt.com/product/what-is-dbt/). API triggered and manually triggered jobs are discarded.\n\nTo use the provider, you MUST install `cron-times` with `[cli]` option.\n\n```bash\ncron-times get-tasks <source> --help\n```\n\nWe could run these providers before starting the app to refresh the definition files.\n\n### Deploy\n\n[Flask suggests to use a WSGI server for production](https://flask.palletsprojects.com/en/2.2.x/deploying/).\nYou can run the WSGI server app and call the module `cron_times:app` for such usage.\n\nTake [gunicorn](https://gunicorn.org/) as an example:\n\n```bash\ngunicorn --bind 0.0.0.0:8000 --workers 2 cron_times:app\n```\n\n> **Note**\n>\n> This app does not reload task definition after it started.\n> You should restart the app in case task definition is changed.\n',
    'author': 'tzing',
    'author_email': 'tzingshih@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
