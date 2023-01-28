from enum import Enum
from typing import TypeVar, Generic, Optional, Union
from pydantic import BaseModel



class ActionStatus(str, Enum):
    success = "success"
    failure = "failure"


T = TypeVar("T")


class WebResult(BaseModel, Generic[T]):
    """
    Factory either http-result or ws-result class.
    Has status, data, error fields.
    Used for general definition of function`s restult.
    Example:
    def send_data_to_remote(data, url):
    	response = post(url, data=data)
    	try:
	    if response.status == 200:
	        return Result.success(data=response.json, status_code=200)
	    else:
	        return Result.failure(status_code=400, detail="Bad request.")
	except Exception as error:
	    return Result.server_error(status_code=500, detail="Internal server error.")
    """
    status: ActionStatus
    data: Optional[T]
    status_code: Union[int, Enum]
    detail: Optional[str]

    class Config:
        use_enum_values = True

    def is_success(self):
        return self.status == ActionStatus.success

    def is_failure(self):
        return not self.is_success()

    @classmethod
    def success(cls, data: Optional[T] = None, status_code: int = 200):
        return WebResult(status=ActionStatus.success, data=data, status_code=status_code)

    @classmethod
    def failure(cls, status_code: int, detail: Optional[str] = None):
        return WebResult(status=ActionStatus.failure, status_code=status_code, detail=detail)

    @classmethod
    def server_error(
        cls,
        status_code: int = 500, detail: Optional[str] = "Internal server error.",
    ):
        return WebResult(status=ActionStatus.failure,  status_code=status_code, detail=detail)

