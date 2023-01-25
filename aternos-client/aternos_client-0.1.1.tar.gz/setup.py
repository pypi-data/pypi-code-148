# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aternos']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0',
 'python-aternos>=2.1.3,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['aternos = aternos.main:app']}

setup_kwargs = {
    'name': 'aternos-client',
    'version': '0.1.1',
    'description': 'A simple client to connect on Aternos server',
    'long_description': "# Hi mineguys  👋\n\n\n## 🛠️ Install     \n```bash\npip install aternos\n```\n\n## 🧑🏻\u200d💻 Usage\n```js\naternos start\naternos stop\naternos info\n```\n\n## Contributing\n\nIf you want participate project\n```bash\npoetry install\n```\n\nDepot coming soon\nif you don't have [poetry](https://python-poetry.org/docs/#installation)\n        ",
    'author': 'qrillet',
    'author_email': 'quentin.rillet@externe.covage.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
