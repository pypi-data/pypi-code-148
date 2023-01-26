import traceback
from . import logger
from .types import TaskResult, Statuses


def handle_errors(func):
    def wrapper(*args, **akwrgs):
        try:
            return TaskResult(result = func(*args, **akwrgs)).dict()
        except Exception as exc:
            logger.error(f"{exc}")
            return TaskResult(
                status_code = Statuses.err,
                result = {
                    "msg": f"{exc}", 
                    "traceback": traceback.format_exc()
                }
            ).dict()
    return wrapper
