import yaml
import os

def create_config(config_file):
    config = {
        "robin_email": "your email address",
        "robin_password": "your password",
        "api_url": "api url",
        "radar_id": "id of the radar you want to download the software for"
    }
    with open(config_file, "w") as stream:
        yaml.dump(config, stream)
    print("Config file created at " + config_file)
    # open the config file in the default editor
    os.system("start " + config_file)
    # print("Please edit the config file and run this script again.")
    exit(0)
#