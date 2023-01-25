# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['firecore', 'firecore.torch']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22',
 'rich>=12.6,<14.0',
 'rjsonnet>=0.4.5,<0.6.0',
 'structlog>=22.3.0,<23.0.0']

setup_kwargs = {
    'name': 'firecore',
    'version': '0.5.0',
    'description': '',
    'long_description': '# firecore\n\n[![Github Actions](https://img.shields.io/github/actions/workflow/status/SunDoge/firecore/python-package.yml?branch=main&style=for-the-badge)](https://github.com/SunDoge/firecore/actions/workflows/python-package.yml)\n[![Pypi](https://img.shields.io/pypi/v/firecore?style=for-the-badge)](https://pypi.org/project/firecore/)\n\nYou have to manully install `torch`, `oneflow`.\n',
    'author': 'SunDoge',
    'author_email': '384813529@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
