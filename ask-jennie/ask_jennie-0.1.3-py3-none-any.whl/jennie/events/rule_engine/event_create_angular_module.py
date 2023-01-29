"""
event_name : create-angular-module
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
import os
from jennie.events.utils.helper import *

class event_create_angular_module():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_CREATE_ANGULAR_MODULE
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        name = event_info[KEY_MODULE_NAME]
        os.system("ng g module {} --routing=true".format(name))
        os.system("ng g c {0}/{0}".format(name))
        content = "<router-outlet></router-outlet>"
        open("src/app/{0}/{0}/{0}.component.html".format(name), "w").write(content)
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_CREATE_ANGULAR_MODULE
        }
        event_info[KEY_MODULE_NAME] = input("Input name of module >> ").replace(" ", "").replace("_", "").replace("-", "")
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        if KEY_MODULE_NAME not in event_info:
            print ("Missing key {} in event configuration".format(KEY_MODULE_NAME))
            return False
        return event_info
