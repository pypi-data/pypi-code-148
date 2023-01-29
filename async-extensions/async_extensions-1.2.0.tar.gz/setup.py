# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_extensions']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.6.2', 'solus>=1.1.0']

setup_kwargs = {
    'name': 'async-extensions',
    'version': '1.2.0',
    'description': 'Asynchronous extensions.',
    'long_description': '# `async-extensions`\n\n[![License][License Badge]][License]\n[![Version][Version Badge]][Package]\n[![Downloads][Downloads Badge]][Package]\n[![Discord][Discord Badge]][Discord]\n[![Check][Check Badge]][Actions]\n\n> *Asynchronous extensions.*\n\n## Installing\n\n**Python 3.7 or above is required.**\n\n### pip\n\nInstalling the library with `pip` is quite simple:\n\n```console\n$ pip install async-extensions\n```\n\nAlternatively, the library can be installed from source:\n\n```console\n$ git clone https://github.com/nekitdev/async-extensions.git\n$ cd async-extensions\n$ python -m pip install .\n```\n\n### poetry\n\nYou can add `async-extensions` as a dependency with the following command:\n\n```console\n$ poetry add async-extensions\n```\n\nOr by directly specifying it in the configuration like so:\n\n```toml\n[tool.poetry.dependencies]\nasync-extensions = "^1.2.0"\n```\n\nAlternatively, you can add it directly from the source:\n\n```toml\n[tool.poetry.dependencies.async-extensions]\ngit = "https://github.com/nekitdev/async-extensions.git"\n```\n\n## Support\n\nIf you need support with the library, you can send an [email][Email]\nor refer to the official [Discord server][Discord].\n\n## Changelog\n\nYou can find the changelog [here][Changelog].\n\n## Security Policy\n\nYou can find the Security Policy of `async-extensions` [here][Security].\n\n## Contributing\n\nIf you are interested in contributing to `async-extensions`, make sure to take a look at the\n[Contributing Guide][Contributing Guide], as well as the [Code of Conduct][Code of Conduct].\n\n## License\n\n`async-extensions` is licensed under the MIT License terms. See [License][License] for details.\n\n[Email]: mailto:support@nekit.dev\n\n[Discord]: https://nekit.dev/discord\n\n[Actions]: https://github.com/nekitdev/async-extensions/actions\n\n[Changelog]: https://github.com/nekitdev/async-extensions/blob/main/CHANGELOG.md\n[Code of Conduct]: https://github.com/nekitdev/async-extensions/blob/main/CODE_OF_CONDUCT.md\n[Contributing Guide]: https://github.com/nekitdev/async-extensions/blob/main/CONTRIBUTING.md\n[Security]: https://github.com/nekitdev/async-extensions/blob/main/SECURITY.md\n\n[License]: https://github.com/nekitdev/async-extensions/blob/main/LICENSE\n\n[Package]: https://pypi.org/project/async-extensions\n\n[Discord Badge]: https://img.shields.io/badge/chat-discord-5865f2\n[License Badge]: https://img.shields.io/pypi/l/async-extensions\n[Version Badge]: https://img.shields.io/pypi/v/async-extensions\n[Downloads Badge]: https://img.shields.io/pypi/dm/async-extensions\n[Check Badge]: https://github.com/nekitdev/async-extensions/workflows/check/badge.svg\n',
    'author': 'nekitdev',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nekitdev/async-extensions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
