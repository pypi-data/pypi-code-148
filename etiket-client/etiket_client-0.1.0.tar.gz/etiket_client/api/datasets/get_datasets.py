import datetime
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.base_error import BaseError
from ...models.dataset_out import DatasetOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    scope: str,
    collection: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    uid: Union[Unset, None, str] = UNSET,
    since: Union[Unset, None, datetime.datetime] = UNSET,
    until: Union[Unset, None, datetime.datetime] = UNSET,
    sample: Union[Unset, None, str] = UNSET,
    fridge: Union[Unset, None, str] = UNSET,
    setup: Union[Unset, None, str] = UNSET,
    measurement_type: Union[Unset, None, str] = UNSET,
    keywords: Union[Unset, None, List[str]] = UNSET,
    variables_measured: Union[Unset, None, List[str]] = UNSET,
    offset: Union[Unset, None, int] = 0,
    ranking: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 500,
) -> Dict[str, Any]:
    url = "{}/api/v1/datasets/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["scope"] = scope

    params["collection"] = collection

    params["name"] = name

    params["uid"] = uid

    json_since: Union[Unset, None, str] = UNSET
    if not isinstance(since, Unset):
        json_since = since.isoformat() if since else None

    params["since"] = json_since

    json_until: Union[Unset, None, str] = UNSET
    if not isinstance(until, Unset):
        json_until = until.isoformat() if until else None

    params["until"] = json_until

    params["sample"] = sample

    params["fridge"] = fridge

    params["setup"] = setup

    params["measurementType"] = measurement_type

    json_keywords: Union[Unset, None, List[str]] = UNSET
    if not isinstance(keywords, Unset):
        if keywords is None:
            json_keywords = None
        else:
            json_keywords = keywords

    params["keywords"] = json_keywords

    json_variables_measured: Union[Unset, None, List[str]] = UNSET
    if not isinstance(variables_measured, Unset):
        if variables_measured is None:
            json_variables_measured = None
        else:
            json_variables_measured = variables_measured

    params["variablesMeasured"] = json_variables_measured

    params["offset"] = offset

    params["ranking"] = ranking

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[BaseError, HTTPValidationError, List[DatasetOut]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = DatasetOut.from_dict(response_200_item_data)

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


def _build_response(*, response: httpx.Response) -> Response[Union[BaseError, HTTPValidationError, List[DatasetOut]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    scope: str,
    collection: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    uid: Union[Unset, None, str] = UNSET,
    since: Union[Unset, None, datetime.datetime] = UNSET,
    until: Union[Unset, None, datetime.datetime] = UNSET,
    sample: Union[Unset, None, str] = UNSET,
    fridge: Union[Unset, None, str] = UNSET,
    setup: Union[Unset, None, str] = UNSET,
    measurement_type: Union[Unset, None, str] = UNSET,
    keywords: Union[Unset, None, List[str]] = UNSET,
    variables_measured: Union[Unset, None, List[str]] = UNSET,
    offset: Union[Unset, None, int] = 0,
    ranking: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 500,
) -> Response[Union[BaseError, HTTPValidationError, List[DatasetOut]]]:
    """Get Datasets

    Args:
        scope (str):
        collection (Union[Unset, None, str]):
        name (Union[Unset, None, str]):
        uid (Union[Unset, None, str]):
        since (Union[Unset, None, datetime.datetime]):
        until (Union[Unset, None, datetime.datetime]):
        sample (Union[Unset, None, str]):
        fridge (Union[Unset, None, str]):
        setup (Union[Unset, None, str]):
        measurement_type (Union[Unset, None, str]):
        keywords (Union[Unset, None, List[str]]):
        variables_measured (Union[Unset, None, List[str]]):
        offset (Union[Unset, None, int]):
        ranking (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 500.

    Returns:
        Response[Union[BaseError, HTTPValidationError, List[DatasetOut]]]
    """

    kwargs = _get_kwargs(
        client=client,
        scope=scope,
        collection=collection,
        name=name,
        uid=uid,
        since=since,
        until=until,
        sample=sample,
        fridge=fridge,
        setup=setup,
        measurement_type=measurement_type,
        keywords=keywords,
        variables_measured=variables_measured,
        offset=offset,
        ranking=ranking,
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
    scope: str,
    collection: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    uid: Union[Unset, None, str] = UNSET,
    since: Union[Unset, None, datetime.datetime] = UNSET,
    until: Union[Unset, None, datetime.datetime] = UNSET,
    sample: Union[Unset, None, str] = UNSET,
    fridge: Union[Unset, None, str] = UNSET,
    setup: Union[Unset, None, str] = UNSET,
    measurement_type: Union[Unset, None, str] = UNSET,
    keywords: Union[Unset, None, List[str]] = UNSET,
    variables_measured: Union[Unset, None, List[str]] = UNSET,
    offset: Union[Unset, None, int] = 0,
    ranking: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 500,
) -> Optional[Union[BaseError, HTTPValidationError, List[DatasetOut]]]:
    """Get Datasets

    Args:
        scope (str):
        collection (Union[Unset, None, str]):
        name (Union[Unset, None, str]):
        uid (Union[Unset, None, str]):
        since (Union[Unset, None, datetime.datetime]):
        until (Union[Unset, None, datetime.datetime]):
        sample (Union[Unset, None, str]):
        fridge (Union[Unset, None, str]):
        setup (Union[Unset, None, str]):
        measurement_type (Union[Unset, None, str]):
        keywords (Union[Unset, None, List[str]]):
        variables_measured (Union[Unset, None, List[str]]):
        offset (Union[Unset, None, int]):
        ranking (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 500.

    Returns:
        Response[Union[BaseError, HTTPValidationError, List[DatasetOut]]]
    """

    return sync_detailed(
        client=client,
        scope=scope,
        collection=collection,
        name=name,
        uid=uid,
        since=since,
        until=until,
        sample=sample,
        fridge=fridge,
        setup=setup,
        measurement_type=measurement_type,
        keywords=keywords,
        variables_measured=variables_measured,
        offset=offset,
        ranking=ranking,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    scope: str,
    collection: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    uid: Union[Unset, None, str] = UNSET,
    since: Union[Unset, None, datetime.datetime] = UNSET,
    until: Union[Unset, None, datetime.datetime] = UNSET,
    sample: Union[Unset, None, str] = UNSET,
    fridge: Union[Unset, None, str] = UNSET,
    setup: Union[Unset, None, str] = UNSET,
    measurement_type: Union[Unset, None, str] = UNSET,
    keywords: Union[Unset, None, List[str]] = UNSET,
    variables_measured: Union[Unset, None, List[str]] = UNSET,
    offset: Union[Unset, None, int] = 0,
    ranking: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 500,
) -> Response[Union[BaseError, HTTPValidationError, List[DatasetOut]]]:
    """Get Datasets

    Args:
        scope (str):
        collection (Union[Unset, None, str]):
        name (Union[Unset, None, str]):
        uid (Union[Unset, None, str]):
        since (Union[Unset, None, datetime.datetime]):
        until (Union[Unset, None, datetime.datetime]):
        sample (Union[Unset, None, str]):
        fridge (Union[Unset, None, str]):
        setup (Union[Unset, None, str]):
        measurement_type (Union[Unset, None, str]):
        keywords (Union[Unset, None, List[str]]):
        variables_measured (Union[Unset, None, List[str]]):
        offset (Union[Unset, None, int]):
        ranking (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 500.

    Returns:
        Response[Union[BaseError, HTTPValidationError, List[DatasetOut]]]
    """

    kwargs = _get_kwargs(
        client=client,
        scope=scope,
        collection=collection,
        name=name,
        uid=uid,
        since=since,
        until=until,
        sample=sample,
        fridge=fridge,
        setup=setup,
        measurement_type=measurement_type,
        keywords=keywords,
        variables_measured=variables_measured,
        offset=offset,
        ranking=ranking,
        limit=limit,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    scope: str,
    collection: Union[Unset, None, str] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    uid: Union[Unset, None, str] = UNSET,
    since: Union[Unset, None, datetime.datetime] = UNSET,
    until: Union[Unset, None, datetime.datetime] = UNSET,
    sample: Union[Unset, None, str] = UNSET,
    fridge: Union[Unset, None, str] = UNSET,
    setup: Union[Unset, None, str] = UNSET,
    measurement_type: Union[Unset, None, str] = UNSET,
    keywords: Union[Unset, None, List[str]] = UNSET,
    variables_measured: Union[Unset, None, List[str]] = UNSET,
    offset: Union[Unset, None, int] = 0,
    ranking: Union[Unset, None, int] = 0,
    limit: Union[Unset, None, int] = 500,
) -> Optional[Union[BaseError, HTTPValidationError, List[DatasetOut]]]:
    """Get Datasets

    Args:
        scope (str):
        collection (Union[Unset, None, str]):
        name (Union[Unset, None, str]):
        uid (Union[Unset, None, str]):
        since (Union[Unset, None, datetime.datetime]):
        until (Union[Unset, None, datetime.datetime]):
        sample (Union[Unset, None, str]):
        fridge (Union[Unset, None, str]):
        setup (Union[Unset, None, str]):
        measurement_type (Union[Unset, None, str]):
        keywords (Union[Unset, None, List[str]]):
        variables_measured (Union[Unset, None, List[str]]):
        offset (Union[Unset, None, int]):
        ranking (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):  Default: 500.

    Returns:
        Response[Union[BaseError, HTTPValidationError, List[DatasetOut]]]
    """

    return (
        await asyncio_detailed(
            client=client,
            scope=scope,
            collection=collection,
            name=name,
            uid=uid,
            since=since,
            until=until,
            sample=sample,
            fridge=fridge,
            setup=setup,
            measurement_type=measurement_type,
            keywords=keywords,
            variables_measured=variables_measured,
            offset=offset,
            ranking=ranking,
            limit=limit,
        )
    ).parsed
