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
    'version': '2.0.0',
    'description': "Minimally maintained fork of deanmalmgren/textract to remove '*' dependencies",
    'long_description': '.. NOTES FOR CREATING A RELEASE:\n..\n..   * bumpversion {major|minor|patch}\n..   * git push && git push --tags\n..   * twine upload -r textract dist/*\n..   * convert into release https://github.com/deanmalmgren/textract/releases\n\ntextract\n========\n\nExtract text from any document. No muss. No fuss.\n\n`Full documentation <http://textract.readthedocs.org>`__.\n\n|Build Status| |Version| |Downloads| |Test Coverage| |Documentation Status|\n|Updates| |Stars| |Forks|\n\n.. |Build Status| image:: https://travis-ci.org/deanmalmgren/textract.svg?branch=master\n   :target: https://travis-ci.org/deanmalmgren/textract\n\n.. |Version| image:: https://img.shields.io/pypi/v/textract.svg\n   :target: https://warehouse.python.org/project/textract/\n\n.. |Downloads| image:: https://img.shields.io/pypi/dm/textract.svg\n   :target: https://warehouse.python.org/project/textract/\n\n.. |Test Coverage| image:: https://coveralls.io/repos/github/deanmalmgren/textract/badge.svg?branch=master\n    :target: https://coveralls.io/github/deanmalmgren/textract?branch=master\n\n.. |Documentation Status| image:: https://readthedocs.org/projects/textract/badge/?version=latest\n   :target: https://readthedocs.org/projects/textract/?badge=latest\n\n.. |Updates| image:: https://pyup.io/repos/github/deanmalmgren/textract/shield.svg\n    :target: https://pyup.io/repos/github/deanmalmgren/textract/\n\n.. |Stars| image:: https://img.shields.io/github/stars/deanmalmgren/textract.svg\n    :target: https://github.com/deanmalmgren/textract/stargazers\n\n.. |Forks| image:: https://img.shields.io/github/forks/deanmalmgren/textract.svg\n    :target: https://github.com/deanmalmgren/textract/network\n',
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
