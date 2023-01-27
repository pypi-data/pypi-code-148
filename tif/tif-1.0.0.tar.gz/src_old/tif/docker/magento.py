import string
from invoke import run
from tif.fabric.logger import Logger

class Cloud:
    def __init__(self, docker_dir : string, magento_root: string) -> None:
        self.docker_dir = docker_dir
        self.magento_root = magento_root

    def docker_compose_deploy_run(self, command : string):
        docker_compose_command = "docker-compose run --rm deploy magento-command {}".format(command)
        full_command = "cd {} && {}".format(self.docker_dir, docker_compose_command)
        Logger().log("Running command '{}'".format(docker_compose_command))
        run(full_command, pty=True)

    def environment_checkout(self, environment : string):
        checkout_command = "magento-cloud environment:checkout {}".format(environment)
        full_command = "cd {} && {}".format(self.magento_root, checkout_command)
        Logger().log("Running command '{}'".format(checkout_command))
        run(full_command, pty=True)
