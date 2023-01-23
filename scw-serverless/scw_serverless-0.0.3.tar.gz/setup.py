# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scw_serverless',
 'scw_serverless.config',
 'scw_serverless.config.generators',
 'scw_serverless.deploy',
 'scw_serverless.deploy.backends',
 'scw_serverless.deploy.gateway',
 'scw_serverless.triggers',
 'scw_serverless.utils']

package_data = \
{'': ['*'], 'scw_serverless.config': ['templates/*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'scaleway>=0.5.0,<0.6.0']

extras_require = \
{':python_version < "3.11"': ['typing-extensions>=4.4.0,<5.0.0']}

entry_points = \
{'console_scripts': ['scw-serverless = scw_serverless.cli:main']}

setup_kwargs = {
    'name': 'scw-serverless',
    'version': '0.0.3',
    'description': 'Framework for writing serverless APIs in Python, using Scaleway functions and containers.',
    'long_description': '# Serverless API Framework\n\n[![PyPI version](https://badge.fury.io/py/scw-serverless.svg)](https://badge.fury.io/py/scw-serverless)\n[![Documentation Status](https://readthedocs.org/projects/serverless-api-project/badge/?version=latest)](https://serverless-api-project.readthedocs.io/en/latest/?badge=latest)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/scaleway/serverless-api-project/main.svg)](https://results.pre-commit.ci/latest/github/scaleway/serverless-api-project/main)\n\nServerless API Framework is a tool that lets you write and deploy serverless functions in python.\nIt bridges your code with the deployment configuration to make it a breeze to work with serverless functions.\n\nStarts by defining a simple Python function:\n\n```python\nfrom scw_serverless import Serverless\n\napp = Serverless("hello-namespace")\n\n@app.func(memory_limit=256)\ndef hello_world(event, context):\n    return "Hello World!"\n```\n\nDeploy it with `scw-serverless`:\n\n```console\nscw-serverless deploy app.py\n```\n\n## Quickstart\n\n### Install\n\n```console\npip install scw-serverless\n```\n\nThis will install the `scw-serverless` CLI:\n\n```console\nscw-serverless --help\n```\n\n### Writing and configuring functions\n\nYou can transform your python functions into serverless functions by using decorators:\n\n```python\nimport os\nimport requests\nfrom scw_serverless import Serverless\n\napp = Serverless("hello-namespace")\nAPI_URL = os.environ["API_URL"]\n\n@app.func(memory_limit=256, env={"API_URL": API_URL})\ndef hello_world(event, context):\n    return requests.get(API_URL)\n```\n\nThe configuration is done by passing arguments to the decorator.\nTo view which arguments are supported, head over to this [documentation](https://serverless-api-project.readthedocs.io/) page.\n\nWhen you are ready, you can deploy your function with the `scw-serverless` CLI tool:\n\n```console\nscw-serverless deploy app.py\n```\n\nThe tool will use your Scaleway credentials from your environment and config file.\n\n## What’s Next?\n\nTo learn more about the framework, have a look at the [documentation](https://serverless-api-project.readthedocs.io/).\nIf you want to see it in action, we provide some [examples](https://github.com/scaleway/serverless-api-project/tree/main/examples) to get you started.\n\n## Contributing\n\nWe welcome all contributions.\n\nThis project uses [pre-commit](https://pre-commit.com/) hooks to run code quality checks locally. We recommended installing them before contributing.\n\n```console\npre-commit install\n```\n',
    'author': 'Scaleway Serverless Team',
    'author_email': 'opensource@scaleway.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/scaleway/serverless-api-project',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
