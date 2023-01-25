# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boardman']

package_data = \
{'': ['*']}

install_requires = \
['adafruit-ampy>=1.1.0,<2.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['boardman = boardman.cli:cli']}

setup_kwargs = {
    'name': 'boardman',
    'version': '0.1.1',
    'description': 'MicroPython deployment tool',
    'long_description': '# boardman\n\nMicroPython deployment tool\n\n\n## Development\n\n```bash\n$ poetry config --local virtualenvs.create false\n$ poetry install\n```\n\n```bash\n$ poetry config repositories.testpypi https://test.pypi.org/legacy/\n$ poetry config pypi-token.testpypi <token>\n\n\n```\n```bash\n$ pip install -U --pre -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ -U "boardman>0.1.0" \n```\n',
    'author': 'Igor Melnyk',
    'author_email': 'liminspace@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/liminspace/boardman',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
