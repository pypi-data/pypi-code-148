# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydicttools']

package_data = \
{'': ['*']}

install_requires = \
['asyncio>=3.4.3,<4.0.0',
 'pytest-asyncio>=0.20.3,<0.21.0',
 'pytest>=7.2.1,<8.0.0']

setup_kwargs = {
    'name': 'pydicttools',
    'version': '0.1.0',
    'description': 'Set of tools to handle Dict type in Python.',
    'long_description': '### Python Dictionary Utility Package\n\nThis package contains a collection of functions that perform various operations on Python dictionaries.\n\n#### Features\n\n##### concat_dict(dict1, dict2):\n\nTakes two dictionaries as input and returns a new dictionary that is the result of merging the keys and values of both input dictionaries.\n\n##### key_exists(dictionary, key):\n\nTakes a dictionary and a key as input and returns a Boolean indicating whether the key exists in the dictionary.\n\n##### value_exists(dictionary, value):\n\nTakes a dictionary and a value as input and returns a Boolean indicating whether the value exists in the dictionary.\n\n##### clone(obj):\n\nTakes an object as input and returns a deep copy of the object.\n\n##### is_empty(dictionary):\n\nTakes a dictionary as input and returns a Boolean indicating whether the dictionary is empty.\n\nget_value_from_dict(dictionary, key_path):\nTakes a dictionary and a key path as input and returns the value associated with the key path.\n\n##### is_subset(dict1, dict2):\n\nTakes two dictionaries as input and returns a Boolean indicating whether dict1 is a subset of dict2.\n\n##### sort_dict_by_key(d):\n\nTakes a dictionary as input and returns a new dictionary with the items sorted by key.\n\n##### sort_dict_by_custom_key(d, key_extractor):\n\nTakes a dictionary and a key extractor function as input and returns a new dictionary with the items sorted by the custom key extractor.\n\n##### pretty_print_dict(d, indent):\n\nTakes a dictionary and an indentation level as input and pretty prints the dictionary.\n\n##### iterate_dict(d):\n\nTakes a dictionary as input and returns an iterator over the key-value pairs of the dictionary.\n\n##### clone_async(obj):\n\nTakes an object as input and returns a deep copy of the object asynchronously.\n\n#### Installation\n\nTo install the package, run the following command:\n\n```python\npip install pydicttool\n```\n\n#### Usage\n\n```python\nfrom python_dictionary_utility import *\n\ndict1 = {\'a\': 1, \'b\': 2}\ndict2 = {\'c\': 3, \'d\': 4}\n\n# Concatenate two dictionaries\nresult = concat_dict(dict1, dict2)\nprint(result) # {\'a\': 1, \'b\': 2, \'c\': 3, \'d\': 4}\n\n# Check if key exists in dictionary\nresult = key_exists(dict1, \'a\')\nprint(result) # True\n\n# Check if value exists in dictionary\nresult = value_exists(dict1, 2)\nprint(result) # True\n\n# Clone object\nresult = clone({\'a\': [1, 2, 3]})\nprint(result) # {\'a\': [1, 2, 3]}\n\n# Check if dictionary is empty\nresult = is_empty({})\nprint(result) # True\n\n# Get value from dictionary by key path\nresult = get_value_from_dict({\'a\': {\'b\': {\'c\': 1}}}, \'a.b.c\')\nprint(result) # 1\n\n# Check if one dictionary is subset of another\noriginal_dict = {\'c\': 3, \'a\': 1, \'b\': 2}\nsorted_dict = sort_dict_by_key(original_dict)\nprint(sorted_dict) # {\'a\': 1, \'b\': 2, \'c\': 3}\n\noriginal_dict = {\'c\': 3, \'a\': 1, \'b\': 2}\n\n# Custom key extractor function\ndef custom_key_extractor(key, value):\n    return value\n\nsorted_dict = sort_dict_by_custom_key(original_dict, custom_key_extractor)\nprint(sorted_dict) # {\'a\': 1, \'b\': 2, \'c\': 3}\n\noriginal_dict = {\'c\': 3, \'a\': 1, \'b\': 2}\npretty_print_dict(original_dict, 2)\n# Output:\n# {\n#   "a": 1,\n#   "b": 2,\n#   "c": 3\n# }\n\noriginal_dict = {\'c\': 3, \'a\': 1, \'b\': 2}\nfor key, value in iterate_dict(original_dict):\n    print(f\'{key}: {value}\')\n# Output:\n# c: 3\n# a: 1\n# b: 2\n``\n\n# Clone object\nresult = clone({\'a\': [1, 2, 3]})\nprint(result) # {\'a\': [1, 2, 3]}\n\n```\n\n##### clone_async example usage for python 3.8>=\n\n```python\nimport asyncio\n\n# Original object\noriginal_obj = {\'a\': [1, 2, 3], \'b\': {\'c\': 4, \'d\': 5}}\n\nasync def main():\n    # Asynchronously clone the object\n    cloned_obj = await clone_async(original_obj)\n\n    # Print the cloned object\n    print(cloned_obj) # {\'a\': [1, 2, 3], \'b\': {\'c\': 4, \'d\': 5}}\n\n# Run the main function\nawait main()\n\n```\n\n##### clone_async example usage for python 3.7<\n\n```python\nimport asyncio\n\n# Original object\noriginal_obj = {\'a\': [1, 2, 3], \'b\': {\'c\': 4, \'d\': 5}}\n\nasync def main():\n    # Asynchronously clone the object\n    cloned_obj = await clone_async(original_obj)\n\n    # Print the cloned object\n    print(cloned_obj) # {\'a\': [1, 2, 3], \'b\': {\'c\': 4, \'d\': 5}}\n\n# Run the main function\nasyncio.run(main())\n```\n',
    'author': 'fadedreams7',
    'author_email': 'fadedreams7@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fadedreams/pydicttools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
