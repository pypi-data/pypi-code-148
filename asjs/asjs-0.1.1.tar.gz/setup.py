# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['asjs']
setup_kwargs = {
    'name': 'asjs',
    'version': '0.1.1',
    'description': 'Python module for implement object with syntax from JavaScript',
    'long_description': '# asjs\n Python module for implement object with syntax from JavaScript\n\nImplementing access to keys by `obj.path.to.your.key` notation as in JavaScript\n\n## Installing\n\n```\npip install asjs\n```\n\nor like this:\n\n```\ncurl https://github.com/tankalxat34/pyasjs/raw/main/asjs.py -o asjs.py\n```\n\n## Using\n\nRecommended import statement:\n\n```py\nfrom asjs import ObjectNotation\n```\n\n### Creating new object\n\nUsing dictionary:\n\n```py\nobj = ObjectNotation({"key1": "value1", "key2": "value2", "key3": {"a": "b", "lst": [14, 5, 6, 12]}})\n```\n\nUsing arguments:\n\n```py\nobj = ObjectNotation(key1="value1", key2="value2", key3={"a": "b", "lst": [14, 5, 6, 12]})\n```\n### Getting values by keys or indexes\n    >>> obj[0]\n    value1\n    >>> obj.key2\n    value2\n    >>> obj["key3"]\n    [14, 5, 6, 12]\n\n### Creating new keys in object\n```py\nobj.year = 2023\n```\n\nor:\n\n```py\n>>> obj.set("year", 2023)\n```\n\nor:\n\n```py\n>>> year = 2023\n>>> obj.set(year)\n```\n\nor:\n\n```py\n>>> obj["year"] = 2023\n```\n### Saving functions in object\n```py\n>>> obj.fibonachi = lambda n: 1 if n <= 2 else obj.fibonachi(n - 1) + obj.fibonachi(n - 2)\n\n>>> obj.fibonachi(7)\n13\n```\n\n### Removing keys by string-names or indexes\n    >>> del obj.year\n\nor:\n    \n    >>> del obj[-1]\n\nor:\n\n    >>> del obj["year"]\n\n### Changing value by key\n    >>> obj.key1 = 123\n\nor:\n\n    >>> obj["key1"] = 123\n\n### Cycle `for` by object\n\nIndexes:\n```py\n>>> for i in range(len(obj)):\n...     print(i)\n0\n1\n2\n```\n\nKeys:\n```py\n>>> for k in obj:\n...     print(k)\nkey1\nkey2\nkey3\nfibonachi\n```\n\nValues:\n```py\n>>> for v in obj.values():\n...     print(v)\n123\nvalue2\nJSObject(a: \'b\', lst: JSObject(0: 14, 1: 5, 2: 6, 3: 12))\n<function <lambda> at 0x0000020189F19480>\n```\n\n### Boolean statements\n```py\n>>> "key3" in obj\nTrue\n>>> "fake_key" in obj\nFalse\n```',
    'author': 'Alexander Podstrechnyy',
    'author_email': 'tankalxat34@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tankalxat34/asjs',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
