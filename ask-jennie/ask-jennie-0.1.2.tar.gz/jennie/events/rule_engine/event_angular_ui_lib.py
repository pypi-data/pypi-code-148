"""
event_name : angular-ui_lib
description : Add Jennie Angular UI lib to project
config format:

**Place Your Sample configuration here here**

"""
import os
from jennie.events.constants import *
from jennie.events.utils.helper import separate_via_comma

class event_angular_ui_lib():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type

        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_ANGULAR_UI_LIB,
            KEY_LIBS: []
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        if KEY_MODULE_NAME in event_info and event_info[KEY_MODULE_NAME] != "":
            for lib in event_info[KEY_LIBS]:
                os.system("jennie angular ui-lib download {} --module={}".format(
                    lib, event_info[KEY_MODULE_NAME]
                ))
        else:
            for lib in event_info[KEY_LIBS]:
                os.system("jennie angular ui-lib download {}".format(lib))
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_ANGULAR_UI_LIB
        }
        libraries_txt = input(INPUT_MESSAGE_LIBS)
        event_info[KEY_LIBS] = separate_via_comma(libraries_txt)
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        if KEY_LIBS not in event_info:
            print(ERR_LIBRARY_NOT_PRESENT)
            return False

        if str(type(event_info[KEY_LIBS])) != "<class 'list'>":
            print(ERR_LIBS_SHOULD_BE_LIST)
            return False
        return event_info
