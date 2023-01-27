# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['emitter_tools']

package_data = \
{'': ['*']}

install_requires = \
['babichjacob-emitter>=0.1.1,<0.2.0',
 'babichjacob-option-and-result>=0.1.2,<0.2.0',
 'babichjacob-store>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'babichjacob-emitter-tools',
    'version': '0.1.0',
    'description': 'Tools for working with event emitters',
    'long_description': '<h1 align="center">📻 Emitter Tools</h1>\nThis library provides tools for working with event emitters.\n\n## 💻 Installation\n\nThis package is [published to PyPI as `babichjacob-emitter-tools`](https://pypi.org/project/babichjacob-emitter-tools/).\n\n## 🛠 Usage\n\nThe various functions this library provides are (mostly) documented individually (see their docstrings).\n\n## 😵 Help! I have a question\n\nCreate an issue and I\'ll try to help.\n\n## 😡 Fix! There is something that needs improvement\n\nCreate an issue or pull request and I\'ll try to fix.\n\n## 📄 License\n\nMIT\n\n## 🙏 Attribution\n\n_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_\n',
    'author': 'J or Jacob Babich',
    'author_email': 'jacobbabichpublic+git@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/babichjacob/python-emitter-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
