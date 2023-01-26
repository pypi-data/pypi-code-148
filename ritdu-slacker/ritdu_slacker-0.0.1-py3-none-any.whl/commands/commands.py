import base64
import logging, click, click_log, json
import requests, json, click, logging, os
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger()
logger.setLevel(logging.ERROR)
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def requests_retry_session(
    retries=5,
    backoff_factor=0.5,
    status_forcelist=(500, 502, 504),
    session=None,
) -> Session:
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def post_message_to_slack(
    text, thread_uuid, message_uuid, workspace, channel, thread_broadcast=False
) -> dict:
    return (
        requests_retry_session()
        .post(
            url="https://slacker.cube-services.net/api/message-template",
            headers={"Content-Type": "application/json"},
            json={
                "command": "SimpleMessage",
                "workspace": workspace,
                "channel": channel,
                "message_uuid": message_uuid,
                "message_or_thread_uuid": "",
                "thread_uuid": thread_uuid,
                "thread_broadcast": thread_broadcast,
                "message": text,
                "fallback_message": text,
            },
            timeout=(10, 10),
        )
        .json()
    )


def post_file_to_slack(
    text,
    thread_uuid,
    message_uuid,
    workspace,
    channel,
    file_name,
    file_bytes,
    thread_broadcast=False,
) -> dict:
    return (
        requests_retry_session()
        .post(
            url="https://slacker.cube-services.net/api/message-template",
            headers={
                "Accept": "application/json",
            },
            files={"file": file_bytes},
            data={
                "json": json.dumps(
                    {
                        "command": "SimpleMessage",
                        "workspace": workspace,
                        "channel": channel,
                        "message_uuid": message_uuid,
                        "message_or_thread_uuid": "",
                        "thread_uuid": thread_uuid,
                        "thread_broadcast": thread_broadcast,
                        "message": text,
                        "fallback_message": text,
                    }
                )
            },
            timeout=(10, 10),
        )
        .json()
    )


def check_result(result):
    return result.get("ok")


@click.group(help="CLI tool send/update slack messages and send files")
@click.help_option("--help", "-h")
def main():
    pass


@click.command(
    help="Command to send message, reply to thread or reply and broadcast to thread"
)
@click.option("--debug", is_flag=True, help="Switch to debug logging")
@click.option("--text", "-m", default=None, required=True, help="text to send")
@click.option(
    "--workspace", "-w", default=None, required=True, help="slack workspace name"
)
@click.option("--channel", "-c", default=None, required=True, help="slack channel name")
@click.option(
    "--message-uuid",
    "-u",
    default=None,
    required=False,
    help="uuid of message to update",
)
@click.option(
    "--thread-uuid",
    "-t",
    default=None,
    required=False,
    help="thread uuid to send message to",
)
@click.option(
    "--thread-broadcast",
    "-b",
    is_flag=True,
    help="flag to broadcast message to thread",
)
def message(
    debug, text, thread_uuid, message_uuid, workspace, channel, thread_broadcast
):
    if debug:
        logger.setLevel(logging.DEBUG)
    logger.debug(f"Send text: {text}")
    result = post_message_to_slack(
        text=f"{text}",
        thread_uuid=thread_uuid if thread_uuid else "",
        message_uuid=message_uuid if message_uuid else "",
        workspace=workspace,
        channel=channel,
        thread_broadcast=thread_broadcast,
    )
    print(json.dumps(result))


@click.command(help="Command to send file to thread")
@click.option("--debug", is_flag=True, help="Switch to debug logging")
@click.option("--text", "-m", default=None, required=False, help="text to send")
@click.option(
    "--workspace", "-w", default=None, required=True, help="slack workspace name"
)
@click.option("--channel", "-c", default=None, required=True, help="slack channel name")
@click.option(
    "--message-uuid",
    "-u",
    default=None,
    required=False,
    help="uuid of message to update",
)
@click.option(
    "--thread-uuid",
    "-t",
    default=None,
    required=False,
    help="thread uuid to send message to",
)
@click.option(
    "--thread-broadcast",
    "-b",
    is_flag=True,
    help="flag to broadcast message to thread",
)
@click.option(
    "--file",
    "-f",
    default=None,
    required=True,
    help="file to send to slack, can be path to file or url",
)
def file(
    debug, text, thread_uuid, message_uuid, workspace, channel, file, thread_broadcast
):
    if debug:
        logger.setLevel(logging.DEBUG)
    logger.debug(f"Send file: {file}")

    file_basename = os.path.basename(file)
    with open(file, "rb") as f:
        result = post_file_to_slack(
            text=f"{text}" if text else f"File: {file_basename}",
            thread_uuid=thread_uuid if thread_uuid else "",
            message_uuid=message_uuid if message_uuid else "",
            workspace=workspace,
            channel=channel,
            file_name=file_basename,
            file_bytes=f,
            thread_broadcast=thread_broadcast,
        )
    print(json.dumps(result))
