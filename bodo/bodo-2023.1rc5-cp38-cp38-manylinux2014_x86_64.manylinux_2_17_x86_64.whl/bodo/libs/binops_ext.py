""" Implementation of binary operators for the different types.
    Currently implemented operators:
        arith: add, sub, mul, truediv, floordiv, mod, pow
        cmp: lt, le, eq, ne, ge, gt
"""
import operator
import numba
from numba.core import types
from numba.core.imputils import lower_builtin
from numba.core.typing.builtins import machine_ints
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type, datetime_timedelta_type
from bodo.hiframes.datetime_timedelta_ext import datetime_datetime_type, datetime_timedelta_array_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import DatetimeIndexType, HeterogeneousIndexType, is_index_type
from bodo.hiframes.pd_offsets_ext import date_offset_type, month_begin_type, month_end_type, week_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_tz_naive_type
from bodo.hiframes.series_impl import SeriesType
from bodo.hiframes.time_ext import TimeType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_ext import string_type
from bodo.utils.typing import BodoError, is_overload_bool, is_str_arr_type, is_timedelta_type


class SeriesCmpOpTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        lhs, rhs = args
        if cmp_timeseries(lhs, rhs) or (isinstance(lhs, DataFrameType) or
            isinstance(rhs, DataFrameType)) or not (isinstance(lhs,
            SeriesType) or isinstance(rhs, SeriesType)):
            return
        if is_cmp_tz_mismatch(lhs, rhs):
            hugmn__aqoy, fgsv__cqqir = get_series_tz(lhs)
            tte__ozrg, fgsv__cqqir = get_series_tz(rhs)
            raise BodoError(
                f'{numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} with two Timestamps requires both Timestamps share the same timezone. '
                 +
                f'Argument 0 has timezone {hugmn__aqoy} and argument 1 has timezone {tte__ozrg}. '
                 +
                'To compare these values please convert to timezone naive with ts.tz_convert(None).'
                )
        ztcy__dbgo = lhs.data if isinstance(lhs, SeriesType) else lhs
        gora__lcd = rhs.data if isinstance(rhs, SeriesType) else rhs
        if ztcy__dbgo in (bodo.pd_timestamp_tz_naive_type, bodo.
            pd_timedelta_type) and gora__lcd.dtype in (bodo.datetime64ns,
            bodo.timedelta64ns):
            ztcy__dbgo = gora__lcd.dtype
        elif gora__lcd in (bodo.pd_timestamp_tz_naive_type, bodo.
            pd_timedelta_type) and ztcy__dbgo.dtype in (bodo.datetime64ns,
            bodo.timedelta64ns):
            gora__lcd = ztcy__dbgo.dtype
        ofmg__zrpf = ztcy__dbgo, gora__lcd
        udh__lawxb = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            tqp__mpri = self.context.resolve_function_type(self.key,
                ofmg__zrpf, {}).return_type
        except Exception as mwm__bjsbr:
            raise BodoError(udh__lawxb)
        if is_overload_bool(tqp__mpri):
            raise BodoError(udh__lawxb)
        qnaj__lsu = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        ciem__kyqa = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        xem__hmmws = types.bool_
        sofvz__nfx = SeriesType(xem__hmmws, tqp__mpri, qnaj__lsu, ciem__kyqa)
        return sofvz__nfx(*args)


def series_cmp_op_lower(op):

    def lower_impl(context, builder, sig, args):
        qwikf__zns = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if qwikf__zns is None:
            qwikf__zns = create_overload_cmp_operator(op)(*sig.args)
        return context.compile_internal(builder, qwikf__zns, sig, args)
    return lower_impl


class SeriesAndOrTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        lhs, rhs = args
        if not (isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType)):
            return
        ztcy__dbgo = lhs.data if isinstance(lhs, SeriesType) else lhs
        gora__lcd = rhs.data if isinstance(rhs, SeriesType) else rhs
        ofmg__zrpf = ztcy__dbgo, gora__lcd
        udh__lawxb = (
            f'{lhs} {numba.core.utils.OPERATORS_TO_BUILTINS[self.key]} {rhs} not supported'
            )
        try:
            tqp__mpri = self.context.resolve_function_type(self.key,
                ofmg__zrpf, {}).return_type
        except Exception as ypq__pxu:
            raise BodoError(udh__lawxb)
        qnaj__lsu = lhs.index if isinstance(lhs, SeriesType) else rhs.index
        ciem__kyqa = lhs.name_typ if isinstance(lhs, SeriesType
            ) else rhs.name_typ
        xem__hmmws = tqp__mpri.dtype
        sofvz__nfx = SeriesType(xem__hmmws, tqp__mpri, qnaj__lsu, ciem__kyqa)
        return sofvz__nfx(*args)


def lower_series_and_or(op):

    def lower_and_or_impl(context, builder, sig, args):
        qwikf__zns = bodo.hiframes.series_impl.create_binary_op_overload(op)(*
            sig.args)
        if qwikf__zns is None:
            lhs, rhs = sig.args
            if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType
                ):
                qwikf__zns = (bodo.hiframes.dataframe_impl.
                    create_binary_op_overload(op)(*sig.args))
        return context.compile_internal(builder, qwikf__zns, sig, args)
    return lower_and_or_impl


def overload_add_operator_scalars(lhs, rhs):
    if lhs == week_type or rhs == week_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_week_offset_type(lhs, rhs))
    if lhs == month_begin_type or rhs == month_begin_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_begin_offset_type(lhs, rhs))
    if lhs == month_end_type or rhs == month_end_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_month_end_offset_type(lhs, rhs))
    if lhs == date_offset_type or rhs == date_offset_type:
        return (bodo.hiframes.pd_offsets_ext.
            overload_add_operator_date_offset_type(lhs, rhs))
    if add_timestamp(lhs, rhs):
        return bodo.hiframes.pd_timestamp_ext.overload_add_operator_timestamp(
            lhs, rhs)
    if add_dt_td_and_dt_date(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_add_operator_datetime_date(lhs, rhs))
    if add_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_add_operator_datetime_timedelta(lhs, rhs))
    raise_error_if_not_numba_supported(operator.add, lhs, rhs)


def overload_sub_operator_scalars(lhs, rhs):
    if sub_offset_to_datetime_or_timestamp(lhs, rhs):
        return bodo.hiframes.pd_offsets_ext.overload_sub_operator_offsets(lhs,
            rhs)
    if (isinstance(lhs, bodo.PandasTimestampType) and rhs in (
        datetime_timedelta_type, pd_timedelta_type) or lhs ==
        pd_timestamp_tz_naive_type and rhs == pd_timestamp_tz_naive_type):
        return bodo.hiframes.pd_timestamp_ext.overload_sub_operator_timestamp(
            lhs, rhs)
    if sub_dt_or_td(lhs, rhs):
        return (bodo.hiframes.datetime_date_ext.
            overload_sub_operator_datetime_date(lhs, rhs))
    if sub_datetime_and_timedeltas(lhs, rhs):
        return (bodo.hiframes.datetime_timedelta_ext.
            overload_sub_operator_datetime_timedelta(lhs, rhs))
    if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
        return (bodo.hiframes.datetime_datetime_ext.
            overload_sub_operator_datetime_datetime(lhs, rhs))
    raise_error_if_not_numba_supported(operator.sub, lhs, rhs)


def create_overload_arith_op(op):

    def overload_arith_operator(lhs, rhs):
        if op not in [operator.add, operator.sub]:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
                f'{op} operator')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
                f'{op} operator')
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if time_series_operation(lhs, rhs) and op in [operator.add,
            operator.sub]:
            return bodo.hiframes.series_dt_impl.create_bin_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return bodo.hiframes.series_impl.create_binary_op_overload(op)(lhs,
                rhs)
        if sub_dt_index_and_timestamp(lhs, rhs) and op == operator.sub:
            return (bodo.hiframes.pd_index_ext.
                overload_sub_operator_datetime_index(lhs, rhs))
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if args_td_and_int_array(lhs, rhs):
            return bodo.libs.int_arr_ext.get_int_array_op_pd_td(op)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if isinstance(lhs, FloatingArrayType) or isinstance(rhs,
            FloatingArrayType):
            return bodo.libs.float_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if op == operator.add and (is_str_arr_type(lhs) or types.unliteral(
            lhs) == string_type):
            return bodo.libs.str_arr_ext.overload_add_operator_string_array(lhs
                , rhs)
        if op == operator.add and (isinstance(lhs, bodo.DatetimeArrayType) or
            isinstance(rhs, bodo.DatetimeArrayType)):
            return (bodo.libs.pd_datetime_arr_ext.
                overload_add_operator_datetime_arr(lhs, rhs))
        if op == operator.add:
            return overload_add_operator_scalars(lhs, rhs)
        if op == operator.sub:
            return overload_sub_operator_scalars(lhs, rhs)
        if op == operator.mul:
            if mul_timedelta_and_int(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mul_operator_timedelta(lhs, rhs))
            if mul_string_arr_and_int(lhs, rhs):
                return bodo.libs.str_arr_ext.overload_mul_operator_str_arr(lhs,
                    rhs)
            if mul_date_offset_and_int(lhs, rhs):
                return (bodo.hiframes.pd_offsets_ext.
                    overload_mul_date_offset_types(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op in [operator.truediv, operator.floordiv]:
            if div_timedelta_and_int(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_pd_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_pd_timedelta(lhs, rhs))
            if div_datetime_timedelta(lhs, rhs):
                if op == operator.truediv:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_truediv_operator_dt_timedelta(lhs, rhs))
                else:
                    return (bodo.hiframes.datetime_timedelta_ext.
                        overload_floordiv_operator_dt_timedelta(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.mod:
            if mod_timedeltas(lhs, rhs):
                return (bodo.hiframes.datetime_timedelta_ext.
                    overload_mod_operator_timedeltas(lhs, rhs))
            raise_error_if_not_numba_supported(op, lhs, rhs)
        if op == operator.pow:
            raise_error_if_not_numba_supported(op, lhs, rhs)
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_arith_operator


def create_overload_cmp_operator(op):

    def overload_cmp_operator(lhs, rhs):
        if isinstance(lhs, DataFrameType) or isinstance(rhs, DataFrameType):
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(lhs,
                f'{op} operator')
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(rhs,
                f'{op} operator')
            return bodo.hiframes.dataframe_impl.create_binary_op_overload(op)(
                lhs, rhs)
        if cmp_timeseries(lhs, rhs):
            return bodo.hiframes.series_dt_impl.create_cmp_op_overload(op)(lhs,
                rhs)
        if isinstance(lhs, SeriesType) or isinstance(rhs, SeriesType):
            return
        if isinstance(lhs, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType
            ) or isinstance(rhs, bodo.libs.pd_datetime_arr_ext.
            DatetimeArrayType):
            return bodo.libs.pd_datetime_arr_ext.create_cmp_op_overload_arr(op
                )(lhs, rhs)
        if isinstance(lhs, types.Array
            ) and lhs.dtype == bodo.datetime64ns and rhs in (
            datetime_date_array_type, datetime_date_type) or lhs in (
            datetime_date_array_type, datetime_date_type) and isinstance(rhs,
            types.Array) and rhs.dtype == bodo.datetime64ns:
            return (bodo.hiframes.datetime_date_ext.
                create_datetime_array_date_cmp_op_overload(op)(lhs, rhs))
        if lhs == datetime_date_array_type or rhs == datetime_date_array_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload_arr(
                op)(lhs, rhs)
        if (lhs == datetime_timedelta_array_type or rhs ==
            datetime_timedelta_array_type):
            qwikf__zns = (bodo.hiframes.datetime_timedelta_ext.
                create_cmp_op_overload(op))
            return qwikf__zns(lhs, rhs)
        if is_str_arr_type(lhs) or is_str_arr_type(rhs):
            return bodo.libs.str_arr_ext.create_binary_op_overload(op)(lhs, rhs
                )
        if isinstance(lhs, Decimal128Type) and isinstance(rhs, Decimal128Type):
            return bodo.libs.decimal_arr_ext.decimal_create_cmp_op_overload(op
                )(lhs, rhs)
        if lhs == boolean_array or rhs == boolean_array:
            return bodo.libs.bool_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
            IntegerArrayType):
            return bodo.libs.int_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if isinstance(lhs, FloatingArrayType) or isinstance(rhs,
            FloatingArrayType):
            return bodo.libs.float_arr_ext.create_op_overload(op, 2)(lhs, rhs)
        if binary_array_cmp(lhs, rhs):
            return bodo.libs.binary_arr_ext.create_binary_cmp_op_overload(op)(
                lhs, rhs)
        if cmp_dt_index_to_string(lhs, rhs):
            return bodo.hiframes.pd_index_ext.overload_binop_dti_str(op)(lhs,
                rhs)
        if operand_is_index(lhs) or operand_is_index(rhs):
            return bodo.hiframes.pd_index_ext.create_binary_op_overload(op)(lhs
                , rhs)
        if lhs == datetime_date_type and rhs == datetime_date_type:
            return bodo.hiframes.datetime_date_ext.create_cmp_op_overload(op)(
                lhs, rhs)
        if isinstance(lhs, TimeType) and isinstance(rhs, TimeType):
            return bodo.hiframes.time_ext.create_cmp_op_overload(op)(lhs, rhs)
        if can_cmp_date_datetime(lhs, rhs, op):
            return (bodo.hiframes.datetime_date_ext.
                create_datetime_date_cmp_op_overload(op)(lhs, rhs))
        if lhs == datetime_datetime_type and rhs == datetime_datetime_type:
            return bodo.hiframes.datetime_datetime_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if lhs == datetime_timedelta_type and rhs == datetime_timedelta_type:
            return bodo.hiframes.datetime_timedelta_ext.create_cmp_op_overload(
                op)(lhs, rhs)
        if cmp_timedeltas(lhs, rhs):
            qwikf__zns = (bodo.hiframes.datetime_timedelta_ext.
                pd_create_cmp_op_overload(op))
            return qwikf__zns(lhs, rhs)
        if cmp_timestamp_or_date(lhs, rhs):
            return (bodo.hiframes.pd_timestamp_ext.
                create_timestamp_cmp_op_overload(op)(lhs, rhs))
        if cmp_op_supported_by_numba(lhs, rhs):
            return
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_cmp_operator


def add_dt_td_and_dt_date(lhs, rhs):
    mdcb__zzs = lhs == datetime_timedelta_type and rhs == datetime_date_type
    zlns__shm = rhs == datetime_timedelta_type and lhs == datetime_date_type
    return mdcb__zzs or zlns__shm


def add_timestamp(lhs, rhs):
    sgvvt__jqf = isinstance(lhs, bodo.PandasTimestampType
        ) and is_timedelta_type(rhs)
    wbzxo__hgh = is_timedelta_type(lhs) and isinstance(rhs, bodo.
        PandasTimestampType)
    return sgvvt__jqf or wbzxo__hgh


def add_datetime_and_timedeltas(lhs, rhs):
    robf__oyz = [datetime_timedelta_type, pd_timedelta_type]
    jutg__rpty = [datetime_timedelta_type, pd_timedelta_type,
        datetime_datetime_type]
    zzqc__nrfhl = lhs in robf__oyz and rhs in robf__oyz
    bkkox__zee = (lhs == datetime_datetime_type and rhs in robf__oyz or rhs ==
        datetime_datetime_type and lhs in robf__oyz)
    return zzqc__nrfhl or bkkox__zee


def mul_string_arr_and_int(lhs, rhs):
    gora__lcd = isinstance(lhs, types.Integer) and is_str_arr_type(rhs)
    ztcy__dbgo = is_str_arr_type(lhs) and isinstance(rhs, types.Integer)
    return gora__lcd or ztcy__dbgo


def mul_timedelta_and_int(lhs, rhs):
    mdcb__zzs = lhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(rhs, types.Integer)
    zlns__shm = rhs in [pd_timedelta_type, datetime_timedelta_type
        ] and isinstance(lhs, types.Integer)
    return mdcb__zzs or zlns__shm


def mul_date_offset_and_int(lhs, rhs):
    fldwf__emy = lhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(rhs, types.Integer)
    vfd__xdp = rhs in [week_type, month_end_type, month_begin_type,
        date_offset_type] and isinstance(lhs, types.Integer)
    return fldwf__emy or vfd__xdp


def sub_offset_to_datetime_or_timestamp(lhs, rhs):
    iwfy__qnpd = [datetime_datetime_type, datetime_date_type,
        pd_timestamp_tz_naive_type]
    tz_aware_classes = bodo.PandasTimestampType,
    vafsq__ctli = week_type, month_begin_type, month_end_type
    ene__aypkf = date_offset_type,
    return rhs in vafsq__ctli and isinstance(lhs, tz_aware_classes) or (rhs in
        ene__aypkf or rhs in vafsq__ctli) and lhs in iwfy__qnpd


def sub_dt_index_and_timestamp(lhs, rhs):
    rfa__wyn = isinstance(lhs, DatetimeIndexType
        ) and rhs == pd_timestamp_tz_naive_type
    wqqv__cxn = isinstance(rhs, DatetimeIndexType
        ) and lhs == pd_timestamp_tz_naive_type
    return rfa__wyn or wqqv__cxn


def sub_dt_or_td(lhs, rhs):
    hdvqm__jawhr = lhs == datetime_date_type and rhs == datetime_timedelta_type
    bki__opg = lhs == datetime_date_type and rhs == datetime_date_type
    xbsxt__mgeb = (lhs == datetime_date_array_type and rhs ==
        datetime_timedelta_type)
    return hdvqm__jawhr or bki__opg or xbsxt__mgeb


def sub_datetime_and_timedeltas(lhs, rhs):
    mdft__hyy = (is_timedelta_type(lhs) or lhs == datetime_datetime_type
        ) and is_timedelta_type(rhs)
    puxg__dagc = (lhs == datetime_timedelta_array_type and rhs ==
        datetime_timedelta_type)
    return mdft__hyy or puxg__dagc


def div_timedelta_and_int(lhs, rhs):
    zzqc__nrfhl = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    yfz__ivf = lhs == pd_timedelta_type and isinstance(rhs, types.Integer)
    return zzqc__nrfhl or yfz__ivf


def div_datetime_timedelta(lhs, rhs):
    zzqc__nrfhl = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    yfz__ivf = lhs == datetime_timedelta_type and rhs == types.int64
    return zzqc__nrfhl or yfz__ivf


def mod_timedeltas(lhs, rhs):
    dyapx__fbwe = lhs == pd_timedelta_type and rhs == pd_timedelta_type
    irt__dle = (lhs == datetime_timedelta_type and rhs ==
        datetime_timedelta_type)
    return dyapx__fbwe or irt__dle


def cmp_dt_index_to_string(lhs, rhs):
    rfa__wyn = isinstance(lhs, DatetimeIndexType) and types.unliteral(rhs
        ) == string_type
    wqqv__cxn = isinstance(rhs, DatetimeIndexType) and types.unliteral(lhs
        ) == string_type
    return rfa__wyn or wqqv__cxn


def cmp_timestamp_or_date(lhs, rhs):
    bohnn__ehayi = isinstance(lhs, bodo.hiframes.pd_timestamp_ext.
        PandasTimestampType
        ) and rhs == bodo.hiframes.datetime_date_ext.datetime_date_type
    vrjp__xuwo = (lhs == bodo.hiframes.datetime_date_ext.datetime_date_type and
        isinstance(rhs, bodo.hiframes.pd_timestamp_ext.PandasTimestampType))
    gecf__wva = isinstance(lhs, bodo.hiframes.pd_timestamp_ext.
        PandasTimestampType) and isinstance(rhs, bodo.hiframes.
        pd_timestamp_ext.PandasTimestampType)
    tzoo__tec = lhs == pd_timestamp_tz_naive_type and rhs == bodo.datetime64ns
    ytqo__eddyv = (rhs == pd_timestamp_tz_naive_type and lhs == bodo.
        datetime64ns)
    return bohnn__ehayi or vrjp__xuwo or gecf__wva or tzoo__tec or ytqo__eddyv


def get_series_tz(val):
    if bodo.hiframes.pd_series_ext.is_dt64_series_typ(val):
        if isinstance(val.data, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType
            ):
            znbh__zxk = val.data.tz
        else:
            znbh__zxk = None
    elif isinstance(val, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        znbh__zxk = val.tz
    elif isinstance(val, types.Array) and val.dtype == bodo.datetime64ns:
        znbh__zxk = None
    elif isinstance(val, bodo.PandasTimestampType):
        znbh__zxk = val.tz
    elif val == bodo.datetime64ns:
        znbh__zxk = None
    else:
        return None, False
    return znbh__zxk, True


def is_cmp_tz_mismatch(lhs, rhs):
    hugmn__aqoy, whlua__ene = get_series_tz(lhs)
    tte__ozrg, ezb__ebpf = get_series_tz(rhs)
    return whlua__ene and ezb__ebpf and hugmn__aqoy != tte__ozrg


def cmp_timeseries(lhs, rhs):
    bmmz__wvl = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (bodo
        .utils.typing.is_overload_constant_str(lhs) or lhs == bodo.libs.
        str_ext.string_type)
    vsjzf__zazr = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (bodo
        .utils.typing.is_overload_constant_str(rhs) or rhs == bodo.libs.
        str_ext.string_type)
    tlkk__wium = (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and 
        rhs.dtype == bodo.datetime64ns and lhs == bodo.hiframes.
        pd_timestamp_ext.pd_timestamp_tz_naive_type or bodo.hiframes.
        pd_series_ext.is_dt64_series_typ(lhs) and lhs.dtype == bodo.
        datetime64ns and rhs == bodo.hiframes.pd_timestamp_ext.
        pd_timestamp_tz_naive_type)
    cghh__xhpnv = bmmz__wvl or vsjzf__zazr or tlkk__wium
    sxftd__gatek = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    qyznw__fkuz = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
    rstj__qqbm = sxftd__gatek or qyznw__fkuz
    return cghh__xhpnv or rstj__qqbm


def cmp_timedeltas(lhs, rhs):
    zzqc__nrfhl = [pd_timedelta_type, bodo.timedelta64ns]
    return lhs in zzqc__nrfhl and rhs in zzqc__nrfhl


def operand_is_index(operand):
    return is_index_type(operand) or isinstance(operand, HeterogeneousIndexType
        )


def helper_time_series_checks(operand):
    cpl__rhhqe = bodo.hiframes.pd_series_ext.is_dt64_series_typ(operand
        ) or bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(operand
        ) or operand in [datetime_timedelta_type, datetime_datetime_type,
        pd_timestamp_tz_naive_type]
    return cpl__rhhqe


def binary_array_cmp(lhs, rhs):
    return lhs == binary_array_type and rhs in [bytes_type, binary_array_type
        ] or lhs in [bytes_type, binary_array_type
        ] and rhs == binary_array_type


def can_cmp_date_datetime(lhs, rhs, op):
    return op in (operator.eq, operator.ne) and (lhs == datetime_date_type and
        rhs == datetime_datetime_type or lhs == datetime_datetime_type and 
        rhs == datetime_date_type)


def time_series_operation(lhs, rhs):
    icr__suka = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs
        ) and rhs == datetime_timedelta_type
    lmma__chw = bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs
        ) and lhs == datetime_timedelta_type
    itx__mdjid = bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
        ) and helper_time_series_checks(rhs)
    rqz__jmc = bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
        ) and helper_time_series_checks(lhs)
    return icr__suka or lmma__chw or itx__mdjid or rqz__jmc


def args_td_and_int_array(lhs, rhs):
    bovd__plci = (isinstance(lhs, IntegerArrayType) or isinstance(lhs,
        types.Array) and isinstance(lhs.dtype, types.Integer)) or (isinstance
        (rhs, IntegerArrayType) or isinstance(rhs, types.Array) and
        isinstance(rhs.dtype, types.Integer))
    czbmk__teq = lhs in [pd_timedelta_type] or rhs in [pd_timedelta_type]
    return bovd__plci and czbmk__teq


def arith_op_supported_by_numba(op, lhs, rhs):
    if op == operator.mul:
        zlns__shm = isinstance(lhs, (types.Integer, types.Float)
            ) and isinstance(rhs, types.NPTimedelta)
        mdcb__zzs = isinstance(rhs, (types.Integer, types.Float)
            ) and isinstance(lhs, types.NPTimedelta)
        xmnw__kcfpx = zlns__shm or mdcb__zzs
        xeyhf__gegz = isinstance(rhs, types.UnicodeType) and isinstance(lhs,
            types.Integer)
        wyyk__kmzm = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.Integer)
        igbk__ejv = xeyhf__gegz or wyyk__kmzm
        hrjll__pwdm = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        swk__sde = isinstance(lhs, types.Float) and isinstance(rhs, types.Float
            )
        bsh__qhguj = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        vcxd__xhfd = hrjll__pwdm or swk__sde or bsh__qhguj
        xly__len = isinstance(lhs, types.List) and isinstance(rhs, types.
            Integer) or isinstance(lhs, types.Integer) and isinstance(rhs,
            types.List)
        tys = types.UnicodeCharSeq, types.CharSeq, types.Bytes
        haqcf__zdtn = isinstance(lhs, tys) or isinstance(rhs, tys)
        fgfq__jrd = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        return (xmnw__kcfpx or igbk__ejv or vcxd__xhfd or xly__len or
            haqcf__zdtn or fgfq__jrd)
    if op == operator.pow:
        eedb__khuxj = isinstance(lhs, types.Integer) and isinstance(rhs, (
            types.IntegerLiteral, types.Integer))
        omx__qpih = isinstance(lhs, types.Float) and isinstance(rhs, (types
            .IntegerLiteral, types.Float, types.Integer) or rhs in types.
            unsigned_domain or rhs in types.signed_domain)
        bsh__qhguj = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        fgfq__jrd = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        return eedb__khuxj or omx__qpih or bsh__qhguj or fgfq__jrd
    if op == operator.floordiv:
        swk__sde = lhs in types.real_domain and rhs in types.real_domain
        hrjll__pwdm = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        iqd__fjabj = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        zzqc__nrfhl = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        fgfq__jrd = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        return (swk__sde or hrjll__pwdm or iqd__fjabj or zzqc__nrfhl or
            fgfq__jrd)
    if op == operator.truediv:
        jxcpb__coz = lhs in machine_ints and rhs in machine_ints
        swk__sde = lhs in types.real_domain and rhs in types.real_domain
        bsh__qhguj = (lhs in types.complex_domain and rhs in types.
            complex_domain)
        hrjll__pwdm = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        iqd__fjabj = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        kspj__bgh = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        zzqc__nrfhl = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            (types.Integer, types.Float, types.NPTimedelta))
        fgfq__jrd = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        return (jxcpb__coz or swk__sde or bsh__qhguj or hrjll__pwdm or
            iqd__fjabj or kspj__bgh or zzqc__nrfhl or fgfq__jrd)
    if op == operator.mod:
        jxcpb__coz = lhs in machine_ints and rhs in machine_ints
        swk__sde = lhs in types.real_domain and rhs in types.real_domain
        hrjll__pwdm = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        iqd__fjabj = isinstance(lhs, types.Float) and isinstance(rhs, types
            .Float)
        fgfq__jrd = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        return jxcpb__coz or swk__sde or hrjll__pwdm or iqd__fjabj or fgfq__jrd
    if op == operator.add or op == operator.sub:
        xmnw__kcfpx = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
            types.NPTimedelta)
        xzacf__kwv = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPDatetime)
        ijwkz__rym = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
            types.NPTimedelta)
        uqm__grgr = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
        hrjll__pwdm = isinstance(lhs, types.Integer) and isinstance(rhs,
            types.Integer)
        swk__sde = isinstance(lhs, types.Float) and isinstance(rhs, types.Float
            )
        bsh__qhguj = isinstance(lhs, types.Complex) and isinstance(rhs,
            types.Complex)
        vcxd__xhfd = hrjll__pwdm or swk__sde or bsh__qhguj
        fgfq__jrd = isinstance(lhs, types.Array) or isinstance(rhs, types.Array
            )
        yazr__blnm = isinstance(lhs, types.BaseTuple) and isinstance(rhs,
            types.BaseTuple)
        xly__len = isinstance(lhs, types.List) and isinstance(rhs, types.List)
        lcyi__ecpjp = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeType)
        dfjvp__ziv = isinstance(rhs, types.UnicodeCharSeq) and isinstance(lhs,
            types.UnicodeType)
        ipssm__xge = isinstance(lhs, types.UnicodeCharSeq) and isinstance(rhs,
            types.UnicodeCharSeq)
        frxx__pzc = isinstance(lhs, (types.CharSeq, types.Bytes)
            ) and isinstance(rhs, (types.CharSeq, types.Bytes))
        shl__zqc = lcyi__ecpjp or dfjvp__ziv or ipssm__xge or frxx__pzc
        igbk__ejv = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeType)
        kkyco__wttn = isinstance(lhs, types.UnicodeType) and isinstance(rhs,
            types.UnicodeCharSeq)
        trj__doa = igbk__ejv or kkyco__wttn
        qpbj__ucnjk = lhs == types.NPTimedelta and rhs == types.NPDatetime
        ynzmq__zuhyr = (yazr__blnm or xly__len or shl__zqc or trj__doa or
            qpbj__ucnjk)
        kfp__qox = op == operator.add and ynzmq__zuhyr
        return (xmnw__kcfpx or xzacf__kwv or ijwkz__rym or uqm__grgr or
            vcxd__xhfd or fgfq__jrd or kfp__qox)


def cmp_op_supported_by_numba(lhs, rhs):
    fgfq__jrd = isinstance(lhs, types.Array) or isinstance(rhs, types.Array)
    xly__len = isinstance(lhs, types.ListType) and isinstance(rhs, types.
        ListType)
    xmnw__kcfpx = isinstance(lhs, types.NPTimedelta) and isinstance(rhs,
        types.NPTimedelta)
    jqmj__bmjo = isinstance(lhs, types.NPDatetime) and isinstance(rhs,
        types.NPDatetime)
    unicode_types = (types.UnicodeType, types.StringLiteral, types.CharSeq,
        types.Bytes, types.UnicodeCharSeq)
    igbk__ejv = isinstance(lhs, unicode_types) and isinstance(rhs,
        unicode_types)
    yazr__blnm = isinstance(lhs, types.BaseTuple) and isinstance(rhs, types
        .BaseTuple)
    uqm__grgr = isinstance(lhs, types.Set) and isinstance(rhs, types.Set)
    vcxd__xhfd = isinstance(lhs, types.Number) and isinstance(rhs, types.Number
        )
    cjgqj__ruye = isinstance(lhs, types.Boolean) and isinstance(rhs, types.
        Boolean)
    lat__whleq = isinstance(lhs, types.NoneType) or isinstance(rhs, types.
        NoneType)
    vjon__iafsq = isinstance(lhs, types.DictType) and isinstance(rhs, types
        .DictType)
    cyu__ctzv = isinstance(lhs, types.EnumMember) and isinstance(rhs, types
        .EnumMember)
    ate__wkuye = isinstance(lhs, types.Literal) and isinstance(rhs, types.
        Literal)
    return (xly__len or xmnw__kcfpx or jqmj__bmjo or igbk__ejv or
        yazr__blnm or uqm__grgr or vcxd__xhfd or cjgqj__ruye or lat__whleq or
        vjon__iafsq or fgfq__jrd or cyu__ctzv or ate__wkuye)


def raise_error_if_not_numba_supported(op, lhs, rhs):
    if arith_op_supported_by_numba(op, lhs, rhs):
        return
    raise BodoError(
        f'{op} operator not supported for data types {lhs} and {rhs}.')


def _install_series_and_or():
    for op in (operator.or_, operator.and_):
        infer_global(op)(SeriesAndOrTyper)
        lower_impl = lower_series_and_or(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)


_install_series_and_or()


def _install_cmp_ops():
    for op in (operator.lt, operator.eq, operator.ne, operator.ge, operator
        .gt, operator.le):
        infer_global(op)(SeriesCmpOpTemplate)
        lower_impl = series_cmp_op_lower(op)
        lower_builtin(op, SeriesType, SeriesType)(lower_impl)
        lower_builtin(op, SeriesType, types.Any)(lower_impl)
        lower_builtin(op, types.Any, SeriesType)(lower_impl)
        hntv__wtjzf = create_overload_cmp_operator(op)
        overload(op, no_unliteral=True)(hntv__wtjzf)


_install_cmp_ops()


def install_arith_ops():
    for op in (operator.add, operator.sub, operator.mul, operator.truediv,
        operator.floordiv, operator.mod, operator.pow):
        hntv__wtjzf = create_overload_arith_op(op)
        overload(op, no_unliteral=True)(hntv__wtjzf)


install_arith_ops()
