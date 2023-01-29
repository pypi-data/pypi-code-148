"""
event_name : create-multiple-angular-components
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
import os
from jennie.events.utils.helper import *

class event_create_multiple_angular_components():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_CREATE_MULTIPLE_ANGULAR_COMPONENTS
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        continue_creating = True
        while(continue_creating):
            component_name = input("\nInput page name that need to be created\n>> ")
            if KEY_MODULE_NAME in event_info and event_info[KEY_MODULE_NAME] != "":
                name = event_info[KEY_MODULE_NAME] + "/" + component_name
            else:
                name = component_name

            os.system("ng g c {} --skip-tests=true > event.logs".format(name))
            choice = input("\nDo you want to add more pages? (y/n) \n>> ")
            if choice.lower() == "y":
                continue_creating = True
            else:
                continue_creating = False
            os.system("rm -rf event.logs")
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_CREATE_MULTIPLE_ANGULAR_COMPONENTS
        }
        module_name = input(
            "Input name of module inside which the component "
            "has to be created, leave it blank for default\n>> "
        )
        if module_name != "":
            event_info[KEY_MODULE_NAME] = module_name
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        return event_info
