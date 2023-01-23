# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypomod']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pomodoro = pypomod.main:main']}

setup_kwargs = {
    'name': 'pypomod',
    'version': '0.0.1',
    'description': 'Simple Python CLI package for Pomodoro timer.',
    'long_description': '# Pypomod\n\nA simple python CLI package for the pomodoro timer.\n\n> Currently, only works on macOS\n\n## Installation\n\n```bash\npip install pypomod\n```\n\n## Use case\n\n### Demo\n\n![screenshot](./assets/screenshot.png)\n\n### Options\n\n```bash\npomodoro -h\n\nusage: pympod [-h] [-w WORK_TIME] [-b BREAK_TIME] [-r REPEAT]\n\nA simple python CLI package for the pomodoro timer.\n\noptions:\n  -h, --help            show this help message and exit\n  -w WORK_TIME, --work_time WORK_TIME\n                        Set the work time. Default is 20 minutes.\n  -b BREAK_TIME, --break_time BREAK_TIME\n                        Set the break time. Default is 5 minutes.\n  -r REPEAT, --repeat REPEAT\n                        Set the number of repeats. Default is 1.\n```\n\n## Known issue\n\n- [ ] Remaining time is not updated by a second.\n- [ ] Linux and Windows are not fully supported yet.\n',
    'author': 'Kyoungseoun Chung',
    'author_email': 'kyoungseoun.chung@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
