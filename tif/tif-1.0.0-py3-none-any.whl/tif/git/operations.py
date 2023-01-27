import string
from fabric.connection import Connection
from tif.fabric import cli
from tif.fabric.logger import Logger
from tif.fabric.CommandPrefix import CommandPrefix
from tif.cli.options import Options

def version(c : Connection, repo_dir : string, command_prefix = ""):
    with c.cd(repo_dir):
        command = "git --version"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def get_remote_url(c: Connection, repo_dir: string, command_prefix=""):
    with c.cd(repo_dir):
        command = "git config --get remote.origin.url"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def clone_repo(c : Connection, clone_dir: string, repo: string, command_prefix = ""):
    with c.cd(clone_dir):
        command = "git clone {} .".format(repo)
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def switch_branch(c: Connection, repo_dir: string, command_prefix = ""):
    with c.cd(repo_dir):
        branch(c, repo_dir, command_prefix)
        sbranch = cli.prompt(">>> Enter branch to switch to: ")
        if (sbranch):
            command = "git checkout {}".format(sbranch)
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())
        else:
            cli.puts("!!! Aborted")

def switch_to_branch(c: Connection, repo_dir: string, branch : string, command_prefix = ""):
    with c.cd(repo_dir):
        command = "git checkout {}".format(branch)
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def new_branch(c: Connection, repo_dir: string, command_prefix = ""):
    with c.cd(repo_dir):
        new_branch = cli.prompt(">>> Enter new branch name: ")
        if (new_branch):
            command = "git checkout -b {}".format(new_branch)
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())
        else:
            cli.puts("!!! Aborted")

def delete_local_branch(c: Connection, repo_dir: string, command_prefix = ""):
    with c.cd(repo_dir):
        delete_branch = cli.prompt(">>> Enter branch to delete: ").strip()
        if (delete_branch):
            command = "git branch --delete {}".format(delete_branch)
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())
        else:
            cli.puts("!!! Aborted")
 
def branch(c : Connection, repo_dir : string, command_prefix = ""):
    with c.cd(repo_dir):
        command = "git branch"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def branch_all(c : Connection, repo_dir : string, command_prefix = ""):
    with c.cd(repo_dir):
        command = "git branch --all"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def current_branch(c : Connection, repo_dir : string, command_prefix = "") -> string :
    with c.cd(repo_dir):
        command = "git rev-parse --abbrev-ref HEAD"
        Logger().log("Running command '{}'".format(command))
        branch = c.run(CommandPrefix(command, command_prefix).prefix_command(), hide=True)
        return branch.stdout.strip()

def pull(c : Connection, repo_dir : string,command_prefix = "", oauth2_url = None):
    with c.cd(repo_dir):
        branch = current_branch(c, repo_dir, command_prefix)
        confirm = cli.cli_confirm("You are about to pull the remote branch {}. Are you sure?".format(branch))
        if (confirm == "y"):
            if oauth2_url:
                command = "git pull {} {}".format(oauth2_url, branch)
            else:
                command = "git pull origin {}".format(branch)
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)
        else:
            cli.puts("!!! Aborted")

def pull_branch(c : Connection, repo_dir : string, command_prefix = ""):
    with c.cd(repo_dir):
        branch = current_branch(c, repo_dir, command_prefix)
        origin_branch = cli.prompt(">>> Enter branch to pull from origin: ")
        confirm = cli.cli_confirm("You are about to pull the remote branch {} into {}. Are you sure?".format(origin_branch, branch))
        if (confirm == "y"):
            command = "git pull origin {}".format(origin_branch)
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)
        else:
            cli.puts("!!! Aborted")

def origin_merge(c : Connection, repo_dir : string, command_prefix = ""):
    with c.cd(repo_dir):
        cli.puts("** Fetching origin...")
        fetch(c, repo_dir, command_prefix)
        branch(c, repo_dir, command_prefix)
        local_branch = current_branch(c, repo_dir, command_prefix)
        origin_branch = cli.prompt(">>> Enter origin branch to merge: ")
        if (local_branch and origin_branch):
            confirm = cli.cli_confirm("You are about to merge the origin branch {} into local branch {}. Are you sure?".format(origin_branch, local_branch))
            if (confirm == "y"):
                command = "git merge origin/{}".format(origin_branch.strip())
                Logger().log("Running command '{}'".format(command))
                c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)
            else:
                cli.puts("!!! Aborted")
        else:
            cli.puts("!!! Aborted")

def push(c : Connection, repo_dir : string, command_prefix = ""):
    with c.cd(repo_dir):
        branch = current_branch(c, repo_dir, command_prefix)
        confirm = cli.cli_confirm("You are about to push to origin branch {}. Are you sure?".format(branch))
        if (confirm == "y"):
            command = "git push origin {}".format(branch)
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)
        else:
            cli.puts("!!! Aborted")

def force_push(c : Connection, repo_dir : string, command_prefix = ""):
    with c.cd(repo_dir):
        branch = current_branch(c, repo_dir, command_prefix)
        confirm = cli.cli_confirm("You are about to force push to origin branch {}. Are you sure?".format(branch))
        if (confirm == "y"):
            command = "git push -f origin {}".format(branch)
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)
        else:
            cli.puts("!!! Aborted")

def fetch(c : Connection, repo_dir : string, command_prefix = "", oauth2_url = None, branch = None):
    with c.cd(repo_dir):
        command = "git fetch"
        if oauth2_url:
            command = command + " " + oauth2_url
        if branch:
            command = command + " " + branch
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def status(c : Connection, repo_dir : string, command_prefix = ""):
    with c.cd(repo_dir):
        command = "git status"
        Logger().log(message="Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def diff(c : Connection, repo_dir : string, command_prefix = ""):
    with c.cd(repo_dir):
        file = cli.prompt(">>> Enter file to diff: ")
        command = "git diff {}".format(file)
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def file_checkout(c : Connection, repo_dir : string, command_prefix = "", remote = True):
    with c.cd(repo_dir):
        status(c, repo_dir, command_prefix)
        if remote:
            file = Options().remote_file_chooser(c, repo_dir, input_text="Navigate to file to checkout (CTRL+c to abort): ")
        else:
            file = Options().local_file_chooser(repo_dir, input_text="Navigate to file to checkout (CTRL+c to abort): ")
        if(file):
            command = "git checkout -- {}".format(file)
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())
        else:
            cli.puts("!!! Aborted")

def add_iteractive(c : Connection, repo_dir : string, command_prefix = ""):
    with c.cd(repo_dir):
        command = "git add -i"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def commit(c : Connection, repo_dir : string, command_prefix = ""):
    with c.cd(repo_dir):
        command = "git commit"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def stash(c : Connection, repo_dir : string, command_prefix = ""):
    with c.cd(repo_dir):
        command = "git stash"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def stash_list(c : Connection, repo_dir : string, command_prefix = ""):
    with c.cd(repo_dir):
        command = "git stash list"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def stash_drop(c : Connection, repo_dir : string, command_prefix = ""):
    with c.cd(repo_dir):
        command = "git stash drop"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def stash_pop(c : Connection, repo_dir : string, command_prefix = ""):
    with c.cd(repo_dir):
        command = "git stash pop"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def reset_head(c : Connection, repo_dir : string, command_prefix = ""):
    with c.cd(repo_dir):
        command = "git reset --hard HEAD"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def remove(c : Connection, repo_dir : string, command_prefix = ""):
     with c.cd(repo_dir):
        file = cli.prompt(">>> Enter file to remove. Type 'exit' to finish the operation: ")
        while file not in ["exit"]:
            command = "git rm {}".format(file)
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())
            status(c, repo_dir, command_prefix)
            file = cli.prompt(">>> Enter file to remove. Type 'exit' to finish the operation: ")
        status(c, repo_dir, command_prefix)

def rename(c : Connection, repo_dir : string, command_prefix = ""):
     with c.cd(repo_dir):
        old_file = cli.prompt(">>> Enter file to rename: ")
        new_file = cli.prompt(">>> Enter new filename: ")
        command = "git mv {} {}".format(old_file, new_file)
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())
        status(c, repo_dir, command_prefix)

def log(c : Connection, repo_dir : string, logs = "-5", command_prefix = ""):
    with c.cd(repo_dir):
        command = "git log -p {}".format(logs)
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def reset_commit(c : Connection, repo_dir : string, logs = "-5", command_prefix = ""):
    with c.cd(repo_dir):
        command = "git reflog"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())
        hash = cli.prompt(">>> Enter commit hash to be reset: ")
        if (hash):
            confirm = cli.cli_confirm("You are about to execute git reset --hard {}. Are you sure?".format(hash))
            if (confirm == 'y'):
                command = "git reset --hard {}".format(hash)
                Logger().log("Running command '{}'".format(command))
                c.run(CommandPrefix(command, command_prefix).prefix_command())
            else:
                cli.puts("!!! Aborted")
        else:
            cli.puts("!!! Aborted")
