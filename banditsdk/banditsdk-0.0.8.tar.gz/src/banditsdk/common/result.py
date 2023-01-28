from enum import Enum
from typing import TypeVar, Generic, Optional
from pydantic import BaseModel


class ActionStatus(str, Enum):
    success = "success"
    failure = "failure"


T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    """
    Factory result class.
    Has status, data, error fields.
    Used for general definition of function`s restult.
    Example:
    def send_data_to_remote(data, url):
    	response = post(url, data=data)
    	try:
	    if response.status == 200:
	        return Result.success(data=response.json)
	    else:
	        return Result.failure(error=response.text)
	except Exception as error:
	    return Result.server_error(error=str(error))
    """
    status: ActionStatus
    data: Optional[T]
    error: Optional[str]

    class Config:
        use_enum_values = True

    def is_success(self):
        return self.status == ActionStatus.success

    def is_failure(self):
        return not self.is_success()

    @classmethod
    def success(cls, data: Optional[T] = None):
        return Result(status=ActionStatus.success, data=data, error=None)

    @classmethod
    def failure(cls, error: str):
        return Result(status=ActionStatus.failure, data=None, error=error)

    @classmethod
    def server_error(
        cls,
        error: str = "An error occurred while performing the operation. please try again late or contact support.",
    ):
        return Result(status=ActionStatus.failure, data=None, error=error)


