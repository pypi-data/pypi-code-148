"""
event_name : update-angular-json
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
import json
from jennie.events.utils.helper import *

class event_update_angular_json():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_UPDATE_ANGULAR_JSON,
            KEY_SCRIPTS: "list_of_scripts",
            KEY_STYLES: "list_of_styles",
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        self.content = json.loads(open("angular.json").read())
        self.project_name = str(os.getcwd()).split("/")[-1]
        if KEY_STYLES in event_info:
            styles = self.content["projects"][self.project_name]["architect"]["build"]["options"][KEY_STYLES]
            counter = 0
            styles_to_add = event_info[KEY_STYLES]
            for path in styles_to_add:
                if path not in styles:
                    styles.insert(counter, path)
                counter += 1
            self.content["projects"][self.project_name]["architect"]["build"]["options"][KEY_STYLES] = styles

        if KEY_SCRIPTS in event_info:
            scripts = self.content["projects"][self.project_name]["architect"]["build"]["options"][KEY_SCRIPTS]
            counter = 0
            scripts_to_add = event_info[KEY_SCRIPTS]
            for path in scripts_to_add:
                if path not in scripts:
                    scripts.insert(counter, path)
                counter += 1
            self.content["projects"][self.project_name]["architect"]["build"]["options"][KEY_SCRIPTS] = scripts

        with open("angular.json", 'w', encoding='utf-8') as f:
            json.dump(self.content, f, ensure_ascii=False, indent=4)

        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_UPDATE_ANGULAR_JSON
        }
        styles_txt = input(INPUT_MESSAGE_STYLES)
        event_info[KEY_STYLES] = separate_via_comma(styles_txt)
        scripts_txt = input(INPUT_MESSAGE_SCRIPTS)
        event_info[KEY_SCRIPTS] = separate_via_comma(scripts_txt)
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        if not KEY_STYLES in event_info and not KEY_SCRIPTS in event_info:
            print(ERR_SCRIPTS_OR_STYLES_MISSING)
            return False
        return event_info


