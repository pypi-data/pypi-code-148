# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strangeworks',
 'strangeworks.core',
 'strangeworks.core.client',
 'strangeworks.core.config',
 'strangeworks.core.errors']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.10.0,<23.0.0',
 'gql>=3.4.0,<4.0.0',
 'pyyaml>=5.4.1,<6.0.0',
 'requests-toolbelt>=0.10.1,<0.11.0',
 'requests==2.26.0',
 'tomlkit>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'strangeworks',
    'version': '0.3.1rc1',
    'description': 'Strangeworks Python SDK',
    'long_description': '| ⚠️    | This SDK is currently in pre-release alpha state and subject to change. To get more info or access to test features check out the [Strangeworks Backstage Pass Program](https://strangeworks.com/backstage). |\n|---------------|:------------------------|\n\n# Strangeworks SDK\n\nThe Strangeworks Python SDK grants easy access to the Strangeworks API. For more information on using the SDK check out the [Strangeworks docs](https://docs.strangeworks.com/).',
    'author': 'Strange Devs',
    'author_email': 'hello@strangeworks.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
