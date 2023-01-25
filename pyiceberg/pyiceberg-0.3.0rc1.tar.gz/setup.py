# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'vendor'}

packages = \
['fb303',
 'hive_metastore',
 'pyiceberg',
 'pyiceberg.avro',
 'pyiceberg.avro.codecs',
 'pyiceberg.catalog',
 'pyiceberg.cli',
 'pyiceberg.expressions',
 'pyiceberg.io',
 'pyiceberg.table',
 'pyiceberg.utils',
 'tests',
 'tests.avro',
 'tests.catalog',
 'tests.cli',
 'tests.expressions',
 'tests.io',
 'tests.table',
 'tests.utils']

package_data = \
{'': ['*']}

modules = \
['check-license', 'Makefile', 'NOTICE']
install_requires = \
['click==8.1.3',
 'fsspec==2023.1.0',
 'mmhash3==3.0.1',
 'pydantic==1.10.4',
 'pyparsing==3.0.9',
 'pyyaml==6.0.0',
 'requests==2.28.2',
 'rich==13.2.0',
 'zstandard==0.19.0']

extras_require = \
{'adlfs': ['adlfs==2023.1.0'],
 'duckdb': ['pyarrow==10.0.1', 'duckdb==0.6.1'],
 'glue': ['boto3==1.24.59'],
 'hive': ['thrift==0.16.0'],
 'pandas': ['pyarrow==10.0.1', 'pandas==1.5.3'],
 'pyarrow': ['pyarrow==10.0.1'],
 's3fs': ['s3fs==2023.1.0'],
 'snappy': ['python-snappy==0.6.1']}

entry_points = \
{'console_scripts': ['pyiceberg = pyiceberg.cli.console:run']}

setup_kwargs = {
    'name': 'pyiceberg',
    'version': '0.3.0rc1',
    'description': 'Apache Iceberg is an open table format for huge analytic datasets',
    'long_description': '<!--\n - Licensed to the Apache Software Foundation (ASF) under one or more\n - contributor license agreements.  See the NOTICE file distributed with\n - this work for additional information regarding copyright ownership.\n - The ASF licenses this file to You under the Apache License, Version 2.0\n - (the "License"); you may not use this file except in compliance with\n - the License.  You may obtain a copy of the License at\n -\n -   http://www.apache.org/licenses/LICENSE-2.0\n -\n - Unless required by applicable law or agreed to in writing, software\n - distributed under the License is distributed on an "AS IS" BASIS,\n - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n - See the License for the specific language governing permissions and\n - limitations under the License.\n -->\n\n# Iceberg Python\n\nPyIceberg is a Python library for programmatic access to Iceberg table metadata as well as to table data in Iceberg format. It is a Python implementation of the [Iceberg table spec](https://iceberg.apache.org/spec/).\n\nThe documentation is available at [https://py.iceberg.apache.org/](https://py.iceberg.apache.org/).\n\n# Get in Touch\n\n- [Iceberg community](https://iceberg.apache.org/community/)\n',
    'author': 'Apache Software Foundation',
    'author_email': 'dev@iceberg.apache.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://iceberg.apache.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
