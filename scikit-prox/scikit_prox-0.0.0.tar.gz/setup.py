# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skprox', 'skprox.linear_model', 'skprox.test']

package_data = \
{'': ['*']}

install_requires = \
['pyproximal>=0.5.0,<0.6.0',
 'pytest>=7.2.1,<8.0.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scikit-learn>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'scikit-prox',
    'version': '0.0.0',
    'description': 'A package for solving regularised optimisation problems in a scikit-learn style.',
    'long_description': '[![codecov](https://codecov.io/gh/jameschapman19/scikit-prox/branch/main/graph/badge.svg?token=JHG9VUB0L8)](https://codecov.io/gh/jameschapman19/scikit-prox)\n![Build Status](https://github.com/jameschapman19/scikit-prox/actions/workflows/test.yml/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/scikit-prox/badge/?version=latest)](https://scikit-prox.readthedocs.io/en/latest/?badge=latest)\n[![version](https://img.shields.io/pypi/v/scikit-prox)](https://pypi.org/project/scikit-prox/)\n[![downloads](https://img.shields.io/pypi/dm/scikit-prox)](https://pypi.org/project/scikit-prox/)\n\n# Scikit-Prox\nThe goal of this project is to implement a set of algorithms for solving the following optimization problem:\nminimize f(x) + g(x) where f is a smooth function and g is a proximal operator. The proximal operator of a function g is defined as:\nproxg(λx) = argmin y g(y) + 1/2λ‖y − x‖2\n\n## Installation\nTo install the package, run the following command:\npip install scikit-prox\n\n## Usage\n\n### Example 1: Lasso\nThe following code solves the following optimization problem:\nminimize 1/2‖Ax − b‖2 + λ‖x‖1\n\n```python\nimport numpy as np\nfrom scipy import sparse\nfrom sklearn.datasets import make_regression\nfrom sklearn.linear_model import Lasso\nfrom skprox.linear_model import RegularisedRegression\n\n# Generate data\nX, y = make_regression(n_samples=100, n_features=1000, random_state=0, noise=4.0, bias=100.0)\nX = sparse.csr_matrix(X)\n\n# Solve the problem using scikit-learn\nmodel = Lasso(alpha=0.1)\nmodel.fit(X, y)\nprint("scikit-learn solution: {}".format(model.coef_))\n\n# Solve the problem using scikit-prox\nmodel = RegularisedRegression(proximal=\'L1\', sigma=0.1)\nmodel.fit(X, y)\nprint("scikit-prox solution: {}".format(model.coef_))\n```\n\n### Example 2: Total Variation Regression\nThe following code solves the following optimization problem:\nminimize 1/2‖Ax − b‖2 + λ‖∇x‖1\n\n```python\nimport numpy as np\nfrom scipy import sparse\nfrom sklearn.datasets import make_regression\nfrom skprox.linear_model import RegularisedRegression\n\n# Generate data\nX, y = make_regression(n_samples=100, n_features=1000, random_state=0, noise=4.0, bias=100.0)\nX = sparse.csr_matrix(X)\n\n# Solve the problem using scikit-prox\nmodel = RegularisedRegression(proximal=\'TV\', sigma=0.1)\nmodel.fit(X, y)\nprint("scikit-prox solution: {}".format(model.coef_))\n```\n\n### Example 3: Grid Search\nThe following code solves the following optimization problem:\nminimize 1/2‖Ax − b‖2 + λ‖x‖1\n\n```python\nimport numpy as np\nfrom scipy import sparse\nfrom sklearn.datasets import make_regression\nfrom sklearn.linear_model import Lasso\nfrom skprox.linear_model import RegularisedRegression\nfrom sklearn.linear_model import GridSearchCV\n\n# Generate data\nX, y = make_regression(n_samples=100, n_features=1000, random_state=0, noise=4.0, bias=100.0)\nX = sparse.csr_matrix(X)\n\n# Solve the problem using scikit-learn\nmodel = Lasso()\ngrid = GridSearchCV(model, {\'alpha\': [0.1, 0.2, 0.3]})\ngrid.fit(X, y)\nprint("scikit-learn solution: {}".format(grid.best_estimator_.coef_))\n\n# Solve the problem using scikit-prox\nmodel = RegularisedRegression(proximal=\'L1\')\ngrid = GridSearchCV(model, {\'sigma\': [0.1, 0.2, 0.3]})\ngrid.fit(X, y)\nprint("scikit-prox solution: {}".format(grid.best_estimator_.coef_))\n```\n\n\n## Documentation\nThe documentation is available at https://scikit-prox.readthedocs.io/en/latest/\n\n## License\nThis project is licensed under the MIT License - see the LICENSE.md file for details\n\n## Acknowledgments\nThis project leans on the pyproximal package borrowing all the proximal operators except for Total Variation which\nis implemented using functions from skimage.',
    'author': 'jameschapman19',
    'author_email': 'james.chapman.19@ucl.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
