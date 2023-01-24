# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mmgmt']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'boto3>=1.26.54,<2.0.0',
 'botocore>=1.29.54,<2.0.0',
 'certifi>=2022.12.7,<2023.0.0',
 'click>=8.1.3,<9.0.0',
 'jmespath>=1.0.1,<2.0.0',
 'pytest>=7.2.1,<8.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 's3transfer>=0.6.0,<0.7.0',
 'six>=1.16.0,<2.0.0',
 'urllib3>=1.26.14,<2.0.0']

entry_points = \
{'console_scripts': ['cync = common_sync.__main__:cli',
                     'mmgmt = mmgmt.cli:cli']}

setup_kwargs = {
    'name': 'mmgmt',
    'version': '0.4.1',
    'description': '',
    'long_description': '# Media Management Command Line Interface\n\n[![PyPI](https://img.shields.io/pypi/v/mmgmt)](https://pypi.org/project/mmgmt/)\n[![Downloads](https://static.pepy.tech/badge/mmgmt/month)](https://pepy.tech/project/mmgmt)\n[![Supported Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)](https://pypi.org/project/mmgmt/)\n[![Contributors](https://img.shields.io/github/contributors/will-wright-eng/media-mgmt-cli.svg)](https://github.com/will-wright-eng/media-mgmt-cli/graphs/contributors)\n[![Tests](https://github.com/will-wright-eng/media-mgmt-cli/workflows/Test/badge.svg)](https://github.com/will-wright-eng/media-mgmt-cli/actions?query=workflow%3ATest)\n[![Codeball](https://github.com/will-wright-eng/media-mgmt-cli/actions/workflows/codeball.yml/badge.svg)](https://github.com/will-wright-eng/media-mgmt-cli/actions/workflows/codeball.yml)\n\n## Summary\n\n**An intuitive CLI wrapper around boto3 to search and manage media assets**\n\n## Installing Media MGMT CLI & Supported Versions\n\nmmgmt is available on PyPI:\n\n```bash\npython -m pip install mmgmt\n```\n\nMedia Management Command Line Interface officially supports Python 3.8+.\n\n## Supported Features & Usage\n\nFor help, run:\n\n```bash\nmmgmt --help\n```\n\nYou can also use:\n\n```bash\npython -m mmgmt --help\n```\n\nCommands:\n\n```bash\nUsage: mmgmt [OPTIONS] COMMAND [ARGS]...\n\n  A simple CLI to search and manage media assets in S3 and locally. Setup with\n  `mmgmt configure`\n\nOptions:\n  --version   Show the version and exit.\n  -h, --help  Show this message and exit.\n\nCommands:\n  configure   print project configs & set configs manually\n  delete      delete file from cloud storage - TODO -\n  download    download object from cloud storage\n  get-status  get object head from cloud storage\n  hello       test endpoint\n  ls          list files in location (local, s3, or global)\n  search      search files in local directory and cloud storage\n  upload      upload file to cloud storage\n```\n\nWhy not use `awscli`?\n\nYou can, and I do, in tandem with `mmgmt` -- the purpose is to create an additional interface that minimized the lookup/copy/paste process I found myself frequently going through.\n\nAnother use case is for rapid prototyping applications that require an S3 interface.\n\nFor example:\n\n```python\nimport pandas as pd\nimport mmgmt as mmgmt\n\naws = mmgmt.AwsStorageMgmt(project_name="mmgmt")\nobj_list = aws.get_bucket_objs()\n\nres = []\nfor s3_obj in obj_list:\n    res.append(\n      [\n        str(s3_obj.key),\n        str(s3_obj.key.split(\'/\')[0]),\n        s3_obj.last_modified,\n        s3_obj.storage_class,\n        s3_obj.size\n      ]\n    )\n\ndf = pd.DataFrame(res)\ndf.columns = [\n  \'key\',\n  \'group\',\n  \'last_modified\',\n  \'storage_class\',\n  \'size\'\n]\n```\n\n## Development\n\nTo contribute to this tool, first checkout the code:\n\n```bash\ngit clone https://github.com/will-wright-eng/media-mgmt-cli.git\ncd media-mgmt-cli\n```\n\nThen create a new virtual environment:\n\n```bash\npython -m venv venv\nsource venv/bin/activate\n```\n\nNow install the dependencies and test dependencies:\n\n```bash\npip install -e \'.[test]\'\n```\n\nTo run the tests:\n\n```bash\npytest\n```\n\nInstall pre-commit before submitting a PR:\n\n```bash\nbrew install pre-commit\npre-commit install\n```\n\n## References\n\n- [PyPI Package](https://pypi.org/project/mmgmt)\n- Based on cookiecutter template [will-wright-eng/click-app](https://github.com/will-wright-eng/click-app)\n- Rewrite of original project [will-wright-eng/media_mgmt_cli](https://github.com/will-wright-eng/media_mgmt_cli)\n',
    'author': 'Will Wright',
    'author_email': 'willwright@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/will-wright-eng/media-mgmt-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
