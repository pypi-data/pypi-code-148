class Router:
    """Class for registering methods"""

    def __init__(self):
        self._handlers: dict[str, callable] = {}

    def method(self, func: callable) -> callable:
        """Register handler"""
        self._handlers[func.__name__] = func
        return func

    def get_handler(self, name: str) -> callable | None:
        """Return handler function by its name"""
        return self._handlers.get(name, None)
