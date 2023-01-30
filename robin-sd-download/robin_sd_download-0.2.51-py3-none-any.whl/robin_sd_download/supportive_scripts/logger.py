#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime

from robin_sd_download.supportive_scripts import yaml_parser

def log(message: str, to_file: bool = True, to_terminal: bool = False, log_level: str = 'info'):
    """ Logs a message to a file and/or the terminal """
    # Usage: log("This is a test message", to_file=True, to_terminal=False)

    # Fetch the logfile location from  config
    config = yaml_parser.parse_config()

    log_file = config['log']['file']
    log_level = config['log']['level']
    app_name = config['static']['app_name']
    log_dir = os.path.dirname(log_file)

    # Create the log directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # If the log file does not exist, create it.
    if not os.path.exists(log_file):
        open(log_file, 'w').close()

    # Fail if the log level is not valid, it can only be 'debug', 'info', 'warning', or 'error'
    if log_level not in ['debug', 'info', 'warning', 'error']:
        raise ValueError("log_level must be either 'debug', 'info', 'warning', or 'error'")

    if not isinstance(log_file, str) or not isinstance(message, str) or not isinstance(app_name, str):
        raise TypeError("log_file, message, and app_name must be of type string")
    if not isinstance(to_file, bool) or not isinstance(to_terminal, bool):
        raise TypeError("to_file and to_terminal must be of type boolean")

    # Create the log file if it doesn't exist
    if to_file and not os.path.exists(log_file):
        open(log_file, 'w').close()

    now = datetime.datetime.now().strftime("%H:%M:%S")
    log_line = f"{app_name} {now} - {message}"

    # Log to file
    if to_file:
        with open(log_file, 'a') as f:
            f.write(log_line + '\n')

    # Log to terminal
    if to_terminal:
        print(log_line)
