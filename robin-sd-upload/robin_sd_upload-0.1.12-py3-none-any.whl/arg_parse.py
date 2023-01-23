import os
import argparse
from .validate_radar_type import validate_radar_type
from .validate_version_name import validate_version_name
from .create_zip import create_zip
from .push_software import push_software
from .remove_zip import remove_zip
from .parse_config import parse_config
from .create_config import create_config
from .check_upload_file import check_upload_file

def arg_parse(config_file):
    parser = argparse.ArgumentParser(
        description = 'Robin Radar Systems Software Uploader',
        usage       = 'python3 robin_sd_upload [options]', 
        prog        = 'Robin Radar Systems Software Uploader',
        epilog      = 'To report any bugs or issues, please visit: https://support.robinradar.systems'
    )

    parser.add_argument('--check', action='store_true', help='ensure all prerequisites are met')
    parser.add_argument('--config', action='store_true', help='create/view a config file')
    parser.add_argument('--upload', action='store_true', help='upload software to the server: python3 robin_sd_upload --upload --type=radar_type --version=version_name')

    parser = argparse.ArgumentParser(description='argument parses for upload script.')
    parser.add_argument("--type", type=str, help="radar type")
    parser.add_argument("--version", type=str, help="version name")
    parser.add_argument("--filepath", type=str, help="file path")

    args = parser.parse_args()
    radarType = args.type
    version_name = args.version
    filepath = args.filepath

    if args.check:
        parse_config(config_file)
        check_upload_file(filepath)
        exit(0)
    if args.config:
        create_config(config_file)
        exit(0)
    elif args.upload:
        parse_config(config_file)
        check_upload_file(filepath)

        print("given type: ", radarType)
        print("given version_name: ", version_name)
        print("given filepath: ", filepath)

        version_dir_to_upload= os.path.join(filepath, version_name)
        zipped_file_path = os.path.join(filepath, version_name + '.zip')

        print('version_dir_to_upload: ', version_dir_to_upload)
        print('zipped_file_path: ', zipped_file_path)

        validate_radar_type(radarType)
        validate_version_name(version_name)
        create_zip(zipped_file_path, version_name)
        print(push_software(zipped_file_path, radarType, version_name))
        # logging or sending log to server
        remove_zip(zipped_file_path)
    else:
        parser.print_help()
        exit(1)





