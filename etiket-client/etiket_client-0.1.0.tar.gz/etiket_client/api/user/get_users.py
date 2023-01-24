from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.base_error import BaseError
from ...models.http_validation_error import HTTPValidationError
from ...models.user_out import UserOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 800,
) -> Dict[str, Any]:
    url = "{}/api/v1/users/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["offset"] = offset

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[BaseError, HTTPValidationError, List[UserOut]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UserOut.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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


def _build_response(*, response: httpx.Response) -> Response[Union[BaseError, HTTPValidationError, List[UserOut]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 800,
) -> Response[Union[BaseError, HTTPValidationError, List[UserOut]]]:
    """Get Users

    Args:
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 800.

    Returns:
        Response[Union[BaseError, HTTPValidationError, List[UserOut]]]
    """

    kwargs = _get_kwargs(
        client=client,
        offset=offset,
        limit=limit,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 800,
) -> Optional[Union[BaseError, HTTPValidationError, List[UserOut]]]:
    """Get Users

    Args:
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 800.

    Returns:
        Response[Union[BaseError, HTTPValidationError, List[UserOut]]]
    """

    return sync_detailed(
        client=client,
        offset=offset,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 800,
) -> Response[Union[BaseError, HTTPValidationError, List[UserOut]]]:
    """Get Users

    Args:
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 800.

    Returns:
        Response[Union[BaseError, HTTPValidationError, List[UserOut]]]
    """

    kwargs = _get_kwargs(
        client=client,
        offset=offset,
        limit=limit,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 800,
) -> Optional[Union[BaseError, HTTPValidationError, List[UserOut]]]:
    """Get Users

    Args:
        offset (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 800.

    Returns:
        Response[Union[BaseError, HTTPValidationError, List[UserOut]]]
    """

    return (
        await asyncio_detailed(
            client=client,
            offset=offset,
            limit=limit,
        )
    ).parsed
