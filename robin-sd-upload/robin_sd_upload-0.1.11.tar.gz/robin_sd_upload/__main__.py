#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# from parse_config import parse_config
from .configure_argparse import configure_argparse
from .validate_radar_type import validate_radar_type
from .validate_version_name import validate_version_name
from .create_zip import create_zip
from .push_software import push_software
from .remove_zip import remove_zip

if __name__ == '__main__':
    # usage: python ./upload.py --type='elvira' --version='2.2.x' TODO:--filepath='path/to/file'
    print("--- Start ---")
    # parse_config()

    args = configure_argparse().parse_args()
    radarType = args.type
    version_name = args.version
    # filepath = args.filepath

    print("given type: ", radarType)
    print("given version_name: ", version_name)
    # print("given filepath: ", filepath)

    version_dir_to_upload= os.path.dirname(os.path.realpath(__file__))+"/"+version_name
    zipped_file_path = os.path.dirname(os.path.realpath(__file__))+"/"+version_name+".zip"

    print('version_dir_to_upload: ', version_dir_to_upload)
    print('zipped_file_path: ', zipped_file_path)

    validate_radar_type(radarType)
    validate_version_name(version_name)
    create_zip(zipped_file_path, version_name)
    print(push_software(zipped_file_path, radarType, version_name))
    # logging or sending log to server
    remove_zip(zipped_file_path)
    
    print("--- End ---")