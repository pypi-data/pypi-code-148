# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['modernenigma']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['src = src.cli:main']}

setup_kwargs = {
    'name': 'modernenigma',
    'version': '0.0.2',
    'description': '',
    'long_description': '# Installation\n\n```\npipx install ModernEnigma\n```\n\n# CLI Usage\n\n```\nUsage: file-template [OPTIONS] KEYWORD FILE1 FILE2\n\n  Replace KEYWORD in FILE1 with the contents of FILE2.\n\nOptions:\n  -i, --inplace   Edit the file in place instead of outputting to stdout.\n  -n, --no-strip  Do not strip FILE2 of leading or trailing blank characters.\n  --help          Show this message and exit.\n```\n\n# Author\n\n* K. Ferry, hobbyist programer & visual designer\n\n# License\n\nAGPLv3+, see LICENSE.txt for more details.\n\n# URLs\n\n* https://pypi.org/project/ModernEnigma/\n* https://github.com/KevinFerryJr/ModernEnigma\n',
    'author': 'K. Ferry',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/KevinFerryJr/ModernEnigma',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
