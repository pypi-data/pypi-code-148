from typing import Any, Dict, Optional

from viburnum.application.base import Handler


def handler_config(
    memory: Optional[int] = None,
    timeout: Optional[int] = None,
    reserved_concurrent_executions: Optional[int] = None,
):
    """Set configuration for specific lambda.

    Args:
        memory (Optional[int], optional): memory size in MB. Defaults to value provided in Configuration.
        timeout (Optional[int], optional): lambda timeout in seconds. Defaults to value provided in Configuration.
        reserved_concurrent_executions (Optional[int], optional): number of reserved concurrent executions. Defaults to value provided in Configuration.
    """

    def wraper(handler: Handler) -> Handler:
        handler.memory = memory
        handler.timeout = timeout
        handler.reserved_concurrent_executions = reserved_concurrent_executions
        return handler

    return wraper


def inject_variables(env_variables: Dict[str, Any]):
    """Inject environment variables for specific lambda.

    Args:
        env_variables (Dict[str, Any]): dict with variables
    """

    def wraper(handler: Handler) -> Handler:
        handler.env_variables.update(env_variables)
        return handler

    return wraper
