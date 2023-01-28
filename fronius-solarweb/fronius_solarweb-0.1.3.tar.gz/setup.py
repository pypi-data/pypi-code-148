# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fronius_solarweb', 'fronius_solarweb.schema']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23,<0.24', 'pydantic>=1.10,<2.0', 'tenacity>=8.1,<9.0']

setup_kwargs = {
    'name': 'fronius-solarweb',
    'version': '0.1.3',
    'description': 'A Python wrapper for the Fronius Solar.web Cloud API',
    'long_description': '# Fronius Solar.web\n\nPython client for the Fronius [Solar.web API](https://www.fronius.com/~/downloads/Solar%20Energy/User%20Information/SE_UI_API_InterfaceDocumentation_EN.pdf).\n\n## Features \n\n- Talks to your Fronius Solar.web PV system via Cloud API\n- Automatic retries with exponential backoff\n- Optionally pass in a `httpx` client\n\n## Usage\n\nAlthough intended as a library [`fronius_sw_example.py`](https://github.com/drc38/python-fronius-web/blob/main/examples/fronius_sw_example.py) is provided for testing purposes.\n\nAuthentication and PV system id for the example is provided via environment variables, e.g. on nix systems:\n\n```\nexport ACCESS_KEY_ID=FKIAFEF58CFEFA94486F9C804CF6077A01AB\nexport ACCESS_KEY_VALUE=47c076bc-23e5-4949-37a6-4bcfcf8d21d6\nexport PV_SYSTEM_ID=20bb600e-019b-4e03-9df3-a0a900cda689\n```',
    'author': 'Derek Caudwell',
    'author_email': 'derek_caudwell@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/drc38/python-fronius-web',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
