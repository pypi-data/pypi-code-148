from typing import Any
from typing import Callable
from typing import Optional
from typing import TypeVar

from drakaina.registries import RPCRegistry

__all__ = ("remote_procedure", "RPCRegistry", "rpc_registry")

rpc_registry = RPCRegistry()


def remote_procedure(*args, **kwargs) -> Callable:
    """Decorator allow wrap function and define it as remote procedure.

    Options:

    name: str
        Procedure name. Default as function name.
    registry: RPCRegistry
        Procedure registry custom object
    provide_request: bool
        Provide a request object (from the transport layer).
    metadata: dict[str, Any]
        Metadata that can be processed by middleware.

    """

    def create_decorator(
        name: Optional[str] = None,
        registry: Optional[RPCRegistry] = None,
        provide_request: Optional[bool] = None,
        metadata: Optional[dict[str, Any]] = None,
        **options,
    ) -> Callable:
        """Takes the parameters of the wrapped function and returns a decorator
        for it.
        """
        T = TypeVar("T")
        _registry = registry or rpc_registry

        def decorator(procedure: T) -> T:
            """Returns a registered procedure"""
            _registry.register_procedure(
                procedure,
                name=name,
                provide_request=provide_request,
                metadata={**(metadata or {}), **options},
            )
            return procedure

        return decorator

    if len(args) == 1 and callable(args[0]):
        return create_decorator()(args[0])
    return create_decorator(*args, **kwargs)
