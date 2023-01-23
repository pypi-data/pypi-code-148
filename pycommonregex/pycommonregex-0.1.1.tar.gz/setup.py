# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycommonregex']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.1,<8.0.0']

setup_kwargs = {
    'name': 'pycommonregex',
    'version': '0.1.1',
    'description': 'A Python package for common regular expressions.',
    'long_description': "### Common Regex\n\nA python package that provides commonly used regular expressions for validating various types of data.\n\n#### Installation\n\n`pip install pycommonregex`\n\n#### Usage\n\n```python\nimport re\nfrom pycommonregex import *\n\nprint(is_int(5)) # True\nprint(is_positive_int('5')) # True\nprint(is_decimal_num('5.5')) # True\nprint(is_num('-5.5')) # True\nprint(is_alpha_numeric('abc123')) # True\nprint(is_alpha_numeric_with_space('abc 123')) # True\nprint(is_email('email@example.com')) # True\nprint(is_good_password('Abc123#')) # True\nprint(is_username('abc_123')) # True\nprint(is_url('https://www.example.com')) # True\nprint(is_ipv4('127.0.0.1')) # True\nprint(is_ipv6('::1')) # True\n\n```\n\n#### Functions\n\n- 'is_int(num)': Check if the given input is an integer.\n- 'is_positive_int(s)': Check if the given input is a positive integer.\n- 'is_decimal_num(s)': Check if the given input is a decimal number.\n- 'is_num(s)': Check if the given input is a number (positive or negative).\n- 'is_alpha_numeric(s)': Check if the given input is alphanumeric (only contains letters and numbers).\n- 'is_alpha_numeric_with_space(s)': Check if the given input is alphanumeric (only contains letters, numbers, and spaces).\n- 'is_email(email)': Check if the given input is a valid email address.\n- 'is_good_password(password)': Check if the given input is a strong password (contains at least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character, and is at least 8 characters long).\n- 'is_username(username)': Check if the given input is a valid username (contains only letters, numbers, and certain special characters, and is between 4 and 20 characters long).\n- 'is_url(url)': Check if the given input is a valid URL.\n- 'is_ipv4(IPv4)': Check if the given input is a valid IPv4 address.\n- 'is_ipv6(address)': Check if the given input is a valid IPv6 address.\n",
    'author': 'fadedreams7',
    'author_email': 'fadedreams7@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
