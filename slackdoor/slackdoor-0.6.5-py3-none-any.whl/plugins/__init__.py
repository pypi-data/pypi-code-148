from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Pattern

from door.plugins.base import DoorBasePlugin


@dataclass(slots=True)
class PluginHandler:
    class_inst: DoorBasePlugin
    class_name: str
    fn_name: str
    function: Callable[..., Awaitable[Any]]
    regex: Pattern[str] | None = None
    url_regex: Pattern[str] | None = None
