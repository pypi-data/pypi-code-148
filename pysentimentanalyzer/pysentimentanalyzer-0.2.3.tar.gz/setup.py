# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pysentimentanalyzer']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.3,<4.0.0',
 'nltk>=3.8.1,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'wordcloud>=1.8.2.2,<2.0.0.0']

setup_kwargs = {
    'name': 'pysentimentanalyzer',
    'version': '0.2.3',
    'description': 'Perform sentiment analysis on text',
    'long_description': '# pysentimentanalyzer [![codecov](https://codecov.io/gh/UBC-MDS/py-sentimentanalyzer/branch/main/graph/badge.svg?token=OwGoN7xkT8)](https://codecov.io/gh/UBC-MDS/py-sentimentanalyzer) [![Documentation Status](https://readthedocs.org/projects/py-sentimentanalyzer/badge/?version=latest)](https://py-sentimentanalyzer.readthedocs.io/en/latest/?badge=latest)\n\n\n\nThis package performs sentiment analysis on the given texts and summarizes information from the text.\n\nWhen a survey asks for written comments, it is often tedious to read through every response to extract useful information or just to get a quick summary.\nBy using this package, responses can be quickly summarized to get a general idea of the sentiments of the comments, which can be useful such as when a PR\nteam wants to know the overall sentiment on a company or when instructors want to know the overall sentiment on a course. The goal is to provide a quick\nsummary that is easily interpretable by combining results from a pre-trained Python natural language processing package with the use of visualizations.\n\n## Installation\n\n```bash\npip install pysentimentanalyzer\n```\n\n## Usage\n\nThis package provides the following 4 functions:\n\n* `generate_wordcloud` - Create a wordcloud of the most common positive and negative words.\n* `aggregate_sentiment_score` - Calculates the overall sentiment score of the input texts.\n* `convert_to_likert` - Converts the sentiment score to a likert scale ranging from 1-5.\n* `sentiment_score_plot` - Creates a binned histogram showing count of reviews against the sentiment score.\n\nAll functions take a Pandas DataFrame and string of the column name containing the texts as arguments.\n\nSee below for an example of how to use the package.\n\n```\nimport pandas as pd\nfrom pysentimentanalyzer.generate_wordcloud import *\nfrom pysentimentanalyzer.get_aggregated_sentiment_score import *\nfrom pysentimentanalyzer.likert_scale import *\nfrom pysentimentanalyzer.sentiment_score_plot import *\n\ndf = pd.read_csv("test_tweets.csv") # assuming the csv exists in the current directory\ndf = df.head(200)       \n```\n\n```\naggregate_sentiment_score(df, "text")\n>>> -0.143\n```\n\n```\nconvert_to_likert(df, "text")\n>>> (\'neutral\', 3)\n```\n\n```\nsentiment_score_plot(df, "text")\n```\n![histogram](img/histogram_output.png)\n\n```\nwordcloud_list = generate_wordcloud(df, "text")\nwordcloud_list[0]\n```\n![wordcloud](img/wordcloud_output.png)\n\n## Similar Packages\n\nWhile there exists many packages and libraries for sentiment analysis and many projects built on top of those packages, we could not find specific packages that combines the use of sentiment analysis with visualizations. However, we expect there to be many projects done by individuals that likely perform similar functions by making use of existing NLP packages. Our package aims enhance the existing NLP packages by providing a quick and simple way to generate summary visualizations.\nSome Python packages that perform sentiment analysis include:\n\n* [spaCy](https://spacy.io/)\n* [VADER](https://github.com/cjhutto/vaderSentiment)\n\n## Contributing\n\nThis package was created by Group 8 of the DSCI 524 course with members Eric Tsai, Ranjit Sundaramurthi, Tanmay Agarwal and Ziyi Chen. Nonetheless, we welcome suggestions and improvements. See below for further details.\n\nInterested in contributing? Check out the [contributing guidelines](CONTRIBUTING.md). Please note that this project is released with a [Code of Conduct](CONDUCT.md). By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pysentimentanalyzer` was created by Eric Tsai, Ranjit Sundaramurthi, Tanmay Agarwal and Ziyi Chen. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`pysentimentanalyzer` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Eric Tsai',
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
