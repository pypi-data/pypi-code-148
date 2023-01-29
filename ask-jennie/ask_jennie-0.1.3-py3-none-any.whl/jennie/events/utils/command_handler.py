from jennie.events.utils.helper import ask_to_select
from jennie.events.constants import *

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

def transverse_inside_commands(dictObj, current_command, commands):
    for key in dictObj:
        if str(type(dictObj[key])) == "<class 'dict'>":
            current_command = current_command + " " + key
            transverse_inside_commands(dictObj[key], current_command, commands)
        else:
            if dictObj[key] != None:
                append_command = current_command + " " + key + " <" + dictObj[key] + ">"
                commands.append(append_command)
            else:
                append_command = current_command + " " + key
                commands.append(append_command)
    return commands

def show_command_list(is_user_logger_in):
    if not is_user_logger_in:
        print ("Package is accessible only after login. To login use command"
               "\n\tjennie setup\nand login with email registered with ask jennie, "
               "To register continue to automations.ask-jennie.com/signup")

    else:
        current_command = "jennie"
        commands = []
        all_commands = transverse_inside_commands(AUTOMATION_COMMANDS, current_command, commands)
        counter = 1
        print ("\n\nList of commands available\n\n")
        for command in all_commands:
            print (str(counter) + ".", command)
            counter += 1
        print ("\n\n")
    return None, None

def map_inputs(arguments):
    args = arguments
    input_selected = AUTOMATION_COMMANDS
    commands = []
    for arg in args:
        if str(type(input_selected)) == "<class 'dict'>":
            if arg not in input_selected:
                print ("Invalid Command\n")
                return show_command_list(True)
            else:
                input_selected = input_selected[arg]
                commands.append(arg)

    while (str(type(input_selected)) == "<class 'dict'>"):
        print ("\n\n")
        input_selected, selected = ask_to_select(input_selected)
        commands.append(selected)

    if input_selected == "library_name" and len(args) > 3:
        commands.append(arguments[3])

    if len(args) > 4:
        for argument in args[4:]:
            commands.append(argument)
    return commands
