# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baby_shap',
 'baby_shap.explainers',
 'baby_shap.plots',
 'baby_shap.plots.colors',
 'baby_shap.utils']

package_data = \
{'': ['*'], 'baby_shap.plots': ['resources/*']}

install_requires = \
['ipython>=8.8.0,<9.0.0',
 'matplotlib>=3.6.3,<4.0.0',
 'numba>=0.56.4,<0.57.0',
 'numpy>=1.23.1,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'scikit-learn>=1.2.1,<2.0.0',
 'slicer==0.0.7',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'baby-shap',
    'version': '0.0.1',
    'description': "A stripped and opiniated version of Scott Lundberg's SHAP (SHapley Additive exPlanations)",
    'long_description': '\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/slundberg/shap/master/docs/artwork/shap_header.svg" width="800" />\n</p>\n\n---\n![example workflow](https://github.com/thomhopmans/baby-shap/actions/workflows/run_tests.yml/badge.svg)\n\nBaby Shap is a stripped and opiniated version of **SHAP (SHapley Additive exPlanations)**, a game theoretic approach to explain the output of any machine learning model by Scott Lundberg. It connects optimal credit allocation with local explanations using the classic Shapley values from game theory and their related extensions (see [papers](#citations) for details and citations). \n\n**Baby Shap solely implements and maintains the Kernel Explainer and a limited range of plots, while limiting the number of raised errors, warnings, dependencies and conflicts.**\n\n## Install\n\nSHAP can be installed from either [PyPI](https://pypi.org/project/shap):\n\n<pre>\npip install baby-shap\n</pre>\n\n## Model agnostic example with KernelExplainer (explains any function)\n\nKernel SHAP uses a specially-weighted local linear regression to estimate SHAP values for any model. Below is a simple example for explaining a multi-class SVM on the classic iris dataset.\n\n```python\nimport sklearn\nimport shap\nfrom sklearn.model_selection import train_test_split\n\n# print the JS visualization code to the notebook\nshap.initjs()\n\n# train a SVM classifier\nX_train,X_test,Y_train,Y_test = train_test_split(*shap.datasets.iris(), test_size=0.2, random_state=0)\nsvm = sklearn.svm.SVC(kernel=\'rbf\', probability=True)\nsvm.fit(X_train, Y_train)\n\n# use Kernel SHAP to explain test set predictions\nexplainer = shap.KernelExplainer(svm.predict_proba, X_train, link="logit")\nshap_values = explainer.shap_values(X_test, nsamples=100)\n\n# plot the SHAP values for the Setosa output of the first instance\nshap.force_plot(explainer.expected_value[0], shap_values[0][0,:], X_test.iloc[0,:], link="logit")\n```\n<p align="center">\n  <img width="810" src="https://raw.githubusercontent.com/slundberg/shap/master/docs/artwork/iris_instance.png" />\n</p>\n\nThe above explanation shows four features each contributing to push the model output from the base value (the average model output over the training dataset we passed) towards zero. If there were any features pushing the class label higher they would be shown in red.\n\nIf we take many explanations such as the one shown above, rotate them 90 degrees, and then stack them horizontally, we can see explanations for an entire dataset. This is exactly what we do below for all the examples in the iris test set:\n\n```python\n# plot the SHAP values for the Setosa output of all instances\nshap.force_plot(explainer.expected_value[0], shap_values[0], X_test, link="logit")\n```\n<p align="center">\n  <img width="813" src="https://raw.githubusercontent.com/slundberg/shap/master/docs/artwork/iris_dataset.png" />\n</p>\n\n### KernelExplainer\n\nAn implementation of Kernel SHAP, a model agnostic method to estimate SHAP values for any model. Because it makes no assumptions about the model type, KernelExplainer is slower than the other model type specific algorithms.\n\n- [**Census income classification with scikit-learn**](https://slundberg.github.io/shap/notebooks/Census%20income%20classification%20with%20scikit-learn.html) - Using the standard adult census income dataset, this notebook trains a k-nearest neighbors classifier using scikit-learn and then explains predictions using `shap`.\n\n- [**ImageNet VGG16 Model with Keras**](https://slundberg.github.io/shap/notebooks/ImageNet%20VGG16%20Model%20with%20Keras.html) - Explain the classic VGG16 convolutional nerual network\'s predictions for an image. This works by applying the model agnostic Kernel SHAP method to a super-pixel segmented image.\n\n- [**Iris classification**](https://slundberg.github.io/shap/notebooks/Iris%20classification%20with%20scikit-learn.html) - A basic demonstration using the popular iris species dataset. It explains predictions from six different models in scikit-learn using `shap`.\n',
    'author': 'Thom Hopmans',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
