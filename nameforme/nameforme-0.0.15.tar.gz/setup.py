# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nameforme']

package_data = \
{'': ['*']}

install_requires = \
['jellyfish>=0.9.0,<0.10.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pytest>=7.2.1,<8.0.0']

setup_kwargs = {
    'name': 'nameforme',
    'version': '0.0.15',
    'description': 'A package used to generate names.',
    'long_description': '# nameforme\n\nA helper python package that can be used to generate names based on the [`dateset`](https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2022/2022-03-22/babynames.csv). This could be used to come up with baby names, character names, pseudonyms, etc. \n\nSource Data: Contains baby names born in the United States for each year from 1880 to 2017, and the number of children of each sex given each name. Names must appear at least 5 times in each year to be included. (Source: http://www.ssa.gov/oact/babynames/limits.html)\n\nThis package is similar to the existing [names](https://pypi.org/project/names/) package by Trey Hunner (last updated in 2014), however, our uses a more recent dataset (with names up to 2017), and more options for users to customize what type of names to generate, including the ability to generate similar sounding names.\n\nYou can check the online documentation of this package on [readthedocs](https://nameforme.readthedocs.io/en/main/index.html).\n\n## Features\nNote that the name of the functions is not finalized. They are subject to change.\n\nThe package is an assimilation of four independent functions:\n\n- `find_unisex_name`: Generate a random set of 10 suggested neutral baby names based on the given limitation and baby names in the past years.\n\n- `find_old_name`: Generate a random set of 10 suggested neutral(by default) baby names based on the given time period and sex.\n\n- `find_similar_name`: Generate a random set of 10 suggested similar baby names based on the syllable of the input name. \n\n- `find_name`: Generate a random set of 10 suggested baby names based on the given limitations.\n\n## Installation\n\n```bash\n$ pip install nameforme\n```\n\n## Usage\n\nBelow is a basic example of how to use each of the four functions included in this package.\n\n```\n# Load all required package functions\nfrom nameforme.nameforme import find_name\nfrom nameforme.nameforme import find_old_name\nfrom nameforme.nameforme import find_similar_name\nfrom nameforme.nameforme import find_unisex_name\n\n# Generate a random set of 10 suggested baby names based on the given limitations.\n# if the given limitation can match to at least 10 names, a list of 10 names will be provided\nfind_name("F", "A", length=3)\n#if the given limitation can only match less than 10 names, all matched names will be provided\nfind_name("m", "b", length=9)\n\n# Generate a random set of suggested neutral(by default) baby names based on the given time period and sex.\nfind_old_name(\'1980s\', limit=3)\n\n# Generate a random list of names that sound similar to a given user input name.\nfind_similar_name(\'Daniel\', limit=20)\n\n# Generate the a random set of suggested neutral baby names based on the given limitation and baby names in the past years.\nfind_unisex_name(bar=0.02,limit=10)\n```\n\n## Dependencies\n- python = "3.9"\n- numpy = "1.24.1"\n- pandas = "1.5.3"\n- jellyfish = "0.9.0"\n- pytest = "7.2.1"\n- sphinx = "6.1.3"\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`nameforme` was created by Daniel Cairns, Eyre Hong, Bruce Wu, Zilong Yi (UBC MDS). It is licensed under the terms of the MIT license.\n\n## Credits\n\n`nameforme` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Daniel Cairns, Eyre Hong, Bruce Wu, Zilong Yi (UBC MDS)',
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
