# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['topicwizard',
 'topicwizard.blueprints',
 'topicwizard.components',
 'topicwizard.components.documents',
 'topicwizard.components.topics',
 'topicwizard.components.words',
 'topicwizard.plots',
 'topicwizard.prepare']

package_data = \
{'': ['*'], 'topicwizard': ['assets/*']}

install_requires = \
['dash-extensions>=0.1.10,<0.2.0',
 'dash-iconify>=0.1.2,<0.2.0',
 'dash-mantine-components>=0.11.1,<0.12.0',
 'dash>=2.7.1,<2.8.0',
 'joblib>=1.2.0,<1.3.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.2,<1.6.0',
 'scikit-learn>=1.2.0,<1.3.0',
 'wordcloud>=1.8.2.2,<1.9.0.0']

setup_kwargs = {
    'name': 'topic-wizard',
    'version': '0.1.12',
    'description': 'Pretty and opinionated topic model visualization in Python.',
    'long_description': '<img align="left" width="82" height="82" src="assets/logo.svg">\n\n# topicwizard\n\n<br>\n\nPretty and opinionated topic model visualization in Python.\n\n[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/x-tabdeveloping/topic-wizard/blob/main/examples/basic_usage.ipynb)\n[![PyPI version](https://badge.fury.io/py/topic-wizard.svg)](https://pypi.org/project/topic-wizard/)\n[![pip downloads](https://img.shields.io/pypi/dm/topic-wizard.svg)](https://pypi.org/project/topic-wizard/)\n[![python version](https://img.shields.io/badge/Python-%3E=3.8-blue)](https://github.com/centre-for-humanities-computing/tweetopic)\n[![Code style: black](https://img.shields.io/badge/Code%20Style-Black-black)](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)\n<br>\n\n## Features\n\n-   Investigate complex relations between topics, words and documents\n-   Highly interactive\n-   Name topics\n-   Pretty :art:\n-   Intuitive :cow:\n-   Clean API :candy:\n-   Sklearn compatible :nut_and_bolt:\n-   Easy deployment :earth_africa:\n\n## Installation\n\nInstall from PyPI:\n\n```bash\npip install topic-wizard\n```\n\n## Usage ([documentation](https://x-tabdeveloping.github.io/topic-wizard/))\n\n### Step 1:\n\nTrain a scikit-learn compatible topic model.\n\n```python\nfrom sklearn.decomposition import NMF\nfrom sklearn.feature_extraction.text import CountVectorizer\nfrom sklearn.pipeline import Pipeline\n\ntopic_pipeline = Pipeline(\n    [\n        ("bow", CountVectorizer()),\n        ("nmf", NMF(n_components=10)),\n    ]\n)\ntopic_pipeline.fit(texts)\n```\n\n### Step 2:\n\nVisualize with topicwizard.\n\n```python\nimport topicwizard\n\ntopicwizard.visualize(pipeline=topic_pipeline, corpus=texts)\n```\n\n### Step 3:\n\nInvestigate :eyes: .\n\n#### a) Topics\n\n![topics screenshot](assets/screenshot_topics.png)\n\n#### b) Words\n\n![words screenshot](assets/screenshot_words.png)\n![words screenshot](assets/screenshot_words_zoomed.png)\n\n#### c) Documents\n\n![documents screenshot](assets/screenshot_documents.png)\n',
    'author': 'Márton Kardos',
    'author_email': 'power.up1163@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0',
}


setup(**setup_kwargs)
