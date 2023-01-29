"""Custom exceptions classes for Flora."""
import json

from sys import exc_info
from typing import Any, Optional, Union
from datetime import datetime as dt

class FloraException(Exception):
    """Base exception for all Flora exceptions.
    """
    def __init__(
            self,
            error_code: int,
            message: str,
            datetime: Optional[Union[str, dt]] = None,
            user_id: Optional[str] = None,
            workplace_id: Optional[str] = None,
            data: Optional[Any] = None,
    ):
        # format is {module}/{error_code}
        # where module would be "model"
        self.error_code = f"model/{error_code}"
        self.message = message
        if datetime is None:
            self.datetime = dt.now().isoformat()
        else:
            # Convert datetime to isoformat if it is not already
            if isinstance(datetime, dt):
                self.datetime = datetime.isoformat()
            else:
                self.datetime = datetime
        self.user_id = user_id
        self.workplace_id = workplace_id
        self.data = data

        self.traceback = exc_info()

        super().__init__(str(self))

    def __str__(self) -> str:
        """Convert the exception to a JSON string,
        which is to be parsed by the error handler.

        All fields are in camelCase.

        Returns:
            str: JSON string
        """
        return json.dumps(
            {
                "errorCode": self.error_code,
                "message": self.message,
                "datetime": self.datetime,
                "userId": self.user_id,
                "workplaceId": self.workplace_id,
                "data": self.data,
            }
        )