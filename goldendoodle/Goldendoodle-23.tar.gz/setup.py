# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['goldendoodle',
 'goldendoodle.docs.source',
 'goldendoodle.goldendoodle',
 'goldendoodle.goldendoodle.spiders',
 'goldendoodle.goldendoodle.spiders.utils']

package_data = \
{'': ['*'],
 'goldendoodle': ['.vscode/*',
                  'chrome_extensions/*',
                  'docs/*',
                  'docs/build/*',
                  'docs/build/.doctrees/*',
                  'docs/build/_images/*',
                  'docs/build/_modules/*',
                  'docs/build/_modules/goldendoodle/*',
                  'docs/build/_modules/goldendoodle/spiders/*',
                  'docs/build/_modules/goldendoodle/spiders/utils/*',
                  'docs/build/_sources/*',
                  'docs/build/_static/*',
                  'docs/build/_static/scripts/*',
                  'docs/build/_static/styles/*',
                  'reports/*',
                  '{workspaceFolder}/goldendoodle/reports/*'],
 'goldendoodle.goldendoodle.spiders': ['reports/*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'cryptography<38',
 'lxml>=4.9.2,<5.0.0',
 'myst-parser>=0.18.1,<0.19.0',
 'regex>=2022.10.31,<2023.0.0',
 'scrapy-selenium-middleware>=0.0.5,<0.0.6',
 'tldextract>=3.4.0,<4.0.0',
 'webdriver-manager>=3.8.5,<4.0.0']

setup_kwargs = {
    'name': 'goldendoodle',
    'version': '23',
    'description': 'Scrapy helper',
    'long_description': "# README\n\n**Goldendoodle** is a universal spider for analyzing wether domains include a search string.\n\nIt is made for a first analyze of a unknown site. The analyze one search string is done for one search string on a list of start URLs. The allowed domain(s) are extracted from the starting URLs.\n\nThe result is a Scrapy output file with Goldendoodle items.\n\n## How to execute:\nFrom goldendoodle run:\n\n```bash\nscrapy crawl recherchedechaîne_gldnddl -O <file> [-a gldnddlSearchString=<string>] -a option=<None|regex|email> -a start_urls=<url>[,<url>]\n```\np. e.:\n```bash\nscrapy crawl recherchedechaîne_gldnddl -O ../reports/findings.json -a gldnddlSearchString='(Bereich.*obe[nr].*?)(?=<)' -a start_urls=https://www.drta-archiv.de/blauaugenkaerpflinge/ 2> ../reports/stderr.log\n```\n\n### option\noption is optional, which means **None**. \n\nIf gldnddlSearchString is a regular expression, than you should set option=**regex**. Otherwise findingElements and findingElementsQuery will not be filled. With option=regex you will get findingElements and findingElementsQuery only for the first finding in the site.\n\nWith option=**email** no **gldnddlSearchString** is necessary. There is a search algorithm that gives a result for the most common types of email coding. If you find an email that is not recognized, please let me know so I can adjust the algorithm.\n\nWith option=**email AND gldnddlSearchString** set, the gldnddlSearchString is used, but the results are prepared, as if emails have been searched.  \n\n### example:\n\n```bash\nscrapy crawl recherchedechaîne_gldnddl -O reports/findings.json -a gldnddlSearchString='for use in illustrative examples in documents' -a start_urls=https://example.com/ | tee reports/log.txt\n```\n\n## Prerequisites\n\n- see requirements.txt\n\n## Documentation\n\nsee [Goldendoodle docs](https://melchiorim3tal.gitlab.io/goldendoodle/index.html)\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.",
    'author': 'Wilfried Dehnen',
    'author_email': 'wilfried.dehnen@gmx.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
