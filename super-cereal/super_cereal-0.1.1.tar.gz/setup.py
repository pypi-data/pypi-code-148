# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['super_cereal', 'super_cereal.cerealizer']

package_data = \
{'': ['*']}

extras_require = \
{'avro': ['avro>=1.11.1,<2.0.0'], 'encryption': ['pycryptodome>=3.16.0,<4.0.0']}

setup_kwargs = {
    'name': 'super-cereal',
    'version': '0.1.1',
    'description': 'Serialize Python objects',
    'long_description': '',
    'author': 'Sean Freitag',
    'author_email': 'sean.freitag@avant.com',
    'maintainer': 'Sean Freitag',
    'maintainer_email': 'sean.freitag@avant.com',
    'url': 'https://github.com/cowboygneox/super-cereal',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
