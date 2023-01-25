import os
from pathlib import Path

from kortical.api.project import Project
from kortical.api.environment import Environment
from kortical.api.component_instance import ComponentInstance
from kortical.cloud.cloud import IS_KUBERNETES_ENVIRONMENT
from kortical.helpers import format_config
from kortical.helpers.exceptions import KorticalKnownException


def get_config(format=None):

    if IS_KUBERNETES_ENVIRONMENT:
        # Get config from platform
        project = Project.get_selected_project()
        environment = Environment.get_selected_environment(project)
        component = ComponentInstance.get_component_instance(project, environment, os.environ["KORE_COMPONENT_INSTANCE_ID"])
        config = component.get_app_config()
        return format_config(config, format)

    else:
        # Search locally for a parent folder that has either an app_config or a config/app_config
        current_directory = os.getcwd()
        while True:
            for path in [os.path.join(current_directory, 'app_config.yml'), os.path.join(current_directory, 'config', 'app_config.yml')]:
                if os.path.isfile(path):
                    with open(path, 'r') as f:
                        config = f.read()
                        return format_config(config, format)
            path = Path(current_directory)
            current_directory = str(path.parent.absolute())
            if path.root == current_directory:
                raise KorticalKnownException(f"No app config found in directory [{os.getcwd()}]")


def get_version():

    if IS_KUBERNETES_ENVIRONMENT:
        # Get version name from environment variable
        return f'v{os.environ["KORE_COMPONENT_VERSION"]}'
    else:
        # Locally, the app has no version. Versions are only created when the app is deployed.
        return None
