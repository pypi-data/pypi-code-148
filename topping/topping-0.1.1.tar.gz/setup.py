# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['topping']

package_data = \
{'': ['*']}

install_requires = \
['rich>=13.2.0,<14.0.0']

setup_kwargs = {
    'name': 'topping',
    'version': '0.1.1',
    'description': 'Topping is a Python library for tracking function data.',
    'long_description': '# Topping\n\n##### Topping is a Python library for tracking function data.  \n\n<br/>\n<br/>\n\n## Installation\n\n\n```\npip install topping\n```\n\n<br/>\n<br/>\n\n## Usage\n\n### Add `@topping` decorator to the function you want to track.\n\n<br/>\n\n![example1](https://user-images.githubusercontent.com/123562684/215257570-9c53ed47-dfcc-4d56-b98d-af8ed2b3d035.png)\n\n<br/>\n<br/>\n\n### The output will be something like:\n\n<br/>\n\n<img width="1200" alt="example1_result" src="https://user-images.githubusercontent.com/123562684/215257227-e607af35-2ffa-4c85-a4b8-1832da8301da.png">\n\n<br/>\n<br/>\n<br/>\n<br/>\n<br/>\n<br/>\n\n### Topping also helps when error occurs\n<br/>\n\n![example3](https://user-images.githubusercontent.com/123562684/215257524-f985af60-990d-410f-903d-33ea9618c454.png)\n<br/>\n<br/>\n\n<img width="1200" alt="example3_result" src="https://user-images.githubusercontent.com/123562684/215257529-5849abd2-6b72-4b79-8b72-4742dd00af52.png">\n\n\n<br/>\n<br/>\n\n\n## License\n\n\nMIT LISENCE\n',
    'author': 'jenz',
    'author_email': '2025.jenz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
