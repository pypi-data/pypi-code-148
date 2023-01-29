import pytz
import re

from datetime import datetime
from logging import Logger, Handler
from types import TracebackType
from typing import Any, Iterable


# from https://stackoverflow.com/q/6760685/2789834
class Singleton(type):
    _instances: dict[type, object] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


def find_shortest_indent(text: str | list[str], *, ignore_empty: bool = True, delimiter: str = "\n") -> int:
    """Given a block of text, find the shortest indent in use.
    If there is a line with an indent of 0, skips the loop and returns 0.
    If `ignore_empty` is set, lines that are empty are skipped.
    If a shortest indent can't be determined, returns 0.
    """
    if isinstance(text, str):
        text = text.split(delimiter)

    indent_sizes = []

    for line in text:
        if ignore_empty and line.strip() == "":
            continue

        count = 0
        for char in line:
            if char.isspace():
                count += 1
            else:
                break

        if count == 0:
            return 0

        indent_sizes.append(count)

    if not indent_sizes:
        return 0

    return min(indent_sizes)


def now_utc() -> datetime:
    return datetime.now(tz=pytz.utc)


def relative_date(the_time: int | float | str | datetime) -> str:
    if not the_time:
        return ""

    # convert the_time to a datetime object if it's just a bare "epoch" int / float
    if isinstance(the_time, (int, float)):
        when = datetime.fromtimestamp(float(the_time), pytz.utc)
    elif isinstance(the_time, str):
        when = datetime.fromisoformat(the_time)
    elif isinstance(the_time, datetime):
        when = the_time if the_time.tzinfo else pytz.utc.localize(the_time)
    else:
        raise ValueError(f"Unknown time format: {the_time}")

    now = now_utc()
    if when > now:
        future = True
        diff = when - now
    else:
        future = False
        diff = now - when

    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 2:
        second_diff += 86400 * day_diff
        if second_diff < 60:
            r = f"about {second_diff + (5 - second_diff) % 5} seconds"
        elif second_diff < 300:
            second_diff //= 60
            r = f"about {second_diff} minute{'s'[:second_diff^1]}"
        elif second_diff < 3600:
            second_diff //= 60
            r = f"about {second_diff + (5 - second_diff) % 5} minutes"
        else:
            nearest_hour = round((second_diff + 1800) / 3600)
            r = "about an hour" if nearest_hour == 1 else f"about {nearest_hour} hours"
    else:
        r = f"{day_diff} days"

    return "in " + r if future else r + " ago"


def deduplicate(items: Iterable) -> list:
    """Remove duplicates in an iterable while preserving order"""
    seen = []
    return [x for x in items if not (x in seen or seen.append(x))]


def fix_timestamp(timestamp: str) -> str:
    # convert Z to +00:00 (RFC 3339 format), or change +0000 to +00:00, so datetime.fromisoformat works
    return re.sub(r"\+(\d\d)(\d\d)$", r"+\1:\2", timestamp.replace("Z", "+00:00"))


def strip_mrkdwn(text: str) -> str:
    """Strip Slack-flavored 'mrkdwn' formatting"""
    text = re.sub(r"\*_((?:\S)(?:.*?))_\*", r"\1", text)  # strip *_..._*
    text = re.sub(r"_\*((?:\S)(?:.*?))\*_", r"\1", text)  # strip *_..._*
    text = re.sub(r"([*_])((?:\S)(?:.*?))(?:\1)", r"\2", text)  # strip *...* or _..._
    text = re.sub(r"<(?!!)([^>]+?)(?:\|[^>]+?)?>", r"\1", text)  # strip URLs
    text = re.sub(r"(?:<![^>]+?\|)([^>]+?)(?:>)", r"\1", text)  # strip Slack ! links (<!subteam^SXYZ|@groupname>)
    return text.replace("\n", " • ")


def ensure_slack_ts(ts: str) -> str:
    """Ensure the timestamp is Slack-compatible by adding the '.' if necessary"""
    if not isinstance(ts, str):
        ts = str(ts)
    return ts if "." in ts else ts[:-6] + "." + ts[-6:]


def ensure_db_key_ts(ts: str) -> str:
    """Ensure the timestamp is compatible as an (integer) database key by removing the '.' if necessary"""
    if not isinstance(ts, str):
        ts = str(ts)
    return ts.replace(".", "")


def ensure_at(user_id: str) -> str:
    """Ensure the string starts with an "@" and isn't just a bare slack user ID"""
    return user_id if user_id.startswith("@") else f"@{user_id}"


class Plural:
    """
    Format is ":always/plural", ":always/singular/plural", or ":/singular/plural"
    Any uppercase 'N' is  replaced by the value.
    Examples:
    f"{Plural(count):N tree/s}"
    f"{Plural(count):N repl/y/ies}"
    f"We need {Plural(count):/a cactus/N cacti}."

    based on answers in https://stackoverflow.com/q/21872366/2789834
    """

    def __init__(self, value: Any) -> None:
        self.value = value

    def __format__(self, formatter: str) -> str:
        formatter = formatter.replace("N", str(self.value))
        start, _, suffixes = formatter.partition("/")
        singular, _, plural = suffixes.rpartition("/")
        return f"{start}{singular if self.value == 1 else plural}"


def partial_mask(text: str, keep: int = 4, mask: str = "****") -> str:
    """
    Replace the middle part of `text` with `mask`, keeping up to `keep`
    characters at the beginning and end of the string when possible.
    """
    mask_len = len(mask)

    text_len = len(text)
    if text_len <= mask_len or keep <= 0:
        return mask

    if text_len >= mask_len + keep * 2:
        left_keep = right_keep = keep
    else:
        left_keep = (text_len - mask_len) // 2
        right_keep = left_keep + (text_len - mask_len) % 2

    return text[:left_keep] + mask + text[-right_keep:]


def exception_name(exception: Exception) -> str:
    """
    Return the name of the exception as a string
    """
    return type(exception).__name__


def get_full_class_name(obj: object) -> str:
    """
    Return the full class name of an object
    """
    module = obj.__class__.__module__
    if module is None or module == "builtins":
        return obj.__class__.__name__
    return f"{module}.{obj.__class__.__name__}"


# From the "Logging Cookbook"
# https://docs.python.org/3/howto/logging-cookbook.html
class LoggingContext:
    def __init__(self, logger: Logger, level: int | None = None, handler: Handler | None = None, *, close: bool = True) -> None:
        self.logger = logger
        self.level = level
        self.handler = handler
        self.close = close

    def __enter__(self) -> None:
        if self.level is not None:
            self.old_level = self.logger.level
            self.logger.setLevel(self.level)
        if self.handler:
            self.logger.addHandler(self.handler)

    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None) -> None:
        if self.level is not None:
            self.logger.setLevel(self.old_level)
        if self.handler:
            self.logger.removeHandler(self.handler)
        if self.handler and self.close:
            self.handler.close()
        # implicit return of None => don't swallow exceptions
