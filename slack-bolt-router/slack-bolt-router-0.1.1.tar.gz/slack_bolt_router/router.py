"""
Contains the Router class that allow to collect and manage routes for
the Slack Application.

(c) Dmytro Hoi <code@dmytrohoi.com>, 2021-2023 | MIT License
"""
from typing import Callable, Dict, List, Optional, Tuple, TYPE_CHECKING
from logging import Logger, getLogger

from .exceptions import InvalidRouteTypeNameError
from .routers import Routers

if TYPE_CHECKING:
    from slack_bolt.app.app import App


__all__ = ('Router',)


class Router:
    """The helper class to register and apply router to the Slack-Bolt App."""
    _routes: Dict[Tuple[str, str], Callable]
    _middlewares: Dict[Tuple[str, str], List[Callable]]

    def __init__(self, *, logger: Optional[Logger] = None):
        """
        Create instance of Router class.

        ..note::
            Your logger can be passed by using keyword argument `logger`.

        :param Optional[Logger] logger: custom logger for current router
        """
        self._logger = logger or getLogger(f"router:{__name__}")
        self._routes = {}
        self._middlewares = {}

        # NOTE: Add router to Routers singletone to apply all routers in one
        Routers.add_router(self)

    def register(self, type: str, id: Optional[str] = None):
        """
        The decorator function to register route.

        ..code::
            from slack_bolt_router import Router

            router = Router()

            @router.register('view')
            def example_submit(ack):
                ack()

        :param str type: the type of route (all types can be found in
            `routes.RouteTypes`)
        :param Optional[str] id: unique identifier for this route, in case of
            None the name of handler function will be passed as identifier
        """
        def __call__(func):
            self.add(func, type=type, id=id)
            return func

        return __call__

    def add(
        self,
        handler: Callable,
        type: str,
        id: Optional[str] = None,
        middlewares: Optional[List[Callable]] = None,
    ) -> bool:
        """
        Add new route for SlackBot.

        ..code::
            from slack_bolt_router import Router

            router = Router()

            def example_submit(ack):
                ack()

            router.add(example_submit, "view")

        :param Callable handler: the reference to function that handles current
        :param str type: the type of route (all types can be found in
            `routes.RouteTypes`)
        :param Optional[str] id: unique identifier for this route, in case of
            None the name of handler function will be passed as identifier
        :param Optional[List[Callable]] middlewares: the desired list of
            middlewares for routes, defaults to None
        :raise ValueError: the same identifier found in routes
        """
        if id is None:
            id = handler.__name__

        if (id, type) in self._routes:
            raise ValueError(f"The same {id=} and {type=} found!")

        self._routes[(id, type)] = handler
        if middlewares:
            self._middlewares[(id, type)] = middlewares
        return True

    def apply_to(self, bot: 'App') -> bool:
        """
        Apply routes to the Slack-Bolt Application.

        ..code::
            from slack_bolt.app.app import App
            from slack_bolt_router import Router

            bot = App()

            router = Router()
            router.add(lambda ack: ack(), "view", "example_submit")

            router.apply_to(bot)

        :param App bot: slack bolt application
        :return bool: status of router applying
        :raise InvalidRouteTypeName: the invalid name of route type passed to
            router
        """
        for (id, type), func in self._routes.items():
            middlewares = self._middlewares.get((id, type))

            app_route_func = getattr(bot, type, None)
            if app_route_func is None:
                raise InvalidRouteTypeNameError(
                    f"Invalid the route {type=} passed to Router for "
                    f"'{func.__name__}' function"
                )

            app_route_func(id, middleware=middlewares)(func)

        self._logger.info(
            f"Routes has been applied to SlackBolt App: {len(self._routes)}"
        )
        return True
