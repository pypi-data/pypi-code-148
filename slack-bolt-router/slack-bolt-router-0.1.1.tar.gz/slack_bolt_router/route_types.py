"""
Contains the RouteTypes class that contains names of all route types that can be
used in the Slack Application.

(c) Dmytro Hoi <code@dmytrohoi.com>, 2021 | MIT License
"""
from enum import EnumMeta
from typing import Tuple


__all__ = ("RouteTypes",)


class RouteTypes(EnumMeta):
    """All the Slack-Bolt routes."""
    STEP = "step"
    EVENT = "event"
    MESSAGE = "message"
    COMMAND = "command"
    SHORTCUT = "shortcut"
    GLOBAL_SHORTCUT = "global_shortcut"
    MESSAGE_SHORTCUT = "message_shortcut"
    ACTION = "action"
    BLOCK_ACTION = "block_action"
    ATTACHMENT_ACTION = "attachment_action"
    DIALOG_SUBMISSION = "dialog_submission"
    DIALOG_CANCELLATION = "dialog_cancellation"
    VIEW = "view"
    VIEW_SUBMISSION = "view_submission"
    VIEW_CLOSED = "view_closed"
    OPTIONS = "options"
    BLOCK_SUGGESTION = "block_suggestion"
    DIALOG_SUGGESTION = "dialog_suggestion"

    @classmethod
    def all_routes(cls) -> Tuple[str]:
        """
        Get all routes that can be applied to the Slack-Bolt App.

        :return Tuple[str]: tuple of the route names
        """
        return tuple(
            value
            for key, value in cls.__dict__.items()
            if not key.startswith("_")
        )
