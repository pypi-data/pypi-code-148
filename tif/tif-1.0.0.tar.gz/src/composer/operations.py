import string
from fabric.connection import Connection
from tif.fabric.CommandPrefix import CommandPrefix
from tif.fabric.logger import Logger

def version(c : Connection, install_dir : string, command_prefix = ""):
    with c.cd(install_dir):
        command = "composer -V"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def install(c : Connection, install_dir : string, command_prefix = ""):
    with c.cd(install_dir):
        command = "composer install"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def install_with_flags(c : Connection, install_dir : string, flags = "", command_prefix = ""):
    with c.cd(install_dir):
        command = "composer install {}".format(flags)
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def update(c : Connection, install_dir : string, command_prefix = ""):
    with c.cd(install_dir):
        command = "composer update"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)
