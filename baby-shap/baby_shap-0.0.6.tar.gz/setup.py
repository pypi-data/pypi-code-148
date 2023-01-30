# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baby_shap',
 'baby_shap.explainers',
 'baby_shap.maskers',
 'baby_shap.plots',
 'baby_shap.plots.colors',
 'baby_shap.utils']

package_data = \
{'': ['*'], 'baby_shap.plots': ['resources/*']}

install_requires = \
['ipython>=8.0.0',
 'matplotlib>=3.6.0',
 'numpy>=1.19.0',
 'pandas>=1.1.0',
 'scikit-learn>=1.0.0',
 'slicer>=0.0.7',
 'tqdm>=4.64.1']

setup_kwargs = {
    'name': 'baby-shap',
    'version': '0.0.6',
    'description': "A stripped and opiniated version of Scott Lundberg's SHAP (SHapley Additive exPlanations)",
    'long_description': '\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/slundberg/shap/master/docs/artwork/shap_header.svg" width="800" />\n</p>\n\n---\n![example workflow](https://github.com/thomhopmans/baby-shap/actions/workflows/run_tests.yml/badge.svg)\n\nBaby Shap is a stripped and opiniated version of **SHAP (SHapley Additive exPlanations)**, a game theoretic approach to explain the output of any machine learning model by Scott Lundberg. It connects optimal credit allocation with local explanations using the classic Shapley values from game theory and their related extensions (see [papers](#citations) for details and citations). \n\n**Baby Shap solely implements and maintains the Linear and Kernel Explainer and a limited range of plots, while limiting the number of dependencies, conflicts and raised warnings and errors.**\n\n## Install\n\nBaby SHAP can be installed from either [PyPI](https://pypi.org/project/baby-shap):\n\n<pre>\npip install baby-shap\n</pre>\n\n## Model agnostic example with KernelExplainer (explains any function)\n\nKernel SHAP uses a specially-weighted local linear regression to estimate SHAP values for any model. Below is a simple example for explaining a multi-class SVM on the classic iris dataset.\n\n```python\nimport baby_shap\nfrom sklearn import datasets, svm, model_selection\n\n# print the JS visualization code to the notebook\nbaby_shap.initjs()\n\n# train a SVM classifier\nd = datasets.load_iris()\nX = pd.DataFrame(data=d.data, columns=d.feature_names)\ny = d.target\n\nX_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, y, test_size=0.2, random_state=0)\nclf = svm.SVC(kernel=\'rbf\', probability=True)\nclf.fit(X_train.to_numpy(), Y_train)\n\n# use Kernel SHAP to explain test set predictions\nexplainer = baby_shap.KernelExplainer(svm.predict_proba, X_train, link="logit")\nshap_values = explainer.shap_values(X_test, nsamples=100)\n\n# plot the SHAP values for the Setosa output of the first instance\nbaby_shap.force_plot(explainer.expected_value[0], shap_values[0][0,:], X_test.iloc[0,:], link="logit")\n```\n<p align="center">\n  <img width="810" src="https://raw.githubusercontent.com/slundberg/shap/master/docs/artwork/iris_instance.png" />\n</p>\n\nThe above explanation shows four features each contributing to push the model output from the base value (the average model output over the training dataset we passed) towards zero. If there were any features pushing the class label higher they would be shown in red.\n\nIf we take many explanations such as the one shown above, rotate them 90 degrees, and then stack them horizontally, we can see explanations for an entire dataset. This is exactly what we do below for all the examples in the iris test set:\n\n```python\n# plot the SHAP values for the Setosa output of all instances\nbaby_shap.force_plot(explainer.expected_value[0], shap_values[0], X_test, link="logit")\n```\n<p align="center">\n  <img width="813" src="https://raw.githubusercontent.com/slundberg/shap/master/docs/artwork/iris_dataset.png" />\n</p>\n',
    'author': 'Thom Hopmans',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
