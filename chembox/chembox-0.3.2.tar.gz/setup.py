# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['chembox']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3', 'pandas>=1.5.2', 'python-semantic-release>=7.33.0,<8.0.0']

setup_kwargs = {
    'name': 'chembox',
    'version': '0.3.2',
    'description': 'A package to analyze chemical formulas',
    'long_description': '# chembox\n\n![example workflow](https://github.com/UBC-MDS/chembox/actions/workflows/ci-cd.yml/badge.svg) [![codecov](https://codecov.io/gh/UBC-MDS/chembox/branch/main/graph/badge.svg?token=AbisKVAtpY)](https://codecov.io/gh/UBC-MDS/chembox)[![Documentation Status](https://readthedocs.org/projects/chembox/badge/?version=latest)](https://chembox.readthedocs.io/en/latest/?badge=latest)\n## Introduction\n\n`chembox` is a package for molecular information calculator based on empirical formulas of chemicals in raw text. It is designed to intelligently process text input containing the chemical formula and provide associated information on the inquired molecule. It is able to provide the molar mass, check a formula\'s validity, and provide a balanced combustion equation if the input is combustible. This tool can be utilized for various educational and research purposes for simple and fast information retrieval.\n\nWe are using a dataset that contains established element data properties from [this site](https://github.com/Bluegrams/periodic-table-data/blob/master/Periodica.Data/Data/ElementData.csv).\n\n## Installation\n\n`chembox` is developed and tested on Python 3.10. You can install it from PyPi via pip:\n\n```bash\n$ pip install chembox\n```\n\n## Usage\n\nThe package includes 4 functions for solving chemistry problems:\n\n- `get_elements`a parser that takes a chemical formula in string format and returns a dictionary that contains the elements and their respective count. \n\n- `is_valid`: a checker that returns a boolean indicating whether a given input is chemically reasonable.\n\n- `get_molec_props`: a method that takes a chemical formula in string format and returns a dataframe with various useful properties of each element in the formula.\n\n- `get_combustion_equation`: a method that takes a text chemical formula that only contains carbon (`C`) and hydrogen (`H`) and outputs a balanced equation resulting from combustion.\n\nA detailed example of usage can be found [here](https://chembox.readthedocs.io/en/latest/example.html).\n\n## Dataset\n\nIn order to be able to perform some of the functions above, a dataset will need to be used that contains various atomic properties of the elements in the periodic table. The data can be found in the Chembox repo [here](https://github.com/UBC-MDS/chembox/tree/main/src/chembox/data) which was sourced from [here](https://github.com/Bluegrams/periodic-table-data/tree/master/Periodica.Data/Data). Please note that we do not take credit for the dataset, it is merely for use with our functions.\n\n## Fitting into the Python ecosystem\n\nA similar package [chemsolve](https://github.com/amogh7joshi/chemsolve) is available online that employs a similar string-parsing design and molar mass calculation.\n\nWhat we do differently:\n\n- We include a dataframe of the molecule properties to give the user enhanced functionality and insights.\n\n- `chemsolve` accepts user-defined reactions. In our package, we include methods for automated combustion equation generation and balancing.\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a [Code of Conduct](https://github.com/UBC-MDS/chembox/blob/main/CONDUCT.md). By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`chembox` is licensed under the terms of the MIT license.\n\n## Contributors\nThe contributors of this project are\nWilfred Hass, Vikram Grewal, Luke Yang, and Nate Puangpanbut.\n\n\n<a href="https://github.com/UBC-MDS/chembox/graphs/contributors">\n  <img src="https://contrib.rocks/image?repo=UBC-MDS/chembox&max=1000" />\n</a>\n\n## Credits\n\n`chembox` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Wilfred Hass',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
