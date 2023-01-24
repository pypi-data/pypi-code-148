# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multi_repo_automation']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML', 'identify', 'requests', 'ruamel.yaml']

extras_require = \
{'update-stabilization-branches': ['c2cciutils']}

setup_kwargs = {
    'name': 'multi-repo-automation',
    'version': '0.1.0',
    'description': 'Library for automation updates on multiple repositories.',
    'long_description': '# Multi repo automation\n\n## Config\n\nCreate a file with something like this:\n\n```yaml\n- dir: /home/user/src/myrepo\n  name: user/myrepo\n  types: [\'javascript\', \'python\', \'docker\']\n  master_branch: master\n  stabilization_branches: [1.0, 1.1]\n  folders_to_clean: []\n```\n\n## Utilities\n\n```python\nimport multi_repo_automation as mra\n\n# Test if a file exists\nif mra.run(["git", "ls-files", "**/*.txt"], stdout=subprocess.PIPE).stdout.strip() != b"":\n  print("Found")\n# Test if a file exists and contains a text\nif mra.git_grep(file, r"\\<text\\>"]):\n  print("Found")\n# Edit a file in vscode\nmra.edit("file")\n```\n\n## To do something on all repo that not depends on the branch\n\n```python\n#!/usr/bin/env python3\nimport argparse\nimport multi_repo_automation as mra\n\ndef _main() -> None:\n    with open(os.path.join(os.path.dirname(__file__), "repo.yaml"), encoding="utf-8") as f:\n        repos = yaml.load(f.read(), Loader=yaml.SafeLoader)\n\n    args_parser = argparse.ArgumentParser(description="Apply an action on all the repos.")\n    args = args_parser.parse_args()\n\n    pull_request_created_message = []\n    try:\n        for repo in repos:\n                try:\n                    print(f"=== {repo[\'name\']} ===")\n                    with mra.Cwd(repo):\n                        # Do something\n                finally:\n                    print(f"=== {repo[\'name\']} ===")\n    finally:\n        print(f"{len(pull_request_created_message)} pull request created")\n        for repo in pull_request_created_message:\n            print(repo)\n\nif __name__ == \'__main__\':\n  _main()\n```\n\n## To update all the master branches write a script like\n\n```python\n#!/usr/bin/env python3\nimport argparse\nimport multi_repo_automation as mra\n\ndef _main() -> None:\n    with open(os.path.join(os.path.dirname(__file__), "repo.yaml"), encoding="utf-8") as f:\n        repos = yaml.load(f.read(), Loader=yaml.SafeLoader)\n\n    args_parser = argparse.ArgumentParser(description="Apply an action on all the repos.")\n    args = args_parser.parse_args()\n\n    pull_request_created_message = []\n    try:\n        for repo in repos:\n                try:\n                    print(f"=== {repo[\'name\']} ===")\n                    with mra.Cwd(repo):\n                        pull_request_created_message.extend(_do(repo))\n                finally:\n                    print(f"=== {repo[\'name\']} ===")\n    finally:\n        print(f"{len(pull_request_created_message)} pull request created")\n        for repo in pull_request_created_message:\n            print(repo)\n\nif __name__ == \'__main__\':\n  _main()\n\ndef _do(repo: mra.Repo) -> List[str]:\n    create_branch = mra.CreateBranch(\n        repo,\n        "branch_name",\n        "Commit/Pull request message",\n    )\n    with create_branch:\n        # Do something\n\n    if create_branch.pull_request_created:\n        if create_branch.message:\n            return [create_branch.message]\n        else:\n            return [f"https://github.com/{repo[\'name\']}/pulls"]\n  return []\n```\n\n## To update all the stabilization branches write a script like\n\n```python\n#!/usr/bin/env python3\nimport argparse\nimport multi_repo_automation as mra\n\ndef _main() -> None:\n    with open(os.path.join(os.path.dirname(__file__), "repo.yaml"), encoding="utf-8") as f:\n        repos = yaml.load(f.read(), Loader=yaml.SafeLoader)\n\n    args_parser = argparse.ArgumentParser(description="Apply an action on all the repos.")\n    args = args_parser.parse_args()\n\n    pull_request_created_message = []\n    try:\n        for repo in repos:\n                try:\n                    print(f"=== {repo[\'name\']} ===")\n                    with mra.Cwd(repo):\n                        pull_request_created_message.extend(\n                          do_on_base_branches(repo:, \'branch_prefix\' , _do)\n                finally:\n                    print(f"=== {repo[\'name\']} ===")\n    finally:\n        print(f"{len(pull_request_created_message)} pull request created")\n        for repo in pull_request_created_message:\n            print(repo)\n\nif __name__ == \'__main__\':\n  _main()\n\ndef _do(repo: mra.Repo) -> List[str]:\n    create_branch = mra.CreateBranch(\n        repo,\n        "branch_name",\n        "Commit/Pull request message",\n    )\n    with create_branch:\n        # Do something\n\n    if create_branch.pull_request_created:\n        if create_branch.message:\n            return [create_branch.message]\n        else:\n            return [f"https://github.com/{repo[\'name\']}/pulls"]\n  return []\n```\n',
    'author': 'Stéphane Brunner',
    'author_email': 'stephane.brunner@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sbrunner/multi-repo-automation',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
