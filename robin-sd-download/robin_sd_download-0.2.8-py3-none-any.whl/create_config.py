import yaml
import os
import subprocess

editor = os.environ.get('EDITOR', 'nano')

def create_config(config_file):
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
    print("Config file created at " + config_file)
    # open the config file in the default editor
    subprocess.run([editor, config_file])
    # os.system("xdg-open " + config_file)
    return 0