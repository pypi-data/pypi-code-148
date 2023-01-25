# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pre_commit_hooks']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['poetry-to-requirements = '
                     'pre_commit_hooks.poetry_to_requirements:main']}

setup_kwargs = {
    'name': 'poetry-to-requirements',
    'version': '1.0.0',
    'description': 'Pre-commit hook to convert Poetry dependancies to pip requirements.txt.',
    'long_description': "# Pre-commit hooks\n\n## Poetry to Pip requirements\n\nThis pre-commit hook can be used to generate a (`requirements`)[https://pip.pypa.io/en/stable/user_guide/#requirements-files] file for pip from Poetry's dependency list.\n\n### General Usage\n\nIn each of your repos, add a file called .pre-commit-config.yaml with the following contents:\n\n```yaml\nrepos:\n  - repo: https://github.com/christopherpickering/pre-commit-hooks\n    rev: <VERSION> # Get the latest from: https://github.com/christopherpickering/pre-commit-hooks/releases\n    hooks:\n      - id: poetry-to-requirements\n        args: [--dev,--output=subfolder/requirements.txt]\n\n```\n\n### Arguments\n\n -  --dev: include dev requirements. Default= False\n -  --output=folder/requirements.txt: output file name. Default= requirements.txt. This path should be relative to the --input path.\n -  (optional) --input=path/to/project_root: path to the project root. Default= .\n",
    'author': 'Christopher Pickering',
    'author_email': 'christopher@going.bg',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/christopherpickering/pre-commit-hooks.git',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
