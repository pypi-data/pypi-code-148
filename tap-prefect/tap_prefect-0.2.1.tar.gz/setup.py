# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_prefect', 'tap_prefect.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0', 'singer-sdk>=0.18.0,<0.19.0']

extras_require = \
{'s3': ['fs-s3fs>=1.1.1,<2.0.0']}

entry_points = \
{'console_scripts': ['tap-prefect = tap_prefect.tap:TapPrefect.cli']}

setup_kwargs = {
    'name': 'tap-prefect',
    'version': '0.2.1',
    'description': '`tap-prefect` is a Singer tap for prefect, built with the Meltano Singer SDK.',
    'long_description': 'None',
    'author': 'Datateer Dev',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.12',
}


setup(**setup_kwargs)
