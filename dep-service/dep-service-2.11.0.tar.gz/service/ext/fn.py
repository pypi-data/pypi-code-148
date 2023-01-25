"""Service helpers."""

from typing import Any, List, Tuple, Set, Union, Dict, Mapping
from datetime import datetime, date, time
from dateutil import parser
from more_itertools import consecutive_groups
from urllib.parse import unquote

from spec import Spec
from fastapi import HTTPException


def str_to_bool(any_str: str) -> bool:
    """Str to bool."""
    true_cases = ('1', 't', 'y')
    for case in true_cases:
        if case in str(any_str).lower():
            return True


def url_query(
    url: str,
    params: Dict[str, Any],
) -> str:
    """Url query from passed options."""
    _query = ''.join([
        f'{param_name}={param_value}&'
        for param_name, param_value in params.items()
    ])
    return f'{url}?{_query}'


def range_to_list(ranges: str) -> Set[str]:
    """Splits str to array of digits.

    Example input ranges: 1,10-12,20,30-33,40
    Example output array: [1, 10, 11, 12, 20, 30, 31, 32, 33, 40]

    """

    fetched_list: List = []
    seats = ''.join(ranges.split())
    for seat in seats.split(','):
        if seat.isdigit():
            fetched_list.append(seat)
        else:
            try:
                start, finish = map(int, seat.split('-'))
                fetched_list += [
                    str(list_item)
                    for list_item in range(start, finish + 1)
                ]
            except (TypeError, ValueError):
                raise HTTPException(400, 'Invalid query range')

    return set(fetched_list)


def list_to_range(array: List[str]) -> str:
    """Joins array to ranges.

    Example input: [1, 10, 11, 12, 20, 30, 31, 32, 33, 40]
    Example output: 1,10-12,20,30-33,40

    """

    fetched_list: List = []
    for group in consecutive_groups(sorted(map(int, array))):
        group = list(group)
        if len(group) == 1:
            fetched_list.append(f'{group[0]}')
        else:
            fetched_list.append(f'{group[0]}-{group[-1]}')
    return ','.join(fetched_list)


def locale_from_lang(lang: str, spec: Spec) -> str:
    """Get locale from lang."""

    for locale in spec.i18n.locales:
        if str(locale).lower().startswith(lang.lower()):
            return locale


def utc_clean(dt: datetime) -> Union[datetime, None]:
    """Clean date for utc."""
    if not dt:
        return

    _n = dt.replace(microsecond=0)
    _n.replace(tzinfo=None)
    return _n


def date_str_to_timestamp(dt: str) -> Union[int, None]:
    """Datetime str to timestamp."""
    if not dt:
        return
    obj = parser.isoparse(dt)
    return round(obj.timestamp())


def timestamp(dt: datetime) -> Union[int, None]:
    """Utc datetime to timestamp."""
    return dt.timestamp() if dt else None


def current_stamp() -> int:
    """Current unix timestamp."""
    return round(datetime.now().timestamp())


def dt_from_ts(ts: int, spec: Spec) -> datetime:
    """Datetime from unix timestamp."""
    if ts:
        return datetime.fromtimestamp(ts, tz=spec.tz)
    # return datetime.fromtimestamp(ts, spec.tz).strftime('%Y-%m-%d %H:%M:%S')


def format_ts(ts: int, spec: Spec) -> str:
    """Formatted unix time stamp as verbose str."""
    if ts:
        return dt_from_ts(ts, spec=spec).isoformat()


def ts_split(
    ts: int,
    spec: Spec,
) -> Tuple[Union[date, None], Union[time, None]]:
    """Split timestamp unix to date and time tuple."""

    if not ts or not isinstance(ts, int):
        return None, None

    dt = datetime.fromtimestamp(ts, tz=spec.tz)
    return dt_split(dt)


def dt_split(dt: datetime) -> Tuple[Union[date, None], Union[time, None]]:
    """Split datetime to date and time tuple."""

    if not dt or not isinstance(dt, datetime):
        return None, None

    _date = date(year=dt.year, month=dt.month, day=dt.day)
    _time = time(hour=dt.hour, minute=dt.minute, second=dt.second)
    return _date, _time


def dt_join(date: str, time: str) -> Union[datetime, None]:  # noqa
    """Join date and time, like 2022-12-04, 02:04:34 to datetime."""
    try:
        return datetime.combine(
            date=datetime.strptime(date, '%Y-%m-%d').date(),
            time=datetime.strptime(time, '%H:%M:%S').time(),
            tzinfo=None,
        )
    except Exception as _any_exc:  # noqa
        pass


def int_list(string: str) -> Union[List[int], None]:
    """List int from text string."""

    if not string:
        return

    if ',' in string:
        try:
            return [
                int(num)
                for num in string.split(',')
            ]
        except Exception as _fault:  # noqa
            return

    try:
        return [int(string)]
    except Exception as _last_fault:  # noqa
        return


def chunked(items, n) -> List[List[Any]]:
    """Yield successive n-sized chunks from items."""
    for i in range(0, len(items), n):
        yield items[i:i + n]


def safe_escape(safe_str: str) -> str:
    """Safe escape url str."""
    return unquote(safe_str)


def get_i18n(
    field: Union[None, Dict, Mapping[str, Union[str, None]]],
    lang: str = 'ru',
    primary_lang: str = 'ru',
    use_fallback: bool = True,
    nullable_str: bool = False,
) -> str:
    """Get i18n."""

    if field is None:
        return None if nullable_str else ''

    primary = field.get(primary_lang, None)
    translate = field.get(lang, None)

    if lang == primary_lang:
        if primary is None:
            return None if nullable_str else ''
        return primary

    if translate is None and use_fallback and primary is not None:
        return primary
    elif translate is None and not use_fallback:
        return None if nullable_str else ''

    return translate


def update_i18n(
    field: Union[None, Dict, Mapping[str, Union[str, None]]],
    value: Union[None, str],
    lang: str,
) -> Union[None, Dict, Mapping[str, Union[str, None]]]:
    """Update i18n."""

    if field is None:
        field = dict()

    if value is None:
        field[lang] = None
    else:
        field[lang] = value

    return field
