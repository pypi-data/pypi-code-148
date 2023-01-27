# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compact_json_qt_gui']

package_data = \
{'': ['*']}

install_requires = \
['PySide6>=6.4.2,<7.0.0', 'compact-json>=1.5.0,<2.0.0']

entry_points = \
{'console_scripts': ['compact-json-qt-gui = compact_json_qt_gui.__main__:main']}

setup_kwargs = {
    'name': 'compact-json-qt-gui',
    'version': '0.1.0',
    'description': 'Qt GUI for JSON formatting with compact-json',
    'long_description': None,
    'author': 'Martin Ueding',
    'author_email': 'mu@martin-ueding.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
