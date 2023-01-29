"""
event_name : add-script-to-index
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
import os
from jennie.events.utils.helper import *
from jennie.events.utils.helper import separate_via_comma

class event_add_script_to_index():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_ADD_SCRIPT_TO_INDEX
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        content_index = open("src/index.html").read()
        for script in event_info[KEY_SCRIPTS]:
            content_index = content_index.replace("<app-root></app-root>", "<app-root></app-root>\n<script src='{}'></script>".format(
                script
            ))
        open("src/index.html", "w").write(content_index)
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_ADD_SCRIPT_TO_INDEX
        }

        event_info[KEY_SCRIPTS] = separate_via_comma(input(INPUT_MESSAGE_SCRIPTS))
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        if KEY_SCRIPTS not in event_info:
            print(ERR_SCRIPTS_MISSING)
            return False

        if str(type(event_info[KEY_SCRIPTS])) != "<class 'list'>":
            print(ERR_SCRIPTS_SHOULD_BE_LIST)
            return False
        return event_info
