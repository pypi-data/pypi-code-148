# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alpha_kentaurus']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'alpha-kentaurus-macos',
    'version': '0.1.2',
    'description': "Not what you're looking for, please make sure you're using the internal pypi",
    'long_description': "## Not what you're looking for\n![nope](http://hamsterexpert1011.weebly.com/uploads/1/1/7/4/11740742/9234812.jpg)  \n",
    'author': 'nope',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
