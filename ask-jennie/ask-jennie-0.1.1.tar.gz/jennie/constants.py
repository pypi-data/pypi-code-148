import os, json

BASE_URL = "https://api.ask-jennie.com/"

LOGIN_URL = BASE_URL + "v1/login/"
LOGIN_VIA_GOOGLE_URL = BASE_URL + "v1/continue-with-google/"
LOGIN_VIA_KEY = BASE_URL + "v1/active-sdk/"
AUTOMATION_URL = BASE_URL + "v1/automation/TYPE/"
AUTOMATION_SYNC_URL = BASE_URL + "v1/automation/sync/"
AUTOMATION_VALIDATE_URL = BASE_URL + "v1/automation/TYPE/validate/"
CUSTOM_AUTOMATION_URL = BASE_URL + "v1/custom-automations/TYPE/validate/"
CUSTOM_AUTOMATION_VALIDATE_URL = BASE_URL + "v1/custom-automations/TYPE/validate/"
IMAGE_UPLOAD_URL = BASE_URL + "v1/image_upload/"
TEXT_UPLOAD_URL = BASE_URL + "v1/file_upload/"


KEY_EVENT_UPLOAD = "upload"
KEY_EVENT_DOWNLOAD = "download"
KEY_EVENT_CREATE_README = "create-readme"
KEY_EVENT_UPDATE = "update"
KEY_EVENT_DELETE = "delete"
KEY_EVENT_CREATE = "create"
KEY_EVENT_ADD_EVENT = "add-event"
KEY_EVENT_SYNC = "sync"
KEY_EVENT_CREATE_API = "create-api"


KEY_APP_TITLE = "app_title"
KEY_APP_DESCRIPTION = "app_description"
JENNIE_CONF_FILE_NAME = "jennie.conf.json"

AUTOMATION_COMMANDS = {
    "angular": {
        "ui-lib": {
            KEY_EVENT_CREATE_README: None,
            KEY_EVENT_DOWNLOAD: "library_name",
            KEY_EVENT_UPLOAD: None,
            KEY_EVENT_UPDATE: None,
            KEY_EVENT_DELETE: "library_name",
            KEY_EVENT_SYNC: "library_name"
        },
        "automations": {
            KEY_EVENT_DOWNLOAD: "library_name",
            KEY_EVENT_UPLOAD: None,
            KEY_EVENT_UPDATE: None,
            KEY_EVENT_DELETE: "library_name",
            KEY_EVENT_SYNC: None,
            KEY_EVENT_CREATE: "library_name",
            KEY_EVENT_ADD_EVENT: "event_name",
            KEY_EVENT_CREATE_README: None
        }
    },
    "django": {
        "automations": {
            KEY_EVENT_DOWNLOAD: "library_name",
            KEY_EVENT_UPLOAD: None,
            KEY_EVENT_UPDATE: None,
            KEY_EVENT_DELETE: "library_name",
            KEY_EVENT_SYNC: None,
            KEY_EVENT_CREATE: "library_name",
            KEY_EVENT_ADD_EVENT: "event_name",
            KEY_EVENT_CREATE_README: None,
            KEY_EVENT_CREATE_API: None
        },
    },
    "ubuntu": {
        "setup":  {
            "lemp": None,
            "phpmyadmin": None,
            "elk": None,
            "elasticsearch": None
        },
        "deploy": {
            "django": None,
            "web": None
        }
    },
    "logout": None,
    "version": None
}

USER_INPUT_FOR_SETUP = {
    "email": "Kindly enter email address registered with ASK jennie, \nDon't have account go to https://ask-jennie.com/register"
}

AUTOMATION_BASIC_INPUT = {
    "app_title": "Title for automations module", "app_description": "Description for automations module",
    "tag": "Tag (optional) for automations module",
}

TYE_STR = "<class 'str'>"
TYE_LIST = "<class 'list'>"
TYE_DICT = "<class 'dict'>"

def is_str(variable):
    if str(type(variable)) == TYE_STR:
        return True
    return False

def is_arr(variable):
    if str(type(variable)) == TYE_LIST:
        return True
    return False

def is_dict(variable):
    if str(type(variable)) == TYE_DICT:
        return True
    return False

def create_automation_package(app_name, basic_automation_detail):
    """
    Creates directory for automations and write jennie.conf.json file in it.
    :param app_name: Application Name
    :param basic_automation_detail: Automation Information.
    :return: True
    """
    os.system("mkdir " + app_name)
    with open('{}/jennie.conf.json'.format(app_name), 'w') as f:
        json.dump(basic_automation_detail, f, indent=2)
    return True