# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mudder']
setup_kwargs = {
    'name': 'mudder',
    'version': '0.2.0',
    'description': 'Python port of mudderjs',
    'long_description': "# mudder-py\n\nThis library is a port of [fasiha/mudderjs][1] to Python.\n\nFrom the original readme:\n\n> Generate lexicographically-spaced strings between two strings from\n> pre-defined alphabets.\n\n[1]: https://github.com/fasiha/mudderjs\n\n\n## Example\n\nUsage is nearly identical to the original:\n\n```python\nfrom mudder import SymbolTable\n\n\nhex_ = SymbolTable('0123456789abcdef')\nhexstrings = hex_.mudder('ffff', 'fe0f', num_strings=3)\nprint(hexstrings)\n# ['ff8', 'ff', 'fe8']\n```\n",
    'author': 'Patrick Gingras',
    'author_email': '775.pg.12@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fellowinsights/mudder-py',
    'py_modules': modules,
    'python_requires': '>=3.8.1,<4',
}


setup(**setup_kwargs)
