"""
event_name : copy-angular-component
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
import os
from jennie.events.utils.helper import download_text_file, list_all_files_from_folder, upload_text_file
from jennie.events.constants import *

class event_copy_angular_component():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        self.sample_conf = {
            KEY_COMPONENTS: [{
                KEY_COMPONENT_NAME: "",
                KEY_COMPONENT_FILES: [],
            }],
            KEY_EVENT_TYPE: EVENT_COPY_ANGULAR_COMPONENT
        } # replace with sample configuration.


    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        files = event_info[KEY_COMPONENT_FILES]
        for file in files:
            file_content = download_text_file(file[KEY_FILE_LINK])
            open(file[KEY_OUT_PATH], "w").write(file_content)
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_COPY_ANGULAR_COMPONENT,
            KEY_COMPONENT_FILES: []
        }

        component_path = input("Input absolute path for the component to copy. \n>> ")
        out_path = input("Input output path for component. \n>> ")
        if out_path[-1] != "/":
            out_path += "/"
        if not os.path.exists(component_path):
            print("Component does not exits :", component_path)
            return False

        files_list = list_all_files_from_folder(component_path)
        for file in files_list:
            if file.split(".")[-1] in ["html", "css", "ts"]:
                filepath = os.path.join(component_path, file)
                file_link = upload_text_file(filepath, self.app_name, self.type, self.user_key)
                event_info[KEY_COMPONENT_FILES].append({
                    KEY_FILE_LINK: file_link,
                    KEY_OUT_PATH: out_path + file_link.split("/")[-1]
                })
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        if KEY_COMPONENT_FILES not in event_info:
            print(ERR_COMPONENT_NAMES_NOT_PRESENT)
            return False

        if str(type(event_info[KEY_COMPONENT_FILES])) != "<class 'list'>":
            print(ERR_COMPONENT_NAMES_SHOULD_BE_LIST)
            return False
        return event_info
