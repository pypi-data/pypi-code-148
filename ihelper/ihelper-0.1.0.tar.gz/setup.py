# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ihelper',
 'ihelper.assets',
 'ihelper.git',
 'ihelper.git.secret',
 'ihelper.git.secret.delete',
 'ihelper.git.secret.set',
 'ihelper.key',
 'ihelper.key._import',
 'ihelper.key.export',
 'ihelper.update']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'ishutils>=0.1.2,<0.2.0',
 'python-slugify>=7.0.0,<8.0.0']

setup_kwargs = {
    'name': 'ihelper',
    'version': '0.1.0',
    'description': 'My Helpers',
    'long_description': '# ihelper\n\nMy Helpers\n',
    'author': 'Qin Li',
    'author_email': 'liblaf@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/liblaf/ihelper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<3.12',
}


setup(**setup_kwargs)
