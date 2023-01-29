"""
event_name : angular-automations
description : Add Jennie Angular Automation to project.
config format:

{
    "event_type": "angular-automations",
    "automations": []
}

"""
import os
from jennie.events.constants import *
from jennie.events.utils.helper import separate_via_comma

class event_angular_automations():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type

        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_ANGULAR_AUTOMATIONS,
            KEY_AUTOMATIONS: []
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        for lib in event_info[KEY_AUTOMATIONS]:
            os.system("jennie angular automations download {}".format(lib))
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_ANGULAR_AUTOMATIONS
        }
        libraries_txt = input(INPUT_MESSAGE_AUTOMATIONS)
        event_info[KEY_AUTOMATIONS] = separate_via_comma(libraries_txt)
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        if KEY_AUTOMATIONS not in event_info:
            print(ERR_AUTOMATIONS_NOT_PRESENT)
            return False

        if str(type(event_info[KEY_AUTOMATIONS])) != "<class 'list'>":
            print(ERR_AUTOMATIONS_SHOULD_BE_LIST)
            return False
        return event_info
