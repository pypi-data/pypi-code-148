import string
from fabric.connection import Connection
from tif.fabric import cli
from tif.files import operations as files
from tif.fabric.logger import Logger
from tif.fabric.CommandPrefix import CommandPrefix

def list_commands(c : Connection, magento_root: string, command_prefix=""):
    with c.cd(magento_root):
        command = "bin/magento list"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def run(c : Connection, magento_root: string, command_prefix=""):
    with c.cd(magento_root):
        list_commands(c, magento_root, command_prefix)
        command = cli.prompt(">>> Enter bin/magento command to run: ")
        command = "bin/magento {}".format(command)
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def run_command(c : Connection, magento_root: string, command: string, command_prefix=""):
    with c.cd(magento_root):
        command = "bin/magento {}".format(command)
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def install(c : Connection, install_dir : string, command_prefix=""):
    with c.cd(install_dir):
        command = "bin/magento setup:install"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def mode_show(c : Connection, install_dir : string, command_prefix=""):
    with c.cd(install_dir):
        command = "bin/magento deploy:mode:show"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def delete_generated(c : Connection, magento_root : string, command_prefix=""):
    with c.cd(magento_root):
        confirm = cli.cli_confirm("You are about to empty the generated directory, Are you sure?")
        if (confirm == "y"):
            command = "rm -rf generated/*"
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())
            cli.puts(".:~ Done")
        else:
            cli.puts("!!! Aborted")

def delete_static(c : Connection, magento_root : string, command_prefix=""):
    with c.cd(magento_root):
        confirm = cli.cli_confirm("You are about to empty the static directory, Are you sure?")
        if (confirm == "y"):
            command = "rm -rf pub/static/*"
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())
            cli.puts(".:~ Done")
        else:
            cli.puts("!!! Aborted")

def delete_logs(c : Connection, magento_root : string, command_prefix=""):
    with c.cd(magento_root):
        confirm = cli.cli_confirm("You are about to empty the var/log directory, Are you sure?")
        if (confirm == "y"):
            command = "rm -rf var/log/*"
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())
            cli.puts(".:~ Done")
        else:
            cli.puts("!!! Aborted")

def delete_cache(c : Connection, magento_root : string, command_prefix=""):
    with c.cd(magento_root):
        confirm = cli.cli_confirm("You are about to empty the var/cache directory, Are you sure?")
        if (confirm == "y"):
            command = "rm -rf var/cache/*"
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())
            cli.puts(".:~ Done")
        else:
            cli.puts("!!! Aborted")

def di_compile(c : Connection, magento_root : string, command_prefix=""):
    with c.cd(magento_root):
        command = "bin/magento setup:di:compile"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def module_enable(c : Connection, magento_root : string, command_prefix=""):
    with c.cd(magento_root):
        module = cli.prompt(">>> Enter module to enable: ")
        if (module):
            command = "bin/magento module:enable {}".format(module)
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())
        else:
            cli.puts("!!! Aborted")

def setup_upgrade(c : Connection, magento_root : string, command_prefix=""):
    with c.cd(magento_root):
        command = "bin/magento setup:upgrade"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def setup_static_content_deploy(c : Connection, magento_root : string, options : None, command_prefix = ""):
    with c.cd(magento_root):
        command = "bin/magento setup:static-content:deploy"
        if options:
            command = "bin/magento setup:static-content:deploy {}".format(options)
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def cache_clean(c : Connection, magento_root : string, command_prefix=""):
    with c.cd(magento_root):
        command = "bin/magento cache:clean"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def cache_flush(c : Connection, magento_root : string, command_prefix=""):
    with c.cd(magento_root):
        command = "bin/magento cache:flush"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def template_hints(c : Connection, magento_root : string, command_prefix=""):
    with c.cd(magento_root):
        status = cli.prompt(">>> Enter disable or enable for template hints: ")
        if (status == "enable" or status == "disable"):
            command = "bin/magento dev:template-hints:{}".format(status)
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())
        else:
            cli.puts("!!! Aborted")

def generate_whitelist(c : Connection, magento_root : string, command_prefix=""):
    with c.cd(magento_root):
        module_name = cli.prompt(">>> Enter module name to generate whitelist json: ")
        command = "bin/magento setup:db-declaration:generate-whitelist --module-name={}".format(module_name)
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command())

def run_cron_group(c : Connection, magento_root : string, command_prefix=""):
        with c.cd(magento_root):
            group = cli.prompt(">>> Specify cron group to run: ")
            command = "bin/magento cron:run --group {}".format(group)
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())

def cron_install(c : Connection, magento_root : string, command_prefix=""):
        with c.cd(magento_root):
            command = "bin/magento cron:install"
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())

def run_cron(c : Connection, magento_root : string, command_prefix=""):
        with c.cd(magento_root):
            command = "bin/magento cron:run"
            Logger().log("Running command {}".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command())

def cat_log(c : Connection, magento_root : string, command_prefix=""):
        with c.cd(magento_root + "/var/log"):
            command = "ls"
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)
            log = cli.prompt(">>> Specify log to cat: ")
            command = "cat {}".format(log)
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def tail_log(c : Connection, magento_root : string, command_prefix=""):
        with c.cd(magento_root + "/var/log"):
            command = "ls"
            Logger().log("Running command '{}'".format(command))
            c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)
            log = cli.prompt(">>> Specify log to tail: ")
            files.tail_f(c, magento_root + "/var/log", log, command_prefix)

def admin_user_create(c: Connection, magento_root : string, command_prefix=""):
    with c.cd(magento_root):
        command = "bin/magento admin:user:create"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def enable_maintenance_mode(c : Connection, magento_root : string, command_prefix=""):
    with c.cd(magento_root):
        command = "bin/magento maintenance:enable"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)

def indexer_reindex(c : Connection, magento_root : string, command_prefix="", indexers = None):
    with c.cd(magento_root):
        if indexers:
            command = "bin/magento indexer:reindex {}".format(indexers)
        else:
            command = "bin/magento indexer:reindex"
        Logger().log("Running command '{}'".format(command))
        c.run(CommandPrefix(command, command_prefix).prefix_command(), pty=True)
