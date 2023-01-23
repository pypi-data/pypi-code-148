# Created by Noé Cruz | Zurckz 22 at 01/08/2022
# See https://www.linkedin.com/in/zurckz
import dataclasses
from functools import wraps
from inspect import isclass, signature
from typing import Callable, Optional, Any, Tuple, TypeVar
from zpy.logger import ZLogger
from zpy.utils.values import if_null_get
from zpy.app import zapp_context as ctx
import time

T = TypeVar("T")


@dataclasses.dataclass
class DLazy:
    type: Any
    initializer: Callable[[Any], Any]


class DIContainer:
    """
    Basic Dependency Container
    """

    def __init__(self, timeit: bool = False, x_logger: ZLogger = None,
                 notifier: Callable[[Any, Optional[Any]], None] = None) -> None:
        self.container: dict = dict()
        self.logger: ZLogger = if_null_get(x_logger, ctx().logger)
        self.timeit: bool = timeit
        self.notifier: Callable[[Any, Optional[Any]], None] = notifier
        self.throw_ex = True
        self.error_message_prefix = "Fatal"
        self.max_time_allowed = 5

    def with_notifier(self, notifier):
        self.notifier = notifier

    @classmethod
    def create(cls, timeit: bool = False, logger: ZLogger = None) -> 'DIContainer':
        return cls(timeit, logger)

    def setup(self, init_fn: Callable[['DIContainer'], None]) -> 'DIContainer':
        try:
            te = time.time()
            init_fn(self)
            ts = time.time()
            self.logger.info(f"🚀 Dependencies loaded successfully... {(ts - te) * 1000:2.2f} ms.")
        except Exception as e:
            self.logger.err("Failed to load dependencies...")
            if self.notifier:
                self.notifier(f"{self.error_message_prefix} - Failed to load dependencies: {str(e)}")
            if self.throw_ex:
                raise
        return self

    def __getitem__(self, item: T) -> T:
        return self.get(item)

    def __setitem__(self, key, value):
        self.container[key] = value

    def register(self, x_type: Any, value: Any) -> None:
        """
        Register object or instance of any type in the container.
        @param x_type: Object type to register
        @param value: instance or value to register
        @return: None
        """
        self[x_type] = value

    def factory_register(self, x_type: Any, initializer: Callable[[Any], Any]) -> None:
        """
        Register object or instance of any type in the container using factory strategy.
        This method evaluates the load time, if the load time exceeds the allowed time, the notifier is invoked
        @param x_type: Object type to register
        @param initializer: Loader function
        @return: None
        """
        self[x_type] = self.__timeit__(self.timeit, initializer, x_type, self)

    def lazy_register(self, x_type, initializer: Callable[[Any], Any]) -> None:
        """
        Register object or instance of any type in the container using lazy strategy.
        This method evaluates the load time, if the load time exceeds the allowed time, the notifier is invoked
        @param x_type: Object type to register
        @param initializer: Loader function
        @return: None
        """
        self[x_type] = DLazy(x_type, initializer)

    def get(self, x_type: T, default=None) -> Optional[T]:
        """
        Retrieve object registered in the container
        @param x_type: Object type
        @param default: If object not registered return this value
        @return: Optional object registered or default value
        """
        dependency = self.container.get(x_type, default)

        if isinstance(dependency, DLazy):
            self.container[x_type] = self.__timeit__(self.timeit, dependency.initializer, x_type, self)
            return self.container[x_type]

        return dependency

    def take(self, key: Any, x_type: T, default=None) -> Optional[T]:
        """
        Retrieve object registered in the container
        @param key: key used in registration
        @param x_type: type of value registered
        @param default: if the value registered not exist this value will be returned
        @return: value registered or default
        """
        return self.get(key, default)

    def __timeit__(self, timeit: bool, fn: Any, x_type: Any, *args):
        if not timeit:
            return fn(args[0])
        te = time.time()
        result = fn(args[0])
        ts = time.time()
        taken = ts - te
        self.logger.info(f"Dependency load time: {x_type} :: {taken * 1000:2.2f} ms.")
        if taken >= self.max_time_allowed:
            msg = f"The dependency: {str(x_type)} is exceeding the allowed time. Taken: {taken:2.2f} - Max: {self.max_time_allowed}s."
            self.logger.warn(msg)
            if self.notifier:
                self.notifier(msg)
        return result

    def __getattr__(self, item: T) -> T:
        return self.get(item)


zdi = DIContainer().create()


def populate(initializer, container):
    print(initializer)
    parameters_name: Tuple[str, ...] = tuple(signature(initializer).parameters.keys())
    parameters: Tuple[str, ...] = tuple(signature(initializer).parameters.items())
    print(parameters_name)
    print(parameters)

    @wraps(initializer)
    def _decorated(*args, **kwargs):
        # all arguments were passed
        # if len(args) == len(parameters_name):
        #    return service(*args, **kwargs)

        # if parameters_name == tuple(kwargs.keys()):
        #    return service(**kwargs)

        # all_kwargs = _resolve_kwargs(args, kwargs)
        return initializer(1, 2, 3)

    return _decorated


def inject(container: DIContainer = zdi):
    def _decorator(_service: Any) -> Any:
        if isclass(_service):
            setattr(
                _service,
                "__init__",
                populate(getattr(_service, "__init__"), container)
            )
            return _service

        return _service

    return _decorator
