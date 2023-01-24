# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'python', 'protos': 'python/pyfoxtrot/protos'}

packages = \
['protos', 'pyfoxtrot', 'pyfoxtrot.protos']

package_data = \
{'': ['*']}

install_requires = \
['poetry-grpc-plugin>=0.1.2,<0.2.0', 'protobuf<=3.20']

setup_kwargs = {
    'name': 'foxtrotpy',
    'version': '0.3.0a1',
    'description': 'Client for Foxtrot RPC hardware server',
    'long_description': 'None',
    'author': 'Dan Weatherill',
    'author_email': 'daniel.weatherill@physics.ox.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
