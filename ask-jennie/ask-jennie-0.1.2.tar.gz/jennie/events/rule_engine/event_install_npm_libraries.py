"""
event_name : install-npm-libraries
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
import os
from jennie.events.constants import *
from jennie.events.utils.helper import separate_via_comma

class event_install_npm_libraries():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_INSTALL_NPM_LIBRARIES,
            KEY_LIBS: []
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        libs_txt = " ".join(event_info["libs"])
        os.system("npm i {}".format(libs_txt))
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_INSTALL_NPM_LIBRARIES
        }
        input_libs = input(INPUT_MESSAGE_LIBS)
        event_info[KEY_LIBS] = separate_via_comma(input_libs)
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        if KEY_LIBS not in event_info:
            print(ERR_LIBRARY_NOT_PRESENT)

        if str(type(event_info["libs"])) != "<class 'list'>":
            print(ERR_LIBS_SHOULD_BE_LIST)
            return False
        return event_info
