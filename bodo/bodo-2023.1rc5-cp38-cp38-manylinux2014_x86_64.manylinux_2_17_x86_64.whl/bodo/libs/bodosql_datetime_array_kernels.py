"""
Implements datetime array kernels that are specific to BodoSQL
"""
import numba
import numpy as np
import pandas as pd
import pytz
from numba.core import types
from numba.extending import overload, register_jitable
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import raise_bodo_error


def standardize_snowflake_date_time_part(part_str):
    pass


@overload(standardize_snowflake_date_time_part)
def overload_standardize_snowflake_date_time_part(part_str):
    wtrjr__axku = pd.array(['year', 'y', 'yy', 'yyy', 'yyyy', 'yr', 'years',
        'yrs'])
    boo__utfhm = pd.array(['month', 'mm', 'mon', 'mons', 'months'])
    asw__ciz = pd.array(['day', 'd', 'dd', 'days', 'dayofmonth'])
    xjlm__rcxag = pd.array(['dayofweek', 'weekday', 'dow', 'dw'])
    wgd__xwxit = pd.array(['week', 'w', 'wk', 'weekofyear', 'woy', 'wy'])
    kyqf__cwn = pd.array(['weekiso', 'week_iso', 'weekofyeariso',
        'weekofyear_iso'])
    yggu__mesr = pd.array(['quarter', 'q', 'qtr', 'qtrs', 'quarters'])
    stdwa__uaz = pd.array(['hour', 'h', 'hh', 'hr', 'hours', 'hrs'])
    vnm__cozvr = pd.array(['minute', 'm', 'mi', 'min', 'minutes', 'mins'])
    izl__aytw = pd.array(['second', 's', 'sec', 'seconds', 'secs'])
    pnhwk__dukpo = pd.array(['millisecond', 'ms', 'msec', 'milliseconds'])
    otk__uey = pd.array(['microsecond', 'us', 'usec', 'microseconds'])
    evrkp__uryzk = pd.array(['nanosecond', 'ns', 'nsec', 'nanosec',
        'nsecond', 'nanoseconds', 'nanosecs', 'nseconds'])
    ovu__nmjxm = pd.array(['epoch_second', 'epoch', 'epoch_seconds'])
    eovr__nqu = pd.array(['epoch_millisecond', 'epoch_milliseconds'])
    sooe__qxl = pd.array(['epoch_microsecond', 'epoch_microseconds'])
    sabuc__iye = pd.array(['epoch_nanosecond', 'epoch_nanoseconds'])
    koh__eovc = pd.array(['timezone_hour', 'tzh'])
    qyq__tuqp = pd.array(['timezone_minute', 'tzm'])
    zjei__kjmik = pd.array(['yearofweek', 'yearofweekiso'])

    def impl(part_str):
        part_str = part_str.lower()
        if part_str in wtrjr__axku:
            return 'year'
        elif part_str in boo__utfhm:
            return 'month'
        elif part_str in asw__ciz:
            return 'day'
        elif part_str in xjlm__rcxag:
            return 'dayofweek'
        elif part_str in wgd__xwxit:
            return 'week'
        elif part_str in kyqf__cwn:
            return 'weekiso'
        elif part_str in yggu__mesr:
            return 'quarter'
        elif part_str in stdwa__uaz:
            return 'hour'
        elif part_str in vnm__cozvr:
            return 'minute'
        elif part_str in izl__aytw:
            return 'second'
        elif part_str in pnhwk__dukpo:
            return 'millisecond'
        elif part_str in otk__uey:
            return 'microsecond'
        elif part_str in evrkp__uryzk:
            return 'nanosecond'
        elif part_str in ovu__nmjxm:
            return 'epoch_second'
        elif part_str in eovr__nqu:
            return 'epoch_millisecond'
        elif part_str in sooe__qxl:
            return 'epoch_microsecond'
        elif part_str in sabuc__iye:
            return 'epoch_nanosecond'
        elif part_str in koh__eovc:
            return 'timezone_hour'
        elif part_str in qyq__tuqp:
            return 'timezone_minute'
        elif part_str in zjei__kjmik:
            return part_str
        else:
            raise ValueError(
                'Invalid date or time part passed into Snowflake array kernel')
    return impl


@numba.generated_jit(nopython=True)
def add_interval(start_dt, interval):
    args = [start_dt, interval]
    for fbc__zek in range(len(args)):
        if isinstance(args[fbc__zek], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.add_interval_util', ['arr'
                ], fbc__zek)

    def impl(start_dt, interval):
        return add_interval_util(start_dt, interval)
    return impl


def add_interval_years(amount, start_dt):
    return


def add_interval_quarters(amount, start_dt):
    return


def add_interval_months(amount, start_dt):
    return


def add_interval_weeks(amount, start_dt):
    return


def add_interval_days(amount, start_dt):
    return


def add_interval_hours(amount, start_dt):
    return


def add_interval_minutes(amount, start_dt):
    return


def add_interval_seconds(amount, start_dt):
    return


def add_interval_milliseconds(amount, start_dt):
    return


def add_interval_microseconds(amount, start_dt):
    return


def add_interval_nanoseconds(amount, start_dt):
    return


@numba.generated_jit(nopython=True)
def dayname(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.dayname_util',
            ['arr'], 0)

    def impl(arr):
        return dayname_util(arr)
    return impl


def dayofmonth(arr):
    return


def dayofweek(arr):
    return


def dayofweekiso(arr):
    return


def dayofyear(arr):
    return


def diff_day(arr0, arr1):
    return


def diff_hour(arr0, arr1):
    return


def diff_microsecond(arr0, arr1):
    return


def diff_minute(arr0, arr1):
    return


def diff_month(arr0, arr1):
    return


def diff_nanosecond(arr0, arr1):
    return


def diff_quarter(arr0, arr1):
    return


def diff_second(arr0, arr1):
    return


def diff_week(arr0, arr1):
    return


def diff_year(arr0, arr1):
    return


def get_year(arr):
    return


def get_quarter(arr):
    return


def get_month(arr):
    return


def get_week(arr):
    return


def get_hour(arr):
    return


def get_minute(arr):
    return


def get_second(arr):
    return


def get_millisecond(arr):
    return


def get_microsecond(arr):
    return


def get_nanosecond(arr):
    return


@numba.generated_jit(nopython=True)
def int_to_days(arr):
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.int_to_days_util', ['arr'], 0)

    def impl(arr):
        return int_to_days_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def last_day(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.last_day_util',
            ['arr'], 0)

    def impl(arr):
        return last_day_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def makedate(year, day):
    args = [year, day]
    for fbc__zek in range(2):
        if isinstance(args[fbc__zek], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.makedate',
                ['year', 'day'], fbc__zek)

    def impl(year, day):
        return makedate_util(year, day)
    return impl


@numba.generated_jit(nopython=True)
def monthname(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.monthname_util',
            ['arr'], 0)

    def impl(arr):
        return monthname_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def next_day(arr0, arr1):
    args = [arr0, arr1]
    for fbc__zek in range(2):
        if isinstance(args[fbc__zek], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.next_day',
                ['arr0', 'arr1'], fbc__zek)

    def impl(arr0, arr1):
        return next_day_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def previous_day(arr0, arr1):
    args = [arr0, arr1]
    for fbc__zek in range(2):
        if isinstance(args[fbc__zek], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.previous_day', ['arr0',
                'arr1'], fbc__zek)

    def impl(arr0, arr1):
        return previous_day_util(arr0, arr1)
    return impl


@numba.generated_jit(nopython=True)
def second_timestamp(arr):
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.second_timestamp_util', ['arr'], 0
            )

    def impl(arr):
        return second_timestamp_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def weekday(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.weekday_util',
            ['arr'], 0)

    def impl(arr):
        return weekday_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def yearofweekiso(arr):
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.yearofweekiso_util', ['arr'], 0)

    def impl(arr):
        return yearofweekiso_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def add_interval_util(start_dt, interval):
    verify_datetime_arg_allow_tz(start_dt, 'add_interval', 'start_dt')
    qaylh__qoai = get_tz_if_exists(start_dt)
    pauzr__tkh = ['start_dt', 'interval']
    vgeut__wyh = [start_dt, interval]
    akwlr__tbkvv = [True] * 2
    psl__idfx = ''
    qnph__yiv = bodo.utils.utils.is_array_typ(interval, True
        ) or bodo.utils.utils.is_array_typ(start_dt, True)
    ofxay__wwil = None
    if qaylh__qoai is not None:
        if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(qaylh__qoai):
            mfzxz__gxni = pytz.timezone(qaylh__qoai)
            uck__xxyxz = np.array(mfzxz__gxni._utc_transition_times, dtype=
                'M8[ns]').view('i8')
            dbo__aotm = np.array(mfzxz__gxni._transition_info)[:, 0]
            dbo__aotm = (pd.Series(dbo__aotm).dt.total_seconds() * 1000000000
                ).astype(np.int64).values
            ofxay__wwil = {'trans': uck__xxyxz, 'deltas': dbo__aotm}
            psl__idfx += f'start_value = arg0.value\n'
            psl__idfx += 'end_value = start_value + arg0.value\n'
            psl__idfx += (
                "start_trans = np.searchsorted(trans, start_value, side='right') - 1\n"
                )
            psl__idfx += (
                "end_trans = np.searchsorted(trans, end_value, side='right') - 1\n"
                )
            psl__idfx += 'offset = deltas[start_trans] - deltas[end_trans]\n'
            psl__idfx += 'arg1 = pd.Timedelta(arg1.value + offset)\n'
        psl__idfx += f'res[i] = arg0 + arg1\n'
        dbua__hfsdl = bodo.DatetimeArrayType(qaylh__qoai)
    else:
        vvqeu__jbh = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
            qnph__yiv else '')
        afuav__mfc = 'bodo.utils.conversion.box_if_dt64' if qnph__yiv else ''
        psl__idfx = f'res[i] = {vvqeu__jbh}({afuav__mfc}(arg0) + arg1)\n'
        dbua__hfsdl = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv, psl__idfx,
        dbua__hfsdl, extra_globals=ofxay__wwil)


def add_interval_years_util(amount, start_dt):
    return


def add_interval_quarters_util(amount, start_dt):
    return


def add_interval_months_util(amount, start_dt):
    return


def add_interval_weeks_util(amount, start_dt):
    return


def add_interval_days_util(amount, start_dt):
    return


def add_interval_hours_util(amount, start_dt):
    return


def add_interval_minutes_util(amount, start_dt):
    return


def add_interval_seconds_util(amount, start_dt):
    return


def add_interval_milliseconds_util(amount, start_dt):
    return


def add_interval_microseconds_util(amount, start_dt):
    return


def add_interval_nanoseconds_util(amount, start_dt):
    return


def create_add_interval_func_overload(unit):

    def overload_func(amount, start_dt):
        args = [amount, start_dt]
        for fbc__zek in range(2):
            if isinstance(args[fbc__zek], types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.add_interval_{unit}',
                    ['amount', 'start_dt'], fbc__zek)
        yglo__hbnd = 'def impl(amount, start_dt):\n'
        yglo__hbnd += (
            f'  return bodo.libs.bodosql_array_kernels.add_interval_{unit}_util(amount, start_dt)'
            )
        dkb__wgp = {}
        exec(yglo__hbnd, {'bodo': bodo}, dkb__wgp)
        return dkb__wgp['impl']
    return overload_func


def create_add_interval_util_overload(unit):

    def overload_add_datetime_interval_util(amount, start_dt):
        verify_int_arg(amount, 'add_interval_' + unit, 'amount')
        if unit in ('hours', 'minutes', 'seconds', 'milliseconds',
            'microseconds', 'nanoseconds'):
            verify_time_or_datetime_arg_allow_tz(start_dt, 'add_interval_' +
                unit, 'start_dt')
        else:
            verify_datetime_arg_allow_tz(start_dt, 'add_interval_' + unit,
                'start_dt')
        qaylh__qoai = get_tz_if_exists(start_dt)
        pauzr__tkh = ['amount', 'start_dt']
        vgeut__wyh = [amount, start_dt]
        akwlr__tbkvv = [True] * 2
        qnph__yiv = bodo.utils.utils.is_array_typ(amount, True
            ) or bodo.utils.utils.is_array_typ(start_dt, True)
        ofxay__wwil = None
        if is_valid_time_arg(start_dt):
            yen__fofnk = start_dt.precision
            if unit == 'hours':
                aaebk__iqrr = 3600000000000
            elif unit == 'minutes':
                aaebk__iqrr = 60000000000
            elif unit == 'seconds':
                aaebk__iqrr = 1000000000
            elif unit == 'milliseconds':
                yen__fofnk = max(yen__fofnk, 3)
                aaebk__iqrr = 1000000
            elif unit == 'microseconds':
                yen__fofnk = max(yen__fofnk, 6)
                aaebk__iqrr = 1000
            elif unit == 'nanoseconds':
                yen__fofnk = max(yen__fofnk, 9)
                aaebk__iqrr = 1
            psl__idfx = f"""amt = bodo.hiframes.time_ext.cast_time_to_int(arg1) + {aaebk__iqrr} * arg0
"""
            psl__idfx += (
                f'res[i] = bodo.hiframes.time_ext.cast_int_to_time(amt % 86400000000000, precision={yen__fofnk})'
                )
            dbua__hfsdl = types.Array(bodo.hiframes.time_ext.TimeType(
                yen__fofnk), 1, 'C')
        elif qaylh__qoai is not None:
            if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(qaylh__qoai
                ):
                mfzxz__gxni = pytz.timezone(qaylh__qoai)
                uck__xxyxz = np.array(mfzxz__gxni._utc_transition_times,
                    dtype='M8[ns]').view('i8')
                dbo__aotm = np.array(mfzxz__gxni._transition_info)[:, 0]
                dbo__aotm = (pd.Series(dbo__aotm).dt.total_seconds() * 
                    1000000000).astype(np.int64).values
                ofxay__wwil = {'trans': uck__xxyxz, 'deltas': dbo__aotm}
            if unit in ('months', 'quarters', 'years'):
                if unit == 'quarters':
                    psl__idfx = f'td = pd.DateOffset(months=3*arg0)\n'
                else:
                    psl__idfx = f'td = pd.DateOffset({unit}=arg0)\n'
                psl__idfx += f'start_value = arg1.value\n'
                psl__idfx += (
                    'end_value = (pd.Timestamp(arg1.value) + td).value\n')
                if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(
                    qaylh__qoai):
                    psl__idfx += """start_trans = np.searchsorted(trans, start_value, side='right') - 1
"""
                    psl__idfx += """end_trans = np.searchsorted(trans, end_value, side='right') - 1
"""
                    psl__idfx += (
                        'offset = deltas[start_trans] - deltas[end_trans]\n')
                    psl__idfx += (
                        'td = pd.Timedelta(end_value - start_value + offset)\n'
                        )
                else:
                    psl__idfx += 'td = pd.Timedelta(end_value - start_value)\n'
            else:
                if unit == 'nanoseconds':
                    psl__idfx = 'td = pd.Timedelta(arg0)\n'
                else:
                    psl__idfx = f'td = pd.Timedelta({unit}=arg0)\n'
                if bodo.hiframes.pd_offsets_ext.tz_has_transition_times(
                    qaylh__qoai):
                    psl__idfx += f'start_value = arg1.value\n'
                    psl__idfx += 'end_value = start_value + td.value\n'
                    psl__idfx += """start_trans = np.searchsorted(trans, start_value, side='right') - 1
"""
                    psl__idfx += """end_trans = np.searchsorted(trans, end_value, side='right') - 1
"""
                    psl__idfx += (
                        'offset = deltas[start_trans] - deltas[end_trans]\n')
                    psl__idfx += 'td = pd.Timedelta(td.value + offset)\n'
            psl__idfx += f'res[i] = arg1 + td\n'
            dbua__hfsdl = bodo.DatetimeArrayType(qaylh__qoai)
        else:
            vvqeu__jbh = (
                'bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
                qnph__yiv else '')
            afuav__mfc = ('bodo.utils.conversion.box_if_dt64' if qnph__yiv else
                '')
            if unit in ('months', 'years'):
                psl__idfx = f"""res[i] = {vvqeu__jbh}({afuav__mfc}(arg1) + pd.DateOffset({unit}=arg0))
"""
            elif unit == 'quarters':
                psl__idfx = f"""res[i] = {vvqeu__jbh}({afuav__mfc}(arg1) + pd.DateOffset(months=3*arg0))
"""
            elif unit == 'nanoseconds':
                psl__idfx = (
                    f'res[i] = {vvqeu__jbh}({afuav__mfc}(arg1) + pd.Timedelta(arg0))\n'
                    )
            else:
                psl__idfx = f"""res[i] = {vvqeu__jbh}({afuav__mfc}(arg1) + pd.Timedelta({unit}=arg0))
"""
            dbua__hfsdl = types.Array(bodo.datetime64ns, 1, 'C')
        return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv,
            psl__idfx, dbua__hfsdl, extra_globals=ofxay__wwil)
    return overload_add_datetime_interval_util


def _install_add_interval_overload():
    hrv__pots = [('years', add_interval_years, add_interval_years_util), (
        'quarters', add_interval_quarters, add_interval_quarters_util), (
        'months', add_interval_months, add_interval_months_util), ('weeks',
        add_interval_weeks, add_interval_weeks_util), ('days',
        add_interval_days, add_interval_days_util), ('hours',
        add_interval_hours, add_interval_hours_util), ('minutes',
        add_interval_minutes, add_interval_minutes_util), ('seconds',
        add_interval_seconds, add_interval_seconds_util), ('milliseconds',
        add_interval_milliseconds, add_interval_milliseconds_util), (
        'microseconds', add_interval_microseconds,
        add_interval_microseconds_util), ('nanoseconds',
        add_interval_nanoseconds, add_interval_nanoseconds_util)]
    for unit, esgw__wcsp, wnk__uyryj in hrv__pots:
        ytm__pms = create_add_interval_func_overload(unit)
        overload(esgw__wcsp)(ytm__pms)
        sjd__iqipb = create_add_interval_util_overload(unit)
        overload(wnk__uyryj)(sjd__iqipb)


_install_add_interval_overload()


def dayofmonth_util(arr):
    return


def dayofweek_util(arr):
    return


def dayofweekiso_util(arr):
    return


def dayofyear_util(arr):
    return


def get_year_util(arr):
    return


def get_quarter_util(arr):
    return


def get_month_util(arr):
    return


def get_week_util(arr):
    return


def get_hour_util(arr):
    return


def get_minute_util(arr):
    return


def get_second_util(arr):
    return


def get_millisecond_util(arr):
    return


def get_microsecond_util(arr):
    return


def get_nanosecond_util(arr):
    return


def create_dt_extract_fn_overload(fn_name):

    def overload_func(arr):
        if isinstance(arr, types.optional):
            return unopt_argument(f'bodo.libs.bodosql_array_kernels.{fn_name}',
                ['arr'], 0)
        yglo__hbnd = 'def impl(arr):\n'
        yglo__hbnd += (
            f'  return bodo.libs.bodosql_array_kernels.{fn_name}_util(arr)')
        dkb__wgp = {}
        exec(yglo__hbnd, {'bodo': bodo}, dkb__wgp)
        return dkb__wgp['impl']
    return overload_func


def create_dt_extract_fn_util_overload(fn_name):

    def overload_dt_extract_fn(arr):
        if fn_name in ('get_hour', 'get_minute', 'get_second',
            'get_microsecond', 'get_millisecond', 'get_nanosecond'):
            verify_time_or_datetime_arg_allow_tz(arr, fn_name, 'arr')
        else:
            verify_datetime_arg_allow_tz(arr, fn_name, 'arr')
        vsui__ccr = get_tz_if_exists(arr)
        afuav__mfc = ('bodo.utils.conversion.box_if_dt64' if vsui__ccr is
            None else '')
        qxw__snfvj = 'microsecond // 1000' if not is_valid_time_arg(arr
            ) else 'millisecond'
        bps__kxrhq = {'get_year': f'{afuav__mfc}(arg0).year', 'get_quarter':
            f'{afuav__mfc}(arg0).quarter', 'get_month':
            f'{afuav__mfc}(arg0).month', 'get_week':
            f'{afuav__mfc}(arg0).week', 'get_hour':
            f'{afuav__mfc}(arg0).hour', 'get_minute':
            f'{afuav__mfc}(arg0).minute', 'get_second':
            f'{afuav__mfc}(arg0).second', 'get_millisecond':
            f'{afuav__mfc}(arg0).{qxw__snfvj}', 'get_microsecond':
            f'{afuav__mfc}(arg0).microsecond', 'get_nanosecond':
            f'{afuav__mfc}(arg0).nanosecond', 'dayofmonth':
            f'{afuav__mfc}(arg0).day', 'dayofweek':
            f'({afuav__mfc}(arg0).dayofweek + 1) % 7', 'dayofweekiso':
            f'{afuav__mfc}(arg0).dayofweek + 1', 'dayofyear':
            f'{afuav__mfc}(arg0).dayofyear'}
        pauzr__tkh = ['arr']
        vgeut__wyh = [arr]
        akwlr__tbkvv = [True]
        psl__idfx = f'res[i] = {bps__kxrhq[fn_name]}'
        dbua__hfsdl = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
        return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv,
            psl__idfx, dbua__hfsdl)
    return overload_dt_extract_fn


def _install_dt_extract_fn_overload():
    hrv__pots = [('get_year', get_year, get_year_util), ('get_quarter',
        get_quarter, get_quarter_util), ('get_month', get_month,
        get_month_util), ('get_week', get_week, get_week_util), ('get_hour',
        get_hour, get_hour_util), ('get_minute', get_minute,
        get_minute_util), ('get_second', get_second, get_second_util), (
        'get_millisecond', get_millisecond, get_millisecond_util), (
        'get_microsecond', get_microsecond, get_microsecond_util), (
        'get_nanosecond', get_nanosecond, get_nanosecond_util), (
        'dayofmonth', dayofmonth, dayofmonth_util), ('dayofweek', dayofweek,
        dayofweek_util), ('dayofweekiso', dayofweekiso, dayofweekiso_util),
        ('dayofyear', dayofyear, dayofyear_util)]
    for fn_name, esgw__wcsp, wnk__uyryj in hrv__pots:
        ytm__pms = create_dt_extract_fn_overload(fn_name)
        overload(esgw__wcsp)(ytm__pms)
        sjd__iqipb = create_dt_extract_fn_util_overload(fn_name)
        overload(wnk__uyryj)(sjd__iqipb)


_install_dt_extract_fn_overload()


def diff_day_util(arr0, arr1):
    return


def diff_hour_util(arr0, arr1):
    return


def diff_microsecond_util(arr0, arr1):
    return


def diff_minute_util(arr0, arr1):
    return


def diff_month_util(arr0, arr1):
    return


def diff_nanosecond_util(arr0, arr1):
    return


def diff_quarter_util(arr0, arr1):
    return


def diff_second_util(arr0, arr1):
    return


def diff_week_util(arr0, arr1):
    return


def diff_year_util(arr0, arr1):
    return


@register_jitable
def get_iso_weeks_between_years(year0, year1):
    bump__mssr = 1
    if year1 < year0:
        year0, year1 = year1, year0
        bump__mssr = -1
    jpiuf__dzy = 0
    for vbmdh__cbca in range(year0, year1):
        jpiuf__dzy += 52
        rpwf__htu = (vbmdh__cbca + vbmdh__cbca // 4 - vbmdh__cbca // 100 + 
            vbmdh__cbca // 400) % 7
        iydkj__xui = (vbmdh__cbca - 1 + (vbmdh__cbca - 1) // 4 - (
            vbmdh__cbca - 1) // 100 + (vbmdh__cbca - 1) // 400) % 7
        if rpwf__htu == 4 or iydkj__xui == 3:
            jpiuf__dzy += 1
    return bump__mssr * jpiuf__dzy


def create_dt_diff_fn_overload(unit):

    def overload_func(arr0, arr1):
        args = [arr0, arr1]
        for fbc__zek in range(len(args)):
            if isinstance(args[fbc__zek], types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.diff_{unit}', ['arr0',
                    'arr1'], fbc__zek)
        yglo__hbnd = 'def impl(arr0, arr1):\n'
        yglo__hbnd += (
            f'  return bodo.libs.bodosql_array_kernels.diff_{unit}_util(arr0, arr1)'
            )
        dkb__wgp = {}
        exec(yglo__hbnd, {'bodo': bodo}, dkb__wgp)
        return dkb__wgp['impl']
    return overload_func


def create_dt_diff_fn_util_overload(unit):

    def overload_dt_diff_fn(arr0, arr1):
        verify_datetime_arg_allow_tz(arr0, 'diff_' + unit, 'arr0')
        verify_datetime_arg_allow_tz(arr1, 'diff_' + unit, 'arr1')
        vsui__ccr = get_tz_if_exists(arr0)
        if get_tz_if_exists(arr1) != vsui__ccr:
            raise_bodo_error(
                f'diff_{unit}: both arguments must have the same timezone')
        pauzr__tkh = ['arr0', 'arr1']
        vgeut__wyh = [arr0, arr1]
        akwlr__tbkvv = [True] * 2
        ofxay__wwil = None
        qpc__uwd = {'yr_diff': 'arg1.year - arg0.year', 'qu_diff':
            'arg1.quarter - arg0.quarter', 'mo_diff':
            'arg1.month - arg0.month', 'y0, w0, _': 'arg0.isocalendar()',
            'y1, w1, _': 'arg1.isocalendar()', 'iso_yr_diff':
            'bodo.libs.bodosql_array_kernels.get_iso_weeks_between_years(y0, y1)'
            , 'wk_diff': 'w1 - w0', 'da_diff':
            '(pd.Timestamp(arg1.year, arg1.month, arg1.day) - pd.Timestamp(arg0.year, arg0.month, arg0.day)).days'
            , 'ns_diff': 'arg1.value - arg0.value'}
        kpu__aaotx = {'year': ['yr_diff'], 'quarter': ['yr_diff', 'qu_diff'
            ], 'month': ['yr_diff', 'mo_diff'], 'week': ['y0, w0, _',
            'y1, w1, _', 'iso_yr_diff', 'wk_diff'], 'day': ['da_diff'],
            'nanosecond': ['ns_diff']}
        psl__idfx = ''
        if vsui__ccr == None:
            psl__idfx += 'arg0 = bodo.utils.conversion.box_if_dt64(arg0)\n'
            psl__idfx += 'arg1 = bodo.utils.conversion.box_if_dt64(arg1)\n'
        for jwce__ffrmm in kpu__aaotx.get(unit, []):
            psl__idfx += f'{jwce__ffrmm} = {qpc__uwd[jwce__ffrmm]}\n'
        if unit == 'nanosecond':
            dbua__hfsdl = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
        else:
            dbua__hfsdl = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
        if unit == 'year':
            psl__idfx += 'res[i] = yr_diff'
        elif unit == 'quarter':
            psl__idfx += 'res[i] = 4 * yr_diff + qu_diff'
        elif unit == 'month':
            psl__idfx += 'res[i] = 12 * yr_diff + mo_diff'
        elif unit == 'week':
            psl__idfx += 'res[i] = iso_yr_diff + wk_diff'
        elif unit == 'day':
            psl__idfx += 'res[i] = da_diff'
        elif unit == 'nanosecond':
            psl__idfx += 'res[i] = ns_diff'
        else:
            if unit == 'hour':
                oszo__hmfpw = 3600000000000
            if unit == 'minute':
                oszo__hmfpw = 60000000000
            if unit == 'second':
                oszo__hmfpw = 1000000000
            if unit == 'microsecond':
                oszo__hmfpw = 1000
            psl__idfx += f"""res[i] = np.floor_divide((arg1.value), ({oszo__hmfpw})) - np.floor_divide((arg0.value), ({oszo__hmfpw}))
"""
        return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv,
            psl__idfx, dbua__hfsdl, extra_globals=ofxay__wwil)
    return overload_dt_diff_fn


def _install_dt_diff_fn_overload():
    hrv__pots = [('day', diff_day, diff_day_util), ('hour', diff_hour,
        diff_hour_util), ('microsecond', diff_microsecond,
        diff_microsecond_util), ('minute', diff_minute, diff_minute_util),
        ('month', diff_month, diff_month_util), ('nanosecond',
        diff_nanosecond, diff_nanosecond_util), ('quarter', diff_quarter,
        diff_quarter), ('second', diff_second, diff_second_util), ('week',
        diff_week, diff_week_util), ('year', diff_year, diff_year_util)]
    for unit, esgw__wcsp, wnk__uyryj in hrv__pots:
        ytm__pms = create_dt_diff_fn_overload(unit)
        overload(esgw__wcsp)(ytm__pms)
        sjd__iqipb = create_dt_diff_fn_util_overload(unit)
        overload(wnk__uyryj)(sjd__iqipb)


_install_dt_diff_fn_overload()


def date_trunc(date_or_time_part, ts_arg):
    pass


@overload(date_trunc)
def overload_date_trunc(date_or_time_part, ts_arg):
    if isinstance(date_or_time_part, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.date_trunc',
            ['date_or_time_part', 'ts_arg'], 0)
    if isinstance(ts_arg, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.date_trunc',
            ['date_or_time_part', 'ts_arg'], 1)

    def impl(date_or_time_part, ts_arg):
        return date_trunc_util(date_or_time_part, ts_arg)
    return impl


def date_trunc_util(date_or_time_part, ts_arg):
    pass


@overload(date_trunc_util)
def overload_date_trunc_util(date_or_time_part, ts_arg):
    verify_string_arg(date_or_time_part, 'DATE_TRUNC', 'date_or_time_part')
    verify_datetime_arg_allow_tz(ts_arg, 'DATE_TRUNC', 'ts_arg')
    jbwy__njufl = get_tz_if_exists(ts_arg)
    pauzr__tkh = ['date_or_time_part', 'ts_arg']
    vgeut__wyh = [date_or_time_part, ts_arg]
    akwlr__tbkvv = [True, True]
    afuav__mfc = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(ts_arg, True) else '')
    vvqeu__jbh = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(ts_arg, True) else '')
    psl__idfx = """part_str = bodo.libs.bodosql_array_kernels.standardize_snowflake_date_time_part(arg0)
"""
    if jbwy__njufl is None:
        psl__idfx += f'arg1 = {afuav__mfc}(arg1)\n'
    psl__idfx += "if part_str == 'quarter':\n"
    psl__idfx += """    out_val = pd.Timestamp(year=arg1.year, month= (3*(arg1.quarter - 1)) + 1, day=1, tz=tz_literal)
"""
    psl__idfx += "elif part_str == 'year':\n"
    psl__idfx += (
        '    out_val = pd.Timestamp(year=arg1.year, month=1, day=1, tz=tz_literal)\n'
        )
    psl__idfx += "elif part_str == 'month':\n"
    psl__idfx += """    out_val = pd.Timestamp(year=arg1.year, month=arg1.month, day=1, tz=tz_literal)
"""
    psl__idfx += "elif part_str == 'day':\n"
    psl__idfx += '    out_val = arg1.normalize()\n'
    psl__idfx += "elif part_str == 'week':\n"
    psl__idfx += '    if arg1.dayofweek == 0:\n'
    psl__idfx += '        out_val = arg1.normalize()\n'
    psl__idfx += '    else:\n'
    psl__idfx += (
        '        out_val = arg1.normalize() - pd.tseries.offsets.Week(n=1, weekday=0)\n'
        )
    psl__idfx += "elif part_str == 'hour':\n"
    psl__idfx += "    out_val = arg1.floor('H')\n"
    psl__idfx += "elif part_str == 'minute':\n"
    psl__idfx += "    out_val = arg1.floor('min')\n"
    psl__idfx += "elif part_str == 'second':\n"
    psl__idfx += "    out_val = arg1.floor('S')\n"
    psl__idfx += "elif part_str == 'millisecond':\n"
    psl__idfx += "    out_val = arg1.floor('ms')\n"
    psl__idfx += "elif part_str == 'microsecond':\n"
    psl__idfx += "    out_val = arg1.floor('us')\n"
    psl__idfx += "elif part_str == 'nanosecond':\n"
    psl__idfx += '    out_val = arg1\n'
    psl__idfx += 'else:\n'
    psl__idfx += (
        "    raise ValueError('Invalid date or time part for DATE_TRUNC')\n")
    if jbwy__njufl is None:
        psl__idfx += f'res[i] = {vvqeu__jbh}(out_val)\n'
    else:
        psl__idfx += f'res[i] = out_val\n'
    if jbwy__njufl is None:
        dbua__hfsdl = types.Array(bodo.datetime64ns, 1, 'C')
    else:
        dbua__hfsdl = bodo.DatetimeArrayType(jbwy__njufl)
    return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv, psl__idfx,
        dbua__hfsdl, extra_globals={'tz_literal': jbwy__njufl})


@numba.generated_jit(nopython=True)
def dayname_util(arr):
    verify_datetime_arg_allow_tz(arr, 'dayname', 'arr')
    vsui__ccr = get_tz_if_exists(arr)
    afuav__mfc = ('bodo.utils.conversion.box_if_dt64' if vsui__ccr is None else
        '')
    pauzr__tkh = ['arr']
    vgeut__wyh = [arr]
    akwlr__tbkvv = [True]
    psl__idfx = f'res[i] = {afuav__mfc}(arg0).day_name()'
    dbua__hfsdl = bodo.string_array_type
    dmonw__accz = ['V']
    otyxs__dblv = pd.array(['Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday'])
    ofxay__wwil = {'day_of_week_dict_arr': otyxs__dblv}
    qqvcz__omz = 'dict_res = day_of_week_dict_arr'
    uxphj__ylh = f'res[i] = {afuav__mfc}(arg0).dayofweek'
    return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv, psl__idfx,
        dbua__hfsdl, synthesize_dict_if_vector=dmonw__accz,
        synthesize_dict_setup_text=qqvcz__omz, synthesize_dict_scalar_text=
        uxphj__ylh, extra_globals=ofxay__wwil, synthesize_dict_global=True,
        synthesize_dict_unique=True)


@numba.generated_jit(nopython=True)
def int_to_days_util(arr):
    verify_int_arg(arr, 'int_to_days', 'arr')
    vvqeu__jbh = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr, True) else '')
    pauzr__tkh = ['arr']
    vgeut__wyh = [arr]
    akwlr__tbkvv = [True]
    psl__idfx = f'res[i] = {vvqeu__jbh}(pd.Timedelta(days=arg0))'
    dbua__hfsdl = np.dtype('timedelta64[ns]')
    return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv, psl__idfx,
        dbua__hfsdl)


@numba.generated_jit(nopython=True)
def last_day_util(arr):
    verify_datetime_arg_allow_tz(arr, 'LAST_DAY', 'arr')
    qaylh__qoai = get_tz_if_exists(arr)
    afuav__mfc = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    vvqeu__jbh = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr, True) else '')
    pauzr__tkh = ['arr']
    vgeut__wyh = [arr]
    akwlr__tbkvv = [True]
    if qaylh__qoai is None:
        psl__idfx = (
            f'res[i] = {vvqeu__jbh}({afuav__mfc}(arg0) + pd.tseries.offsets.MonthEnd(n=0, normalize=True))'
            )
        dbua__hfsdl = np.dtype('datetime64[ns]')
    else:
        psl__idfx = 'y = arg0.year\n'
        psl__idfx += 'm = arg0.month\n'
        psl__idfx += (
            'd = bodo.hiframes.pd_offsets_ext.get_days_in_month(y, m)\n')
        psl__idfx += (
            f'res[i] = pd.Timestamp(year=y, month=m, day=d, tz={repr(qaylh__qoai)})\n'
            )
        dbua__hfsdl = bodo.DatetimeArrayType(qaylh__qoai)
    return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv, psl__idfx,
        dbua__hfsdl)


@numba.generated_jit(nopython=True)
def makedate_util(year, day):
    verify_int_arg(year, 'MAKEDATE', 'year')
    verify_int_arg(day, 'MAKEDATE', 'day')
    vvqeu__jbh = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if 
        bodo.utils.utils.is_array_typ(year, True) or bodo.utils.utils.
        is_array_typ(day, True) else '')
    pauzr__tkh = ['year', 'day']
    vgeut__wyh = [year, day]
    akwlr__tbkvv = [True] * 2
    psl__idfx = (
        f'res[i] = {vvqeu__jbh}(pd.Timestamp(year=arg0, month=1, day=1) + pd.Timedelta(days=arg1-1))'
        )
    dbua__hfsdl = np.dtype('datetime64[ns]')
    return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv, psl__idfx,
        dbua__hfsdl)


@numba.generated_jit(nopython=True)
def monthname_util(arr):
    verify_datetime_arg_allow_tz(arr, 'monthname', 'arr')
    vsui__ccr = get_tz_if_exists(arr)
    afuav__mfc = ('bodo.utils.conversion.box_if_dt64' if vsui__ccr is None else
        '')
    pauzr__tkh = ['arr']
    vgeut__wyh = [arr]
    akwlr__tbkvv = [True]
    psl__idfx = f'res[i] = {afuav__mfc}(arg0).month_name()'
    dbua__hfsdl = bodo.string_array_type
    dmonw__accz = ['V']
    ufqut__tbqaw = pd.array(['January', 'February', 'March', 'April', 'May',
        'June', 'July', 'August', 'September', 'October', 'November',
        'December'])
    ofxay__wwil = {'month_names_dict_arr': ufqut__tbqaw}
    qqvcz__omz = 'dict_res = month_names_dict_arr'
    uxphj__ylh = f'res[i] = {afuav__mfc}(arg0).month - 1'
    return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv, psl__idfx,
        dbua__hfsdl, synthesize_dict_if_vector=dmonw__accz,
        synthesize_dict_setup_text=qqvcz__omz, synthesize_dict_scalar_text=
        uxphj__ylh, extra_globals=ofxay__wwil, synthesize_dict_global=True,
        synthesize_dict_unique=True)


@numba.generated_jit(nopython=True)
def next_day_util(arr0, arr1):
    verify_datetime_arg_allow_tz(arr0, 'NEXT_DAY', 'arr0')
    verify_string_arg(arr1, 'NEXT_DAY', 'arr1')
    uuitx__ehy = is_valid_tz_aware_datetime_arg(arr0)
    vvqeu__jbh = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if 
        bodo.utils.utils.is_array_typ(arr0, True) or bodo.utils.utils.
        is_array_typ(arr1, True) else '')
    pauzr__tkh = ['arr0', 'arr1']
    vgeut__wyh = [arr0, arr1]
    akwlr__tbkvv = [True] * 2
    brl__uaia = (
        "dow_map = {'mo': 0, 'tu': 1, 'we': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}"
        )
    psl__idfx = f'arg1_trimmed = arg1.lstrip()[:2].lower()\n'
    if uuitx__ehy:
        jklsi__jezy = 'arg0'
    else:
        jklsi__jezy = 'bodo.utils.conversion.box_if_dt64(arg0)'
    psl__idfx += f"""new_timestamp = {jklsi__jezy}.normalize() + pd.tseries.offsets.Week(weekday=dow_map[arg1_trimmed])
"""
    psl__idfx += f'res[i] = {vvqeu__jbh}(new_timestamp.tz_localize(None))\n'
    dbua__hfsdl = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv, psl__idfx,
        dbua__hfsdl, prefix_code=brl__uaia)


@numba.generated_jit(nopython=True)
def previous_day_util(arr0, arr1):
    verify_datetime_arg_allow_tz(arr0, 'PREVIOUS_DAY', 'arr0')
    verify_string_arg(arr1, 'PREVIOUS_DAY', 'arr1')
    uuitx__ehy = is_valid_tz_aware_datetime_arg(arr0)
    vvqeu__jbh = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if 
        bodo.utils.utils.is_array_typ(arr0, True) or bodo.utils.utils.
        is_array_typ(arr1, True) else '')
    pauzr__tkh = ['arr0', 'arr1']
    vgeut__wyh = [arr0, arr1]
    akwlr__tbkvv = [True] * 2
    brl__uaia = (
        "dow_map = {'mo': 0, 'tu': 1, 'we': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}"
        )
    psl__idfx = f'arg1_trimmed = arg1.lstrip()[:2].lower()\n'
    if uuitx__ehy:
        jklsi__jezy = 'arg0'
    else:
        jklsi__jezy = 'bodo.utils.conversion.box_if_dt64(arg0)'
    psl__idfx += f"""new_timestamp = {jklsi__jezy}.normalize() - pd.tseries.offsets.Week(weekday=dow_map[arg1_trimmed])
"""
    psl__idfx += f'res[i] = {vvqeu__jbh}(new_timestamp.tz_localize(None))\n'
    dbua__hfsdl = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv, psl__idfx,
        dbua__hfsdl, prefix_code=brl__uaia)


@numba.generated_jit(nopython=True)
def second_timestamp_util(arr):
    verify_int_arg(arr, 'second_timestamp', 'arr')
    vvqeu__jbh = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr, True) else '')
    pauzr__tkh = ['arr']
    vgeut__wyh = [arr]
    akwlr__tbkvv = [True]
    psl__idfx = f"res[i] = {vvqeu__jbh}(pd.Timestamp(arg0, unit='s'))"
    dbua__hfsdl = np.dtype('datetime64[ns]')
    return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv, psl__idfx,
        dbua__hfsdl)


@numba.generated_jit(nopython=True)
def weekday_util(arr):
    verify_datetime_arg(arr, 'WEEKDAY', 'arr')
    pauzr__tkh = ['arr']
    vgeut__wyh = [arr]
    akwlr__tbkvv = [True]
    afuav__mfc = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    psl__idfx = f'dt = {afuav__mfc}(arg0)\n'
    psl__idfx += (
        'res[i] = bodo.hiframes.pd_timestamp_ext.get_day_of_week(dt.year, dt.month, dt.day)'
        )
    dbua__hfsdl = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv, psl__idfx,
        dbua__hfsdl)


@numba.generated_jit(nopython=True)
def yearofweekiso_util(arr):
    verify_datetime_arg_allow_tz(arr, 'YEAROFWEEKISO', 'arr')
    pauzr__tkh = ['arr']
    vgeut__wyh = [arr]
    akwlr__tbkvv = [True]
    afuav__mfc = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils.
        is_array_typ(arr, True) else '')
    psl__idfx = f'dt = {afuav__mfc}(arg0)\n'
    psl__idfx += 'res[i] = dt.isocalendar()[0]'
    dbua__hfsdl = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv, psl__idfx,
        dbua__hfsdl)


def to_days(arr):
    pass


@overload(to_days)
def overload_to_days(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.to_days_util',
            ['arr'], 0)

    def impl(arr):
        return to_days_util(arr)
    return impl


def to_days_util(arr):
    pass


@overload(to_days_util)
def overload_to_days_util(arr):
    verify_datetime_arg(arr, 'TO_DAYS', 'arr')
    pauzr__tkh = ['arr']
    vgeut__wyh = [arr]
    akwlr__tbkvv = [True]
    brl__uaia = 'unix_days_to_year_zero = 719528\n'
    brl__uaia += 'nanoseconds_divisor = 86400000000000\n'
    dbua__hfsdl = bodo.IntegerArrayType(types.int64)
    rwqo__nmd = bodo.utils.utils.is_array_typ(arr, False)
    if rwqo__nmd:
        psl__idfx = (
            '  in_value = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg0)\n'
            )
    else:
        psl__idfx = '  in_value = arg0.value\n'
    psl__idfx += (
        '  res[i] = (in_value // nanoseconds_divisor) + unix_days_to_year_zero\n'
        )
    return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv, psl__idfx,
        dbua__hfsdl, prefix_code=brl__uaia)


def from_days(arr):
    pass


@overload(from_days)
def overload_from_days(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.from_days_util',
            ['arr'], 0)

    def impl(arr):
        return from_days_util(arr)
    return impl


def from_days_util(arr):
    pass


@overload(from_days_util)
def overload_from_days_util(arr):
    verify_int_arg(arr, 'TO_DAYS', 'arr')
    pauzr__tkh = ['arr']
    vgeut__wyh = [arr]
    akwlr__tbkvv = [True]
    rwqo__nmd = bodo.utils.utils.is_array_typ(arr, False)
    if rwqo__nmd:
        dbua__hfsdl = types.Array(bodo.datetime64ns, 1, 'C')
    else:
        dbua__hfsdl = bodo.pd_timestamp_tz_naive_type
    brl__uaia = 'unix_days_to_year_zero = 719528\n'
    brl__uaia += 'nanoseconds_divisor = 86400000000000\n'
    psl__idfx = (
        '  nanoseconds = (arg0 - unix_days_to_year_zero) * nanoseconds_divisor\n'
        )
    if rwqo__nmd:
        psl__idfx += (
            '  res[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(nanoseconds)\n'
            )
    else:
        psl__idfx += '  res[i] = pd.Timestamp(nanoseconds)\n'
    return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv, psl__idfx,
        dbua__hfsdl, prefix_code=brl__uaia)


def to_seconds(arr):
    pass


@overload(to_seconds)
def overload_to_seconds(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.to_seconds_util'
            , ['arr'], 0)

    def impl(arr):
        return to_seconds_util(arr)
    return impl


def to_seconds_util(arr):
    pass


@overload(to_seconds_util)
def overload_to_seconds_util(arr):
    verify_datetime_arg_allow_tz(arr, 'TO_SECONDS', 'arr')
    uhe__phvu = get_tz_if_exists(arr)
    pauzr__tkh = ['arr']
    vgeut__wyh = [arr]
    akwlr__tbkvv = [True]
    brl__uaia = 'unix_seconds_to_year_zero = 62167219200\n'
    brl__uaia += 'nanoseconds_divisor = 1000000000\n'
    dbua__hfsdl = bodo.IntegerArrayType(types.int64)
    rwqo__nmd = bodo.utils.utils.is_array_typ(arr, False)
    if rwqo__nmd and not uhe__phvu:
        psl__idfx = (
            f'  in_value = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg0)\n'
            )
    else:
        psl__idfx = f'  in_value = arg0.value\n'
    psl__idfx += (
        '  res[i] = (in_value // nanoseconds_divisor) + unix_seconds_to_year_zero\n'
        )
    return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv, psl__idfx,
        dbua__hfsdl, prefix_code=brl__uaia)


def tz_aware_interval_add(tz_arg, interval_arg):
    pass


@overload(tz_aware_interval_add)
def overload_tz_aware_interval_add(tz_arg, interval_arg):
    if isinstance(tz_arg, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.tz_aware_interval_add', [
            'tz_arg', 'interval_arg'], 0)
    if isinstance(interval_arg, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.tz_aware_interval_add', [
            'tz_arg', 'interval_arg'], 1)

    def impl(tz_arg, interval_arg):
        return tz_aware_interval_add_util(tz_arg, interval_arg)
    return impl


def tz_aware_interval_add_util(tz_arg, interval_arg):
    pass


@overload(tz_aware_interval_add_util)
def overload_tz_aware_interval_add_util(tz_arg, interval_arg):
    verify_datetime_arg_require_tz(tz_arg, 'INTERVAL_ADD', 'tz_arg')
    verify_sql_interval(interval_arg, 'INTERVAL_ADD', 'interval_arg')
    uhe__phvu = get_tz_if_exists(tz_arg)
    pauzr__tkh = ['tz_arg', 'interval_arg']
    vgeut__wyh = [tz_arg, interval_arg]
    akwlr__tbkvv = [True, True]
    if uhe__phvu is not None:
        dbua__hfsdl = bodo.DatetimeArrayType(uhe__phvu)
    else:
        dbua__hfsdl = bodo.datetime64ns
    if interval_arg == bodo.date_offset_type:
        psl__idfx = """  timedelta = bodo.libs.pd_datetime_arr_ext.convert_months_offset_to_days(arg0.year, arg0.month, arg0.day, ((arg1._years * 12) + arg1._months) * arg1.n)
"""
    else:
        psl__idfx = '  timedelta = arg1\n'
    psl__idfx += """  timedelta = bodo.hiframes.pd_offsets_ext.update_timedelta_with_transition(arg0, timedelta)
"""
    psl__idfx += '  res[i] = arg0 + timedelta\n'
    return gen_vectorized(pauzr__tkh, vgeut__wyh, akwlr__tbkvv, psl__idfx,
        dbua__hfsdl)
