# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['faucetconfrpc']

package_data = \
{'': ['*'], 'faucetconfrpc': ['protos/faucetconfrpc/*']}

install_requires = \
['c65faucet==1.0.45',
 'dnspython<2.3.0',
 'grpcio-tools==1.51.1',
 'grpcio==1.51.1',
 'os-ken==2.6.0',
 'prometheus_client==0.16.0',
 'protobuf==4.21.12',
 'pybind11==2.10.3',
 'pyopenssl>22.1.0']

entry_points = \
{'console_scripts': ['faucetconfrpc_client = '
                     'faucetconfrpc.faucetconfrpc_client:main',
                     'faucetconfrpc_server = '
                     'faucetconfrpc.faucetconfrpc_server:serve']}

setup_kwargs = {
    'name': 'faucetconfrpc',
    'version': '0.22.47',
    'description': 'utility to manage FAUCET config files via RPC',
    'long_description': 'None',
    'author': 'Charlie Lewis',
    'author_email': 'clewis@iqt.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
