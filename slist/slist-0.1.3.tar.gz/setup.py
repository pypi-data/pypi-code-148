# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slist', 'tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'slist',
    'version': '0.1.3',
    'description': 'A typesafe list with more method chaining!',
    'long_description': '# Slist\nThis is a drop in replacement for the built-in mutable python list\n\nBut with more post-fixed methods for chaining in a typesafe manner!!\n\nLeverage the latest mypy features to spot errors during coding.\n\nAll these methods return a new list. They do not mutate the original list.\n\nNot able to convince your colleagues to use immutable functional data structures? I understand.   \nThis library lets you still have the benefits of typesafe chaining methods while letting your colleagues have their mutable lists!\n\n\n\n\n\n[![pypi](https://img.shields.io/pypi/v/slist.svg)](https://pypi.org/project/slist)\n[![python](https://img.shields.io/pypi/pyversions/slist.svg)](https://pypi.org/project/slist)\n[![Build Status](https://github.com/thejaminator/slist/actions/workflows/dev.yml/badge.svg)](https://github.com/thejaminator/slist/actions/workflows/dev.yml)\n\n```\npip install slist\n```\n\n\n* GitHub: <https://github.com/thejaminator/slist>\n\n\n## Quick Start\nEasily spot errors when you call the wrong methods on your sequence with mypy.\n\n```python\nfrom slist import Slist\n\nmany_strings = Slist(["Lucy, Damion, Jon"])  # Slist[str]\nmany_strings.sum()  # Mypy errors with \'Invalid self argument\'. You can\'t sum a sequence of strings!\n\nmany_nums = Slist([1, 1.2])\nassert many_nums.sum() == 2.2  # ok!\n\nclass CannotSortMe:\n    def __init__(self, value: int):\n        self.value: int = value\n\nstuff = Slist([CannotSortMe(value=1), CannotSortMe(value=1)])\nstuff.sort_by(lambda x: x)  # Mypy errors with \'Cannot be "CannotSortMe"\'. There isn\'t a way to sort by the class itself\nstuff.sort_by(lambda x: x.value)  # ok! You can sort by the value\n\nSlist([{"i am a dict": "value"}]).distinct_by(\n    lambda x: x\n)  # Mypy errors with \'Cannot be Dict[str, str]. You can\'t hash a dict itself\n```\n\nSlist provides methods to easily flatten and infer the types of your data.\n```python\nfrom slist import Slist, List\nfrom typing import Optional\n\ntest_optional: Slist[Optional[int]] = Slist([-1, 0, 1]).map(\n    lambda x: x if x >= 0 else None\n)\n# Mypy infers slist[int] correctly\ntest_flattened: Slist[int] = test_optional.flatten_option()\n\n\ntest_nested: Slist[List[str]] = Slist([["bob"], ["dylan", "chan"]])\n# Mypy infers slist[str] correctly\ntest_flattened_str: Slist[str] = test_nested.flatten_list()\n```\n\nThere are plenty more methods to explore!\n```python\nfrom slist import Slist\n\nresult = (\n    Slist([1, 2, 3])\n    .repeat_until_size_or_raise(20)\n    .grouped(2)\n    .map(lambda inner_list: inner_list[0] + inner_list[1] if inner_list.length == 2 else inner_list[0])\n    .flatten_option()\n    .distinct_by(lambda x: x)\n    .map(str)\n    .reversed()\n    .mk_string(sep=",")\n)\nassert result == "5,4,3"\n```\n',
    'author': 'James Chua',
    'author_email': 'chuajamessh@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/thejaminator/slist',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
