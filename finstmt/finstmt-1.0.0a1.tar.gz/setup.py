# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['finstmt',
 'finstmt.bs',
 'finstmt.clean',
 'finstmt.combined',
 'finstmt.config_manage',
 'finstmt.findata',
 'finstmt.forecast',
 'finstmt.forecast.models',
 'finstmt.inc',
 'finstmt.items',
 'finstmt.loaders',
 'finstmt.resolver']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib', 'pandas', 'statsmodels', 'sympy', 'tqdm', 'xlrd']

extras_require = \
{'forecast': ['prophet']}

setup_kwargs = {
    'name': 'finstmt',
    'version': '1.0.0a1',
    'description': 'Contains classes to work with financial statement data. Can calculate free cash flows and help project financial statements.',
    'long_description': "\n\n[![](https://codecov.io/gh/nickderobertis/py-finstmt/branch/master/graph/badge.svg)](https://codecov.io/gh/nickderobertis/py-finstmt)\n[![PyPI](https://img.shields.io/pypi/v/finstmt)](https://pypi.org/project/finstmt/)\n![PyPI - License](https://img.shields.io/pypi/l/finstmt)\n[![Documentation](https://img.shields.io/badge/documentation-pass-green)](https://nickderobertis.github.io/py-finstmt/)\n![Tests Run on Ubuntu Python Versions](https://img.shields.io/badge/Tests%20Ubuntu%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)\n![Tests Run on Macos Python Versions](https://img.shields.io/badge/Tests%20Macos%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)\n![Tests Run on Windows Python Versions](https://img.shields.io/badge/Tests%20Windows%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)\n[![Github Repo](https://img.shields.io/badge/repo-github-informational)](https://github.com/nickderobertis/py-finstmt/)\n\n\n#  py-finstmt\n\n## Overview\n\nContains classes to work with financial statement data. Can calculate free cash flows and help project financial statements.\n\n## Getting Started\n\nInstall `finstmt`:\n\n```\npip install finstmt\n```\n\nA simple example:\n\n```python\nfrom finstmt import BalanceSheets, IncomeStatements, FinancialStatements\nimport pandas as pd\n\nbs_path = r'WMT Balance Sheet.xlsx'\ninc_path = r'WMT Income Statement.xlsx'\nbs_df = pd.read_excel(bs_path)\ninc_df = pd.read_excel(inc_path)\nbs_data = BalanceSheets.from_df(bs_df)\ninc_data = IncomeStatements.from_df(inc_df)\nstmts = FinancialStatements(inc_data, bs_data)\n```\n\nSee a\n[more in-depth tutorial here.](\nhttps://nickderobertis.github.io/py-finstmt/tutorial.html\n)\n\n## Links\n\nSee the\n[documentation here.](\nhttps://nickderobertis.github.io/py-finstmt/\n)\n\n## Development Status\n\nThis project is currently in early-stage development. There may be\nbreaking changes often. While the major version is 0, minor version\nupgrades will often have breaking changes.\n\n## Developing\n\nSee the [development guide](\nhttps://github.com/nickderobertis/py-finstmt/blob/master/DEVELOPING.md\n) for development details.\n\n## Author\n\nCreated by Nick DeRobertis. MIT License.\n\n",
    'author': 'Nick DeRobertis',
    'author_email': 'whoopnip@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
