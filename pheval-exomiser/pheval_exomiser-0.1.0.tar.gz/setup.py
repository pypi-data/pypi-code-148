# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pheval_exomiser']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['pheval-exomiser = pheval_exomiser.cli:main'],
 'pheval.plugins': ['exomiser = pheval_exomiser.runner:ExomiserPhEvalRunner']}

setup_kwargs = {
    'name': 'pheval-exomiser',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Exomiser Runner for PhEval\n\nThis is the Exomiser plugin for PhEval. Highly experimental. Do not use.\n\n## Developers\n\nWarning, the `pheval` library is currently included as a file reference in the toml file.\n\n```\npheval = { path = "/Users/matentzn/ws/pheval" }\n```\n\nThis will change when pheval is published on pypi.\n\n',
    'author': 'Nico Matentzoglu',
    'author_email': 'nicolas.matentzoglu@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
