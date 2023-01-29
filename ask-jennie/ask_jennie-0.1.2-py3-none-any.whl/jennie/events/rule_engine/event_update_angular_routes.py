"""
event_name : update-angular-routes
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
from jennie.events.utils.helper import *

class event_update_angular_routes():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_UPDATE_ANGULAR_ROUTES,
            KEY_ROUTES_FILE_LINK: "route_file_server_link",
            KEY_AUTH_GUARD_FILE_LINK: "auth_gaurd_server_link (optional)"
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        route_file_content = download_text_file(event_info[KEY_ROUTES_FILE_LINK])
        open("app/src/app.routes.ts", "w").write(route_file_content)
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_UPDATE_ANGULAR_ROUTES,
            KEY_ROUTES_FILE_LINK: "",
            KEY_AUTH_GUARD_FILE_LINK: ""
        }

        filepath = input("Input routes.ts file path \n >> ")
        authguard_filepath = input("Input auth-guard.ts file path ( Optional )\n >> ")
        event_info[KEY_ROUTES_FILE_LINK] = upload_text_file(filepath, self.app_name, self.type, self.user_key)
        if len(authguard_filepath) > 3:
            event_info[KEY_AUTH_GUARD_FILE_LINK] = upload_text_file(
                authguard_filepath, self.app_name, self.type, self.user_key)

        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        if not KEY_ROUTES_FILE_LINK in event_info:
            print ("Missing '{}' in event information".format(KEY_ROUTES_FILE_LINK))
            return False
        return event_info
