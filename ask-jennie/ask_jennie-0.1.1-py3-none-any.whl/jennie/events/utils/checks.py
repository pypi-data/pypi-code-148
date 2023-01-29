import os
from os.path import isfile, join
from jennie.events.utils.helper import read_json_file

def check_angular_ui_module_directory(directory):
    """
    Check if directory contain files releated to angular ui module
    return back events for download files for UI module.
    :param directory: directory to search for
    :return: events for download files for UI module. or raise error.
    """
    if directory[-1] == "/":
        directory = directory[:-1]
    component_name = directory.split("/")[-1]
    files = [f for f in os.listdir(directory) if isfile(join(directory, f))]
    if component_name + ".component.ts" not in files:
        raise ValueError("Missing TS file for the component")
    elif component_name + ".component.css" not in files:
        raise ValueError("Missing CSS file for the component")
    elif component_name + ".component.html" not in files:
        raise ValueError("Missing CSS file for the component")

    return files

def check_if_angular_project(directory):
    """
    Check if directory is an angular project
    :param directory: directory path
    :return: Boolean
    """
    if directory[-1] != "/":
        directory += "/"
    search_files = [
        "angular.json", "karma.conf.js",
        "package.json"
    ]

    is_angular = True
    for file in search_files:
        if not os.path.isfile(directory + file):
            is_angular = False

    return is_angular

def check_if_django_project(directory):
    """
    Check if directory is an angular project
    :param directory: directory path
    :return: Boolean
    """
    if directory[-1] == "/":
        directory = directory[:-1]
    return os.path.isfile( directory + "/manage.py")

def check_if_uploaded_automation(directory):
    """
    Check if directory is an angular project
    :param directory: directory path
    :return: Boolean
    """
    if directory[-1] != "/":
        directory += "/"

    if not os.path.isfile(directory + "jennie.conf.json"):
        raise ValueError("Jennie configuration file does not exits")

    jsonConf = read_json_file(directory + "jennie.conf.json")
    if jsonConf == None:
        raise ValueError("Not a valid json.conf.json")

    if "_id" not in jsonConf:
        raise ValueError("Not a valid json.conf.json")
    return jsonConf
