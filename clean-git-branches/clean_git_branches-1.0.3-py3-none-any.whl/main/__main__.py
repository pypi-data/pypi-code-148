import os
import sys
import uuid
import git

protected_branches = ["master", "main", "dev"]

def delete_local_branches(cwd: str, caution: bool = True):
    stash_name = f"stash_{uuid.uuid4().hex[:6].upper()}"
    stash_flag = False

    # Initialize repo and remote
    repo = git.Repo()
    remote = repo.remotes.origin

    git_fetch_repos = remote.fetch()
    git.cmd.Git().execute(["git", "fetch", "--prune"])

    # Get list of remote branches
    remote_branches = [branch.remote_ref_path.strip() for branch in git_fetch_repos]
    print(f"Remote branches: {remote_branches}")

    # Get list of stale branches
    known_local_branches = [branch.name for branch in remote.repo.branches if branch.name]
    stale_branches = [branch for branch in known_local_branches if branch not in remote_branches]
    if stale_branches:
        print(f"Stale branches: {str(stale_branches)}")
    else:
        print(f"No stale branches to delete found. These are the known local branches: {known_local_branches}")
        return

    # Show the stale branches to be deleted and confirm if the confirm parameter is passed
    if caution:
        if not get_delete_confirm_from_user(stale_branches):
            print("Deletion not confirmed. Aborting.")
            return
        else:
            print("Deletion confirmed.")

    # Stash changes if there are any
    if repo.is_dirty():
        repo.git.stash("save", stash_name)
        stash_flag = True


    # Using a lambda function, get one of the remote branches.
    # First check the protected branches if they exist on the remotes.
    # If not, checkout the first branch in the remote_branches list
    branch_to_switch_to = next((branch for branch in protected_branches if branch in remote_branches), remote_branches[0])
    repo.git.checkout(branch_to_switch_to)

    # Delete local branches that have been deleted on remote
    for branch in stale_branches:
        try:
            repo.delete_head(branch, force=True)
            print(f"Deleted local branch {branch}")
        except Exception as error:
            print(f"Could not delete local branch '{branch}' because {error}")

    if stash_flag:
        pop_stash_by_name(stash_name)
    else:
        print("No stash was performed, so no stash was popped.")


def get_delete_confirm_from_user(stale_branches, tries=0):
    confirm_message = f"The following branches will be deleted: {', '.join(stale_branches)}. Are you sure you want to continue? (y/n): "
    confirm_input = input(confirm_message).lower().strip()
    if confirm_input in ["y", "yes"]:
        return True
    # clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    if confirm_input in ["n", "no"] or tries >= 2:
        return False
    else:
        tries += 1
        print("Invalid input. Please enter 'y' or 'n' or 'yes' or 'no'")
        print("") # empty line
        return get_delete_confirm_from_user(stale_branches, tries=tries)


def pop_stash_by_name(stash_name:str):
    repo = git.Repo()
    stash_list = repo.git.stash("list")
    # map the stash list to a list of lists with the stash name and the stash hash
    # the first element in the list is the stash hash and the second element is the stash name
    stashes_map = map(lambda stash: [stash.split(":")[-1].strip(), stash.split(":")[0].strip()], stash_list.splitlines())
    for stash in stashes_map:
        if stash_name == stash[0]:
            try:
                repo.git.stash("pop", stash[1])
                print(f"Stash '{stash_name}' was popped successfully.")
            except Exception as error:
                print(f"Could not pop stash '{stash_name}' because {error}")
            return
        print(f"No stash with the name '{stash_name}' was found.")
    return

def start():
    cwd = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    caution = sys.argv[2] if len(sys.argv) > 2 else True

    current_working_directory = os.getcwd()
    os.chdir(cwd)
    try:
        delete_local_branches(current_working_directory, caution=caution)
    except git.exc.InvalidGitRepositoryError as error:
        print(f"Could not delete local branches because repo was not available, or it was not yet initialized.")
        print(f"You can pass the path to the repo or any sub folder of a repo as the first argument to the script.")
    os.chdir(current_working_directory)

if __name__ == "__main__":
    # get first and second arguments
    # first argument is the path to the repo
    # second argument is the caution flag
    cwd = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    caution = sys.argv[2] if len(sys.argv) > 2 else True
    start(cwd, caution)
