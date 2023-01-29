"""
event_name : create-angular-services
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
import os
from jennie.events.constants import *

class event_create_angular_services():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_CREATE_ANGULAR_SERVICE,
            KEY_SERVICE_NAME: "service_name"
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        os.system("ng g s services/{}".format(event_info[KEY_SERVICE_NAME]))
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_CREATE_ANGULAR_SERVICE
        }
        event_info[KEY_SERVICE_NAME] = input(INPUT_MESSAGE_SERVICE)
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        if KEY_SERVICE_NAME not in event_info:
            print (ERR_SERVICE_NAME_NOT_PRESENT)
            return False
        return event_info
