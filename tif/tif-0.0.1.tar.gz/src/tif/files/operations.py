import string
import os
from fabric.connection import Connection
from fabric.transfer import Transfer
from tif.fabric import cli
from tif.fabric.logger import Logger
from tif.fabric.CommandPrefix import CommandPrefix
from tif.cli.options import Options
from python_hosts import Hosts, HostsEntry

def gunzip(c : Connection , dir : string, listFiles = True, command_prefix = ""):
    with c.cd(dir):
        if (listFiles):
            command = "ls"
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())
        zip = cli.prompt(">>> Enter file to gunzip: ")
        if (zip):
            command = "gunzip {}".format(zip)
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())
        else:
            cli.puts("!!! Aborted")

def ls(c : Connection, dir : string, command_prefix = ""):
    with c.cd(dir):
        command = "ls"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def mv(c : Connection, dir : string, filename : string, mv_filename : string, command_prefix = ""):
     with c.cd(dir):
        command = "mv {} {}".format(filename, mv_filename)
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def rsync(c : Connection, dir : string, command : string, command_prefix = ""):
    with c.cd(dir):
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def mount(c : Connection, command : string, command_prefix = ""):
    Logger().log("Running command '{}'".format(command))
    c.run(CommandPrefix(command, command_prefix).prefix_command())

def dfh(c : Connection, dir : string, command_prefix = ""):
    with c.cd(dir):
        command = "df -h"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def grep(c : Connection, dir : string, command : string, search : string, command_prefix = "") -> int:
    with c.cd(dir):
        command = "{} | grep -q '{}'".format(command, search)
        Logger().log("Running command '{}'".format(command))
        result = c.run(CommandPrefix(command, command_prefix).prefix_command(), hide=True, warn=True)
        return result.return_code


def mkdir(c : Connection, dir : string, command_prefix = ""):
    with c.cd(dir):
        curr_dir = c.run("pwd")
        new_dir = cli.prompt(">>> Enter directory to create in {} directory: ".format(curr_dir.stdout.strip()))
        if (new_dir):
            command = "mkdir {}".format(new_dir)
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())
        else:
            cli.puts("!!! Aborted")

def ls_tmp(c : Connection, command_prefix = ""):
    with c.cd("/tmp"):
        command = "ls -la"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def rm(c : Connection, dir : string, command_prefix = ""):
    with c.cd(dir):
        command = "ls"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())
        to_delete = cli.prompt(">>> Enter directory/file to delete: ")
        if c.run(CommandPrefix('test -d {0}'.format(to_delete), command_prefix).prefix_command(), warn=True):
            confirm = cli.cli_confirm("You are about to delete the directory {0}. Are you sure?".format(to_delete))
            if (confirm == "y"):
                command = "rm -rf {0}".format(to_delete.strip())
                Logger().log("Running command '{}'".format(command))
                c.run(CommandPrefix(command, command_prefix).prefix_command())
            else:
                cli.puts("!!! Aborted")
        elif c.run(CommandPrefix('test -f {}'.format(to_delete), command_prefix).prefix_command(), warn=True):
            confirm = cli.cli_confirm("You are about to delete the file {0}. Are you sure?".format(to_delete))
            if (confirm == "y"):
                command = "rm -f {}".format(to_delete.strip())
                Logger().log("Running command '{}'".format(command))
                c.run(CommandPrefix(command, command_prefix).prefix_command())
            else:
                cli.puts("!!! Aborted")
        else:
            cli.puts("!!! Aborted operation. {} not found.".format(to_delete))

def vim(c : Connection, dir : string, command_prefix = ""):
    with c.cd(dir):
        file = cli.prompt(">>> Enter file to edit in vim: ")
        command = "vim {}".format(file.strip())
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def ls_dir(c : Connection, dir : string, command_prefix = "", prompt_for_dir = True):
    if (prompt_for_dir):
        ls_dir = cli.prompt(">>> Enter directory to list: ")
    else:
        ls_dir = ""
    with c.cd(dir + "/" + ls_dir.strip()):
        command = "ls -la"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def ls_la(c : Connection, dir : string, command_prefix = ""):
    with c.cd(dir):
        command = "ls -la"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def find_mount(c : Connection, dir : string, command_prefix = ""):
    with c.cd(dir):
        command = "findmnt -T ."
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def mount_column(c : Connection, dir : string, command_prefix = ""):
    with c.cd(dir):
        command = "mount | column -t"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def get(c : Connection, from_dir : string, to_dir : string):
    t = Transfer(c)
    remote_file = Options().remote_file_chooser(c, dir = from_dir, absolute_path=True,input_text="Navigate to file to transfter (CTRL+c to abort): ")
    local_dir = Options().local_directory_chooser(input_text="Navigate to local directory for the transfter (CTRL+c to abort): ", absolute_path=True)
    local_fileName = cli.prompt(">>> Enter local file name to be tansferred in {}: ".format(local_dir))
    t.get(remote_file, local_dir + os.sep + local_fileName)
    cli.puts(".:~ Done!")

def put(c : Connection, remote_working_dir = None):
    local_file = cli.prompt(">>> Enter local file path to upload (relative to fabfile location): ")
    remote_file = cli.prompt(">>> Enter remote file path to upload (relative to home directory or specified working dir): ")
    t = Transfer(c)
    if (remote_working_dir):
        remote_dir = remote_working_dir + '/' + remote_file
        cli.puts(">>> Uploading to {}".format(remote_dir))
        t.put(local=local_file, remote=remote_dir)
    else:
         t.put(local=local_file, remote=remote_file)

def cat(c : Connection, dir : string, command_prefix=""):
        with c.cd(dir):
            file = Options().remote_file_chooser(c, dir, input_text="Navigate to file to cat (CTRL+c to abort): ")
            command = "cat {}".format(file.strip())
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def cat_and_grep(c : Connection, dir : string, file : string, grep : string, command_prefix=""):
        with c.cd(dir):
            command = "cat {} | grep '{}'".format(file.strip(), grep.strip())
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def cat_file(c : Connection, dir : string, file : string, command_prefix=""):
        with c.cd(dir):
            command = "cat {}".format(file.strip())
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def cat_tmp_file(c : Connection, command_prefix=""):
        with c.cd("/tmp"):
            ls_tmp(c, command_prefix=command_prefix)
            file = cli.prompt(">>> Enter file to cat: ")
            command = "cat {}".format(file.strip())
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def set_files_permissions(c : Connection, dir : string, path : string, chmod : string, command_prefix = ""):
    with c.cd(dir):
        command = "sudo -s && find {} -type d -exec chmod {} {{}} \;".format(path, chmod)
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def chown(c : Connection, dir : string, owner : string, group : string, file : string, command_prefix = ""):
    with c.cd(dir):
        command = "chown {}:{} {}".format(owner, group, file)
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def tail_f(c : Connection, dir : string, file : string, command_prefix = ""):
    with c.cd(dir):
        command = "tail -f {}".format(file.strip())
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def etc_hosts_add_entry(c : Connection, address : string, names : tuple, entry_type='ipv4', hosts_file='/etc/hosts'):
    command = "sudo chmod 766 {}".format(hosts_file)
    Logger().log("Running command '{}'".format(command))
    c.run(command, pty=False)
    hosts = Hosts()
    new_entry = HostsEntry(entry_type, address= address, names = names)
    hosts.add([new_entry])
    Logger().log("Adding to {} entry '{} {}'".format(hosts_file, address, names))
    hosts.write()
    command = "sudo chmod 644 {}".format(hosts_file)
    Logger().log("Running command '{}'".format(command))
    c.run(command, pty=False)

def etc_hosts_remove_entry(c : Connection, address : string, hosts_file='/etc/hosts'):
    command = "sudo chmod 766 {}".format(hosts_file)
    Logger().log("Running command '{}'".format(command))
    c.run(command, pty=False)
    hosts = Hosts()
    hosts.remove_all_matching(address=address)
    Logger().log("Removing from {} entry for address '{}'".format(hosts_file, address))
    hosts.write()
    command = "sudo chmod 644 {}".format(hosts_file)
    Logger().log("Running command '{}'".format(command))
    c.run(command, pty=False)