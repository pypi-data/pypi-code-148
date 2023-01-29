"""
event_name : replace-in-file
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
import os
from jennie.events.constants import *

class event_replace_in_file():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_REPLACE_IN_FILE,
            KEY_FIND_AND_REPLACE_EVENTS: [{
                KEY_FIND_TEXT: "text _to_find",
                KEY_REPLACE_TEXT: "replaceable_text",
            }]
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        content = open(event_info[KEY_OUT_PATH], "r").read()
        events = event_info[KEY_FIND_AND_REPLACE_EVENTS]
        for element in events:
            content = content.replace(element[KEY_FIND_TEXT], element[KEY_REPLACE_TEXT])
        open(event_info[KEY_OUT_PATH], "w").write(content)
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_REPLACE_IN_FILE
        }
        event_info[KEY_OUT_PATH] = input("Enter filepath on which replace operation will be performed\n>> ")
        event_info[KEY_FIND_AND_REPLACE_EVENTS] = []
        doContinue = True
        while(doContinue):
            find_text = input("Input text that need to be found\n>> ")
            replace_with = input("Input replacement text\n>> ")
            user_choice = input("Do you want to add more events (y/n)?")
            event_info[KEY_FIND_AND_REPLACE_EVENTS].append(
                {
                    KEY_FIND_TEXT: find_text,
                    KEY_REPLACE_TEXT: replace_with
                }
            )
            doContinue = user_choice.lower().replace(" ", "") == "y"

        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        if KEY_FIND_AND_REPLACE_EVENTS not in event_info:
            print ("Missing find and replace events")
            return False

        if KEY_OUT_PATH not in event_info:
            print ("Missing output path where event has to perform.")
            return False
        return event_info
