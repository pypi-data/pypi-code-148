import datetime
import numba
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
"""
Implementation is based on
https://github.com/python/cpython/blob/39a5c889d30d03a88102e56f03ee0c95db198fb3/Lib/datetime.py
"""


class DatetimeDatetimeType(types.Type):

    def __init__(self):
        super(DatetimeDatetimeType, self).__init__(name=
            'DatetimeDatetimeType()')


datetime_datetime_type = DatetimeDatetimeType()
types.datetime_datetime_type = datetime_datetime_type


@typeof_impl.register(datetime.datetime)
def typeof_datetime_datetime(val, c):
    return datetime_datetime_type


@register_model(DatetimeDatetimeType)
class DatetimeDateTimeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        fagyg__gpxtf = [('year', types.int64), ('month', types.int64), (
            'day', types.int64), ('hour', types.int64), ('minute', types.
            int64), ('second', types.int64), ('microsecond', types.int64)]
        super(DatetimeDateTimeModel, self).__init__(dmm, fe_type, fagyg__gpxtf)


@box(DatetimeDatetimeType)
def box_datetime_datetime(typ, val, c):
    nucj__yih = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    enhy__ybg = c.pyapi.long_from_longlong(nucj__yih.year)
    dler__rdcwg = c.pyapi.long_from_longlong(nucj__yih.month)
    hazym__qfjxi = c.pyapi.long_from_longlong(nucj__yih.day)
    hpzg__exazy = c.pyapi.long_from_longlong(nucj__yih.hour)
    tfp__hac = c.pyapi.long_from_longlong(nucj__yih.minute)
    cbaes__gkse = c.pyapi.long_from_longlong(nucj__yih.second)
    xnwgz__heb = c.pyapi.long_from_longlong(nucj__yih.microsecond)
    ocg__mbwa = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.datetime)
        )
    vho__fqu = c.pyapi.call_function_objargs(ocg__mbwa, (enhy__ybg,
        dler__rdcwg, hazym__qfjxi, hpzg__exazy, tfp__hac, cbaes__gkse,
        xnwgz__heb))
    c.pyapi.decref(enhy__ybg)
    c.pyapi.decref(dler__rdcwg)
    c.pyapi.decref(hazym__qfjxi)
    c.pyapi.decref(hpzg__exazy)
    c.pyapi.decref(tfp__hac)
    c.pyapi.decref(cbaes__gkse)
    c.pyapi.decref(xnwgz__heb)
    c.pyapi.decref(ocg__mbwa)
    return vho__fqu


@unbox(DatetimeDatetimeType)
def unbox_datetime_datetime(typ, val, c):
    enhy__ybg = c.pyapi.object_getattr_string(val, 'year')
    dler__rdcwg = c.pyapi.object_getattr_string(val, 'month')
    hazym__qfjxi = c.pyapi.object_getattr_string(val, 'day')
    hpzg__exazy = c.pyapi.object_getattr_string(val, 'hour')
    tfp__hac = c.pyapi.object_getattr_string(val, 'minute')
    cbaes__gkse = c.pyapi.object_getattr_string(val, 'second')
    xnwgz__heb = c.pyapi.object_getattr_string(val, 'microsecond')
    nucj__yih = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    nucj__yih.year = c.pyapi.long_as_longlong(enhy__ybg)
    nucj__yih.month = c.pyapi.long_as_longlong(dler__rdcwg)
    nucj__yih.day = c.pyapi.long_as_longlong(hazym__qfjxi)
    nucj__yih.hour = c.pyapi.long_as_longlong(hpzg__exazy)
    nucj__yih.minute = c.pyapi.long_as_longlong(tfp__hac)
    nucj__yih.second = c.pyapi.long_as_longlong(cbaes__gkse)
    nucj__yih.microsecond = c.pyapi.long_as_longlong(xnwgz__heb)
    c.pyapi.decref(enhy__ybg)
    c.pyapi.decref(dler__rdcwg)
    c.pyapi.decref(hazym__qfjxi)
    c.pyapi.decref(hpzg__exazy)
    c.pyapi.decref(tfp__hac)
    c.pyapi.decref(cbaes__gkse)
    c.pyapi.decref(xnwgz__heb)
    sltcr__noy = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(nucj__yih._getvalue(), is_error=sltcr__noy)


@lower_constant(DatetimeDatetimeType)
def constant_datetime(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    hour = context.get_constant(types.int64, pyval.hour)
    minute = context.get_constant(types.int64, pyval.minute)
    second = context.get_constant(types.int64, pyval.second)
    microsecond = context.get_constant(types.int64, pyval.microsecond)
    return lir.Constant.literal_struct([year, month, day, hour, minute,
        second, microsecond])


@overload(datetime.datetime, no_unliteral=True)
def datetime_datetime(year, month, day, hour=0, minute=0, second=0,
    microsecond=0):

    def impl_datetime(year, month, day, hour=0, minute=0, second=0,
        microsecond=0):
        return init_datetime(year, month, day, hour, minute, second,
            microsecond)
    return impl_datetime


@intrinsic
def init_datetime(typingctx, year, month, day, hour, minute, second,
    microsecond):

    def codegen(context, builder, signature, args):
        typ = signature.return_type
        nucj__yih = cgutils.create_struct_proxy(typ)(context, builder)
        nucj__yih.year = args[0]
        nucj__yih.month = args[1]
        nucj__yih.day = args[2]
        nucj__yih.hour = args[3]
        nucj__yih.minute = args[4]
        nucj__yih.second = args[5]
        nucj__yih.microsecond = args[6]
        return nucj__yih._getvalue()
    return DatetimeDatetimeType()(year, month, day, hour, minute, second,
        microsecond), codegen


make_attribute_wrapper(DatetimeDatetimeType, 'year', '_year')
make_attribute_wrapper(DatetimeDatetimeType, 'month', '_month')
make_attribute_wrapper(DatetimeDatetimeType, 'day', '_day')
make_attribute_wrapper(DatetimeDatetimeType, 'hour', '_hour')
make_attribute_wrapper(DatetimeDatetimeType, 'minute', '_minute')
make_attribute_wrapper(DatetimeDatetimeType, 'second', '_second')
make_attribute_wrapper(DatetimeDatetimeType, 'microsecond', '_microsecond')


@overload_attribute(DatetimeDatetimeType, 'year')
def datetime_get_year(dt):

    def impl(dt):
        return dt._year
    return impl


@overload_attribute(DatetimeDatetimeType, 'month')
def datetime_get_month(dt):

    def impl(dt):
        return dt._month
    return impl


@overload_attribute(DatetimeDatetimeType, 'day')
def datetime_get_day(dt):

    def impl(dt):
        return dt._day
    return impl


@overload_attribute(DatetimeDatetimeType, 'hour')
def datetime_get_hour(dt):

    def impl(dt):
        return dt._hour
    return impl


@overload_attribute(DatetimeDatetimeType, 'minute')
def datetime_get_minute(dt):

    def impl(dt):
        return dt._minute
    return impl


@overload_attribute(DatetimeDatetimeType, 'second')
def datetime_get_second(dt):

    def impl(dt):
        return dt._second
    return impl


@overload_attribute(DatetimeDatetimeType, 'microsecond')
def datetime_get_microsecond(dt):

    def impl(dt):
        return dt._microsecond
    return impl


@overload_method(DatetimeDatetimeType, 'date', no_unliteral=True)
def date(dt):

    def impl(dt):
        return datetime.date(dt.year, dt.month, dt.day)
    return impl


@register_jitable
def now_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.now()
    return d


@register_jitable
def today_impl():
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.today()
    return d


@register_jitable
def strptime_impl(date_string, dtformat):
    with numba.objmode(d='datetime_datetime_type'):
        d = datetime.datetime.strptime(date_string, dtformat)
    return d


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


def create_cmp_op_overload(op):

    def overload_datetime_cmp(lhs, rhs):
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

            def impl(lhs, rhs):
                y, ttomq__yrhc = lhs.year, rhs.year
                irf__tpl, slx__ehqa = lhs.month, rhs.month
                d, jsef__iudt = lhs.day, rhs.day
                jsksu__pequ, swieo__rvzk = lhs.hour, rhs.hour
                cmpi__evab, twgq__bjvjt = lhs.minute, rhs.minute
                oczvd__rkj, kqvm__wrpt = lhs.second, rhs.second
                lxg__gwytd, inrf__zbuo = lhs.microsecond, rhs.microsecond
                return op(_cmp((y, irf__tpl, d, jsksu__pequ, cmpi__evab,
                    oczvd__rkj, lxg__gwytd), (ttomq__yrhc, slx__ehqa,
                    jsef__iudt, swieo__rvzk, twgq__bjvjt, kqvm__wrpt,
                    inrf__zbuo)), 0)
            return impl
    return overload_datetime_cmp


def overload_sub_operator_datetime_datetime(lhs, rhs):
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:

        def impl(lhs, rhs):
            wkq__geeq = lhs.toordinal()
            jmzvn__vcby = rhs.toordinal()
            bzypa__whn = lhs.second + lhs.minute * 60 + lhs.hour * 3600
            gupxw__fwpzg = rhs.second + rhs.minute * 60 + rhs.hour * 3600
            yvtn__qmdij = datetime.timedelta(wkq__geeq - jmzvn__vcby, 
                bzypa__whn - gupxw__fwpzg, lhs.microsecond - rhs.microsecond)
            return yvtn__qmdij
        return impl


@lower_cast(types.Optional(numba.core.types.NPTimedelta('ns')), numba.core.
    types.NPTimedelta('ns'))
@lower_cast(types.Optional(numba.core.types.NPDatetime('ns')), numba.core.
    types.NPDatetime('ns'))
def optional_dt64_to_dt64(context, builder, fromty, toty, val):
    tic__ewfso = context.make_helper(builder, fromty, value=val)
    lsvnf__qkl = cgutils.as_bool_bit(builder, tic__ewfso.valid)
    with builder.if_else(lsvnf__qkl) as (svizv__gxgt, cdpc__kxck):
        with svizv__gxgt:
            xmfwy__tmizk = context.cast(builder, tic__ewfso.data, fromty.
                type, toty)
            rmig__qsw = builder.block
        with cdpc__kxck:
            uxu__kcjuu = numba.np.npdatetime.NAT
            vcw__xmmed = builder.block
    vho__fqu = builder.phi(xmfwy__tmizk.type)
    vho__fqu.add_incoming(xmfwy__tmizk, rmig__qsw)
    vho__fqu.add_incoming(uxu__kcjuu, vcw__xmmed)
    return vho__fqu
