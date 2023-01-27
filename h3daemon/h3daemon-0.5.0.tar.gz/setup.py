# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['h3daemon']

package_data = \
{'': ['*']}

install_requires = \
['podman>=4.3.0,<5.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['h3d = h3daemon.cli:app']}

setup_kwargs = {
    'name': 'h3daemon',
    'version': '0.5.0',
    'description': 'Run HMMER daemon on containers',
    'long_description': '# h3daemon\n',
    'author': 'Danilo Horta',
    'author_email': 'danilo.horta@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
