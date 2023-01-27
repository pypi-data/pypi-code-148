import os
import yaml
import validators

def parse_config(config_file):

    contents = {
        "robin_email": "your email address",
        "robin_password": "your password",
        "api_url": "api url"
    }

    if os.path.isfile(config_file):
        print("Config file exists at " + config_file)
        with open(config_file, "r") as stream:
            try:
                config = yaml.safe_load(stream)
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
                # if type(config['filepath']) is not str:
                #     print("filepath is not a string")
                #     exit(1)
                return config
            except yaml.YAMLError as exc:
                print(exc)

    else:
        print("Config file does not exist, creating it at " + config_file)
        # create the directory if it doesn't exist
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        # write the config file
        with open(config_file, "w") as stream:
            yaml.dump(contents, stream)
        print("Config file created at " + config_file)
        exit(1)