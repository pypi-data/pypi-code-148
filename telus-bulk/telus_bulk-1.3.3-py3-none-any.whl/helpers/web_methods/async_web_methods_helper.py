import httpx
from typing import Literal, Optional
from loguru import logger
from httpx._types import QueryParamTypes


async def async_http_get(
    base_url: str,
    segment: str = "",
    params: QueryParamTypes = None,
    access_token: str = None,
):
    """
    Async fetch get request
    :param base_url: principal domain
    :param segment: request segment
    :param access_token: JWT access token
    :return: JSON response
    """
    headers = {
        "authorization": f"Bearer {access_token}",
    }
    # USING ASYNC CLIENT
    async with httpx.AsyncClient(
        base_url=base_url, headers=headers, verify=False, timeout=30
    ) as client:
        try:
            r = await client.get(url=segment, params=params)
            r.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}"
            )
            return None
        except httpx.HTTPError as exc:
            logger.error(f"Error while requesting {exc.request.url!r}")
            return None
    return r.json()


async def async_http_post(
    base_url: str,
    segment: str = "",
    data: Optional[dict[str, str]] = None,
    content_type: Literal["JSON", "FORM-ENCODED"] = "FORM-ENCODED",
):
    """
    Async post request
    :param base_url: principal domain
    :param segment: request segment
    :param data: request payload
    :return: JSON response
    """
    if content_type == "JSON":
        headers = [
            (b"content-type", b"application/json"),
            (b"accept", b"application/json"),
        ]
    elif content_type == "FORM-ENCODED":
        headers = {"content-type": "application/x-www-form-urlencoded"}
    # USING ASYNC CLIENT
    async with httpx.AsyncClient(
        base_url=base_url, headers=headers, verify=False, timeout=30
    ) as client:
        try:
            if content_type == "JSON":
                r = await client.post(url=segment, json=data)
            else:
                r = await client.post(url=segment, data=data)
            r.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"Error response {exc.response.status_code} while requesting {exc.request.url}"
            )
            return None
        except httpx.HTTPError as exc:
            logger.error(f"Error while requesting {exc.request.url}")
            return None
    return r.json()
