"""
event_name : create-angular-component
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
import os
from jennie.events.constants import *
from jennie.events.colorprinting import ColorPrinting

print_log = ColorPrinting()
class event_create_angular_component():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_CREATE_ANGULAR_COMPONENT,
            KEY_COMPONENT_NAME: "name_of_component"
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        if KEY_MODULE_NAME in event_info and event_info[KEY_MODULE_NAME] != "":
            name = event_info[KEY_MODULE_NAME] + "/" + event_info[KEY_COMPONENT_NAME]
        else:                
            name = event_info[KEY_COMPONENT_NAME]


        os.system("ng g c {} --skip-tests=true > jennie.logs".format(name))
        os.system("rm -rf jennie.logs")
        print_log.success("Created Component {}".format(name))
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_CREATE_ANGULAR_COMPONENT
        }
        event_info[KEY_COMPONENT_NAME] = input("Input name of component >> ").replace(" ", "").replace("_", "").replace("-", "")
        module_name = input("Input name of module inside which the component has to be created, leave it blank for default")
        if module_name != "":
            event_info[KEY_MODULE_NAME] = module_name
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        if KEY_COMPONENT_NAME not in event_info:
            print ("Missing key {} in event configuration".format(KEY_COMPONENT_NAME))
            return False
        
        return event_info
