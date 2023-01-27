#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from .arg_parse import arg_parse

home_dir = os.path.expanduser("~")
config_file = home_dir + "/.config/robin/software_deployment.yaml"


log_filename = 'upload.log'
log_level = logging.INFO
log_format = '%(asctime)s %(levelname)s %(message)s'

logging.basicConfig(filename=log_filename, level=log_level, format=log_format)
logger = logging.getLogger()

def main():
    arg_parse(config_file)

if __name__ == "__main__":
    main()