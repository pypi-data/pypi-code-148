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
    'version': '0.1.3',
    'description': 'Python Wrapper for Wikidata KG',
    'long_description': '# pyWikiData\n\nPython wrapper for Wikidata Knowledge Graph\n\nSupported SPARQL backend\n\n## Install\n\n```bash\npip install pywikidata\n```\n\n#### Install from source by poetry\n```bash\npoetry build\n```\n\n## Usage\n```python\nfrom pywikidata import Entity\n\nentity = Entity(\'Q90\')\nentity.label # >> Paris\n\nEntity.from_label(\'Paris\') # >> [<Entity: Q116373885>, <Entity: Q116373939>, <Entity: Q90>, ...]\n\nentity.instance_of # >> [<Entity: Q174844>, <Entity: Q200250>, <Entity: Q208511>, ...]\n\nentity.forward_one_hop_neighbours # >> [(<Entity(Property): P6>, <Entity: Q2851133>), (<Entity(Property): P8138>, <Entity: Q108921672>), ...]\nentity.backward_one_hop_neighbours\n\nEntity("P81").is_property # >> True\nEntity("Q90").is_property # >> False\n```',
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
