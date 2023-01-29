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
    'version': '0.0.1',
    'description': 'CLI for your python projects',
    'long_description': '# ans-pycli\n',
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
