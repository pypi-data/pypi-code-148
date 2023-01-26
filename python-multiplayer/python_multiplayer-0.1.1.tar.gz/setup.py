# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py_mp',
 'py_mp.commands',
 'py_mp.models',
 'py_mp.network',
 'py_mp.network.threaded']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-multiplayer',
    'version': '0.1.1',
    'description': 'Server Client Structure for Python',
    'long_description': '# Python Multiplayer\n\nFramework for Client Server Structure in Python.\nIs intended to be used for multiplayer games in pygame with this Module.\n\n[pygame-multiplayer](https://github.com/BroCodeAT/python-multiplayer)\n\n----\n\n## Planned features\n- [x] Command based Network\n- [ ] Threaded Network\n- [ ] Async Network',
    'author': 'dpfurners',
    'author_email': 'dpfurner@tsn.at',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/BroCodeAT/python-multiplayer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
