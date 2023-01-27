import string
import re
import os
from tif.fabric import cli
from fabric.connection import Connection
from tif.docker.service import Service

class Options:
    def __init__(self, **options) -> None:
        self.options = options

    def render(self, input_text= None, confirm_prompt = True) -> string:
        self._print()
        if (input_text):
            option = input(input_text)
        else:
            option = input("Choose an option: ")
        return self._get_option(option.strip(), confirm_prompt=confirm_prompt)

    def docker_container_chooser(self, service : Service, confirm_prompt = True) -> string:
        containers = service.containers_dictionary()
        containers[str(len(containers) + 1)] = "Exit"
        self.options = containers
        return self.render(input_text="Choose a container: ", confirm_prompt=confirm_prompt)


    def remote_directory_chooser(self, c : Connection, dir = None, absolute_path = True, input_text = None, list_all = False):
        options = []
        dir = dir or c.cwd
        dir_list = c.sftp().listdir(dir)
        if not list_all:
            filtered_dir_list = [file for file in dir_list if (not file.startswith(".") and not re.search(r"\.([\w\d]){1,}$", file))]
        else:
            filtered_dir_list = dir_list
        filtered_dir_list.sort()
        for file in filtered_dir_list:
            print (cli.puts_hide(">>> {}".format(filtered_dir_list.index(file) + 1)), '--', file)
        if (input_text):
            option = input(input_text)
        else:
            option = input("Choose an option: ")
        if not option.isnumeric():
            cli.puts("!!! Invalid option selected")
            exit()
        chosen = cli.cli_confirm("You have selected the directory '{}'. Keep this choice?".format(filtered_dir_list[int(option) - 1]))
        if chosen == 'y':
            if not absolute_path:
                return os.sep.join(options) + filtered_dir_list[int(option) - 1]
            else:
                return dir + os.sep + os.sep.join(options) + filtered_dir_list[int(option) - 1]
        else:
            while(option is not None):
                options.append(filtered_dir_list[int(option) - 1])
                c.sftp().chdir(dir + os.sep + os.sep.join(options))
                dir_list = c.sftp().listdir(dir + os.sep + os.sep.join(options))
                if not list_all:
                    filtered_dir_list = [file for file in dir_list if (not file.startswith(".") and not re.search(r"\.([\w\d]){1,}$", file))]
                else:
                    filtered_dir_list = dir_list
                if len(filtered_dir_list) == 0:
                    cli.puts("!! There are no more directories to list")
                    exit() 
                filtered_dir_list.sort()
                for file in filtered_dir_list:
                    print (cli.puts_hide(">>> {}".format(filtered_dir_list.index(file) + 1)), '--', file)
                if (input_text):
                    option = input(input_text)
                else:
                    option = input("Choose an option: ")
                if not option.isnumeric():
                    cli.puts("!!! Invalid option selected")
                    exit()
                chosen = cli.cli_confirm("You have selected the directory '{}'. Keep this choice?".format(filtered_dir_list[int(option) - 1]))
                if chosen == 'y':
                    if not absolute_path:
                        return os.sep.join(options) + os.sep + filtered_dir_list[int(option) - 1]
                    else:
                        return dir + os.sep + os.sep.join(options) + os.sep + filtered_dir_list[int(option) - 1]

    def remote_file_chooser(self, c : Connection, dir = None, absolute_path = False, input_text = None, list_all = False):
        options = []
        dir = dir or c.cwd
        dir_list = c.sftp().listdir(dir)
        if not list_all:
            filtered_dir_list = [file for file in dir_list if (not file.startswith(".") and not re.search(r"\.([\w\d]){1,}$", file))]
        else:
            filtered_dir_list = dir_list
        filtered_dir_list.sort()
        for file in filtered_dir_list:
            print (cli.puts_hide(">>> {}".format(filtered_dir_list.index(file) + 1)), '--', file)
        if (input_text):
            option = input(input_text)
        else:
            option = input("Choose an option: ")
        if not option.isnumeric():
            cli.puts("!!! Invalid option selected")
            exit()
        while(option is not None):
            if (re.search(r"\.([\w\d]){1,}$", filtered_dir_list[int(option) - 1])):
                if not absolute_path:
                    return os.sep.join(options) + os.sep + filtered_dir_list[int(option) - 1]
                else:
                    return dir + os.sep + os.sep.join(options) + os.sep + filtered_dir_list[int(option) - 1]
            options.append(filtered_dir_list[int(option) - 1])
            c.sftp().chdir(dir + os.sep + os.sep.join(options))
            dir_list = c.sftp().listdir(dir + os.sep + os.sep.join(options))
            if not list_all:
                filtered_dir_list = [file for file in dir_list if (not file.startswith("."))]
            else:
                filtered_dir_list = dir_list
            filtered_dir_list.sort()
            for file in filtered_dir_list:
                print (cli.puts_hide(">>> {}".format(filtered_dir_list.index(file) + 1)), '--', file)
            if (input_text):
                option = input(input_text)
            else:
                option = input("Choose an option: ")
            if not option.isnumeric():
                cli.puts("!!! Invalid option selected")
                exit()

    def local_directory_chooser(self, dir = None, absolute_path = True, input_text = None, list_all = False):
        options = []
        if not dir: 
            return os.curdir
        dir = dir or os.curdir
        dir_list = os.listdir(dir)
        if not list_all:
            filtered_dir_list = [file for file in dir_list if (not file.startswith(".") and not re.search(r"\.([\w\d]){1,}$", file))]
        else:
            filtered_dir_list = dir_list
        filtered_dir_list.sort()
        for file in filtered_dir_list:
            print (cli.puts_hide(">>> {}".format(filtered_dir_list.index(file) + 1)), '--', file)
        if (input_text):
            option = input(input_text)
        else:
            option = input("Choose an option: ")
        if not option.isnumeric():
            cli.puts("!!! Invalid option selected")
            exit()
        chosen = cli.cli_confirm("You have selected the directory '{}'. Keep this choice?".format(filtered_dir_list[int(option) - 1]))
        if chosen == 'y':
            if not absolute_path:
                return os.sep.join(options) + filtered_dir_list[int(option) - 1]
            else:
                return dir + os.sep + os.sep.join(options) + filtered_dir_list[int(option) - 1]
        else:
            while(option is not None):
                options.append(filtered_dir_list[int(option) - 1])
                os.chdir(dir + os.sep + os.sep.join(options))
                dir_list = os.listdir(dir + os.sep + os.sep.join(options))
                if not list_all:
                    filtered_dir_list = [file for file in dir_list if (not file.startswith(".") and not re.search(r"\.([\w\d]){1,}$", file))]
                else:
                    filtered_dir_list = dir_list
                if len(filtered_dir_list) == 0:
                    cli.puts("!! There are no more directories to list")
                    exit() 
                filtered_dir_list.sort()
                for file in filtered_dir_list:
                    print (cli.puts_hide(">>> {}".format(filtered_dir_list.index(file) + 1)), '--', file)
                if (input_text):
                    option = input(input_text)
                else:
                    option = input("Choose an option: ")
                if not option.isnumeric():
                    cli.puts("!!! Invalid option selected")
                    exit()
                chosen = cli.cli_confirm("You have selected the directory '{}'. Keep this choice?".format(filtered_dir_list[int(option) - 1]))
                if chosen == 'y':
                    if not absolute_path:
                        return os.sep.join(options) + os.sep + filtered_dir_list[int(option) - 1]
                    else:
                        return dir + os.sep + os.sep.join(options) + os.sep + filtered_dir_list[int(option) - 1]

    def local_file_chooser(self, dir = None, absolute_path = False, input_text = None, list_all = False):
        options = []
        dir = dir or os.curdir
        dir_list = os.listdir(dir)
        if not list_all:
            filtered_dir_list = [file for file in dir_list if (not file.startswith(".") and not re.search(r"\.([\w\d]){1,}$", file))]
        else:
            filtered_dir_list = dir_list
        filtered_dir_list.sort()
        for file in filtered_dir_list:
            print (cli.puts_hide(">>> {}".format(filtered_dir_list.index(file) + 1)), '--', file)
        if (input_text):
            option = input(input_text)
        else:
            option = input("Choose an option: ")
        if not option.isnumeric():
            cli.puts("!!! Invalid option selected")
            exit()
        while(option is not None):
            if (re.search(r"\.([\w\d]){1,}$", filtered_dir_list[int(option) - 1])):
                if not absolute_path:
                    return os.sep.join(options) + os.sep + filtered_dir_list[int(option) - 1]
                else:
                    return dir + os.sep + os.sep.join(options) + os.sep + filtered_dir_list[int(option) - 1]
            options.append(filtered_dir_list[int(option) - 1])
            os.chdir(dir + os.sep + os.sep.join(options))
            dir_list = os.listdir(dir + os.sep + os.sep.join(options))
            if not list_all:
                filtered_dir_list = [file for file in dir_list if (not file.startswith("."))]
            else:
                filtered_dir_list = dir_list
            filtered_dir_list.sort()
            for file in filtered_dir_list:
                print (cli.puts_hide(">>> {}".format(filtered_dir_list.index(file) + 1)), '--', file)
            if (input_text):
                option = input(input_text)
            else:
                option = input("Choose an option: ")
            if not option.isnumeric():
                cli.puts("!!! Invalid option selected")
                exit()

    def _print(self) -> string:
        for key in self.options.keys():
            print (cli.puts_hide(">>> {}".format(key)), '--', self.options[key])

    def _get_option(self, option, confirm_prompt = True):
        if (option.strip() not in self.options.keys()):
                cli.puts("!!! Not a valid choice")
                exit()
        elif (self.options[option].lower() == 'exit'):
            cli.puts("!!! Exited")
            exit()
        elif (self.options[option].lower() == 'skip'):
            cli.puts("!!! Skipped")
            pass
        else:
            if confirm_prompt:
                choise = cli.cli_confirm("You have chosen '{}'. Continue?".format(self.options[option]))
                if (choise == 'y'):
                    return self.options[option]
                else:
                    cli.puts("!!! Aborted")
                    exit()
            return self.options[option]