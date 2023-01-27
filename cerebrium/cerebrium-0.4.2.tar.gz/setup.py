# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cerebrium', 'cerebrium.models']

package_data = \
{'': ['*']}

install_requires = \
['censius>=1.5.8,<2.0.0',
 'cloudpickle>=2.0,<2.1',
 'numpy>=1.21,<2.0',
 'onnxruntime>=1.12.1,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'scikit-learn>=1.0,<2.0',
 'tenacity>=8.1.0,<9.0.0',
 'torch>=1.12,<2.0',
 'tqdm>=4.64.1,<5.0.0',
 'xgboost>=1.6,<2.0',
 'yaspin>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'cerebrium',
    'version': '0.4.2',
    'description': '',
    'long_description': '# Cerebrium\n\nCerebrium is the Python package built for use with the [Cerebrium](https://www.cerebrium.ai/) platform, which allows you to deploy your machine learning models as a REST API with a single line of code.\n\nFor usage consult the [documentation](https://docs.cerebrium.ai/). The repo for the documentation can be found [here](https://github.com/CerebriumAI/docs).\n\n# Development environment\nCerebrium uses Poetry for dependency management and packaging. To install Poetry, follow the instructions [here](https://python-poetry.org/docs/#installation). Alternatively, consult our article on [how to manage your python environments](https://blog.cerebrium.ai/setting-up-your-data-science-and-ml-development-environment-949277339939?gi=54b980dd4e1d).\n\nYou can run the following steps to setup your Python development environment with the following commands:\n```bash\npoetry install\npoetry shell\n```\nYou should use this environment to run tests, notebooks and build the package.\n\nFurthermore, you should set up a `.env` file in the project root with the following environment variables:\n```bash\nDEVELOPMENT_ENV=dev\n```\n',
    'author': 'Elijah Roussos',
    'author_email': 'elijah@cerebrium.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<3.11',
}


setup(**setup_kwargs)
