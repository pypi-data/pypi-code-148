"""
event_name : update-angular-modules
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
import os
from jennie.events.constants import *

class UpdateAngularModuleFile():
    def __init__(self, filepath):
        self.filepath = filepath
        self.content = open(filepath).read()

    def add_imports(self, imports):
        for modulename in imports:
            if imports[modulename] not in self.content:
                self.content = self.content.replace("BrowserModule,", "BrowserModule," + "\n" + "    " + modulename + ",")
                self.content = self.content.replace("import { BrowserModule } from '@angular/platform-browser';", "import { BrowserModule } from '@angular/platform-browser';" + "\n" + imports[modulename])
        self.content = self.content.replace(",],", "],")
        open(self.filepath, "w").write(self.content)
        return True

    def add_providers(self, providers):
        for providername in providers:
            if providers[providername] not in self.content:
                self.content = self.content.replace("providers: [", "providers: [" + "\n" + "    " + providername + ",")
                self.content = self.content.replace("import { BrowserModule } from '@angular/platform-browser';", "import { BrowserModule } from '@angular/platform-browser';" + "\n" + providers[providername])
        self.content = self.content.replace(",],", "],")
        open(self.filepath, "w").write(self.content)
        return True


class event_update_angular_modules():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_UPDATE_ANGULAR_MODULES,
            KEY_IMPORTS: {
                "module_name": "import_path"
            },
            KEY_PROVIDERS: {
                "provider_name": "import_path"
            }
        } # replace with sample configuration.

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        module = UpdateAngularModuleFile("src/app/app.module.ts")
        if KEY_IMPORTS in event_info:
            module.add_imports(imports=event_info[KEY_IMPORTS])

        if KEY_PROVIDERS in event_info:
            module.add_providers(providers=event_info[KEY_PROVIDERS])
        return True


    def take_input(self, module_name="import"):
        name = input("Input name of {}".format(module_name))
        import_path = input("Input import path for {}".format(name))
        return name, import_path

    def take_user_input(self, event_info):
        continueAdding = True
        while(continueAdding):
            print ("\n\nInput ( 1 ) to add a import")
            print ("Input ( 2 ) to add a provider")
            print ("press any other key to finish adding.")
            input_choice = input (">> ")
            if (input_choice.replace(" ", "") == "1"):
                module, import_path = self.take_input()
                if KEY_IMPORTS not in event_info:
                    event_info[KEY_IMPORTS] = {}
                event_info[KEY_IMPORTS][module] = import_path
            elif (input_choice.replace(" ", "") == "2"):
                module, import_path = self.take_input("provider")
                if KEY_PROVIDERS not in event_info:
                    event_info[KEY_PROVIDERS] = {}
                event_info[KEY_PROVIDERS][module] = import_path
            else:
                continueAdding = False
        return event_info

    def build_event(self):
        """
        :return: event_info
        """
        print ("Update.md Angular module event can update imports and "
               "providers in angular.module.ts file inside an angular project.")
        event_info = {
            KEY_EVENT_TYPE: EVENT_UPDATE_ANGULAR_MODULES
        }
        event_info = self.take_user_input(event_info)
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        if not KEY_IMPORTS in event_info and not KEY_PROVIDERS in event_info:
            print(ERR_IMPORTS_OR_PROVIDER_MISSING)
            return False
        return event_info
