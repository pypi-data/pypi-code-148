# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_setupinfo']

package_data = \
{'': ['*']}

install_requires = \
['pytest-cov>=4.0.0,<5.0.0']

entry_points = \
{'pytest11': ['setupinfo = pytest_setupinfo.pytest_setupinfo']}

setup_kwargs = {
    'name': 'pytest-setupinfo',
    'version': '0.1.1',
    'description': 'Displaying setup info during pytest command run',
    'long_description': '# pytest_setupinfo\n\nDisplaying setup info during pytest command run\n\n## Installation\n\n```bash\n$ pip install pytest_setupinfo\n```\n\n## Usage\n\nOnce pytest_setupinfo plugin is installed we can get setup related information using following command \n\n$ pytest -vs --setupinfo\n\nthis plugin also have one method which returns pytest version/number fixtures/plugin which it supported \n\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pytest_setupinfo` was created by Maheshwar Bolewar. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`pytest_setupinfo` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Maheshwar Bolewar',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
