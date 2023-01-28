# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ptt_clk_mal']

package_data = \
{'': ['*'], 'ptt_clk_mal': ['static/pttsets.yaml']}

install_requires = \
['PyYAML>=6.0,<7.0', 'rich>=13.0.0,<14.0.0']

entry_points = \
{'console_scripts': ['pttClk = ptt_clk_mal.pc_parser:cli']}

setup_kwargs = {
    'name': 'ptt-clk-mal',
    'version': '0.1.1.3',
    'description': 'A small script help get your time used better',
    'long_description': '# MALoPotatoClock\n\nThis is a simple clock that uses a potato to tell the time.\n\ntry type `<CMD>` to enjoy your journal.',
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
