from typing import Any, Dict, Iterable, Type, TypeVar, Union

from the_spymaster_util.http.errors import ApiError

CONTEXT_HEADER_KEY = "x-spymaster-context"
CONTEXT_ID_HEADER_KEY = "x-spymaster-context-id"
JsonType = Union[str, int, float, bool, list, Dict[str, Any], None]
E = TypeVar("E", bound=ApiError)
ErrorTypes = Iterable[Type[E]]
ErrorCodeMapping = Dict[str, Type[E]]
