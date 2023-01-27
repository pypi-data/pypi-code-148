"""
Guardian API websocket utilities.
"""
import os
import json
from dataclasses import dataclass, asdict
import socket
import datetime
import asyncio
import requests
import websockets
from dotenv import load_dotenv
from typing import Union


from .config import settings
from .igeb_utils import unpack_from_queue
from .mock_utils import mock_cloud_package
from .debug_logs import (
    log_first_message,
    log_final_message,
    logging_connection,
    logging_break,
    logging_empty,
    logging_ping_error,
    logging_not_empty,
    log_interrupt_error,
    logging_connection_closed,
    logging_reconnection,
    logging_cloud_termination,
    logging_gaieerror,
    logging_cancelled_error,
    logging_connection_refused,
    logging_api_completed,
    logging_connecting_to_cloud,
)

load_dotenv()


class GuardianAPI:
    """Main Guardian API client."""

    def __init__(self, debug: bool = True) -> None:
        """Initialize Guardian API client.

        Args:
            debug (bool, optional): Enable debug logging. Defaults to True.
        """
        self.debug: bool = debug
        self.ping_timeout: int = 10
        self.retry_time: int = 5
        self.first_message_check = True
        self.final_message_check = False
        self.sample_rate = 250
        self.sentinal = object()
        self.encrypted_data_queue: asyncio.Queue = asyncio.Queue(maxsize=864000)
        self.decrypted_data_queue: asyncio.Queue = asyncio.Queue(maxsize=864000)

    async def connect_ws_api(
        self,
        data_queue: asyncio.Queue,
        device_id: str = "deviceMockID",
        recording_id: str = "dummy_recID",
    ) -> None:
        """Connect to the Guardian API websocket.

        Args:
            data_queue (asyncio.Queue): Data queue from the BLE client
            deviceID (str, optional): Device ID. Defaults to "deviceMockID".
            recordingID (str, optional): Recording ID. Defaults to "dummy_recID".

        Raises:
            Exception: If the websocket connection fails
        """

        async def unpack_and_load_data():
            """Get data from the queue and pack it into a dataclass"""
            package = await data_queue.get()
            (
                device_timestamp,
                device_id,
                data,
                stop,
                impedance,
            ) = unpack_from_queue(package)
            if data is not None:
                data_model.payload = data
            if device_timestamp is not None:
                data_model.deviceTimestamp = device_timestamp
            if device_id is not None:
                data_model.deviceID = device_id
            if stop is not None:
                data_model.stop = stop
            if impedance is not None:
                data_model.impedance = impedance

        async def create_timestamp(debug):
            """Create a timestamp for the data"""
            if data_queue.empty():
                logging_empty(debug)  # Fetch the current time from the device
                device_timestamp = datetime.datetime.now().astimezone().isoformat()
            else:
                logging_not_empty(debug)
                package = (
                    await data_queue.get()
                )  # Fetch the timestamp from the BLE package
                (device_timestamp, _, _, _, _) = unpack_from_queue(package)
            return device_timestamp

        async def unpack_and_load_data_termination():
            """Get data from the queue and pack it into a dataclass"""
            logging_cloud_termination(self.debug)
            data_model.payload = "STOP_CANCELLED"
            data_model.stop = True
            device_timestamp = await create_timestamp(self.debug)
            if device_timestamp is not None:
                data_model.deviceTimestamp = device_timestamp

        async def send_messages(websocket, data_model):
            while True:
                await unpack_and_load_data()
                await websocket.send(json.dumps(asdict(data_model)))
                await self.encrypted_data_queue.put([data_model.payload])
                if data_model.stop:
                    break

        async def receive_messages(websocket):
            while True:
                package_receipt = await websocket.recv()
                mocked_package = mock_cloud_package()
                if "bp_filter_eeg" in mocked_package:
                    await self.decrypted_data_queue.put(
                        [mocked_package["bp_filter_eeg"]]
                    )

                if self.first_message_check:
                    self.first_message_check = False
                    log_first_message(
                        data_model,
                        package_receipt,
                        self.debug,
                    )
                if data_model.stop:
                    log_final_message(
                        data_model,
                        package_receipt,
                        self.debug,
                    )
                    self.final_message_check = True
                    break

        # initiate flags
        self.first_message_check = True
        self.final_message_check = False
        # initiate data model
        data_model = GuardianDataModel(None, device_id, recording_id, None, None, False)

        while True:
            logging_connecting_to_cloud(self.debug)
            try:

                async with websockets.connect(settings.WS_IDENTIFIER) as websocket:  # type: ignore
                    try:
                        self.first_message_check = True
                        logging_connection(settings.WS_IDENTIFIER, self.debug)
                        send_task = asyncio.create_task(
                            send_messages(websocket, data_model)
                        )
                        receive_task = asyncio.create_task(receive_messages(websocket))
                        await asyncio.gather(send_task, receive_task)

                    except (
                        asyncio.TimeoutError,
                        websockets.exceptions.ConnectionClosed,  # type: ignore
                    ) as error:
                        log_interrupt_error(error, self.debug)
                        try:
                            logging_connection_closed(self.debug)
                            pong = await websocket.ping()
                            await asyncio.wait_for(pong, timeout=self.ping_timeout)
                            logging_reconnection(self.debug)
                            continue
                        except Exception as error:
                            logging_ping_error(error, self.retry_time, self.debug)
                            await asyncio.sleep(self.ping_timeout)

                    except asyncio.CancelledError as error:
                        async with websockets.connect(  # type: ignore
                            settings.WS_IDENTIFIER
                        ) as websocket:
                            logging_cancelled_error(error, self.debug)
                            await unpack_and_load_data_termination()

                            await websocket.send(json.dumps(asdict(data_model)))
                            package_receipt = await websocket.recv()

                            log_final_message(
                                data_model,
                                package_receipt,
                                self.debug,
                            )
                            self.final_message_check = True
                            break

            except socket.gaierror as error:
                logging_gaieerror(error, self.retry_time, self.debug)
                await asyncio.sleep(self.retry_time)
                continue

            except ConnectionRefusedError as error:
                logging_connection_refused(error, self.retry_time, self.debug)
                await asyncio.sleep(self.retry_time)
                continue

            if self.final_message_check:
                logging_break(self.debug)
                break

        logging_api_completed(self.debug)

    def get_recordings_info_all(
        self, device_id: str = "mock-device-0", first_to_last=False
    ) -> list:
        recordings_url = f"{settings.REST_API_LOGIN}recordings"
        print(recordings_url)
        with requests.Session() as session:
            r = session.get(recordings_url, auth=(device_id, ""))
            if r.status_code == 200:
                print("Recording list retrieved successfully")
                recordings = r.json()
                recordings.sort(
                    key=lambda x: datetime.datetime.strptime(
                        x["startDeviceTimestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    reverse=first_to_last,
                )
                print(json.dumps(recordings, indent=4, sort_keys=True))
                return r.json()
            else:
                print("Loading recording list failed")
                return []

    def get_recording_info_by_id(
        self, device_id: str, recording_id: str = "recordingId-0"
    ) -> list:
        recordings_url = f"{settings.REST_API_LOGIN}recordings/{recording_id}"

        with requests.Session() as session:
            r = session.get(recordings_url, auth=(device_id, ""))
            if r.status_code == 200:
                print("Recording ID file found")
                print(json.dumps(r.json(), indent=4, sort_keys=True))
                return r.json()
            else:
                print("Recording not found")
                print(r.status_code)
                print(r.json())
                return []

    def download_recording_by_id(
        self, device_id: str, recording_id: str = "recordingId-0"
    ) -> None:

        recordings_folder_name = "recordings"
        recording_subfolder_name = recording_id
        # combine the folder name and subfolder name
        folder_path = os.path.join(recordings_folder_name, recording_subfolder_name)
        # create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # create subfolde
        recording_types = ["eeg", "imu"]

        for data_type in recording_types:
            with requests.Session() as session:

                record_url = f"{settings.REST_API_LOGIN}recordings/{recording_id}/download/{data_type}"
                r = session.get(record_url, auth=(device_id, ""))
                if r.status_code == 200:
                    print(f"Recording ID file found, downloading {data_type} data")
                    print(r.json())
                    # get url from response
                    url = r.json()["downloadUrl"]
                    r = session.get(url)
                    filename = f"{recording_id}_{data_type}.csv"
                    # combine folder name and filename
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, "wb") as f:
                        # giving a name and saving it in any required format
                        # opening the file in write mode
                        f.write(r.content)

                    print("Downloading complete for recording ID: ", recording_id)
                else:
                    print("Data download failed")
                    print(r.status_code)
                    print(r.json())


@dataclass
class GuardianDataModel:
    """Data model for Guardian data"""

    deviceTimestamp: Union[str, None]
    deviceID: Union[str, None]
    recordingID: Union[str, None]
    payload: Union[str, None]  # This is a base64 encoded bytearray as a string
    impedance: Union[int, None]
    stop: Union[bool, None]
