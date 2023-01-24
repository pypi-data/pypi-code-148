"""Timestamp extension for Pandas Timestamp with timezone support."""
import calendar
import datetime
import operator
from typing import Union
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pytz
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.core.typing.templates import ConcreteTemplate, infer_global, signature
from numba.extending import NativeValue, box, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
import bodo.libs.str_ext
import bodo.utils.utils
from bodo.hiframes.datetime_date_ext import DatetimeDateType, _ord2ymd, _ymd2ord, get_isocalendar
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType, _no_input, datetime_timedelta_type, pd_timedelta_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.libs import hdatetime_ext
from bodo.libs.pd_datetime_arr_ext import get_pytz_type_info
from bodo.libs.str_arr_ext import string_array_type
from bodo.utils.typing import BodoError, check_unsupported_args, get_literal_value, get_overload_const_bool, get_overload_const_int, get_overload_const_str, is_iterable_type, is_literal_type, is_overload_constant_int, is_overload_constant_str, is_overload_none, raise_bodo_error
ll.add_symbol('extract_year_days', hdatetime_ext.extract_year_days)
ll.add_symbol('get_month_day', hdatetime_ext.get_month_day)
ll.add_symbol('npy_datetimestruct_to_datetime', hdatetime_ext.
    npy_datetimestruct_to_datetime)
npy_datetimestruct_to_datetime = types.ExternalFunction(
    'npy_datetimestruct_to_datetime', types.int64(types.int64, types.int32,
    types.int32, types.int32, types.int32, types.int32, types.int32))
date_fields = ['year', 'month', 'day', 'hour', 'minute', 'second',
    'microsecond', 'nanosecond', 'quarter', 'dayofyear', 'day_of_year',
    'dayofweek', 'day_of_week', 'daysinmonth', 'days_in_month',
    'is_leap_year', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end', 'week', 'weekofyear',
    'weekday']
date_methods = ['normalize', 'day_name', 'month_name']
timedelta_fields = ['days', 'seconds', 'microseconds', 'nanoseconds']
timedelta_methods = ['total_seconds', 'to_pytimedelta']
iNaT = pd._libs.tslibs.iNaT


class PandasTimestampType(types.Type):

    def __init__(self, tz_val=None):
        self.tz = tz_val
        if tz_val is None:
            vvu__xdwrj = 'PandasTimestampType()'
        else:
            vvu__xdwrj = f'PandasTimestampType({tz_val})'
        super(PandasTimestampType, self).__init__(name=vvu__xdwrj)


pd_timestamp_tz_naive_type = PandasTimestampType()


def check_tz_aware_unsupported(val, func_name):
    if isinstance(val, bodo.hiframes.series_dt_impl.
        SeriesDatetimePropertiesType):
        val = val.stype
    if isinstance(val, PandasTimestampType) and val.tz is not None:
        raise BodoError(
            f'{func_name} on Timezone-aware timestamp not yet supported. Please convert to timezone naive with ts.tz_convert(None)'
            )
    elif isinstance(val, bodo.DatetimeArrayType):
        raise BodoError(
            f'{func_name} on Timezone-aware array not yet supported. Please convert to timezone naive with arr.tz_convert(None)'
            )
    elif isinstance(val, bodo.DatetimeIndexType) and isinstance(val.data,
        bodo.DatetimeArrayType):
        raise BodoError(
            f'{func_name} on Timezone-aware index not yet supported. Please convert to timezone naive with index.tz_convert(None)'
            )
    elif isinstance(val, bodo.SeriesType) and isinstance(val.data, bodo.
        DatetimeArrayType):
        raise BodoError(
            f'{func_name} on Timezone-aware series not yet supported. Please convert to timezone naive with series.dt.tz_convert(None)'
            )
    elif isinstance(val, bodo.DataFrameType):
        for pjql__hunc in val.data:
            if isinstance(pjql__hunc, bodo.DatetimeArrayType):
                raise BodoError(
                    f'{func_name} on Timezone-aware columns not yet supported. Please convert each column to timezone naive with series.dt.tz_convert(None)'
                    )


@typeof_impl.register(pd.Timestamp)
def typeof_pd_timestamp(val, c):
    return PandasTimestampType(get_pytz_type_info(val.tz) if val.tz else None)


ts_field_typ = types.int64


@register_model(PandasTimestampType)
class PandasTimestampModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ttuc__qxz = [('year', ts_field_typ), ('month', ts_field_typ), (
            'day', ts_field_typ), ('hour', ts_field_typ), ('minute',
            ts_field_typ), ('second', ts_field_typ), ('microsecond',
            ts_field_typ), ('nanosecond', ts_field_typ), ('value',
            ts_field_typ)]
        models.StructModel.__init__(self, dmm, fe_type, ttuc__qxz)


make_attribute_wrapper(PandasTimestampType, 'year', 'year')
make_attribute_wrapper(PandasTimestampType, 'month', 'month')
make_attribute_wrapper(PandasTimestampType, 'day', 'day')
make_attribute_wrapper(PandasTimestampType, 'hour', 'hour')
make_attribute_wrapper(PandasTimestampType, 'minute', 'minute')
make_attribute_wrapper(PandasTimestampType, 'second', 'second')
make_attribute_wrapper(PandasTimestampType, 'microsecond', 'microsecond')
make_attribute_wrapper(PandasTimestampType, 'nanosecond', 'nanosecond')
make_attribute_wrapper(PandasTimestampType, 'value', 'value')


@unbox(PandasTimestampType)
def unbox_pandas_timestamp(typ, val, c):
    ynmk__scmp = c.pyapi.object_getattr_string(val, 'year')
    rwp__epbe = c.pyapi.object_getattr_string(val, 'month')
    kvaud__tark = c.pyapi.object_getattr_string(val, 'day')
    vznd__scyv = c.pyapi.object_getattr_string(val, 'hour')
    njcc__jli = c.pyapi.object_getattr_string(val, 'minute')
    pizca__jod = c.pyapi.object_getattr_string(val, 'second')
    ckd__qrmqp = c.pyapi.object_getattr_string(val, 'microsecond')
    aee__wmsed = c.pyapi.object_getattr_string(val, 'nanosecond')
    nbcur__zkbgf = c.pyapi.object_getattr_string(val, 'value')
    xsbgl__gatks = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    xsbgl__gatks.year = c.pyapi.long_as_longlong(ynmk__scmp)
    xsbgl__gatks.month = c.pyapi.long_as_longlong(rwp__epbe)
    xsbgl__gatks.day = c.pyapi.long_as_longlong(kvaud__tark)
    xsbgl__gatks.hour = c.pyapi.long_as_longlong(vznd__scyv)
    xsbgl__gatks.minute = c.pyapi.long_as_longlong(njcc__jli)
    xsbgl__gatks.second = c.pyapi.long_as_longlong(pizca__jod)
    xsbgl__gatks.microsecond = c.pyapi.long_as_longlong(ckd__qrmqp)
    xsbgl__gatks.nanosecond = c.pyapi.long_as_longlong(aee__wmsed)
    xsbgl__gatks.value = c.pyapi.long_as_longlong(nbcur__zkbgf)
    c.pyapi.decref(ynmk__scmp)
    c.pyapi.decref(rwp__epbe)
    c.pyapi.decref(kvaud__tark)
    c.pyapi.decref(vznd__scyv)
    c.pyapi.decref(njcc__jli)
    c.pyapi.decref(pizca__jod)
    c.pyapi.decref(ckd__qrmqp)
    c.pyapi.decref(aee__wmsed)
    c.pyapi.decref(nbcur__zkbgf)
    guh__vrfa = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(xsbgl__gatks._getvalue(), is_error=guh__vrfa)


@box(PandasTimestampType)
def box_pandas_timestamp(typ, val, c):
    xkzu__badde = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    ynmk__scmp = c.pyapi.long_from_longlong(xkzu__badde.year)
    rwp__epbe = c.pyapi.long_from_longlong(xkzu__badde.month)
    kvaud__tark = c.pyapi.long_from_longlong(xkzu__badde.day)
    vznd__scyv = c.pyapi.long_from_longlong(xkzu__badde.hour)
    njcc__jli = c.pyapi.long_from_longlong(xkzu__badde.minute)
    pizca__jod = c.pyapi.long_from_longlong(xkzu__badde.second)
    dqn__uzoeh = c.pyapi.long_from_longlong(xkzu__badde.microsecond)
    zaax__ptrft = c.pyapi.long_from_longlong(xkzu__badde.nanosecond)
    dnvp__pyj = c.pyapi.unserialize(c.pyapi.serialize_object(pd.Timestamp))
    if typ.tz is None:
        res = c.pyapi.call_function_objargs(dnvp__pyj, (ynmk__scmp,
            rwp__epbe, kvaud__tark, vznd__scyv, njcc__jli, pizca__jod,
            dqn__uzoeh, zaax__ptrft))
    else:
        if isinstance(typ.tz, int):
            doio__wfc = c.pyapi.long_from_longlong(lir.Constant(lir.IntType
                (64), typ.tz))
        else:
            sawz__ieit = c.context.insert_const_string(c.builder.module,
                str(typ.tz))
            doio__wfc = c.pyapi.string_from_string(sawz__ieit)
        args = c.pyapi.tuple_pack(())
        kwargs = c.pyapi.dict_pack([('year', ynmk__scmp), ('month',
            rwp__epbe), ('day', kvaud__tark), ('hour', vznd__scyv), (
            'minute', njcc__jli), ('second', pizca__jod), ('microsecond',
            dqn__uzoeh), ('nanosecond', zaax__ptrft), ('tz', doio__wfc)])
        res = c.pyapi.call(dnvp__pyj, args, kwargs)
        c.pyapi.decref(args)
        c.pyapi.decref(kwargs)
        c.pyapi.decref(doio__wfc)
    c.pyapi.decref(ynmk__scmp)
    c.pyapi.decref(rwp__epbe)
    c.pyapi.decref(kvaud__tark)
    c.pyapi.decref(vznd__scyv)
    c.pyapi.decref(njcc__jli)
    c.pyapi.decref(pizca__jod)
    c.pyapi.decref(dqn__uzoeh)
    c.pyapi.decref(zaax__ptrft)
    return res


@intrinsic
def init_timestamp(typingctx, year, month, day, hour, minute, second,
    microsecond, nanosecond, value, tz):

    def codegen(context, builder, sig, args):
        (year, month, day, hour, minute, second, bei__lgo, fkjho__xykf,
            value, iwn__wui) = args
        ts = cgutils.create_struct_proxy(sig.return_type)(context, builder)
        ts.year = year
        ts.month = month
        ts.day = day
        ts.hour = hour
        ts.minute = minute
        ts.second = second
        ts.microsecond = bei__lgo
        ts.nanosecond = fkjho__xykf
        ts.value = value
        return ts._getvalue()
    if is_overload_none(tz):
        typ = pd_timestamp_tz_naive_type
    elif is_overload_constant_str(tz):
        typ = PandasTimestampType(get_overload_const_str(tz))
    elif is_overload_constant_int(tz):
        typ = PandasTimestampType(get_overload_const_int(tz))
    else:
        raise_bodo_error('tz must be a constant string, int, or None')
    return typ(types.int64, types.int64, types.int64, types.int64, types.
        int64, types.int64, types.int64, types.int64, types.int64, tz), codegen


@numba.generated_jit
def zero_if_none(value):
    if value == types.none:
        return lambda value: 0
    return lambda value: value


@lower_constant(PandasTimestampType)
def constant_timestamp(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    hour = context.get_constant(types.int64, pyval.hour)
    minute = context.get_constant(types.int64, pyval.minute)
    second = context.get_constant(types.int64, pyval.second)
    microsecond = context.get_constant(types.int64, pyval.microsecond)
    nanosecond = context.get_constant(types.int64, pyval.nanosecond)
    value = context.get_constant(types.int64, pyval.value)
    return lir.Constant.literal_struct((year, month, day, hour, minute,
        second, microsecond, nanosecond, value))


def tz_has_transition_times(tz: Union[str, int, None]):
    if isinstance(tz, str):
        bdau__xwfzq = pytz.timezone(tz)
        return isinstance(bdau__xwfzq, pytz.tzinfo.DstTzInfo)
    return False


@overload(pd.Timestamp, no_unliteral=True)
def overload_pd_timestamp(ts_input=_no_input, freq=None, tz=None, unit=None,
    year=None, month=None, day=None, hour=None, minute=None, second=None,
    microsecond=None, nanosecond=None, tzinfo=None):
    if not is_overload_none(tz) and is_overload_constant_str(tz
        ) and get_overload_const_str(tz) not in pytz.all_timezones_set:
        raise BodoError(
            "pandas.Timestamp(): 'tz', if provided, must be constant string found in pytz.all_timezones"
            )
    if ts_input == _no_input or getattr(ts_input, 'value', None) == _no_input:

        def impl_kw(ts_input=_no_input, freq=None, tz=None, unit=None, year
            =None, month=None, day=None, hour=None, minute=None, second=
            None, microsecond=None, nanosecond=None, tzinfo=None):
            return compute_val_for_timestamp(year, month, day, zero_if_none
                (hour), zero_if_none(minute), zero_if_none(second),
                zero_if_none(microsecond), zero_if_none(nanosecond), tz)
        return impl_kw
    if isinstance(types.unliteral(freq), types.Integer):

        def impl_pos(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            return compute_val_for_timestamp(ts_input, freq, tz,
                zero_if_none(unit), zero_if_none(year), zero_if_none(month),
                zero_if_none(day), zero_if_none(hour), None)
        return impl_pos
    if isinstance(ts_input, types.Number):
        if is_overload_none(unit):
            unit = 'ns'
        if not is_overload_constant_str(unit):
            raise BodoError(
                'pandas.Timedelta(): unit argument must be a constant str')
        unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
            get_overload_const_str(unit))
        wosa__xjwh, precision = pd._libs.tslibs.conversion.precision_from_unit(
            unit)
        if isinstance(ts_input, types.Integer):

            def impl_int(ts_input=_no_input, freq=None, tz=None, unit=None,
                year=None, month=None, day=None, hour=None, minute=None,
                second=None, microsecond=None, nanosecond=None, tzinfo=None):
                value = ts_input * wosa__xjwh
                return convert_val_to_timestamp(value, tz)
            return impl_int

        def impl_float(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            pvcbr__azgny = np.int64(ts_input)
            pofz__ehqab = ts_input - pvcbr__azgny
            if precision:
                pofz__ehqab = np.round(pofz__ehqab, precision)
            value = pvcbr__azgny * wosa__xjwh + np.int64(pofz__ehqab *
                wosa__xjwh)
            return convert_val_to_timestamp(value, tz)
        return impl_float
    if ts_input == bodo.string_type or is_overload_constant_str(ts_input):
        types.pd_timestamp_tz_naive_type = pd_timestamp_tz_naive_type
        if is_overload_none(tz):
            tz_val = None
        elif is_overload_constant_str(tz):
            tz_val = get_overload_const_str(tz)
        else:
            raise_bodo_error(
                'pandas.Timestamp(): tz argument must be a constant string or None'
                )
        typ = PandasTimestampType(tz_val)

        def impl_str(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            with numba.objmode(res=typ):
                res = pd.Timestamp(ts_input, tz=tz)
            return res
        return impl_str
    if isinstance(ts_input, PandasTimestampType):
        return (lambda ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None: ts_input)
    if ts_input == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:

        def impl_datetime(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            year = ts_input.year
            month = ts_input.month
            day = ts_input.day
            hour = ts_input.hour
            minute = ts_input.minute
            second = ts_input.second
            microsecond = ts_input.microsecond
            return compute_val_for_timestamp(year, month, day, zero_if_none
                (hour), zero_if_none(minute), zero_if_none(second),
                zero_if_none(microsecond), zero_if_none(nanosecond), tz)
        return impl_datetime
    if ts_input == bodo.hiframes.datetime_date_ext.datetime_date_type:

        def impl_date(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            year = ts_input.year
            month = ts_input.month
            day = ts_input.day
            return compute_val_for_timestamp(year, month, day, zero_if_none
                (hour), zero_if_none(minute), zero_if_none(second),
                zero_if_none(microsecond), zero_if_none(nanosecond), tz)
        return impl_date
    if isinstance(ts_input, numba.core.types.scalars.NPDatetime):
        wosa__xjwh, precision = pd._libs.tslibs.conversion.precision_from_unit(
            ts_input.unit)

        def impl_date(ts_input=_no_input, freq=None, tz=None, unit=None,
            year=None, month=None, day=None, hour=None, minute=None, second
            =None, microsecond=None, nanosecond=None, tzinfo=None):
            value = np.int64(ts_input) * wosa__xjwh
            return convert_val_to_timestamp(value, tz)
        return impl_date


@overload_attribute(PandasTimestampType, 'dayofyear')
@overload_attribute(PandasTimestampType, 'day_of_year')
def overload_pd_dayofyear(ptt):

    def pd_dayofyear(ptt):
        return get_day_of_year(ptt.year, ptt.month, ptt.day)
    return pd_dayofyear


@overload_method(PandasTimestampType, 'weekday')
@overload_attribute(PandasTimestampType, 'dayofweek')
@overload_attribute(PandasTimestampType, 'day_of_week')
def overload_pd_dayofweek(ptt):

    def pd_dayofweek(ptt):
        return get_day_of_week(ptt.year, ptt.month, ptt.day)
    return pd_dayofweek


@overload_attribute(PandasTimestampType, 'week')
@overload_attribute(PandasTimestampType, 'weekofyear')
def overload_week_number(ptt):

    def pd_week_number(ptt):
        iwn__wui, lmzci__yapgm, iwn__wui = get_isocalendar(ptt.year, ptt.
            month, ptt.day)
        return lmzci__yapgm
    return pd_week_number


@overload_method(PandasTimestampType, '__hash__', no_unliteral=True)
def dt64_hash(val):
    return lambda val: hash(val.value)


@overload_attribute(PandasTimestampType, 'days_in_month')
@overload_attribute(PandasTimestampType, 'daysinmonth')
def overload_pd_daysinmonth(ptt):

    def pd_daysinmonth(ptt):
        return get_days_in_month(ptt.year, ptt.month)
    return pd_daysinmonth


@overload_attribute(PandasTimestampType, 'is_leap_year')
def overload_pd_is_leap_year(ptt):

    def pd_is_leap_year(ptt):
        return is_leap_year(ptt.year)
    return pd_is_leap_year


@overload_attribute(PandasTimestampType, 'is_month_start')
def overload_pd_is_month_start(ptt):

    def pd_is_month_start(ptt):
        return ptt.day == 1
    return pd_is_month_start


@overload_attribute(PandasTimestampType, 'is_month_end')
def overload_pd_is_month_end(ptt):

    def pd_is_month_end(ptt):
        return ptt.day == get_days_in_month(ptt.year, ptt.month)
    return pd_is_month_end


@overload_attribute(PandasTimestampType, 'is_quarter_start')
def overload_pd_is_quarter_start(ptt):

    def pd_is_quarter_start(ptt):
        return ptt.day == 1 and ptt.month % 3 == 1
    return pd_is_quarter_start


@overload_attribute(PandasTimestampType, 'is_quarter_end')
def overload_pd_is_quarter_end(ptt):

    def pd_is_quarter_end(ptt):
        return ptt.month % 3 == 0 and ptt.day == get_days_in_month(ptt.year,
            ptt.month)
    return pd_is_quarter_end


@overload_attribute(PandasTimestampType, 'is_year_start')
def overload_pd_is_year_start(ptt):

    def pd_is_year_start(ptt):
        return ptt.day == 1 and ptt.month == 1
    return pd_is_year_start


@overload_attribute(PandasTimestampType, 'is_year_end')
def overload_pd_is_year_end(ptt):

    def pd_is_year_end(ptt):
        return ptt.day == 31 and ptt.month == 12
    return pd_is_year_end


@overload_attribute(PandasTimestampType, 'quarter')
def overload_quarter(ptt):

    def quarter(ptt):
        return (ptt.month - 1) // 3 + 1
    return quarter


@overload_method(PandasTimestampType, 'date', no_unliteral=True)
def overload_pd_timestamp_date(ptt):

    def pd_timestamp_date_impl(ptt):
        return datetime.date(ptt.year, ptt.month, ptt.day)
    return pd_timestamp_date_impl


@overload_method(PandasTimestampType, 'isocalendar', no_unliteral=True)
def overload_pd_timestamp_isocalendar(ptt):

    def impl(ptt):
        year, lmzci__yapgm, mtcxn__dumni = get_isocalendar(ptt.year, ptt.
            month, ptt.day)
        return year, lmzci__yapgm, mtcxn__dumni
    return impl


@overload_method(PandasTimestampType, 'isoformat', no_unliteral=True)
def overload_pd_timestamp_isoformat(ts, sep=None):
    if is_overload_none(sep):

        def timestamp_isoformat_impl(ts, sep=None):
            hrfx__ahp = str_2d(ts.hour) + ':' + str_2d(ts.minute
                ) + ':' + str_2d(ts.second)
            if ts.microsecond != 0:
                hrfx__ahp += '.' + str_2d(ts.microsecond)
                if ts.nanosecond != 0:
                    hrfx__ahp += str_2d(ts.nanosecond)
            res = str(ts.year) + '-' + str_2d(ts.month) + '-' + str_2d(ts.day
                ) + 'T' + hrfx__ahp
            return res
        return timestamp_isoformat_impl
    else:

        def timestamp_isoformat_impl(ts, sep=None):
            hrfx__ahp = str_2d(ts.hour) + ':' + str_2d(ts.minute
                ) + ':' + str_2d(ts.second)
            if ts.microsecond != 0:
                hrfx__ahp += '.' + str_2d(ts.microsecond)
                if ts.nanosecond != 0:
                    hrfx__ahp += str_2d(ts.nanosecond)
            res = str(ts.year) + '-' + str_2d(ts.month) + '-' + str_2d(ts.day
                ) + sep + hrfx__ahp
            return res
    return timestamp_isoformat_impl


@overload_method(PandasTimestampType, 'normalize', no_unliteral=True)
def overload_pd_timestamp_normalize(ptt):
    tz_literal = ptt.tz

    def impl(ptt):
        return pd.Timestamp(year=ptt.year, month=ptt.month, day=ptt.day, tz
            =tz_literal)
    return impl


@overload_method(PandasTimestampType, 'day_name', no_unliteral=True)
def overload_pd_timestamp_day_name(ptt, locale=None):
    zpnml__tafcx = dict(locale=locale)
    buh__oiib = dict(locale=None)
    check_unsupported_args('Timestamp.day_name', zpnml__tafcx, buh__oiib,
        package_name='pandas', module_name='Timestamp')

    def impl(ptt, locale=None):
        ywe__rolhv = ('Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday')
        iwn__wui, iwn__wui, awkm__jxr = ptt.isocalendar()
        return ywe__rolhv[awkm__jxr - 1]
    return impl


@overload_method(PandasTimestampType, 'month_name', no_unliteral=True)
def overload_pd_timestamp_month_name(ptt, locale=None):
    zpnml__tafcx = dict(locale=locale)
    buh__oiib = dict(locale=None)
    check_unsupported_args('Timestamp.month_name', zpnml__tafcx, buh__oiib,
        package_name='pandas', module_name='Timestamp')

    def impl(ptt, locale=None):
        hlp__xlxsc = ('January', 'February', 'March', 'April', 'May',
            'June', 'July', 'August', 'September', 'October', 'November',
            'December')
        return hlp__xlxsc[ptt.month - 1]
    return impl


@overload_method(PandasTimestampType, 'tz_convert', no_unliteral=True)
def overload_pd_timestamp_tz_convert(ptt, tz):
    if ptt.tz is None:
        raise BodoError(
            'Cannot convert tz-naive Timestamp, use tz_localize to localize')
    if is_overload_none(tz):
        return lambda ptt, tz: convert_val_to_timestamp(ptt.value)
    elif is_overload_constant_str(tz):
        return lambda ptt, tz: convert_val_to_timestamp(ptt.value, tz=tz)


@overload_method(PandasTimestampType, 'tz_localize', no_unliteral=True)
def overload_pd_timestamp_tz_localize(ptt, tz, ambiguous='raise',
    nonexistent='raise'):
    if ptt.tz is not None and not is_overload_none(tz):
        raise BodoError(
            'Cannot localize tz-aware Timestamp, use tz_convert for conversions'
            )
    zpnml__tafcx = dict(ambiguous=ambiguous, nonexistent=nonexistent)
    jrc__meze = dict(ambiguous='raise', nonexistent='raise')
    check_unsupported_args('Timestamp.tz_localize', zpnml__tafcx, jrc__meze,
        package_name='pandas', module_name='Timestamp')
    if is_overload_none(tz) and ptt.tz is None:
        return lambda ptt, tz, ambiguous='raise', nonexistent='raise': ptt
    if is_overload_none(tz):
        clz__vvv = ptt.tz
        wtqf__fegcq = False
    else:
        if not is_literal_type(tz):
            raise_bodo_error(
                'Timestamp.tz_localize(): tz value must be a literal string, integer, or None'
                )
        clz__vvv = get_literal_value(tz)
        wtqf__fegcq = True
    aprg__sxgan = None
    oxoxd__nztjh = None
    lnuqq__aua = False
    if tz_has_transition_times(clz__vvv):
        lnuqq__aua = wtqf__fegcq
        doio__wfc = pytz.timezone(clz__vvv)
        oxoxd__nztjh = np.array(doio__wfc._utc_transition_times, dtype='M8[ns]'
            ).view('i8')
        aprg__sxgan = np.array(doio__wfc._transition_info)[:, 0]
        aprg__sxgan = (pd.Series(aprg__sxgan).dt.total_seconds() * 1000000000
            ).astype(np.int64).values
        uysbo__vqz = "deltas[np.searchsorted(trans, value, side='right') - 1]"
    elif isinstance(clz__vvv, str):
        doio__wfc = pytz.timezone(clz__vvv)
        uysbo__vqz = str(np.int64(doio__wfc._utcoffset.total_seconds() * 
            1000000000))
    elif isinstance(clz__vvv, int):
        uysbo__vqz = str(clz__vvv)
    else:
        raise_bodo_error(
            'Timestamp.tz_localize(): tz value must be a literal string, integer, or None'
            )
    if wtqf__fegcq:
        tjagq__dkap = '-'
    else:
        tjagq__dkap = '+'
    cceg__wdv = "def impl(ptt, tz, ambiguous='raise', nonexistent='raise'):\n"
    cceg__wdv += f'    value =  ptt.value\n'
    cceg__wdv += f'    delta =  {uysbo__vqz}\n'
    cceg__wdv += f'    new_value = value {tjagq__dkap} delta\n'
    if lnuqq__aua:
        cceg__wdv += """    end_delta = deltas[np.searchsorted(trans, new_value, side='right') - 1]
"""
        cceg__wdv += '    offset = delta - end_delta\n'
        cceg__wdv += '    new_value = new_value + offset\n'
    cceg__wdv += f'    return convert_val_to_timestamp(new_value, tz=tz)\n'
    dkvdd__yesje = {}
    exec(cceg__wdv, {'np': np, 'convert_val_to_timestamp':
        convert_val_to_timestamp, 'trans': oxoxd__nztjh, 'deltas':
        aprg__sxgan}, dkvdd__yesje)
    impl = dkvdd__yesje['impl']
    return impl


@numba.njit
def str_2d(a):
    res = str(a)
    if len(res) == 1:
        return '0' + res
    return res


@overload(str, no_unliteral=True)
def ts_str_overload(a):
    if a == pd_timestamp_tz_naive_type:
        return lambda a: a.isoformat(' ')


@intrinsic
def extract_year_days(typingctx, dt64_t=None):
    assert dt64_t in (types.int64, types.NPDatetime('ns'))

    def codegen(context, builder, sig, args):
        eyqyq__udn = cgutils.alloca_once(builder, lir.IntType(64))
        builder.store(args[0], eyqyq__udn)
        year = cgutils.alloca_once(builder, lir.IntType(64))
        vyyir__uxzfm = cgutils.alloca_once(builder, lir.IntType(64))
        hno__azat = lir.FunctionType(lir.VoidType(), [lir.IntType(64).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer()])
        mnvc__bhdax = cgutils.get_or_insert_function(builder.module,
            hno__azat, name='extract_year_days')
        builder.call(mnvc__bhdax, [eyqyq__udn, year, vyyir__uxzfm])
        return cgutils.pack_array(builder, [builder.load(eyqyq__udn),
            builder.load(year), builder.load(vyyir__uxzfm)])
    return types.Tuple([types.int64, types.int64, types.int64])(dt64_t
        ), codegen


@intrinsic
def get_month_day(typingctx, year_t, days_t=None):
    assert year_t == types.int64
    assert days_t == types.int64

    def codegen(context, builder, sig, args):
        month = cgutils.alloca_once(builder, lir.IntType(64))
        day = cgutils.alloca_once(builder, lir.IntType(64))
        hno__azat = lir.FunctionType(lir.VoidType(), [lir.IntType(64), lir.
            IntType(64), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer()])
        mnvc__bhdax = cgutils.get_or_insert_function(builder.module,
            hno__azat, name='get_month_day')
        builder.call(mnvc__bhdax, [args[0], args[1], month, day])
        return cgutils.pack_array(builder, [builder.load(month), builder.
            load(day)])
    return types.Tuple([types.int64, types.int64])(types.int64, types.int64
        ), codegen


@register_jitable
def get_day_of_year(year, month, day):
    lcpgw__nmrmj = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 
        365, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
    xyfi__rcqzs = is_leap_year(year)
    tia__xss = lcpgw__nmrmj[xyfi__rcqzs * 13 + month - 1]
    yzute__dhgsp = tia__xss + day
    return yzute__dhgsp


@register_jitable
def get_day_of_week(y, m, d):
    toutj__xqcku = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    y -= m < 3
    day = (y + y // 4 - y // 100 + y // 400 + toutj__xqcku[m - 1] + d) % 7
    return (day + 6) % 7


@register_jitable
def get_days_in_month(year, month):
    is_leap_year = year & 3 == 0 and (year % 100 != 0 or year % 400 == 0)
    eymg__pyf = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 29, 31,
        30, 31, 30, 31, 31, 30, 31, 30, 31]
    return eymg__pyf[12 * is_leap_year + month - 1]


@register_jitable
def is_leap_year(year):
    return year & 3 == 0 and (year % 100 != 0 or year % 400 == 0)


@numba.generated_jit(nopython=True)
def compute_val_for_timestamp(year, month, day, hour, minute, second,
    microsecond, nanosecond, tz):
    uysbo__vqz = '0'
    clz__vvv = get_literal_value(tz)
    aprg__sxgan = None
    oxoxd__nztjh = None
    lnuqq__aua = False
    if tz_has_transition_times(clz__vvv):
        lnuqq__aua = True
        doio__wfc = pytz.timezone(clz__vvv)
        oxoxd__nztjh = np.array(doio__wfc._utc_transition_times, dtype='M8[ns]'
            ).view('i8')
        aprg__sxgan = np.array(doio__wfc._transition_info)[:, 0]
        aprg__sxgan = (pd.Series(aprg__sxgan).dt.total_seconds() * 1000000000
            ).astype(np.int64).values
        uysbo__vqz = (
            "deltas[np.searchsorted(trans, original_value, side='right') - 1]")
    elif isinstance(clz__vvv, str):
        doio__wfc = pytz.timezone(clz__vvv)
        uysbo__vqz = str(np.int64(doio__wfc._utcoffset.total_seconds() * 
            1000000000))
    elif isinstance(clz__vvv, int):
        uysbo__vqz = str(clz__vvv)
    elif clz__vvv is not None:
        raise_bodo_error(
            'compute_val_for_timestamp(): tz value must be a constant string, integer or None'
            )
    cceg__wdv = (
        'def impl(year, month, day, hour, minute, second, microsecond, nanosecond, tz):\n'
        )
    cceg__wdv += f"""  original_value = npy_datetimestruct_to_datetime(year, month, day, hour, minute, second, microsecond) + nanosecond
"""
    cceg__wdv += f'  value = original_value - {uysbo__vqz}\n'
    if lnuqq__aua:
        cceg__wdv += (
            "  start_trans = np.searchsorted(trans, original_value, side='right') - 1\n"
            )
        cceg__wdv += (
            "  end_trans = np.searchsorted(trans, value, side='right') - 1\n")
        cceg__wdv += '  offset = deltas[start_trans] - deltas[end_trans]\n'
        cceg__wdv += '  value = value + offset\n'
    cceg__wdv += '  return init_timestamp(\n'
    cceg__wdv += '    year=year,\n'
    cceg__wdv += '    month=month,\n'
    cceg__wdv += '    day=day,\n'
    cceg__wdv += '    hour=hour,\n'
    cceg__wdv += '    minute=minute,'
    cceg__wdv += '    second=second,\n'
    cceg__wdv += '    microsecond=microsecond,\n'
    cceg__wdv += '    nanosecond=nanosecond,\n'
    cceg__wdv += f'    value=value,\n'
    cceg__wdv += '    tz=tz,\n'
    cceg__wdv += '  )\n'
    dkvdd__yesje = {}
    exec(cceg__wdv, {'np': np, 'pd': pd, 'init_timestamp': init_timestamp,
        'npy_datetimestruct_to_datetime': npy_datetimestruct_to_datetime,
        'trans': oxoxd__nztjh, 'deltas': aprg__sxgan}, dkvdd__yesje)
    impl = dkvdd__yesje['impl']
    return impl


@numba.generated_jit(nopython=True)
def convert_val_to_timestamp(ts_input, tz=None, is_convert=True):
    oxoxd__nztjh = aprg__sxgan = np.array([])
    uysbo__vqz = '0'
    if is_overload_constant_str(tz):
        sawz__ieit = get_overload_const_str(tz)
        doio__wfc = pytz.timezone(sawz__ieit)
        if isinstance(doio__wfc, pytz.tzinfo.DstTzInfo):
            oxoxd__nztjh = np.array(doio__wfc._utc_transition_times, dtype=
                'M8[ns]').view('i8')
            aprg__sxgan = np.array(doio__wfc._transition_info)[:, 0]
            aprg__sxgan = (pd.Series(aprg__sxgan).dt.total_seconds() * 
                1000000000).astype(np.int64).values
            uysbo__vqz = (
                "deltas[np.searchsorted(trans, ts_input, side='right') - 1]")
        else:
            aprg__sxgan = np.int64(doio__wfc._utcoffset.total_seconds() * 
                1000000000)
            uysbo__vqz = 'deltas'
    elif is_overload_constant_int(tz):
        ugst__vix = get_overload_const_int(tz)
        uysbo__vqz = str(ugst__vix)
    elif not is_overload_none(tz):
        raise_bodo_error(
            'convert_val_to_timestamp(): tz value must be a constant string or None'
            )
    is_convert = get_overload_const_bool(is_convert)
    if is_convert:
        jvjt__bkdg = 'tz_ts_input'
        jsy__vax = 'ts_input'
    else:
        jvjt__bkdg = 'ts_input'
        jsy__vax = 'tz_ts_input'
    cceg__wdv = 'def impl(ts_input, tz=None, is_convert=True):\n'
    cceg__wdv += f'  tz_ts_input = ts_input + {uysbo__vqz}\n'
    cceg__wdv += (
        f'  dt, year, days = extract_year_days(integer_to_dt64({jvjt__bkdg}))\n'
        )
    cceg__wdv += '  month, day = get_month_day(year, days)\n'
    cceg__wdv += '  return init_timestamp(\n'
    cceg__wdv += '    year=year,\n'
    cceg__wdv += '    month=month,\n'
    cceg__wdv += '    day=day,\n'
    cceg__wdv += '    hour=dt // (60 * 60 * 1_000_000_000),\n'
    cceg__wdv += '    minute=(dt // (60 * 1_000_000_000)) % 60,\n'
    cceg__wdv += '    second=(dt // 1_000_000_000) % 60,\n'
    cceg__wdv += '    microsecond=(dt // 1000) % 1_000_000,\n'
    cceg__wdv += '    nanosecond=dt % 1000,\n'
    cceg__wdv += f'    value={jsy__vax},\n'
    cceg__wdv += '    tz=tz,\n'
    cceg__wdv += '  )\n'
    dkvdd__yesje = {}
    exec(cceg__wdv, {'np': np, 'pd': pd, 'trans': oxoxd__nztjh, 'deltas':
        aprg__sxgan, 'integer_to_dt64': integer_to_dt64,
        'extract_year_days': extract_year_days, 'get_month_day':
        get_month_day, 'init_timestamp': init_timestamp, 'zero_if_none':
        zero_if_none}, dkvdd__yesje)
    impl = dkvdd__yesje['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def convert_datetime64_to_timestamp(dt64):
    eyqyq__udn, year, vyyir__uxzfm = extract_year_days(dt64)
    month, day = get_month_day(year, vyyir__uxzfm)
    return init_timestamp(year=year, month=month, day=day, hour=eyqyq__udn //
        (60 * 60 * 1000000000), minute=eyqyq__udn // (60 * 1000000000) % 60,
        second=eyqyq__udn // 1000000000 % 60, microsecond=eyqyq__udn // 
        1000 % 1000000, nanosecond=eyqyq__udn % 1000, value=dt64, tz=None)


@numba.njit(no_cpython_wrapper=True)
def convert_numpy_timedelta64_to_datetime_timedelta(dt64):
    hihxc__gtab = (bodo.hiframes.datetime_timedelta_ext.
        cast_numpy_timedelta_to_int(dt64))
    pto__ewt = hihxc__gtab // (86400 * 1000000000)
    gmq__xamip = hihxc__gtab - pto__ewt * 86400 * 1000000000
    reerr__qlv = gmq__xamip // 1000000000
    eqxlr__zyqzj = gmq__xamip - reerr__qlv * 1000000000
    ddeuk__ujj = eqxlr__zyqzj // 1000
    return datetime.timedelta(pto__ewt, reerr__qlv, ddeuk__ujj)


@numba.njit(no_cpython_wrapper=True)
def convert_numpy_timedelta64_to_pd_timedelta(dt64):
    hihxc__gtab = (bodo.hiframes.datetime_timedelta_ext.
        cast_numpy_timedelta_to_int(dt64))
    return pd.Timedelta(hihxc__gtab)


@intrinsic
def integer_to_timedelta64(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.NPTimedelta('ns')(val), codegen


@intrinsic
def integer_to_dt64(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.NPDatetime('ns')(val), codegen


@intrinsic
def dt64_to_integer(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.int64(val), codegen


@lower_cast(types.NPDatetime('ns'), types.int64)
def cast_dt64_to_integer(context, builder, fromty, toty, val):
    return val


@overload_method(types.NPDatetime, '__hash__', no_unliteral=True)
def dt64_hash(val):
    return lambda val: hash(dt64_to_integer(val))


@overload_method(types.NPTimedelta, '__hash__', no_unliteral=True)
def td64_hash(val):
    return lambda val: hash(dt64_to_integer(val))


@intrinsic
def timedelta64_to_integer(typingctx, val=None):

    def codegen(context, builder, sig, args):
        return args[0]
    return types.int64(val), codegen


@lower_cast(bodo.timedelta64ns, types.int64)
def cast_td64_to_integer(context, builder, fromty, toty, val):
    return val


@numba.njit
def parse_datetime_str(val):
    with numba.objmode(res='int64'):
        res = pd.Timestamp(val).value
    return integer_to_dt64(res)


@numba.njit
def datetime_timedelta_to_timedelta64(val):
    with numba.objmode(res='NPTimedelta("ns")'):
        res = pd.to_timedelta(val)
        res = res.to_timedelta64()
    return res


@numba.njit
def series_str_dt64_astype(data):
    with numba.objmode(res="NPDatetime('ns')[::1]"):
        res = pd.Series(data.to_numpy()).astype('datetime64[ns]').values
    return res


@numba.njit
def series_str_td64_astype(data):
    with numba.objmode(res="NPTimedelta('ns')[::1]"):
        res = data.astype('timedelta64[ns]')
    return res


@numba.njit
def datetime_datetime_to_dt64(val):
    with numba.objmode(res='NPDatetime("ns")'):
        res = np.datetime64(val).astype('datetime64[ns]')
    return res


@register_jitable
def datetime_date_arr_to_dt64_arr(arr):
    with numba.objmode(res='NPDatetime("ns")[::1]'):
        res = np.array(arr, dtype='datetime64[ns]')
    return res


types.pd_timestamp_tz_naive_type = pd_timestamp_tz_naive_type


@register_jitable
def to_datetime_scalar(a, errors='raise', dayfirst=False, yearfirst=False,
    utc=None, format=None, exact=True, unit=None, infer_datetime_format=
    False, origin='unix', cache=True):
    with numba.objmode(t='pd_timestamp_tz_naive_type'):
        t = pd.to_datetime(a, errors=errors, dayfirst=dayfirst, yearfirst=
            yearfirst, utc=utc, format=format, exact=exact, unit=unit,
            infer_datetime_format=infer_datetime_format, origin=origin,
            cache=cache)
    return t


@numba.njit
def pandas_string_array_to_datetime(arr, errors, dayfirst, yearfirst, utc,
    format, exact, unit, infer_datetime_format, origin, cache):
    with numba.objmode(result='datetime_index'):
        result = pd.to_datetime(arr, errors=errors, dayfirst=dayfirst,
            yearfirst=yearfirst, utc=utc, format=format, exact=exact, unit=
            unit, infer_datetime_format=infer_datetime_format, origin=
            origin, cache=cache)
    return result


@numba.njit
def pandas_dict_string_array_to_datetime(arr, errors, dayfirst, yearfirst,
    utc, format, exact, unit, infer_datetime_format, origin, cache):
    kaa__hyqy = len(arr)
    eeo__nkkuz = np.empty(kaa__hyqy, 'datetime64[ns]')
    vkb__zbh = arr._indices
    xbh__pwq = pandas_string_array_to_datetime(arr._data, errors, dayfirst,
        yearfirst, utc, format, exact, unit, infer_datetime_format, origin,
        cache).values
    for iuqi__mggdl in range(kaa__hyqy):
        if bodo.libs.array_kernels.isna(vkb__zbh, iuqi__mggdl):
            bodo.libs.array_kernels.setna(eeo__nkkuz, iuqi__mggdl)
            continue
        eeo__nkkuz[iuqi__mggdl] = xbh__pwq[vkb__zbh[iuqi__mggdl]]
    return eeo__nkkuz


@overload(pd.to_datetime, inline='always', no_unliteral=True)
def overload_to_datetime(arg_a, errors='raise', dayfirst=False, yearfirst=
    False, utc=None, format=None, exact=True, unit=None,
    infer_datetime_format=False, origin='unix', cache=True):
    umgn__evckk = {'errors': errors}
    xdg__okc = {'errors': 'raise'}
    check_unsupported_args('pd.to_datetime', umgn__evckk, xdg__okc,
        package_name='pandas')
    if arg_a == bodo.string_type or is_overload_constant_str(arg_a
        ) or is_overload_constant_int(arg_a) or isinstance(arg_a, types.Integer
        ):

        def pd_to_datetime_impl(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return to_datetime_scalar(arg_a, errors=errors, dayfirst=
                dayfirst, yearfirst=yearfirst, utc=utc, format=format,
                exact=exact, unit=unit, infer_datetime_format=
                infer_datetime_format, origin=origin, cache=cache)
        return pd_to_datetime_impl
    if isinstance(arg_a, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            mgqk__luljf = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            vvu__xdwrj = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            mvv__ykhq = bodo.utils.conversion.coerce_to_ndarray(pd.
                to_datetime(arr, errors=errors, dayfirst=dayfirst,
                yearfirst=yearfirst, utc=utc, format=format, exact=exact,
                unit=unit, infer_datetime_format=infer_datetime_format,
                origin=origin, cache=cache))
            return bodo.hiframes.pd_series_ext.init_series(mvv__ykhq,
                mgqk__luljf, vvu__xdwrj)
        return impl_series
    if arg_a == bodo.hiframes.datetime_date_ext.datetime_date_array_type:
        qcte__lokn = np.dtype('datetime64[ns]')
        iNaT = pd._libs.tslibs.iNaT

        def impl_date_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            kaa__hyqy = len(arg_a)
            eeo__nkkuz = np.empty(kaa__hyqy, qcte__lokn)
            for iuqi__mggdl in numba.parfors.parfor.internal_prange(kaa__hyqy):
                val = iNaT
                if not bodo.libs.array_kernels.isna(arg_a, iuqi__mggdl):
                    data = arg_a[iuqi__mggdl]
                    val = (bodo.hiframes.pd_timestamp_ext.
                        npy_datetimestruct_to_datetime(data.year, data.
                        month, data.day, 0, 0, 0, 0))
                eeo__nkkuz[iuqi__mggdl
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(val)
            return bodo.hiframes.pd_index_ext.init_datetime_index(eeo__nkkuz,
                None)
        return impl_date_arr
    if arg_a == types.Array(types.NPDatetime('ns'), 1, 'C'):
        return (lambda arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True: bodo.
            hiframes.pd_index_ext.init_datetime_index(arg_a, None))
    if arg_a == string_array_type:

        def impl_string_array(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return pandas_string_array_to_datetime(arg_a, errors, dayfirst,
                yearfirst, utc, format, exact, unit, infer_datetime_format,
                origin, cache)
        return impl_string_array
    if isinstance(arg_a, types.Array) and isinstance(arg_a.dtype, types.Integer
        ):
        qcte__lokn = np.dtype('datetime64[ns]')

        def impl_date_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            kaa__hyqy = len(arg_a)
            eeo__nkkuz = np.empty(kaa__hyqy, qcte__lokn)
            for iuqi__mggdl in numba.parfors.parfor.internal_prange(kaa__hyqy):
                data = arg_a[iuqi__mggdl]
                val = to_datetime_scalar(data, errors=errors, dayfirst=
                    dayfirst, yearfirst=yearfirst, utc=utc, format=format,
                    exact=exact, unit=unit, infer_datetime_format=
                    infer_datetime_format, origin=origin, cache=cache)
                eeo__nkkuz[iuqi__mggdl
                    ] = bodo.hiframes.pd_timestamp_ext.datetime_datetime_to_dt64(
                    val)
            return bodo.hiframes.pd_index_ext.init_datetime_index(eeo__nkkuz,
                None)
        return impl_date_arr
    if isinstance(arg_a, CategoricalArrayType
        ) and arg_a.dtype.elem_type == bodo.string_type:
        qcte__lokn = np.dtype('datetime64[ns]')

        def impl_cat_arr(arg_a, errors='raise', dayfirst=False, yearfirst=
            False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            kaa__hyqy = len(arg_a)
            eeo__nkkuz = np.empty(kaa__hyqy, qcte__lokn)
            zxae__gnjv = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arg_a))
            xbh__pwq = pandas_string_array_to_datetime(arg_a.dtype.
                categories.values, errors, dayfirst, yearfirst, utc, format,
                exact, unit, infer_datetime_format, origin, cache).values
            for iuqi__mggdl in numba.parfors.parfor.internal_prange(kaa__hyqy):
                c = zxae__gnjv[iuqi__mggdl]
                if c == -1:
                    bodo.libs.array_kernels.setna(eeo__nkkuz, iuqi__mggdl)
                    continue
                eeo__nkkuz[iuqi__mggdl] = xbh__pwq[c]
            return bodo.hiframes.pd_index_ext.init_datetime_index(eeo__nkkuz,
                None)
        return impl_cat_arr
    if arg_a == bodo.dict_str_arr_type:

        def impl_dict_str_arr(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            eeo__nkkuz = pandas_dict_string_array_to_datetime(arg_a, errors,
                dayfirst, yearfirst, utc, format, exact, unit,
                infer_datetime_format, origin, cache)
            return bodo.hiframes.pd_index_ext.init_datetime_index(eeo__nkkuz,
                None)
        return impl_dict_str_arr
    if isinstance(arg_a, PandasTimestampType):

        def impl_timestamp(arg_a, errors='raise', dayfirst=False, yearfirst
            =False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return arg_a
        return impl_timestamp
    if arg_a == bodo.datetime64ns:

        def impl_np_datetime(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return pd.Timestamp(arg_a)
        return impl_np_datetime
    if is_overload_none(arg_a):

        def impl_np_datetime(arg_a, errors='raise', dayfirst=False,
            yearfirst=False, utc=None, format=None, exact=True, unit=None,
            infer_datetime_format=False, origin='unix', cache=True):
            return None
        return impl_np_datetime
    raise_bodo_error(f'pd.to_datetime(): cannot convert date type {arg_a}')


@overload(pd.to_timedelta, inline='always', no_unliteral=True)
def overload_to_timedelta(arg_a, unit='ns', errors='raise'):
    if not is_overload_constant_str(unit):
        raise BodoError(
            'pandas.to_timedelta(): unit should be a constant string')
    unit = pd._libs.tslibs.timedeltas.parse_timedelta_unit(
        get_overload_const_str(unit))
    if isinstance(arg_a, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(arg_a, unit='ns', errors='raise'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            mgqk__luljf = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            vvu__xdwrj = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            mvv__ykhq = bodo.utils.conversion.coerce_to_ndarray(pd.
                to_timedelta(arr, unit, errors))
            return bodo.hiframes.pd_series_ext.init_series(mvv__ykhq,
                mgqk__luljf, vvu__xdwrj)
        return impl_series
    if is_overload_constant_str(arg_a) or arg_a in (pd_timedelta_type,
        datetime_timedelta_type, bodo.string_type):

        def impl_string(arg_a, unit='ns', errors='raise'):
            return pd.Timedelta(arg_a)
        return impl_string
    if isinstance(arg_a, types.Float):
        m, lazbh__xafv = pd._libs.tslibs.conversion.precision_from_unit(unit)

        def impl_float_scalar(arg_a, unit='ns', errors='raise'):
            val = float_to_timedelta_val(arg_a, lazbh__xafv, m)
            return pd.Timedelta(val)
        return impl_float_scalar
    if isinstance(arg_a, types.Integer):
        m, iwn__wui = pd._libs.tslibs.conversion.precision_from_unit(unit)

        def impl_integer_scalar(arg_a, unit='ns', errors='raise'):
            return pd.Timedelta(arg_a * m)
        return impl_integer_scalar
    if is_iterable_type(arg_a) and not isinstance(arg_a, types.BaseTuple):
        m, lazbh__xafv = pd._libs.tslibs.conversion.precision_from_unit(unit)
        pehzd__sgo = np.dtype('timedelta64[ns]')
        if isinstance(arg_a.dtype, types.Float):

            def impl_float(arg_a, unit='ns', errors='raise'):
                kaa__hyqy = len(arg_a)
                eeo__nkkuz = np.empty(kaa__hyqy, pehzd__sgo)
                for iuqi__mggdl in numba.parfors.parfor.internal_prange(
                    kaa__hyqy):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, iuqi__mggdl):
                        val = float_to_timedelta_val(arg_a[iuqi__mggdl],
                            lazbh__xafv, m)
                    eeo__nkkuz[iuqi__mggdl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    eeo__nkkuz, None)
            return impl_float
        if isinstance(arg_a.dtype, types.Integer):

            def impl_int(arg_a, unit='ns', errors='raise'):
                kaa__hyqy = len(arg_a)
                eeo__nkkuz = np.empty(kaa__hyqy, pehzd__sgo)
                for iuqi__mggdl in numba.parfors.parfor.internal_prange(
                    kaa__hyqy):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, iuqi__mggdl):
                        val = arg_a[iuqi__mggdl] * m
                    eeo__nkkuz[iuqi__mggdl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    eeo__nkkuz, None)
            return impl_int
        if arg_a.dtype == bodo.timedelta64ns:

            def impl_td64(arg_a, unit='ns', errors='raise'):
                arr = bodo.utils.conversion.coerce_to_ndarray(arg_a)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(arr,
                    None)
            return impl_td64
        if arg_a.dtype == bodo.string_type or isinstance(arg_a.dtype, types
            .UnicodeCharSeq):

            def impl_str(arg_a, unit='ns', errors='raise'):
                return pandas_string_array_to_timedelta(arg_a, unit, errors)
            return impl_str
        if arg_a.dtype == datetime_timedelta_type:

            def impl_datetime_timedelta(arg_a, unit='ns', errors='raise'):
                kaa__hyqy = len(arg_a)
                eeo__nkkuz = np.empty(kaa__hyqy, pehzd__sgo)
                for iuqi__mggdl in numba.parfors.parfor.internal_prange(
                    kaa__hyqy):
                    val = iNaT
                    if not bodo.libs.array_kernels.isna(arg_a, iuqi__mggdl):
                        xoqxe__dcc = arg_a[iuqi__mggdl]
                        val = (xoqxe__dcc.microseconds + 1000 * 1000 * (
                            xoqxe__dcc.seconds + 24 * 60 * 60 * xoqxe__dcc.
                            days)) * 1000
                    eeo__nkkuz[iuqi__mggdl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        val)
                return bodo.hiframes.pd_index_ext.init_timedelta_index(
                    eeo__nkkuz, None)
            return impl_datetime_timedelta
    if is_overload_none(arg_a):
        return lambda arg_a, unit='ns', errors='raise': None
    raise_bodo_error(
        f'pd.to_timedelta(): cannot convert date type {arg_a.dtype}')


@register_jitable
def float_to_timedelta_val(data, precision, multiplier):
    pvcbr__azgny = np.int64(data)
    pofz__ehqab = data - pvcbr__azgny
    if precision:
        pofz__ehqab = np.round(pofz__ehqab, precision)
    return pvcbr__azgny * multiplier + np.int64(pofz__ehqab * multiplier)


@numba.njit
def pandas_string_array_to_timedelta(arg_a, unit='ns', errors='raise'):
    with numba.objmode(result='timedelta_index'):
        result = pd.to_timedelta(arg_a, errors=errors)
    return result


def create_timestamp_cmp_op_overload(op):

    def overload_date_timestamp_cmp(lhs, rhs):
        if isinstance(lhs, PandasTimestampType
            ) and rhs == bodo.hiframes.datetime_date_ext.datetime_date_type:
            tz_literal = lhs.tz
            return lambda lhs, rhs: op(lhs, pd.Timestamp(rhs, tz=tz_literal))
        if (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and
            isinstance(rhs, PandasTimestampType)):
            tz_literal = rhs.tz
            return lambda lhs, rhs: op(pd.Timestamp(lhs, tz=tz_literal), rhs)
        if isinstance(lhs, PandasTimestampType) and isinstance(rhs,
            PandasTimestampType):
            if lhs.tz != rhs.tz:
                raise BodoError(
                    f'{numba.core.utils.OPERATORS_TO_BUILTINS[op]} with two Timestamps requires both Timestamps share the same timezone. '
                     +
                    f'Argument 0 has timezone {lhs.tz} and argument 1 has timezone {rhs.tz}. '
                     +
                    'To compare these values please convert to timezone naive with ts.tz_convert(None).'
                    )
            return lambda lhs, rhs: op(lhs.value, rhs.value)
        if lhs == pd_timestamp_tz_naive_type and rhs == bodo.datetime64ns:
            return lambda lhs, rhs: op(bodo.hiframes.pd_timestamp_ext.
                integer_to_dt64(lhs.value), rhs)
        if lhs == bodo.datetime64ns and rhs == pd_timestamp_tz_naive_type:
            return lambda lhs, rhs: op(lhs, bodo.hiframes.pd_timestamp_ext.
                integer_to_dt64(rhs.value))
    return overload_date_timestamp_cmp


@overload_method(PandasTimestampType, 'toordinal', no_unliteral=True)
def toordinal(date):

    def impl(date):
        return _ymd2ord(date.year, date.month, date.day)
    return impl


def overload_freq_methods(method):

    def freq_overload(td, freq, ambiguous='raise', nonexistent='raise'):
        zpnml__tafcx = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        onmm__amep = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Timestamp.{method}', zpnml__tafcx,
            onmm__amep, package_name='pandas', module_name='Timestamp')
        mfq__ytxy = ["freq == 'D'", "freq == 'H'",
            "freq == 'min' or freq == 'T'", "freq == 'S'",
            "freq == 'ms' or freq == 'L'", "freq == 'U' or freq == 'us'",
            "freq == 'N'"]
        hfu__hgeq = [24 * 60 * 60 * 1000000 * 1000, 60 * 60 * 1000000 * 
            1000, 60 * 1000000 * 1000, 1000000 * 1000, 1000 * 1000, 1000, 1]
        aprg__sxgan = None
        oxoxd__nztjh = None
        tz_literal = None
        cceg__wdv = (
            "def impl(td, freq, ambiguous='raise', nonexistent='raise'):\n")
        for iuqi__mggdl, qpts__mzx in enumerate(mfq__ytxy):
            gvedl__vola = 'if' if iuqi__mggdl == 0 else 'elif'
            cceg__wdv += '    {} {}:\n'.format(gvedl__vola, qpts__mzx)
            cceg__wdv += '        unit_value = {}\n'.format(hfu__hgeq[
                iuqi__mggdl])
        cceg__wdv += '    else:\n'
        cceg__wdv += (
            "        raise ValueError('Incorrect Frequency specification')\n")
        if td == pd_timedelta_type:
            cceg__wdv += (
                """    return pd.Timedelta(unit_value * np.int64(np.{}(td.value / unit_value)))
"""
                .format(method))
        else:
            assert isinstance(td, PandasTimestampType
                ), 'Value must be a timestamp'
            cceg__wdv += f'    value = td.value\n'
            tz_literal = td.tz
            if tz_literal is not None:
                uysbo__vqz = '0'
                bcc__lbguh = False
                if tz_has_transition_times(tz_literal):
                    bcc__lbguh = True
                    doio__wfc = pytz.timezone(tz_literal)
                    oxoxd__nztjh = np.array(doio__wfc._utc_transition_times,
                        dtype='M8[ns]').view('i8')
                    aprg__sxgan = np.array(doio__wfc._transition_info)[:, 0]
                    aprg__sxgan = (pd.Series(aprg__sxgan).dt.total_seconds(
                        ) * 1000000000).astype(np.int64).values
                    uysbo__vqz = (
                        "deltas[np.searchsorted(trans, value, side='right') - 1]"
                        )
                elif isinstance(tz_literal, str):
                    doio__wfc = pytz.timezone(tz_literal)
                    uysbo__vqz = str(np.int64(doio__wfc._utcoffset.
                        total_seconds() * 1000000000))
                elif isinstance(tz_literal, int):
                    uysbo__vqz = str(tz_literal)
                cceg__wdv += f'    delta = {uysbo__vqz}\n'
                cceg__wdv += f'    value = value + delta\n'
            if method == 'ceil':
                cceg__wdv += (
                    '    value = value + np.remainder(-value, unit_value)\n')
            if method == 'floor':
                cceg__wdv += (
                    '    value = value - np.remainder(value, unit_value)\n')
            if method == 'round':
                cceg__wdv += '    if unit_value == 1:\n'
                cceg__wdv += '        value = value\n'
                cceg__wdv += '    else:\n'
                cceg__wdv += (
                    '        quotient, remainder = np.divmod(value, unit_value)\n'
                    )
                cceg__wdv += """        mask = np.logical_or(remainder > (unit_value // 2), np.logical_and(remainder == (unit_value // 2), quotient % 2))
"""
                cceg__wdv += '        if mask:\n'
                cceg__wdv += '            quotient = quotient + 1\n'
                cceg__wdv += '        value = quotient * unit_value\n'
            if tz_literal is not None:
                if bcc__lbguh:
                    cceg__wdv += f'    original_value = value\n'
                    cceg__wdv += """    start_trans = deltas[np.searchsorted(trans, original_value, side='right') - 1]
"""
                    cceg__wdv += '    value = value - start_trans\n'
                    cceg__wdv += """    end_trans = deltas[np.searchsorted(trans, value, side='right') - 1]
"""
                    cceg__wdv += '    offset = start_trans - end_trans\n'
                    cceg__wdv += '    value = value + offset\n'
                else:
                    cceg__wdv += f'    value = value - delta\n'
            cceg__wdv += '    return pd.Timestamp(value, tz=tz_literal)\n'
        dkvdd__yesje = {}
        exec(cceg__wdv, {'np': np, 'pd': pd, 'deltas': aprg__sxgan, 'trans':
            oxoxd__nztjh, 'tz_literal': tz_literal}, dkvdd__yesje)
        impl = dkvdd__yesje['impl']
        return impl
    return freq_overload


def _install_freq_methods():
    aprq__ior = ['ceil', 'floor', 'round']
    for method in aprq__ior:
        ilcpa__cfyyv = overload_freq_methods(method)
        overload_method(PDTimeDeltaType, method, no_unliteral=True)(
            ilcpa__cfyyv)
        overload_method(PandasTimestampType, method, no_unliteral=True)(
            ilcpa__cfyyv)


_install_freq_methods()


@register_jitable
def compute_pd_timestamp(totmicrosec, nanosecond):
    microsecond = totmicrosec % 1000000
    uwp__tgfsr = totmicrosec // 1000000
    second = uwp__tgfsr % 60
    xxz__hdgt = uwp__tgfsr // 60
    minute = xxz__hdgt % 60
    xjfnr__myqc = xxz__hdgt // 60
    hour = xjfnr__myqc % 24
    rzzm__kqnlb = xjfnr__myqc // 24
    year, month, day = _ord2ymd(rzzm__kqnlb)
    value = npy_datetimestruct_to_datetime(year, month, day, hour, minute,
        second, microsecond)
    value += zero_if_none(nanosecond)
    return init_timestamp(year, month, day, hour, minute, second,
        microsecond, nanosecond, value, None)


def overload_sub_operator_timestamp(lhs, rhs):
    if isinstance(lhs, PandasTimestampType) and rhs == datetime_timedelta_type:
        tz_literal = lhs.tz

        def impl(lhs, rhs):
            xoop__lrutx = bodo.hiframes.datetime_timedelta_ext._to_nanoseconds(
                rhs)
            return pd.Timestamp(lhs.value - xoop__lrutx, tz=tz_literal)
        return impl
    if lhs == pd_timestamp_tz_naive_type and rhs == pd_timestamp_tz_naive_type:

        def impl_timestamp(lhs, rhs):
            return convert_numpy_timedelta64_to_pd_timedelta(lhs.value -
                rhs.value)
        return impl_timestamp
    if isinstance(lhs, PandasTimestampType) and rhs == pd_timedelta_type:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl


def overload_add_operator_timestamp(lhs, rhs):
    if isinstance(lhs, PandasTimestampType) and rhs == datetime_timedelta_type:
        tz_literal = lhs.tz

        def impl(lhs, rhs):
            xoop__lrutx = bodo.hiframes.datetime_timedelta_ext._to_nanoseconds(
                rhs)
            return pd.Timestamp(lhs.value + xoop__lrutx, tz=tz_literal)
        return impl
    if isinstance(lhs, PandasTimestampType) and rhs == pd_timedelta_type:
        tz_literal = lhs.tz

        def impl(lhs, rhs):
            return pd.Timestamp(lhs.value + rhs.value, tz=tz_literal)
        return impl
    if lhs == pd_timedelta_type and isinstance(rhs, PandasTimestampType
        ) or lhs == datetime_timedelta_type and isinstance(rhs,
        PandasTimestampType):

        def impl(lhs, rhs):
            return rhs + lhs
        return impl


@overload(min, no_unliteral=True)
def timestamp_min(lhs, rhs):
    check_tz_aware_unsupported(lhs, f'Timestamp.min()')
    check_tz_aware_unsupported(rhs, f'Timestamp.min()')
    if lhs == pd_timestamp_tz_naive_type and rhs == pd_timestamp_tz_naive_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@overload(max, no_unliteral=True)
def timestamp_max(lhs, rhs):
    check_tz_aware_unsupported(lhs, f'Timestamp.max()')
    check_tz_aware_unsupported(rhs, f'Timestamp.max()')
    if lhs == pd_timestamp_tz_naive_type and rhs == pd_timestamp_tz_naive_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload_method(DatetimeDateType, 'strftime')
@overload_method(PandasTimestampType, 'strftime')
def strftime(ts, format):
    if isinstance(ts, DatetimeDateType):
        ghpu__jttn = 'datetime.date'
    else:
        ghpu__jttn = 'pandas.Timestamp'
    if types.unliteral(format) != types.unicode_type:
        raise BodoError(
            f"{ghpu__jttn}.strftime(): 'strftime' argument must be a string")

    def impl(ts, format):
        with numba.objmode(res='unicode_type'):
            res = ts.strftime(format)
        return res
    return impl


@overload_method(PandasTimestampType, 'to_datetime64')
def to_datetime64(ts):

    def impl(ts):
        return integer_to_dt64(ts.value)
    return impl


def now_impl(tz=None):
    pass


@overload(now_impl, no_unilteral=True)
def now_impl_overload(tz=None):
    if is_overload_none(tz):
        ccx__rjrsh = PandasTimestampType(None)
    elif is_overload_constant_str(tz):
        ccx__rjrsh = PandasTimestampType(get_overload_const_str(tz))
    elif is_overload_constant_int(tz):
        ccx__rjrsh = PandasTimestampType(get_overload_const_int(tz))
    else:
        raise_bodo_error(
            'pandas.Timestamp.now(): tz argument must be a constant string or integer literal if provided'
            )

    def impl(tz=None):
        with numba.objmode(d=ccx__rjrsh):
            d = pd.Timestamp.now(tz)
        return d
    return impl


class CompDT64(ConcreteTemplate):
    cases = [signature(types.boolean, types.NPDatetime('ns'), types.
        NPDatetime('ns'))]


@infer_global(operator.lt)
class CmpOpLt(CompDT64):
    key = operator.lt


@infer_global(operator.le)
class CmpOpLe(CompDT64):
    key = operator.le


@infer_global(operator.gt)
class CmpOpGt(CompDT64):
    key = operator.gt


@infer_global(operator.ge)
class CmpOpGe(CompDT64):
    key = operator.ge


@infer_global(operator.eq)
class CmpOpEq(CompDT64):
    key = operator.eq


@infer_global(operator.ne)
class CmpOpNe(CompDT64):
    key = operator.ne


@typeof_impl.register(calendar._localized_month)
def typeof_python_calendar(val, c):
    return types.Tuple([types.StringLiteral(xtzje__rty) for xtzje__rty in val])


@overload(str)
def overload_datetime64_str(val):
    if val == bodo.datetime64ns:

        def impl(val):
            return (bodo.hiframes.pd_timestamp_ext.
                convert_datetime64_to_timestamp(val).isoformat('T'))
        return impl


timestamp_unsupported_attrs = ['asm8', 'components', 'freqstr', 'tz',
    'fold', 'tzinfo', 'freq']
timestamp_unsupported_methods = ['astimezone', 'ctime', 'dst', 'isoweekday',
    'replace', 'strptime', 'time', 'timestamp', 'timetuple', 'timetz',
    'to_julian_date', 'to_numpy', 'to_period', 'to_pydatetime', 'tzname',
    'utcoffset', 'utctimetuple']


def _install_pd_timestamp_unsupported():
    from bodo.utils.typing import create_unsupported_overload
    for npsy__stj in timestamp_unsupported_attrs:
        rqb__yrxsk = 'pandas.Timestamp.' + npsy__stj
        overload_attribute(PandasTimestampType, npsy__stj)(
            create_unsupported_overload(rqb__yrxsk))
    for zzsyv__qli in timestamp_unsupported_methods:
        rqb__yrxsk = 'pandas.Timestamp.' + zzsyv__qli
        overload_method(PandasTimestampType, zzsyv__qli)(
            create_unsupported_overload(rqb__yrxsk + '()'))


_install_pd_timestamp_unsupported()


@lower_builtin(numba.core.types.functions.NumberClass,
    pd_timestamp_tz_naive_type, types.StringLiteral)
def datetime64_constructor(context, builder, sig, args):

    def datetime64_constructor_impl(a, b):
        return integer_to_dt64(a.value)
    return context.compile_internal(builder, datetime64_constructor_impl,
        sig, args)
