# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'competitive_verifier_oj_clone': 'src/competitive_verifier_oj_clone',
 'competitive_verifier_oj_clone.languages': 'src/competitive_verifier_oj_clone/languages',
 'competitive_verifier_resources': 'src/competitive_verifier_resources'}

packages = \
['competitive_verifier',
 'competitive_verifier.check',
 'competitive_verifier.console',
 'competitive_verifier.documents',
 'competitive_verifier.download',
 'competitive_verifier.merge_input',
 'competitive_verifier.merge_result',
 'competitive_verifier.migrate',
 'competitive_verifier.models',
 'competitive_verifier.oj_resolve',
 'competitive_verifier.verify',
 'competitive_verifier_oj_clone',
 'competitive_verifier_oj_clone.languages',
 'competitive_verifier_resources']

package_data = \
{'': ['*'],
 'competitive_verifier_resources': ['jekyll/*',
                                    'jekyll/_includes/*',
                                    'jekyll/_includes/highlight/*',
                                    'jekyll/_includes/mathjax/*',
                                    'jekyll/_layouts/*',
                                    'jekyll/assets/css/*',
                                    'jekyll/assets/js/*']}

install_requires = \
['colorama>=0.4.6,<0.5.0',
 'colorlog>=6.7.0,<7.0.0',
 'importlab>=0.8,<0.9',
 'online-judge-tools==11.5.1',
 'pydantic>=1.10.2,<2.0.0',
 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['competitive-verifier = '
                     'competitive_verifier.console.app:main']}

setup_kwargs = {
    'name': 'competitive-verifier',
    'version': '1.4.1',
    'description': 'Verifier for libraries of competitive programming',
    'long_description': '# competitive-verifier\n\n[![Actions Status](https://github.com/competitive-verifier/competitive-verifier/workflows/verify/badge.svg)](https://github.com/competitive-verifier/competitive-verifier/actions) [![GitHub Pages](https://img.shields.io/static/v1?label=GitHub+Pages&message=+&color=brightgreen&logo=github)](https://competitive-verifier.github.io/competitive-verifier)\n[![PyPI](https://img.shields.io/pypi/v/competitive-verifier)](https://pypi.org/project/competitive-verifier/)\n\nThe library is inspired by [online-judge-tools/verification-helper](https://github.com/online-judge-tools/verification-helper).\n\nIf you want more info, see [DESIGN.md](DESIGN.md).\n\n## Get started\n\n### GitHub Actions\n\nSee [GitHub Pages](https://competitive-verifier.github.io/competitive-verifier/installer.html).\n[日本語](https://competitive-verifier.github.io/competitive-verifier/installer.ja.html)\n\n### Install(local)\n\nNeeds Python 3.9 or greater.\n\n```sh\npip install competitive-verifier\n```\n\nOr\n\n```sh\npip install git+https://github.com/competitive-verifier/competitive-verifier.git@latest\n```\n\n#### Migrate from verification-helper\n\nRun this script.\n\n```sh\ncompetitive-verifier migrate\n```\n\n## Development\n\n```sh\npip install -U poetry\npoetry install\n\n# test\npoetry run pytest\n\n# format\npoetry run poe format\n```',
    'author': 'kzrnm',
    'author_email': 'gengesa@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/competitive-verifier/competitive-verifier',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
