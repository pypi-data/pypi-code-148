# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djext',
 'djext.blame',
 'djext.blame.forms',
 'djext.datetime',
 'djext.datetime.forms',
 'djext.http',
 'djext.json',
 'djext.json.auth',
 'djext.json.http',
 'djext.status',
 'djext.templatetags',
 'djext.urls']

package_data = \
{'': ['*'], 'djext': ['templates/*']}

setup_kwargs = {
    'name': 'djext',
    'version': '0.5.0',
    'description': 'Quick tools for Django',
    'long_description': '# djext - Django Extended\n\nQuick tools for Django\n',
    'author': 'Yehuda Deutsch',
    'author_email': 'yeh@uda.co.il',
    'maintainer': 'Yehuda Deutsch',
    'maintainer_email': 'yeh@uda.co.il',
    'url': 'https://gitlab.com/x59/djext',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
