import string
from fabric.connection import Connection
from tif.fabric.logger import Logger

class Cloud:
    def __init__(self, docker_dir : string, magento_root: string) -> None:
        self.docker_dir = docker_dir
        self.magento_root = magento_root

    def docker_compose_deploy_run(self, c : Connection, command : string):
        docker_compose_command = "docker-compose run --rm deploy magento-command {}".format(command)
        with c.cd(self.docker_dir):
            Logger().log("Running command '{}'".format(docker_compose_command))
            c.run(docker_compose_command, pty=True)

    def environment_checkout(self, c : Connection, environment : string):
        checkout_command = "magento-cloud environment:checkout {}".format(environment)
        with c.cd(self.magento_root):
            Logger().log("Running command '{}'".format(checkout_command))
            c.run(checkout_command, pty=True)

    def start_mutagen(self, c : Connection):
        with c.cd(self.magento_root):
            Logger().log("Running command '{}'".format("./mutagen.sh"))
            c.run("./mutagen.sh", pty=True)

    def ece_patches_apply(self, c : Connection):
        with c.cd(self.docker_dir):
            command = "docker-compose run --rm deploy php ./vendor/bin/ece-patches apply"
            Logger().log("Running command '{}'".format(command))
            result = c.run(command, pty=True, warn=True)
            if result.return_code == 0:
                Logger().success("ece-patches apply command run successfully")
            else:
                Logger().error("ece-patches apply command exited with error")

    def exec_db_query(self, c : Connection, container : string, db_user : string, db_password : string, db_name : string, query: string):
        with c.cd(self.docker_dir):
            command = 'docker exec {} mysql -u{} -p{} {} -e "{}"'.format(container, db_user, db_password, db_name, query)
            Logger().log("Running command '{}'".format(command))
            c.run(command, pty=True)

    def cloud_deploy(self, c : Connection):
        with c.cd(self.docker_dir):
            command = "docker-compose run --rm deploy cloud-deploy"
            Logger().log("Running command '{}'".format(command))
            c.run(command, pty=True)

    def cloud_post_deploy(self, c : Connection):
        with c.cd(self.docker_dir):
            command = "docker-compose run --rm deploy cloud-post-deploy"
            Logger().log("Running command '{}'".format(command))
            c.run(command, pty=True)


    def magento_cloud_command_test(self, c : Connection) -> int:
        with c.cd(self.magento_root):
            command = 'magento-cloud'
            Logger().log("Running command '{}'".format(command))
            result = c.run(command, hide=True, warn=True)
            return result.return_code
