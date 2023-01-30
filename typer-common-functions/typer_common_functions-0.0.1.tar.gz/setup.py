# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['typer_common_functions']

package_data = \
{'': ['*']}

install_requires = \
['rich>=13.2.0,<14.0.0', 'typer>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'typer-common-functions',
    'version': '0.0.1',
    'description': 'Commonly used Functions around the Typer CLI Library',
    'long_description': '# Typer Common Functions\n\nSome Helpful Functions around the wonderful CLI Library [Typer](https://typer.tiangolo.com/)\n',
    'author': 'Joshua Kreuder',
    'author_email': 'joshua_kreuder@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/OpenJKSoftware/typer-common-functions',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
