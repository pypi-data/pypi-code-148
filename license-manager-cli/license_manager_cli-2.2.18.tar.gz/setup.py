# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lm_cli', 'lm_cli.subapps']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0',
 'importlib-metadata>=4.2,<5.0',
 'loguru>=0.6.0,<0.7.0',
 'pendulum>=2.1.2,<3.0.0',
 'py-buzz>=3.1.1,<4.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'pyperclip>=1.8.2,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'python-jose>=3.3.0,<4.0.0',
 'rich>=11.2.0,<12.0.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['lm-cli = lm_cli.main:app']}

setup_kwargs = {
    'name': 'license-manager-cli',
    'version': '2.2.18',
    'description': 'License Manager CLI Client',
    'long_description': '====================\n License Manager CLI\n====================\n\nThe License Manager CLI is a client to interact with the License Manager API.\n\nThe resources that can be interacted with are:\n\n- **Configurations:** information about the license, its features and the location of the license server.\n- **Licenses:** Information about license usage and availability.\n- **Bookings:** Information about licenses booked for future use.\n\nThe Bookings and Licenses information are read only. The Configurations can be edited by users with permission to do so.\n\nUsage\n-----\n\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| **Command**                                                                 | **Description**                                    |   \n+=============================================================================+====================================================+\n| lm-cli login                                                                | Generate a URL for logging in via browser          |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli show-token                                                           | Print your access token (created after logging in) |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli logout                                                               | Logout and remove your access token                |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli licenses list                                                        | List all licenses                                  |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli licenses list --search <search string>                               | Search licenses with the specified string          |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli licenses list --sort-field <sort field>                              | Sort licenses by the specified field               |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli licenses list --sort-field <sort field> --sort-order ascending       | Sort licenses by the specified order               |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli bookings list                                                        | List all bookings                                  |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli bookings list --search <search string>                               | Search bookings with the specified string          |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli bookings list --sort-field <sort field>                              | Sort bookings by the specified field               |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli bookings list --sort-field <sort field> --sort-order ascending       | Sort bookings by the specified order               |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli configurations list                                                  | List all configurations                            |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli configurations get-one -- id <configuration id>                      | List the configuration with the specified id       |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli configurations list --search <search string>                         | Search configurations with the specified string    |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli configurations list --sort-field <sort field>                        | Sort configurations by the specified field         |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli configurations list --sort-field <sort field> --sort-order ascending | Sort configurations by the specified order         |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli configurations create                                                | Create a new configuration                         |\n| --name <config name>                                                        |                                                    |\n| --product <product name>                                                    |                                                    |\n| --features <features as a string serialized JSON object>                    |                                                    |\n| --license-servers <license servers list>                                    |                                                    |\n| --license-server-type <license server type>                                 |                                                    |\n| --grace-time <grace time in seconds>                                        |                                                    |\n| --client-id <cluster identification where the license is configured>        |                                                    |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n| lm-cli configurations delete --id <id to delete>                            | Delete the configuration with the specified id     |\n+-----------------------------------------------------------------------------+----------------------------------------------------+\n\nDevelopment Setup\n-----------------\nTo create a development setup, use ``Poetry`` to create the virtualenv with the dependencies:\n\n.. code-block:: console\n    \n    $ cd lm-cli\n    $ poetry install\n\nAlso create a ``.env`` file with the needed values needed to run the project. These include the License Manager API endpoint and the \nOIDC provider information to retrieve the access token.\n\n.. code-block:: console\n\n    $ cat <<EOF > .env\n    LM_API_ENDPOINT="<API endpoint>"\n    OIDC_DOMAIN="<OIDC domain>"\n    OIDC_AUDIENCE="<OIDC audience>"\n    OIDC_CLIENT_ID="<OIDC client id>"\n    EOF\n\nTo run the tests, use the Makefile:\n\n.. code-block:: console\n\n    $ make test\n\nTo lint and format the code, use the Makefile:\n\n.. code-block:: console\n\n    $ make format\n\nLicense\n-------\n* `MIT <LICENSE>`_\n\n\nCopyright\n---------\n* Copyright (c) 2022 OmniVector Solutions <info@omnivector.solutions>\n',
    'author': 'Omnivector Solutions',
    'author_email': 'info@omnivector.solutions',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/omnivector-solutions/license-manager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
