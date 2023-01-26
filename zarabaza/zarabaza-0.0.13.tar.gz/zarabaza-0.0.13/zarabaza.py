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
# branch iniziale
initial_branch = repo.active_branch
# lista di tutti i branch presenti nella repository
branch_list = repo.remotes.origin.fetch()
# lista dei commit più recenti
commit_list = list(repo.iter_commits(initial_branch, max_count=7))
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

# chiediamo quali commit e su quali branch fare cherry-pick
answers = prompt(questions)
print_json(answers)

# se non è stato selezionato nessun commit o nessun branch esco
if(answers['selected_commit'] == None or len(answers['selected_branches']) == 0):
    print("No commit or branch selected. Exiting.")
    exit(1)

# faccio lo stash del branch iniziale per evitare di sovrascrivere modifiche pendenti
repo.git.stash()
for branch in answers['selected_branches']:
    branch = branch.replace("origin/", "")
    print("Cherry-pick " + answers['selected_commit'].split("hash=>")[1] + " commit onto " + branch + " branch")
    # mi sposto sul branch in cui cherry-pickare
    repo.git.checkout(branch)
    # faccio il pull del branch per avere le modifiche più recenti
    repo.git.pull("origin", branch)
    # faccio il cherry-pick
    try:
        repo.git.cherry_pick(answers['selected_commit'].split("hash=>")[1], strategy_option="theirs")
    except Exception as e:
        print("Cherry-pick failed. Skipping branch " + branch + "\n")
        print(e)
        all_done = False
        continue
    # faccio il push del branch con il cherry pick fatto
    try:
        repo.git.push("origin", branch)
    except Exception as e:
        print("Push failed. Skipping branch " + branch + "\n")
        print(e)
        all_done = False
        continue
    # se il branch è un dev chiedo se fare il merge in master
    if branch.find("/dev") != -1:
        # chiediamo se fare anche il merge in master
        questiones = [
            {
                'type': 'confirm',
                'name': 'merge_master',
                'message': 'Do you want to merge this branch into '+ branch.replace("/dev", "/master") + "?",
                'default': False,
            }
        ]
        answers_to_merge = prompt(questiones)
        if(answers_to_merge['merge_master']):
            master_branch = branch.replace("/dev", "/master")
            print("Merging " + branch + " into " + master_branch)
            # mi sposto sul branch xxx/master
            try:
                repo.git.checkout(master_branch)
            except Exception as e:
                print("No branch found with name: " + master_branch + "\n")
                all_done = False
                continue
            # faccio il pull del branch per avere le modifiche più recenti
            repo.git.pull("origin",master_branch)
            # faccio il merge
            try:
                repo.git.merge(branch, strategy_option="theirs")
            except Exception as e:
                print("Merge failed. Skipping branch " + master_branch + "\n")
                print(e)
                all_done = False
                continue
            # faccio il push del branch con il merge fatto
            try:
                repo.git.push("origin", master_branch)
            except Exception as e:
                print("Push failed. Skipping branch " + master_branch + "\n")
                print(e)
                all_done = False
                continue
# torno sul branch iniziale
repo.git.checkout(initial_branch)
# faccio il pop dello stash per ripristinare le modifiche pendenti
try:
    repo.git.stash("pop")
except Exception as e:
    print("No stash to pop. Skipping stash pop.\n")
print("Back on branch " + str(initial_branch) + "\n")
if(all_done): print("Operations successfully completed.")