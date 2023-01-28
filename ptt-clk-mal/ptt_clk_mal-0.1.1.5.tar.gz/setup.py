# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ptt_clk_mal']

package_data = \
{'': ['*'], 'ptt_clk_mal': ['static/*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'rich>=13.0.0,<14.0.0']

entry_points = \
{'console_scripts': ['pttClk = ptt_clk_mal.pc_parser:cli']}

setup_kwargs = {
    'name': 'ptt-clk-mal',
    'version': '0.1.1.5',
    'description': 'A small timer help make your time used better,inspired by tomatoclock.',
    'long_description': '# MALoPotatoClock\n\n*It\'s my first time to write a python package.*\n\n## Overview\n\n> A simple potato clock inspired by tomato clock.\n> > sadly, I don\'t have a potato, so I use a scheduled timer instead.\n>\n> It\'s a simple timer that helps you to focus on your work.\n\n- [x] A simple timer\n- [x] A simple CLI\n- [x] A simple notification (for Linux only)\n- [ ] A simple GUI\n- [ ] A simple notification for Windows\n- [ ] Recurring schedule with rests like tomato clock\n\n## Usage\n\n### Install\n\n#### from PyPI\n\n```bash\npip install mal-potato-clock\n```\n\n#### from release\n\n```bash\npip install mal-potato-clock-<release>.tar.gz\n```\n\n#### from source (using poetry only)\n\n```bash\ngit clone <url>\ncd mal-potato-clock\npoetry install\n```\n\n### Run\n\n#### Run the timer\n\n```bash\npttClk -t <time> -n <notification intervals> -a <aiming things>\n```\n#### history\n\n```bash\npttClk his -q <last x days> -g <aim group>\n```\n\n#### setting\n\nYou should type below for more information.\n> All commands above\'s help(-h) information are also available.\n```bash\npttClk set -h \n```\n#### Example\n\n```bash\npttClk -t 25 -n 5 -a "study"\npttClk his -q 7 -g "study"\npttClk -s # show setting\n```\n\n### Images\n\n![example Overview](./asserts/eg0.png)\n',
    'author': 'MALossov',
    'author_email': 'lshy1104@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
