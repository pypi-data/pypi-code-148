import yaml
import os
import subprocess


def create_config(config_file):
    if os.path.isfile(config_file):
        print("Config file already exists at " + config_file)
        return 0
    else:
        print("Creating config file at " + config_file)
        config = {
            "robin_email": "your email address",
            "robin_password": "your password",
            "api_url": "api url",
            "radar_id": "id of the radar you want to download the software for"
        }
        # create the directory if it doesn't exist
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        # write the config file
        with open(config_file, "w") as stream:
            yaml.dump(config, stream)
        print("Config file created at " + config_file + ". Please edit it with your details.")
        return 0
