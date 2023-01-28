# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wind_parser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wind-parser',
    'version': '0.1.3',
    'description': 'Python wind parser is a parser used to retrieve arguments for command line interfaces and turn them into python dictionary',
    'long_description': "# Wind Parser \n![Python versions badge](https://img.shields.io/pypi/pyversions/wind-parser) [![Python package](https://github.com/anthonyraf/wind-parser/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/anthonyraf/wind-parser/actions/workflows/python-package.yml) [![DeepSource](https://deepsource.io/gh/anthonyraf/wind-parser.svg/?label=active+issues&show_trend=true&token=_GxN7KijEstuTXJ7QC8Q0vGb)](https://deepsource.io/gh/anthonyraf/wind-parser/?ref=repository-badge)\n\n*Python wind parser is a parser used to retrieve arguments for command line interfaces and turn them into python dictionary.*\n\n- Wind parser has a very simple and easy use\n- Wind parser supports keyword arguments, flags and keyword arguments that accept lists\n> This parser was created for the [speed](https://github.com/anthonyraf/speed-cli) framework.\n## Installation\n\nInstallation with **pip** : \n\n    $ pip install wind-parser\n    \n## Usage\n\nAfter installing wind-parser you can just instantiate the Parser class with `sys.argv` as argument (`sys.argv` isn't required but it's better for the code clarity)\n\nHere is an example of how the parser is used:\n```python\n# command.py\n\nimport sys\nfrom wind_parser import Parser\n\nparser = Parser(sys.argv) # This variable stores the arguments with their values in a python dictionary\n \nif __name__ == '__main__':\n    print(parser) # Print the dictionary\n```\n> **Note**\n> : You can also use `p.args` for printing the dictionary\n\n\nThen you can run in your terminal:\n    \n    $ python command.py --name=John --age=32 --hobbies Football,Basketball,Cinema --verbose\nOutput:\n\n    {'name':'John', 'age':'32', 'hobbies': ['Football', 'Basketball', 'Cinema'],  'verbose':True}\nTo access the value of an argument, you can choose between:\n\n- Use dictionary key access: \n```python\nprint(p['name'])\n# or\nprint(p.args['name'])\n```\n- Use class attribute access:\n```python\nprint(p.name)\n```\n> **Note**\n> : With this method, you will not be able to retrieve arguments with a `-` in its name.\n\n## Specifications\nThe different types of arguments supported:\n\n- Keyword argument : `-a 1`, `--a=1`, `-a item1,item2,item3`\n- Flag : `--verbose`, `-v`, `--help`\n\n\nHere are the types of the different possible values depending on the type of argument:\n\n| Arguments | Python type|\n|-----------|-----|\n|`--name=John` or `--age 16`| str |\n|`--verbose` or `-v` | bool (always True) |\n|`--files main.py,m.cfg,test.txt` | list[str]\n\n",
    'author': 'Anthony Rafidison',
    'author_email': 'benjaraf006@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/anthonyraf/wind-parser',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
