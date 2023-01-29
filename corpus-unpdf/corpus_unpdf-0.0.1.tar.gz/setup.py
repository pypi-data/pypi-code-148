# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['corpus_unpdf', 'corpus_unpdf.blocks', 'corpus_unpdf.images']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python>=4.7.0.68,<5.0.0.0',
 'pdfplumber>=0.7.6,<0.8.0',
 'pillow>=9.4.0,<10.0.0',
 'pytesseract>=0.3.10,<0.4.0',
 'python-dotenv>=0.21,<0.22']

setup_kwargs = {
    'name': 'corpus-unpdf',
    'version': '0.0.1',
    'description': 'Parse Philippine Supreme Court decisions issued in PDF format as text.',
    'long_description': '# corpus-unpdf\n\n![Github CI](https://github.com/justmars/corpus-unpdf/actions/workflows/main.yml/badge.svg)\n\nParse Philippine Supreme Court decisions issued in PDF format as text; _hopefully_, this can be utilized in the [LawSQL dataset](https://lawsql.com).\n\n## Documentation\n\nSee [documentation](https://justmars.github.io/corpus-unpdf).\n\n## Development\n\nCheckout code, create a new virtual environment:\n\n```sh\npoetry add corpus-unpdf # python -m pip install corpus-unpdf\npoetry update # install dependencies\npoetry shell\n```\n\nRun tests:\n\n```sh\npytest\n```\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://lawsql.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
