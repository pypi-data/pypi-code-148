# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrateye']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0',
 'opencv-python>=4.7.0.68,<5.0.0.0',
 'pythonnet>=3.0.1,<4.0.0']

setup_kwargs = {
    'name': 'pyrateye',
    'version': '0.0.1',
    'description': 'RatEye ported to Python',
    'long_description': '# RatEye ported to Python\n\nThis is a port of the RatEye project to Python. The original project is written in C# and can be found [here](https://github.com/RatScanner/RatEye).\n\n## Installation\n\n`pip install pyrateye`\n\n## Usage\n\n```python\nfrom pyrateye import RatEye\n# TBD\n```\n\n## Development\n\n### Setup\n\nClone and install the project:\n\n```bash\ngit clone https://github.com/marmig0404/pyrateye.git\ncd pyrateye\npoetry install --with dev\n```\n\nInstall RatEye C# project:\n\n```bash\ngit clone https://github.com/RatScanner/RatEye.git\ncd RatEye\nmsbuild .\\RatEye.csproj /property:Configuration=Release\n```\n',
    'author': 'Martin Miglio',
    'author_email': 'marmig0404@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
