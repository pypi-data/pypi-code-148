# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywikidata']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.2.0,<2.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'pywikidata',
    'version': '0.1.2',
    'description': 'Python Wrapper for Wikidata KG',
    'long_description': "# pyWikiData\n\nPython wrapper for Wikidata Knowledge Graph\n\nSupported SPARQL backend\n\n## Install\n\n```bash\npip install pywikidata\n```\n\n#### Install from source by poetry\n```bash\npoetry build\n```\n\n## Usage\n```python\nfrom pywikidata import Entity\ne = Entity('Q90')\ne.label # >> Paris\n```",
    'author': 'Mikhail Salnikov',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
