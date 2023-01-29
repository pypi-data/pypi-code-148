from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel
from script_master_helper.executor.client import errors


class HttpErrorDetail(BaseModel):
    message: str
    detail: Any


def get_404_exception(detail: Any):
    return HTTPException(
        errors.not_found_error.code,
        detail=HttpErrorDetail(
            message=errors.not_found_error.message,
            detail=detail,
        ),
    )


def get_max_number_processes_exception(detail):
    return HTTPException(
        errors.max_number_processes_error.code,
        detail=HttpErrorDetail(
            message=errors.max_number_processes_error.message,
            detail=detail,
        ),
    )
