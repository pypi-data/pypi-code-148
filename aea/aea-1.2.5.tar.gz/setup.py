# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aea',
 'aea.cli',
 'aea.cli.registry',
 'aea.cli.utils',
 'aea.components',
 'aea.configurations',
 'aea.connections',
 'aea.connections.scaffold',
 'aea.context',
 'aea.contracts',
 'aea.contracts.scaffold',
 'aea.crypto',
 'aea.crypto.registries',
 'aea.decision_maker',
 'aea.error_handler',
 'aea.helpers',
 'aea.helpers.acn',
 'aea.helpers.ipfs',
 'aea.helpers.ipfs.pb',
 'aea.helpers.multiaddr',
 'aea.helpers.preference_representations',
 'aea.helpers.search',
 'aea.helpers.storage',
 'aea.helpers.storage.backends',
 'aea.helpers.transaction',
 'aea.identity',
 'aea.mail',
 'aea.manager',
 'aea.protocols',
 'aea.protocols.dialogue',
 'aea.protocols.generator',
 'aea.protocols.scaffold',
 'aea.registries',
 'aea.skills',
 'aea.skills.scaffold',
 'aea.test_tools']

package_data = \
{'': ['*'],
 'aea.configurations': ['schemas/*', 'schemas/configurable_parts/*'],
 'aea.helpers.storage.backends': ['binaries/*']}

install_requires = \
['base58>=1.0.3,<3.0.0',
 'ecdsa>=0.15,<0.17.0',
 'importlib-metadata>4,<5',
 'jsonschema>=3.2.0,<5',
 'packaging>=21.0,<22.0',
 'protobuf>=3.19.4,<4',
 'pymultihash==0.8.2',
 'python-dotenv>=0.14.0,<0.18.0',
 'pyyaml>=4.2b1,<6.0',
 'requests>=2.22.0,<3.0.0',
 'semver>=2.9.1,<3.0.0']

extras_require = \
{':sys_platform == "win32" or platform_system == "Windows"': ['pywin32==303'],
 'all': ['click>=8.0.0,<9.0.0'],
 'cli': ['click>=8.0.0,<9.0.0']}

entry_points = \
{'console_scripts': ['aea = aea.cli:cli']}

setup_kwargs = {
    'name': 'aea',
    'version': '1.2.5',
    'description': 'Autonomous Economic Agent framework',
    'long_description': '<h1 align="center">\n    <b>AEA Framework</b>\n</h1>\n\n<p align="center">\nCreate Autonomous Economic Agents (AEAs)\n</p>\n\n<p align="center">\n  <a href="https://pypi.org/project/aea/">\n    <img alt="PyPI" src="https://img.shields.io/pypi/v/aea">\n  </a>\n  <a href="https://pypi.org/project/aea/">\n    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/aea">\n  </a>\n  <a href="https://github.com/fetchai/agents-aea/blob/main/LICENSE">\n    <img alt="License" src="https://img.shields.io/pypi/l/aea">\n  </a>\n  <a href="https://pypi.org/project/aea/">\n    <img alt="License" src="https://img.shields.io/pypi/dm/aea">\n  </a>\n  <br />\n  <a href="https://github.com/fetchai/agents-aea/workflows/AEA%20framework%20sanity%20checks%20and%20tests">\n    <img alt="AEA framework sanity checks and tests" src="https://github.com/fetchai/agents-aea/workflows/AEA%20framework%20sanity%20checks%20and%20tests/badge.svg?branch=main">\n  </a>\n  <a href="">\n    <img alt="Codecov" src="https://img.shields.io/codecov/c/github/fetchai/agents-aea">\n  </a>\n  <a href="https://discord.gg/hy8SyhNnXf">\n    <img src="https://img.shields.io/discord/441214316524339210.svg?logo=discord&logoColor=fff&label=Discord&color=7389d8" alt="Discord conversation" />\n  </a>\n</p>\n\nThe AEA framework allows you to create **Autonomous Economic Agents**:\n\n- An AEA is an <b>Agent</b>, representing an individual, family, organisation or object (a.k.a. its "owner") in the digital world. It looks after its owner\'s interests and has their preferences in mind when acting on their behalf.\n- AEAs are <b>Autonomous</b>; acting with no, or minimal, interference from their owners.\n- AEAs have a narrow and specific focus: creating <b>Economic</b> value for their owners.\n\n<p align="center">\n  <a href="https://www.youtube.com/embed/xpJA4IT5X88">\n    <img src="/data/video-aea.png?raw=true" alt="AEA Video" width="70%"/>\n  </a>\n</p>\n\n## To install\n\n1. Ensure you have Python (version `3.8`, `3.9` or `3.10`).\n2. (optional) Use a virtual environment (e.g. [`pipenv`][pipenv] or [`poetry`][poetry]).\n3. Install: `pip install aea[all]`\n\nPlease see the [installation page][docs-install] for more details.\n\n## Documentation\n\nThe full documentation, including how to get started, can be found [here][docs].\n\n## Contributing\n\nAll contributions are very welcome! Remember, contribution is not only PRs and code, but any help with docs or helping other developers solve their issues are very appreciated!\n\nRead below to learn how you can take part in the AEA project.\n\n### Code of Conduct\n\nPlease be sure to read and follow our [Code of Conduct][coc]. By participating, you are expected to uphold this code.\n\n### Contribution Guidelines\n\nRead our [contribution guidelines][contributing] to learn about our issue and PR submission processes, coding rules, and more.\n\n### Development Guidelines\n\nRead our [development guidelines][developing] to learn about the development processes and workflows when contributing to different parts of the AEA project.\n\n### Issues, Questions and Discussions\n\nWe use [GitHub Issues][issues] for tracking requests and bugs, and [GitHub Discussions][discussion] for general questions and discussion.\n\n## License\n\nThe AEA project is licensed under [Apache License 2.0][license].\n\n[poetry]: https://python-poetry.org\n[pipenv]: https://pypi.org/project/pipenv/\n[docs]: https://docs.fetch.ai\n[contributing]: https://github.com/fetchai/agents-aea/blob/main/CONTRIBUTING.md\n[developing]: https://github.com/fetchai/agents-aea/blob/main/DEVELOPING.md\n[coc]: https://github.com/fetchai/agents-aea/blob/main/CODE_OF_CONDUCT.md\n[discussion]: https://github.com/fetchai/agents-aea/discussions\n[issues]: https://github.com/fetchai/agents-aea/issues\n[license]: https://github.com/fetchai/agents-aea/blob/main/LICENSE\n[docs-install]: https://docs.fetch.ai/aea/installation/\n',
    'author': 'Fetch.AI Limited',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fetchai/agents-aea',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
