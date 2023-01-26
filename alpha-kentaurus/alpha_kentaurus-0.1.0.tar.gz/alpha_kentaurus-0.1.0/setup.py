# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alpha_kentaurus']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'alpha-kentaurus',
    'version': '0.1.0',
    'description': "Not what you're looking for",
    'long_description': "## Not what you're looking for\n![nope](https://cultfilmclub.com/wp-content/uploads/2015/04/Nedry.png)  \n",
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
