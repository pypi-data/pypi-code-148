# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lm_agent',
 'lm_agent.parsing',
 'lm_agent.server_interfaces',
 'lm_agent.workload_managers',
 'lm_agent.workload_managers.slurm']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.4.0,<3.0.0',
 'boto3>=1.18.17,<2.0.0',
 'httpx>=0.18.2,<0.19.0',
 'py-buzz>=2.1.3,<3.0.0',
 'pydantic[dotenv]>=1.8.2,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'sentry-sdk>=1.3.1,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['reconcile = lm_agent.reconcile:main',
                     'slurmctld-epilog = '
                     'lm_agent.workload_managers.slurm.slurmctld_epilog:main',
                     'slurmctld-prolog = '
                     'lm_agent.workload_managers.slurm.slurmctld_prolog:main']}

setup_kwargs = {
    'name': 'license-manager-agent',
    'version': '2.2.18',
    'description': 'Provides an agent for interacting with license manager',
    'long_description': '# License-manager Agent',
    'author': 'OmniVector Solutions',
    'author_email': 'info@omnivector.solutions',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/omnivector-solutions/license-manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
