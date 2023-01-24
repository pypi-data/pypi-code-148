# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notebooks',
 'notebooks.co_occurrence',
 'notebooks.common',
 'notebooks.most_discriminating_words',
 'notebooks.pos_statistics',
 'notebooks.topic_modelling',
 'notebooks.word_trends']

package_data = \
{'': ['*']}

install_requires = \
['bokeh',
 'click',
 'humlab-penelope[full]>=0.7.21,<0.8.0',
 'ipysheet',
 'ipywidgets',
 'jupyterlab',
 'matplotlib',
 'msgpack',
 'pandas',
 'pandas-bokeh',
 'tqdm']

setup_kwargs = {
    'name': 'humlab-inidun',
    'version': '0.3.14',
    'description': 'INIDUN research project text analysis tools and utilities',
    'long_description': '# The INIDUN Text Analytics Repository\n\n### Prerequisites\n\n### Installation\n\n### Note\n\n\n',
    'author': 'Roger Mähler',
    'author_email': 'roger.mahler@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://inidun.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<3.10.0',
}


setup(**setup_kwargs)
