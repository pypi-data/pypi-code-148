import os, json
import requests, os
from pathlib import Path
from jennie.events.constants import *
from jennie.events.responses import INVALID_PROTOCOL
from jennie.events.constants import KEY_STACK_ANGULAR_UI_LIB, \
    KEY_STACK_DJANGO_AUTOMATIONS, KEY_STACK_ANGULAR_AUTOMATION

KEY_APP_TITLE = "app_title"
KEY_APP_DESCRIPTION = "app_description"

AUTOMATION_BASIC_INPUT = {
    "app_title": "Title for automations module", "app_description": "Description for automations module",
    "tag": "Tag (optional) for automations module",
}

home = os.path.expanduser("~")
if home[-1] != "/":
    home += "/"

TOKEN_PATH = home + ".jennie.conf.json"

def read_json_file(filepath):
    return json.loads(open(filepath, "r").read())

def write_json_file(filepath, content):
    with open(filepath, 'w') as f:
        json.dump(content, f, indent=4)
    return True

def list_all_files_from_folder(folder_path):
    # list to store files
    res = []

    # Iterate directory
    for path in os.listdir(folder_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(folder_path, path)):
            res.append(path)
    return res

def get_user_access_token():
    if not os.path.isfile(TOKEN_PATH):
        return None
    return json.loads(open(TOKEN_PATH, "r").read())

def ask_to_select(inputs):
    input_arr = []
    for key in inputs:
        input_arr.append(key)

    idx = 1
    print ("Select Subcommand ...")
    for key in input_arr:
        print (str(idx) + ". " + key)
        idx += 1

    try:
        selected = int(input(">> "))
        return inputs[input_arr[selected-1]], input_arr[selected-1]
    except Exception as e:
        print ("Invalid Option try selecting again")
        return ask_to_select(inputs)

def take_user_input(userinputs, default_values=None):
    """
    The method take dict inputs for list of inputs to be taken,
    takes all input from user and returns back input taken
    :param default_values: Provide default values for key.
    If default values are provided user is asked for update.
    {
        "key": "value"
    }
    :param inputs: Format for dict
    {
        "key": "Description to be show for input"
    }
    :return:
    {
        "key": "[INPUT_FROM_USER]"
    }
    """
    response = { }
    for key in userinputs:
        if default_values and key in default_values:
            confirm = input("Do you want to update information for {} (Y/N) ".format(key))
            if confirm.lower() == "y" or confirm.lower() == "yes":
                response[key] = input(userinputs[key] + "\n>> ")
            else:
                response[key] = default_values[key]
        else:
            response[key] = input(userinputs[key] + "\n>> ")
    return response

def raise_error(msg, print_only=False):
    if print_only:
        print (msg)
        return False
    else:
        raise Exception(msg)

def is_file(filepath):
    return os.path.isfile(filepath)

def is_folder(filepath):
    return os.path.isdir(filepath)

def create_readme(app_name, app_type, title, description):
    if app_type == KEY_STACK_ANGULAR_UI_LIB:
        command = "jennie angular ui-lib download " + app_name
    elif app_type == KEY_STACK_DJANGO_AUTOMATIONS:
        command = "jennie django automations download " + app_name
    elif app_type == KEY_STACK_ANGULAR_AUTOMATION:
        command = "jennie angular automations download " + app_name
    else:
        return raise_error(INVALID_PROTOCOL)

    content = '''# {0}

{1}

## Download Command.

```{2}```

**make sure to run the command inside project**

## How to use
'''.format(
        title, description, command
    )

    open("readme.md", "w").write(content)
    return True

def create_readme_without_config(app_name, app_type):
    """
    ask user for ( app_title, app_description)
    create readme content
    write readme file
    :param app_name: App name required for command
    :param app_type:  App type required for command
    :return: Application title
    """

    jsonInfo = take_user_input({
        KEY_APP_TITLE: "Enter Title for Library",
        KEY_APP_DESCRIPTION: "Enter Description for Library",
    })

    jsonInfo["type"] = app_type
    jsonInfo["app_name"] = app_name

    create_readme(
        app_name, app_type, jsonInfo[KEY_APP_TITLE],
        jsonInfo[KEY_APP_DESCRIPTION]
    )
    return jsonInfo[KEY_APP_TITLE]

def create_readme_with_config(filepath):
    """
    read ( app_title, app_description) from filepath
    create readme content
    write readme file
    :param filepath: Jennie Conf File
    :return: Application title
    """
    if not os.path.isfile(filepath):
        raise_error("Error:File path not present\nMake sure the command is executed in a proper application directory.")

    jsonInfo = read_json_file("jennie.conf.json")

    create_readme(
        jsonInfo["app_name"], jsonInfo["type"], jsonInfo[KEY_APP_TITLE],
        jsonInfo[KEY_APP_DESCRIPTION]
    )

    return jsonInfo[KEY_APP_TITLE]

def get_app_name(type, app_name=None, api_call_handler=None):
    """
    Get app name and check if app name exits on SERVER or not
    :param type: Type of automations
    :param app_name: Application name, if none, ask for application name
    :return: app_exits, app_name
    """
    while(app_name == None):
        app_name = input("Enter App name (Make sure app name is unique under {} category): \n>> ".format(type))
        if len(app_name) < 3:
            app_name = None
    try:
        does_app_exits = api_call_handler.validate_automation_api_call(type, app_name)
    except Exception as e:
        print ("Exceptions occured:", e)
        raise ValueError("Unhandled API Exception, unable to validate {} automations with name {} on server ".format(type, app_name))
    return does_app_exits, app_name

def get_basic_conf(app_name, type, stack, api_call_obj, default_inputs=None, is_create=False):
    """
    Build Basic Automation / UI configration for application
    :param app_name: Application name
    :param type: Application Type
    :param stack: Application Stack
    :param default_inputs: default-inputs
    :return: general configuration
    """
    configuration = {
        "app_name": app_name,
        "stack": stack,
        "type": type
    }

    user_input = take_user_input(AUTOMATION_BASIC_INPUT, default_inputs)
    for key in user_input:
        configuration[key] = user_input[key]

    if type == KEY_STACK_ANGULAR_UI_LIB:
        configuration["dependencies"] = ["bootstrap-5"]
    else:
        configuration["dependencies"] = []

    if default_inputs != None and "automation_conf" in default_inputs:
        configuration["automation_conf"] = default_inputs["automation_conf"]
    else:
        configuration["automation_conf"] = []

    # if image is found upload image
    configuration["app_image"] = ""
    configuration["readme"] = ""
    if not is_create:
        files = list_all_files_from_folder(os.getcwd())

        for file in files:
            if file.split(".")[-1] == "png" or file.split(".")[-1] == "jpg" and configuration["app_image"] == "":
                configuration["app_image"] = api_call_obj.upload_image(file)

            elif file.split(".")[-1] == "md" and configuration["readme"] == "":
                configuration["readme"] = api_call_obj.upload_text_file(
                    text_file_path=file, app_name=configuration["app_name"],
                    type=configuration["type"]
            )

    return configuration

def separate_via_comma(input_str):
    if input_str.replace(" ", "") == "":
        return []
    return input_str.replace(", ", ",").replace(" ,", ",").split(",")

def download_text_file(url):
    """
    Make a get api call, if params are present add params to url,
    if headers are present add headers to requests
    :param url: Request URL
    :param headers: Request Headers ( optional )
    :param params: Request Params ( optional )
    :return: API Call JSON Response.
    """
    response = requests.get(url)
    return response.text

def get_shorted_path(folder_path, module_name):
    paths = sorted(Path(folder_path).iterdir(), key=os.path.getmtime)
    shorted = []
    for path in paths:
        if path.is_dir():
            path = str(path.name)
            if path != module_name and path != "ui-lib":
                shorted.append(path)
    return shorted

def upload_text_file(text_file_path, app_name, type, user_key):
    """
    Upload text file to ASK SERVER
    :param text_file_path: Local path for text file.
    :param app_name: Application name
    :param type: Type of application
    :return: Uploaded File path
    """
    json_content = {
        "file_content": open(text_file_path, 'r').read(),
        "app_name": app_name,
        "filename": text_file_path.split("/")[-1],
        "type": type
    }
    text_res = requests.post(TEXT_UPLOAD_API, headers={"token": user_key},
                             json=json_content)
    return text_res.json()["payload"]["file_link"]

def list_all_files_from_folder(folder_path):
    # list to store files
    res = []

    # Iterate directory
    for path in os.listdir(folder_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(folder_path, path)):
            res.append(path)
    return res