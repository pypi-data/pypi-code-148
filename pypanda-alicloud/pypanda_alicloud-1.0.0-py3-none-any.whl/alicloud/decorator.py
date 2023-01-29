import Tea.exceptions
from Tea.exceptions import UnretryableException
from requests.exceptions import SSLError

from pypanda.alicloud.exceptions import *


def has_attrs(obj, attrs: list):
    for attr in attrs:
        if not hasattr(obj, attr):
            return False
        if getattr(obj, attr) is None:
            return False
    return True


def page_reader(nodes=None):
    if nodes is None:
        nodes = []

    def decorator(func):
        def wrapper(*args, **kwargs):
            while True:
                response = func(*args, **kwargs)
                content = response
                if response is not None:
                    for _node in nodes:
                        content = getattr(content, _node, None)
                yield content
                if hasattr(response, 'is_truncated') and response.is_truncated is True:
                    kwargs['marker'] = response.marker
                    continue
                if has_attrs(response, ['page_info']):
                    _pager = response.page_info
                    if _pager.total_count > _pager.page_size * _pager.page_number:
                        kwargs['page_number'] = _pager.page_number + 1
                        continue
                if has_attrs(response, ["page_size", "page_number", "total_count"]):
                    if response.total_count > response.page_size * response.page_number:
                        kwargs['page_number'] = response.page_number + 1
                        if getattr(response, "next_token", None):
                            kwargs['next_token'] = response.next_token
                        continue
                if has_attrs(response, ['next_token', 'max_results', "total_count"]):
                    if response.next_token:
                        kwargs['next_token'] = response.next_token
                        continue
                break

        return wrapper

    return decorator


def tea_request_wrapper(func):
    def wrapper(*args, **kwargs):
        exception = None
        try:
            return func(*args, **kwargs)
        except SSLError as e:
            exception = PleaseRetryError("Network ssl error,please retry")
        except UnretryableException as e:
            exception = PleaseRetryError(e.inner_exception.message)
        except Tea.exceptions.TeaException as e:
            error_code = e.code
            error_code_type = error_code.split('.')[0]
            error_message = e.args[0]["message"]
            if error_code_type in ['EntityNotExist', 'EntityAlreadyExists', 'Throttling']:
                exception = PleaseRetryError({"message": error_message, "code": error_code})
            else:
                exception = e
        if exception is not None:
            raise exception

    return wrapper
