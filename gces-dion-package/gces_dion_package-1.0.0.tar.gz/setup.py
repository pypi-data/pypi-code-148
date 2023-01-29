# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src',
 'src.data_pipeline',
 'src.data_pipeline.feature_engineering',
 'src.data_pipeline.pre_processing',
 'src.parser']

package_data = \
{'': ['*'], 'src': ['yamls/*']}

setup_kwargs = {
    'name': 'gces-dion-package',
    'version': '1.0.0',
    'description': 'Pacote do trabalho de GCES.',
    'long_description': 'None',
    'author': 'dionvitor',
    'author_email': 'dionvictor11@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
