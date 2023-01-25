# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prfr']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'noisyopt>=0.2.2,<0.3.0',
 'numpy>=1.21,<2.0',
 'scikit-learn>=1.1,<2.0',
 'scipy>=1.8.0,<2.0.0',
 'tqdm>=4.64.0,<5.0.0']

extras_require = \
{'jax': ['jax>=0.3.24,<0.4.0', 'jaxopt>=0.5.5,<0.6.0', 'optax>=0.1.3,<0.2.0']}

setup_kwargs = {
    'name': 'prfr',
    'version': '0.2.4',
    'description': 'Probabilitic random forest regression algorithm',
    'long_description': '# prfr\n\nProbabilistic random forest regressor: random forest model that accounts for errors in predictors and labels, yields calibrated probabilistic predictions, and corrects for bias.\n\nFor a faster and more elaborate calibration routine (highly recommended), a [JAX](https://github.com/google/jax#installation) installation is required. You can install the package with the extra `jax` feature, which will install the necessary dependencies. \n\n## Installation\n\nFrom PyPI, with `jax` feature:\n```bash\npip install "prfr[jax]" \n```\n\nFrom PyPI, without `jax` feature:\n```bash\npip install prfr\n```\n\nFrom Github (latest), with `jax` feature:\n\n```bash\npip install "prfr[jax] @ git+https://github.com/al-jshen/prfr"\n```\n\nFrom Github (latest), without `jax` feature:\n\n```bash\npip install "git+https://github.com/al-jshen/prfr"\n```\n\n## Example usage\n\n```python\nimport numpy as np\nimport prfr\n\nx_obs = np.random.uniform(0., 10., size=10000).reshape(-1, 1)\nx_err = np.random.exponential(1., size=10000).reshape(-1, 1)\ny_obs = np.random.normal(x_obs, x_err).reshape(-1, 1) * 2. + 1.\ny_err = np.ones_like(y_obs)\n\ntrain, test, valid = prfr.split_arrays(x_obs, y_obs, x_err, y_err, test_size=0.2, valid_size=0.2)\n\nmodel = prfr.ProbabilisticRandomForestRegressor(n_estimators=250, n_jobs=-1)\nmodel.fit(train[0], train[1], eX=train[2], eY=train[3])\nmodel.fit_bias(valid[0], valid[1], eX=valid[2])\n\n# check whether the calibration routine will run with JAX\nprint(prfr.has_jax)\n\nmodel.calibrate(valid[0], valid[1], eX=valid[2])\n\npred = model.predict(test[0], eX=test[2])\npred_qtls = np.quantile(pred, [0.16, 0.5, 0.84], axis=-1)\n\nprint(pred.shape)\n```\n',
    'author': 'Jeff Shen',
    'author_email': 'shenjeff@princeton.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/al-jshen/prfr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
