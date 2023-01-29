# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['twitterpersona']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.3,<4.0.0',
 'nltk>=3.8.1,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'pillow>=9.4.0,<10.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'tweepy>=4.12.1,<5.0.0',
 'tweet-preprocessor>=0.6.0,<0.7.0',
 'wordcloud>=1.8.2.2,<2.0.0.0']

setup_kwargs = {
    'name': 'twitterpersona',
    'version': '0.3.0',
    'description': "Assess whether a twitter is positive or negative based on the user's recent tweets",
    'long_description': '[![ci-cd](https://github.com/UBC-MDS/twitter-persona/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/twitter-persona/actions/workflows/ci-cd.yml) [![Documentation Status](https://readthedocs.org/projects/twitterpersona/badge/?version=latest)](https://twitterpersona.readthedocs.io/en/latest/?badge=latest) ![PyPI](https://img.shields.io/pypi/v/twitterpersona) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) \n# twitterpersona\n\nTwitter is a popular social media app with over 1 billion user accounts. While a diversity of users is a strength, some individuals have concerns with the prevalence of "troll" accounts and individuals who exhibit unconstructive tone and diction whom they deem not worth engaging with.\nThe package twitterpersona is intended to provide insight into a twitter user based on their tweet history in effort to determine if an account is worth engaging with. The package provides an easy to use interface for determining the general sentiment expressed by a user.\n\n## Contributors and Maintainers\n- [Renzo Wijngaarden](https://github.com/Hawknum)\n- [Roan Raina](https://github.com/roanraina)\n- [Andy Wang](https://github.com/tiger12055)\n- [Yurui Feng](https://github.com/Yurui-Feng)\n\n\n## Quick Start\n\nTo get started with `twitterpersona`, install it using `pip`:\n\n```bash\n$ pip install twitterpersona\n```\nPlease visit the [documentation](https://twitterpersona.readthedocs.io/en/latest/?badge=latest) for more information and examples.\n\n## Classes and Functions\n1. `load_twitter_msg`: returns a user\'s recent tweets (as a dataframe) given their `user id` using the Twitter API.\n   1. `user_info()`: get user credentials details\n   2. `load_twitter_by_user()`: load specific user\'s tweets\n   3. `load_twitter_by_keywords()`: load specific keyword\'s tweets\n2. `sentiment_analysis`: determines the general (average) sentiment of recent tweets\n   1. `sentiment_labler()`: returns all tweets with the corresponding labels\n3. `preprocessing`: a spotter that identifies credit card numbers\n   1. `generalPreprocessing`: returns the processed tweet dataframe\n4. `generate_word_cloud`: a spotter that identifies credit card numbers\n   1. `create_wordcloud`: returns a matplotlib plot of the wordcloud\n\nBelow is a simple quick start example:\n\n```python\nfrom twitterpersona import load_twitter_msg, sentiment_analysis, preprocessing, generate_word_cloud\n\n# Create a cleanser, and don\'t add the default spotters\nuser = user_info(\'consumer key\', \'consumer secret\', \'access_token\', \'token_secret\')\ntwitter_df = load_twitter_by_user(\'someuser\', 30, user)\nsentiment_df = sentiment_labler(twitter_df, \'text\')\ncleaned_df = generalPreprocessing(sentiment_df)\nplt = generate_word_cloud(cleaned_df)\n```\nIn order to run test, you need to first install the vader_lexicon package\n\n```bash\n$ python -m nltk.downloader vader_lexicon\n```\n## Scope and Fit\n\nThere are existing packages that preform tweet analysis (including [twitter-sentiment-analysis](https://github.com/abdulfatir/twitter-sentiment-analysis), [tweetlytics](https://github.com/UBC-MDS/tweetlytics), and [pytweet](https://github.com/UBC-MDS/pytweet)). However, none of these packages focus of providing metrics in the context of determining if the twitter user is worth engaging with.\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines in CONTRIBUTING.md. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`twitterpersona` was created by Andy Wang, Renzo Wijngaarden, Roan Raina, Yurui Feng. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`twitterpersona` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Andy Wang, Renzo Wijngaarden, Roan Raina, Yurui Feng',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
