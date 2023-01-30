#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from robin_sd_download.supportive_scripts import logger
from robin_sd_download.supportive_scripts import yaml_parser

def zip_files(log_dir):
    # Zip the files
    try:
        zip_file = shutil.make_archive(log_dir, 'zip', log_dir)
        return zip_file
    except Exception as e:
        logger.log(message=f"Error zipping files: {e}", to_file=True, to_terminal=True, log_level='error')

def send_slack(file_to_send, customer_name: str = None):

    config = yaml_parser.parse_config()

    # Set variables from config
    slack_token = config['slack']['token']
    # slack_channel = config['slack']['channel']

    slack_channel = []
    slack_channel.append(config['slack']['channel'])
    
    client = WebClient(token=slack_token)

    try:
        response = client.files_upload(
            channels=slack_channel,
            file=file_to_send,
            filename=os.path.basename(file_to_send),
            title=f"SD API Downloader log files for {customer_name}",
            initial_comment=f"SD API Downloader log files for {customer_name}"
        )

        logger.log(message=f"Slack response: {response}", to_file=True, to_terminal=True, log_level='info')
        
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'
        logger.log(message=f"Slack error: {e.response['error']}", to_file=True, to_terminal=True, log_level='error')

def send_slack_entrypoint():
    config = yaml_parser.parse_config()

    customer_name = config['customer']['name']

    log_dir = config['log']['file']
    log_dir = os.path.dirname(log_dir)

    # Zip the files
    zip_file = zip_files(log_dir)

    # Send the files to Slack
    send_slack(zip_file, customer_name=customer_name)

    # Delete the zip file
    os.remove(zip_file)
