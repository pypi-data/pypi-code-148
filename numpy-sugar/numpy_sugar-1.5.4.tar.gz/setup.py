# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['numpy_sugar',
 'numpy_sugar.linalg',
 'numpy_sugar.linalg.test',
 'numpy_sugar.ma',
 'numpy_sugar.ma.test',
 'numpy_sugar.random',
 'numpy_sugar.special',
 'numpy_sugar.test']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.5,<2.0.0', 'pytest>=6.1.2,<7.0.0', 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'numpy-sugar',
    'version': '1.5.4',
    'description': 'Missing NumPy functionalities',
    'long_description': '# numpy-sugar\n\n[![Documentation](https://readthedocs.org/projects/numpy-sugar/badge/?version=latest)](https://numpy-sugar.readthedocs.io/en/latest/?badge=latest)\n\nMissing NumPy functionalities.\n\n## Install\n\nEnter\n\n```bash\npip3 install numpy-sugar\n```\n\nfrom the command-line.\n\n## Running the tests\n\nEnter\n\n```python\npython3 -c "import numpy_sugar; numpy_sugar.test()"\n```\n\n\n## Authors\n\n* [Danilo Horta](https://github.com/horta)\n\n## License\n\nThis project is licensed under the [MIT License](https://raw.githubusercontent.com/limix/numpy-sugar/master/LICENSE.md).\n',
    'author': 'Danilo Horta',
    'author_email': 'danilo.horta@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/limix/numpy-sugar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
