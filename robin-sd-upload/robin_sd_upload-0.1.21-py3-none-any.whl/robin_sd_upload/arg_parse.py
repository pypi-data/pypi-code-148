import os
import argparse
import yaml
from .validate import validate
from .create_zip import create_zip
from .push_software import push_software
from .remove_zip import remove_zip
from .parse_config import parse_config
from .create_config import create_config
from .check_upload_file import check_upload_file

def arg_parse(config_file):
    parser = argparse.ArgumentParser(
        description = 'Robin Radar Systems Software Uploader',
        usage       = 'robin-sd-upload [options]', 
        prog        = 'Robin Radar Systems Software Uploader',
        epilog      = 'To report any bugs or issues, please visit: https://support.robinradar.systems'
    )

    parser.add_argument('--check', action='store_true', help='ensure all prerequisites are met')
    parser.add_argument('--config', action='store_true', help='create/view a config file (/.config/robin/software_deployment.yaml)')
    parser.add_argument('--upload', action='store_true', help='upload software to the server: python3 robin_sd_upload --upload --type=radar_type --version=version_name')
    # arguments for upload
    parser.add_argument("--type", type=str, help="radar type")
    parser.add_argument("--version", type=str, help="version name")

    args = parser.parse_args()
    radarType = args.type
    version_name = args.version

    if args.check:
        parse_config(config_file)
        check_upload_file(config_file['filepath'])
        exit(0)
    if args.config:
        create_config(config_file)
        exit(0)
    elif args.upload:
        parse_config(config_file)
        check_upload_file(config_file['filepath'])

        version_dir_to_upload= os.path.join(config_file['filepath'], version_name)
        zipped_file_path = os.path.join(config_file['filepath'], version_name + '.zip')

        print('version_dir_to_upload: ', version_dir_to_upload)
        print('zipped_file_path: ', zipped_file_path)

        validate(radarType, version_name)
        create_zip(zipped_file_path, version_name)
        push_software(config_file, zipped_file_path, radarType, version_name)
        # TODO:logging or sending log to server
        remove_zip(zipped_file_path)
    else:
        parser.print_help()
        exit(1)





