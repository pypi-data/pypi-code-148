# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['obsidian_metadata',
 'obsidian_metadata._config',
 'obsidian_metadata._utils',
 'obsidian_metadata.models']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'questionary>=1.10.0,<2.0.0',
 'rich>=13.2.0,<14.0.0',
 'ruamel-yaml>=0.17.21,<0.18.0',
 'shellingham>=1.4.0,<2.0.0',
 'tomlkit>=0.11.6,<0.12.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['obsidian-metadata = obsidian_metadata.cli:app']}

setup_kwargs = {
    'name': 'obsidian-metadata',
    'version': '0.2.0',
    'description': 'Make batch updates to Obsidian metadata',
    'long_description': '[![Python Code Checker](https://github.com/natelandau/obsidian-metadata/actions/workflows/python-code-checker.yml/badge.svg)](https://github.com/natelandau/obsidian-metadata/actions/workflows/python-code-checker.yml) [![codecov](https://codecov.io/gh/natelandau/obsidian-metadata/branch/main/graph/badge.svg?token=3F2R43SSX4)](https://codecov.io/gh/natelandau/obsidian-metadata)\n# obsidian-metadata\nA script to make batch updates to metadata in an Obsidian vault.  Provides the following capabilities:\n\n- `in-text tag`: delete every occurrence\n- `in-text tags`: Rename tag (`#tag1` -> `#tag2`)\n- `frontmatter`: Delete a key matching a regex pattern and all associated values\n- `frontmatter`: Rename a key\n- `frontmatter`: Delete a value matching a regex pattern from a specified key\n- `frontmatter`: Rename a value from a specified key\n- `inline metadata`: Delete a key matching a regex pattern and all associated values\n- `inline metadata`: Rename a key\n- `inline metadata`: Delete a value matching a regex pattern from a specified key\n- `inline metadata`: Rename a value from a specified key\n- `vault`: Create a backup of the Obsidian vault\n\n\n## Install\n`obsidian-metadata` requires Python v3.10 or above.\n\n```bash\npip install obsidian-metadata\n```\n\n\n## Important Disclaimer\n**It is strongly recommended that you back up your vault prior to committing changes.** This script makes changes directly to the markdown files in your vault. Once the changes are committed, there is no ability to recreate the original information unless you have a backup.  Follow the instructions in the script to create a backup of your vault if needed.  The author of this script is not responsible for any data loss that may occur. Use at your own risk.\n\n## Usage\nThe script provides a menu of available actions. Make as many changes as you require and review them as you go.  No changes are made to the Vault until they are explicitly committed.\n\n[![asciicast](https://asciinema.org/a/553464.svg)](https://asciinema.org/a/553464)\n\n\n### Configuration\n`obsidian-metadata` requires a configuration file at `~/.obsidian_metadata.toml`.  On first run, this file will be created.  You can specify a new location for the configuration file with the `--config-file` option.\n\nTo add additional vaults, copy the default section and add the appropriate information. The script will prompt you to select a vault if multiple exist in the configuration file\n\nBelow is an example with two vaults.\n\n```toml\n["Vault One"] # Name of the vault.\n\n    # Path to your obsidian vault\n    path = "/path/to/vault"\n\n    # Folders within the vault to ignore when indexing metadata\n    exclude_paths = [".git", ".obsidian"]\n\n["Vault Two"]\n    path = "/path/to/second_vault"\n    exclude_paths = [".git", ".obsidian"]\n```\n\nTo bypass the configuration file and specify a vault to use at runtime use the `--vault-path` option.\n\n\n# Contributing\n\n## Setup: Once per project\n\nThere are two ways to contribute to this project.\n\n### 1. Containerized development (Recommended)\n\n1. Clone this repository. `git clone https://github.com/natelandau/obsidian-metadata`\n2. Open the repository in Visual Studio Code\n3. Start the [Dev Container](https://code.visualstudio.com/docs/remote/containers). Run <kbd>Ctrl/⌘</kbd> + <kbd>⇧</kbd> + <kbd>P</kbd> → _Remote-Containers: Reopen in Container_.\n4. Run `poetry env info -p` to find the PATH to the Python interpreter if needed by VSCode.\n\n### 2. Local development\n\n1. Install Python 3.10 and [Poetry](https://python-poetry.org)\n2. Clone this repository. `git clone https://github.com/natelandau/obsidian-metadata`\n3. Install the Poetry environment with `poetry install`.\n4. Activate your Poetry environment with `poetry shell`.\n5. Install the pre-commit hooks with `pre-commit install --install-hooks`.\n\n## Developing\n\n-   This project follows the [Conventional Commits](https://www.conventionalcommits.org/) standard to automate [Semantic Versioning](https://semver.org/) and [Keep A Changelog](https://keepachangelog.com/) with [Commitizen](https://github.com/commitizen-tools/commitizen).\n    -   When you\'re ready to commit changes run `cz c`\n-   Run `poe` from within the development environment to print a list of [Poe the Poet](https://github.com/nat-n/poethepoet) tasks available to run on this project. Common commands:\n    -   `poe lint` runs all linters\n    -   `poe test` runs all tests with Pytest\n-   Run `poetry add {package}` from within the development environment to install a run time dependency and add it to `pyproject.toml` and `poetry.lock`.\n-   Run `poetry remove {package}` from within the development environment to uninstall a run time dependency and remove it from `pyproject.toml` and `poetry.lock`.\n-   Run `poetry update` from within the development environment to upgrade all dependencies to the latest versions allowed by `pyproject.toml`.\n',
    'author': 'Nate Landau',
    'author_email': 'github@natenate.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/natelandau/obsidian-metadata',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
