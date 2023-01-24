# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['firecrest', 'firecrest.cli']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.4.0', 'requests>=2.14.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['firecrest = firecrest.cli_script:main']}

setup_kwargs = {
    'name': 'pyfirecrest',
    'version': '1.3.0',
    'description': 'pyFirecrest is a python wrapper for FirecREST',
    'long_description': '# PyFirecREST\n\nThis is a simple python wrapper for the [FirecREST API](https://github.com/eth-cscs/firecrest).\n\n### How to install\n- Through [PyPI](https://pypi.org/project/pyfirecrest/):\n\n  ```\n  python3 -m pip install pyfirecrest\n  ```\n\n### How to use\nThe full documentation of pyFirecREST is in [this page](https://pyfirecrest.readthedocs.io) but you can get an idea from the following example.\nThis is how you can use the testbuild from the demo environment [here](https://github.com/eth-cscs/firecrest/tree/master/deploy/demo).\nThe configuration corresponds to the account `firecrest-sample`.\n\n```python\nimport firecrest as f7t\n\n# Configuration parameters for the Authorization Object\nclient_id = "firecrest-sample"\nclient_secret = "b391e177-fa50-4987-beaf-e6d33ca93571"\ntoken_uri = "http://localhost:8080/auth/realms/kcrealm/protocol/openid-connect/token"\n\n# Create an authorization object with Client Credentials authorization grant\nkeycloak = f7t.ClientCredentialsAuth(\n    client_id, client_secret, token_uri\n)\n\n# Setup the client for the specific account\nclient = f7t.Firecrest(\n    firecrest_url="http://localhost:8000", authorization=keycloak\n)\n\ntry:\n    parameters = client.parameters()\n    print(f"Firecrest parameters: {parameters}")\nexcept f7t.FirecrestException as e:\n    # When the error comes from the responses to a firecrest request you will get a\n    # `FirecrestException` and from this you can examine the http responses yourself\n    # through the `responses` property\n    print(e)\n    print(e.responses)\nexcept Exception as e:\n    # You might also get regular exceptions in some cases. For example when you are\n    # trying to upload a file that doesn\'t exist in your local filesystem.\n    pass\n```',
    'author': 'CSCS',
    'author_email': 'None',
    'maintainer': 'Eirini Koutsaniti',
    'maintainer_email': 'eirini.koutsaniti@cscs.ch',
    'url': 'https://pyfirecrest.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
