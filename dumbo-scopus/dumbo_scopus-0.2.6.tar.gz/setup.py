# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dumbo_scopus']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0',
 'rich>=13.2.0,<14.0.0',
 'selenium>=4.8.0,<5.0.0',
 'typer>=0.7.0,<0.8.0',
 'xlsxwriter>=3.0.7,<4.0.0']

setup_kwargs = {
    'name': 'dumbo-scopus',
    'version': '0.2.6',
    'description': 'Simple CLI to search on Scopus and obtain the results in a XLSX file',
    'long_description': '# Dumbo Scopus\n\nSimple CLI to search on Scopus and obtain the results in a XLSX file.\n\n\n# Prerequisites\n\n- Python 3.10\n- An API key from http://dev.elsevier.com\n\n\n# Install\n\n```bash\n$ pip install dumbo-scopus\n```\n\n\n# Usage\n\nGet help directly from the command:\n```bash\n$ python -m dumbo_scopus --help\n$ python -m dumbo_scopus search --help\n$ python -m dumbo_scopus citations --help\n```\n\nUse the following command line to perform a Scopus Search and obtain the result as an Excel file:\n```bash\n$ python -m dumbo_scopus search "TITLE(magic sets)" --api-key=YOUR-API-KEY\n```\nCheck [this web page](https://dev.elsevier.com/sc_search_tips.html) for the format of the query.\n\nTo download the citations of an article, given its Scopus ID as for example `2-s2.0-84949895809`, use the following command line:\n```bash\n$ python -m dumbo_scopus citations 2-s2.0-84949895809\n```\n',
    'author': 'Mario Alviano',
    'author_email': 'mario.alviano@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
