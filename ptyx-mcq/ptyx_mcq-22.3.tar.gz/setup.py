# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ptyx_mcq', 'ptyx_mcq.compile', 'ptyx_mcq.scan', 'ptyx_mcq.tools']

package_data = \
{'': ['*'],
 'ptyx_mcq': ['bin/*',
              'doc/*',
              'template/*',
              'template/questions/*',
              'template/scan/*']}

install_requires = \
['Pillow>=9.2,<10.0',
 'numpy>=1.23.0,<2.0.0',
 'pdf2image>=1.16.0,<2.0.0',
 'ptyx>=22.4.1,<23.0.0',
 'sympy>=1.10.1,<2.0.0',
 'types-Pillow>=9.0.20,<10.0.0']

entry_points = \
{'console_scripts': ['mcq = ptyx_mcq.cli:main'],
 'ptyx.extensions': ['mcq = ptyx_mcq']}

setup_kwargs = {
    'name': 'ptyx-mcq',
    'version': '22.3',
    'description': 'pTyX is a python precompiler for LaTeX.',
    'long_description': "pTyX MCQ Extension\n==================\n\n***Disclaimer:*** installation is broken for now (work in progress...)\n\nIf you're interested, **please wait a few months** before it becomes fully usable.\n\n(For now, the following document is only a draft documenting future usage.)\n\nOverview\n--------\npTyX is a LaTeX precompiler, written in Python.\npTyX enables to generate LaTeX documents, using custom commands or plain python code.\nOne single pTyX file may generate many latex documents, with different values.\nI developed and used pTyX to make several versions of a same test in exams,\nfor my student, to discourage cheating.\nSince it uses sympy library, pTyX has symbolic calculus abilities too.\n\nThe `pTyX MCQ extension` makes it easy to use pTyX to generate Multiple Choice Questions as pdf documents.\nThe students MCQ can then be scanned and automatically corrected and scored.\n\nInstallation\n------------\n\nObviously, pTyX needs a working Python installation.\nPython version 3.8 (at least) is required for pTyX MCQ to run.\n\nCurrently, pTyX is only supported on GNU/Linux.\n\nThe easiest way to install it is to use pip.\n\n    $ pip install --user ptyx_mcq\n\nUsage\n-----\n\nTo generate a template, run:\n\n    $ mcq new new_folder\n\nThis will generate a `new_folder/new.ptyx` file, which is the main configuration file.\n\nThis will also create a `new_folder/questions/` folder, where you should put all the exercises, \nas `.txt` files. \n\nSee the next section (*MCQ file format*) for more information about those files format.\n\nTo compile the template, run:\n\n    $ mcq make\n\nFor more options:\n\n    $ mcq make --help\n\nTo automatically corrected the scanned students MCQs, but them as a pdf inside `new_folder/scan`.\n\nThen run:\n    \n    $ mcq scan\n\n\nMCQ file format\n---------------\n\nWhen running `mcq new`, a template folder will be generated, including a `new.ptyx` file.\n\n(More to come...)\n",
    'author': 'Nicolas Pourcelot',
    'author_email': 'nicolas.pourcelot@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wxgeo/ptyx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
