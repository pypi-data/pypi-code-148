# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tricky']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tricky',
    'version': '0.0.5',
    'description': 'A set of useful features to make working with your code easier.',
    'long_description': "# tricky - that's about python.\n\nThis module is simply a collection of useful code, utilities, and functions to simplify your work with the language and the tasks you solve.\n\n## Collection:\n1. Iterables module `tricky.iterables`\n2. Typing `tricky.typing` (wip)\n\n\n## Examples:\n\n1. `tricky.iterables.filter_item`\n```python\nnumbers = range(1000)\nresult: int = filter_item(\n    numbers,  # the iterable\n    lambda number: number == 342,  # condition to get your item\n    None,  # the default value to return, if condition not met\n)\nprint(result)\n# 342\n```\n",
    'author': 'Alexander Walther',
    'author_email': 'alexander.walther.engineering@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Walther-s-Engineering/tricky',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
