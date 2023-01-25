# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flet']

package_data = \
{'': ['*']}

install_requires = \
['flet-core==0.4.0.dev1106']

setup_kwargs = {
    'name': 'flet-pyodide',
    'version': '0.4.0.dev1106',
    'description': 'Flet for Pyodide',
    'long_description': '# Flet for Pyodide\n\nRun standalone Flet apps in a browser!',
    'author': 'Appveyor Systems Inc.',
    'author_email': 'hello@flet.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
