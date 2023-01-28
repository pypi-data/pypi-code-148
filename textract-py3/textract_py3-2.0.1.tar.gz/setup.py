# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textract', 'textract.bin', 'textract.parsers']

package_data = \
{'': ['*']}

install_requires = \
['SpeechRecognition>=3.8.1',
 'argcomplete>=1.10.0',
 'beautifulsoup4>=4.8.0',
 'chardet>=3',
 'docx2txt>=0.8',
 'extract-msg>=0.30.11',
 'pdfminer.six>=20221105',
 'python-pptx>=0.6.18',
 'six>=1.16.0',
 'xlrd>=1.2.0']

entry_points = \
{'console_scripts': ['textract = textract.bin.textract:main']}

setup_kwargs = {
    'name': 'textract-py3',
    'version': '2.0.1',
    'description': "Minimally maintained fork of deanmalmgren/textract to remove '*' dependencies",
    'long_description': "# Textract\n\nThis is a minimally maintained fork of [deanmalmgren/textract](https://github.com/deanmalmgren/textract) to remove '*' dependencies for use with `asdf` or `rtx` (`rtx plugin add textract-py3 https://github.com/amrox/asdf-pyapp.git`)\n",
    'author': 'Dean Malmgren',
    'author_email': 'dean.malmgren@datascopeanalytics.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/KyleKing/textract-py3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
