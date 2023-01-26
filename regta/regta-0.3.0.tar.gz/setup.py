# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['regta']

package_data = \
{'': ['*'], 'regta': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'regta-period>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['regta = regta.console:main']}

setup_kwargs = {
    'name': 'regta',
    'version': '0.3.0',
    'description': 'Production-ready scheduler with async, multithreading and multiprocessing support.',
    'long_description': '# regta\n\n**Production-ready scheduler with async, multithreading and multiprocessing support for Python.**\n\n[![versions](https://img.shields.io/pypi/pyversions/regta.svg)](https://github.com/SKY-ALIN/regta)\n![Code Quality](https://github.com/SKY-ALIN/regta/actions/workflows/code-quality.yml/badge.svg)\n[![PyPI version](https://badge.fury.io/py/regta.svg)](https://pypi.org/project/regta/)\n[![license](https://img.shields.io/github/license/SKY-ALIN/regta.svg)](https://github.com/SKY-ALIN/regta/blob/main/LICENSE)\n\n### Core Features\n\n- **[Various Job Types](https://regta.alinsky.tech/user_guide/make_jobs)** - Create async, thread-based,\n  or process-based jobs depending on your goals.\n\n\n- **[Flexible Intervals](https://regta.alinsky.tech/user_guide/interval_types)** - Use standard `timedelta`\n  or specially designed `Period` for highly responsible jobs.\n\n\n- **[Multi-Paradigm](https://regta.alinsky.tech/user_guide/oop_style)** - Design OOP styled\n  or functional styled jobs.\n\n\n- **[CLI Interface](https://regta.alinsky.tech/cli_reference)** - Regta provides a CLI tool\n  to start, list and create jobs by template.\n\n\n- **[Professional Logging](https://regta.alinsky.tech/user_guide/logging)** - Redefine standard logger\n  and define your own. ANSI coloring is supported.\n\nYou may discover scheduling alternatives and find the comparison with Regta on \n[regta.alinsky.tech/alternatives](https://regta.alinsky.tech/alternatives)\n\n---\n\n### Installation\nInstall using `pip install regta` or `poetry add regta`.\n\nIf you use python < 3.9, then also install backports: `pip install "backports.zoneinfo[tzdata]"`.\n\nYou can check if Regta was installed correctly with the following command `regta --version`.\n\n### Example\n\nTo write async job just use `@regta.async_job()` decorator.\n\n```python\n# jobs/my_jobs.py\n\nfrom datetime import timedelta\nfrom regta import async_job, Period\n\n\n@async_job(Period().every(10).seconds)\nasync def my_period_based_job():\n    return "1. Hello world! This is just a log message."\n\n\n@async_job(timedelta(seconds=10))\nasync def my_timedelta_based_job():\n    return "2. You may use `timedelta` or `Period` as interval."\n\n\n@async_job(Period().on.sunday.at("18:35").by("Asia/Almaty"))\nasync def my_sunday_job():\n    return "3. `Period` is recommended for highly responsible jobs because it does not accumulate shift."\n```\n\nRead more about various job types \n[here](https://regta.alinsky.tech/user_guide/make_jobs).\n\n### Start Up\n\nTo start jobs use `regta run` command:\n\n```shell\n$ regta run\n> [3] jobs were found.\n> 2023-01-08 18:31:00,005 [jobs.my_jobs:my_period_based_job] [INFO] - 1. Hello world! This is just a log message.\n> 2023-01-08 18:31:05,622 [jobs.my_jobs:my_timedelta_based_job] [INFO] - 2. You may use `timedelta` or `Period` as interval.\n.  .  .\n> 2023-01-08 18:34:50,002 [jobs.my_jobs:my_period_based_job] [INFO] - 1. Hello world! This is just a log message.\n> 2023-01-08 18:34:55,689 [jobs.my_jobs:my_timedelta_based_job] [INFO] - 2. You may use `timedelta` or `Period` as interval.\n> 2023-01-08 18:35:00,001 [jobs.my_jobs:my_sunday_job] [INFO] - 3. `Period` is recommended for highly responsible jobs because it does not accumulate shift.\n.  .  .\n```\n\nRead CLI reference [here](https://regta.alinsky.tech/cli_reference).\n\n---\n\nFull documentation and reference are available on \n[regta.alinsky.tech](https://regta.alinsky.tech)\n',
    'author': 'Vladimir Alinsky',
    'author_email': 'Vladimir@Alinsky.tech',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://regta.alinsky.tech',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
