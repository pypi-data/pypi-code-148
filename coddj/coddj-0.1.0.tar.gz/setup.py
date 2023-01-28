# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['coddj']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=2.74.0,<3.0.0',
 'pafy>=0.5.5,<0.6.0',
 'pyfiglet>=0.8.post1,<0.9',
 'pyinquirer>=1.0.3,<2.0.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'python-vlc>=3.0.18121,<4.0.0',
 'youtube-dl>=2021.12.17,<2022.0.0']

setup_kwargs = {
    'name': 'coddj',
    'version': '0.1.0',
    'description': 'Personal package for playing youtube audio',
    'long_description': '# coddj\n\nPersonal package for playing youtube audio\n\n## Installation\n\n```bash\n$ pip install coddj\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`coddj` was created by Dylan Garrett. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`coddj` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Dylan Garrett',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
