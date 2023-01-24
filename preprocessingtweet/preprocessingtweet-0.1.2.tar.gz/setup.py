# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['preprocessingtweet']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'emot>=3.1,<4.0',
 'gensim>=4.3.0,<5.0.0',
 'joblib>=1.2.0,<2.0.0',
 'nltk>=3.8.1,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'regex>=2022.10.31,<2023.0.0',
 'scipy>=1.10.0,<2.0.0',
 'six>=1.16.0,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'preprocessingtweet',
    'version': '0.1.2',
    'description': 'Preprocessing tweets prior to use in Transformers',
    'long_description': '# dataPreprocessing\n\nParsing tweet object to lower and clean text. Remove entities (RT, Hashtags, mentions, urls) from the text (can keep the hashtags) and can replace them with placeholder.\nDo some basic retweet detection to return if it is a Retweet or no.\n\n\n',
    'author': 'Olivier Philippe',
    'author_email': 'olivier.philippe@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
