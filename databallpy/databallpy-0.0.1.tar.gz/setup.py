# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['databallpy']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0', 'pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'databallpy',
    'version': '0.0.1',
    'description': 'A package for loading, preprocessing, vizualising and synchronizing soccere event aand tracking data.',
    'long_description': '# databallpy\n\nA package for loading, preprocessing, vizualising and synchronizing soccere event aand tracking data.\n\n## Installation\n\n```bash\n$ pip install databallpy\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`databallpy` was created by Alexander Oonk & Daan Grob. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`databallpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Alexander Oonk',
    'author_email': 'alexanderoonk26@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Alek050/databallpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1',
}


setup(**setup_kwargs)
