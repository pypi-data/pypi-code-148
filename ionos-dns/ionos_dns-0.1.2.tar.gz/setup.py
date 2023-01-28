# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ionos']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.0']

setup_kwargs = {
    'name': 'ionos-dns',
    'version': '0.1.2',
    'description': 'This contains tools to use the IONOS DNS management API and to perform letsencrypt DNS challenges',
    'long_description': '# ionos-dns-python\n\n[![Release](https://img.shields.io/github/v/release/FredStober/ionos-dns-python)](https://img.shields.io/github/v/release/FredStober/ionos-dns-python)\n[![Build status](https://img.shields.io/github/workflow/status/fpgmaas/ionos-dns-python/Main/main)](https://github.com/fpgmaas/ionos-dns-python/actions/workflows/main.yml?query=branch%3Amain)\n[![codecov](https://codecov.io/gh/FredStober/ionos-dns-python/branch/main/graph/badge.svg)](https://codecov.io/gh/FredStober/ionos-dns-python)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/FredStober/ionos-dns-python)](https://img.shields.io/github/commit-activity/m/FredStober/ionos-dns-python)\n[![License](https://img.shields.io/github/license/FredStober/ionos-dns-python)](https://img.shields.io/github/license/FredStober/ionos-dns-python)\n\nThis contains tools to use the IONOS DNS management API in oder to perform letsencrypt DNS challenges\n\n- **Github repository**: <https://github.com/FredStober/ionos-dns-python/>\n- **Documentation** <https://FredStober.github.io/ionos-dns-python/>\n\n## Getting started with your project\n\nFirst, create a repository on GitHub with the same name as this project, and then run the following commands:\n\n``` bash\ngit init -b main\ngit add .\ngit commit -m "init commit"\ngit remote add origin git@github.com:FredStober/ionos-dns-python.git\ngit push -u origin main\n```\n\nFinally, install the environment and the pre-commit hooks with \n\n```bash\nmake install\n```\n\nYou are now ready to start development on your project! The CI/CD\npipeline will be triggered when you open a pull request, merge to main,\nor when you create a new release.\n\nTo finalize the set-up for publishing to PyPi or Artifactory, see\n[here](https://fpgmaas.github.io/cookiecutter-poetry/features/publishing/#set-up-for-pypi).\nFor activating the automatic documentation with MkDocs, see\n[here](https://fpgmaas.github.io/cookiecutter-poetry/features/mkdocs/#enabling-the-documentation-on-github).\nTo enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/codecov/).\n\n## Releasing a new version\n\n- Create an API Token on [Pypi](https://pypi.org/).\n- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting \n[this page](https://github.com/FredStober/ionos-dns-python/settings/secrets/actions/new).\n- Create a [new release](https://github.com/FredStober/ionos-dns-python/releases/new) on Github. \nCreate a new tag in the form ``*.*.*``.\n\nFor more details, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/cicd/#how-to-trigger-a-release).\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).',
    'author': 'Fred Stober',
    'author_email': 'fmail@fredstober.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/FredStober/ionos-dns-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.11',
}


setup(**setup_kwargs)
