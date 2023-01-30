# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rivertils']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-translate==3.9.0']

setup_kwargs = {
    'name': 'rivertils',
    'version': '0.1.8',
    'description': 'utilities commonly used by rivers cuomo',
    'long_description': "To publish to PyPi you have to pass the creds for pypi\n- increment the version number in pyproject.toml\n- poetry build\n- poetry publish --username(not email) --password\n\n# Rivertils\nScripts that are imported by packages you've deployed to pypi",
    'author': 'Rivers Cuomo',
    'author_email': 'riverscuomo@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
