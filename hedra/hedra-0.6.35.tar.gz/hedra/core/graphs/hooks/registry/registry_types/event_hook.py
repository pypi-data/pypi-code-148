from typing import Coroutine, Dict, Any, Callable, Awaitable, Type, Optional
from hedra.core.graphs.hooks.hook_types.hook_type import HookType
from .hook import Hook


class EventHook(Hook):

    def __init__(
        self, 
        name: str, 
        shortname: str, 
        call: Callable[..., Awaitable[Any]], 
        *names: str,
        pre: bool=False,
        key: Optional[str]=None
    ) -> None:
        super().__init__(
            name, 
            shortname, 
            call, 
            hook_type=HookType.EVENT
        )

        self.call: Type[self._call] = self._call
        self.names = list(set(names))
        self.pre = pre
        self.key = key
        self.events: Dict[str, Coroutine] = {}