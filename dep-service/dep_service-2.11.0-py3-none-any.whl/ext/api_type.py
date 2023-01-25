"""Service api type helpers."""

from typing import List, Type, Dict
from pydantic import BaseModel

from fastapi.responses import UJSONResponse
from fastapi import status

from service.ext import exc


def create(
    model: Type[BaseModel],
    tags: List[str],
    error_responses: Dict[int, Dict] = None,
) -> Dict:
    """API Doc CREATE generate."""

    responses = {
        status.HTTP_201_CREATED: {'model': model},
        status.HTTP_400_BAD_REQUEST: {'model': exc.ErrorBadRequest},
    }

    if error_responses:
        responses.update(error_responses)

    return {
        'tags': tags,
        'status_code': status.HTTP_201_CREATED,
        'response_model': model,
        'responses': responses,
    }


def read(
    model: Type[BaseModel],
    tags: List[str],
    error_responses: Dict[int, Dict] = None,
) -> Dict:
    """API Doc READ generate."""

    responses = {
        status.HTTP_200_OK: {'model': model},
        status.HTTP_404_NOT_FOUND: {'model': exc.ErrorNotFound},
        status.HTTP_400_BAD_REQUEST: {'model': exc.ErrorBadRequest},
    }

    if error_responses:
        responses.update(error_responses)

    return {
        'tags': tags,
        'status_code': status.HTTP_200_OK,
        'response_model': model,
        'responses': responses,
    }


def update(
    model: Type[BaseModel],
    tags: List[str],
    error_responses: Dict[int, Dict] = None,
) -> Dict:
    """API Doc UPDATE generate."""

    responses = {
        status.HTTP_200_OK: {'model': model},
        status.HTTP_404_NOT_FOUND: {'model': exc.ErrorNotFound},
        status.HTTP_400_BAD_REQUEST: {'model': exc.ErrorBadRequest},
    }

    if error_responses:
        responses.update(error_responses)

    return {
        'tags': tags,
        'status_code': status.HTTP_200_OK,
        'response_model': model,
        'responses': responses,
    }


def delete(
    model: Type[BaseModel],  # noqa
    tags: List[str],
    error_responses: Dict[int, Dict] = None,
) -> Dict:
    """API Doc DELETE generate."""

    responses = {
        status.HTTP_204_NO_CONTENT: {'response_model': None},
        status.HTTP_404_NOT_FOUND: {'model': exc.ErrorNotFound},
    }

    if error_responses:
        responses.update(error_responses)

    return {
        'tags': tags,
        'status_code': status.HTTP_204_NO_CONTENT,
        'responses': responses,
    }


def lookup(
    model: Type[BaseModel],  # noqa
    paginated_model: Type[BaseModel],
    tags: List[str],
    error_responses: Dict[int, Dict] = None,
) -> Dict:
    """API Doc LOOKUP generate."""

    responses = {
        status.HTTP_200_OK: {'model': paginated_model},
    }

    if error_responses:
        responses.update(error_responses)

    return {
        'tags': tags,
        'response_model': paginated_model,
        'responses': responses,
    }


def custom(
    model: Type[BaseModel],
    tags: List[str],
    error_responses: Dict[int, Dict] = None,
) -> Dict:
    """API Doc CUSTOM generate."""

    responses = {
        status.HTTP_200_OK: {'model': model},
    }

    if error_responses:
        responses.update(error_responses)

    return {
        'tags': tags,
        'response_model': model,
        'responses': responses,
    }


def bulk(
    tags: List[str],
    model: Type[BaseModel] = None,
    error_responses: Dict[int, Dict] = None,
) -> Dict:
    """API Doc BULK generate."""

    responses = {
        status.HTTP_200_OK: {'model': model},
    }

    if error_responses:
        responses.update(error_responses)

    return {
        'tags': tags,
        'response_model': model,
        'responses': responses,
    }


def ujson_decoder(
    model: Type[BaseModel],
    tags: List[str],
    error_responses: Dict[int, Dict] = None,
) -> Dict:
    """API UJSON decoder generate."""

    responses = {
        status.HTTP_200_OK: {'model': model},
    }

    if error_responses:
        responses.update(error_responses)

    return {
        'tags': tags,
        'response_model': model,
        'response_class': UJSONResponse,
        'responses': responses,
    }
