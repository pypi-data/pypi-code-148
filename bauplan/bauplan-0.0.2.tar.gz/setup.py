# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bauplan_cli']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bauplan',
    'version': '0.0.2',
    'description': 'Bauplan CLI',
    'long_description': '# Bauplan CLI\n\n## Package publication\n\n```bash\n$ poetry build\n$ poetry publish\n```\n',
    'author': 'Jacopo Tagliabue',
    'author_email': 'jacopo.tagliabue@bauplanlabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
