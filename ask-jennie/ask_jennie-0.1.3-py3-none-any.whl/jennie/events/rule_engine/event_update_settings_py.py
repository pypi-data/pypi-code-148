"""
event_name : update-settings-py
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
from jennie.events.utils.helper import *

class event_update_settings_py():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_UPDATE_SETTINGS_PY,
            KEY_SETTINGS_PY_FILE_LINK: "settings-py_file_download_link"
        } # replace with sample configuration.

    def get_settings_file_path(self):
        result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(".") for f in filenames if
                  os.path.splitext(f)[1] == '.py']
        path = None
        for key in result:
            key = key.replace("./", "")
            if key.split("/")[-1] == "settings.py" and len(key.split("/")) == 2:
                path = key

        return path

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        content = download_text_file(event_info[KEY_SETTINGS_PY_FILE_LINK])
        filepath = self.get_settings_file_path()
        if not filepath:
            filepath = input("Input filepath for settings.py file")
        open(filepath, "w").write(content)
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_UPDATE_SETTINGS_PY
        }

        filepath = input("Input updated settings.py file path\n >> ")
        event_info[KEY_SETTINGS_PY_FILE_LINK] = upload_text_file(filepath, self.app_name, self.type, self.user_key)
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        if KEY_SETTINGS_PY_FILE_LINK not in event_info:
            print ("Missing {} in event info".format(KEY_SETTINGS_PY_FILE_LINK))
            return False
        return event_info
