# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['docker']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.6,<0.5.0', 'psutil>=5.9.4,<6.0.0', 'typefit>=0.4.2,<0.5.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1,<3.0.0']}

entry_points = \
{'console_scripts': ['modelw-docker = model_w.docker.__main__:__main__']}

setup_kwargs = {
    'name': 'modelw-docker',
    'version': '2023.1.0b4',
    'description': 'Utility to simplify Dockerfiles',
    'long_description': '# Model W Docker\n\nA tool so that your Dockerfile looks like this:\n\n```Dockerfile\nFROM modelw/base:2023.01\n\nCOPY --chown=user package.json package-lock.json ./\n\nRUN modelw-docker install\n\nCOPY --chown=user . .\n\nRUN modelw-docker build\n\nCMD ["modelw-docker", "serve"]\n```\n\n## Organization\n\nThis repository contains different elements that work together, found in\nsub-directories here:\n\n-   `src` &mdash; Contains the source of the `modelw-docker` package, that is\n    published on Pypi.\n-   `image` &mdash; Is the source for the Docker image that can be used as a\n    base for all Model&nbsp;W projects.\n-   `demo` &mdash; A demo project used to test the image during development\n\n## `modelw-docker`\n\nThis is a helper that is pre-installed in the Docker image and helps you build\nand run a Model&nbsp;W project.\n\nIf called from the root of a project, it will automatically detect the project\'s\ntype and run appropriate commands for each step of the build. If later on the\nway the Docker image is built or the requirements of Model&nbsp;W change, it is\nexpected that those changes can be reflected in the `modelw-docker` package\nwithout requiring the developers to change their Dockerfiles.\n\n### Available actions\n\n-   `modelw-docker install` &mdash; Installs the project\'s dependencies (creates\n    the virtualenv, runs `npm install` or whatever is required). It only\n    requires the dependencies files to run (`package.json`/`package-lock.json`\n    for front components, `pyproject.toml`/`poetry.lock` for api components).\n-   `modelw-docker build` &mdash; Builds the project. It requires the project to\n    be installed first. It also requires all the source code to be present.\n-   `modelw-docker serve` &mdash; Runs the project. It requires the project to\n    be installed and built first.\n-   `modelw-docker run` &mdash; Runs a command in the project\'s virtualenv. It\n    requires the project to be installed first.\n\nThe reason why `install` and `build` are separate and why you need first to copy\njust the dependencies list and then the source code is to allow for caching of\nthe dependencies. This way, the dependencies are only re-installed when the\ndependencies list changes, not when the source code changes. This makes very\nfast builds when only the source code changes.\n\n### Dry run\n\nThere is a `--dry-run` option for all the commands that will just print what\nwould have been done but not do it. The dry run mode is automatically enabled if\nyou run the package outside of Docker in order to avoid fucking up your desktop.\n\n### Config file\n\nAll the settings are automatically detected, however if something isn\'t to your\ntaste you can always override it using a `model-w.toml` file, following this\nstructure:\n\n```toml\n[project]\n# For printing purposes\nname = "demo_project"\n# Either "front" or "api"\ncomponent = "api"\n\n[project.required_files]\n# All the files to be created before the install step and their content\n"src/demo_project/__init__.py" = ""\n\n[apt.repos]\n# APT repositories to be added, you need to give both the source and the key\n# for each one of them\npgdg.source = "deb http://apt.postgresql.org/pub/repos/apt/ bullseye-pgdg main"\npgdg.key = { url = "https://www.postgresql.org/media/keys/ACCC4CF8.asc" }\n\n[apt.packages]\n# APT packages to be installed. Put * to install the default version, or a\n# version number to install a specific version.\ngdal-bin = "*"\n```\n\nIn addition, Python project also have the following settings:\n\n```toml\n[project]\n# [...]\n# Either "gunicorn" or "daphne"\nserver = "daphne"\n\n# Modules that have the WSGI and ASGI entry points\nwsgi = "demo_project.django.wsgi:application"\nasgi = "demo_project.django.asgi:application"\n```\n\n## Contribution\n\nThe Docker image and the package are auto-built and published on Docker Hub and\nPypi respectively. The build is triggered by pushing a tag to the repository\n(for the Python package) and for each branch\'s head (for the Docker image).\n\nIf you want to make a release, the Makefile will help you:\n\n```bash\nmake release VERSION=2022.10.0\n```\n\nThis will use Git Flow to make the release, and then also make sure to update\nthe version in the Dockerfile and the `modelw-docker` package.\n\nOnce this is done, you have to:\n\n-   Push the tag to the repository\n-   Push develop and master\n-   Make sure you update support branches accordingly (this cannot be automated\n    it\'s a human decision)\n\n> **Note** &mdash; If you\'re releasing a new major version of Model&nbsp;W, you\n> need to update the `image/Dockerfile` to match the new "upper" version limit.\n> This script will only update the "lower" version limit, to make sure the image\n> is built with the package you just released.\n',
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@hyperthese.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ModelW/docker/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
