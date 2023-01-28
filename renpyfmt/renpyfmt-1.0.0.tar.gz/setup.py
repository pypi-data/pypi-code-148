# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['renpyfmt']

package_data = \
{'': ['*']}

install_requires = \
['mypy-extensions>=0.4.3,<0.5.0',
 'pathspec>=0.11.0,<0.12.0',
 'rich-click>=1.6.1,<2.0.0']

entry_points = \
{'console_scripts': ['renpyfmt = renpyfmt:cli']}

setup_kwargs = {
    'name': 'renpyfmt',
    'version': '1.0.0',
    'description': "A Ren'Py formatter.",
    'long_description': '![](docs/banner.jpg "renpyfmt logo")\n\n# renpyfmt\n\n`renpyfmt` is a source code formatter for Ren\'Py script.\n\nRight now it only supports formatting blocks of Python code contained within Ren\'Py script files, but the intent is to expand this to allow formatting of actual Ren\'Py script as well.\n\nThe contained Python source code is formatted via [black](https://github.com/psf/black).\n\nAll Python related statements are supported:\n- `$` single-line statements\n- `python:` blocks\n- `init python:` blocks\n- `python early:` blocks\n\n<a href="https://unsplash.com/photos/E8Ufcyxz514?utm_source=unsplash&utm_medium=referral&utm_content=creditShareLink">Photo by Milad Fakurian on Unsplash</a>\n',
    'author': 'cobaltcore',
    'author_email': 'cobaltcore@yandex.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
