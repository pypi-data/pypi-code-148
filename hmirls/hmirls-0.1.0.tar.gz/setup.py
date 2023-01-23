# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hmirls']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0', 'scipy>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'hmirls',
    'version': '0.1.0',
    'description': 'Library for Schatten-p norm minimization via iteratively reweighted least squares',
    'long_description': '# Harmonic Mean Iteratively Reweighted Least Squares for Low-Rank Matrix Recovery\n\nThis repository contains python code to implement a basic variant of the Harmonic Mean Iteratively Reweighted Least Squares (HM-IRLS) algorithm for low-rank matrix recovery, in particular for the low-rank matrix completion problem, described in the paper:\n\n> C. Kümmerle, J. Sigl.\n> "Harmonic Mean Iteratively Reweighted Least Squares for Low-Rank Matrix Recovery", Journal of Machine Learning Research (JMLR) volume 19, number 47, pages 1-49, 2018.\n> Available online: https://jmlr.org/papers/volume19/17-244/17-244.pdf\n\n## Version history\n* Version 0.0.1, 10/25/2020\n\n## Author\nKristof Schröder\n\n## Documentation\n> https://hmirls.readthedocs.io/en/latest/',
    'author': 'Kristof Schroeder',
    'author_email': 'kristof_schroeder@web.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
