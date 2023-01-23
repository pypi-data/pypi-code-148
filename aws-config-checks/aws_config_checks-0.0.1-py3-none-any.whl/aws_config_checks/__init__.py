import yaml
from yaml.loader import SafeLoader
import os

__version__ = "0.0.1"
__author__ = 'Dheeraj Banodha'


# returns the list of all the aws config checks
def list_config_checks(**kwargs) -> dict:
    """
    :param kwargs:
    :return:
    """

    def get_config_checks(module_name) -> dict:
        try:
            with open('aws-config-conformance-packs/'+module_name+'.yaml') as f:
                data = yaml.load(f, Loader=SafeLoader)

            response = {}
            for key in data['Resources'].keys():
                response.setdefault(module_name, []).append(key)

            return response
        except FileNotFoundError:
            return {}

    if 'module_name' in kwargs:
        return get_config_checks(kwargs['module_name'])

    files = os.listdir('aws-config-conformance-packs')

    configs = {}
    for filename in files:
        filename = filename.rstrip('.yaml')
        configs.update(get_config_checks(module_name=filename))

    return configs

