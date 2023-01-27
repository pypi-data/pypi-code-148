# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['np_session']

package_data = \
{'': ['*']}

install_requires = \
['np_config', 'psycopg2>=2.9.5,<3.0.0', 'requests', 'typing-extensions']

extras_require = \
{'dev': ['pip-tools', 'isort', 'mypy', 'black', 'pytest', 'poetry']}

setup_kwargs = {
    'name': 'np-session',
    'version': '0.0.11',
    'description': 'Tools for managing files and metadata associated with ecephys and behavior sessions for the Mindscope Neuropixels team.',
    'long_description': '',
    'author': 'Ben Hardcastle',
    'author_email': 'ben.hardcastle@alleninstitute.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
