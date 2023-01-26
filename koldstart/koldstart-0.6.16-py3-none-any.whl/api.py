from __future__ import annotations

import os
from dataclasses import dataclass, field, replace
from functools import partial, wraps
from typing import Any, Callable, ClassVar, Dict, Generic, TypeVar, cast

import dill
import isolate
from isolate.backends.settings import DEFAULT_SETTINGS
from isolate.connections import PythonIPC
from koldstart.sdk import (
    Credentials,
    HostedRunState,
    KoldstartClient,
    KoldstartConnection,
    MachineRequirements,
    get_default_credentials,
)

ReturnT = TypeVar("ReturnT")
BasicConfig = Dict[str, Any]
_UNSET = object()


@dataclass
class KoldstartError(Exception):
    message: str


@dataclass
class InternalKoldstartError(Exception):
    ...


@dataclass
class Host:
    """The physical environment where the isolated code
    is executed."""

    _SUPPORTED_KEYS: ClassVar[frozenset[str]] = frozenset()

    @classmethod
    def parse_options(cls, **config: Any) -> Options:
        """Split the given set of options into host and
        environment options."""

        options = Options()
        for key, value in config.items():
            if key in cls._SUPPORTED_KEYS:
                options.host[key] = value
            else:
                options.environment[key] = value

        return options

    def run(
        self,
        func: Callable[..., ReturnT],
        options: Options,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> ReturnT:
        """Run the given function in the isolated environment."""
        raise NotImplementedError


@dataclass
class LocalHost(Host):
    # The environment which provides the default set of
    # packages for isolate agent to run.
    _AGENT_ENVIRONMENT = isolate.prepare_environment(
        "virtualenv",
        requirements=[f"dill=={dill.__version__}"],
    )

    def run(
        self,
        func: Callable[..., ReturnT],
        options: Options,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> ReturnT:
        settings = replace(DEFAULT_SETTINGS, serialization_method="dill")
        environment = isolate.prepare_environment(
            **options.environment,
            context=settings,
        )
        with PythonIPC(
            environment,
            environment.create(),
            extra_inheritance_paths=[self._AGENT_ENVIRONMENT.create()],
        ) as connection:
            executable = partial(func, *args, **kwargs)
            return connection.run(executable)


KOLDSTART_DEFAULT_URL = os.getenv("KOLDSTART_HOST", "api.alpha.fal.ai:443")
KOLDSTART_DEFAULT_MACHINE_TYPE = "XS"


# TODO: Should we build all these in fal/dbt-fal packages instead?
@dataclass
class KoldstartHost(Host):
    _SUPPORTED_KEYS = frozenset({"machine_type", "keep_alive", "setup_function"})

    url: str = KOLDSTART_DEFAULT_URL
    credentials: Credentials = field(default_factory=get_default_credentials)

    @property
    def _connection(self) -> KoldstartConnection:
        client = KoldstartClient(self.url, self.credentials)
        return client.connect()

    def run(
        self,
        func: Callable[..., ReturnT],
        options: Options,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> ReturnT:
        environments = [self._connection.define_environment(**options.environment)]

        machine_type = options.host.pop("machine_type", KOLDSTART_DEFAULT_MACHINE_TYPE)
        machine_requirements = MachineRequirements(machine_type=machine_type)

        return_value = _UNSET
        for partial_result in self._connection.run(
            partial(func, *args, **kwargs),
            environments,
            machine_requirements=machine_requirements,
        ):
            for log in partial_result.logs:
                print(str(log))

            if partial_result.status.state is not HostedRunState.IN_PROGRESS:
                state = partial_result.status.state
                if state is HostedRunState.INTERNAL_FAILURE:
                    raise InternalKoldstartError(
                        "An internal failure occurred while performing this run."
                    )
                elif state is HostedRunState.SUCCESS:
                    return_value = partial_result.result
                else:
                    raise NotImplementedError("Unknown state: ", state)

        if return_value is _UNSET:
            raise InternalKoldstartError("The input function did not return any value.")

        return cast(ReturnT, return_value)


@dataclass
class Options:
    host: BasicConfig = field(default_factory=dict)
    environment: BasicConfig = field(default_factory=dict)


_DEFAULT_HOST = KoldstartHost()


def isolated(
    kind: str = "virtualenv",
    *,
    host: Host = _DEFAULT_HOST,
    **config: Any,
) -> Callable[[Callable[..., ReturnT]], IsolatedFunction[ReturnT]]:
    options = host.parse_options(kind=kind, **config)

    def wrapper(func: Callable[..., ReturnT]) -> IsolatedFunction[ReturnT]:
        proxy = IsolatedFunction(
            host=host,
            func=func,
            options=options,
        )
        return wraps(func)(proxy)

    return wrapper


@dataclass
class IsolatedFunction(Generic[ReturnT]):
    host: Host
    func: Callable[..., ReturnT]
    options: Options

    def __call__(self, *args, **kwargs) -> ReturnT:
        return self.host.run(
            self.func,
            self.options,
            args=args,
            kwargs=kwargs,
        )

    def on(self, host: Host | None = None, **config: Any) -> IsolatedFunction[ReturnT]:
        host = host or self.host
        if isinstance(host, type(self.host)):
            previous_host_options = self.options.host
        else:
            previous_host_options = {}

        new_options = host.parse_options(
            **self.options.environment,
            **previous_host_options,
            **config,  # The order here is important since the new config
            # Should take precedence over the previous one.
        )
        return replace(
            self,
            host=host,
            options=new_options,
        )
