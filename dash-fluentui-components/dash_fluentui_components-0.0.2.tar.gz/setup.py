# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dash_fluentui_components']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.7.0']}

setup_kwargs = {
    'name': 'dash-fluentui-components',
    'version': '0.0.2',
    'description': 'FluentUI components for Plotly Dash.',
    'long_description': "# dash-fluentui-components\n\nA component library for Plotly's Dash based on the fluentui react components.\n\n## TODO\n\n- [smooth sidebar transitions][smmoth]\n\n[smmoth]: http://reactcommunity.org/react-transition-group/\n",
    'author': 'Robert Pack',
    'author_email': 'robstar.pack@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
