# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shell_genie']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.26.1,<0.27.0',
 'pyperclip>=1.8.2,<2.0.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['shell-genie = shell_genie.main:app']}

setup_kwargs = {
    'name': 'shell-genie',
    'version': '0.1.6',
    'description': '',
    'long_description': '# 🧞\u200d♂️ Shell Genie\n\n_Your wishes are my commands._\n\nShell Genie is a command line assistant that helps you to use the command line like a pro.\n',
    'author': 'Dylan Castillo',
    'author_email': 'dylanjcastillo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
