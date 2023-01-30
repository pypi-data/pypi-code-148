#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import zipfile
import datetime

from robin_sd_download.api_interaction import get_bearer_token
from robin_sd_download.supportive_scripts import yaml_parser
from robin_sd_download.supportive_scripts import logger

def get_software():
    config = yaml_parser.parse_config()

    radar_id = config['radar_id']
    request_url = config['api_url']
    
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    bearer_token = get_bearer_token.get_bearer_token()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + bearer_token,
    }

    api_endpoint = '/api/radars/' + radar_id + '/software'

    response = requests.get(request_url + api_endpoint, allow_redirects=True, headers=headers)

    # Get the name of the file
    file_name = response.headers.get("Content-Disposition").split("=")[1]
    file_name = file_name.replace('"','')
    file_name = file_name.replace('.zip','')

    # Define the location to save the file
    file_location = config['static']['download_location']

    # Create the destination folder
    file_location += file_name
    os.makedirs(file_location, exist_ok=True)

    # Write the file to disk
    write_file = file_location + "/"+ current_date + ".zip"

    with open(write_file, 'wb') as f:
        f.write(response.content)
        f.close()

        logger.log(message="Downloaded to " + write_file, log_level="info", to_file=True, to_terminal=True)

    # Extract the file
    with zipfile.ZipFile(write_file, "r") as zip_ref:
        zip_ref.extractall(file_location)
        zip_ref.close()

    # Remove the zip file
    os.remove(write_file)

    return 0
