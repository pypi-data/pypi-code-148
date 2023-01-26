from typing import Any, Dict, Iterable, Type, Union

CONTEXT_HEADER_KEY = "x-spymaster-context"
CONTEXT_ID_HEADER_KEY = "x-spymaster-context-id"
JsonType = Union[str, int, float, bool, list, Dict[str, Any], None]
ErrorTypes = Iterable[Type[Exception]]
