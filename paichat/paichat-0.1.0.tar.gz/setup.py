# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paichat']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'colorama>=0.4.6,<0.5.0',
 'rich>=13.2.0,<14.0.0',
 'shellingham>=1.5.0.post1,<2.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['paichat = paichat.main:app']}

setup_kwargs = {
    'name': 'paichat',
    'version': '0.1.0',
    'description': 'A Terminal experience',
    'long_description': '# paichat\n\n\n## Contribute\n\nStart a virtualenv using poetry: `poetry shell`\n\nIf `poetry shell` does not activate the virtualenv, then use this:\n`source $(poetry env info --path)/bin/activate`\n\n',
    'author': 'Kumar Anirudha',
    'author_email': 'mail@anirudha.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
