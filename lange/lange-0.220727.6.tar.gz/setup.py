# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lange', 'lange.abs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lange',
    'version': '0.220727.6',
    'description': 'Haskell-like intervals for Python',
    'long_description': '![test](https://github.com/davips/lange/workflows/test/badge.svg)\n[![codecov](https://codecov.io/gh/davips/lange/branch/main/graph/badge.svg)](https://codecov.io/gh/davips/lange)\n<a href="https://pypi.org/project/lange">\n<img src="https://img.shields.io/github/v/release/lange/lange?display_name=tag&sort=semver&color=blue" alt="github">\n</a>\n![Python version](https://img.shields.io/badge/python-3.8%20%7C%203.10-blue.svg)\n[![license: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n\n<!--- [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5501845.svg)](https://doi.org/10.5281/zenodo.5501845) --->\n[![arXiv](https://img.shields.io/badge/arXiv-2109.06028-b31b1b.svg?style=flat-square)](https://arxiv.org/abs/2109.06028)\n[![API documentation](https://img.shields.io/badge/doc-API%20%28auto%29-a0a0a0.svg)](https://davips.github.io/lange)\n\n# lange\nLazy lists (i.e. Haskell-like ranges) for Python.\n\n## Installation\n### from package\n```bash\n# Set up a virtualenv. \npython3 -m venv venv\nsource venv/bin/activate\n\n# Install from PyPI\npip install lange\n```\n\n### from source\n```bash\ncd my-project\ngit clone https://github.com/davips/lange ../lange\npip install -e ../lange\n```\n\n\n### Features\n * Stable floating-point range generation, e.g.: `0.8 - 0.6 == 0.2` up to 28 digits (customizable).\n * Infinite `[1 2 ...]` or bounded.\n * O(1) access/evaluation `lst[3443]`\n\n\n### Examples\n\n**Arithmetic Progression**\n<details>\n<p>\n\n```python3\n\n# Bounded\nfrom lange import ap\nprint(ap[0.4, 0.8, ..., 2])\n"""\n[0.4 0.8 1.2 1.6 2.0]\n"""\n```\n\n```python3\n\n# Infinite + slicing\nprog = ap[0.4, 0.8, ...]\nprint(prog[:5])\n"""\n[0.4 0.8 1.2 1.6 2.0]\n"""\n```\n\n```python3\n\n# As list\nprint(list(prog[:5]))\n"""\n[0.4, 0.8, 1.2, 1.6, 2.0]\n"""\n```\n\n```python3\n\nprint(prog[:5].l)\n"""\n[0.4, 0.8, 1.2, 1.6, 2.0]\n"""\n```\n\n\n</p>\n</details>\n\n**Geometric Progression**\n<details>\n<p>\n\n```python3\n\n# Bounded\nfrom lange import gp\nprint(gp[0.4, 0.8, ..., 2])\n"""\n[0.4 0.8 1.6]\n"""\n```\n\n```python3\n\n# Infinite + slicing\nprog = gp[0.4, 0.8, ...]\nprint(prog[:5])\n"""\n[0.4 0.8 1.6 3.2 6.4]\n"""\n```\n\n```python3\n\n# As list\nprint(list(prog[:5]))\n"""\n[0.4, 0.8, 1.6, 3.2, 6.4]\n"""\n```\n\n```python3\n\nprint(prog[:5].l)\n"""\n[0.4, 0.8, 1.6, 3.2, 6.4]\n"""\n```\n\n\n</p>\n</details>\n',
    'author': 'davips',
    'author_email': 'dpsabc@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
