from fastapi import HTTPException


def throw(exception: Exception):
    raise exception


NotFoundException = HTTPException(status_code=404, detail="Item not found")
