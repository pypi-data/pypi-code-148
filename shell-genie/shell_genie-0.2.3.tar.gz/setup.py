# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shell_genie']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.26.1,<0.27.0',
 'pyperclip>=1.8.2,<2.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['shell-genie = shell_genie.main:app']}

setup_kwargs = {
    'name': 'shell-genie',
    'version': '0.2.3',
    'description': '',
    'long_description': '# 🧞\u200d♂️ Shell Genie\n\n_Your wishes are my commands._\n\nShell Genie is a command-line tool that lets you interact with the terminal in plain English. You ask the genie what you want to do and it will generate the command for you.\n\n## Installation\n\nThe recommended way to install is using [pipx](https://pypa.github.io/pipx/):\n\n1. Install Python 3.10 or higher.\n2. Install [pipx](https://github.com/pypa/pipx#install-pipx).\n3. Install Shell Genie: `pipx install shell-genie`\n\nAlternatively, you can install it using pip:\n\n1. Install Python 3.10 or higher.\n2. Install Shell Genie: `pip install shell-genie`\n\n## How to use\n\n1. First, you need to initialize the tool by running the following command:\n\n   ```shell\n   shell-genie init\n   ```\n\n   This will prompt you to select a backend (either `openai-gpt3` or `free-genie`) and provide any additional information that is required (e.g. your own [OpenAI API](https://openai.com/api/) key for `openai-gpt3`).\n\n   The `free-genie` backend is free to use. I\'m hosting, but as you can imagine I\'m not a big corporation with unlimited money, so there\'s no guarantee that it will be available at all times. My goal is to generate a dataset of commands to fine-tune a model later on (this is mentioned during the initialization process).\n\n2. Once you have initialized the tool, you can start asking the genie what you want to do. For example, you may ask it to find all the `json` files in the current directory that are larger than 1MB:\n\n   ```shell\n   shell-genie ask "find all json files in the current directory that are larger than 1MB"\n   ```\n\n   You\'ll see an output similar to this:\n\n   ```shell\n   Command: find . -name "*.json" -size +1M\n   Do you want to run this command? [y/n]:\n   ```\n\n   If you have questions about how the command works, you can ask the genie to explain it:\n\n   ```shell\n   shell-genie ask "find all json files in the current directory that are larger than 1MB" --explain\n   ```\n\n   And you\'ll see an output similar to this:\n\n   ```shell\n   Command: find . -name "*.json" -size +1M\n   Description: This command will search the current directory for all... (shortened for brevity)\n   Do you want to run the command? [y/n]:\n   ```\n\n3. Run the command if you want to. If you\'re using `free-genie`, and you want to help improve the tool, you can provide feedback after you\'ve run the command.\n\n## Examples\n\nHere\'s a short video showing how to use the tool:\n\n[![asciicast](https://asciinema.org/a/438574.svg)](https://asciinema.org/a/438574)\n',
    'author': 'Dylan Castillo',
    'author_email': 'dylanjcastillo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
