#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from robin_sd_download.apt_interaction import ensure_hook
from robin_sd_download.apt_interaction import ensure_local_repo
from robin_sd_download.api_interaction import get_software
from robin_sd_download import _version
from robin_sd_download.slack_interaction import slack_handler
from robin_sd_download.supportive_scripts import yaml_parser
from robin_sd_download.supportive_scripts import logger

def arg_parser():
    parser = argparse.ArgumentParser(
        description='Robin Radar Systems Software Puller',
        usage='robin-sd-download [options]',
        prog='Robin Radar Systems Software Puller',
        epilog='To report any bugs or issues, please visit: \
        https://support.robinradar.systems or run: robin-sd-download --slack'
    )

    parser.add_argument('-c', '--check', action='store_true', help='ensure all prerequisites are met')
    parser.add_argument('-p', '--pull', action='store_true', help='pull software from the server')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {version}'.format(version=_version.__version__))
    parser.add_argument('-s', '--slack', action='store_true', help='Send the logs to IT/DevOps Slack channel')
    
    args = parser.parse_args()

    config = yaml_parser.parse_config()
    logger.log(message="Starting Robin Radar Systems Software Puller", log_level="info", to_file=True, to_terminal=True)
    logger.log(message="Version: " + _version.__version__, log_level="info", to_file=True, to_terminal=True)
    logger.log(message="Username: " + config['robin_email'], log_level="info", to_file=True, to_terminal=True)

    if args.check:
        ensure_hook.ensure_hook()
        ensure_local_repo.ensure_local_repo()
        logger.log(message="All prerequisites met.", log_level="info", to_file=True, to_terminal=True)
        exit(0)

    elif args.pull:
        ensure_hook.ensure_hook()
        ensure_local_repo.ensure_local_repo()
        get_software.get_software()
        logger.log(message="Software pulled successfully.", log_level="info", to_file=True, to_terminal=True)
        exit(0)

    elif args.slack:
        slack_handler.send_slack_entrypoint()
        logger.log(message="Slack message sent successfully.", log_level="info", to_file=True, to_terminal=True)
        exit(0)

    else:
        parser.print_help()
        exit(1)
