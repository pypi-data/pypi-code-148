"""
event_name : create-angular-module-routing
description : Add Angular libraries to project
config format:

**Place Your Sample configuration here here**

"""
import os, json
from jennie.events.utils.helper import *

BASE_DIR = "src/app"

SAMPLE_ROUTES_FILES = '''import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
IMPORT_LINES 

const routes: Routes = [
  ROUTES
]


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
'''

MODULE_SAMPLE_ROUTES_FILES = '''import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MODULE_NAMEComponent } from './MODULE_NAME_SMALL/MODULE_NAME_SMALL.component';
IMPORT_LINES 

const routes: Routes = [
  {
    path: '',
    component: MODULE_NAMEComponent,
    children: [\nCHILD_ROUTES\n    ]
  }
]


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MODULE_NAMERoutingModule { }
'''

class event_create_angular_module_routing():
    def __init__(self, user_key, app_name, type):
        self.user_key = user_key
        self.app_name = app_name
        self.type = type
        
        self.sample_conf = {
            KEY_EVENT_TYPE: EVENT_CREATE_ANGULAR_MODULE_ROUTING
        } # replace with sample configuration.

    def get_components(self, module_name):
        """
        Get all components from module directory
        if directory exits, else throw error
        :param module_name: name of module.
        :return: True.
        """
        app_dir = BASE_DIR
        if module_name != "":
            app_dir = BASE_DIR + "/" + module_name

        if os.path.exists(app_dir):
            return get_shorted_path(app_dir, module_name)
        else:
            raise Exception("Error in Event : {} : Invalid path for creating routes, Event".format(
                EVENT_CREATE_ANGULAR_MODULE_ROUTING
            ))

    def create_routing(self, module_name, components):
        """
        Update routing file and creates routes.menu.ts
        for sidebar and navbar menu's
        :param module_name: name of module for whom route is to be created
        :param components: list of all components
        :return: True
        """
        child_routes = ""
        imports_lines = ""
        sidebar_menu = []
        if module_name == "":
            route_file_name = "src/app/app-routing.module.ts"
        else:
            route_file_name = "src/app/" + module_name + "/" + module_name + "-routing.module.ts"

        if module_name == "":
            space = "  "
        else:
            space = "       "
        if os.path.exists(route_file_name):
            for component in components:
                is_active = False
                if child_routes == "":
                    child_routes = space + "{ path: '' , redirectTo: '" + component + "', pathMatch: 'full' },\n"
                    is_active = True
                route = "path: '{}', component: {}Component".format(str(component), str(component).capitalize())
                import_line = "import { " + str(component).capitalize() + "Component } from " + "'./{0}/{0}.component';\n".format(str(component))
                child_routes += space + "{ ROUTE },\n".replace("ROUTE", route)
                imports_lines += import_line

                name = component.capitalize()

                sidebar_menu.append(
                    {
                        "name": name,
                        "is_active": is_active,
                        "link": '/' + component,
                        "icon_class": "fa-columns"
                    }
                )

        if module_name == "":
            current_route_file = SAMPLE_ROUTES_FILES.replace("ROUTES", child_routes)
            current_route_file = current_route_file.replace("IMPORT_LINES", imports_lines)
            open(route_file_name, "w").write(current_route_file)
        else:
            current_route_file = MODULE_SAMPLE_ROUTES_FILES.replace("CHILD_ROUTES", child_routes)
            current_route_file = current_route_file.replace("IMPORT_LINES", imports_lines)
            current_route_file = current_route_file.replace("MODULE_NAME_SMALL", module_name)
            current_route_file = current_route_file.replace("MODULE_NAME", str(module_name).capitalize())
            open(route_file_name, "w").write(current_route_file)

        content = '''export var route_menu = {}
        '''.format(json.dumps(sidebar_menu, indent=2))
        if module_name:
            directory_file = BASE_DIR + "/" + module_name + "/route.menu.ts"
        else:
            directory_file = BASE_DIR + "/route.menu.ts"

        open(directory_file, "w").write(content)
        return True

    def execute(self, event_info):
        """
        :param event: event information
        :return: True / False
        """
        module_name = event_info[KEY_MODULE_NAME]
        components = self.get_components(module_name)
        self.create_routing(module_name, components)
        return True

    def build_event(self):
        """
        :return: event_info
        """
        event_info = {
            KEY_EVENT_TYPE: EVENT_CREATE_ANGULAR_MODULE_ROUTING
        }
        event_info[KEY_MODULE_NAME] = input("Input module name for whom the routing is to be created,\nleave black for default app >> ")
        return event_info

    def validate(self, event_info):
        """
        Validate Configuration.
        :param event: event info
        :return: event_info / False
        """
        if KEY_MODULE_NAME not in event_info:
            print("Missing Module name for event")
            return False

        return event_info
