# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wikicite']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['test_wikicite = tests.test_wikicite:runner',
                     'wikicite = wikicite.wikicite:cite']}

setup_kwargs = {
    'name': 'wikicite',
    'version': '0.1.3',
    'description': 'Create ready-to-use Wikipedia citations from a series of inputs',
    'long_description': "# wikicite\n\n<!-- [![CI](https://img.shields.io/github/workflow/status/rgieseke/cite/CI?style=for-the-badge&label=actions&logo=github&logoColor=white)](https://github.com/rgieseke/wikicite/actions) -->\n\n[![PyPI](https://img.shields.io/pypi/v/wikicite.svg?style=for-the-badge)](https://pypi.org/project/wikicite/)\n\n## Installation\n\n```\npip install wikicite\n```\n\n## Usage\n\nCommand line tool to create ready-to-use Wikipedia citations from a series of inputs.\n\n```\n$ wikicite news bbc -t 'An Important Article' -a Fred Bloggs -d 01062020 -url http://www.bbc.co.uk/an-important-article\n\n<ref name=Bloggs200601>\n{{cite news |last=Bloggs |first=Fred |title=An Important Article |work=[[BBC]] |url=http://www.bbc.co.uk/an-important-article |date=1 June 2020 |access-date=28 January 2023}}\n</ref>\n```\n\nWhere any options are not specified, the user will be prompted to add them, but all except date are optional.\nA note on formatting for certain options:\n\n- Titles `-t` or `--title` should be provided in quotation marks\n- Authors `-a` or `--author` should be provided as `<firstname> <lastname>`. Where multi-part names are needed, quotation marks should be used to identify the parts, e.g. `Lynn 'Faulds Wood'` or `'John Paul' Jones`\n- Dates `-d` or `--date` should be provided in `ddmmyyyy` format\n\nFor a full list of options, see\n\n```\n$ cite --help\n```\n\nFor more details on Wikipedia citations please see [Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Citing_sources)\n",
    'author': 'peaky76',
    'author_email': 'robertjamespeacock@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
