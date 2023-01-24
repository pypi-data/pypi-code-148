# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xarray_multiscale']

package_data = \
{'': ['*']}

install_requires = \
['dask>=2020.12.0', 'numpy>=1.19.4', 'scipy>=1.5.4', 'xarray>=2022.03.0']

setup_kwargs = {
    'name': 'xarray-multiscale',
    'version': '1.1.1',
    'description': '',
    'long_description': 'None',
    'author': 'Davis Vann Bennett',
    'author_email': 'davis.v.bennett@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
