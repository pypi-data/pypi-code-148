# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cdcstream']

package_data = \
{'': ['*']}

install_requires = \
['numpy',
 'packaging',
 'pandas',
 'python-javabridge',
 'python-weka-wrapper3>=0.2,<0.3']

setup_kwargs = {
    'name': 'cdcstream',
    'version': '0.2.2',
    'description': "Implementation of Ienco's algorithm CDCStream",
    'long_description': "Cite this work as (BibTex):\n```\n@techreport{TratBenderOvtcharova2023_1000155196,\n    author       = {Trat, Martin and Bender, Janek and Ovtcharova, Jivka},\n    year         = {2023},\n    title        = {Sensitivity-Based Optimization of Unsupervised Drift Detection for Categorical Data Streams},\n    doi          = {10.5445/IR/1000155196},\n    institution  = {{Karlsruher Institut für Technologie (KIT)}},\n    issn         = {2194-1629},\n    series       = {KIT Scientific Working Papers},\n    keywords     = {unsupervised conceptdriftdetection, data streammining, productiveartificialintelligence, categorical data processing},\n    pagetotal    = {10},\n    language     = {english},\n    volume       = {208}\n}\n```\n\nImplementation of an augmented version of Dino Ienco's algorithm **CDCStream** (Change Detection in Categorical Evolving Data Streams) ([https://doi.org/10.1145/2554850.2554864](https://doi.org/10.1145/2554850.2554864)).\n\n## Requirements\nPlease note that several requirements need to be fulfilled in order to run the software.\nSee repository readme for details.\n\n## Acknowledgements\nThis software was developed at the FZI Research Center for Information Technology.\nThe associated research was funded by the German Federal Ministry of Education and Research (grant number: 02K18D033) within the context of the project SEAMLESS.\n",
    'author': 'Martin Trat',
    'author_email': 'trat@fzi.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fzi-forschungszentrum-informatik/cdcstream',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
