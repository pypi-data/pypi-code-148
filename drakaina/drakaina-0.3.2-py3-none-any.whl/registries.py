from inspect import getfullargspec
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional

# Reserved procedure argument names
RESERVED_KWARGS = ("self", "request")


class RPCRegistry:
    """Registry of remote procedures"""

    _remote_procedures: Dict[str, Callable[..., Any]]

    def __init__(self):
        self._remote_procedures = {}

    def register_procedure(
        self,
        procedure: Callable[..., Any],
        name: Optional[str] = None,
        provide_request: Optional[bool] = None,
        metadata: Optional[dict] = None,
    ):
        """Register a function as a remote procedure.

        :param procedure: Registered procedure.
        :type procedure: Callable
        :param name: Procedure name. Default as function name.
        :type name: str
        :param provide_request:
        :type provide_request: bool
        :param metadata: Metadata that can be processed by middleware.
        :type metadata: dict

        """

        procedure_name = procedure.__name__ if name is None else name
        procedure.__rpc_name = procedure_name
        procedure.__rpc_provide_request = provide_request
        procedure.__rpc_meta = metadata
        procedure.__rpc_args = [
            a
            for a in getfullargspec(procedure).args
            if a not in RESERVED_KWARGS
        ]

        self._remote_procedures[procedure_name] = procedure

    def __getitem__(self, item) -> Optional[Callable]:
        return self._remote_procedures.get(item)

    def __setitem__(self, key, value):
        self.register_procedure(procedure=value, name=key)

    def __delitem__(self, key):
        del self._remote_procedures[key]

    def __len__(self):
        return len(self._remote_procedures)

    def __iter__(self):
        return iter(self._remote_procedures)

    def get(self, key, default: Callable = None) -> Optional[Callable]:
        return self._remote_procedures.get(key, default)
