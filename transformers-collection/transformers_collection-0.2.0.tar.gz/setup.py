# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transformers_collection', 'transformers_collection.models']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=2.8.0,<3.0.0',
 'evaluate>=0.4.0,<0.5.0',
 'loguru>=0.6.0,<0.7.0',
 'munch>=2.5.0,<3.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pytorch-lightning>=1.9.0,<2.0.0',
 'scikit-learn>=1.2.1,<2.0.0',
 'scipy>=1.10.0,<2.0.0',
 'tensorboard>=2.11.2,<3.0.0',
 'torch>1.10,<2.0',
 'transformers>=4.26.0,<5.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['transformers-collection = '
                     'transformers_collection.__main__:app']}

setup_kwargs = {
    'name': 'transformers-collection',
    'version': '0.2.0',
    'description': 'A collection of transformer models built  using huggingface for various tasks.',
    'long_description': '# transformers-collection\n- A collection of transformer models built  using huggingface for various tasks. Training done using pytorch lightning.\n- Datasets, models and tokenizers from hugging face.\n- **Goal**: Get familiar with huggingface and pytorch lightning ecosystems.\n\n## Get started\n### Train Models using the library\n- To train models, install using pip: `pip install transformers_collection`\n- check installation: `transformers-collection version`\n\n### Clone project and modify code\nTo play around with the code clone the repo:\n- `git clone git@github.com:aadhithya/transformers-collection.git`\n- Install poetry: `pip install poetry`\n- Intsall dependencies: `poetry install`\n\n**Note:** `poetry install` will create a new venv.\n**Note**: `poetry/pip install` installs CPU version of pytorch if not available, please make sure to install CUDA version if needed.\n\n\n## Train a model\n- Create the yaml config file for the model (see configs/sentiment-clf.yml for example).\n- train model using: `transformers-collection train /path/to/config.yml`\n\n- For a list of supported models, see section Supported Models.\n\n\n\n## Supported Models / Task\nThe following models are planned:\n| Model                            |                      Dataset                       |  Status   | Checkpoint |\n| :------------------------------- | :------------------------------------------------: | :-------: | ---------: |\n| Sentiment/Emotion Classification | [emotion](https://huggingface.co/datasets/emotion) |     ✅     |        TBD |\n| Text Summarization               |                                                    | 🗓️ Planned |        TBD |\n',
    'author': 'Aadhithya Sankar',
    'author_email': 'aadhithya.s@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aadhithya/transformers-collection',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
