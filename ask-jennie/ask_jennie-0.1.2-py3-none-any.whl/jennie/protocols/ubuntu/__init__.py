from jennie.events.ubuntu.deployfrontend import deploy_folder_nginx
from jennie.events.ubuntu.deploybackend import deploy_django
from jennie.events.ubuntu.setuplemp import setup_lemp
from jennie.events.ubuntu.setupelasticsearchkibana import setup_elasticsearchkibana
from jennie.events.ubuntu.setupphpmyadmin import install_phpmyadmin
from jennie.events.ubuntu.setupelasticsearch import setup_elasticsearch
from jennie.events.utils.helper import take_user_input

DEPLOY_INFO_COMMANDS = {
    "port": "Input port no to which the project has to be deployed",
    "domain": "Input your domain name, can add IP address as domain name"
}

class UbuntuAutomation():
    def execute(self, args):
        if args[1] == "setup" and args[2] == "elk":
            return setup_elasticsearchkibana()

        elif args[1] == "setup" and args[2] == "elasticsearch":
            return setup_elasticsearch()

        elif args[1] == "setup" and args[2] == "lemp":
            return setup_lemp()

        elif args[1] == "setup" and args[2] == "phpmyadmin":
            return install_phpmyadmin()

        elif args[1] == "deploy" and args[2] == "web":
            UbuntuDeployAutomations().web()

        elif args[1] == "deploy" and args[2] == "django":
            UbuntuDeployAutomations().django()

class UbuntuDeployAutomations():
    def __init__(self):
        self.info = take_user_input(DEPLOY_INFO_COMMANDS)

    def web(self):
        deploy_folder_nginx(self.info["port"], self.info["domain"])

    def django(self):
        deploy_django(self.info["port"], self.info["domain"])




