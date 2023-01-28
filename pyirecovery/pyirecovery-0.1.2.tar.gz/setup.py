# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyirecovery']

package_data = \
{'': ['*']}

install_requires = \
['pymobiledevice3>=1.36.2,<2.0.0']

entry_points = \
{'console_scripts': ['pyirecovery = pyirecovery.__main__:main']}

setup_kwargs = {
    'name': 'pyirecovery',
    'version': '0.1.2',
    'description': 'A CLI wrapper of pymobiledevice3 that interacts with Recovery/DFU Apple devices',
    'long_description': '## pyirecovery\nA CLI wrapper of pymobiledevice3 that interacts with Recovery/DFU Apple devices\n# Installation\n* Install with PIP:\n```\npython3 -m pip install pyirecovery\n```\n* Install locally:\n```\ngit clone https://github.com/Mini-Exploit/pyirecovery\ncd pyirecovery\nbash ./install.sh\n```\n# Usage\n* Run `pyirecovery` and see the usage\n\n# Credits\n* [doronz88](https://github.com/doronz88) - [pymobiledevice3](https://github.com/doronz88/pymobiledevice3)\n',
    'author': 'Mini-Exploit',
    'author_email': 'miniexploitttt@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
