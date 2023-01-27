import string
import docker
import re
from invoke import run
from tif.fabric import cli
from tif.fabric.logger import Logger

class Service:
    def __init__(self, docker_dir : string) -> None:
        self.docker_dir = docker_dir

    def container_name_search(self, search : string) -> string:
        client = docker.from_env()
        containers = client.containers.list()
        for container in containers:
            if re.search(search, container.name):
                return container.name
        raise Exception("No {} container match".format(search))

    def containers_dictionary(self) -> dict:
        """
        Returns dictionary with numbers as key and container's name as value
        """
        containers_dict = {}
        client = docker.from_env()
        containers = client.containers.list()
        index = 1
        for container in containers:
            containers_dict[str(index)] = container.name
            index = index + 1
        return containers_dict

    def exec(self, options, command = None, confirm_prompt = True, exec_options = "-it"):
        """
        Exec a command in chosen container. Expect Options object from tif.cli.options module
        """
        container_choice = options.docker_container_chooser(self, confirm_prompt=confirm_prompt)
        if not command:
            command = cli.prompt(">>> Enter command to execute: ")
        command = self.command(container_choice, command.strip(), exec_options)
        run(command, pty=True)

    def command(self, container : string, command : string, exec_options = "-it") -> string:
        """
        Returns formatted command to execute on a docker container
        """
        command = "docker exec {} {} bash -c \"{}\"".format(exec_options, container, command)
        Logger().log("Running command '{}'".format(command))
        return command

    def composeExec(self, yml_location: string, container : string, command : string, exec_options = "-it") -> string:
        """
        Returns formatted command to execute on a docker container
        """
        command = "cd {} && docker-compose exec {} {} bash -c \"{}\"".format(yml_location, exec_options, container, command)
        Logger().log("Running command '{}'".format(command))
        return command

    def containerBash(self, container : string):
        """
        Returns formatted command to execute on a docker container
        """
        docker_compose_command = "docker-compose exec {} bash".format(container)
        command = "cd {} && {}".format(self.docker_dir, docker_compose_command)
        Logger().log("Running command '{}'".format(docker_compose_command))
        run(command, pty=True)