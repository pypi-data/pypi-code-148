# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ans_pycli', 'ans_pycli.commands', 'ans_pycli.commands.Dev']

package_data = \
{'': ['*'], 'ans_pycli.commands.Dev': ['stubs/*']}

entry_points = \
{'console_scripts': ['cli = ans_pycli.cli:cli']}

setup_kwargs = {
    'name': 'ans-pycli',
    'version': '0.0.3',
    'description': 'CLI for your python projects',
    'long_description': '# ans-pycli\n\n[![Tests](https://github.com/alxnsmith/ans-pycli/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/alxnsmith/ans-pycli/actions/workflows/tests.yml)\n\nQuickly build CLI for your own python projects with lightweight module\n\n## How to Install\n\n- pip\n\n  ```bash\n  pip install ans-pycli\n  ```\n\n- poetry\n  ```bash\n  poetry add ans-pycli\n  ```\n',
    'author': 'alxnsmith',
    'author_email': 'alx.n.smith@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
