# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'binarylane': 'lib/binarylane',
 'binarylane.api': 'lib/binarylane/api',
 'binarylane.api.accounts': 'lib/binarylane/api/accounts',
 'binarylane.api.actions': 'lib/binarylane/api/actions',
 'binarylane.api.customers': 'lib/binarylane/api/customers',
 'binarylane.api.data_usages': 'lib/binarylane/api/data_usages',
 'binarylane.api.domains': 'lib/binarylane/api/domains',
 'binarylane.api.failover_ips': 'lib/binarylane/api/failover_ips',
 'binarylane.api.images': 'lib/binarylane/api/images',
 'binarylane.api.keys': 'lib/binarylane/api/keys',
 'binarylane.api.load_balancers': 'lib/binarylane/api/load_balancers',
 'binarylane.api.regions': 'lib/binarylane/api/regions',
 'binarylane.api.reverse_names': 'lib/binarylane/api/reverse_names',
 'binarylane.api.sample_sets': 'lib/binarylane/api/sample_sets',
 'binarylane.api.server_actions': 'lib/binarylane/api/server_actions',
 'binarylane.api.servers': 'lib/binarylane/api/servers',
 'binarylane.api.sizes': 'lib/binarylane/api/sizes',
 'binarylane.api.software': 'lib/binarylane/api/software',
 'binarylane.api.vpcs': 'lib/binarylane/api/vpcs',
 'binarylane.models': 'lib/binarylane/models'}

packages = \
['binarylane',
 'binarylane.api',
 'binarylane.api.accounts',
 'binarylane.api.actions',
 'binarylane.api.customers',
 'binarylane.api.data_usages',
 'binarylane.api.domains',
 'binarylane.api.failover_ips',
 'binarylane.api.images',
 'binarylane.api.keys',
 'binarylane.api.load_balancers',
 'binarylane.api.regions',
 'binarylane.api.reverse_names',
 'binarylane.api.sample_sets',
 'binarylane.api.server_actions',
 'binarylane.api.servers',
 'binarylane.api.sizes',
 'binarylane.api.software',
 'binarylane.api.vpcs',
 'binarylane.console',
 'binarylane.console.app',
 'binarylane.console.commands',
 'binarylane.console.commands.accounts',
 'binarylane.console.commands.actions',
 'binarylane.console.commands.customers',
 'binarylane.console.commands.data_usages',
 'binarylane.console.commands.domains',
 'binarylane.console.commands.failover_ips',
 'binarylane.console.commands.images',
 'binarylane.console.commands.keys',
 'binarylane.console.commands.load_balancers',
 'binarylane.console.commands.regions',
 'binarylane.console.commands.reverse_names',
 'binarylane.console.commands.sample_sets',
 'binarylane.console.commands.server_actions',
 'binarylane.console.commands.servers',
 'binarylane.console.commands.sizes',
 'binarylane.console.commands.software',
 'binarylane.console.commands.vpcs',
 'binarylane.console.parser',
 'binarylane.console.printers',
 'binarylane.console.runners',
 'binarylane.models',
 'binarylane.pycompat']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.2.0,<23.0.0',
 'httpx>=0.23.0,<0.24.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'terminaltables>=3.1.10,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['backports.cached-property>=1.0.2,<2.0.0',
                             'typing-extensions>=4.0.0,<5.0.0']}

entry_points = \
{'console_scripts': ['bl = binarylane.console.app:main']}

setup_kwargs = {
    'name': 'binarylane-cli',
    'version': '0.11.1',
    'description': '',
    'long_description': '# python-blcli\n',
    'author': "Nathan O'Sullivan",
    'author_email': 'nathan.osullivan@mammoth.com.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
