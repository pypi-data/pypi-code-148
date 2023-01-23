from .utils import cookiecutter_generate
import requests
import json
import json.decoder
import logging
from click import echo
from evolved5g.sdk import CAPIFInvokerConnector
import traceback


class CLI_helper:

    def __init__(self):

        self.url_curl = "https://epg-api.tid.es/api/executions"
        self.url_token = "https://epg-api.tid.es/api/auth"
        self.username_token = "usu_Evolved5g"
        self.password_token = "evolved5g"
        self.netapp_branch = "evolved5g"
        self.branch_cicd_repo = "develop"
        self.header = {"Content-Type": "application/json", "accept": "application/json", "Authorization": None}
        self.repository = "https://api.github.com/repos/EVOLVED-5G"
        self.jenkinsjob = {"bdd": "003-NETAPPS/999-ToReview/",
                               "code_analysis": "003-NETAPPS/003-Helpers/001-Static Code Analysis",
                               "capif_nef": "1001-DUMMY_NETAPP_VERIFICATION/test-dummy-netapp/verification-tests",
                               "security_scan": ["003-NETAPPS/003-Helpers/002-Security Scan Code",
                                                 "003-NETAPPS/003-Helpers/003-Security Scan Secrets",
                                                 "003-NETAPPS/003-Helpers/004-Security Scan Docker Images"]}

    def generate(self, config_file):
        """Generate EVOLVED-5G compliant NetApp from template"""
        location = "gh:EVOLVED-5G/NetApp-template"
        directory = "template"
        cookiecutter_generate(location, config_file, directory, no_input=True)

    def generate_token(self):

        self.header = {"content-Type": "application/json", "accept": None, "Authorization": None}
        data = '{ "username": "' + self.username_token + '", "password": "' + self.password_token + '" }'
        resp = requests.post(self.url_token, headers=self.header, data=data)
        return (resp.json()["access_token"])

    def run_verification_tests(self, mode, repo):
        """Run the build pipeline for the EVOLVED-5G NetApp"""

        if repo is None:
            echo ("'None' value provided.\nPlease enter the correct command: evolved5g run-verification-tests --mode build --repo REPOSITORY_NAME")
        else:
            r = requests.get(f"{self.repository}/{repo}")
            repo_exist = r.json()

            if "message" not in repo_exist:
                try:
                    if mode == "build":
                        self.header = {"content-Type": "application/json", "accept": "application/json",
                                       "Authorization": self.generate_token()}
                        data = '{ "instance": "pro-dcip-evol5-01.hi.inet", "job": "' + self.jenkinsjob["bdd"] + mode + '", "parameters": { "VERSION": "1.0", "GIT_NETAPP_URL": "https://github.com/EVOLVED-5G/' + repo + '", "GIT_NETAPP_BRANCH": "' + self.netapp_branch + '", "GIT_CICD_BRANCH": "' + self.branch_cicd_repo + '"} }'
                        resp = requests.post(self.url_curl, headers=self.header, data=data)
                        
                        echo(f"Your pipeline ID is: {resp.json()['id']} and the actual status is: {resp.json()['status']}.")
                    elif mode == "deploy":
                        self.header = {"content-Type": "application/json", "accept": "application/json",
                                       "Authorization": self.generate_token()}
                        data = '{ "instance": "pro-dcip-evol5-01.hi.inet", "job": "' + self.jenkinsjob["bdd"] + mode + '", "parameters": { "GIT_CICD_BRANCH": "' + self.branch_cicd_repo + '", "APP_REPLICAS": "1", "DEPLOYMENT_NAME": "' + repo + '", "DEPLOYMENT": "openshift" } }'
                        resp = requests.post(self.url_curl, headers=self.header, data=data)

                        echo(f"Your pipeline ID is: {resp.json()['id']} and the actual status is: {resp.json()['status']}.")
                    elif mode == "destroy":
                        self.header = {"content-Type": "application/json", "accept": "application/json",
                                       "Authorization": self.generate_token()}
                        data = '{ "instance": "pro-dcip-evol5-01.hi.inet", "job": "' + self.jenkinsjob["bdd"] + mode + '", "parameters": { "VERSION": "1.0", "GIT_NETAPP_URL": "https://github.com/EVOLVED-5G/' + repo + '", "GIT_NETAPP_BRANCH": "' + self.netapp_branch + '", "GIT_CICD_BRANCH": "' + self.branch_cicd_repo + '"} }'
                        resp = requests.post(self.url_curl, headers=self.header, data=data)

                        echo(f"Your pipeline ID is: {resp.json()['id']} and the actual status is: {resp.json()['status']}.")
                    elif mode == "code_analysis":
                        self.header = {"content-Type": "application/json", "accept": "application/json",
                                       "Authorization": self.generate_token()}
                        data = '{ "instance": "pro-dcip-evol5-01.hi.inet", "job": "' + self.jenkinsjob["code_analysis"] + '", "parameters": { "GIT_NETAPP_URL": "https://github.com/EVOLVED-5G/' + repo + '","GIT_CICD_BRANCH": "develop", "BUILD_ID": "0" , "REPORTING": "true" , "GIT_NETAPP_BRANCH": "' + self.netapp_branch + '"} }'
                        resp = requests.post(self.url_curl, headers=self.header, data=data)

                        echo(f"Your pipeline ID is: {resp.json()['id']} and the actual status is: {resp.json()['status']}.")
                    elif mode == "security_scan":
                        self.header = {"content-Type": "application/json", "accept": "application/json",
                                       "Authorization": self.generate_token()}
                        data1 = '{ "instance": "pro-dcip-evol5-01.hi.inet", "job": "' + self.jenkinsjob["security_scan"][0] + '", "parameters": { "GIT_NETAPP_URL": "https://github.com/EVOLVED-5G/' + repo + '","GIT_CICD_BRANCH": "develop", "BUILD_ID": "0" , "REPORTING": "true" , "GIT_NETAPP_BRANCH": "' + self.netapp_branch + '"} }'
                        data2 = '{ "instance": "pro-dcip-evol5-01.hi.inet", "job": "' + self.jenkinsjob["security_scan"][1] + '", "parameters": { "GIT_NETAPP_URL": "https://github.com/EVOLVED-5G/' + repo + '","GIT_CICD_BRANCH": "develop", "BUILD_ID": "0" , "REPORTING": "true" , "GIT_NETAPP_BRANCH": "' + self.netapp_branch + '"} }'
                        data3 = '{ "instance": "pro-dcip-evol5-01.hi.inet", "job": "' + self.jenkinsjob["security_scan"][2] + '", "parameters": { "GIT_NETAPP_URL": "https://github.com/EVOLVED-5G/' + repo + '","GIT_CICD_BRANCH": "develop", "BUILD_ID": "0" , "REPORTING": "true" , "GIT_NETAPP_BRANCH": "' + self.netapp_branch + '"} }'
                        resp1 = requests.post(self.url_curl, headers=self.header, data=data1)
                        resp2 = requests.post(self.url_curl, headers=self.header, data=data2)
                        resp3 = requests.post(self.url_curl, headers=self.header, data=data3)

                        echo(f"Your pipeline ID is: {resp1.json()['id']} and the actual status is: {resp1.json()['status']}.")
                        echo(f"Your pipeline ID is: {resp2.json()['id']} and the actual status is: {resp2.json()['status']}.")
                        echo(f"Your pipeline ID is: {resp3.json()['id']} and the actual status is: {resp3.json()['status']}.")
                    elif mode == "capif_nef":
                        self.header = {"content-Type": "application/json", "accept": "application/json",
                                       "Authorization": self.generate_token()}
                        data = '{ "instance": "pro-dcip-evol5-01.hi.inet", "job": "' + self.jenkinsjob["capif_nef"] + '", "parameters": { "NetApp_repo": "' + repo + '","NetApp_repo_branch": "' + self.netapp_branch + '", "ROBOT_DOCKER_IMAGE_NAME": "dockerhub.hi.inet/dummy-netapp-testing/robot-test-image", "ROBOT_DOCKER_IMAGE_VERSION": "3.1.1"} }'
                        resp = requests.post(self.url_curl, headers=self.header, data=data)

                        echo(f"Your pipeline ID is: {resp.json()['id']} and the actual status is: {resp.json()['status']}.")
                    else:
                        echo(f"The {mode} you have chosen does not exist, please check the modes and try again")

                except ValueError as e:
                    echo("Please enter the correct command: evolved5g run-verification-tests --mode build --repo REPOSITORY_NAME")
            else:
                echo(f"The {repo} repository you have chosen does not exist, please check the name you typed and try again.")

    def check_job(self, id):

        """Check the status of the pipeline for the EVOLVED-5G NetApp"""

        try:
            self.header = {"content-Type": "application/json", "accept": "application/json",
                           "Authorization": self.generate_token()}
            resp = requests.get(f"{self.url_curl}/{id}", headers=self.header)
            result = resp.json()

            if result["status"] == "QUEUED":
                echo(result)
            else:
                console = (json.dumps(result["console_log"]).split('\\n'))

                for element in console:
                    if "] { (" in element:
                        echo(element)
                    elif "[Pipeline]" not in element:
                        echo(element)
                    elif "] stage" in element:
                        echo(element)
        except ValueError as e:
            echo("Please add the ID: evolved5g check-job --id <yourID>")

    def register_and_onboard_to_capif(self, config_file_full_path: str) -> None:
        with open(config_file_full_path, 'r') as openfile:
            config = json.load(openfile)
        capif_connector = CAPIFInvokerConnector(folder_to_store_certificates=config["folder_to_store_certificates"],
                                                capif_host=config["capif_host"],
                                                capif_http_port=config["capif_http_port"],
                                                capif_https_port=config["capif_https_port"],
                                                capif_netapp_username=config["capif_netapp_username"],
                                                capif_netapp_password=config["capif_netapp_password"],
                                                capif_callback_url=config["capif_callback_url"],
                                                description=config["description"],
                                                csr_common_name=config["csr_common_name"],
                                                csr_organizational_unit=config["csr_organizational_unit"],
                                                csr_organization=config["csr_organization"],
                                                crs_locality=config["crs_locality"],
                                                csr_state_or_province_name= config["csr_state_or_province_name"],
                                                csr_country_name=config["csr_country_name"],
                                                csr_email_address=config["csr_email_address"])
        try:
            capif_connector.register_and_onboard_netapp()
            echo("Your netApp has been successfully registered and onboarded to the CAPIF server." +
                 "You can now start using the evolved5G SDK!")
        except Exception:
            echo("An error occurred. Registration failed:")
            traceback.print_exc()
