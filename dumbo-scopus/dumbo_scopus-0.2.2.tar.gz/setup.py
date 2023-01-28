# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dumbo_scopus']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0',
 'rich>=13.2.0,<14.0.0',
 'typer>=0.7.0,<0.8.0',
 'xlsxwriter>=3.0.7,<4.0.0']

setup_kwargs = {
    'name': 'dumbo-scopus',
    'version': '0.2.2',
    'description': 'Simple CLI to search on Scopus and obtain the results in a XLSX file',
    'long_description': '# Dumbo Scopus\n\nSimple CLI to search on Scopus and obtain the results in a XLSX file.\n\n\n# Prerequisites\n\n- Python 3.10\n- An API key from http://dev.elsevier.com\n\n\n# Install\n\n```bash\n$ pip install dumbo-scopus\n```\n\n\n# Usage\n\nUse the following command line:\n```bash\n$ python -m dumbo_scopus "TITLE(magic sets)" --api-key=YOUR-API-KEY\n```\n\nA file `scopus.xlsx` with the results will be produced.\nAdd `--help` to see more options.\n\nCheck [this web page](https://dev.elsevier.com/sc_search_tips.html) for the format of the query.\nAdditionally, if the API key is authorized to access the [Citation Overview API](https://dev.elsevier.com/documentation/AbstractCitationAPI.wadl), citations of an article can be obtained by using `"CITATIONS(2-s2.0-scopus-id-here)"` as query.\n',
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
