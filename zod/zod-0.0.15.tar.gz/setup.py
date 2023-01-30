# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zod',
 'zod.cli',
 'zod.frames.evaluation.object_detection',
 'zod.frames.evaluation.object_detection.nuscenes_eval.common',
 'zod.frames.evaluation.object_detection.nuscenes_eval.detection',
 'zod.frames.polygon_annotations',
 'zod.frames.traffic_sign_classification',
 'zod.utils',
 'zod.visualization',
 'zod.zod_dataclasses']

package_data = \
{'': ['*'], 'zod.frames.evaluation.object_detection': ['nuscenes_eval/*']}

install_requires = \
['dataclass-wizard>=0.22.2',
 'h5py>=3.1,<4.0',
 'numpy-quaternion>=2022.4.2,<2023.0.0',
 'numpy>=1.19,<2.0',
 'pyquaternion>=0.9',
 'scipy>=1.5,<2.0',
 'tqdm>=4.60']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 ':python_version >= "3.8" and python_version < "4.0" and sys_platform == "darwin"': ['numpy>=1.21,<2.0',
                                                                                      'scipy>=1.9,<2.0',
                                                                                      'h5py>=3.3,<4.0'],
 'all': ['typer[all]>=0.7.0,<0.8.0',
         'dropbox>=11.36.0,<12.0.0',
         'opencv-python>=4,<5',
         'pyproj>=3,<4',
         'matplotlib>=3,<4',
         'plotly>=5.11.0,<6.0.0',
         'pandas'],
 'cli': ['typer[all]>=0.7.0,<0.8.0', 'dropbox>=11.36.0,<12.0.0']}

entry_points = \
{'console_scripts': ['zod = zod.cli.main:app']}

setup_kwargs = {
    'name': 'zod',
    'version': '0.0.15',
    'description': 'Zenseact Open Dataset',
    'long_description': '# Zenseact Open Dataset\nThe Zenseact Open Dataset (ZOD) is a large multi-modal autonomous driving dataset developed by a team of researchers at [Zenseact](https://zenseact.com/). The dataset is split into three categories: *Frames*, *Sequences*, and *Drives*. For more information about the dataset, please refer to our [coming soon](), or visit our [website](https://zenseact.github.io/zod-web/).\n\n## Examples\nFind examples of how to use the dataset in the [examples](examples/) folder. Here you will find a set of jupyter notebooks that demonstrate how to use the dataset, as well as an example of how to train an object detection model using [Detectron2](https://github.com/facebookresearch/detectron2).\n\n## Installation\n\nTo install the full devkit, including the CLI, run:\n```bash\npip install zod[cli]\n```\n\nElse, to install the library only, run:\n```bash\npip install zod\n```\n\n## Download using the CLI\n\nThis is an example of how to download the ZOD Frames mini-dataset using the CLI. Prerequisites are that you have applied for access and received a download link. To download the mini-dataset, run:\n```bash\nzod download --url <download-link> --output-dir <path/to/outputdir> frames --mini\n```\nsimilarly, to download the full dataset, run:\n```bash\nzod download --url <download-link> --output-dir <path/to/outputdir> frames --lidar -num-scans-before -1 --num-scans-after -1 --oxts --images --blur --dnat ---calibrations --annotations\n```\nthis will download all the previous and future lidar scans (num-scans-before and num-scans-after), the OxTS data, the images (with both the blur and DNAT anonymization), the calibration files, the annotations, and all other necessary files. For a full list of options for ZOD download, run:\n```bash\nzod download frames --help\nzod download sequences --help\n```\ndepending on which dataset you want to download.\n\n\n## Anonymization\nTo preserve privacy, the dataset is anonymized. The anonymization is performed by [brighterAI](https://brighter.ai/), and we provide two separate modes of anonymization: deep fakes (DNAT) and blur. In our paper, we show that the performance of an object detector is not affected by the anonymization method. For more details regarding this experiment, please refer to our [coming soon]().\n\n## Citation\nIf you publish work that uses Zenseact Open Dataset, please cite: [coming soon]()\n\n```\n@misc{zod2021,\n  author = {TODO},\n  title = {Zenseact Open Dataset},\n  year = {2023},\n  publisher = {TODO},\n  journal = {TODO},\n```\n\n## Contact\nFor questions about the dataset, please [Contact Us](mailto:opendataset@zenseact.com).\n\n## Contributing\nWe welcome contributions to the development kit. If you would like to contribute, please open a pull request.\n\n## License\n**Dataset**:\nThis dataset is the property of Zenseact AB (© 2023 Zenseact AB) and is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Any public use, distribution, or display of this dataset must contain this notice in full:\n\n> For this dataset, Zenseact AB has taken all reasonable measures to remove all personally identifiable information, including faces and license plates. To the extent that you like to request the removal of specific images from the dataset, please contact [privacy@zenseact.com](mailto:privacy@zenseact.com).\n\n\n**Development kit**:\nThis development kit is the property of Zenseact AB (© 2023 Zenseact AB) and is licensed under [MIT](https://opensource.org/licenses/MIT).\n',
    'author': 'Zenseact',
    'author_email': 'opendataset@zenseact.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://zod.zenseact.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
