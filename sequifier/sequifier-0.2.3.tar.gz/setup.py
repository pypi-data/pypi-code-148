# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sequifier', 'sequifier.config']

package_data = \
{'': ['*']}

install_requires = \
['numpy==1.23.5',
 'onnxruntime==1.12.1',
 'pandas==1.5.2',
 'poetry==1.3.2',
 'pydantic==1.10.2',
 'pytest==7.2.1',
 'pyyaml==5.3.1']

entry_points = \
{'console_scripts': ['sequifier = sequifier.sequifier:main']}

setup_kwargs = {
    'name': 'sequifier',
    'version': '0.2.3',
    'description': 'Train a transformer model with the command line',
    'long_description': '<img src="./design/logo.png">\n\n\n## Overview\nThe sequifier package enables:\n  - the extraction of sequences for training from a standardised format\n  - the configuration and training of a transformer classification model\n  - inference on data with a trained model\n\nEach of these steps is explained below.\n\n\n## Preprocessing of data into sequences for training\n\nThe preprocessing step is specifically designed for scenarios where for long series\nof events, the prediction of the next event from the previous N events  is of interest.\nIn cases of sequences where only the last item is a valid target, the  preprocessing\nstep does not apply.\n\nThis step presupposes input data with three columns: sequenceId, itemId and timesort.\nsequenceId and itemId identify sequence and item, and the timesort column must\nprovide values that enable sequential sorting. Often this will simply be a timestamp.\n\nThe data can then be processed into training, validation and testing datasets of all\nvalid subsequences in the original data with the command:\n\n> sequifier --preprocess --config_path=[CONFIG PATH] --project_path=[PROJECT PATH]\n\nThe config path specifies the path to the preprocessing config and the project\npath the path to the (preferably empty) folder the output files of the different\nsteps are written to.\n\nThe default config can be found on this path:\n\n> configs/preprocess/default.yaml\n\n\n## Configuring and training the sequence classification model\n\nThe training step is executed with the command:\n\n> sequifier --train --config_path=[CONFIG PATH] --project_path=[PROJECT PATH]\n\nIf the data on which the model is trained comes from the preprocessing step, the flag\n\n> --on-preprocessed\n\nshould also be added.\n\nIf the training data does not come from the preprocessing step, both train and validation\ndata have to take the form of a csv file with the columns:\n\n> sequenceId, seq_length, seq_length-1,...,1, target\n\nThe training step is configured using the config. The two default configs can be found here:\n\n> configs/train/default.yaml\n\n> configs/train/default-on-preprocessed.yaml\n\n\n## Inferring on test data using the trained model\n\nInference is done using the command:\n\n> sequifier --infer --config_path=[CONFIG PATH] --project_path=[PROJECT PATH]\n\nand configured using a config file. The default version can be found here:\n\n> configs/infer/default.yaml\n\n\n## Complete example how to use the repository\n\n1. create a new project folder at PROJECT PATH and a "configs" subfolder\n2. copy default configs from repository for preprocessing, training and inference and name them preprocess.yaml, train.yaml and infer.yaml\n3. adapt preprocess config to take the path to the data you want to preprocess\n4. run \n> sequifier --preprocess --config_path=[PROJECT PATH]/configs/preprocess.yaml --project_path=[PROJECT PATH]\n5. adapt dd_config parameter in train.yaml and infer.yaml in to dd_config path from preprocessing\n6. run \n> sequifier --train --on-preprocessed --config_path=[PROJECT PATH]/configs/train.yaml --project_path=[PROJECT PATH]\n7. adapt inference_data_path in infer.yaml\n8. run  \n> sequifier --infer --config_path=PROJECT PATH]/configs/infer.yaml --project_path=[PROJECT PATH]\n9. find your predictions at [PROJECT PATH]/outputs/predictions/sequifier-default-best_predictions.csv\n',
    'author': 'Leon Luithlen',
    'author_email': 'leontimnaluithlen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/0xideas/sequifier',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.9.12',
}


setup(**setup_kwargs)
