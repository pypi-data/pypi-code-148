# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azstream',
 'azstream.authenticators',
 'azstream.authenticators.authenticator',
 'azstream.authenticators.bellmedia_authenticator',
 'azstream.authenticators.bellmedia_external_authenticator',
 'azstream.authenticators.jwt_authenticator',
 'azstream.authenticators.toutv_authenticator',
 'azstream.authenticators.unauthenticated_authenticator',
 'azstream.platforms',
 'azstream.platforms.crave',
 'azstream.platforms.noovo',
 'azstream.platforms.platform',
 'azstream.platforms.toutv',
 'azstream.types',
 'azstream.utils']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.6,<0.5.0',
 'pyjwt==1.7.1',
 'pypasser>=0.0.5,<0.0.6',
 'pytz>=2022.7.1,<2023.0.0',
 'requests>=2.28.2,<3.0.0',
 'schedule>=1.1.0,<2.0.0',
 'thefuzz>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'azstream',
    'version': '0.1.0',
    'description': 'A package to interact with some streaming platform.',
    'long_description': '# AZStream\n\n## Platform specific options\n\nPlatform specific options can be using the `platform_options` arguments when adding a new platform.\n\n### **TOU.TV**\n\n\n|Parameter|Type|Description|Possible values|Required|Default value|\n|---|---|---|---|---|---|\n|android_version|str|The Android version to be used in the requests headers|`8.0.0`, `13`, ...|No|`13`|\n|android_type|str|The Android device type|`phone`, `tv`|No|`phone`|',
    'author': 'Antoine Lombardo',
    'author_email': 'lombardoa@oxoc.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
