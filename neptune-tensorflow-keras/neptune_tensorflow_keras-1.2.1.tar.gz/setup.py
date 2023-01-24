# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['neptune_tensorflow_keras', 'neptune_tensorflow_keras.impl']

package_data = \
{'': ['*']}

install_requires = \
['neptune-client>=0.16.7', 'tensorflow>2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata'],
 'dev': ['pre-commit', 'pytest>=5.0', 'pytest-cov==2.10.1', 'pydot']}

setup_kwargs = {
    'name': 'neptune-tensorflow-keras',
    'version': '1.2.1',
    'description': 'Neptune.ai tensorflow-keras integration library',
    'long_description': '# Neptune + TensorFlow/Keras Integration\n\nExperiment tracking, model registry, data versioning, and live model monitoring for TensorFlow/Keras trained models.\n\n## What will you get with this integration?\n\n* Log, display, organize, and compare ML experiments in a single place\n* Version, store, manage, and query trained models, and model building metadata\n* Record and monitor model training, evaluation, or production runs live\n* Collaborate with a team\n\n## What will be logged to Neptune?\n\n* hyperparameters for every run,\n* learning curves for losses and metrics during training,\n* hardware consumption and stdout/stderr output during training,\n* TensorFlow tensors as images to see model predictions live,\n* training code and git commit information,\n* model weights\n* [other metadata](https://docs.neptune.ai/you-should-know/what-can-you-log-and-display)\n\n![image](https://user-images.githubusercontent.com/97611089/160638338-8a276866-6ce8-4d0a-93f5-bd564d00afdf.png)\n*Example charts in the Neptune UI with logged accuracy and loss*\n\n\n## Resources\n\n* [Documentation](https://docs.neptune.ai/integrations-and-supported-tools/model-training/tensorflow-keras)\n* [Code example on GitHub](https://github.com/neptune-ai/examples/blob/main/integrations-and-supported-tools/tensorflow-keras/scripts)\n* [Runs logged in the Neptune app](https://app.neptune.ai/o/common/org/tf-keras-integration/e/TFK-18/all)\n* [Run example in Google Colab](https://colab.research.google.com/github/neptune-ai/examples/blob/master/integrations-and-supported-tools/tensorflow-keras/notebooks/Neptune_TensorFlow_Keras.ipynb)\n\n## Example\n\n```python\n# On the command line:\npip install tensorflow neptune-client neptune-tensorflow-keras\n```\n```python\n# In Python:\nimport neptune.new as neptune\nfrom neptune.new.integrations.tensorflow_keras import NeptuneCallback\n\n\n# Start a run\nrun = neptune.init(project="common/tf-keras-integration",\n                   api_token="ANONYMOUS")\n\n\n# Create a NeptuneCallback instance\nneptune_cbk = NeptuneCallback(run=run, base_namespace="metrics")\n\n\n# Pass the callback to model.fit()\nmodel.fit(x_train, y_train,\n          epochs=5,\n          batch_size=64,\n          callbacks=[neptune_cbk])\n\n\n# Stop the run\nrun.stop()\n```\n\n## Support\n\nIf you got stuck or simply want to talk to us, here are your options:\n\n* Check our [FAQ page](https://docs.neptune.ai/getting-started/getting-help#frequently-asked-questions)\n* You can submit bug reports, feature requests, or contributions directly to the repository.\n* Chat! When in the Neptune application click on the blue message icon in the bottom-right corner and send a message. A real person will talk to you ASAP (typically very ASAP),\n* You can just shoot us an email at support@neptune.ai\n',
    'author': 'neptune.ai',
    'author_email': 'contact@neptune.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://neptune.ai/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
