# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_genie']

package_data = \
{'': ['*']}

install_requires = \
['langchain>=0.0.71,<0.0.72',
 'openai>=0.26.4,<0.27.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['git-genie = git_genie.main:app']}

setup_kwargs = {
    'name': 'git-genie',
    'version': '0.1.0',
    'description': '',
    'long_description': '# git-genie\n\nGenerate & explain git commands using plain english.\n\n## Installation\n\n```bash\npip install git-genie\n```\n\n## Usage\n\n`❯ git-genie [OPTIONS] INSTRUCTION`\n\nOptions:\n - --explain, -e: Explain the generated git command automatically.\n - --execute, -x: Execute the generated git command automatically.\n - --install-completion: Install completion for the current shell.\n - --show-completion: Show completion for the current shell, to copy it or customize the installation.\n - --help, -h: Show this message and exit.\n\nIf no options are provided, the program will run in interactive mode.\n\nOptionally, you can add a "gg" alias to your shell\'s rc file (e.g. ~/.bashrc) to make the command shorter:\n\n```bash\nalias gg="git-genie"\n```\n\n### Pre-requisites\n\n#### OpenAI API key\n\n```shell\nexport OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n```\n\n### Interactive mode\n\n```bash\n~/git-genie ❯ git-genie "count how many times the README.md file was modified in the last week"\n\nGenerated git command: git log --since=1.week -- README.md | grep "^commit" | wc -l\n\n(E)xplain or e(X)ecute or (N)ew?: E\n\nExplanation\n git log -> Show commit logs\n--since=1.week -> Show commits more recent than a specific date\n-- README.md -> Only commits that affect README.md\n| -> Pipe the output of the previous command to the next command\ngrep "^commit" -> Only show lines that start with "commit"\nwc -l -> Count the number of lines\n\ne(X)ecute or (N)ew?: X\n\nRunning command:  git log --since=1.week -- README.md | grep "^commit" | wc -l\nOutput:\n       2\n```\n\n### Non-interactive mode\n\n#### Explain\n\n```bash\n~/git-genie ❯ git-genie "amend all previous commits with new email address" --explain\n\nGenerated git command:  git rebase -i HEAD~5 --autosquash -m "legacy code"\n\nExplanation\n\n git rebase -> Forward-port local commits to the updated upstream head\n-i, --interactive -> Make a list of the commits which are about to be rebased.Let the user edit that list before rebasing.\n--autosquash -> Automatically move commits that begin with squash!/fixup! to the beginningof the todo list.\n-m, --merge -> Use the given message as the merge commit message.If multiple -m options are given, their values are concatenated as separate paragraphs.\nHEAD~5 -> The last 5 commits\nlegacy code -> The message of the merge commit\n```\n\n#### Execute\n\n```bash\n~/git-genie ❯ git-genie "print last 5 commits logs, condensed" --execute\n\nGenerated git command:  git log -5 --oneline\n\nRunning command:  git log -5 --oneline\n\nOutput:\n9a33bc3 update email\nf76f041 CLI interface\nae8abbd Add pycache to gitignore\n67169fd rich print\n3bac238 Refactor\n```\n',
    'author': 'Daniel Palma',
    'author_email': 'danivgy@gmail.com',
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
