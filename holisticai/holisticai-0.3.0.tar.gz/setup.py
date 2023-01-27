# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['holisticai',
 'holisticai.bias',
 'holisticai.bias.metrics',
 'holisticai.bias.mitigation',
 'holisticai.bias.mitigation.commons.disparate_impact_remover',
 'holisticai.bias.mitigation.commons.fairlet_clustering',
 'holisticai.bias.mitigation.commons.fairlet_clustering.clustering',
 'holisticai.bias.mitigation.commons.fairlet_clustering.decomposition',
 'holisticai.bias.mitigation.commons.fairlet_clustering.decompositions',
 'holisticai.bias.mitigation.inprocessing',
 'holisticai.bias.mitigation.inprocessing.adversarial_debiasing.torch',
 'holisticai.bias.mitigation.inprocessing.commons',
 'holisticai.bias.mitigation.inprocessing.commons.classification',
 'holisticai.bias.mitigation.inprocessing.commons.regression',
 'holisticai.bias.mitigation.inprocessing.exponentiated_gradient',
 'holisticai.bias.mitigation.inprocessing.fair_k_center_clustering',
 'holisticai.bias.mitigation.inprocessing.fair_k_mediam_clustering',
 'holisticai.bias.mitigation.inprocessing.fair_scoring_classifier',
 'holisticai.bias.mitigation.inprocessing.fairlet_clustering',
 'holisticai.bias.mitigation.inprocessing.grid_search',
 'holisticai.bias.mitigation.inprocessing.matrix_factorization',
 'holisticai.bias.mitigation.inprocessing.matrix_factorization.common_utils',
 'holisticai.bias.mitigation.inprocessing.matrix_factorization.debiasing_learning',
 'holisticai.bias.mitigation.inprocessing.meta_fair_classifier',
 'holisticai.bias.mitigation.inprocessing.prejudice_remover',
 'holisticai.bias.mitigation.inprocessing.two_sided_fairness',
 'holisticai.bias.mitigation.inprocessing.variational_fair_clustering',
 'holisticai.bias.mitigation.inprocessing.variational_fair_clustering.algorithm_utils',
 'holisticai.bias.mitigation.postprocessing',
 'holisticai.bias.mitigation.postprocessing.debiasing_exposure',
 'holisticai.bias.mitigation.postprocessing.fair_topk',
 'holisticai.bias.mitigation.postprocessing.fair_topk.algorithm_utils',
 'holisticai.bias.mitigation.postprocessing.lp_debiaser.binary_balancer',
 'holisticai.bias.mitigation.postprocessing.lp_debiaser.multiclass_balancer',
 'holisticai.bias.mitigation.postprocessing.mcmf_clustering',
 'holisticai.bias.mitigation.postprocessing.mcmf_clustering.utils',
 'holisticai.bias.mitigation.postprocessing.ml_debiaser',
 'holisticai.bias.mitigation.postprocessing.ml_debiaser.randomized_threshold',
 'holisticai.bias.mitigation.postprocessing.ml_debiaser.reduce2binary',
 'holisticai.bias.mitigation.postprocessing.plugin_estimator_and_recalibration',
 'holisticai.bias.mitigation.postprocessing.wasserstein_barycenters',
 'holisticai.bias.mitigation.preprocessing',
 'holisticai.bias.mitigation.preprocessing.fairlet_clustering',
 'holisticai.bias.plots',
 'holisticai.datasets',
 'holisticai.datasets.synthetic',
 'holisticai.pipeline',
 'holisticai.pipeline.handlers',
 'holisticai.utils',
 'holisticai.utils.models.cluster',
 'holisticai.utils.models.recommender',
 'holisticai.utils.models.recommender.item_selection',
 'holisticai.utils.models.recommender.matrix_factorization',
 'holisticai.utils.optimizers',
 'holisticai.utils.transformers',
 'holisticai.utils.transformers.bias']

package_data = \
{'': ['*']}

install_requires = \
['cvxopt>=1.3.0,<2.0.0',
 'cvxpy[cbc]>=1.3.0,<2.0.0',
 'scikit-learn>=1.0.2',
 'seaborn>=0.11.2',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'holisticai',
    'version': '0.3.0',
    'description': 'Holistic AI Library',
    'long_description': '<h1 align="center">\n<img src="docs/holistic_ai.png" width="100">\n<br>Holistic AI\n</h1>\n\nThe Holistic AI library is an open-source tool to assess and improve the trustworthiness of AI systems.  \n\nCurrently, the library offers a set of techniques to easily measure and mitigate Bias across numerous tasks. In the future, it will be extended to include tools for Efficacy, Robustness, Privacy and Explainability as well. This will allow a holistic assessment of AI systems.  \n\n- Documentation:https://holisticai.readthedocs.io/en/latest/ \n- Tutorials: https://github.com/holistic-ai/holisticai/tree/main/tutorials\n- Source code: https://github.com/holistic-ai/holisticai/tree/main\n- Holistic Ai website: https://holisticai.com\n\n## Installation\n\nInstall the library with:\n\n    pip install holisticai\n',
    'author': 'Research Team',
    'author_email': 'None',
    'maintainer': 'Research Team',
    'maintainer_email': 'researchteam@holisticai.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
