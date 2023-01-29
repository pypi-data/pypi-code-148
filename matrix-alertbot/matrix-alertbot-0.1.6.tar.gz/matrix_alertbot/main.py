#!/usr/bin/env python3
import asyncio
import json
import logging
import os
import sys
from asyncio import TimeoutError

from aiohttp import ClientConnectionError, ServerDisconnectedError
from diskcache import Cache
from nio import (
    AsyncClient,
    AsyncClientConfig,
    InviteMemberEvent,
    KeyVerificationCancel,
    KeyVerificationKey,
    KeyVerificationMac,
    KeyVerificationStart,
    LocalProtocolError,
    LoginError,
    MegolmEvent,
    RedactionEvent,
    RoomMessageText,
    UnknownEvent,
)

from matrix_alertbot.alertmanager import AlertmanagerClient
from matrix_alertbot.callback import Callbacks
from matrix_alertbot.config import Config
from matrix_alertbot.webhook import Webhook

logger = logging.getLogger(__name__)


def create_matrix_client(config: Config) -> AsyncClient:
    # Configuration options for the AsyncClient
    try:
        matrix_client_config = AsyncClientConfig(
            max_limit_exceeded=5,
            max_timeouts=3,
            store_sync_tokens=True,
            encryption_enabled=True,
        )
    except ImportWarning as e:
        logger.warning(e)
        matrix_client_config = AsyncClientConfig(
            max_limit_exceeded=5,
            max_timeouts=3,
            store_sync_tokens=True,
            encryption_enabled=False,
        )

    # Load credentials from a previous session
    if os.path.exists(config.user_token_file):
        with open(config.user_token_file, "r") as ifd:
            credentials = json.load(ifd)
            config.user_token = credentials["access_token"]
            config.device_id = credentials["device_id"]

    # Initialize the matrix client based on stored credentials
    matrix_client = AsyncClient(
        config.homeserver_url,
        config.user_id,
        device_id=config.device_id,
        store_path=config.store_dir,
        config=matrix_client_config,
    )

    return matrix_client


async def start_matrix_client(
    matrix_client: AsyncClient, cache: Cache, config: Config
) -> bool:
    # Keep trying to reconnect on failure (with some time in-between)
    while True:
        try:
            if config.device_id and config.user_token:
                matrix_client.restore_login(
                    user_id=config.user_id,
                    device_id=config.device_id,
                    access_token=config.user_token,
                )

                # Sync encryption keys with the server
                if matrix_client.should_upload_keys:
                    await matrix_client.keys_upload()
            else:
                # Try to login with the configured username/password
                try:
                    login_response = await matrix_client.login(
                        password=config.user_password,
                        device_name=config.device_name,
                    )

                    # Check if login failed
                    if type(login_response) == LoginError:
                        logger.error("Failed to login: %s", login_response.message)
                        return False
                except LocalProtocolError as e:
                    # There's an edge case here where the user hasn't installed the correct C
                    # dependencies. In that case, a LocalProtocolError is raised on login.
                    logger.fatal(
                        "Failed to login. Have you installed the correct dependencies? "
                        "https://github.com/poljar/matrix-nio#installation "
                        "Error: %s",
                        e,
                    )
                    return False

                # Save user's access token and device ID
                # See https://stackoverflow.com/a/45368120
                user_token_fd = os.open(
                    config.user_token_file,
                    flags=os.O_CREAT | os.O_WRONLY | os.O_TRUNC,
                    mode=0o640,
                )
                with os.fdopen(user_token_fd, "w") as ofd:
                    json.dump(
                        {
                            "device_id": login_response.device_id,
                            "access_token": login_response.access_token,
                        },
                        ofd,
                    )

                # Login succeeded!

            logger.info(f"Logged in as {config.user_id}")
            await matrix_client.sync_forever(timeout=30000, full_state=True)
        except (ClientConnectionError, ServerDisconnectedError, TimeoutError):
            logger.warning("Unable to connect to homeserver, retrying in 15s...")

            # Sleep so we don't bombard the server with login requests
            await asyncio.sleep(15)
        finally:
            await matrix_client.close()


def main() -> None:
    """The first function that is run when starting the bot"""

    # Read user-configured options from a config file.
    # A different config file path can be specified as the first command line argument
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = "config.yaml"

    # Read the parsed config file and create a Config object
    config = Config(config_path)

    matrix_client = create_matrix_client(config)

    # Configure the cache
    cache = Cache(config.cache_dir)

    # Configure Alertmanager client
    alertmanager_client = AlertmanagerClient(config.alertmanager_url, cache)

    # Set up event callbacks
    callbacks = Callbacks(matrix_client, alertmanager_client, cache, config)
    matrix_client.add_event_callback(callbacks.message, (RoomMessageText,))
    matrix_client.add_event_callback(
        callbacks.invite_event_filtered_callback, (InviteMemberEvent,)
    )
    matrix_client.add_event_callback(callbacks.decryption_failure, (MegolmEvent,))
    matrix_client.add_event_callback(callbacks.unknown, (UnknownEvent,))
    matrix_client.add_event_callback(callbacks.redaction, (RedactionEvent,))
    matrix_client.add_to_device_callback(
        callbacks.key_verification_start, (KeyVerificationStart,)
    )
    matrix_client.add_to_device_callback(
        callbacks.key_verification_cancel, (KeyVerificationCancel,)
    )
    matrix_client.add_to_device_callback(
        callbacks.key_verification_confirm, (KeyVerificationKey,)
    )
    matrix_client.add_to_device_callback(
        callbacks.key_verification_end, (KeyVerificationMac,)
    )
    # Configure webhook server
    webhook_server = Webhook(matrix_client, alertmanager_client, cache, config)

    loop = asyncio.get_event_loop()
    loop.create_task(webhook_server.start())
    loop.create_task(start_matrix_client(matrix_client, cache, config))

    try:
        loop.run_forever()
    except Exception as e:
        logger.error(e)
    finally:
        loop.run_until_complete(webhook_server.close())
        loop.run_until_complete(alertmanager_client.close())
        loop.run_until_complete(matrix_client.close())
        cache.close()
