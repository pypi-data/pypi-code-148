# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['main']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.30,<4.0.0']

entry_points = \
{'console_scripts': ['clean_git_branches = main.__main__:start']}

setup_kwargs = {
    'name': 'clean-git-branches',
    'version': '1.0.3.2',
    'description': '',
    'long_description': '# clean-git-branches\n\nclean-git-branches is a command line utility for cleaning stale branches from your local git repository. The program will check for branches that have been deleted on the remote and prompt the user to confirm before deleting them locally.\n\n## Installation\n\nTo install clean, simply run the following command:\n\n```pip3 install clean-git-branches```\n\n\n## Usage\n\nTo use clean-git-branches, navigate to the root of your local git repository in the command line and run the following command:\n\n```clean_git_branches```\n\nIt is also possible pass the path as the first argument:\n```clean_git_branches "/Users/butler/my_repo/"```\n\nThe cleaner is set the be cautious by default, asking the user to verify deleting the local branches.\nIn order to bypass this, pass ```False``` as the second argument. Examples:\n```clean_git_branches "/Users/butler/my_repo/" False```\n```clean_git_branches "" False``` - will default the path to the current working directory\n\nThe program will then check for stale branches and prompt the user to confirm before deleting them (unless bypassed).\n\nBy default, the program will also protect certain branches from being deleted (master, main, dev) in case they exist on the remote repository. To change the list of protected branches, you can modify the "protected_branches" variable in the clean-git-branches.py file.\n\n```Please note that this program is only compatible with Git.```\n\n\n## Contributing\n\nIf you would like to contribute to the development of clean-git-branches, please feel free to fork the repository and submit pull requests with your changes.\n\n## License\n\nclean-git-branches is released under the [MIT License](https://opensource.org/licenses/MIT).\n\n',
    'author': 'Nick Holden',
    'author_email': 'holden.o.nick@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
