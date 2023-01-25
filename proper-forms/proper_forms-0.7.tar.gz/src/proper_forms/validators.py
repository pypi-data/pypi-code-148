from __future__ import annotations

import datetime
import typing as t
from abc import ABCMeta, abstractmethod
from itertools import groupby

if t.TYPE_CHECKING:
    TValidateResult = t.Literal[True] | tuple[t.Literal[False], str]


__all__ = (
    "After",
    "AfterNow",
    "Before",
    "BeforeNow",
    "Confirmed",
    "InRange",
    "LessThan",
    "LongerThan",
    "MoreThan",
    "ShorterThan",
)


class Comparable(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other: t.Any) -> bool:
        ...


class Sizeable(metaclass=ABCMeta):
    @abstractmethod
    def __len__(self) -> int:
        ...


def validate_values(
    values: list[t.Any],
    test: t.Callable,
    message: str,
) -> "TValidateResult":
    for value in values:
        if not test(value):
            return False, message
    return True


class After:
    """Validates than the date happens after another.

    date (date|datetime):
        The soonest valid date.

    message (str):
        Error message to raise in case of a validation error.
    """

    message = "Enter a valid date after %s."

    def __init__(self, dt: datetime.date, message: str | None = None) -> None:
        assert isinstance(dt, datetime.date)
        if not isinstance(dt, datetime.datetime):
            dt = datetime.datetime(dt.year, dt.month, dt.day)
        self.dt = dt
        if message is None:
            message = self.message % "{}-{:02d}-{:02d}".format(
                dt.year, dt.month, dt.day
            )
        self.message = message

    def __call__(self, values: list[datetime.date]) -> "TValidateResult":
        def test(value):
            assert isinstance(value, datetime.date)
            if not isinstance(value, datetime.datetime):
                value = datetime.datetime(value.year, value.month, value.day)
            return value >= self.dt

        return validate_values(values, test, self.message)


class AfterNow:
    """Validates than the date happens after now.
    This will work with both date and datetime values.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Enter a valid date in the future."

    def __init__(self, message: str | None = None) -> None:
        if message is not None:
            self.message = message

    def __call__(self, values: list[datetime.date]) -> "TValidateResult":
        v = After(datetime.datetime.utcnow(), self.message)
        return v(values)


class Before:
    """Validates than the date happens before another.

    date (date|datetime):
        The latest valid date.

    message (str):
        Error message to raise in case of a validation error.
    """

    message = "Enter a valid date before %s."

    def __init__(self, dt: datetime.date, message: str | None = None) -> None:
        assert isinstance(dt, datetime.date)
        if not isinstance(dt, datetime.datetime):
            dt = datetime.datetime(dt.year, dt.month, dt.day)
        self.dt = dt
        if message is None:
            message = self.message % "{}-{:02d}-{:02d}".format(
                dt.year, dt.month, dt.day
            )
        self.message = message

    def __call__(self, values: list[datetime.date]) -> "TValidateResult":
        def test(value):
            assert isinstance(value, datetime.date)
            if not isinstance(value, datetime.datetime):
                value = datetime.datetime(value.year, value.month, value.day)
            return value <= self.dt

        return validate_values(values, test, self.message)


class BeforeNow:
    """Validates than the date happens before now.
    This will work with both date and datetime values.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Enter a valid date in the past."

    def __init__(self, message: str | None = None) -> None:
        if message is not None:
            self.message = message

    def __call__(self, values: list[datetime.date]) -> "TValidateResult":
        v = Before(datetime.datetime.utcnow(), self.message)
        return v(values)


class Confirmed:
    """Validates that a value is identical every time has been repeated.
    Classic use is for password confirmation fields.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Values doesn't match."

    def __init__(self, message: str | None = None) -> None:
        if message is not None:
            self.message = message

    def __call__(self, values: list[t.Any]) -> "TValidateResult":
        if len(values) < 2:
            return False, self.message
        g = groupby(values)
        if next(g, True) and not next(g, False):
            return True
        return False, self.message


class InRange:
    """Validates that a value is between a minimum and maximum value.
    This will work with integers, floats, decimals and strings.

    minval:
        The minimum value acceptable.

    maxval:
        The maximum value acceptable.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Number must be between %s and %s."

    def __init__(self, minval: Comparable, maxval: Comparable, message: str | None = None) -> None:
        self.minval = minval
        self.maxval = maxval
        if message is None:
            message = self.message % (minval, maxval)
        self.message = message

    def __call__(self, values: list[Comparable]) -> "TValidateResult":
        def test(value):
            if value < self.minval:
                return False
            if value > self.maxval:
                return False
            return True

        return validate_values(values, test, self.message)


class LessThan:
    """Validates that a value is less or equal than another.
    This will work with integers, floats, decimals and strings.

    value:
        The maximum value acceptable.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Number must be less than %s."

    def __init__(self, value: Comparable, message: str | None = None) -> None:
        self.value = value
        if message is None:
            message = self.message % (value,)
        self.message = message

    def __call__(self, values: list[Comparable]) -> "TValidateResult":
        def test(value):
            return value <= self.value

        return validate_values(values, test, self.message)


class MoreThan:
    """Validates that a value is greater or equal than another.
    This will work with any integers, floats, decimals and strings.

    value:
        The minimum value acceptable.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Number must be greater than %s."

    def __init__(self, value: Comparable, message: str | None = None) -> None:
        self.value = value
        if message is None:
            message = self.message % (value,)
        self.message = message

    def __call__(self, values: list[Comparable]) -> "TValidateResult":
        def test(value):
            return value >= self.value

        return validate_values(values, test, self.message)


class LongerThan:
    """Validates the length of a value is longer or equal than minimum.

    length (int):
        The minimum required length of the value.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Field must be at least %s character long."

    def __init__(self, length: int, message: str | None = None) -> None:
        assert isinstance(length, int)
        self.length = length
        if message is None:
            message = self.message % (length,)
        self.message = message

    def __call__(self, values: list[Sizeable]) -> "TValidateResult":
        def test(value):
            return len(value) >= self.length

        return validate_values(values, test, self.message)


class ShorterThan:
    """Validates the length of a value is shorter or equal than maximum.

    length (int):
        The maximum allowed length of the value.

    message (str):
        Error message to raise in case of a validation error.

    """

    message = "Field cannot be longer than %s characters."

    def __init__(self, length: int, message: str | None = None) -> None:
        assert isinstance(length, int)
        self.length = length
        if message is None:
            message = self.message % (length,)
        self.message = message

    def __call__(self, values: list[Sizeable]) -> "TValidateResult":
        def test(value):
            return len(value) <= self.length

        return validate_values(values, test, self.message)
