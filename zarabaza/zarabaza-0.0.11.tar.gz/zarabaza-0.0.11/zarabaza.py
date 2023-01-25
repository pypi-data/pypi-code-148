from __future__ import print_function, unicode_literals
from whaaaaat import prompt, print_json
import os
from git import Repo

all_done = True
current_directory = os.getcwd()
root_directory =  os.path.expanduser('~/.deployer_config')
try:
    config_file_content = open(root_directory, 'r').read()
except:
    print("No configuration file in " + root_directory)
    exit(1)
try:
    repo = Repo(current_directory)
except:
    print("No git repository found in " + current_directory)
    exit(1)
initial_branch = repo.active_branch
branch_list = repo.remotes.origin.fetch()
commit_list = list(repo.iter_commits(initial_branch, max_count=5))
repo.config_writer().set_value("user", "name", "zarabaza").release()
repo.config_writer().set_value("user", "email", "zarabaza@test.it").release()

print("Current branch: " + str(initial_branch) + "\n")

questions = [
    {
        'type': 'list',
        'name': 'selected_commit',
        'message': 'Select a commit to cherry-pick',
        'choices': [str(c.message.replace("\n", "") + " [hash=>" +c.hexsha) for c in commit_list]
    },
    {
        "type": "checkbox",
        "message": "Select branches to cherry-pick onto",
        "name": "selected_branches",
        "choices": [{'name': str(b)} for b in filter(lambda x: x!=initial_branch, branch_list)],
        'validate': lambda answer: 'You must have to select at least one branch.' \
            if len(answer) == 0 else True
    }
]


answers = prompt(questions)
print_json(answers)

if(answers['selected_commit'] == None or len(answers['selected_branches']) == 0):
    print("No commit or branch selected. Exiting.")
    exit(1)

repo.git.stash()
for branch in answers['selected_branches']:
    branch = branch.replace("origin/", "")
    print("Cherry-pick " + answers['selected_commit'].split("hash=>")[1] + " commit onto " + branch + " branch")
    repo.git.checkout(branch)
    repo.git.pull("origin", branch)
    try:
        repo.git.cherry_pick(answers['selected_commit'].split("hash=>")[1], strategy_option="theirs")
    except Exception as e:
        print("Cherry-pick failed. Skipping branch " + branch + "\n")
        print(e)
        all_done = False
        continue
    try:
        repo.git.push("origin", branch)
    except Exception as e:
        print("Push failed. Skipping branch " + branch + "\n")
        print(e)
        all_done = False
        continue

repo.git.checkout(initial_branch)
repo.git.stash("pop")
print("Back on branch " + str(initial_branch) + "\n")
if(all_done): print("Operations successfully completed.")