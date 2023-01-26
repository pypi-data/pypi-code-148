# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['learning_pipeline_plugin', 'learning_pipeline_plugin.algorithms']

package_data = \
{'': ['*']}

install_requires = \
['actfw-core>=2.2.0,<3.0.0',
 'numpy>=1,<2',
 'requests>=2.28.1,<3.0.0',
 'typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'learning-pipeline-plugin',
    'version': '0.2.0',
    'description': '',
    'long_description': '# learning-pipeline-plugin\n\n\n## Installation\n\n```console\nsudo apt-get update\nsudo apt-get install -y python3-pip python3-pil\n\npip3 install poetry\npoetry build\npip3 install dist/learning_pipeline_plugin-<PACKAGE_VERSION>.whl\n```\n\n\n## Usage\n\nTo collect data, create a pipe that inherits from `learning_pipeline_plugin.collect_pipe.CollectPipeBase`\nand define `interpret_inputs()`.\n\nExample:\n```python\nfrom typing import Optional\nfrom learning_pipeline_plugin.collect_pipe import CollectPipeBase, DataDict\n\nclass CollectPipe(CollectPipeBase):\n    def interpret_inputs(self, inputs) -> Optional[DataDict]:\n        img, probs, feature = inputs\n        return {\n            "image": img,\n            "feature_vector": feature,\n            "other_data": {\n                "probabilities": probs\n            }\n        }\n```\n\n`interpret_inputs()` gets the previous pipe output and must return `DataDict` or `None`.\n\n`DataDict` is TypedDict for type hint, and must have following properties:\n\n- `image`: PIL.Image\n- `feature_vector`: vector with shape (N,)\n- `other_data`: any data used for calculating uncertainty\n\nThen, instantiate this and connect to other pipes:\n\n```python\ndef main():\n    [...]\n\n    collect_pipe = CollectPipe(...)\n\n    prev_pipe.connect(collect_pipe)\n    collect_pipe.connect(after_pipe)\n```\n',
    'author': 'Idein Inc.',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Idein/learning-pipeline-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<3.8',
}


setup(**setup_kwargs)
