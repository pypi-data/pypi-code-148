import os, requests
from jennie.create_api.djangoapis import DjangoBackendAPIs
from jennie.events.rule_engine.rule_engine import RuleEngine
from jennie.events.utils.helper import get_basic_conf
from jennie.events.utils.apicallhandler import APICalls
from jennie.events.utils.checks import check_if_angular_project, check_if_django_project
from jennie.events.utils.helper import raise_error, create_readme_with_config
from jennie.events.utils.helper import take_user_input, read_json_file, write_json_file, is_file, get_app_name

from jennie.constants import KEY_EVENT_CREATE_README, \
    KEY_EVENT_DOWNLOAD, KEY_EVENT_UPLOAD, KEY_EVENT_UPDATE, \
    KEY_EVENT_DELETE, KEY_EVENT_SYNC, KEY_APP_TITLE, \
    KEY_APP_DESCRIPTION, JENNIE_CONF_FILE_NAME, KEY_EVENT_CREATE, \
    KEY_EVENT_ADD_EVENT, KEY_EVENT_CREATE_API

from jennie.events.responses import NOT_A_VALID_ANGULAR_PROJECT, NOT_A_VALID_DJANGO_PROJECT, INVALID_PROTOCOL

from jennie.events.constants import KEY_STACK_ANGULAR_AUTOMATION, \
    KEY_STACK_DJANGO_AUTOMATIONS, KEY_EVENT_TYPE, EVENT_DOWNLOAD_FILES, KEY_FILES, KEY_FILE_LINK

class AutomationHelper():
    def __init__(self, library_type, args, logger, user_info):
        """
        AutomationHelper provides basic method for automation protocols

        The basic methods provided by AutomationHelper class are
        - Download
        - Upload
        - Update
        - Delete
        - Sync
        - Create-Readme
        - Create
        - Add-Event

        Supported automations : Angular, Django

        :param library_type: TYPE OF LIBRARY
        :param args: All arguments
        :param logger: logger instance for logging purpose.
        :param user_info: User Information
        """

        self.type = library_type
        self.logger = logger
        if len(args) < 0:
            raise_error("Invalid Arguments")

        self.api_calls = APICalls(logger)
        self.event = args[0]
        self.args = args[1:]
        self.out = os.getcwd()
        if self.out[-1] == "/":
            self.out = self.out[:-1]
        self.user_info = user_info
        self.validate_protcols()

    def validate_if_library_exits(self):
        self.api_calls


    def validate_protcols(self):
        if self.type == KEY_STACK_ANGULAR_AUTOMATION:
            self.stack = "angular"
        elif self.type == KEY_STACK_DJANGO_AUTOMATIONS:
            self.stack = "django"
        else:
            raise_error(INVALID_PROTOCOL)

    @property
    def execute(self):
        """
        Generic Property supporting all events.
        :return:
        """

        if self.event == KEY_EVENT_CREATE_README:
            return self.create_readme

        elif self.event == KEY_EVENT_CREATE:
            return self.create

        elif self.event == KEY_EVENT_ADD_EVENT:
            return self.add_event

        elif self.event == KEY_EVENT_CREATE_API:
            return self.create_api

        else:
            if self.event == KEY_EVENT_DOWNLOAD:
                return self.download

            elif self.event == KEY_EVENT_UPLOAD:
                self.is_update = False
                return self.upload

            elif self.event == KEY_EVENT_UPDATE:
                self.is_update = True
                return self.upload

            elif self.event == KEY_EVENT_DELETE:
                return self.delete

            elif self.event == KEY_EVENT_SYNC:
                return self.sync_library
            else:
                print("Unknown Automation library Event")

    @property
    def create_readme(self):
        """
        Create Readme for UI library.
        A basic readme contains
        # [Title]

        [Description around the ui library]

        ## Usage Info
        :return: True/False
        """
        self.logger.debug("Create Readme for type {}".format(self.type))
        app_title = create_readme_with_config(
            JENNIE_CONF_FILE_NAME
        )
        self.logger.debug("Created Readme for {}".format(app_title))
        return True

    @property
    def download(self):
        """
        Download Automation
        Steps
        if type === "angular-automations":
            if project is not angular project
                raise error ( Not a valid angular project )

        elif type === "django-automations":
            if project is not django project
                raise error ( Not a valid angular project )

        else
            raise error ( Not a valid protocol )

        get configuration from Server.
        validate automation conf
        execute all configuration.
        :return:
        """
        # self.logger.debug("Download Automation with type ".format(self.type))
        if len(self.args) > 0:
            self.app_name = self.args[0]
        else:
            self.app_name = take_user_input({"app_name": "Input application name require to download"})["app_name"]

        if self.type == KEY_STACK_ANGULAR_AUTOMATION:
            if not check_if_angular_project(self.out):
                raise_error(NOT_A_VALID_ANGULAR_PROJECT)

        elif self.type == KEY_STACK_DJANGO_AUTOMATIONS:
            if not check_if_django_project(self.out):
                raise_error(NOT_A_VALID_DJANGO_PROJECT)
        else:
            raise_error(INVALID_PROTOCOL)

        automation_conf = self.download_config(self.app_name, self.type)
        self.logger.debug("Downloaded Automation event, execute events.", automation_conf)
        rule_engine = RuleEngine(
            app_name=self.app_name,
            app_type=self.type,
            logger=self.logger,
            token=self.user_info["token"]
        )

        validated = rule_engine.validate_events(automation_conf)
        if validated:
            rule_engine.execute_events(automation_conf)
        return True

    @property
    def upload(self):
        """
        if jennie conf filename does not exits throw error
        configuration = read jennie config file
        if update flag is on set default to configuration.
            set default = configuration

        get_basic_application with app_name, type, stack,
        api_calling_obj, and defaults.
        validate automation configration.
        upload automation to server.
        :return:
        """
        if not os.path.isfile(JENNIE_CONF_FILE_NAME):
            raise_error("Missing jennie.conf.json file for updating automations. "
                        "go to project home and run \n\tjennie angular automations sync")

        conf = read_json_file(JENNIE_CONF_FILE_NAME)
        if self.is_update:
            conf = get_basic_conf(
                app_name=conf["app_name"], type=conf["type"],
                stack=conf["stack"], api_call_obj=self.api_calls, default_inputs=conf
            )

        validated_events = RuleEngine(
            app_name=conf["app_name"],
            app_type=conf["type"],
            logger=self.logger,
            token=self.user_info["token"]
        ).validate_events(conf["automation_conf"])

        if validated_events:
            response = self.api_calls.upload_automation(
                type=self.type, json_conf=conf, is_update=self.is_update
            )
            write_json_file(JENNIE_CONF_FILE_NAME, response)
        else:
            raise_error("There is some problem with automation events, please check")
        return True

    @property
    def delete(self):
        if len(self.args) > 0:
            self.app_name = self.args[0]
        else:
            self.app_name = take_user_input({"app_name": "Input application name require to delete"})["app_name"]

        choice = input("Are your sure you want to delete {} module from server? press C to cancel".format(self.app_name))
        if choice.lower() != "c":
            self.api_calls.delete_automation_api_call(self.type, self.app_name)
            print ("Automation module deleted successfully")
        return True

    def sync_files(self, configuration):
        write_json_file(
            "{}/jennie.conf.json".format(configuration["app_name"]), configuration
        )

        if configuration["readme"] != "":
            readme_file_link = configuration["readme"]
            readme_file_path = "{}/readme.md".format(configuration["app_name"])

            file_content = self.api_calls.download_file(readme_file_link)
            open(readme_file_path, "w").write(file_content)

        if configuration["app_image"] != "":
            image_file_link = configuration["app_image"]
            image_file_path = "{}/{}".format(configuration["app_name"], image_file_link.split("/")[-1])

            f = open(image_file_path, 'wb')
            f.write(requests.get(image_file_link).content)
            f.close()

        # @todo this part of code is not running.
        for event in configuration["automation_conf"]:
            if event[KEY_EVENT_TYPE]  == EVENT_DOWNLOAD_FILES:
                for file in event[KEY_FILES]:
                    content = self.api_calls.download_file(
                        file[KEY_FILE_LINK]
                    )
                    filepath = "{}/{}".format(configuration["app_name"], file[KEY_FILE_LINK].split("/")[-1])
                    open(filepath, "w").write(content)

        return True

    @property
    def sync_library(self):
        """
        Get application name from user.
        download application configration
        create folder with app_name
        create file jennie.conf.json with application configuration inside created folder
        transverse inside automation configuration, if event_type if download_file,
        fetch and download files inside the folder.
        :return:
        """
        self.logger.debug("Sync UI Lib with type ".format(self.type))
        if len(self.args) > 0:
            self.app_name = self.args[0]
        else:
            self.app_name = take_user_input({"app_name": "Input application name require to download"})["app_name"]


        configuration = self.api_calls.download_automation(self.app_name, self.type)
        os.system("mkdir {}".format(configuration["app_name"]))
        write_json_file("{}/jennie.conf.json".format(configuration["app_name"]), configuration)

        self.sync_files(configuration)
        return True


    @property
    def create(self):
        """
        As User input for basic application configuration
        ( app_name, app_title, app_description, tag )

        once input is take, create folder with app_name
        and write jennie.conf.json file inside it.
        :return:
        """
        if len(self.args) > 0:
            self.app_name = self.args[0]
            does_app_exits, self.app_name = get_app_name(self.type, api_call_handler=self.api_calls, app_name=self.app_name)
        else:
            does_app_exits, self.app_name = get_app_name(self.type, api_call_handler=self.api_calls)

        config = get_basic_conf(
            app_name=self.app_name, type=self.type,
            stack=self.stack, api_call_obj=self.api_calls, is_create=True
        )

        os.system("mkdir {}".format(self.app_name))
        write_json_file("{}/jennie.conf.json".format(self.app_name), config)
        return True

    @property
    def add_event(self):
        """
        Check if jennie.conf.json file is present in directory.
        fetch event from Rule engine and append event to jennie.conf.json file
        update jennie.conf.json file with added event.
        :return:
        """
        if os.path.isfile(JENNIE_CONF_FILE_NAME):
            conf = read_json_file(JENNIE_CONF_FILE_NAME)
        else:
            raise Exception("Missing jennie.conf.json file for updating automations. go to project home and run \n\t"
                            "jennie angular automations sync")

        if len(self.args) > 0:
            self.event_type = self.args[0]
        else:
            self.event_type = None

        event_info = RuleEngine(
            app_name=conf["app_name"],
            app_type=conf["type"],
            logger=self.logger,
            token=self.user_info["token"]
        ).add_event(self.event_type)
        self.logger.debug("Event found: ", event_info)
        conf["automation_conf"].append(event_info)
        write_json_file(JENNIE_CONF_FILE_NAME, conf)
        return True

    @property
    def create_api(self):
        if not self.type == KEY_STACK_DJANGO_AUTOMATIONS:
            raise Exception("Create api is not available for platform type : ", self.type)

        if not check_if_django_project(self.out):
            raise Exception("Not a valid django project")

        resp = DjangoBackendAPIs(self.logger, self.api_calls).create_normal_api
        return True

    def download_config(self, app_name, app_type):
        ui_library_conf = self.api_calls.download_automation(
            app_name, app_type
        )
        return ui_library_conf["automation_conf"]



