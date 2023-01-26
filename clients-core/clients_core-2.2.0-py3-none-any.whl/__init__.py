__version__ = "2.2.0"

__all__ = [
    "authentication",
    "SimpleRestClient",
    "SecuredRestClient",
    "RestClient",
    "ApiMatchClient",
    "ServiceDirectoryMatchClient",
    "GatewayMatchClient",
]


from clients_core.simple_rest_client import SimpleRestClient
from clients_core.secured_rest_client import SecuredRestClient
from clients_core.rest_client import RestClient
from clients_core.api_match_client import (
    ApiMatchClient,
    ServiceDirectoryMatchClient,
    GatewayMatchClient,
)
