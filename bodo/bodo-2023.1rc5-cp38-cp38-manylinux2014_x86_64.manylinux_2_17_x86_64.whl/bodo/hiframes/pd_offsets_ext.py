"""
Implement support for the various classes in pd.tseries.offsets.
"""
import operator
import llvmlite.binding as ll
import numpy as np
import pandas as pd
import pytz
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.pd_timestamp_ext import PandasTimestampType, get_days_in_month, pd_timestamp_tz_naive_type, tz_has_transition_times
from bodo.libs import hdatetime_ext
from bodo.utils.typing import BodoError, create_unsupported_overload, is_overload_none
ll.add_symbol('box_date_offset', hdatetime_ext.box_date_offset)
ll.add_symbol('unbox_date_offset', hdatetime_ext.unbox_date_offset)


class MonthBeginType(types.Type):

    def __init__(self):
        super(MonthBeginType, self).__init__(name='MonthBeginType()')


month_begin_type = MonthBeginType()


@typeof_impl.register(pd.tseries.offsets.MonthBegin)
def typeof_month_begin(val, c):
    return month_begin_type


@register_model(MonthBeginType)
class MonthBeginModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        aiox__qqvd = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthBeginModel, self).__init__(dmm, fe_type, aiox__qqvd)


@box(MonthBeginType)
def box_month_begin(typ, val, c):
    rppok__gnw = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    pqrbn__cjh = c.pyapi.long_from_longlong(rppok__gnw.n)
    bet__obg = c.pyapi.from_native_value(types.boolean, rppok__gnw.
        normalize, c.env_manager)
    zxv__gpgnu = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthBegin))
    zclhu__abqnk = c.pyapi.call_function_objargs(zxv__gpgnu, (pqrbn__cjh,
        bet__obg))
    c.pyapi.decref(pqrbn__cjh)
    c.pyapi.decref(bet__obg)
    c.pyapi.decref(zxv__gpgnu)
    return zclhu__abqnk


@unbox(MonthBeginType)
def unbox_month_begin(typ, val, c):
    pqrbn__cjh = c.pyapi.object_getattr_string(val, 'n')
    bet__obg = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(pqrbn__cjh)
    normalize = c.pyapi.to_native_value(types.bool_, bet__obg).value
    rppok__gnw = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    rppok__gnw.n = n
    rppok__gnw.normalize = normalize
    c.pyapi.decref(pqrbn__cjh)
    c.pyapi.decref(bet__obg)
    eqhwp__ouj = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(rppok__gnw._getvalue(), is_error=eqhwp__ouj)


@overload(pd.tseries.offsets.MonthBegin, no_unliteral=True)
def MonthBegin(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_begin(n, normalize)
    return impl


@intrinsic
def init_month_begin(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        rppok__gnw = cgutils.create_struct_proxy(typ)(context, builder)
        rppok__gnw.n = args[0]
        rppok__gnw.normalize = args[1]
        return rppok__gnw._getvalue()
    return MonthBeginType()(n, normalize), codegen


make_attribute_wrapper(MonthBeginType, 'n', 'n')
make_attribute_wrapper(MonthBeginType, 'normalize', 'normalize')


@register_jitable
def calculate_month_begin_date(year, month, day, n):
    if n <= 0:
        if day > 1:
            n += 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = 1
    return year, month, day


def overload_add_operator_month_begin_offset_type(lhs, rhs):
    if lhs == month_begin_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_begin_type and isinstance(rhs, PandasTimestampType):
        kaxoy__ejlke = rhs.tz

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day, tz=
                    kaxoy__ejlke)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond,
                    tz=kaxoy__ejlke)
        return impl
    if lhs == month_begin_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_begin_date(rhs.year, rhs.
                month, rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if (isinstance(lhs, PandasTimestampType) or lhs in [
        datetime_datetime_type, datetime_date_type]
        ) and rhs == month_begin_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


class MonthEndType(types.Type):

    def __init__(self):
        super(MonthEndType, self).__init__(name='MonthEndType()')


month_end_type = MonthEndType()


@typeof_impl.register(pd.tseries.offsets.MonthEnd)
def typeof_month_end(val, c):
    return month_end_type


@register_model(MonthEndType)
class MonthEndModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        aiox__qqvd = [('n', types.int64), ('normalize', types.boolean)]
        super(MonthEndModel, self).__init__(dmm, fe_type, aiox__qqvd)


@box(MonthEndType)
def box_month_end(typ, val, c):
    tqt__nryne = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    pqrbn__cjh = c.pyapi.long_from_longlong(tqt__nryne.n)
    bet__obg = c.pyapi.from_native_value(types.boolean, tqt__nryne.
        normalize, c.env_manager)
    vfxew__rop = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.MonthEnd))
    zclhu__abqnk = c.pyapi.call_function_objargs(vfxew__rop, (pqrbn__cjh,
        bet__obg))
    c.pyapi.decref(pqrbn__cjh)
    c.pyapi.decref(bet__obg)
    c.pyapi.decref(vfxew__rop)
    return zclhu__abqnk


@unbox(MonthEndType)
def unbox_month_end(typ, val, c):
    pqrbn__cjh = c.pyapi.object_getattr_string(val, 'n')
    bet__obg = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(pqrbn__cjh)
    normalize = c.pyapi.to_native_value(types.bool_, bet__obg).value
    tqt__nryne = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    tqt__nryne.n = n
    tqt__nryne.normalize = normalize
    c.pyapi.decref(pqrbn__cjh)
    c.pyapi.decref(bet__obg)
    eqhwp__ouj = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(tqt__nryne._getvalue(), is_error=eqhwp__ouj)


@overload(pd.tseries.offsets.MonthEnd, no_unliteral=True)
def MonthEnd(n=1, normalize=False):

    def impl(n=1, normalize=False):
        return init_month_end(n, normalize)
    return impl


@intrinsic
def init_month_end(typingctx, n, normalize):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        tqt__nryne = cgutils.create_struct_proxy(typ)(context, builder)
        tqt__nryne.n = args[0]
        tqt__nryne.normalize = args[1]
        return tqt__nryne._getvalue()
    return MonthEndType()(n, normalize), codegen


make_attribute_wrapper(MonthEndType, 'n', 'n')
make_attribute_wrapper(MonthEndType, 'normalize', 'normalize')


@lower_constant(MonthBeginType)
@lower_constant(MonthEndType)
def lower_constant_month_end(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    return lir.Constant.literal_struct([n, normalize])


@register_jitable
def calculate_month_end_date(year, month, day, n):
    if n > 0:
        tqt__nryne = get_days_in_month(year, month)
        if tqt__nryne > day:
            n -= 1
    month = month + n
    month -= 1
    year += month // 12
    month = month % 12 + 1
    day = get_days_in_month(year, month)
    return year, month, day


def overload_add_operator_month_end_offset_type(lhs, rhs):
    if lhs == month_end_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond)
        return impl
    if lhs == month_end_type and isinstance(rhs, PandasTimestampType):
        kaxoy__ejlke = rhs.tz

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            if lhs.normalize:
                return pd.Timestamp(year=year, month=month, day=day, tz=
                    kaxoy__ejlke)
            else:
                return pd.Timestamp(year=year, month=month, day=day, hour=
                    rhs.hour, minute=rhs.minute, second=rhs.second,
                    microsecond=rhs.microsecond, nanosecond=rhs.nanosecond,
                    tz=kaxoy__ejlke)
        return impl
    if lhs == month_end_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            year, month, day = calculate_month_end_date(rhs.year, rhs.month,
                rhs.day, lhs.n)
            return pd.Timestamp(year=year, month=month, day=day)
        return impl
    if (isinstance(lhs, PandasTimestampType) or lhs in [
        datetime_datetime_type, datetime_date_type]) and rhs == month_end_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_mul_date_offset_types(lhs, rhs):
    if lhs == month_begin_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthBegin(lhs.n * rhs, lhs.normalize)
    if lhs == month_end_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.MonthEnd(lhs.n * rhs, lhs.normalize)
    if lhs == week_type:

        def impl(lhs, rhs):
            return pd.tseries.offsets.Week(lhs.n * rhs, lhs.normalize, lhs.
                weekday)
    if lhs == date_offset_type:

        def impl(lhs, rhs):
            n = lhs.n * rhs
            normalize = lhs.normalize
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                nanoseconds = lhs._nanoseconds
                nanosecond = lhs._nanosecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize)
    if rhs in [week_type, month_end_type, month_begin_type, date_offset_type]:

        def impl(lhs, rhs):
            return rhs * lhs
        return impl
    return impl


class DateOffsetType(types.Type):

    def __init__(self):
        super(DateOffsetType, self).__init__(name='DateOffsetType()')


date_offset_type = DateOffsetType()
date_offset_fields = ['years', 'months', 'weeks', 'days', 'hours',
    'minutes', 'seconds', 'microseconds', 'nanoseconds', 'year', 'month',
    'day', 'weekday', 'hour', 'minute', 'second', 'microsecond', 'nanosecond']


@typeof_impl.register(pd.tseries.offsets.DateOffset)
def type_of_date_offset(val, c):
    return date_offset_type


@register_model(DateOffsetType)
class DateOffsetModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        aiox__qqvd = [('n', types.int64), ('normalize', types.boolean), (
            'years', types.int64), ('months', types.int64), ('weeks', types
            .int64), ('days', types.int64), ('hours', types.int64), (
            'minutes', types.int64), ('seconds', types.int64), (
            'microseconds', types.int64), ('nanoseconds', types.int64), (
            'year', types.int64), ('month', types.int64), ('day', types.
            int64), ('weekday', types.int64), ('hour', types.int64), (
            'minute', types.int64), ('second', types.int64), ('microsecond',
            types.int64), ('nanosecond', types.int64), ('has_kws', types.
            boolean)]
        super(DateOffsetModel, self).__init__(dmm, fe_type, aiox__qqvd)


@box(DateOffsetType)
def box_date_offset(typ, val, c):
    bco__dnf = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val
        )
    onq__vvrng = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    for ivt__cxi, ssq__fjss in enumerate(date_offset_fields):
        c.builder.store(getattr(bco__dnf, ssq__fjss), c.builder.inttoptr(c.
            builder.add(c.builder.ptrtoint(onq__vvrng, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * ivt__cxi)), lir.IntType(64).
            as_pointer()))
    ozo__dia = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(1), lir.IntType(64).as_pointer(), lir.IntType(1)])
    kaxg__fze = cgutils.get_or_insert_function(c.builder.module, ozo__dia,
        name='box_date_offset')
    dleca__lxgy = c.builder.call(kaxg__fze, [bco__dnf.n, bco__dnf.normalize,
        onq__vvrng, bco__dnf.has_kws])
    c.context.nrt.decref(c.builder, typ, val)
    return dleca__lxgy


@unbox(DateOffsetType)
def unbox_date_offset(typ, val, c):
    pqrbn__cjh = c.pyapi.object_getattr_string(val, 'n')
    bet__obg = c.pyapi.object_getattr_string(val, 'normalize')
    n = c.pyapi.long_as_longlong(pqrbn__cjh)
    normalize = c.pyapi.to_native_value(types.bool_, bet__obg).value
    onq__vvrng = c.builder.alloca(lir.IntType(64), size=lir.Constant(lir.
        IntType(64), 18))
    ozo__dia = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer(
        ), lir.IntType(64).as_pointer()])
    yed__nqj = cgutils.get_or_insert_function(c.builder.module, ozo__dia,
        name='unbox_date_offset')
    has_kws = c.builder.call(yed__nqj, [val, onq__vvrng])
    bco__dnf = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    bco__dnf.n = n
    bco__dnf.normalize = normalize
    for ivt__cxi, ssq__fjss in enumerate(date_offset_fields):
        setattr(bco__dnf, ssq__fjss, c.builder.load(c.builder.inttoptr(c.
            builder.add(c.builder.ptrtoint(onq__vvrng, lir.IntType(64)),
            lir.Constant(lir.IntType(64), 8 * ivt__cxi)), lir.IntType(64).
            as_pointer())))
    bco__dnf.has_kws = has_kws
    c.pyapi.decref(pqrbn__cjh)
    c.pyapi.decref(bet__obg)
    eqhwp__ouj = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(bco__dnf._getvalue(), is_error=eqhwp__ouj)


@lower_constant(DateOffsetType)
def lower_constant_date_offset(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    ckilg__yln = [n, normalize]
    has_kws = False
    zywae__oonw = [0] * 9 + [-1] * 9
    for ivt__cxi, ssq__fjss in enumerate(date_offset_fields):
        if hasattr(pyval, ssq__fjss):
            fqdq__vmxwf = context.get_constant(types.int64, getattr(pyval,
                ssq__fjss))
            has_kws = True
        else:
            fqdq__vmxwf = context.get_constant(types.int64, zywae__oonw[
                ivt__cxi])
        ckilg__yln.append(fqdq__vmxwf)
    has_kws = context.get_constant(types.boolean, has_kws)
    ckilg__yln.append(has_kws)
    return lir.Constant.literal_struct(ckilg__yln)


@overload(pd.tseries.offsets.DateOffset, no_unliteral=True)
def DateOffset(n=1, normalize=False, years=None, months=None, weeks=None,
    days=None, hours=None, minutes=None, seconds=None, microseconds=None,
    nanoseconds=None, year=None, month=None, day=None, weekday=None, hour=
    None, minute=None, second=None, microsecond=None, nanosecond=None):
    has_kws = False
    wwxwx__hwv = [years, months, weeks, days, hours, minutes, seconds,
        microseconds, year, month, day, weekday, hour, minute, second,
        microsecond]
    for himip__mend in wwxwx__hwv:
        if not is_overload_none(himip__mend):
            has_kws = True
            break

    def impl(n=1, normalize=False, years=None, months=None, weeks=None,
        days=None, hours=None, minutes=None, seconds=None, microseconds=
        None, nanoseconds=None, year=None, month=None, day=None, weekday=
        None, hour=None, minute=None, second=None, microsecond=None,
        nanosecond=None):
        years = 0 if years is None else years
        months = 0 if months is None else months
        weeks = 0 if weeks is None else weeks
        days = 0 if days is None else days
        hours = 0 if hours is None else hours
        minutes = 0 if minutes is None else minutes
        seconds = 0 if seconds is None else seconds
        microseconds = 0 if microseconds is None else microseconds
        nanoseconds = 0 if nanoseconds is None else nanoseconds
        year = -1 if year is None else year
        month = -1 if month is None else month
        weekday = -1 if weekday is None else weekday
        day = -1 if day is None else day
        hour = -1 if hour is None else hour
        minute = -1 if minute is None else minute
        second = -1 if second is None else second
        microsecond = -1 if microsecond is None else microsecond
        nanosecond = -1 if nanosecond is None else nanosecond
        return init_date_offset(n, normalize, years, months, weeks, days,
            hours, minutes, seconds, microseconds, nanoseconds, year, month,
            day, weekday, hour, minute, second, microsecond, nanosecond,
            has_kws)
    return impl


@intrinsic
def init_date_offset(typingctx, n, normalize, years, months, weeks, days,
    hours, minutes, seconds, microseconds, nanoseconds, year, month, day,
    weekday, hour, minute, second, microsecond, nanosecond, has_kws):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        bco__dnf = cgutils.create_struct_proxy(typ)(context, builder)
        bco__dnf.n = args[0]
        bco__dnf.normalize = args[1]
        bco__dnf.years = args[2]
        bco__dnf.months = args[3]
        bco__dnf.weeks = args[4]
        bco__dnf.days = args[5]
        bco__dnf.hours = args[6]
        bco__dnf.minutes = args[7]
        bco__dnf.seconds = args[8]
        bco__dnf.microseconds = args[9]
        bco__dnf.nanoseconds = args[10]
        bco__dnf.year = args[11]
        bco__dnf.month = args[12]
        bco__dnf.day = args[13]
        bco__dnf.weekday = args[14]
        bco__dnf.hour = args[15]
        bco__dnf.minute = args[16]
        bco__dnf.second = args[17]
        bco__dnf.microsecond = args[18]
        bco__dnf.nanosecond = args[19]
        bco__dnf.has_kws = args[20]
        return bco__dnf._getvalue()
    return DateOffsetType()(n, normalize, years, months, weeks, days, hours,
        minutes, seconds, microseconds, nanoseconds, year, month, day,
        weekday, hour, minute, second, microsecond, nanosecond, has_kws
        ), codegen


make_attribute_wrapper(DateOffsetType, 'n', 'n')
make_attribute_wrapper(DateOffsetType, 'normalize', 'normalize')
make_attribute_wrapper(DateOffsetType, 'years', '_years')
make_attribute_wrapper(DateOffsetType, 'months', '_months')
make_attribute_wrapper(DateOffsetType, 'weeks', '_weeks')
make_attribute_wrapper(DateOffsetType, 'days', '_days')
make_attribute_wrapper(DateOffsetType, 'hours', '_hours')
make_attribute_wrapper(DateOffsetType, 'minutes', '_minutes')
make_attribute_wrapper(DateOffsetType, 'seconds', '_seconds')
make_attribute_wrapper(DateOffsetType, 'microseconds', '_microseconds')
make_attribute_wrapper(DateOffsetType, 'nanoseconds', '_nanoseconds')
make_attribute_wrapper(DateOffsetType, 'year', '_year')
make_attribute_wrapper(DateOffsetType, 'month', '_month')
make_attribute_wrapper(DateOffsetType, 'weekday', '_weekday')
make_attribute_wrapper(DateOffsetType, 'day', '_day')
make_attribute_wrapper(DateOffsetType, 'hour', '_hour')
make_attribute_wrapper(DateOffsetType, 'minute', '_minute')
make_attribute_wrapper(DateOffsetType, 'second', '_second')
make_attribute_wrapper(DateOffsetType, 'microsecond', '_microsecond')
make_attribute_wrapper(DateOffsetType, 'nanosecond', '_nanosecond')
make_attribute_wrapper(DateOffsetType, 'has_kws', '_has_kws')


@register_jitable
def relative_delta_addition(dateoffset, ts):
    if dateoffset._has_kws:
        vkto__bzb = -1 if dateoffset.n < 0 else 1
        for bne__apc in range(np.abs(dateoffset.n)):
            year = ts.year
            month = ts.month
            day = ts.day
            hour = ts.hour
            minute = ts.minute
            second = ts.second
            microsecond = ts.microsecond
            nanosecond = ts.nanosecond
            if dateoffset._year != -1:
                year = dateoffset._year
            year += vkto__bzb * dateoffset._years
            if dateoffset._month != -1:
                month = dateoffset._month
            month += vkto__bzb * dateoffset._months
            year, month, xzcde__easnv = calculate_month_end_date(year,
                month, day, 0)
            if day > xzcde__easnv:
                day = xzcde__easnv
            if dateoffset._day != -1:
                day = dateoffset._day
            if dateoffset._hour != -1:
                hour = dateoffset._hour
            if dateoffset._minute != -1:
                minute = dateoffset._minute
            if dateoffset._second != -1:
                second = dateoffset._second
            if dateoffset._microsecond != -1:
                microsecond = dateoffset._microsecond
            if dateoffset._nanosecond != -1:
                nanosecond = dateoffset._nanosecond
            ts = pd.Timestamp(year=year, month=month, day=day, hour=hour,
                minute=minute, second=second, microsecond=microsecond,
                nanosecond=nanosecond)
            td = pd.Timedelta(days=dateoffset._days + 7 * dateoffset._weeks,
                hours=dateoffset._hours, minutes=dateoffset._minutes,
                seconds=dateoffset._seconds, microseconds=dateoffset.
                _microseconds)
            td = td + pd.Timedelta(dateoffset._nanoseconds, unit='ns')
            if vkto__bzb == -1:
                td = -td
            ts = ts + td
            if dateoffset._weekday != -1:
                qkxpg__aktw = ts.weekday()
                bys__vhrn = (dateoffset._weekday - qkxpg__aktw) % 7
                ts = ts + pd.Timedelta(days=bys__vhrn)
        return ts
    else:
        return pd.Timedelta(days=dateoffset.n) + ts


def overload_add_operator_date_offset_type(lhs, rhs):
    if lhs == date_offset_type and rhs == pd_timestamp_tz_naive_type:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, rhs)
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs == date_offset_type and rhs in [datetime_date_type,
        datetime_datetime_type]:

        def impl(lhs, rhs):
            ts = relative_delta_addition(lhs, pd.Timestamp(rhs))
            if lhs.normalize:
                return ts.normalize()
            return ts
        return impl
    if lhs in [datetime_datetime_type, pd_timestamp_tz_naive_type,
        datetime_date_type] and rhs == date_offset_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def overload_sub_operator_offsets(lhs, rhs):
    if (lhs in [datetime_datetime_type, datetime_date_type] or isinstance(
        lhs, PandasTimestampType)) and rhs in [date_offset_type,
        month_begin_type, month_end_type, week_type]:

        def impl(lhs, rhs):
            return lhs + -rhs
        return impl


@overload(operator.neg, no_unliteral=True)
def overload_neg(lhs):
    if lhs == month_begin_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthBegin(-lhs.n, lhs.normalize)
    elif lhs == month_end_type:

        def impl(lhs):
            return pd.tseries.offsets.MonthEnd(-lhs.n, lhs.normalize)
    elif lhs == week_type:

        def impl(lhs):
            return pd.tseries.offsets.Week(-lhs.n, lhs.normalize, lhs.weekday)
    elif lhs == date_offset_type:

        def impl(lhs):
            n = -lhs.n
            normalize = lhs.normalize
            if lhs._has_kws:
                years = lhs._years
                months = lhs._months
                weeks = lhs._weeks
                days = lhs._days
                hours = lhs._hours
                minutes = lhs._minutes
                seconds = lhs._seconds
                microseconds = lhs._microseconds
                year = lhs._year
                month = lhs._month
                day = lhs._day
                weekday = lhs._weekday
                hour = lhs._hour
                minute = lhs._minute
                second = lhs._second
                microsecond = lhs._microsecond
                nanoseconds = lhs._nanoseconds
                nanosecond = lhs._nanosecond
                return pd.tseries.offsets.DateOffset(n, normalize, years,
                    months, weeks, days, hours, minutes, seconds,
                    microseconds, nanoseconds, year, month, day, weekday,
                    hour, minute, second, microsecond, nanosecond)
            else:
                return pd.tseries.offsets.DateOffset(n, normalize)
    else:
        return
    return impl


def is_offsets_type(val):
    return val in [date_offset_type, month_begin_type, month_end_type,
        week_type]


class WeekType(types.Type):

    def __init__(self):
        super(WeekType, self).__init__(name='WeekType()')


week_type = WeekType()


@typeof_impl.register(pd.tseries.offsets.Week)
def typeof_week(val, c):
    return week_type


@register_model(WeekType)
class WeekModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        aiox__qqvd = [('n', types.int64), ('normalize', types.boolean), (
            'weekday', types.int64)]
        super(WeekModel, self).__init__(dmm, fe_type, aiox__qqvd)


make_attribute_wrapper(WeekType, 'n', 'n')
make_attribute_wrapper(WeekType, 'normalize', 'normalize')
make_attribute_wrapper(WeekType, 'weekday', 'weekday')


@overload(pd.tseries.offsets.Week, no_unliteral=True)
def Week(n=1, normalize=False, weekday=None):

    def impl(n=1, normalize=False, weekday=None):
        jdtbs__iyoz = -1 if weekday is None else weekday
        return init_week(n, normalize, jdtbs__iyoz)
    return impl


@intrinsic
def init_week(typingctx, n, normalize, weekday):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        cug__rpzxd = cgutils.create_struct_proxy(typ)(context, builder)
        cug__rpzxd.n = args[0]
        cug__rpzxd.normalize = args[1]
        cug__rpzxd.weekday = args[2]
        return cug__rpzxd._getvalue()
    return WeekType()(n, normalize, weekday), codegen


@lower_constant(WeekType)
def lower_constant_week(context, builder, ty, pyval):
    n = context.get_constant(types.int64, pyval.n)
    normalize = context.get_constant(types.boolean, pyval.normalize)
    if pyval.weekday is not None:
        weekday = context.get_constant(types.int64, pyval.weekday)
    else:
        weekday = context.get_constant(types.int64, -1)
    return lir.Constant.literal_struct([n, normalize, weekday])


@box(WeekType)
def box_week(typ, val, c):
    cug__rpzxd = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    pqrbn__cjh = c.pyapi.long_from_longlong(cug__rpzxd.n)
    bet__obg = c.pyapi.from_native_value(types.boolean, cug__rpzxd.
        normalize, c.env_manager)
    qseq__bgjo = c.pyapi.long_from_longlong(cug__rpzxd.weekday)
    ihh__tck = c.pyapi.unserialize(c.pyapi.serialize_object(pd.tseries.
        offsets.Week))
    yqk__owoya = c.builder.icmp_signed('!=', lir.Constant(lir.IntType(64), 
        -1), cug__rpzxd.weekday)
    with c.builder.if_else(yqk__owoya) as (rrj__xmlco, jur__ptvz):
        with rrj__xmlco:
            fnp__gxma = c.pyapi.call_function_objargs(ihh__tck, (pqrbn__cjh,
                bet__obg, qseq__bgjo))
            idpr__mfyb = c.builder.block
        with jur__ptvz:
            dxdmo__vgo = c.pyapi.call_function_objargs(ihh__tck, (
                pqrbn__cjh, bet__obg))
            zxk__pmxnp = c.builder.block
    zclhu__abqnk = c.builder.phi(fnp__gxma.type)
    zclhu__abqnk.add_incoming(fnp__gxma, idpr__mfyb)
    zclhu__abqnk.add_incoming(dxdmo__vgo, zxk__pmxnp)
    c.pyapi.decref(qseq__bgjo)
    c.pyapi.decref(pqrbn__cjh)
    c.pyapi.decref(bet__obg)
    c.pyapi.decref(ihh__tck)
    return zclhu__abqnk


@unbox(WeekType)
def unbox_week(typ, val, c):
    pqrbn__cjh = c.pyapi.object_getattr_string(val, 'n')
    bet__obg = c.pyapi.object_getattr_string(val, 'normalize')
    qseq__bgjo = c.pyapi.object_getattr_string(val, 'weekday')
    n = c.pyapi.long_as_longlong(pqrbn__cjh)
    normalize = c.pyapi.to_native_value(types.bool_, bet__obg).value
    oqaza__kjkr = c.pyapi.make_none()
    uhb__wyw = c.builder.icmp_unsigned('==', qseq__bgjo, oqaza__kjkr)
    with c.builder.if_else(uhb__wyw) as (jur__ptvz, rrj__xmlco):
        with rrj__xmlco:
            fnp__gxma = c.pyapi.long_as_longlong(qseq__bgjo)
            idpr__mfyb = c.builder.block
        with jur__ptvz:
            dxdmo__vgo = lir.Constant(lir.IntType(64), -1)
            zxk__pmxnp = c.builder.block
    zclhu__abqnk = c.builder.phi(fnp__gxma.type)
    zclhu__abqnk.add_incoming(fnp__gxma, idpr__mfyb)
    zclhu__abqnk.add_incoming(dxdmo__vgo, zxk__pmxnp)
    cug__rpzxd = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    cug__rpzxd.n = n
    cug__rpzxd.normalize = normalize
    cug__rpzxd.weekday = zclhu__abqnk
    c.pyapi.decref(pqrbn__cjh)
    c.pyapi.decref(bet__obg)
    c.pyapi.decref(qseq__bgjo)
    eqhwp__ouj = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cug__rpzxd._getvalue(), is_error=eqhwp__ouj)


def overload_add_operator_week_offset_type(lhs, rhs):
    if lhs == week_type and isinstance(rhs, PandasTimestampType):

        def impl(lhs, rhs):
            if lhs.normalize:
                bow__jyr = rhs.normalize()
            else:
                bow__jyr = rhs
            zqq__byi = calculate_week_date(lhs.n, lhs.weekday, bow__jyr)
            return bow__jyr + zqq__byi
        return impl
    if lhs == week_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            if lhs.normalize:
                bow__jyr = pd.Timestamp(year=rhs.year, month=rhs.month, day
                    =rhs.day)
            else:
                bow__jyr = pd.Timestamp(year=rhs.year, month=rhs.month, day
                    =rhs.day, hour=rhs.hour, minute=rhs.minute, second=rhs.
                    second, microsecond=rhs.microsecond)
            zqq__byi = calculate_week_date(lhs.n, lhs.weekday, bow__jyr)
            return bow__jyr + zqq__byi
        return impl
    if lhs == week_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            zqq__byi = calculate_week_date(lhs.n, lhs.weekday, rhs)
            return rhs + zqq__byi
        return impl
    if (lhs in [datetime_datetime_type, datetime_date_type] or isinstance(
        lhs, PandasTimestampType)) and rhs == week_type:

        def impl(lhs, rhs):
            return rhs + lhs
        return impl
    raise BodoError(
        f'add operator not supported for data types {lhs} and {rhs}.')


def calculate_week_date(n, weekday, input_date_or_ts):
    pass


@overload(calculate_week_date)
def overload_calculate_week_date(n, weekday, input_date_or_ts):
    if isinstance(input_date_or_ts, PandasTimestampType
        ) and tz_has_transition_times(input_date_or_ts.tz):

        def impl_tz_aware(n, weekday, input_date_or_ts):
            if weekday == -1:
                td = pd.Timedelta(weeks=n)
            else:
                kuy__jlufb = input_date_or_ts.weekday()
                if weekday != kuy__jlufb:
                    xkffw__pwei = (weekday - kuy__jlufb) % 7
                    if n > 0:
                        n = n - 1
                td = pd.Timedelta(weeks=n, days=xkffw__pwei)
            return update_timedelta_with_transition(input_date_or_ts, td)
        return impl_tz_aware
    else:

        def impl(n, weekday, input_date_or_ts):
            if weekday == -1:
                return pd.Timedelta(weeks=n)
            kuy__jlufb = input_date_or_ts.weekday()
            if weekday != kuy__jlufb:
                xkffw__pwei = (weekday - kuy__jlufb) % 7
                if n > 0:
                    n = n - 1
            return pd.Timedelta(weeks=n, days=xkffw__pwei)
        return impl


def update_timedelta_with_transition(ts_value, timedelta):
    pass


@overload(update_timedelta_with_transition)
def overload_update_timedelta_with_transition(ts, td):
    if tz_has_transition_times(ts.tz):
        qpkv__xgnv = pytz.timezone(ts.tz)
        gnxah__xalyr = np.array(qpkv__xgnv._utc_transition_times, dtype=
            'M8[ns]').view('i8')
        jxgdm__vuvr = np.array(qpkv__xgnv._transition_info)[:, 0]
        jxgdm__vuvr = (pd.Series(jxgdm__vuvr).dt.total_seconds() * 1000000000
            ).astype(np.int64).values

        def impl_tz_aware(ts, td):
            zclb__iwqkl = ts.value
            dcl__dwk = zclb__iwqkl + td.value
            bildk__nqvf = np.searchsorted(gnxah__xalyr, zclb__iwqkl, side=
                'right') - 1
            wie__lztc = np.searchsorted(gnxah__xalyr, dcl__dwk, side='right'
                ) - 1
            xkffw__pwei = jxgdm__vuvr[bildk__nqvf] - jxgdm__vuvr[wie__lztc]
            return pd.Timedelta(td.value + xkffw__pwei)
        return impl_tz_aware
    else:
        return lambda ts, td: td


date_offset_unsupported_attrs = {'base', 'freqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
date_offset_unsupported = {'__call__', 'rollback', 'rollforward',
    'is_month_start', 'is_month_end', 'apply', 'apply_index', 'copy',
    'isAnchored', 'onOffset', 'is_anchored', 'is_on_offset',
    'is_quarter_start', 'is_quarter_end', 'is_year_start', 'is_year_end'}
month_end_unsupported_attrs = {'base', 'freqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
month_end_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
month_begin_unsupported_attrs = {'basefreqstr', 'kwds', 'name', 'nanos',
    'rule_code'}
month_begin_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
week_unsupported_attrs = {'basefreqstr', 'kwds', 'name', 'nanos', 'rule_code'}
week_unsupported = {'__call__', 'rollback', 'rollforward', 'apply',
    'apply_index', 'copy', 'isAnchored', 'onOffset', 'is_anchored',
    'is_on_offset', 'is_month_start', 'is_month_end', 'is_quarter_start',
    'is_quarter_end', 'is_year_start', 'is_year_end'}
offsets_unsupported = {pd.tseries.offsets.BusinessDay, pd.tseries.offsets.
    BDay, pd.tseries.offsets.BusinessHour, pd.tseries.offsets.
    CustomBusinessDay, pd.tseries.offsets.CDay, pd.tseries.offsets.
    CustomBusinessHour, pd.tseries.offsets.BusinessMonthEnd, pd.tseries.
    offsets.BMonthEnd, pd.tseries.offsets.BusinessMonthBegin, pd.tseries.
    offsets.BMonthBegin, pd.tseries.offsets.CustomBusinessMonthEnd, pd.
    tseries.offsets.CBMonthEnd, pd.tseries.offsets.CustomBusinessMonthBegin,
    pd.tseries.offsets.CBMonthBegin, pd.tseries.offsets.SemiMonthEnd, pd.
    tseries.offsets.SemiMonthBegin, pd.tseries.offsets.WeekOfMonth, pd.
    tseries.offsets.LastWeekOfMonth, pd.tseries.offsets.BQuarterEnd, pd.
    tseries.offsets.BQuarterBegin, pd.tseries.offsets.QuarterEnd, pd.
    tseries.offsets.QuarterBegin, pd.tseries.offsets.BYearEnd, pd.tseries.
    offsets.BYearBegin, pd.tseries.offsets.YearEnd, pd.tseries.offsets.
    YearBegin, pd.tseries.offsets.FY5253, pd.tseries.offsets.FY5253Quarter,
    pd.tseries.offsets.Easter, pd.tseries.offsets.Tick, pd.tseries.offsets.
    Day, pd.tseries.offsets.Hour, pd.tseries.offsets.Minute, pd.tseries.
    offsets.Second, pd.tseries.offsets.Milli, pd.tseries.offsets.Micro, pd.
    tseries.offsets.Nano}
frequencies_unsupported = {pd.tseries.frequencies.to_offset}


def _install_date_offsets_unsupported():
    for jmwu__igiba in date_offset_unsupported_attrs:
        inpys__clp = 'pandas.tseries.offsets.DateOffset.' + jmwu__igiba
        overload_attribute(DateOffsetType, jmwu__igiba)(
            create_unsupported_overload(inpys__clp))
    for jmwu__igiba in date_offset_unsupported:
        inpys__clp = 'pandas.tseries.offsets.DateOffset.' + jmwu__igiba
        overload_method(DateOffsetType, jmwu__igiba)(
            create_unsupported_overload(inpys__clp))


def _install_month_begin_unsupported():
    for jmwu__igiba in month_begin_unsupported_attrs:
        inpys__clp = 'pandas.tseries.offsets.MonthBegin.' + jmwu__igiba
        overload_attribute(MonthBeginType, jmwu__igiba)(
            create_unsupported_overload(inpys__clp))
    for jmwu__igiba in month_begin_unsupported:
        inpys__clp = 'pandas.tseries.offsets.MonthBegin.' + jmwu__igiba
        overload_method(MonthBeginType, jmwu__igiba)(
            create_unsupported_overload(inpys__clp))


def _install_month_end_unsupported():
    for jmwu__igiba in date_offset_unsupported_attrs:
        inpys__clp = 'pandas.tseries.offsets.MonthEnd.' + jmwu__igiba
        overload_attribute(MonthEndType, jmwu__igiba)(
            create_unsupported_overload(inpys__clp))
    for jmwu__igiba in date_offset_unsupported:
        inpys__clp = 'pandas.tseries.offsets.MonthEnd.' + jmwu__igiba
        overload_method(MonthEndType, jmwu__igiba)(create_unsupported_overload
            (inpys__clp))


def _install_week_unsupported():
    for jmwu__igiba in week_unsupported_attrs:
        inpys__clp = 'pandas.tseries.offsets.Week.' + jmwu__igiba
        overload_attribute(WeekType, jmwu__igiba)(create_unsupported_overload
            (inpys__clp))
    for jmwu__igiba in week_unsupported:
        inpys__clp = 'pandas.tseries.offsets.Week.' + jmwu__igiba
        overload_method(WeekType, jmwu__igiba)(create_unsupported_overload(
            inpys__clp))


def _install_offsets_unsupported():
    for fqdq__vmxwf in offsets_unsupported:
        inpys__clp = 'pandas.tseries.offsets.' + fqdq__vmxwf.__name__
        overload(fqdq__vmxwf)(create_unsupported_overload(inpys__clp))


def _install_frequencies_unsupported():
    for fqdq__vmxwf in frequencies_unsupported:
        inpys__clp = 'pandas.tseries.frequencies.' + fqdq__vmxwf.__name__
        overload(fqdq__vmxwf)(create_unsupported_overload(inpys__clp))


_install_date_offsets_unsupported()
_install_month_begin_unsupported()
_install_month_end_unsupported()
_install_week_unsupported()
_install_offsets_unsupported()
_install_frequencies_unsupported()
