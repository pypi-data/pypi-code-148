# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['emitter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'babichjacob-emitter',
    'version': '0.1.1',
    'description': 'An event emitter',
    'long_description': '<h1 align="center">📻 Emitter</h1>\n\nThis library provides the emitter data type.\nAn emitter calls listening handlers whenever an event is emitted. This allows the separation of sourcing an event and reacting to it.\n\n## 💻 Installation\n\nThis package is [published to PyPI as `babichjacob-emitter`](https://pypi.org/project/babichjacob-emitter/).\n\n## 🛠 Usage\n\n```py\nfrom emitter import emittable\n\nmy_emitter = emittable()\nmy_emitter.listen(lambda event: print(f"Received the event {event}"))\nmy_emitter.emit(23) # "Received the event 23" gets printed\n```\n\n## 😵 Help! I have a question\n\nCreate an issue and I\'ll try to help.\n\n## 😡 Fix! There is something that needs improvement\n\nCreate an issue or pull request and I\'ll try to fix.\n\n## 📄 License\n\nMIT\n\n## 🙏 Attribution\n\n_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_\n',
    'author': 'J or Jacob Babich',
    'author_email': 'jacobbabichpublic+git@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/babichjacob/python-emitter',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
