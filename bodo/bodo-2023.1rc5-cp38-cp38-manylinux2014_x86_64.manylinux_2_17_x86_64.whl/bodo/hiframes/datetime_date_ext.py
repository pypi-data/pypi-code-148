"""Numba extension support for datetime.date objects and their arrays.
"""
import datetime
import operator
import warnings
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_builtin, lower_constant
from numba.core.typing.templates import AttributeTemplate, infer_getattr
from numba.core.utils import PYVERSION
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_getattr, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_datetime_ext import DatetimeDatetimeType
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_type
from bodo.libs import hdatetime_ext
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, is_iterable_type, is_list_like_index_type, is_overload_int, is_overload_none
ll.add_symbol('box_datetime_date_array', hdatetime_ext.box_datetime_date_array)
ll.add_symbol('unbox_datetime_date_array', hdatetime_ext.
    unbox_datetime_date_array)
ll.add_symbol('get_isocalendar', hdatetime_ext.get_isocalendar)


class DatetimeDateType(types.Type):

    def __init__(self):
        super(DatetimeDateType, self).__init__(name='DatetimeDateType()')
        self.bitwidth = 64


datetime_date_type = DatetimeDateType()


@typeof_impl.register(datetime.date)
def typeof_datetime_date(val, c):
    return datetime_date_type


register_model(DatetimeDateType)(models.IntegerModel)


@infer_getattr
class DatetimeAttribute(AttributeTemplate):
    key = DatetimeDateType

    def resolve_year(self, typ):
        return types.int64

    def resolve_month(self, typ):
        return types.int64

    def resolve_day(self, typ):
        return types.int64


@lower_getattr(DatetimeDateType, 'year')
def datetime_get_year(context, builder, typ, val):
    return builder.lshr(val, lir.Constant(lir.IntType(64), 32))


@lower_getattr(DatetimeDateType, 'month')
def datetime_get_month(context, builder, typ, val):
    return builder.and_(builder.lshr(val, lir.Constant(lir.IntType(64), 16)
        ), lir.Constant(lir.IntType(64), 65535))


@lower_getattr(DatetimeDateType, 'day')
def datetime_get_day(context, builder, typ, val):
    return builder.and_(val, lir.Constant(lir.IntType(64), 65535))


@unbox(DatetimeDateType)
def unbox_datetime_date(typ, val, c):
    jsoim__rchi = c.pyapi.object_getattr_string(val, 'year')
    weu__cgv = c.pyapi.object_getattr_string(val, 'month')
    wbjl__gmmx = c.pyapi.object_getattr_string(val, 'day')
    whe__btjl = c.pyapi.long_as_longlong(jsoim__rchi)
    qwkxt__zqq = c.pyapi.long_as_longlong(weu__cgv)
    elrg__bfavj = c.pyapi.long_as_longlong(wbjl__gmmx)
    qru__zut = c.builder.add(elrg__bfavj, c.builder.add(c.builder.shl(
        whe__btjl, lir.Constant(lir.IntType(64), 32)), c.builder.shl(
        qwkxt__zqq, lir.Constant(lir.IntType(64), 16))))
    c.pyapi.decref(jsoim__rchi)
    c.pyapi.decref(weu__cgv)
    c.pyapi.decref(wbjl__gmmx)
    foa__iqu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(qru__zut, is_error=foa__iqu)


@lower_constant(DatetimeDateType)
def lower_constant_datetime_date(context, builder, ty, pyval):
    year = context.get_constant(types.int64, pyval.year)
    month = context.get_constant(types.int64, pyval.month)
    day = context.get_constant(types.int64, pyval.day)
    qru__zut = builder.add(day, builder.add(builder.shl(year, lir.Constant(
        lir.IntType(64), 32)), builder.shl(month, lir.Constant(lir.IntType(
        64), 16))))
    return qru__zut


@box(DatetimeDateType)
def box_datetime_date(typ, val, c):
    jsoim__rchi = c.pyapi.long_from_longlong(c.builder.lshr(val, lir.
        Constant(lir.IntType(64), 32)))
    weu__cgv = c.pyapi.long_from_longlong(c.builder.and_(c.builder.lshr(val,
        lir.Constant(lir.IntType(64), 16)), lir.Constant(lir.IntType(64), 
        65535)))
    wbjl__gmmx = c.pyapi.long_from_longlong(c.builder.and_(val, lir.
        Constant(lir.IntType(64), 65535)))
    mkv__kasdo = c.pyapi.unserialize(c.pyapi.serialize_object(datetime.date))
    npxd__rgi = c.pyapi.call_function_objargs(mkv__kasdo, (jsoim__rchi,
        weu__cgv, wbjl__gmmx))
    c.pyapi.decref(jsoim__rchi)
    c.pyapi.decref(weu__cgv)
    c.pyapi.decref(wbjl__gmmx)
    c.pyapi.decref(mkv__kasdo)
    return npxd__rgi


@type_callable(datetime.date)
def type_datetime_date(context):

    def typer(year, month, day):
        return datetime_date_type
    return typer


@lower_builtin(datetime.date, types.IntegerLiteral, types.IntegerLiteral,
    types.IntegerLiteral)
@lower_builtin(datetime.date, types.int64, types.int64, types.int64)
def impl_ctor_datetime_date(context, builder, sig, args):
    year, month, day = args
    qru__zut = builder.add(day, builder.add(builder.shl(year, lir.Constant(
        lir.IntType(64), 32)), builder.shl(month, lir.Constant(lir.IntType(
        64), 16))))
    return qru__zut


@intrinsic
def cast_int_to_datetime_date(typingctx, val=None):
    assert val == types.int64

    def codegen(context, builder, signature, args):
        return args[0]
    return datetime_date_type(types.int64), codegen


@intrinsic
def cast_datetime_date_to_int(typingctx, val=None):
    assert val == datetime_date_type

    def codegen(context, builder, signature, args):
        return args[0]
    return types.int64(datetime_date_type), codegen


"""
Following codes are copied from
https://github.com/python/cpython/blob/39a5c889d30d03a88102e56f03ee0c95db198fb3/Lib/datetime.py
"""
_MAXORDINAL = 3652059
_DAYS_IN_MONTH = np.array([-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 
    31], dtype=np.int64)
_DAYS_BEFORE_MONTH = np.array([-1, 0, 31, 59, 90, 120, 151, 181, 212, 243, 
    273, 304, 334], dtype=np.int64)


@register_jitable
def _is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


@register_jitable
def _days_before_year(year):
    y = year - 1
    return y * 365 + y // 4 - y // 100 + y // 400


@register_jitable
def _days_in_month(year, month):
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]


@register_jitable
def _days_before_month(year, month):
    return _DAYS_BEFORE_MONTH[month] + (month > 2 and _is_leap(year))


_DI400Y = _days_before_year(401)
_DI100Y = _days_before_year(101)
_DI4Y = _days_before_year(5)


@register_jitable
def _ymd2ord(year, month, day):
    cvj__qpnzj = _days_in_month(year, month)
    return _days_before_year(year) + _days_before_month(year, month) + day


@register_jitable
def _ord2ymd(n):
    n -= 1
    zpp__mcgkw, n = divmod(n, _DI400Y)
    year = zpp__mcgkw * 400 + 1
    ahe__zdzeg, n = divmod(n, _DI100Y)
    euvh__vqhzz, n = divmod(n, _DI4Y)
    dwgu__kzswn, n = divmod(n, 365)
    year += ahe__zdzeg * 100 + euvh__vqhzz * 4 + dwgu__kzswn
    if dwgu__kzswn == 4 or ahe__zdzeg == 4:
        return year - 1, 12, 31
    fbi__itk = dwgu__kzswn == 3 and (euvh__vqhzz != 24 or ahe__zdzeg == 3)
    month = n + 50 >> 5
    xpj__uohe = _DAYS_BEFORE_MONTH[month] + (month > 2 and fbi__itk)
    if xpj__uohe > n:
        month -= 1
        xpj__uohe -= _DAYS_IN_MONTH[month] + (month == 2 and fbi__itk)
    n -= xpj__uohe
    return year, month, n + 1


@register_jitable
def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


@intrinsic
def get_isocalendar(typingctx, dt_year, dt_month, dt_day):

    def codegen(context, builder, sig, args):
        year = cgutils.alloca_once(builder, lir.IntType(64))
        tjfnn__cbkcj = cgutils.alloca_once(builder, lir.IntType(64))
        qjk__ycis = cgutils.alloca_once(builder, lir.IntType(64))
        muz__qogzv = lir.FunctionType(lir.VoidType(), [lir.IntType(64), lir
            .IntType(64), lir.IntType(64), lir.IntType(64).as_pointer(),
            lir.IntType(64).as_pointer(), lir.IntType(64).as_pointer()])
        uuu__zen = cgutils.get_or_insert_function(builder.module,
            muz__qogzv, name='get_isocalendar')
        builder.call(uuu__zen, [args[0], args[1], args[2], year,
            tjfnn__cbkcj, qjk__ycis])
        return cgutils.pack_array(builder, [builder.load(year), builder.
            load(tjfnn__cbkcj), builder.load(qjk__ycis)])
    npxd__rgi = types.Tuple([types.int64, types.int64, types.int64])(types.
        int64, types.int64, types.int64), codegen
    return npxd__rgi


types.datetime_date_type = datetime_date_type


@register_jitable
def today_impl():
    with numba.objmode(d='datetime_date_type'):
        d = datetime.date.today()
    return d


@register_jitable
def fromordinal_impl(n):
    y, lqg__ktev, d = _ord2ymd(n)
    return datetime.date(y, lqg__ktev, d)


@overload_method(DatetimeDateType, 'replace')
def replace_overload(date, year=None, month=None, day=None):
    if not is_overload_none(year) and not is_overload_int(year):
        raise BodoError('date.replace(): year must be an integer')
    elif not is_overload_none(month) and not is_overload_int(month):
        raise BodoError('date.replace(): month must be an integer')
    elif not is_overload_none(day) and not is_overload_int(day):
        raise BodoError('date.replace(): day must be an integer')

    def impl(date, year=None, month=None, day=None):
        bcrp__hoywf = date.year if year is None else year
        iaor__eyf = date.month if month is None else month
        vzg__bwt = date.day if day is None else day
        return datetime.date(bcrp__hoywf, iaor__eyf, vzg__bwt)
    return impl


@overload_method(DatetimeDatetimeType, 'toordinal', no_unliteral=True)
@overload_method(DatetimeDateType, 'toordinal', no_unliteral=True)
def toordinal(date):

    def impl(date):
        return _ymd2ord(date.year, date.month, date.day)
    return impl


@overload_method(DatetimeDatetimeType, 'weekday', no_unliteral=True)
@overload_method(DatetimeDateType, 'weekday', no_unliteral=True)
def weekday(date):

    def impl(date):
        return (date.toordinal() + 6) % 7
    return impl


@overload_method(DatetimeDateType, 'isocalendar', no_unliteral=True)
def overload_pd_timestamp_isocalendar(date):

    def impl(date):
        year, tjfnn__cbkcj, qgp__utkib = get_isocalendar(date.year, date.
            month, date.day)
        return year, tjfnn__cbkcj, qgp__utkib
    return impl


def overload_add_operator_datetime_date(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            adwxq__twsce = lhs.toordinal() + rhs.days
            if 0 < adwxq__twsce <= _MAXORDINAL:
                return fromordinal_impl(adwxq__twsce)
            raise OverflowError('result out of range')
        return impl
    elif lhs == datetime_timedelta_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            adwxq__twsce = lhs.days + rhs.toordinal()
            if 0 < adwxq__twsce <= _MAXORDINAL:
                return fromordinal_impl(adwxq__twsce)
            raise OverflowError('result out of range')
        return impl


def overload_sub_operator_datetime_date(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            return lhs + datetime.timedelta(-rhs.days)
        return impl
    elif lhs == datetime_date_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            qyaie__jyisi = lhs.toordinal()
            emb__tzd = rhs.toordinal()
            return datetime.timedelta(qyaie__jyisi - emb__tzd)
        return impl
    if lhs == datetime_date_array_type and rhs == datetime_timedelta_type:

        def impl(lhs, rhs):
            ddd__nvp = lhs
            numba.parfors.parfor.init_prange()
            n = len(ddd__nvp)
            A = alloc_datetime_date_array(n)
            for ttlw__evnoi in numba.parfors.parfor.internal_prange(n):
                A[ttlw__evnoi] = ddd__nvp[ttlw__evnoi] - rhs
            return A
        return impl


@overload(min, no_unliteral=True)
def date_min(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@overload(max, no_unliteral=True)
def date_max(lhs, rhs):
    if lhs == datetime_date_type and rhs == datetime_date_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload_method(DatetimeDateType, '__hash__', no_unliteral=True)
def __hash__(td):

    def impl(td):
        ddcf__wxexn = np.uint8(td.year // 256)
        rji__atw = np.uint8(td.year % 256)
        month = np.uint8(td.month)
        day = np.uint8(td.day)
        vun__aclc = ddcf__wxexn, rji__atw, month, day
        return hash(vun__aclc)
    return impl


@overload(bool, inline='always', no_unliteral=True)
def date_to_bool(date):
    if date != datetime_date_type:
        return

    def impl(date):
        return True
    return impl


if PYVERSION >= (3, 9):
    IsoCalendarDate = datetime.date(2011, 1, 1).isocalendar().__class__


    class IsoCalendarDateType(types.Type):

        def __init__(self):
            super(IsoCalendarDateType, self).__init__(name=
                'IsoCalendarDateType()')
    iso_calendar_date_type = DatetimeDateType()

    @typeof_impl.register(IsoCalendarDate)
    def typeof_datetime_date(val, c):
        return iso_calendar_date_type


class DatetimeDateArrayType(types.ArrayCompatible):

    def __init__(self):
        super(DatetimeDateArrayType, self).__init__(name=
            'DatetimeDateArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return datetime_date_type

    def copy(self):
        return DatetimeDateArrayType()


datetime_date_array_type = DatetimeDateArrayType()
types.datetime_date_array_type = datetime_date_array_type
data_type = types.Array(types.int64, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(DatetimeDateArrayType)
class DatetimeDateArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        flu__yhzkk = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, flu__yhzkk)


make_attribute_wrapper(DatetimeDateArrayType, 'data', '_data')
make_attribute_wrapper(DatetimeDateArrayType, 'null_bitmap', '_null_bitmap')


@overload_method(DatetimeDateArrayType, 'copy', no_unliteral=True)
def overload_datetime_date_arr_copy(A):
    return lambda A: bodo.hiframes.datetime_date_ext.init_datetime_date_array(A
        ._data.copy(), A._null_bitmap.copy())


@overload_attribute(DatetimeDateArrayType, 'dtype')
def overload_datetime_date_arr_dtype(A):
    return lambda A: np.object_


@unbox(DatetimeDateArrayType)
def unbox_datetime_date_array(typ, val, c):
    n = bodo.utils.utils.object_length(c, val)
    lhv__xby = types.Array(types.intp, 1, 'C')
    gmavh__iad = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        lhv__xby, [n])
    dtcyn__kzax = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    spo__ohoq = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types
        .Array(types.uint8, 1, 'C'), [dtcyn__kzax])
    muz__qogzv = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64), lir.IntType(64).as_pointer(), lir.
        IntType(8).as_pointer()])
    qvrey__mllfg = cgutils.get_or_insert_function(c.builder.module,
        muz__qogzv, name='unbox_datetime_date_array')
    c.builder.call(qvrey__mllfg, [val, n, gmavh__iad.data, spo__ohoq.data])
    fphlg__eyme = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    fphlg__eyme.data = gmavh__iad._getvalue()
    fphlg__eyme.null_bitmap = spo__ohoq._getvalue()
    foa__iqu = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(fphlg__eyme._getvalue(), is_error=foa__iqu)


def int_to_datetime_date_python(ia):
    return datetime.date(ia >> 32, ia >> 16 & 65535, ia & 65535)


def int_array_to_datetime_date(ia):
    return np.vectorize(int_to_datetime_date_python, otypes=[object])(ia)


@box(DatetimeDateArrayType)
def box_datetime_date_array(typ, val, c):
    ddd__nvp = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    gmavh__iad = c.context.make_array(types.Array(types.int64, 1, 'C'))(c.
        context, c.builder, ddd__nvp.data)
    hrm__bnqwj = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, ddd__nvp.null_bitmap).data
    n = c.builder.extract_value(gmavh__iad.shape, 0)
    muz__qogzv = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), lir.
        IntType(64).as_pointer(), lir.IntType(8).as_pointer()])
    mgnn__ihy = cgutils.get_or_insert_function(c.builder.module, muz__qogzv,
        name='box_datetime_date_array')
    ryqa__lyll = c.builder.call(mgnn__ihy, [n, gmavh__iad.data, hrm__bnqwj])
    c.context.nrt.decref(c.builder, typ, val)
    return ryqa__lyll


@intrinsic
def init_datetime_date_array(typingctx, data, nulls=None):
    assert data == types.Array(types.int64, 1, 'C') or data == types.Array(
        types.NPDatetime('ns'), 1, 'C')
    assert nulls == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        nfg__zsi, zwxti__njf = args
        hsh__jdgye = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        hsh__jdgye.data = nfg__zsi
        hsh__jdgye.null_bitmap = zwxti__njf
        context.nrt.incref(builder, signature.args[0], nfg__zsi)
        context.nrt.incref(builder, signature.args[1], zwxti__njf)
        return hsh__jdgye._getvalue()
    sig = datetime_date_array_type(data, nulls)
    return sig, codegen


@lower_constant(DatetimeDateArrayType)
def lower_constant_datetime_date_arr(context, builder, typ, pyval):
    n = len(pyval)
    iqibj__vvt = (1970 << 32) + (1 << 16) + 1
    gmavh__iad = np.full(n, iqibj__vvt, np.int64)
    ffjqm__dpty = np.empty(n + 7 >> 3, np.uint8)
    for ttlw__evnoi, deox__zsvf in enumerate(pyval):
        onyhc__kbj = pd.isna(deox__zsvf)
        bodo.libs.int_arr_ext.set_bit_to_arr(ffjqm__dpty, ttlw__evnoi, int(
            not onyhc__kbj))
        if not onyhc__kbj:
            gmavh__iad[ttlw__evnoi] = (deox__zsvf.year << 32) + (deox__zsvf
                .month << 16) + deox__zsvf.day
    yqt__ewrfs = context.get_constant_generic(builder, data_type, gmavh__iad)
    tee__gfiyq = context.get_constant_generic(builder, nulls_type, ffjqm__dpty)
    return lir.Constant.literal_struct([yqt__ewrfs, tee__gfiyq])


@numba.njit(no_cpython_wrapper=True)
def alloc_datetime_date_array(n):
    gmavh__iad = np.empty(n, dtype=np.int64)
    nulls = np.full(n + 7 >> 3, 255, np.uint8)
    return init_datetime_date_array(gmavh__iad, nulls)


def alloc_datetime_date_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_datetime_date_ext_alloc_datetime_date_array
    ) = alloc_datetime_date_array_equiv


@overload(operator.getitem, no_unliteral=True)
def dt_date_arr_getitem(A, ind):
    if A != datetime_date_array_type:
        return
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda A, ind: cast_int_to_datetime_date(A._data[ind])
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            ajcp__msy, bhoo__dum = array_getitem_bool_index(A, ind)
            return init_datetime_date_array(ajcp__msy, bhoo__dum)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            ajcp__msy, bhoo__dum = array_getitem_int_index(A, ind)
            return init_datetime_date_array(ajcp__msy, bhoo__dum)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            ajcp__msy, bhoo__dum = array_getitem_slice_index(A, ind)
            return init_datetime_date_array(ajcp__msy, bhoo__dum)
        return impl_slice
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for DatetimeDateArray with indexing type {ind} not supported.'
            )


@overload(operator.setitem, no_unliteral=True)
def dt_date_arr_setitem(A, idx, val):
    if A != datetime_date_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    dyfbm__qjck = (
        f"setitem for DatetimeDateArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == datetime_date_type:

            def impl(A, idx, val):
                A._data[idx] = cast_datetime_date_to_int(val)
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl
        else:
            raise BodoError(dyfbm__qjck)
    if not (is_iterable_type(val) and val.dtype == bodo.datetime_date_type or
        types.unliteral(val) == datetime_date_type):
        raise BodoError(dyfbm__qjck)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):
        if types.unliteral(val) == datetime_date_type:
            return lambda A, idx, val: array_setitem_int_index(A, idx,
                cast_datetime_date_to_int(val))

        def impl_arr_ind(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if types.unliteral(val) == datetime_date_type:
            return lambda A, idx, val: array_setitem_bool_index(A, idx,
                cast_datetime_date_to_int(val))

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):
        if types.unliteral(val) == datetime_date_type:
            return lambda A, idx, val: array_setitem_slice_index(A, idx,
                cast_datetime_date_to_int(val))

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for DatetimeDateArray with indexing type {idx} not supported.'
        )


@overload(len, no_unliteral=True)
def overload_len_datetime_date_arr(A):
    if A == datetime_date_array_type:
        return lambda A: len(A._data)


@overload_attribute(DatetimeDateArrayType, 'shape')
def overload_datetime_date_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(DatetimeDateArrayType, 'nbytes')
def datetime_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


def create_cmp_op_overload(op):

    def overload_date_cmp(lhs, rhs):
        if lhs == datetime_date_type and rhs == datetime_date_type:

            def impl(lhs, rhs):
                y, tlgf__qyxx = lhs.year, rhs.year
                lqg__ktev, jsgwb__pft = lhs.month, rhs.month
                d, wflby__tzrtu = lhs.day, rhs.day
                return op(_cmp((y, lqg__ktev, d), (tlgf__qyxx, jsgwb__pft,
                    wflby__tzrtu)), 0)
            return impl
    return overload_date_cmp


def create_datetime_date_cmp_op_overload(op):

    def overload_cmp(lhs, rhs):
        oivy__niom = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[op]} {rhs} is always {op == operator.ne} in Python. If this is unexpected there may be a bug in your code.'
            )
        warnings.warn(oivy__niom, bodo.utils.typing.BodoWarning)
        if op == operator.eq:
            return lambda lhs, rhs: False
        elif op == operator.ne:
            return lambda lhs, rhs: True
    return overload_cmp


def create_datetime_array_date_cmp_op_overload(op):

    def overload_arr_cmp(lhs, rhs):
        if isinstance(lhs, types.Array) and lhs.dtype == bodo.datetime64ns:
            if rhs == datetime_date_type:

                def impl(lhs, rhs):
                    numba.parfors.parfor.init_prange()
                    n = len(lhs)
                    lpf__ucld = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                    for ttlw__evnoi in numba.parfors.parfor.internal_prange(n):
                        if bodo.libs.array_kernels.isna(lhs, ttlw__evnoi):
                            bodo.libs.array_kernels.setna(lpf__ucld,
                                ttlw__evnoi)
                        else:
                            lpf__ucld[ttlw__evnoi] = op(lhs[ttlw__evnoi],
                                bodo.utils.conversion.
                                unbox_if_tz_naive_timestamp(pd.Timestamp(rhs)))
                    return lpf__ucld
                return impl
            elif rhs == datetime_date_array_type:

                def impl(lhs, rhs):
                    numba.parfors.parfor.init_prange()
                    n = len(lhs)
                    lpf__ucld = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                    for ttlw__evnoi in numba.parfors.parfor.internal_prange(n):
                        if bodo.libs.array_kernels.isna(lhs, ttlw__evnoi
                            ) or bodo.libs.array_kernels.isna(rhs, ttlw__evnoi
                            ):
                            bodo.libs.array_kernels.setna(lpf__ucld,
                                ttlw__evnoi)
                        else:
                            lpf__ucld[ttlw__evnoi] = op(lhs[ttlw__evnoi],
                                bodo.utils.conversion.
                                unbox_if_tz_naive_timestamp(pd.Timestamp(
                                rhs[ttlw__evnoi])))
                    return lpf__ucld
                return impl
        elif isinstance(rhs, types.Array) and rhs.dtype == bodo.datetime64ns:
            if lhs == datetime_date_type:

                def impl(lhs, rhs):
                    numba.parfors.parfor.init_prange()
                    n = len(rhs)
                    lpf__ucld = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                    for ttlw__evnoi in numba.parfors.parfor.internal_prange(n):
                        if bodo.libs.array_kernels.isna(rhs, ttlw__evnoi):
                            bodo.libs.array_kernels.setna(lpf__ucld,
                                ttlw__evnoi)
                        else:
                            lpf__ucld[ttlw__evnoi] = op(bodo.utils.
                                conversion.unbox_if_tz_naive_timestamp(pd.
                                Timestamp(lhs)), rhs[ttlw__evnoi])
                    return lpf__ucld
                return impl
            elif lhs == datetime_date_array_type:

                def impl(lhs, rhs):
                    numba.parfors.parfor.init_prange()
                    n = len(rhs)
                    lpf__ucld = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                    for ttlw__evnoi in numba.parfors.parfor.internal_prange(n):
                        if bodo.libs.array_kernels.isna(lhs, ttlw__evnoi
                            ) or bodo.libs.array_kernels.isna(rhs, ttlw__evnoi
                            ):
                            bodo.libs.array_kernels.setna(lpf__ucld,
                                ttlw__evnoi)
                        else:
                            lpf__ucld[ttlw__evnoi] = op(bodo.utils.
                                conversion.unbox_if_tz_naive_timestamp(pd.
                                Timestamp(lhs[ttlw__evnoi])), rhs[ttlw__evnoi])
                    return lpf__ucld
                return impl
    return overload_arr_cmp


def create_cmp_op_overload_arr(op):

    def overload_date_arr_cmp(lhs, rhs):
        if op == operator.ne:
            rve__gdnc = True
        else:
            rve__gdnc = False
        if lhs == datetime_date_array_type and rhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                lpf__ucld = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for ttlw__evnoi in numba.parfors.parfor.internal_prange(n):
                    ysx__xojfn = bodo.libs.array_kernels.isna(lhs, ttlw__evnoi)
                    mqfik__esif = bodo.libs.array_kernels.isna(rhs, ttlw__evnoi
                        )
                    if ysx__xojfn or mqfik__esif:
                        ymrj__imony = rve__gdnc
                    else:
                        ymrj__imony = op(lhs[ttlw__evnoi], rhs[ttlw__evnoi])
                    lpf__ucld[ttlw__evnoi] = ymrj__imony
                return lpf__ucld
            return impl
        elif lhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                lpf__ucld = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for ttlw__evnoi in numba.parfors.parfor.internal_prange(n):
                    eyars__irtm = bodo.libs.array_kernels.isna(lhs, ttlw__evnoi
                        )
                    if eyars__irtm:
                        ymrj__imony = rve__gdnc
                    else:
                        ymrj__imony = op(lhs[ttlw__evnoi], rhs)
                    lpf__ucld[ttlw__evnoi] = ymrj__imony
                return lpf__ucld
            return impl
        elif rhs == datetime_date_array_type:

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                n = len(rhs)
                lpf__ucld = bodo.libs.bool_arr_ext.alloc_bool_array(n)
                for ttlw__evnoi in numba.parfors.parfor.internal_prange(n):
                    eyars__irtm = bodo.libs.array_kernels.isna(rhs, ttlw__evnoi
                        )
                    if eyars__irtm:
                        ymrj__imony = rve__gdnc
                    else:
                        ymrj__imony = op(lhs, rhs[ttlw__evnoi])
                    lpf__ucld[ttlw__evnoi] = ymrj__imony
                return lpf__ucld
            return impl
    return overload_date_arr_cmp
