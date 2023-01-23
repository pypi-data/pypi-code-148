# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['artemis',
 'artemis._utilities',
 'artemis.additivity',
 'artemis.comparison',
 'artemis.importance_methods',
 'artemis.importance_methods.model_agnostic',
 'artemis.importance_methods.model_specific',
 'artemis.interactions_methods',
 'artemis.interactions_methods.model_agnostic',
 'artemis.interactions_methods.model_agnostic.partial_dependence_based',
 'artemis.interactions_methods.model_agnostic.performance_based',
 'artemis.interactions_methods.model_specific',
 'artemis.interactions_methods.model_specific.gb_trees',
 'artemis.interactions_methods.model_specific.random_forest',
 'artemis.visualizer']

package_data = \
{'': ['*']}

install_requires = \
['ipykernel>=6.17.0,<7.0.0',
 'networkx>=2.8.8,<3.0.0',
 'numpy>=1.22.0,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'scikit-learn>=1.1.3,<2.0.0',
 'seaborn>=0.12.1,<0.13.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'pyartemis',
    'version': '0.1.4',
    'description': 'A Python package with explanation methods for extraction of feature interactions from predictive models',
    'long_description': '# ARTEMIS: A Robust Toolkit of Explanation Methods for Interaction Spotting\nA Python package with explanation methods for extraction of feature interactions from predictive models\n\n[![build](https://github.com/pyartemis/artemis/actions/workflows/python-app.yml/badge.svg)](https://github.com/pyartemis/artemis/actions/workflows/python-app.yml)\n[![PyPI version](https://badge.fury.io/py/pyartemis.svg)](https://pypi.org/project/pyartemis/)\n[![Downloads](https://static.pepy.tech/badge/pyartemis)](https://pepy.tech/project/pyartemis)\n\n## Overview\n`artemis` is a **Python** package for data scientists and machine learning practitioners which exposes standardized API for extracting feature interactions from predictive models using a number of different methods described in scientific literature.\n\nThe package provides both model-agnostic (no assumption about model structure), and model-specific (e.g., tree-based models) feature interaction methods, as well as other methods that can facilitate and support the analysis and exploration of the predictive model in the context of feature interactions. \n\nThe available methods are suited to tabular data and classification and regression problems. The main functionality is that users are able to scrutinize a wide range of models by examining feature interactions in them by finding the strongest ones (in terms of numerical values of implemented methods) and creating tailored visualizations.\n\n## Documentation\nFull documentation is available at [https://pyartemis.github.io/](https://pyartemis.github.io/).\n\n## Installation\nLatest released version of the `artemis` package is available on [Python Package Index (PyPI)](https://pypi.org/project/pyartemis/):\n\n```\npip install -U pyartemis\n```\n\nThe source code and development version is currently hosted on [GitHub](https://github.com/pyartemis/artemis).\n\n***\n\n## Authors\n\nThe package was created as a software project associated with the BSc thesis ***Methods for extraction of interactions from predictive models*** in the field of Data Science (pl. *Inżynieria i analiza danych*) at Faculty of Mathematics and Information Science (MiNI), Warsaw University of Technology. \n\nThe authors of the `artemis` package are: \n- [Paweł Fijałkowski](https://github.com/pablo2811)\n- [Mateusz Krzyziński](https://github.com/krzyzinskim)\n- [Artur Żółkowski](https://github.com/arturzolkowski)\n\nBSc thesis and work on the `artemis` package was supervised by [Przemysław Biecek, PhD, DSc](https://github.com/pbiecek). \n\n',
    'author': 'Artur Żółkowski',
    'author_email': 'artur.zolkowski@wp.pl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
