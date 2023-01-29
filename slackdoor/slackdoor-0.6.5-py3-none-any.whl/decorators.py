import asyncio
import inspect
import re

from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Pattern


@dataclass(slots=True)
class PluginMetadata:
    events: list[str] = field(default_factory=list)
    message_regexps: list[Pattern[str]] = field(default_factory=list)
    link_shared_regexps: list[Pattern[str]] = field(default_factory=list)


def event(slack_event: str) -> Callable[..., Any]:
    """Handle a specific Slack event

    Enables a plugin to receive Slack events of the specified type.

    Decorators can be stacked on a plugin method if it can process
    multiple event types.

    .. _Slack events: https://api.slack.com/events

    :param slack_event_type: type of event the method will process.
    :return: wrapped method
    """

    def event_decorator(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Callable[..., Any]:
        func.metadata = getattr(func, "metadata", PluginMetadata())
        func.metadata.events.append(slack_event)
        return ignore_unmatched_kwargs(func, *args, **kwargs)

    return event_decorator


def message(regex: str, flags: re.RegexFlag | None = re.IGNORECASE) -> Callable[..., Any]:
    """Handle Slack 'message' events that match a regex pattern

    Enables a plugin method to receive "message" events that match a regex.
    Named groups can be used in the regex pattern to extract specific parts
    of the message, which are then passed to the plugin as keyword args.

    If the regex containts "(?#Multi)" then the plugin is "multi-match aware"
    and the dispatcher will pass down multple occurrences of the regex in the
    same message as a list (of named regex matches).

    A plugin method can be decorated multiple times to match multiple
    regexs.

    :param regex: regex pattern to listen for
    :param flags: regex flags to apply when matching; defaults to re.IGNORECASE.
                  use "flags=None" to force case-sensitive matching
    :return: wrapped method
    """

    def message_decorator(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Callable[..., Any]:
        func.metadata = getattr(func, "metadata", PluginMetadata())
        regex_compiled = re.compile(regex, flags) if flags else re.compile(regex)
        func.metadata.message_regexps.append(regex_compiled)
        return ignore_unmatched_kwargs(func, *args, **kwargs)

    return message_decorator


def message_callback(func: Callable[..., Any]) -> Callable[..., Any]:
    """Register a message callback handler.

    Enables a plugin to receive information about bot-generated messages.

    :return: wrapped method
    """

    def message_callback_decorator(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Callable[..., Any]:
        func.metadata = getattr(func, "metadata", PluginMetadata())
        func.metadata.events.append("message_callback")
        return ignore_unmatched_kwargs(func, *args, **kwargs)

    return message_callback_decorator(func)


def link_shared(url_regex: str) -> Callable[..., Any]:
    """Handle Slack 'link_shared' events for a matching URL

    Enables a plugin method to receive "link_shared" events that match url_regex.
    Named groups can be used in the regex pattern to extract specific parts of the
    URL passed by Slack for unfurling, which are then passed to the plugin as
    keyword args.

    A plugin method can be decorated multiple times to match multiple regexes.

    :param url_regex: regex pattern of URL to match
    :return: wrapped method
    """

    def link_shared_decorator(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Callable[..., Any]:
        func.metadata = getattr(func, "metadata", PluginMetadata())
        func.metadata.link_shared_regexps.append(re.compile(url_regex, re.IGNORECASE))
        return ignore_unmatched_kwargs(func, *args, **kwargs)

    return link_shared_decorator


def ignore_unmatched_kwargs(func: Callable[..., Any]) -> Callable[..., Any]:
    """Allow function to be called with extra kwargs... but if the
    function already has a catch-all **kwargs, don't do anything.

    Inspired by https://stackoverflow.com/a/63787701/2789834
    """
    if any(param.kind == inspect.Parameter.VAR_KEYWORD for param in inspect.signature(func).parameters.values()):
        return func

    async def helper(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        # For each keyword arguments recognized by 'func', use the binding from the received **kwargs
        filtered_kwargs = {
            name: kwargs[name]
            for name, param in inspect.signature(func).parameters.items()
            if (param.kind is inspect.Parameter.KEYWORD_ONLY or param.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD)
            and name in kwargs
        }
        return await helper(func, *args, **filtered_kwargs)

    return wrapper
