# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'empiric',
 'core': 'empiric/core',
 'core.abis': 'empiric/core/abis',
 'core.mixins': 'empiric/core/mixins',
 'publisher': 'empiric/publisher',
 'publisher.fetchers': 'empiric/publisher/fetchers',
 'test': 'empiric/test'}

packages = \
['cli',
 'cli.contracts',
 'cli.publisher',
 'cli.randomness',
 'cli.tests',
 'core',
 'core.abis',
 'core.mixins',
 'empiric',
 'empiric.cli',
 'empiric.cli.contracts',
 'empiric.cli.publisher',
 'empiric.cli.randomness',
 'empiric.cli.tests',
 'empiric.core',
 'empiric.core.abis',
 'empiric.core.mixins',
 'empiric.publisher',
 'empiric.publisher.fetchers',
 'empiric.test',
 'publisher',
 'publisher.fetchers',
 'test']

package_data = \
{'': ['*'], 'cli': ['sample_config/*'], 'empiric.cli': ['sample_config/*']}

install_requires = \
['cairo-lang==0.10.3', 'starknet.py==0.13.0a0', 'typer==0.6.1']

entry_points = \
{'console_scripts': ['empiric = empiric.cli:main',
                     'interface-check = '
                     'empiric.test.interface_consistency:main']}

setup_kwargs = {
    'name': 'empiric-network',
    'version': '1.4.11',
    'description': 'Core package for rollup-native Empiric Network',
    'long_description': "# Empiric Network\n\n## About\n\nFor more information, see the [project's repository](https://github.com/Astraly-Labs/Empiric), [documentation overview](https://docs.empiric.network/) and [documentation on how to publish data](https://docs.empiric.network/using-empiric/publishing-data).\n",
    'author': 'Astraly Labs',
    'author_email': 'contact@astraly.xyz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://empiric.network',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
