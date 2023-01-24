# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lonedruid']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['int_to_eso = stufftoeso.eso:int_to_eso',
                     'multieso = stufftoeso.eso:multieso',
                     'power_find = stufftoeso.eso:power_find']}

setup_kwargs = {
    'name': 'lonedruid',
    'version': '0.4.7',
    'description': 'Package to convert stuff to esoteric stuff, maybe something else later.',
    'long_description': '---\n\n![Logo][Logo.img]\n\n---\n# **LoneDruid**\n\n## Description:\nPackage with some functions to help you annoy people and mock on the python language.\n\n## Built with:\n---\n[![Poetry][Poetry.img]][Poetry-url]\n\n---\n\n## Getting started:\n\n### Installation:\nPip:\n`pip install LoneDruid`\n\n### Example of usage:\n\nRight now there are only 3 functions:\n\n`power_find(n: int)`\nCan be used to deconstruct an integer into a list of powers of 2 (basically, a binary representation, but with a list)\n\n`int_to_eso(n: int, eso_num: bool, eso_oper: bool)` Converts an integer into a funky representation of itself.\n\n`multieso(nums: list[int], path: str, eso_num: bool, eso_oper: bool)` Basically calls the int_to_eso() function on each element of the list `nums` and constructs a list with those elements inside a file specified in the `path` variable.\n\n```python\nimport LoneDruid\n\nprint(LoneDruid.int_to_eso(42)\n>>> ((-~int().__add__(-~int())).__pow__(-~int())).__add__(((-~int().__add__(-~int())).__pow__(-~int().__add__(-~int()).__add__(-~int())))).__add__(((-~int().__add__(-~int())).__pow__(-~int().__add__(-~int()).__add__(-~int()).__add__(-~int()).__add__(-~int()))))\n```\nVerify:\n```py\nprint(((-~int().__add__(-~int())).__pow__(-~int())).__add__(((-~int().__add__(-~int())).__pow__(-~int().__add__(-~int()).__add__(-~int())))).__add__(((-~int().__add__(-~int())).__pow__(-~int().__add__(-~int()).__add__(-~int()).__add__(-~int()).__add__(-~int())))))\n>>> 42\n```\n\n## Credits:\n\n* [Python discord community](https://discord.gg/python)  (specially **eivl#1134**)\n\n<!-- MARKDOWN LINKS & IMAGES -->\n<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->\n[Poetry.img]: https://johnfraney.ca/blog/images/poetry.png\n[Poetry-url]: https://python-poetry.org/\n[Logo.img]: https://media.discordapp.net/attachments/470884583684964352/1066117775166283897/image.png?width=2000&height=662\n[Logo.url]: https://discord.gg/python   ',
    'author': 'NikitaNightBot',
    'author_email': 'enikita332@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
