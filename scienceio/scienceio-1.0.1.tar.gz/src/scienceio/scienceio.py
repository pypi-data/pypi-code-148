import aiohttp
import asyncio
import configparser
import os
import requests
import time
import types

from enum import Enum
from pathlib import Path
from typing import Dict, Optional, Union

CONFIG = types.SimpleNamespace(
    API_URL="https://api.aws.science.io/v2",
    HELP_EMAIL="api_support@science.io",
    SETTINGS_DIR=Path.home() / ".scienceio",
    SETTINGS_FILE_PATH=Path.home() / ".scienceio" / "config",
    MAX_POLL_DURATION_SEC=300,
    POLL_SLEEP_DURATION_SEC=2,
)


class ScienceIOError(Exception):
    """Base class for all exceptions that are raised by the ScienceIO SDK."""


class HTTPError(ScienceIOError):
    """Raised when an HTTP error occurs when using the ScienceIO SDK."""

    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.status_code = status_code


class TimeoutError(ScienceIOError):
    """Raised when a call to the ScienceIO API times out."""

    def __init__(self, msg):
        self.msg = msg


class ResponseFormat(str, Enum):
    JSON = "application/json"

    def format_response(self, response):
        """
        Defines response format

        Args:
            response: string with desired format
        """
        if self is ResponseFormat.JSON:
            return response.json()
        else:
            raise NotImplementedError("Unknown response format")

    def create_headers(self, api_id: str, api_secret: str) -> dict:
        """
        Create headers for API call

        Args:
            api_id: API Key, obtained from api.science.io
            api_secret: API secret, obtained from api.science.io

        Returns:
            Dict containing content type and API credentials
        """
        return {
            "Content-Type": self.value,
            "x-api-id": api_id,
            "x-api-secret": api_secret,
        }


class ScienceIO(object):
    def __init__(
        self,
        response_format: ResponseFormat = ResponseFormat.JSON,
        timeout: Optional[Union[int, float]] = 1200,
    ):
        """Initializer for the ScienceIO client. The client will attempt to
        configure itself by trying to read from environment variables, if set.
        If unable to, the config values will be read from the ScienceIO config
        file.

        Args:
            response_format:
                Format to use for responses (default: `ResponseFormat.JSON`).
            timeout:
                Amount of time to wait before timing out network calls, in seconds.
                If `None`, timeouts will be disabled. (default: 1200)
        """

        self.response_format = response_format
        self.timeout = timeout

        # Create a persistent session across requests.
        # https://docs.python-requests.org/en/master/user/advanced/
        self.session = requests.Session()
        self.session.params = {}

        # Lazy loading of configuration (no need to try and load the settings if user specifies
        # their own API ID and secret). Also, this prevents breakage when in envs with no
        # settings file, such as test environments or hosted Jupyter notebooks.
        config = None

        def get_config_value(key: str) -> str:
            nonlocal config
            if config is None:
                config = configparser.RawConfigParser()
                config.read(CONFIG.SETTINGS_FILE_PATH)

            return config["SETTINGS"][key].strip("\"'")

        # Handles config values from user arguments, config file, and user
        # input, in that order from most to least preferred.
        write_out_conf = False

        def get_value(initial: Optional[str], key: str, human_name: str) -> str:
            nonlocal write_out_conf
            if initial is None:
                try:
                    return get_config_value(key)
                except KeyError:
                    user_input = str(
                        input(f"Please provide your ScienceIO API key {human_name}: ")
                    )

                    # User input was collected, flag the config file for rewriting.
                    write_out_conf = True
                    return user_input

            return initial

        # API endpoints to use.
        self.api_url = os.environ.get("SCIENCEIO_API_URL", CONFIG.API_URL)
        self.structure_url = f"{self.api_url}/structure"

        # API key and secret (with extra handling for env vars, config file, and user prompts).
        self.api_id = get_value(os.environ.get("SCIENCEIO_KEY_ID"), "KEY_ID", "id")
        self.api_secret = get_value(
            os.environ.get("SCIENCEIO_KEY_SECRET"), "KEY_SECRET", "secret"
        )

        # Construct the headers.
        self.headers = self.response_format.create_headers(
            api_id=self.api_id,
            api_secret=self.api_secret,
        )

        # Write out the API key ID and secret if either or both of those values
        # needed user input.
        if write_out_conf:
            # Create a new `ConfigParser` to hold the configuration we want to
            # write to the config file.
            new_conf = configparser.ConfigParser()
            new_conf["SETTINGS"] = {
                "KEY_ID": self.api_id,
                "KEY_SECRET": self.api_secret,
            }

            # Create the config directory (and any parents) if it does not
            # already exist.
            CONFIG.SETTINGS_DIR.mkdir(parents=True, exist_ok=True)

            # Write out the new config.
            with open(CONFIG.SETTINGS_FILE_PATH, "w") as fp:
                new_conf.write(fp)

    def _construct_poll_url(self, request_id: str) -> str:
        """Helper method to construct a polling URL."""
        return f"{self.structure_url}/{request_id}"

    def annotate(self, *args, **kwargs) -> dict:
        return self.structure(*args, **kwargs)

    def structure(self, text: str) -> dict:
        """Annotates a block of text using the ScienceIO API.

        Args:
            text (str): The text to structure.

        Raises:
            ValueError: Raised if the input text is not a `str`.
            TimeoutError: Raised if the annotation request exceeds the timeout
                limit.

        Returns:
            dict: The annotation data, as a Python dictionary.
        """
        request_id = self.send_structure_request(text)

        poll_url = self._construct_poll_url(request_id)

        # Poll for the response.
        first_loop = True
        start_time = time.time()
        while first_loop or time.time() - start_time < CONFIG.MAX_POLL_DURATION_SEC:
            # Sleep for a bit if we're not on the first loop.
            if not first_loop:
                time.sleep(CONFIG.POLL_SLEEP_DURATION_SEC)

            first_loop = False

            inf_result = self._poll_attempt(poll_url)

            if inf_result is not None:
                return inf_result

            # At this point, the request is still processing, so try again.

        # Here, we've exhausted all of our retry attempts, so fail.
        raise TimeoutError("structure request timed out, try again later")

    def send_annotate_request(self, *args, **kwargs) -> str:
        return self.send_structure_request(*args, **kwargs)

    def send_structure_request(self, text: str) -> str:
        """Submits a request to structure a block of text using the ScienceIO API.

        Args:
            text (str): The text to structure.

        Returns:
            str: A request token that is used with `get_annotation_reponse` to
                check the status of the annotation request, and to fetch the
                results when ready.
        """
        raw_response = self.session.post(
            self.structure_url,
            json={"text": text},
            headers=self.headers,
        )

        response = _response_handler(raw_response, self.response_format)

        request_id = response["request_id"]

        return request_id

    def get_annotate_response(self, *args, **kwargs) -> Optional[Dict]:
        return self.get_structure_response(*args, **kwargs)

    def get_structure_response(self, request_id: str) -> Optional[Dict]:
        """Given a request token, returns annotations if the corresponding
        annotation request has completed successfully.

        Args:
            request_id (str): The request token returned from a prior call to
                `send_structure_request`.

        Returns:
            Optional[Dict]: The annotations if the request has completed
                successfully, or `None` if it is still processing.
        """
        # Construct the URL to poll.
        poll_url = self._construct_poll_url(request_id)
        return self._poll_attempt(poll_url)

    async def annotate_async(self, *args, **kwargs):
        return self.structure_async(*args, **kwargs)

    async def structure_async(self, text: str):
        """Asynchronously structures a block of text using the ScienceIO API.

        Args:
            text (str): The text to structure.

        Raises:
            TimeoutError: Raised if the annotation request exceeds the timeout
                limit.

        Returns:
            dict: The annotation data, as a Python dictionary.
        """
        request_id = self.send_structure_request(text)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.structure_url, json={"text": text}, headers=self.headers
            ) as response_future:
                response = await _response_handler_async(response_future)

                request_id = response["request_id"]

            poll_url = self._construct_poll_url(request_id)

            # Poll for the response.
            first_loop = True
            start_time = time.time()
            while (
                first_loop or (time.time() - start_time) < CONFIG.MAX_POLL_DURATION_SEC
            ):
                # Sleep for a bit if we're not on the first loop.
                if not first_loop:
                    await asyncio.sleep(CONFIG.POLL_SLEEP_DURATION_SEC)

                first_loop = False

                async with session.get(
                    poll_url, headers=self.headers
                ) as response_future:
                    response = await _response_handler_async(response_future)

                inf_result = _poll_payload_handler(response)

                if inf_result is not None:
                    return inf_result

                # At this point, the request is still processing, so try again.

            # Here, we've exhausted all of our retry attempts, so fail.
            raise TimeoutError("structure request timed out, try again later")

    def _poll_attempt(self, poll_url: str) -> Optional[Dict]:
        """Helper method to make a single poll attempt, given a constructed
        poll URL with a request id."""
        raw_response = self.session.get(
            poll_url,
            headers=self.headers,
        )

        raw_response.raise_for_status()

        response = self.response_format.format_response(raw_response)

        return _poll_payload_handler(response)


def _response_handler(
    raw_response: requests.Response, response_format: ResponseFormat
) -> Dict:
    status_code = raw_response.status_code
    response = response_format.format_response(raw_response)

    if 400 <= status_code <= 599:
        details = response["detail"]
        raise HTTPError(
            status_code=status_code,
            message=f"{', '.join(details['errors']['text'])}",
        )

    return response


async def _response_handler_async(response_future: aiohttp.ClientResponse) -> Dict:
    status_code = response_future.status
    response = await response_future.json()

    if 400 <= status_code <= 599:
        details = response["detail"]
        raise HTTPError(
            status_code=status_code,
            message=f"{', '.join(details['errors']['text'])}",
        )

    return response


def _poll_payload_handler(payload: Dict) -> Optional[Dict]:
    status = payload["inference_status"]
    if status == "ERRORED" or status == "EXPIRED":
        raise ScienceIOError(payload["message"])
    elif status == "COMPLETED":
        return payload["inference_result"]
    elif status == "SUBMITTED":
        return None
    else:
        raise ScienceIOError("unknown status")
