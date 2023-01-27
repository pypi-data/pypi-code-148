# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['insightly',
 'insightly.data_pipeline',
 'insightly.data_pipeline.feature_engineering',
 'insightly.data_pipeline.pre_processing',
 'insightly.parser']

package_data = \
{'': ['*'], 'insightly': ['yamls/*']}

install_requires = \
['altair==4.2.0',
 'attrs==22.2.0',
 'bpemb==0.3.4',
 'certifi==2022.12.7',
 'charset-normalizer==2.1.1',
 'contourpy==1.0.6',
 'coverage==7.0.2',
 'cycler==0.11.0',
 'entrypoints==0.4',
 'exceptiongroup==1.1.0',
 'fonttools==4.38.0',
 'gensim==3.8.3',
 'idna==3.4',
 'importlib-resources==5.10.2',
 'iniconfig==1.1.1',
 'jinja2==3.1.2',
 'joblib==1.2.0',
 'jsonschema==4.17.3',
 'kiwisolver==1.4.4',
 'markupsafe==2.1.1',
 'matplotlib==3.6.2',
 'numpy==1.24.1',
 'packaging==22.0',
 'pandas==1.5.2',
 'pillow==9.4.0',
 'pkgutil-resolve-name==1.3.10',
 'pluggy==1.0.0',
 'pyparsing==3.0.9',
 'pyrsistent==0.19.3',
 'python-dateutil==2.8.2',
 'pytz==2022.7',
 'pyyaml==6.0',
 'requests==2.28.1',
 'scikit-learn==1.2.0',
 'scipy==1.9.3',
 'sentencepiece==0.1.97',
 'six==1.16.0',
 'smart-open==6.3.0',
 'threadpoolctl==3.1.0',
 'tomli==2.0.1',
 'toolz==0.12.0',
 'tqdm==4.64.1',
 'urllib3==1.26.13',
 'whatlies==0.7.0',
 'zipp==3.11.0']

entry_points = \
{'console_scripts': ['main = insightly.main:main']}

setup_kwargs = {
    'name': 'insightly-outliers',
    'version': '1.0.1',
    'description': 'Individual work for the discipline of configuration management and software evolution at the university of Brasília - Gama for semester 2022.2',
    'long_description': '# Individual Work 2022.2\n\n## Insightly Outlier\n\n\nThe name "Insightly Outlier" was chosen for this project because it accurately describes the function of the library. The name was created by combining the words Insight - Internal Vision and outlier - anomaly. The library is designed to aid developers in exploring data and identifying outliers and anomalies, which is an essential part of understanding and making sense of data. The use of the word "Insightly" highlights the library\'s ability to provide valuable insights into the data, and the word "Outlier" specifically refers to the library\'s focus on identifying and analyzing outliers. Overall, the name "Insightly Outlier" effectively communicates the purpose of the library and its capabilities in a clear and concise manner.\n\n## Objective\n\nThe knowledge of Software Configuration Management is fundamental in the life cycle of a software product. The techniques for management range from version control, build and environment configuration automation, automated testing, environment isolation to system deployment. Today, this entire cycle is integrated into a DevOps pipeline with Continuous Integration (CI) and Continuous Deployment (CD) stages implemented and automated.\n\nTo exercise these knowledge, this work has applied the concepts studied throughout the course in the software product contained in this repository.\n\nThe system is a python library for running customizable data pipelines in databases.\n\n## Requirements\n\n- Python 3.9\n- poetry 1.3.2\n- Docker\n\n## Environment Preparation\n\n### Environment Variables\n\nTo run the project, you need to copy the `.env.example` files in the metabase/config directory with the commands below:\n```bash\ncp metabase/config/metabase.env.example metabase/config/metabase.env\ncp metabase/config/postgres.env.example metabase/config/postgres.env\ncp metabase/config/mongo.env.example metabase/config/mongo.env\n```\n\n## How to execute\n\nThe project contains a Makefile with commands to execute the project.\nTo view the available commands, run the command below:\n\n```bash\nmake help\n```\n\n### Packages\n\nThe project\'s packages can be found in the [Package Registry](https://gitlab.com/JonathanOliveira/trabalho-individual-2022.2/-/packages) of the repository or in the [PyPI](https://pypi.org/project/insightly-outliers/).\n\nTo install the package, run the command below:\n\n```bash\npip install insightly-outliers --index-url https://TI-GCES:glpat-EXagzHgL_nhmG54ytWwN@gitlab.com/api/v4/projects/42373446/packages/pypi/simple\n```\n\nor\n  \n```bash\npip install insightly-outliers \n```\n\n### Metabase\n\nAfter execute the command `docker-up-build`, the metabase will be available in the address `http://localhost:3000`, and the credentials are:\n\n- username: `admin@admin.com`\n- password: `tigce20222`',
    'author': 'Jonathan Oliveira',
    'author_email': 'jonathan.jb.oliveira@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
