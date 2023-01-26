# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['container_mngr', 'container_mngr.components', 'container_mngr.data']

package_data = \
{'': ['*']}

install_requires = \
['docker>=6.0.1,<7.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'textual>=0.5.0,<0.6.0']

extras_require = \
{':sys_platform == "win32"': ['pypiwin32>=223,<224']}

setup_kwargs = {
    'name': 'container-mngr',
    'version': '0.3.0',
    'description': 'Simple console application for managing Docker containers',
    'long_description': '# container_mngr\n',
    'author': 'Stefan Szarek',
    'author_email': 'stefan.szarek@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
