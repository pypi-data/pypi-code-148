# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tf2md']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'logging>=0.4.9.6,<0.5.0.0',
 'mdutils>=1.4.0,<2.0.0',
 'python-hcl2>=4.3.0,<5.0.0']

entry_points = \
{'console_scripts': ['tf2md = src.cli.main:cli']}

setup_kwargs = {
    'name': 'tf2md',
    'version': '0.1.0',
    'description': '',
    'long_description': '# TF2MD\nA readme generator for terraform code.\n\n\n# Usage\n\nRun the command and point it to either a variable file or an output file\n\n```\ntf2md gen-docs --file-type output terraform/outputs.tf\n```\n\nPlease note to include the `--file-type` as either `output` or `variable`\n\nRight now it does not work if you have a mixture of variables and outputs in the same file.\n\n\n# Dev Setup\n\n- Setup dev env\n```\npoetry install\n```\n\n- Install pre-commit\n```\npoetry run pre-commit install\n```',
    'author': 'Karl Webster',
    'author_email': '19327709+ktasper@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
