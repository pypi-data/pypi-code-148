import inspect, re
import simplejson
from typing import Tuple, Union
from pydantic import BaseModel
from . import logger
from enum import Enum


class Task(BaseModel):
    procedure: str  # remote procedure name
    kwargs: dict = {}  # remote procedure kwargs

class Statuses(Enum):
    ok:int = 200
    err:int = 500

class TaskResult(BaseModel):
    status_code: Statuses = Statuses.ok
    result:Union[str,dict,None]

    def __str__(self):
        ''' str(TaskResult(result={})) -> '{}' '''
        return simplejson.dumps(self.result)

    class Config:
        use_enum_values = True

class ReturnTypeError(Exception):
    ...


class CallbackHandler:
    """Class to extend"""

    __RETURN_TYPE_TEMPLATE = Tuple[int, dict]
    __TASK_EXECUTOR_PATTERN = "^task_"

    def __init__(self) -> None:
        task_member_count: int = 0  # count of task executor
        for method in inspect.getmembers(self, predicate=inspect.ismethod):
            method_name = method[0]
            if re.match(self.__TASK_EXECUTOR_PATTERN, method_name):
                task_member_count += 1
                if (
                    inspect.signature(getattr(self, method_name)).return_annotation
                    != self.__RETURN_TYPE_TEMPLATE
                ):
                    raise ReturnTypeError(
                        f'"{method_name}" -> Return type must be type <{self.__RETURN_TYPE_TEMPLATE}>'
                    )
        if task_member_count == 0:
            logger.warning("CallbackHandler -> No tasks to execute was founded!")


# ---| Exmaple
# class TestCallbackHandler(CallbackHandler):
#     def __init__(
#         self,
#     ) -> None:
#         super(TestCallbackHandler, self).__init__()

#     def task_test(self, arg1, arg2=0) -> Tuple[int, dict, int]:
#         return 200, {"result": "test({arg1}, {arg2})"}


# TestCallbackHandler()
