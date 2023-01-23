import argparse
import yaml

from .ensure_hook import ensure_hook
from .ensure_local_repo import ensure_local_repo
from .get_software import get_software
from .parse_config import parse_config
from .create_config import create_config

def arg_parse(config_file, home_dir):
    parser = argparse.ArgumentParser(
        description = 'Robin Radar Systems Software Puller',
        usage       = 'python3 -m robin_sd_download.download [options]', 
        prog        = 'Robin Radar Systems Software Puller',
        epilog      = 'To report any bugs or issues, please visit: https://support.robinradar.systems'
    )

    parser.add_argument('--check', action='store_true', help='ensure all prerequisites are met')
    parser.add_argument('--config', action='store_true', help='create/view a config file')
    parser.add_argument('--pull', action='store_true', help='pull software from the server')
    

    args = parser.parse_args()

    if args.check:
        parse_config(config_file)
        # ensure_hook()
        # ensure_local_repo()
        exit(0)
    if args.config:
        create_config(config_file)
        exit(0)
    elif args.pull:
        parse_config(config_file)
        # ensure_hook()
        # ensure_local_repo()
        with open(config_file, "r") as stream:
            try:
                config = yaml.safe_load(stream)
                get_software(config, home_dir)
                exit(0)
            except yaml.YAMLError as exc:
                print(exc)
                exit(1)
    else:
        parser.print_help()
        exit(1)
