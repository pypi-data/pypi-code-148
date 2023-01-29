# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pollingstream']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'pollingstream',
    'version': '0.1.0',
    'description': 'A polling-based websocket alternative (used for applications where only polling can be used).',
    'long_description': '# PollingStream\nIm gonna do this later im lazy xdddzs\n',
    'author': 'BadPythonCoder',
    'author_email': 'no@email.foru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
