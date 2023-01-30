# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['viburnum', 'viburnum.application', 'viburnum.cli', 'viburnum.deployer']

package_data = \
{'': ['*']}

extras_require = \
{'deployer': ['constructs>=2.51,<3.0',
              'aws-cdk-lib>=2.50.0,<3.0.0',
              'boto3>=1.26.8,<2.0.0',
              'typer[all]>=0.7.0,<0.8.0',
              'aws-cdk.aws-lambda-python-alpha>=2.51.1a0,<3.0.0']}

entry_points = \
{'console_scripts': ['viburnum = viburnum.cli:app']}

setup_kwargs = {
    'name': 'viburnum',
    'version': '0.1.7.dev1',
    'description': "It's abstraction on top of AWS CDK, that helps in building serverless web applications.",
    'long_description': '# Viburnum\n\n**Viburum** - it\'s a small framework built on top of AWS CDK to simplify development and deploying AWS Serverless web applications.\n\n## Installing\n\n### Installing CDK toolkit\n\nViburnum uses [CDK toolkit](https://docs.aws.amazon.com/cdk/v2/guide/cli.html), so first of all you need to install it:\n\n```bash\nnpm install -g aws-cdk  \n```\n\n### Installing Viburnum\n\nPackage consist of two pats `primitives` that help to describe your handlers and resources and `deployer` that will convert primitives into CloudFormation using CDK.\n\n#### Installing only primitives\n\n```bash\npip install viburnum\n```\n\n#### Installing with deployer\n\n```bash\npip install "viburnum[deployer]"\n```\n\nLambda function will require only primitives to work correctly. That\'s why it\'s recommended to add `viburnum` into `requirements.txt` and `viburnum[deployer]` into `requirements-dev.txt`\n\n## Project structure\n\nEach Lambda function handler is represented as folder with `handler.py` inside and other files if required.\n\n**Example** `handler.py`:\n\n```python\nfrom viburnum.application import Request, Response, route\n\n@route("/tests/{id}", methods=["GET"])\ndef get_test(request: Request, test_queue):\n    print(f"Get test: {request.path_params.get(\'id\')}")\n    return Response(200, {})\n```\n\nIn the root folder you need to have `app.py` file with `Application`, this file used by deployer and CDK to determine all related resources.\n\n**Example** `app.py`\n\n```python\nimport aws_cdk as cdk\nfrom viburnum.deployer.builders import AppConstruct\nfrom viburnum.application import Application, Sqs\n\nfrom functions.api.get_test.handler import get_test\n\napp = Application("TestApp")\n# Handlers\napp.add_handler(get_test)\n\ncontext = cdk.App()\nAppConstruct(context, app)\ncontext.synth()\n```\n\nAll logic that shared across all lambdas, must be placed inside `shared` folder, and it will be plugged into Lambda as a Layer.\n\nConfigurations are stored in `config.py` file.\n\n**Example** `config.py`\n\n```python\n# config.py\nfrom viburnum.deployer import Configuration\nfrom aws_cdk import Environment, aws_lambda\n\n\n# DEV CONFIG\nConfiguration(\n    env_name="dev",\n    env=Environment(account="267695621767", region="eu-central-1"),\n    python_version=aws_lambda.Runtime.PYTHON_3_9,\n    ...\n)\n```\n\n### Recommended structure\n\n```project\n├── functions\n│   ├── __init__.py\n│   ├── api\n│   │   ├── __init__.py\n│   │   ├── some_api\n│   │   │    ├── __init__.py\n│   │   │    ├── handler.py\n│   │   │    └── ...\n│   │   │\n│   │   └── ...\n│   │   \n│   ├── jobs\n│   │   ├── __init__.py\n│   │   ├── some_job\n│   │   │    ├── __init__.py\n│   │   │    ├── handler.py\n│   │   │    └── ...\n│   │   │\n│   │   └── ...\n│   │   \n│   └── workers\n│       ├── __init__.py\n│       ├── some_job\n│       │    ├── __init__.py\n│       │    ├── handler.py\n│       │    └── ...\n│       │\n│       └── ...\n│      \n├── shared\n│   ├── __init__.py\n│   └── ...\n│\n├── app.py\n├── config.py\n├── requirements-dev.txt\n└── requirements.txt\n```\n\n### CLI tool\n\nViburnum deployer include CLI tool that helps initializing project and creating a new handlers.\nAfter initializing project folder with `cdk init app --language python` you can call `virburnum init`, that command will change some files so Virburnum can work correctly.\nThere is command for creating new handlers `virburnum add [HANDLER_TYPE]` that will create a handler.\n\nSupported `HANDLER_TYPE`:\n\n- `api`\n- `worker`\n- `job`\n\n## Example app\n\nSimple [example app](https://github.com/yarik2215/Viburnum-example)\n',
    'author': 'Yaroslav Martynenko',
    'author_email': 'stikblacklabel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/yarik2215/Viburnum',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
