import json
import os

import yaml

from kortical.helpers.exceptions import KorticalKnownException


def is_interactive():

    if os.isatty(0) or ("PYCHARM_HOSTED" in os.environ and 'KORTICAL_TEST' not in os.environ):
        return 'true'
    # this condition is nearly always false, except for CI builds
    elif "CI_INTERACTIVE_TESTS" in os.environ:
        return 'non_interactive_ci'
    else:
        return 'false'


def load_from_path(file_path):
    file_path = os.path.abspath(file_path)

    # Validate filepath
    if not os.path.exists(file_path):
        raise KorticalKnownException(f"Path [{file_path}] was not found.")
    # Read file
    with open(file_path) as f:
        text = f.read()
    return text


def check_project_selected():
    from kortical.api.project import Project
    project = Project.get_selected_project()
    if project is None:
        raise KorticalKnownException("Please select a project first.")

    return project


def check_project_and_environment_selected():
    from kortical.api.environment import Environment

    project = check_project_selected()
    environment = Environment.get_selected_environment(project)
    if environment is None:
        raise KorticalKnownException("Please select a project and environment first.")

    return project, environment


def format_config(config, format):
    if format == 'json':
        return json.loads(config)
    elif format == 'yaml' or format == 'yml':
        return yaml.safe_load(config)
    else:
        return config
