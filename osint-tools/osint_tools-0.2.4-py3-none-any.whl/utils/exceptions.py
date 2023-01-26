
# https://fastapi.tiangolo.com/tutorial/handling-errors/?h=#install-custom-exception-handlers
from fastapi.exceptions import HTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST)

class EnumException(Exception):
    def __init__(self, error_message: str):
        self.error_message = error_message

class AuthException(Exception):
    def __init__(self, error_message: str):
        self.error_message = error_message



login_exc: HTTPException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"})

register_exc: HTTPException = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="User Exists with that Email.")
    
credentials_exc: HTTPException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"})
    
current_user_exc: HTTPException = HTTPException(
    status_code=HTTP_400_BAD_REQUEST, 
    detail="Inactive user")
