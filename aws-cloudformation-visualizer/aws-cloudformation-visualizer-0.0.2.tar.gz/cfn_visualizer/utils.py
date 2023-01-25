from datetime import datetime
from dateutil import tz


def get_status(status: str):
    color = ''
    base_str = '\x1b[{}{:<27}\x1b[0m'

    if 'ROLLBACK' in status or 'FAILED' in status:
        color = '91m'  # Bright Red

    elif 'PROGRESS' in status or 'SKIPPED' in status:
        color = '96m'  # Bright Cyan

    elif 'COMPLETE' in status:
        color = '92m'  # Bright Green

    return base_str.format(color, status)


def get_timestamp(timestamp: datetime):
    return timestamp.astimezone(tz.tzlocal()).strftime('%I:%M:%S %p')


def print_event(event: dict):
    event_info = ' {:>11} | {} | {:<40} | {:<35} | {}'.format(
        # 10:20:58 AM | CREATE_IN_PROGRESS          | AWS::CloudFormation::Stack                     | User Initiated
        get_timestamp(event.get('Timestamp')),
        get_status(event.get('ResourceStatus')),
        event.get('ResourceType'),
        event.get('LogicalResourceId'),
        event.get('ResourceStatusReason', '')
    )
    print(event_info)
