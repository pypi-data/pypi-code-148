# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scSLAT',
 'scSLAT.model',
 'scSLAT.model.graphconv',
 'scSLAT.model.prematch',
 'scSLAT.viz']

package_data = \
{'': ['*']}

install_requires = \
['anndata>0.7',
 'dill>0.2.3',
 'faiss-cpu',
 'h5py',
 'harmony-pytorch',
 'harmonypy',
 'joblib',
 'leidenalg',
 'matplotlib>3.1.2',
 'numpy>1.19',
 'opencv-python',
 'packaging',
 'pandas>1.1',
 'parse>1.3.2',
 'plotly',
 'pynvml',
 'pyyaml',
 'scanpy>1.5',
 'scikit-learn>0.21.2',
 'scikit-misc',
 'scipy>1.3',
 'seaborn>0.9',
 'statsmodels>0.10',
 'tqdm>4.27']

extras_require = \
{'dev': ['pytest',
         'pytest-cov',
         'papermill',
         'snakemake',
         'ipykernel',
         'ipython',
         'jupyter'],
 'docs': ['sphinx',
          'sphinx-autodoc-typehints',
          'sphinx-copybutton',
          'sphinx-intl',
          'nbsphinx',
          'sphinx-rtd-theme',
          'sphinx_gallery>=0.8.2,<0.11',
          'jinja2',
          'myst-parser',
          'ipykernel'],
 'pyg': ['torch-scatter', 'torch-sparse', 'torch-cluster', 'torch-geometric'],
 'torch': ['torch==1.11.0']}

setup_kwargs = {
    'name': 'scslat',
    'version': '0.2.0',
    'description': 'A graph deep learning based tool to align single cell spatial omics data',
    'long_description': '[![stars-badge](https://img.shields.io/github/stars/gao-lab/SLAT?logo=GitHub&color=yellow)](https://github.com/gao-lab/SLAT/stargazers)\n[![dev-badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/xiachenrui/bc835db052fde5bd731a09270b42006c/raw/slat_version.json)](https://gist.github.com/xiachenrui/bc835db052fde5bd731a09270b42006c)\n[![build-badge](https://github.com/gao-lab/SLAT/actions/workflows/build.yml/badge.svg)](https://github.com/gao-lab/SLAT/actions/workflows/build.yml)\n[![license-badge](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![docs-badge](https://readthedocs.org/projects/slat/badge/?version=latest)](https://slat.readthedocs.io/en/latest/?badge=latest)\n\n<!-- [![pypi-badge](https://img.shields.io/pypi/v/<name>)](https://pypi.org/project/<name>) -->\n\n<!-- [![conda-badge](https://anaconda.org/bioconda/<name>/badges/version.svg)](https://anaconda.org/bioconda/<name>) -->\n\n# scSLAT: single cell spatial alignment tools\n\n**scSLAT** package implements the **SLAT** (**S**patial **L**inked **A**lignment **T**ool) model to align single cell spatial omics data.\n\n![Model architecture](docs/_static/Model.png)\n\n## Directory structure\n\n```\n.\n├── scSLAT/                  # Main Python package\n├── env/                     # Extra environment\n├── data/                    # Data files\n├── evaluation/              # SLAT evaluation pipeline\n├── benchmark/               # Benchmark pipeline\n├── case/                    # Case studies in paper\n├── docs/                    # Documentation files\n├── resource/                # Other useful resource \n├── pyproject.toml           # Python package metadata\n└── README.md\n```\n\n## Tutorial\n\nTutorial of `scSLAT` is [here](https://slat.readthedocs.io/en/latest/), if you have any question please open an issue on github\n\n\n<img src=\'docs/_static/imgalignment.gif\' width=\'400\'>\n\n## Installation\n### Docker\n\nDockerfile of `scSLAT` is available at [`env/Dockerfile`](env/Dockerfile). You can also pull the docker image directly from [here](https://hub.docker.com/repository/docker/huhansan666666/slat) by :\n```\ndocker pull huhansan666666/slat:latest\n```\n\n### Development\n> Installing `scSLAT` within a new [conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) is recommended.\n> Warning: machine with old NVIDIA driver may raise error, please update NVIDIA driver to the latest version or use Docker.\n\nFor development purpose, clone this repo and install:\n\n```bash\ngit clone git@github.com:gao-lab/SLAT.git\ncd SLAT\npip install -e ".[torch]"\npip install -e ".[pyg,dev,doc]"\n```\n\n### PyPI  (Ongoing)\n\nFist we create a clean environment and install `scSLAT` from PyPI:\n\n> We need install dependency `torch` before install `pyg`.\n\n```bash\nconda create -n scSLAT python=3.8 -y && conda activate scSLAT\npip install scSLAT[torch]\npip install scSLAT[pyg]\n```\n\n### Conda (Ongoing)\n\nWe plan to provide a conda package of `scSLAT` in the near future.\n\n## Reproduce manuscript results\n\n1. Please follow the [`env/README.md`](env/README.md) to install all dependencies. Please checkout the repository to v0.1.0 before install `scSLAT`:\n\n```\ngit clone git@github.com:gao-lab/SLAT.git\ngit checkout tags/v0.2.0\npip install -e ".[torch]"\npip install -e ".[pyg,dev,doc]"\n```\n\n2. Download and pre-process data follow the [`data/README.md`](data/README.md)\n3. Whole benchmark and evaluation procedure can be found in `/benchmark` and `/evaluation`, respectively.\n4. Every case study is recorded in the `/case` directory in the form of jupyter notebook.\n',
    'author': 'Chen-Rui Xia',
    'author_email': 'xiachenrui@mail.cbi.pku.edu.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gao-lab/SLAT',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
