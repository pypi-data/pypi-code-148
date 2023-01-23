import os
import validators
import yaml

home_dir = os.path.expanduser("~")
config_file = home_dir + "/.config/robin/config.yaml"


def parse_config():
    if os.path.isfile(config_file):
        with open(config_file, "r") as stream:
            try:
                global config
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    else:
        print("Config file is missing at " + config_file)
        exit(1)

    # Validate types
    if type(config['robin_email']) is not str:
        print("robin_email is not a string")
        exit(1)
    
    if type(config['robin_password']) is not str:
        print("robin_password is not a string")
        exit(1)

    if not validators.url(config['api_url']):
        print("api_url is not a valid URL")
        exit(1)