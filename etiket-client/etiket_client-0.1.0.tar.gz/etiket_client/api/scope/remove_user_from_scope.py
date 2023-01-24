from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.base_error import BaseError
from ...models.http_validation_error import HTTPValidationError
from ...models.scope_out import ScopeOut
from ...types import Response


def _get_kwargs(
    scope: str,
    username: str,
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/api/v1/scopes/{scope}/members/{username}".format(client.base_url, scope=scope, username=username)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[BaseError, HTTPValidationError, ScopeOut]]:
    if response.status_code == 200:
        response_200 = ScopeOut.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = BaseError.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = BaseError.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = BaseError.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = BaseError.from_dict(response.json())

        return response_404
    if response.status_code == 409:
        response_409 = BaseError.from_dict(response.json())

        return response_409
    if response.status_code == 410:
        response_410 = BaseError.from_dict(response.json())

        return response_410
    if response.status_code == 413:
        response_413 = BaseError.from_dict(response.json())

        return response_413
    if response.status_code == 500:
        response_500 = BaseError.from_dict(response.json())

        return response_500
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[BaseError, HTTPValidationError, ScopeOut]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    scope: str,
    username: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[BaseError, HTTPValidationError, ScopeOut]]:
    """Remove User From Scope

    Args:
        scope (str):
        username (str):

    Returns:
        Response[Union[BaseError, HTTPValidationError, ScopeOut]]
    """

    kwargs = _get_kwargs(
        scope=scope,
        username=username,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    scope: str,
    username: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[BaseError, HTTPValidationError, ScopeOut]]:
    """Remove User From Scope

    Args:
        scope (str):
        username (str):

    Returns:
        Response[Union[BaseError, HTTPValidationError, ScopeOut]]
    """

    return sync_detailed(
        scope=scope,
        username=username,
        client=client,
    ).parsed


async def asyncio_detailed(
    scope: str,
    username: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[BaseError, HTTPValidationError, ScopeOut]]:
    """Remove User From Scope

    Args:
        scope (str):
        username (str):

    Returns:
        Response[Union[BaseError, HTTPValidationError, ScopeOut]]
    """

    kwargs = _get_kwargs(
        scope=scope,
        username=username,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    scope: str,
    username: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[BaseError, HTTPValidationError, ScopeOut]]:
    """Remove User From Scope

    Args:
        scope (str):
        username (str):

    Returns:
        Response[Union[BaseError, HTTPValidationError, ScopeOut]]
    """

    return (
        await asyncio_detailed(
            scope=scope,
            username=username,
            client=client,
        )
    ).parsed
