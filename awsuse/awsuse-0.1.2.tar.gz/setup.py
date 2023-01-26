# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awsuse']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.56,<2.0.0', 'click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['awsuse = awsuse.cli:run']}

setup_kwargs = {
    'name': 'awsuse',
    'version': '0.1.2',
    'description': 'CLI to switch the aws cli default profile quickly',
    'long_description': '# awsuse\n\nA CLI tool to easily switch the AWS CLI active `default` profile by changing directly the `~/.aws/config` and the `~/.aws/credentials` file.\n\n## Instalation\npip install awsuse\n\n## Usage\n```\nawsuse --help\nUsage: awsuse [OPTIONS] SOURCE_PROFILE\n\nOptions:\n  --credentials-file PATH     Path to aws cli credentials file\n  --config-file PATH          Path to aws cli config file\n  --token-code TEXT           MFA token code (applicable on MFA based\n                              profiles)\n  --session-duration INTEGER  Session duration in seconds (applicable on MFA\n                              based profiles)\n  --help                      Show this message and exit.\n```\n\n## Supported profile types\n\n* Simple profiles\n* MFA Profiles\n* SSO profiles\n\n\n### Simple profiles\n\nThese are simple profiles that define only the `aws_access_key_id` and `aws_secret_access_key` credentials.\n\nFor these, it just copies the profile values defined in both `credentials` and  `config` file into those files `[default]` section\n\n\n### MFA profiles\n\nThese are profiles that contain the key `mfa_serial` defined in the `config` file. \n\nIt uses the `SOURCE_PROFILE` definition, the token code (`--token-code`) to get a new session token with credentials from AWS STS and writes them into the `[default]` section of the `credentials` file. It also copies the profile configs into the `config` file `[default]` section\n\n\n### SSO profiles\n\nThese are profiles that contain the key `sso_session` defined in the `config` file.\n\nFor these profiles this CLI ony copies the profile `config` settings into the `[default]` section.\n\nIf the specified `sso_session` is expired, this CLI will not try to refresh it automaticaly.',
    'author': 'Andre Lopes',
    'author_email': 'afsalopes@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aflopes/awsuse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
