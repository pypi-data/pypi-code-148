# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dputils']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'docx2txt>=0.8,<0.9',
 'fpdf2>=2.5.4,<3.0.0',
 'pdfminer.six>=20220524,<20220525',
 'python-docx>=0.8.11,<0.9.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'dputils',
    'version': '0.2.1',
    'description': 'This library is utility library from digipodium',
    'long_description': 'A python library which can be used to extraxct data from files, pdfs, doc(x) files, as well as save data into these\nfiles. This library can be used to scrape and extract webpage data from websites as well.\n\n### Installation Requirements and Instructions\n\nPython versions 3.8 or above should be installed. After that open your terminal:\nFor Windows users:\n\n```shell\npip install dputils\n```\n\nFor Mac/Linux users:\n\n```shell\npip3 install dputils\n```\n\n### Files Modules\n\nFunctions from dputils.files:\n\n1. get_data:\n    - To import, use statement:\n        ```python3\n\nfrom dputils.files import get_data\n\n```\n- Obtains data from files of any extension given as args(supports text files, binary files, pdf, doc for now, more\ncoming!)\n- sample call:\n```python3\ncontent = get_data(r"sample.docx")\nprint(content)\n```\n\n- Returns a string or binary data depending on the output arg\n- images will not be extracted\n\n2. save_data:\n- save_data can be used to write and save data into a file of valid extension.\n- sample call:\n```python3\nfrom dputils.files import save_data\n\npdfContent = save_data("sample.pdf", "Sample text to insert")\nprint(pdfContent)\n```\n- Returns True if file is successfully accessed and modified. Otherwise, False.\n\n### Scrape Modules\n\nThe Scraper class is a web scraping tool that uses the BeautifulSoup library to extract data from a specified URL. The\nclass has several methods including init, validate_url, clean_url, soup, get, and get_all. The init method takes in a\nURL, a user agent, cookies, and a clean flag. The validate_url method checks if the URL is valid and the clean_url\nmethod removes any query parameters from the URL. The soup method makes a request to the URL and returns a BeautifulSoup\nobject of the webpage. The get method takes in a list of Tag objects and returns a dictionary of the extracted data. The\nget_all method takes in a target tag, an items tag, and a list of tags and returns a list of dictionaries of the\nextracted data for each item. The class also has the ability to handle errors and provide information about the\nextraction process.\n\nThese functions can used on python versions 3.8 or greater.\n\nReferences for more help: https://github.com/digipodium/dputils\n\nThank you for using dputils!',
    'author': 'AkulS1008',
    'author_email': 'akulsingh0708@gmail.com',
    'maintainer': 'Zaid Kamil',
    'maintainer_email': 'xaidmetamorphos@gmail.com',
    'url': 'https://digipodium.github.io/dputils/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
