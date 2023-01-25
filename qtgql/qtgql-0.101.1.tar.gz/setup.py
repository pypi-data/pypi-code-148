# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qtgql',
 'qtgql.codegen',
 'qtgql.codegen.py',
 'qtgql.codegen.py.templates',
 'qtgql.ext',
 'qtgql.gqltransport',
 'qtgql.itemsystem']

package_data = \
{'': ['*']}

install_requires = \
['PySide6>=6.4.2,<7.0.0', 'attrs>=22.2.0,<23.0.0']

extras_require = \
{'codegen': ['graphql-core>=3.2.3,<4.0.0',
             'jinja2>=3.1.2,<4.0.0',
             'typer[all]>=0.7.0,<0.8.0',
             'toml>=0.10.2,<0.11.0']}

entry_points = \
{'console_scripts': ['qtgql = qtgql.codegen.cli:entrypoint']}

setup_kwargs = {
    'name': 'qtgql',
    'version': '0.101.1',
    'description': 'Qt framework for building graphql driven QML applications',
    'long_description': '![qt-graphql.png](assets%2Fqt-graphql.png)\n###  Qt framework for building graphql driven QML applications\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/qtgql?style=for-the-badge)\n![PyPI](https://img.shields.io/pypi/v/qtgql?style=for-the-badge)\n![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/nrbnlulu/qtgql/tests.yml?branch=main&style=for-the-badge)\n![Codecov](https://img.shields.io/codecov/c/github/nrbnlulu/qtgql?style=for-the-badge)\n[![forthebadge](https://forthebadge.com/images/badges/gluten-free.svg)](https://forthebadge.com)\n[![forthebadge](https://forthebadge.com/images/badges/contains-cat-gifs.svg)](https://forthebadge.com)\n\n### Disclaimer\nThis project is currently under development and **it is not** production ready,\nYou can play-around and tell us what is wrong / missing / awesome :smile:.\n\n### Intro\nQt-QML IMO is a big game changer\n- you get native performance\n- UI code is very clear and declarative\n- Easy to customize\n- Easy to learn\n\nOne of the big disadvantages in Qt-QML is that Qt-C++ API is very repititive and hard to maintain\nfor data-driven applications.\n\nalthough it is tempting to just use `relay` or other `JS` graphql lib\nthere is a point where you would suffer from performance issues (:roll_eyes:  react-native).\n\n\n### GraphQL support\nAs I have proggresed with the codebase I realized that I can do better and possibly mimic some\nfeatures of graphql relay at the cost of making this project more opinionated.\nSo I decided to rename it to `qtgql` (previouslly cuter :cat: ).\nSome of the current features:\n - Qt-native graphql-transport-ws network manager (supports subscriptions).\n - generic models that get created from dictionaries (with update, pop, insert implemeanted by default)\n - property classes that are accessible from QML, with dataclasses  syntax (using attrs)\n\n### Future vision\n- Code generation from schema inspection\nIdeally every graphql type would be a `QObject` with `Property` for each field.\n- possibly generate C++ bindings from schema inspection\n- Query only what defined by the user (similar to how relay does this)\n- Auto mutations\n- Subscriptions\n\n[Visit the docs for more info](https://nrbnlulu.github.io/qtgql/)\n',
    'author': 'Nir',
    'author_email': '88795475+nrbnlulu@users.noreply.github.com',
    'maintainer': 'Nir.J Benlulu',
    'maintainer_email': 'nrbnlulu@gmail.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
