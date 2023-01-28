# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airavata_mft_cli', 'airavata_mft_cli.storage']

package_data = \
{'': ['*']}

install_requires = \
['airavata_mft_sdk==0.0.1-alpha21',
 'grpcio-tools>=1.46.3,<2.0.0',
 'grpcio>=1.46.3,<2.0.0',
 'pick==2.2.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['mft = airavata_mft_cli.main:app']}

setup_kwargs = {
    'name': 'airavata-mft-cli',
    'version': '0.1.6',
    'description': 'Command Line Client for Airavata MFT data transfer software',
    'long_description': '<!--\nLicensed to the Apache Software Foundation (ASF) under one\nor more contributor license agreements.  See the NOTICE file\ndistributed with this work for additional information\nregarding copyright ownership.  The ASF licenses this file\nto you under the Apache License, Version 2.0 (the\n"License"); you may not use this file except in compliance\nwith the License.  You may obtain a copy of the License at\n\n  http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing,\nsoftware distributed under the License is distributed on an\n"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\nKIND, either express or implied.  See the License for the\nspecific language governing permissions and limitations\nunder the License.\n-->\n\n# Airavata MFT Command Line Client',
    'author': 'Apache Airavata',
    'author_email': 'dev@apache.airavata.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
