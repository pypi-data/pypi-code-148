# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flarespy']

package_data = \
{'': ['*'], 'flarespy': ['data/*']}

install_requires = \
['bottleneck>=1.3',
 'lightkurve>=2.3',
 'numba>=0.55.2',
 'retrying>=1.3',
 'scikit-learn>=1.1',
 'tsfresh>=0.20',
 'wotan>=1.10']

setup_kwargs = {
    'name': 'flarespy',
    'version': '0.2.4',
    'description': 'Find flares in TESS light curves',
    'long_description': 'None',
    'author': 'Keyu Xing',
    'author_email': 'kyxing@mail.bnu.edu.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/keyuxing/flarespy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
