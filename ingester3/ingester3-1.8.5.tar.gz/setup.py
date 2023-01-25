# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ingester3']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=36.0,<37.0',
 'diskcache>=5.0.0,<6.0.0',
 'levenshtein>=0.20,<0.21',
 'numpy>=1.20,<2.0',
 'pandas>=1.2.3,<2.0.0',
 'psycopg2>=2.8.1,<3.0.0',
 'python-dotenv>=0.18,<0.19',
 'sqlalchemy>=1.3,<2.0']

setup_kwargs = {
    'name': 'ingester3',
    'version': '1.8.5',
    'description': 'Data ingester for ViEWS3.',
    'long_description': '# Ingester3\n\nIngester3 is the Pandas extension-based system for ingesting data in the ViEWS3 system.\n\n## Funding\n\nThe contents of this repository is the outcome of projects that have received funding from the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (Grant agreement No. 694640, *ViEWS*) and Horizon Europe (Grant agreement No. 101055176, *ANTICIPATE*; and No. 101069312, *ViEWS* (ERC-2022-POC1)), Riksbankens Jubileumsfond (Grant agreement No. M21-0002, *Societies at Risk*), Uppsala University, Peace Research Institute Oslo, the United Nations Economic and Social Commission for Western Asia (*ViEWS-ESCWA*), the United Kingdom Foreign, Commonwealth & Development Office (GSRA – *Forecasting Fatalities in Armed Conflict*), the Swedish Research Council (*DEMSCORE*), the Swedish Foundation for Strategic Environmental Research (*MISTRA Geopolitics*), the Norwegian MFA (*Conflict Trends* QZA-18/0227), and the United Nations High Commissioner for Refugees (*the Sahel Predictive Analytics project*).\n',
    'author': 'Mihai Croicu',
    'author_email': 'mihai.croicu@pcr.uu.se',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/UppsalaConflictDataProgram/ingester3>',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
