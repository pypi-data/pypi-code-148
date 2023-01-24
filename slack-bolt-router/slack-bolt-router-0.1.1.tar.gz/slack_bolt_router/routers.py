"""
Contains the Routers class that allow to manage routers from one place.

(c) Dmytro Hoi <code@dmytrohoi.com>, 2021 | MIT License
"""
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from slack_bolt.app.app import App
    from .router import Router


__all__ = ("Routers",)


class Routers:
    """The singletone class to store all routes that uses in the Application."""
    _routers: List['Router'] = []

    def __new__(cls, routers: List['Router']):
        """
        Add routers directly to routers list to apply many routers by one
        method.

        ..note::
            routers = Routers([first_router, second_router])
            routers.apply_to(app)

        :param list[Router] routers: routers that should be added
        """
        cls._routers = routers
        return super().__new__(cls)

    @classmethod
    def add_router(cls, router: 'Router'):
        """
        Add single router to list of routers.

        :param 'Router' router: the desired router that should be added
        """
        cls._routers.append(router)

    @classmethod
    def apply_to(cls, bot: 'App'):
        """
        Apply all routes to the Slack-Bolt Application.

        ..code::
            from slack_bolt.app.app import App
            from slack_bolt_router import Routers

            bot = App()

            Routers.apply_to(bot)

        :param App bot: slack bolt application
        """
        for router in cls._routers:
            router.apply_to(bot)
