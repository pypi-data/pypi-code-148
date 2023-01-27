# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['process_cuwb_data',
 'process_cuwb_data.filters',
 'process_cuwb_data.honeycomb_service',
 'process_cuwb_data.utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17,<2.0',
 'click-log>=0.4.0,<0.5.0',
 'click>=8.0.0,<9.0.0',
 'matplotlib>=3.4.1,<4.0.0',
 'nocasedict>=1.0.2,<2.0.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'python-slugify>=7.0.0,<8.0.0',
 'pyyaml>=6.0,<7.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'scipy>=1.6.3,<2.0.0',
 'wf-geom-render>=0.3.0,<0.4.0',
 'wf-honeycomb-io>=2.0.0,<3.0.0',
 'wf-process-pose-data>=6.0.0,<7.0.0']

entry_points = \
{'console_scripts': ['process_cuwb_data = process_cuwb_data.cli:cli']}

setup_kwargs = {
    'name': 'wf-process-cuwb-data',
    'version': '1.6.0',
    'description': 'Tools for reading, processing, and writing CUWB data',
    'long_description': '# process_cuwb_data\n\nTools for reading, processing, and writing CUWB data\n\n### Steps\n\n1. Copy `.env.template` to `.env` and update variables\n\n\n2. Install packages\n\n    `just build`\n\n    You may need to install pybind11 `brew install pybind11`\n    And you may need to manually install cython and numpy `pip install numpy cython pythran`\n\n\n3. (Optional) Train Tray Detection Model\n    1. Download/create [ground_truth_tray_carry.csv](https://docs.google.com/spreadsheets/d/1NLQ_7Cj432T1AXFcbKLX3P6LGGGRAklxMTjtBYS_xhA/edit?usp=sharing) to `./downloads/ground_truth_tray_carry.csv`\n```\n    curl -L \'https://docs.google.com/spreadsheets/d/1NLQ_7Cj432T1AXFcbKLX3P6LGGGRAklxMTjtBYS_xhA/export?exportFormat=csv\' --output ./downloads/ground_truth_tray_carry.csv\n```\n3.\n   2. Generate pickled groundtruth features dataframe from ground_truth_tray_carry.csv\n```\n    process_cuwb_data \\\n        generate-tray-carry-groundtruth \\\n        --groundtruth-csv ./downloads/ground_truth_tray_carry.csv\n```\n\n3.\n    3. Train and pickle Tray Carry Detection Model using pickled groundtruth features\n\n```\n    process_cuwb_data \\\n        train-tray-carry-model \\\n        --groundtruth-features ./output/groundtruth/2021-05-13T12:53:26_tray_carry_groundtruth_features.pkl\n```\n\n4. Infer Tray Interactions using pickled Tray Carry Detection Model\n    1. Use the model you\'ve trained by following step 3\n    2. Or, download the latest model:\n```\n    curl -L \'https://drive.google.com/uc?export=download&id=1_veyjLdAa8Fq7eYeT9GLdkcS6_VY0FLX\' --output ./output/models/tray_carry_model_v1.pkl\n```   \n\nThen use the model to infer tray interactions:\n```\n    process_cuwb_data \\\n      infer-tray-interactions \\\n      --environment greenbrier \\\n      --start 2021-04-20T9:00:00-0500 \\\n      --end 2021-04-20T9:05:00-0500 \\\n      --tray-carry-model ./output/models/tray_carry_model_v1.pkl\n```\n\n### Other CLI Commands/Options\n\n#### Export pickled UWB data\n\nWorking with Honeycomb\'s UWB endpoint can be painfully slow. For that reason there is an option to export pickled UWB data and provide that to subsequent inference commands.\n\n        process_cuwb_data \\\n            fetch-cuwb-data \\\n            --environment greenbrier \\\n            --start 2021-04-20T9:00:00-0500 \\\n            --end 2021-04-20T9:05:00-0500\n\n\n#### Use UWB export to run Tray Interaction Inference\n\n        process_cuwb_data \\\n            infer-tray-interactions \\\n            --environment greenbrier \\\n            --start 2021-04-20T9:00:00-0500 \\\n            --end 2021-04-20T9:05:00-0500 \\\n            --tray-carry-model ./output/models/2021-05-13T14:49:32_tray_carry_model.pkl \\\n            --cuwb-data ./output/uwb_data/uwb-greenbrier-20210420-140000-20210420-140500.pkl\n\n#### Supply Pose Track Inference to Tray Interaction Inference\n\nUse Pose Tracks when determining nearest person to tray carry events.\n\nPose Inferences need to be sourced in a local directory. The pose directory can be supplied via CLI options.\n\n        process_cuwb_data \\\n            infer-tray-interactions \\\n            --environment greenbrier \\\n            --start 2021-04-20T9:00:00-0500 \\\n            --end 2021-04-20T9:05:00-0500 \\\n            --tray-carry-model ./output/models/2021-05-13T14:49:32_tray_carry_model.pkl \\\n            --cuwb-data ./output/uwb_data/uwb-greenbrier-20210420-140000-20210420-140500.pkl \\\n            --pose-inference-id 3c2cca86ceac4ab1b13f9f7bfed7834e\n\n### Development\n\n#### MacOS (Monterey)\n\n1) Install **pyenv**:\n\n\n    brew install pyenv\n\n2) Create a 3.x venv:\n\n\n    pyenv virtualenv 3.x.x wf-process-cuwb-data\n\n3) Set ENV\n\n\nThis was helpful after the transition from macOS X to macOS 11. As packages evolve, this may not be needed depending on exact Mac version and python version. e.g. macOS 12 with Python 3.10 doesn\'t require the env var\n\n\n    export SYSTEM_VERSION_COMPAT=1\n\n4) Install scipy dependencies:\n\n    \n    brew install openblas lapack pythran pybind11\n    \n    export OPENBLAS=$(brew --prefix openblas)\n    export CFLAGS="-falign-functions=8 ${CFLAGS}"\n\n5) Install python libraries\n\n\n    pip install numpy cython pythran\n\n6) Install add\'l packages:\n\n\n    just install-dev\n\n',
    'author': 'Theodore Quinn',
    'author_email': 'ted.quinn@wildflowerschools.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/WildflowerSchools/wf-process-cuwb-data',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
