"""
event_name : update-urls-py
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
import os
from jennie.events.utils.helper import *

class event_update_urls_py():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_UPDATE_URLS_PY,
            KEY_URLS_PY_FILE_LINK: "url_file_server_link"
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        route_file_content = download_text_file(event_info[KEY_URLS_PY_FILE_LINK])
        filepath = input("Input url.py filepath \n>>")
        open(filepath, "w").write(route_file_content)
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_UPDATE_URLS_PY
        }

        filepath = input("Input updated urls.py file path\n >> ")
        event_info[KEY_URLS_PY_FILE_LINK] = upload_text_file(filepath, self.app_name, self.type, self.user_key)
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        if KEY_URLS_PY_FILE_LINK not in event_info:
            print ("Missing urls'py file file.")
            return False
        return event_info
