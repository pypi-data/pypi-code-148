import json
import os, requests
from jennie.events.rule_engine.rule_engine import RuleEngine
from jennie.events.utils.helper import raise_error
from jennie.events.utils.helper import get_basic_conf
from jennie.events.utils.apicallhandler import APICalls
from jennie.events.utils.helper import take_user_input, read_json_file, write_json_file, create_readme_without_config
from jennie.events.utils.checks import check_angular_ui_module_directory, check_if_angular_project
from jennie.events.responses import NOT_A_VALID_ANGULAR_PROJECT, INVALID_PROTOCOL
from jennie.protocols.uilib.check_for_images import get_all_images
import urllib.request
from jennie.events.colorprinting import ColorPrinting

print_logs = ColorPrinting()

from jennie.constants import KEY_EVENT_CREATE_README, \
    KEY_EVENT_DOWNLOAD, KEY_EVENT_UPLOAD, KEY_EVENT_UPDATE, \
    KEY_EVENT_DELETE, KEY_EVENT_SYNC

from jennie.events.constants import KEY_EVENT_TYPE, \
    EVENT_CREATE_ANGULAR_COMPONENT, EVENT_DOWNLOAD_FILES, KEY_COMPONENT_NAME, \
    KEY_FILE_LINK, KEY_OUT_PATH, KEY_STACK_ANGULAR_UI_LIB, KEY_MODULE_NAME, KEY_FILES


class UILibHelper():
    def __init__(self, library_type, args, logger, user_info):
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
        self.validate_platform()

    def validate_platform(self):
        if self.type == KEY_STACK_ANGULAR_UI_LIB:
            self.stack = "angular"
        else:
            raise_error(INVALID_PROTOCOL)

    @property
    def execute(self):
        if self.event == KEY_EVENT_CREATE_README:
            return self.create_readme

        elif self.event == KEY_EVENT_DOWNLOAD:
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
            print("Unknown UI library Event")

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
        files = check_angular_ui_module_directory(self.out)
        if files:
            self.app_name = self.out.split("/")[-1]
            create_readme_without_config(
                self.app_name, self.type
            )
        else:
            raise_error("Not a valid Angular UI Library directory")
        return True

    def add_module_to_downloaded_config(self, module_name, automation_conf):
        if module_name == "":
            return automation_conf
        else:
            for event in automation_conf:
                if event[KEY_EVENT_TYPE] == EVENT_CREATE_ANGULAR_COMPONENT:
                    event[KEY_MODULE_NAME] = module_name

                elif event[KEY_EVENT_TYPE] == EVENT_DOWNLOAD_FILES:
                    for file in event[KEY_FILES]:
                        file[KEY_OUT_PATH] = file[KEY_OUT_PATH].replace("/ui-lib/", "/" + module_name + "/ui-lib/")
            return automation_conf

    @property
    def download(self):
        """
        Check if directory is an angular project
        if angular project:
            if type === "angular-ui-lib":
                - download automation configuration
                - execute downloaded configuration

        :return:
        """
        print_logs.info("Downloading UI library")
        self.logger.debug("Download UI Lib with type ".format(self.type))
        self.module_name = ""
        if len(self.args) > 0:
            self.app_name = self.args[0]
            if (len(self.args) > 1):
                if self.args[1].split("=")[0] == "--module" and len(self.args[1].split("=")) > 1:
                    self.module_name = self.args[1].split("=")[1]
        else:
            self.app_name = take_user_input(
                {"app_name": "Input application name require to download"}
            )["app_name"]

        if check_if_angular_project(self.out):
            automation_conf = self.download_ui_config(self.app_name, self.type)
            automation_conf = self.add_module_to_downloaded_config(self.module_name, automation_conf)
            self.logger.debug("Downloaded Automation event, execute events.", automation_conf)

            RuleEngine(
                app_name=self.app_name,
                app_type=self.type,
                logger=self.logger,
                token=self.user_info["token"]
            ).execute_events(automation_conf)
            print_logs.success("Angular UI library Downloaded Successfully")
            if (self.type == "angular-ui-lib"):
                print("\n")
                message = "Declare html component to use library\n<app-{0}></app-{0}>".format(self.app_name)
                ColorPrinting().info(message)
                print("\n")
        else:
            print_logs.error("UI library is not found on the server")
            raise Exception (NOT_A_VALID_ANGULAR_PROJECT)
        return True

    @property
    def upload(self):
        if self.is_update:
            if os.path.isfile("jennie.conf.json"):
                default_inputs = read_json_file("jennie.conf.json")
            else:
                raise Exception("Missing jennie.conf.json file for updating automations. go to project home and run \n\t"
                                "jennie angular ui-lib sync")
            self.logger.debug("Update UI Lib with type ".format(self.type))
        else:
            self.logger.debug("Download UI Lib with type ".format(self.type))
            default_inputs = None

        files = check_angular_ui_module_directory(self.out)
        if not files:
            raise Exception(NOT_A_VALID_ANGULAR_PROJECT)
        self.app_name = self.out.split("/")[-1]
        status = self.api_calls.validate_automation_api_call(KEY_STACK_ANGULAR_UI_LIB, self.app_name)

        if not self.is_update and status:
            raise Exception("Library Already Exits")

        if self.is_update and not status:
            raise Exception("Library Does not Exits")

        app_conf = get_basic_conf(
            app_name=self.app_name, type=self.type, stack="angular",
            api_call_obj=self.api_calls, default_inputs=default_inputs
        )
        app_conf["automation_conf"] = self.build_angular_ui_module_automation_conf()
        self.logger.debug("Upload App configration to sererver", app_conf)
        self.upload_angular_ui_module_automation_conf(
            type=self.type, app_conf=app_conf, is_update=self.is_update
        )

        print_logs.success("Angular UI library Uploaded Successfully")
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
            print ("UI module deleted successfully")
        return True

    def download_image(self, filepath, filelink):
        f = open(filepath, 'wb')
        f.write(requests.get(filelink).content)
        f.close()
        return True

    def sync_library_files(self, ui_library_conf):
        write_json_file(
            "src/app/ui-lib/{}/jennie.conf.json".format(ui_library_conf["app_name"]), ui_library_conf
        )

        if ui_library_conf["readme"] != "":
            readme_file_link = ui_library_conf["readme"]
            readme_file_path = "src/app/ui-lib/{}/readme.md".format(ui_library_conf["app_name"])

            file_content = self.api_calls.download_file(readme_file_link)
            open(readme_file_path, "w").write(file_content)

        if ui_library_conf["app_image"] != "":

            image_file_link = ui_library_conf["app_image"]
            image_file_path = "src/app/ui-lib/{}/{}".format(ui_library_conf["app_name"], image_file_link.split("/")[-1])

            self.download_image(image_file_path, image_file_link)

        return True

    @property
    def sync_library(self):
        self.logger.debug("Sync UI Lib with type ".format(self.type))
        if len(self.args) > 0:
            self.app_name = self.args[0]
        else:
            self.app_name = take_user_input({"app_name": "Input application name require to sync"})["app_name"]

        if check_if_angular_project(self.out):
            ui_library_conf = self.api_calls.download_automation(
                self.app_name, self.type
            )
            automation_conf = ui_library_conf["automation_conf"]
            self.logger.debug("Downloaded Automation event, execute events.", automation_conf)
            RuleEngine(
                app_name=self.app_name,
                app_type=self.type,
                logger=self.logger,
                token=self.user_info["token"]
            ).execute_events(automation_conf)
            self.sync_library_files(ui_library_conf)

        else:
            raise Exception("Not a valid angular project")
        return True

    def download_ui_config(self, app_name, app_type):
        ui_library_conf = self.api_calls.download_automation(
            app_name, app_type
        )
        return ui_library_conf["automation_conf"]

    def execute_automation_event(self):
        return True

    def build_angular_ui_module_automation_conf(self):
        """
        Upload CSS, HTML, TS file to server and build automation
        configuration for angular application.
        :return: automation_conf
        """
        automation_conf = []
        automation_conf.append(
            {
                KEY_EVENT_TYPE: EVENT_CREATE_ANGULAR_COMPONENT,
                KEY_COMPONENT_NAME: "ui-lib/" + self.app_name
            }
        )
        files = [
            self.app_name + ".component.css",
            self.app_name + ".component.ts",
            self.app_name + ".component.html",
        ]

        response = self.api_calls.upload_files(
            filepaths=files,
            app_name=self.app_name,
            type=self.type
        )
        automation_conf.append(
            {
                KEY_EVENT_TYPE: EVENT_DOWNLOAD_FILES,
                "files": [
                    {
                        KEY_FILE_LINK: response[0],
                        KEY_OUT_PATH: "src/app/ui-lib/{0}/{0}.component.css".format(self.app_name)
                    },
                    {
                        KEY_FILE_LINK: response[1],
                        KEY_OUT_PATH: "src/app/ui-lib/{0}/{0}.component.ts".format(self.app_name)
                    },
                    {
                        KEY_FILE_LINK: response[2],
                        KEY_OUT_PATH: "src/app/ui-lib/{0}/{0}.component.html".format(self.app_name)
                    }
                ]
            }
        )
        images = get_all_images(self.app_name + ".component.html")
        for key in images:
            image_path = os.getcwd().split("/src/")[0] + "/src/" + key
            response_images = self.api_calls.upload_image(image_path)
            automation_conf[1]["files"].append(
                {
                    KEY_FILE_LINK: response_images,
                    "KEY_OUT_PATH": "src/assets/" + key
                }
            )
        return automation_conf

    def upload_angular_ui_module_automation_conf(self, type, app_conf, is_update):
        """
        Upload CSS, HTML, TS file to server and build automation
        configuration for angular application.
        :return: automation_conf
        """
        response = self.api_calls.upload_automation(type, app_conf, is_update)
        write_json_file("jennie.conf.json", response)
        return True



