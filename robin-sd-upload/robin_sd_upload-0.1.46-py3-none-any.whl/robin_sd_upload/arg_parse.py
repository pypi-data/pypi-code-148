import os
import tempfile
import argparse
import yaml
from .validate import validate
from .create_zip import create_zip
from .push_software import push_software
from .remove_zip import remove_zip
from .parse_config import parse_config
from .check_upload_file import check_upload_file

def arg_parse(config_file):
    parser = argparse.ArgumentParser(
        description = 'Robin Radar Systems Software Uploader',
        usage       = 'robin-sd-upload [options]', 
        prog        = 'Robin Radar Systems Software Uploader',
        epilog      = 'To report any bugs or issues, please visit: https://support.robinradar.systems'
    )

    parser.add_argument('--check', action='store_true', help='ensure all prerequisites are met')
    parser.add_argument('--upload', action='store_true', help='upload software: robin-sd-upload --upload --type=radar_type --version=version_name --source=upload_file_folder_path')
    # arguments for upload
    parser.add_argument("--type", type=str, help="radar type")
    parser.add_argument("--version", type=str, help="version name")
    parser.add_argument("--source", type=str, help="upload file absolute path")

    args = parser.parse_args()
    radarType = args.type
    version_name = args.version
    upload_file_path = args.source


    if args.check:
        parse_config(config_file)
        exit(0)
    elif args.upload:
        #check if type,version,source are given
        if radarType is None or version_name is None or upload_file_path is None:
            print('Please provide all the arguments: --type, --version, --source')
            exit(1)
        parse_config(config_file)
        validate(radarType, version_name)
        # if check_upload_file return false, exit
        if check_upload_file(upload_file_path, version_name) is False:
            exit(1)

        temp_dir = tempfile.mkdtemp()
        # version_dir_to_upload= os.path.join(upload_file_path, version_name)
        zipped_file_path = os.path.join(temp_dir, version_name + '.zip')

        # print('version_dir_to_upload: ', version_dir_to_upload)
        # print('zipped_file_path: ', zipped_file_path)

        # second param was version_name
        create_zip(zipped_file_path, upload_file_path, version_name)
        with open(config_file, "r") as stream:
            try:
                config = yaml.safe_load(stream)
                push_software(config, zipped_file_path, radarType, version_name)
                remove_zip(zipped_file_path)
                exit(0)
            except yaml.YAMLError as exc:
                print(exc)
                exit(1)
    else:
        parser.print_help()
        exit(1)





