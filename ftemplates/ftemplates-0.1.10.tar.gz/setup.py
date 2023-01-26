# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ftemplates']

package_data = \
{'': ['*'], 'ftemplates': ['available_templates/*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['ftemp = ftemplates.cli:ftemp']}

setup_kwargs = {
    'name': 'ftemplates',
    'version': '0.1.10',
    'description': 'CLI app to create files with templates.',
    'long_description': '# ftemplates\n\nA CLI application to create files with templates.\n\n\n## Abstract\n\nThis project is a command-line interface application that allows you to create your own templates for any kind of file\nand use them to create new files easily with a few commands.\n\n## Rationale\n\nMany times the files we use follows some kind of pattern or predefined structure. Sometimes we end up writing that\nstructure ourselves to frame better some workflow. Those structures driven by conventions or personal preferences\ncommonly stay the same or change slowly. Writing them over and over again is tedious and inconsistent. Instead of\nrelying in our busy memory to rebuild the structure of some `.ipynb` or `README` files who been handy in the past,\nautomate the process with templates and a CLI.\n\n## Installation\n\n### Using pip\n```console\n$ pip install ftemplates\n```\n\n### Using poetry\n```console\n$ poetry add ftemplates  // Adding as dependency to poetry\'s pyproject.toml.\n```\n\n## Usage\n\nIn the terminal run `ftemp` or `ftemp --help` to know what to do. From there all its functionality should be easy\nto use.\n\n## Examples\n\n```console\n// List all available templates.\n$ ftemp list  \n\n// Create new file using a template.\n$ ftemp create --new-file python_template.py new_file.py\n\n// Create new template using a file.\n$ ftemp create --new-template file4template.ipynb notebook_template.ipynb\n\n// Override template with new template.\n$ ftemp create --new-template --override updated_file4template.md markdown_template.md\n```\n\n## Q&A\n\n<details>\n<summary>What was your personal motivation to create this project?</summary>\n\nI create this project to create jupyter notebook files (`.ipynb`) with a custom structure to frame data science\nworkflows better. The structure of the file was already developed by me (you can find it as the\n`data_science_notebook.ipynb` built-in template), but copying and pasting the file manually over and over was\nsuboptimal. *"I want to create notebooks with predefined structure with a simple command"* gave birth this project.\n</details>\n\n<details>\n<summary>Why the names of the commands and built-in templates are too long and explicit?</summary>\n\nThe project try to be as clear as possible enforcing legibility and intuitive usage. Reading it will be beneficial\nfor understanding. Typing it will be a curse, so make your own 2-4 character aliases, write them once and understand\nthem whenever you read them with a single look. Therefore both things will be meeting their purposes: self-documented\ncommands giving legibility and aliases giving practicality.\n</details>\n',
    'author': 'smv7',
    'author_email': 'smv7.github@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/smv7/ftemplates',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
