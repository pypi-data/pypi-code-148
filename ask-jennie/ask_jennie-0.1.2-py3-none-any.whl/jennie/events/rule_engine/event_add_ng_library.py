import os
from jennie.events.constants import *
from jennie.events.utils.helper import separate_via_comma

class event_add_ng_library():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type

        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_ADD_NG_LIBRARY,
            KEY_LIBS: []
        }

    def execute(self, event_info):
        for lib in event_info[KEY_LIBS]:
            os.system("ng add {}".format(lib))
        return True

    def build_event(self):
        event_info = {
            KEY_EVENT_TYPE: EVENT_ADD_NG_LIBRARY
        }
        libraries_txt = input(INPUT_MESSAGE_LIBS)
        event_info[KEY_LIBS] = separate_via_comma(libraries_txt)
        return event_info

    def validate(self, event_info):
        if KEY_LIBS not in event_info:
            print(ERR_LIBRARY_NOT_PRESENT)
            return False

        if str(type(event_info[KEY_LIBS])) != "<class 'list'>":
            print(ERR_LIBS_SHOULD_BE_LIST)
            return False
        return event_info
