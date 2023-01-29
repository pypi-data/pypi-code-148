"""
event_name : django-automations-automations
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
import os
from jennie.events.constants import *
from jennie.events.utils.helper import separate_via_comma

class event_django_automations():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_AUTOMATIONS: [],
            KEY_EVENT_TYPE: EVENT_DJANGO_AUTOMATIONS
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        for lib in event_info[KEY_AUTOMATIONS]:
            os.system("jennie django automations download {}".format(lib))
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_DJANGO_AUTOMATIONS
        }
        libs_txt = input(INPUT_MESSAGE_AUTOMATIONS)
        event_info[KEY_AUTOMATIONS] = separate_via_comma(libs_txt)
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
