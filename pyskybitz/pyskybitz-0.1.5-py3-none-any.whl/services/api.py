"""API calls happen here."""
import logging
from enum import Enum
from typing import Any, Dict, Optional

import inject
import requests

from pyskybitz.config import ConnectionConfig
from pyskybitz.models.base import SkyBitz
from pyskybitz.services.parser import Parser

LOGGER = logging.getLogger("API")
LOGGER.setLevel(logging.INFO)


class HTTPMethod(str, Enum):
    """HTTP methods."""

    GET = "GET"
    POST = "POST"


class SortingOptions(str, Enum):
    """Options for sorting the response."""

    # asset id ascending, observation time descending order
    ASSET_ID_ASCENDING = "1"
    # assert id descending, observation time ascending order
    ASSERT_ID_DESCENDING = "-1"
    # observation time descending order
    OBSERVATION_TIME_DESCENDING = "2"
    # observation time ascending order
    OBSERVATION_TIME_ASCENDING = "-2"


class AssetIdPreset(str, Enum):
    """Preset values for asset id."""

    RETURN_ALL_ASSETS = "ALL"


class APIMethods(str, Enum):
    """API methods that we support."""

    QueryPositions = "QueryPositions"
    QueryList = "QueryList"


class API:
    """Class to work with API calls."""

    @inject.autoparams()
    def __init__(
        self,
        parser_service: Parser,
        connection_config: ConnectionConfig,
        http_client_session: requests.Session,
    ):
        """Initialize API instance."""
        self.parser_service = parser_service
        self.connection_config = connection_config
        self.http_client_session = http_client_session

    def _credentials_for_url(self) -> Dict[str, str]:
        """Generate URL params as dict with credentials."""
        return {
            "customer": self.connection_config.customer,
            "password": self.connection_config.password,
            "version": self.connection_config.version,
        }

    def _base_url(self) -> str:
        """Generate base URL with port information."""
        return f"https://{self.connection_config.base_domain}:{self.connection_config.port}"

    @staticmethod
    def _api_call_url(base_url: str, api_method_name: str) -> str:
        """Generate a final URL to call a method on API."""
        return f"{base_url}/{api_method_name}"

    @staticmethod
    def _prepare_kwargs_for_method_call(
        method: str, payload: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Depending on the method type, use params, json or other keywords to attach payload.

        :param method: HTTP method name.
        :param payload: Payload data as a dictionary.
        :return: Dictionary object including the necessary keywords and data.
        """
        kwargs = {}
        if method == HTTPMethod.GET:
            kwargs["params"] = payload
        else:
            kwargs["data"] = payload
        return kwargs

    def _call(
        self,
        method: HTTPMethod,
        api_method_name: APIMethods,
        payload: Dict[str, str],
    ) -> Optional[requests.Response]:
        """Execute a call to API."""
        try:
            credentials = self._credentials_for_url()
            payload.update(credentials)
            kwargs = self._prepare_kwargs_for_method_call(method, payload)
            api_url = self._api_call_url(self._base_url(), api_method_name)
            return self.http_client_session.request(
                method=method, url=api_url, **kwargs
            )
        except requests.RequestException:
            LOGGER.error("Could not finish the request", exc_info=True)

    def _parse_response(self, response: requests.Response) -> SkyBitz:
        """
        Parse incoming response from API and convert it into SkyBItz python object.

        :param response: XML Response from API.
        :return: SkyBitz python object.
        """
        return self.parser_service.parse_string(response.text, silence=True)

    def _call_api_method(
        self, method: HTTPMethod, api_method_name: APIMethods, payload: Dict[str, str]
    ) -> SkyBitz:
        """
        Call API method and parse the response.

        :param method: HTTP method name.
        :param api_method_name: API method name.
        :param payload: Payload data.
        :return: SkyBitz object.
        """
        response = self._call(
            method=method,
            api_method_name=api_method_name,
            payload=payload,
        )
        return self._parse_response(response)

    def query_positions(
        self,
        asset_id: str,
        sort_by: SortingOptions = SortingOptions.ASSET_ID_ASCENDING,
    ) -> SkyBitz:
        """Query positions of all assets."""
        payload = {"assetid": asset_id, "sortby": str(sort_by.value)}  # noqa
        return self._call_api_method(
            method=HTTPMethod.GET,
            api_method_name=APIMethods.QueryPositions,
            payload=payload,
        )
