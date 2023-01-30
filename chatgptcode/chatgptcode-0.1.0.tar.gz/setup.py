# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chatgptcode']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'pygments>=2.14.0,<3.0.0',
 'revChatGPT>=0.3.1,<0.4.0',
 'termcolor>=2.2.0,<3.0.0',
 'twocaptcha>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'chatgptcode',
    'version': '0.1.0',
    'description': 'A command line tool for interacting with ChatGPT to help with development',
    'long_description': '# Chat GPT Code\nThis extension is for terminal based AI assisted programming. It takes advantage of the ChatGPT python package and has additional formatting to make it easier to use for developers.\n\n## Installation\nI\'ll publish a pip package soon, but for now you can install it by cloning the repo and running the following from the project\'s root directory.\n```bash\n> git clone https://github.com/BrianKmdy/ChatGPTCode.git\n> cd ChatGPTCode\n> pip install poetry\n> poetry install\n```\n\n## Setup\nCreate a file called `config.json` in folder `.gptcode` in your home directory. The file should be formatted as follows, where `session_token` referers to the `__Secure-next-auth.session-token` to the browser cookie found on the chat GPT website ([see terry3041\'s guide for additional info](https://github.com/terry3041/pyChatGPT)):\n\n```json\n{\n  "session_token": "eyJhbGciOiJkaXIiL...",\n}\n```\n\n## Usage\nTo run the app with poetry use the following command. In order for this to work you\'ll need to have chrome or chromium installed. A browser instance will pop up, connect to chat GPT, and then will automatically be hidden from view.\n```bash\n> poetry run python -m gptcode\n```\n\nYou can then ask chat GPT questions and get a response in your terminal! With nicely formatted code and easy to read output.\n\nThanks so much to user [acheong08](https://github.com/acheong08) for the amazing [ChatGPT Python package](https://github.com/acheong08/ChatGPT) which this is based on!',
    'author': 'Brian Moody',
    'author_email': 'brian.kmdy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
