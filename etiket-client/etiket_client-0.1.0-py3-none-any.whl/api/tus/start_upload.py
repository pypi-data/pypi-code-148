from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...models.base_error import BaseError
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    upload_length: Union[Unset, int] = UNSET,
    tus_resumable: str,
    upload_metadata: str,
    content_length: int,
    content_type: Union[Unset, str] = UNSET,
    upload_concat: Union[Unset, str] = UNSET,
    upload_defer_length: Union[Unset, int] = UNSET,
    upload_checksum: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/uploads/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(upload_length, Unset):
        headers["upload-length"] = str(upload_length)

    headers["tus-resumable"] = tus_resumable

    headers["upload-metadata"] = upload_metadata

    headers["content-length"] = str(content_length)

    if not isinstance(content_type, Unset):
        headers["content-type"] = content_type

    if not isinstance(upload_concat, Unset):
        headers["upload-concat"] = upload_concat

    if not isinstance(upload_defer_length, Unset):
        headers["upload-defer-length"] = str(upload_defer_length)

    if not isinstance(upload_checksum, Unset):
        headers["upload-checksum"] = upload_checksum

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, BaseError, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = cast(Any, response.json())
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


def _build_response(*, response: httpx.Response) -> Response[Union[Any, BaseError, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    upload_length: Union[Unset, int] = UNSET,
    tus_resumable: str,
    upload_metadata: str,
    content_length: int,
    content_type: Union[Unset, str] = UNSET,
    upload_concat: Union[Unset, str] = UNSET,
    upload_defer_length: Union[Unset, int] = UNSET,
    upload_checksum: Union[Unset, str] = UNSET,
) -> Response[Union[Any, BaseError, HTTPValidationError]]:
    """Start Upload

    Args:
        upload_length (Union[Unset, int]):
        tus_resumable (str):
        upload_metadata (str):
        content_length (int):
        content_type (Union[Unset, str]):
        upload_concat (Union[Unset, str]):
        upload_defer_length (Union[Unset, int]):
        upload_checksum (Union[Unset, str]):

    Returns:
        Response[Union[Any, BaseError, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        upload_length=upload_length,
        tus_resumable=tus_resumable,
        upload_metadata=upload_metadata,
        content_length=content_length,
        content_type=content_type,
        upload_concat=upload_concat,
        upload_defer_length=upload_defer_length,
        upload_checksum=upload_checksum,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    upload_length: Union[Unset, int] = UNSET,
    tus_resumable: str,
    upload_metadata: str,
    content_length: int,
    content_type: Union[Unset, str] = UNSET,
    upload_concat: Union[Unset, str] = UNSET,
    upload_defer_length: Union[Unset, int] = UNSET,
    upload_checksum: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, BaseError, HTTPValidationError]]:
    """Start Upload

    Args:
        upload_length (Union[Unset, int]):
        tus_resumable (str):
        upload_metadata (str):
        content_length (int):
        content_type (Union[Unset, str]):
        upload_concat (Union[Unset, str]):
        upload_defer_length (Union[Unset, int]):
        upload_checksum (Union[Unset, str]):

    Returns:
        Response[Union[Any, BaseError, HTTPValidationError]]
    """

    return sync_detailed(
        client=client,
        upload_length=upload_length,
        tus_resumable=tus_resumable,
        upload_metadata=upload_metadata,
        content_length=content_length,
        content_type=content_type,
        upload_concat=upload_concat,
        upload_defer_length=upload_defer_length,
        upload_checksum=upload_checksum,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    upload_length: Union[Unset, int] = UNSET,
    tus_resumable: str,
    upload_metadata: str,
    content_length: int,
    content_type: Union[Unset, str] = UNSET,
    upload_concat: Union[Unset, str] = UNSET,
    upload_defer_length: Union[Unset, int] = UNSET,
    upload_checksum: Union[Unset, str] = UNSET,
) -> Response[Union[Any, BaseError, HTTPValidationError]]:
    """Start Upload

    Args:
        upload_length (Union[Unset, int]):
        tus_resumable (str):
        upload_metadata (str):
        content_length (int):
        content_type (Union[Unset, str]):
        upload_concat (Union[Unset, str]):
        upload_defer_length (Union[Unset, int]):
        upload_checksum (Union[Unset, str]):

    Returns:
        Response[Union[Any, BaseError, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        upload_length=upload_length,
        tus_resumable=tus_resumable,
        upload_metadata=upload_metadata,
        content_length=content_length,
        content_type=content_type,
        upload_concat=upload_concat,
        upload_defer_length=upload_defer_length,
        upload_checksum=upload_checksum,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    upload_length: Union[Unset, int] = UNSET,
    tus_resumable: str,
    upload_metadata: str,
    content_length: int,
    content_type: Union[Unset, str] = UNSET,
    upload_concat: Union[Unset, str] = UNSET,
    upload_defer_length: Union[Unset, int] = UNSET,
    upload_checksum: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, BaseError, HTTPValidationError]]:
    """Start Upload

    Args:
        upload_length (Union[Unset, int]):
        tus_resumable (str):
        upload_metadata (str):
        content_length (int):
        content_type (Union[Unset, str]):
        upload_concat (Union[Unset, str]):
        upload_defer_length (Union[Unset, int]):
        upload_checksum (Union[Unset, str]):

    Returns:
        Response[Union[Any, BaseError, HTTPValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            upload_length=upload_length,
            tus_resumable=tus_resumable,
            upload_metadata=upload_metadata,
            content_length=content_length,
            content_type=content_type,
            upload_concat=upload_concat,
            upload_defer_length=upload_defer_length,
            upload_checksum=upload_checksum,
        )
    ).parsed
