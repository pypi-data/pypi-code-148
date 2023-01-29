"""
event_name : create-python-package
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
import os
from jennie.events.constants import *
from jennie.events.utils.helper import separate_via_comma

class event_create_python_package():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_PACKAGES: [],
            KEY_EVENT_TYPE: EVENT_CREATE_PYTHON_PACKAGE
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        for package in event_info[KEY_PACKAGES]:
            os.system("mkdir {}".format(package))
            os.system("touch {}/__init__.py".format(package))
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_CREATE_PYTHON_PACKAGE
        }
        packages_txt = input(INPUT_MESSAGE_PACKAGES_NAME)
        event_info[KEY_PACKAGES] = separate_via_comma(packages_txt)
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        if KEY_EVENT_TYPE not in event_info:
            print (ERR_PACKAGES_NOT_PRESENT)
            return False

        if str(type(event_info[KEY_PACKAGES])) != "<class 'list'>":
            print(ERR_PACKAGES_SHOULD_BE_LIST)
            return False
        return event_info
