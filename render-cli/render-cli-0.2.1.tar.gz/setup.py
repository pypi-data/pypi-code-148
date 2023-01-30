# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['render_cli', 'render_cli.output']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'nox>=2022.8.7,<2023.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.5.1,<13.0.0']

entry_points = \
{'console_scripts': ['render-cli = render_cli.console:cli']}

setup_kwargs = {
    'name': 'render-cli',
    'version': '0.2.1',
    'description': 'Render CLI - a command line interface for use with Render https://render.com/',
    'long_description': '# render-cli\n\n-------------\n\n[![Tests](https://github.com/mnapoleon/renderctl/workflows/Tests/badge.svg)](https://github.com/mnapoleon/renderctl/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/mnapoleon/render-cli/branch/main/graph/badge.svg)](https://codecov.io/gh/mnapoleon/render-cli)\n[![PyPI](https://img.shields.io/pypi/v/render-cli.svg)](https://pypi.org/project/renderctl/)\n[![Documentation Status](https://readthedocs.org/projects/render-cli/badge/?version=latest)](https://render-cli.readthedocs.io/en/latest/?badge=latest)\n\n---------\n\n\n## Installation\nTo install the renderctl package, run this command in your terminal\n\n    $ pip install renderctl\n\n## Setup\nYou will need to set an environment variable to your Render API key in order to use the cli\n\n    $ export RENDER_TOKEN=<api-token>\n\nThis token can you created in your Render Account Settings -> Api Keys.\n\n\n## Usage\n render-cli usage looks like:\n\nUsage: `cli [OPTIONS] COMMAND [ARGS]...`\n\nA cli to manage your Render services.\n\n### Options:\n\n  `--version  Show the version and exit.`\n\n  `--help     Show this message and exit.`\n\n***\n\n## Commands:\n\n  - **dump-help**     Command to dump all help screen.\n\n  - **find-service**  Finds a Render service by name.\n\n  - **list**          Returns a list of all services associated with your Render account.\n\n  - **list-env**      Fetches list of environment variables of a service.\n\n  - **set-env**       Will set environment variables for the specified service.\n\n***\n### list\n\nUsage: `cli list [OPTIONS]`\n\nReturns a list of all services associated with your Render account.\n\nOptions:\n\n    -v, --verbose  Display full json output from render api call.\n    --help         Show this message and exit.\n\n![list services!](./assets/list_services.gif "list services")\n\n***\n\n### find-service\n\nUsage: `cli find-service [OPTIONS]`\n\nFinds a Render service by name.\n\nReturns information about service if found.\n\nOptions:\n    \n    -sn, --service-name TEXT  Find service by name\n    --help                    Show this message and exit.\n\n![find servicw!](./assets/find_service.gif "find service")\n\n***\n\n### list-env\n\nUsage: `cli list-env [OPTIONS]`\n\n  Fetches list of environment variables of a service.\n\n  Returns and lists the environment variables associated with the passed\n  in service id or service name.  Verbose mode will display json.\n\n\n  Options:\n\n      -sid, --service-id TEXT   Render service id\n      -sn, --service-name TEXT  Render service name\n      -v, --verbose             Display full json output from render api call.\n      --help                    Show this message and exit.\n\n![list env!](./assets/list_env.gif "list env")\n\n***\n\n### set-env\n\nUsage: `cli set-env [OPTIONS]`\n\n  Will set environment variables for the specified service.\n\nOptions:\n\n    -f, --file          TEXT  File to load env vars from\n    -sn, --service-name TEXT  Render service name\n    -u, --update              flag to indicate it env vars should be overwritten or updated\n    --help                    Show this message and exit.\n\n![set_envs!](./assets/set_envs.gif "set envs")\n\n***\n\n#### dump-help\n\nUsage: `cli dump-help [OPTIONS]`\n\n  Command to dump all help screen.\n\n  Options:\n    \n    --help  Show this message and exit.\n    \n***\n\n#### Unsupported Operations at this time\n- Create services with CLI. (https://api-docs.render.com/reference/create-service)\n- Deploy services with CLI.  (https://api-docs.render.com/reference/create-deploy)\n',
    'author': 'michaelnapoloen',
    'author_email': 'michael.napoleon@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mnapoleon/render-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
