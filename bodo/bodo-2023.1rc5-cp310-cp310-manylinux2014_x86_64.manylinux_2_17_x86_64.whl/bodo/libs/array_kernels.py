"""
Implements array kernels such as median and quantile.
"""
import hashlib
import inspect
import math
import operator
import re
import warnings
from math import sqrt
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types, typing
from numba.core.imputils import lower_builtin
from numba.core.ir_utils import find_const, guard
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import overload, overload_attribute, register_jitable
from numba.np.arrayobj import make_array
from numba.np.numpy_support import as_dtype
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, init_categorical_array
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.hiframes.time_ext import TimeArrayType
from bodo.libs import quantile_alg
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, drop_duplicates_local_dictionary, drop_duplicates_table, info_from_table, info_to_array, sample_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, offset_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import DictionaryArrayType, init_dict_arr
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType, alloc_int_array
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import pre_alloc_string_array, str_arr_set_na, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, check_unsupported_args, decode_if_dict_array, element_type, find_common_np_dtype, get_overload_const_bool, get_overload_const_list, get_overload_const_str, is_bin_arr_type, is_overload_constant_bool, is_overload_constant_str, is_overload_none, is_overload_true, is_str_arr_type, raise_bodo_error, to_str_arr_if_dict_array
from bodo.utils.utils import build_set_seen_na, check_and_propagate_cpp_exception, numba_to_c_type, unliteral_all
ll.add_symbol('quantile_sequential', quantile_alg.quantile_sequential)
ll.add_symbol('quantile_parallel', quantile_alg.quantile_parallel)
MPI_ROOT = 0
sum_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value)
max_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Max.value)
min_op = np.int32(bodo.libs.distributed_api.Reduce_Type.Min.value)


def isna(arr, i):
    return False


@overload(isna)
def overload_isna(arr, i):
    i = types.unliteral(i)
    if arr == string_array_type:
        return lambda arr, i: bodo.libs.str_arr_ext.str_arr_is_na(arr, i)
    if isinstance(arr, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, TimeArrayType)) or arr in (boolean_array,
        datetime_date_array_type, datetime_timedelta_array_type,
        string_array_split_view_type):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
            ._null_bitmap, i)
    if isinstance(arr, ArrayItemArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, bodo.libs.map_arr_ext.MapArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr._data), i)
    if isinstance(arr, StructArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.struct_arr_ext.get_null_bitmap(arr), i)
    if isinstance(arr, TupleArrayType):
        return lambda arr, i: bodo.libs.array_kernels.isna(arr._data, i)
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return lambda arr, i: arr.codes[i] == -1
    if arr == bodo.binary_array_type:
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(bodo
            .libs.array_item_arr_ext.get_null_bitmap(arr._data), i)
    if isinstance(arr, types.List):
        if arr.dtype == types.none:
            return lambda arr, i: True
        elif isinstance(arr.dtype, types.optional):
            return lambda arr, i: arr[i] is None
        else:
            return lambda arr, i: False
    if isinstance(arr, bodo.NullableTupleType):
        return lambda arr, i: arr._null_values[i]
    if isinstance(arr, DictionaryArrayType):
        return lambda arr, i: not bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr
            ._indices._null_bitmap, i) or bodo.libs.array_kernels.isna(arr.
            _data, arr._indices[i])
    if isinstance(arr, DatetimeArrayType):
        return lambda arr, i: np.isnat(arr._data[i])
    assert isinstance(arr, types.Array), f'Invalid array type in isna(): {arr}'
    dtype = arr.dtype
    if isinstance(dtype, types.Float):
        return lambda arr, i: np.isnan(arr[i])
    if isinstance(dtype, (types.NPDatetime, types.NPTimedelta)):
        return lambda arr, i: np.isnat(arr[i])
    return lambda arr, i: False


def setna(arr, ind, int_nan_const=0):
    arr[ind] = np.nan


@overload(setna, no_unliteral=True)
def setna_overload(arr, ind, int_nan_const=0):
    if isinstance(arr, types.Array) and isinstance(arr.dtype, types.Float):
        return setna
    if isinstance(arr.dtype, (types.NPDatetime, types.NPTimedelta)):
        sev__suja = arr.dtype('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr[ind] = sev__suja
        return _setnan_impl
    if isinstance(arr, DatetimeArrayType):
        sev__suja = bodo.datetime64ns('NaT')

        def _setnan_impl(arr, ind, int_nan_const=0):
            arr._data[ind] = sev__suja
        return _setnan_impl
    if arr == string_array_type:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = ''
            str_arr_set_na(arr, ind)
        return impl
    if isinstance(arr, DictionaryArrayType):
        return lambda arr, ind, int_nan_const=0: bodo.libs.array_kernels.setna(
            arr._indices, ind)
    if arr == boolean_array:

        def impl(arr, ind, int_nan_const=0):
            arr[ind] = False
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ):
        return (lambda arr, ind, int_nan_const=0: bodo.libs.int_arr_ext.
            set_bit_to_arr(arr._null_bitmap, ind, 0))
    if arr == bodo.binary_array_type:

        def impl_binary_arr(arr, ind, int_nan_const=0):
            tafit__enduj = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            tafit__enduj[ind + 1] = tafit__enduj[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_binary_arr
    if isinstance(arr, bodo.libs.array_item_arr_ext.ArrayItemArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            tafit__enduj = bodo.libs.array_item_arr_ext.get_offsets(arr)
            tafit__enduj[ind + 1] = tafit__enduj[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr), ind, 0)
        return impl_arr_item
    if isinstance(arr, bodo.libs.map_arr_ext.MapArrayType):

        def impl_arr_item(arr, ind, int_nan_const=0):
            tafit__enduj = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            tafit__enduj[ind + 1] = tafit__enduj[ind]
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.
                array_item_arr_ext.get_null_bitmap(arr._data), ind, 0)
        return impl_arr_item
    if isinstance(arr, bodo.libs.struct_arr_ext.StructArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.int_arr_ext.set_bit_to_arr(bodo.libs.struct_arr_ext.
                get_null_bitmap(arr), ind, 0)
            data = bodo.libs.struct_arr_ext.get_data(arr)
            setna_tup(data, ind)
        return impl
    if isinstance(arr, TupleArrayType):

        def impl(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._data, ind)
        return impl
    if arr.dtype == types.bool_:

        def b_set(arr, ind, int_nan_const=0):
            arr[ind] = False
        return b_set
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):

        def setna_cat(arr, ind, int_nan_const=0):
            arr.codes[ind] = -1
        return setna_cat
    if isinstance(arr.dtype, types.Integer):

        def setna_int(arr, ind, int_nan_const=0):
            arr[ind] = int_nan_const
        return setna_int
    if arr == datetime_date_array_type:

        def setna_datetime_date(arr, ind, int_nan_const=0):
            arr._data[ind] = (1970 << 32) + (1 << 16) + 1
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_date
    if isinstance(arr, bodo.TimeArrayType):

        def setna_time(arr, ind, int_nan_const=0):
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_time
    if arr == datetime_timedelta_array_type:

        def setna_datetime_timedelta(arr, ind, int_nan_const=0):
            bodo.libs.array_kernels.setna(arr._days_data, ind)
            bodo.libs.array_kernels.setna(arr._seconds_data, ind)
            bodo.libs.array_kernels.setna(arr._microseconds_data, ind)
            bodo.libs.int_arr_ext.set_bit_to_arr(arr._null_bitmap, ind, 0)
        return setna_datetime_timedelta
    return lambda arr, ind, int_nan_const=0: None


def copy_array_element(out_arr, out_ind, in_arr, in_ind):
    pass


@overload(copy_array_element)
def overload_copy_array_element(out_arr, out_ind, in_arr, in_ind):
    if out_arr == bodo.string_array_type and is_str_arr_type(in_arr):

        def impl_str(out_arr, out_ind, in_arr, in_ind):
            if bodo.libs.array_kernels.isna(in_arr, in_ind):
                bodo.libs.array_kernels.setna(out_arr, out_ind)
            else:
                bodo.libs.str_arr_ext.get_str_arr_item_copy(out_arr,
                    out_ind, in_arr, in_ind)
        return impl_str
    if isinstance(out_arr, DatetimeArrayType) and isinstance(in_arr,
        DatetimeArrayType) and out_arr.tz == in_arr.tz:

        def impl_dt(out_arr, out_ind, in_arr, in_ind):
            if bodo.libs.array_kernels.isna(in_arr, in_ind):
                bodo.libs.array_kernels.setna(out_arr, out_ind)
            else:
                out_arr._data[out_ind] = in_arr._data[in_ind]
        return impl_dt

    def impl(out_arr, out_ind, in_arr, in_ind):
        if bodo.libs.array_kernels.isna(in_arr, in_ind):
            bodo.libs.array_kernels.setna(out_arr, out_ind)
        else:
            out_arr[out_ind] = in_arr[in_ind]
    return impl


def setna_tup(arr_tup, ind, int_nan_const=0):
    pass


@overload(setna_tup, no_unliteral=True)
def overload_setna_tup(arr_tup, ind, int_nan_const=0):
    jpg__nplhk = arr_tup.count
    wbp__gsvz = 'def f(arr_tup, ind, int_nan_const=0):\n'
    for i in range(jpg__nplhk):
        wbp__gsvz += '  setna(arr_tup[{}], ind, int_nan_const)\n'.format(i)
    wbp__gsvz += '  return\n'
    nxpc__izwqb = {}
    exec(wbp__gsvz, {'setna': setna}, nxpc__izwqb)
    impl = nxpc__izwqb['f']
    return impl


def setna_slice(arr, s):
    arr[s] = np.nan


@overload(setna_slice, no_unliteral=True)
def overload_setna_slice(arr, s):

    def impl(arr, s):
        lij__wdre = numba.cpython.unicode._normalize_slice(s, len(arr))
        for i in range(lij__wdre.start, lij__wdre.stop, lij__wdre.step):
            setna(arr, i)
    return impl


@numba.generated_jit
def first_last_valid_index(arr, index_arr, is_first=True, parallel=False):
    is_first = get_overload_const_bool(is_first)
    if is_first:
        eeug__vlzm = 'n'
        xtq__mup = 'n_pes'
        stlgy__essts = 'min_op'
    else:
        eeug__vlzm = 'n-1, -1, -1'
        xtq__mup = '-1'
        stlgy__essts = 'max_op'
    wbp__gsvz = f"""def impl(arr, index_arr, is_first=True, parallel=False):
    n = len(arr)
    index_value = index_arr[0]
    has_valid = False
    loc_valid_rank = -1
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        loc_valid_rank = {xtq__mup}
    for i in range({eeug__vlzm}):
        if not isna(arr, i):
            if parallel:
                loc_valid_rank = rank
            index_value = index_arr[i]
            has_valid = True
            break
    if parallel:
        possible_valid_rank = np.int32(bodo.libs.distributed_api.dist_reduce(loc_valid_rank, {stlgy__essts}))
        if possible_valid_rank != {xtq__mup}:
            has_valid = True
            index_value = bodo.libs.distributed_api.bcast_scalar(index_value, possible_valid_rank)
    return has_valid, box_if_dt64(index_value)

    """
    nxpc__izwqb = {}
    exec(wbp__gsvz, {'np': np, 'bodo': bodo, 'isna': isna, 'max_op': max_op,
        'min_op': min_op, 'box_if_dt64': bodo.utils.conversion.box_if_dt64},
        nxpc__izwqb)
    impl = nxpc__izwqb['impl']
    return impl


ll.add_symbol('median_series_computation', quantile_alg.
    median_series_computation)
_median_series_computation = types.ExternalFunction('median_series_computation'
    , types.void(types.voidptr, bodo.libs.array.array_info_type, types.
    bool_, types.bool_))


@numba.njit
def median_series_computation(res, arr, is_parallel, skipna):
    yheyu__pkk = array_to_info(arr)
    _median_series_computation(res, yheyu__pkk, is_parallel, skipna)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(yheyu__pkk)


ll.add_symbol('autocorr_series_computation', quantile_alg.
    autocorr_series_computation)
_autocorr_series_computation = types.ExternalFunction(
    'autocorr_series_computation', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def autocorr_series_computation(res, arr, lag, is_parallel):
    yheyu__pkk = array_to_info(arr)
    _autocorr_series_computation(res, yheyu__pkk, lag, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(yheyu__pkk)


@numba.njit
def autocorr(arr, lag=1, parallel=False):
    res = np.empty(1, types.float64)
    autocorr_series_computation(res.ctypes, arr, lag, parallel)
    return res[0]


ll.add_symbol('compute_series_monotonicity', quantile_alg.
    compute_series_monotonicity)
_compute_series_monotonicity = types.ExternalFunction(
    'compute_series_monotonicity', types.void(types.voidptr, bodo.libs.
    array.array_info_type, types.int64, types.bool_))


@numba.njit
def series_monotonicity_call(res, arr, inc_dec, is_parallel):
    yheyu__pkk = array_to_info(arr)
    _compute_series_monotonicity(res, yheyu__pkk, inc_dec, is_parallel)
    check_and_propagate_cpp_exception()
    delete_info_decref_array(yheyu__pkk)


@numba.njit
def series_monotonicity(arr, inc_dec, parallel=False):
    res = np.empty(1, types.float64)
    series_monotonicity_call(res.ctypes, arr, inc_dec, parallel)
    csnoq__jqv = res[0] > 0.5
    return csnoq__jqv


@numba.generated_jit(nopython=True)
def get_valid_entries_from_date_offset(index_arr, offset, initial_date,
    is_last, is_parallel=False):
    if get_overload_const_bool(is_last):
        txjy__tpfdw = '-'
        ddgm__tazyc = 'index_arr[0] > threshhold_date'
        eeug__vlzm = '1, n+1'
        yvc__qrnp = 'index_arr[-i] <= threshhold_date'
        jck__vor = 'i - 1'
    else:
        txjy__tpfdw = '+'
        ddgm__tazyc = 'index_arr[-1] < threshhold_date'
        eeug__vlzm = 'n'
        yvc__qrnp = 'index_arr[i] >= threshhold_date'
        jck__vor = 'i'
    wbp__gsvz = (
        'def impl(index_arr, offset, initial_date, is_last, is_parallel=False):\n'
        )
    if types.unliteral(offset) == types.unicode_type:
        wbp__gsvz += (
            '  with numba.objmode(threshhold_date=bodo.pd_timestamp_tz_naive_type):\n'
            )
        wbp__gsvz += (
            '    date_offset = pd.tseries.frequencies.to_offset(offset)\n')
        if not get_overload_const_bool(is_last):
            wbp__gsvz += """    if not isinstance(date_offset, pd._libs.tslibs.Tick) and date_offset.is_on_offset(index_arr[0]):
"""
            wbp__gsvz += (
                '      threshhold_date = initial_date - date_offset.base + date_offset\n'
                )
            wbp__gsvz += '    else:\n'
            wbp__gsvz += '      threshhold_date = initial_date + date_offset\n'
        else:
            wbp__gsvz += (
                f'    threshhold_date = initial_date {txjy__tpfdw} date_offset\n'
                )
    else:
        wbp__gsvz += f'  threshhold_date = initial_date {txjy__tpfdw} offset\n'
    wbp__gsvz += '  local_valid = 0\n'
    wbp__gsvz += f'  n = len(index_arr)\n'
    wbp__gsvz += f'  if n:\n'
    wbp__gsvz += f'    if {ddgm__tazyc}:\n'
    wbp__gsvz += '      loc_valid = n\n'
    wbp__gsvz += '    else:\n'
    wbp__gsvz += f'      for i in range({eeug__vlzm}):\n'
    wbp__gsvz += f'        if {yvc__qrnp}:\n'
    wbp__gsvz += f'          loc_valid = {jck__vor}\n'
    wbp__gsvz += '          break\n'
    wbp__gsvz += '  if is_parallel:\n'
    wbp__gsvz += (
        '    total_valid = bodo.libs.distributed_api.dist_reduce(loc_valid, sum_op)\n'
        )
    wbp__gsvz += '    return total_valid\n'
    wbp__gsvz += '  else:\n'
    wbp__gsvz += '    return loc_valid\n'
    nxpc__izwqb = {}
    exec(wbp__gsvz, {'bodo': bodo, 'pd': pd, 'numba': numba, 'sum_op':
        sum_op}, nxpc__izwqb)
    return nxpc__izwqb['impl']


def quantile(A, q):
    pass


def quantile_parallel(A, q):
    pass


@infer_global(quantile)
@infer_global(quantile_parallel)
class QuantileType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) in [2, 3]
        return signature(types.float64, *unliteral_all(args))


@lower_builtin(quantile, types.Array, types.float64)
@lower_builtin(quantile, IntegerArrayType, types.float64)
@lower_builtin(quantile, FloatingArrayType, types.float64)
@lower_builtin(quantile, BooleanArrayType, types.float64)
def lower_dist_quantile_seq(context, builder, sig, args):
    tbaw__oigv = numba_to_c_type(sig.args[0].dtype)
    drzz__nthpm = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), tbaw__oigv))
    dbna__xaczc = args[0]
    mjsii__ghoh = sig.args[0]
    if isinstance(mjsii__ghoh, (IntegerArrayType, FloatingArrayType,
        BooleanArrayType)):
        dbna__xaczc = cgutils.create_struct_proxy(mjsii__ghoh)(context,
            builder, dbna__xaczc).data
        mjsii__ghoh = types.Array(mjsii__ghoh.dtype, 1, 'C')
    assert mjsii__ghoh.ndim == 1
    arr = make_array(mjsii__ghoh)(context, builder, dbna__xaczc)
    hwi__xqz = builder.extract_value(arr.shape, 0)
    xnxz__qrapg = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        hwi__xqz, args[1], builder.load(drzz__nthpm)]
    pdbyu__smqo = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        DoubleType(), lir.IntType(32)]
    jts__lkdtp = lir.FunctionType(lir.DoubleType(), pdbyu__smqo)
    uveqc__bxeu = cgutils.get_or_insert_function(builder.module, jts__lkdtp,
        name='quantile_sequential')
    rxfq__zdab = builder.call(uveqc__bxeu, xnxz__qrapg)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return rxfq__zdab


@lower_builtin(quantile_parallel, types.Array, types.float64, types.intp)
@lower_builtin(quantile_parallel, IntegerArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, FloatingArrayType, types.float64, types.intp)
@lower_builtin(quantile_parallel, BooleanArrayType, types.float64, types.intp)
def lower_dist_quantile_parallel(context, builder, sig, args):
    tbaw__oigv = numba_to_c_type(sig.args[0].dtype)
    drzz__nthpm = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(32), tbaw__oigv))
    dbna__xaczc = args[0]
    mjsii__ghoh = sig.args[0]
    if isinstance(mjsii__ghoh, (IntegerArrayType, FloatingArrayType,
        BooleanArrayType)):
        dbna__xaczc = cgutils.create_struct_proxy(mjsii__ghoh)(context,
            builder, dbna__xaczc).data
        mjsii__ghoh = types.Array(mjsii__ghoh.dtype, 1, 'C')
    assert mjsii__ghoh.ndim == 1
    arr = make_array(mjsii__ghoh)(context, builder, dbna__xaczc)
    hwi__xqz = builder.extract_value(arr.shape, 0)
    if len(args) == 3:
        buboq__ckiy = args[2]
    else:
        buboq__ckiy = hwi__xqz
    xnxz__qrapg = [builder.bitcast(arr.data, lir.IntType(8).as_pointer()),
        hwi__xqz, buboq__ckiy, args[1], builder.load(drzz__nthpm)]
    pdbyu__smqo = [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
        IntType(64), lir.DoubleType(), lir.IntType(32)]
    jts__lkdtp = lir.FunctionType(lir.DoubleType(), pdbyu__smqo)
    uveqc__bxeu = cgutils.get_or_insert_function(builder.module, jts__lkdtp,
        name='quantile_parallel')
    rxfq__zdab = builder.call(uveqc__bxeu, xnxz__qrapg)
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return rxfq__zdab


@numba.generated_jit(nopython=True)
def _rank_detect_ties(arr):

    def impl(arr):
        n = len(arr)
        shl__mmsmp = bodo.utils.utils.alloc_type(n, np.bool_, (-1,))
        shl__mmsmp[0] = True
        yhefj__jwmtw = pd.isna(arr)
        for i in range(1, len(arr)):
            if yhefj__jwmtw[i] and yhefj__jwmtw[i - 1]:
                shl__mmsmp[i] = False
            elif yhefj__jwmtw[i] or yhefj__jwmtw[i - 1]:
                shl__mmsmp[i] = True
            else:
                shl__mmsmp[i] = arr[i] != arr[i - 1]
        return shl__mmsmp
    return impl


def rank(arr, method='average', na_option='keep', ascending=True, pct=False):
    pass


@overload(rank, no_unliteral=True, inline='always')
def overload_rank(arr, method='average', na_option='keep', ascending=True,
    pct=False):
    if not is_overload_constant_str(method):
        raise_bodo_error(
            "Series.rank(): 'method' argument must be a constant string")
    method = get_overload_const_str(method)
    if not is_overload_constant_str(na_option):
        raise_bodo_error(
            "Series.rank(): 'na_option' argument must be a constant string")
    na_option = get_overload_const_str(na_option)
    if not is_overload_constant_bool(ascending):
        raise_bodo_error(
            "Series.rank(): 'ascending' argument must be a constant boolean")
    ascending = get_overload_const_bool(ascending)
    if not is_overload_constant_bool(pct):
        raise_bodo_error(
            "Series.rank(): 'pct' argument must be a constant boolean")
    pct = get_overload_const_bool(pct)
    if method == 'first' and not ascending:
        raise BodoError(
            "Series.rank(): method='first' with ascending=False is currently unsupported."
            )
    wbp__gsvz = (
        "def impl(arr, method='average', na_option='keep', ascending=True, pct=False):\n"
        )
    wbp__gsvz += '  na_idxs = pd.isna(arr)\n'
    wbp__gsvz += '  sorter = bodo.hiframes.series_impl.argsort(arr)\n'
    wbp__gsvz += '  nas = sum(na_idxs)\n'
    if not ascending:
        wbp__gsvz += '  if nas and nas < (sorter.size - 1):\n'
        wbp__gsvz += '    sorter[:-nas] = sorter[-(nas + 1)::-1]\n'
        wbp__gsvz += '  else:\n'
        wbp__gsvz += '    sorter = sorter[::-1]\n'
    if na_option == 'top':
        wbp__gsvz += (
            '  sorter = np.concatenate((sorter[-nas:], sorter[:-nas]))\n')
    wbp__gsvz += '  inv = np.empty(sorter.size, dtype=np.intp)\n'
    wbp__gsvz += '  inv[sorter] = np.arange(sorter.size)\n'
    if method == 'first':
        wbp__gsvz += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
        wbp__gsvz += '    inv,\n'
        wbp__gsvz += '    new_dtype=np.float64,\n'
        wbp__gsvz += '    copy=True,\n'
        wbp__gsvz += '    nan_to_str=False,\n'
        wbp__gsvz += '    from_series=True,\n'
        wbp__gsvz += '    ) + 1\n'
    else:
        wbp__gsvz += '  arr = arr[sorter]\n'
        wbp__gsvz += '  obs = bodo.libs.array_kernels._rank_detect_ties(arr)\n'
        wbp__gsvz += '  dense = obs.cumsum()[inv]\n'
        if method == 'dense':
            wbp__gsvz += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            wbp__gsvz += '    dense,\n'
            wbp__gsvz += '    new_dtype=np.float64,\n'
            wbp__gsvz += '    copy=True,\n'
            wbp__gsvz += '    nan_to_str=False,\n'
            wbp__gsvz += '    from_series=True,\n'
            wbp__gsvz += '  )\n'
        else:
            wbp__gsvz += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            wbp__gsvz += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                wbp__gsvz += '  ret = count_float[dense]\n'
            elif method == 'min':
                wbp__gsvz += '  ret = count_float[dense - 1] + 1\n'
            else:
                wbp__gsvz += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            if na_option == 'keep':
                wbp__gsvz += '  ret[na_idxs] = -1\n'
            wbp__gsvz += '  div_val = np.max(ret)\n'
        elif na_option == 'keep':
            wbp__gsvz += '  div_val = arr.size - nas\n'
        else:
            wbp__gsvz += '  div_val = arr.size\n'
        wbp__gsvz += '  for i in range(len(ret)):\n'
        wbp__gsvz += '    ret[i] = ret[i] / div_val\n'
    if na_option == 'keep':
        wbp__gsvz += '  ret[na_idxs] = np.nan\n'
    wbp__gsvz += '  return ret\n'
    nxpc__izwqb = {}
    exec(wbp__gsvz, {'np': np, 'pd': pd, 'bodo': bodo}, nxpc__izwqb)
    return nxpc__izwqb['impl']


@numba.njit
def min_heapify(arr, ind_arr, n, start, cmp_f):
    nugy__bhqs = start
    cht__gkky = 2 * start + 1
    iep__lrnvt = 2 * start + 2
    if cht__gkky < n and not cmp_f(arr[cht__gkky], arr[nugy__bhqs]):
        nugy__bhqs = cht__gkky
    if iep__lrnvt < n and not cmp_f(arr[iep__lrnvt], arr[nugy__bhqs]):
        nugy__bhqs = iep__lrnvt
    if nugy__bhqs != start:
        arr[start], arr[nugy__bhqs] = arr[nugy__bhqs], arr[start]
        ind_arr[start], ind_arr[nugy__bhqs] = ind_arr[nugy__bhqs], ind_arr[
            start]
        min_heapify(arr, ind_arr, n, nugy__bhqs, cmp_f)


def select_k_nonan(A, index_arr, m, k):
    return A[:k]


@overload(select_k_nonan, no_unliteral=True)
def select_k_nonan_overload(A, index_arr, m, k):
    dtype = A.dtype
    if isinstance(dtype, types.Integer):
        return lambda A, index_arr, m, k: (A[:k].copy(), index_arr[:k].copy
            (), k)

    def select_k_nonan_float(A, index_arr, m, k):
        xsath__scog = np.empty(k, A.dtype)
        wpe__ohbuv = np.empty(k, index_arr.dtype)
        i = 0
        ind = 0
        while i < m and ind < k:
            if not bodo.libs.array_kernels.isna(A, i):
                xsath__scog[ind] = A[i]
                wpe__ohbuv[ind] = index_arr[i]
                ind += 1
            i += 1
        if ind < k:
            xsath__scog = xsath__scog[:ind]
            wpe__ohbuv = wpe__ohbuv[:ind]
        return xsath__scog, wpe__ohbuv, i
    return select_k_nonan_float


@numba.njit
def nlargest(A, index_arr, k, is_largest, cmp_f):
    A = bodo.utils.conversion.coerce_to_ndarray(A)
    m = len(A)
    if k == 0:
        return A[:0], index_arr[:0]
    if k >= m:
        xavqm__yosu = np.sort(A)
        jkf__hlz = index_arr[np.argsort(A)]
        xfk__fppyd = pd.Series(xavqm__yosu).notna().values
        xavqm__yosu = xavqm__yosu[xfk__fppyd]
        jkf__hlz = jkf__hlz[xfk__fppyd]
        if is_largest:
            xavqm__yosu = xavqm__yosu[::-1]
            jkf__hlz = jkf__hlz[::-1]
        return np.ascontiguousarray(xavqm__yosu), np.ascontiguousarray(jkf__hlz
            )
    xsath__scog, wpe__ohbuv, start = select_k_nonan(A, index_arr, m, k)
    wpe__ohbuv = wpe__ohbuv[xsath__scog.argsort()]
    xsath__scog.sort()
    if not is_largest:
        xsath__scog = np.ascontiguousarray(xsath__scog[::-1])
        wpe__ohbuv = np.ascontiguousarray(wpe__ohbuv[::-1])
    for i in range(start, m):
        if cmp_f(A[i], xsath__scog[0]):
            xsath__scog[0] = A[i]
            wpe__ohbuv[0] = index_arr[i]
            min_heapify(xsath__scog, wpe__ohbuv, k, 0, cmp_f)
    wpe__ohbuv = wpe__ohbuv[xsath__scog.argsort()]
    xsath__scog.sort()
    if is_largest:
        xsath__scog = xsath__scog[::-1]
        wpe__ohbuv = wpe__ohbuv[::-1]
    return np.ascontiguousarray(xsath__scog), np.ascontiguousarray(wpe__ohbuv)


@numba.njit
def nlargest_parallel(A, I, k, is_largest, cmp_f):
    xrky__lnt = bodo.libs.distributed_api.get_rank()
    A = bodo.utils.conversion.coerce_to_ndarray(A)
    rpc__lbz, qmxem__vsk = nlargest(A, I, k, is_largest, cmp_f)
    hnj__yrpgm = bodo.libs.distributed_api.gatherv(rpc__lbz)
    gfhcq__ndvjf = bodo.libs.distributed_api.gatherv(qmxem__vsk)
    if xrky__lnt == MPI_ROOT:
        res, ckyv__fvl = nlargest(hnj__yrpgm, gfhcq__ndvjf, k, is_largest,
            cmp_f)
    else:
        res = np.empty(k, A.dtype)
        ckyv__fvl = np.empty(k, I.dtype)
    bodo.libs.distributed_api.bcast(res)
    bodo.libs.distributed_api.bcast(ckyv__fvl)
    return res, ckyv__fvl


@numba.njit(no_cpython_wrapper=True, cache=True)
def nancorr(mat, cov=0, minpv=1, parallel=False):
    pstfb__zuav, awab__mxowf = mat.shape
    ymwta__lomk = np.empty((awab__mxowf, awab__mxowf), dtype=np.float64)
    for ccdt__htbfp in range(awab__mxowf):
        for lfnm__vwi in range(ccdt__htbfp + 1):
            azde__aui = 0
            qzio__xko = gzu__phy = dptjz__dxqw = bhkv__duw = 0.0
            for i in range(pstfb__zuav):
                if np.isfinite(mat[i, ccdt__htbfp]) and np.isfinite(mat[i,
                    lfnm__vwi]):
                    jzcu__gks = mat[i, ccdt__htbfp]
                    lbbm__gkwu = mat[i, lfnm__vwi]
                    azde__aui += 1
                    dptjz__dxqw += jzcu__gks
                    bhkv__duw += lbbm__gkwu
            if parallel:
                azde__aui = bodo.libs.distributed_api.dist_reduce(azde__aui,
                    sum_op)
                dptjz__dxqw = bodo.libs.distributed_api.dist_reduce(dptjz__dxqw
                    , sum_op)
                bhkv__duw = bodo.libs.distributed_api.dist_reduce(bhkv__duw,
                    sum_op)
            if azde__aui < minpv:
                ymwta__lomk[ccdt__htbfp, lfnm__vwi] = ymwta__lomk[lfnm__vwi,
                    ccdt__htbfp] = np.nan
            else:
                dwe__het = dptjz__dxqw / azde__aui
                fgcyq__xnrn = bhkv__duw / azde__aui
                dptjz__dxqw = 0.0
                for i in range(pstfb__zuav):
                    if np.isfinite(mat[i, ccdt__htbfp]) and np.isfinite(mat
                        [i, lfnm__vwi]):
                        jzcu__gks = mat[i, ccdt__htbfp] - dwe__het
                        lbbm__gkwu = mat[i, lfnm__vwi] - fgcyq__xnrn
                        dptjz__dxqw += jzcu__gks * lbbm__gkwu
                        qzio__xko += jzcu__gks * jzcu__gks
                        gzu__phy += lbbm__gkwu * lbbm__gkwu
                if parallel:
                    dptjz__dxqw = bodo.libs.distributed_api.dist_reduce(
                        dptjz__dxqw, sum_op)
                    qzio__xko = bodo.libs.distributed_api.dist_reduce(qzio__xko
                        , sum_op)
                    gzu__phy = bodo.libs.distributed_api.dist_reduce(gzu__phy,
                        sum_op)
                eign__fnwg = azde__aui - 1.0 if cov else sqrt(qzio__xko *
                    gzu__phy)
                if eign__fnwg != 0.0:
                    ymwta__lomk[ccdt__htbfp, lfnm__vwi] = ymwta__lomk[
                        lfnm__vwi, ccdt__htbfp] = dptjz__dxqw / eign__fnwg
                else:
                    ymwta__lomk[ccdt__htbfp, lfnm__vwi] = ymwta__lomk[
                        lfnm__vwi, ccdt__htbfp] = np.nan
    return ymwta__lomk


@numba.generated_jit(nopython=True)
def duplicated(data, parallel=False):
    n = len(data)
    if n == 0:
        return lambda data, parallel=False: np.empty(0, dtype=np.bool_)
    logbc__mijd = n != 1
    wbp__gsvz = 'def impl(data, parallel=False):\n'
    wbp__gsvz += '  if parallel:\n'
    ixzce__nqhd = ', '.join(f'array_to_info(data[{i}])' for i in range(n))
    wbp__gsvz += f'    cpp_table = arr_info_list_to_table([{ixzce__nqhd}])\n'
    wbp__gsvz += (
        f'    out_cpp_table = bodo.libs.array.shuffle_table(cpp_table, {n}, parallel, 1)\n'
        )
    bhaj__khztd = ', '.join(
        f'info_to_array(info_from_table(out_cpp_table, {i}), data[{i}])' for
        i in range(n))
    wbp__gsvz += f'    data = ({bhaj__khztd},)\n'
    wbp__gsvz += (
        '    shuffle_info = bodo.libs.array.get_shuffle_info(out_cpp_table)\n')
    wbp__gsvz += '    bodo.libs.array.delete_table(out_cpp_table)\n'
    wbp__gsvz += '    bodo.libs.array.delete_table(cpp_table)\n'
    wbp__gsvz += '  n = len(data[0])\n'
    wbp__gsvz += '  out = np.empty(n, np.bool_)\n'
    wbp__gsvz += '  uniqs = dict()\n'
    if logbc__mijd:
        wbp__gsvz += '  for i in range(n):\n'
        wfcnb__fgb = ', '.join(f'data[{i}][i]' for i in range(n))
        ixhb__zyi = ',  '.join(
            f'bodo.libs.array_kernels.isna(data[{i}], i)' for i in range(n))
        wbp__gsvz += f"""    val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({wfcnb__fgb},), ({ixhb__zyi},))
"""
        wbp__gsvz += '    if val in uniqs:\n'
        wbp__gsvz += '      out[i] = True\n'
        wbp__gsvz += '    else:\n'
        wbp__gsvz += '      out[i] = False\n'
        wbp__gsvz += '      uniqs[val] = 0\n'
    else:
        wbp__gsvz += '  data = data[0]\n'
        wbp__gsvz += '  hasna = False\n'
        wbp__gsvz += '  for i in range(n):\n'
        wbp__gsvz += '    if bodo.libs.array_kernels.isna(data, i):\n'
        wbp__gsvz += '      out[i] = hasna\n'
        wbp__gsvz += '      hasna = True\n'
        wbp__gsvz += '    else:\n'
        wbp__gsvz += '      val = data[i]\n'
        wbp__gsvz += '      if val in uniqs:\n'
        wbp__gsvz += '        out[i] = True\n'
        wbp__gsvz += '      else:\n'
        wbp__gsvz += '        out[i] = False\n'
        wbp__gsvz += '        uniqs[val] = 0\n'
    wbp__gsvz += '  if parallel:\n'
    wbp__gsvz += (
        '    out = bodo.hiframes.pd_groupby_ext.reverse_shuffle(out, shuffle_info)\n'
        )
    wbp__gsvz += '  return out\n'
    nxpc__izwqb = {}
    exec(wbp__gsvz, {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table}, nxpc__izwqb)
    impl = nxpc__izwqb['impl']
    return impl


def sample_table_operation(data, ind_arr, n, frac, replace, parallel=False):
    pass


@overload(sample_table_operation, no_unliteral=True)
def overload_sample_table_operation(data, ind_arr, n, frac, replace,
    parallel=False):
    jpg__nplhk = len(data)
    wbp__gsvz = 'def impl(data, ind_arr, n, frac, replace, parallel=False):\n'
    wbp__gsvz += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        jpg__nplhk)))
    wbp__gsvz += '  table_total = arr_info_list_to_table(info_list_total)\n'
    wbp__gsvz += (
        '  out_table = sample_table(table_total, n, frac, replace, parallel)\n'
        .format(jpg__nplhk))
    for vlo__cxo in range(jpg__nplhk):
        wbp__gsvz += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(vlo__cxo, vlo__cxo, vlo__cxo))
    wbp__gsvz += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(jpg__nplhk))
    wbp__gsvz += '  delete_table(out_table)\n'
    wbp__gsvz += '  delete_table(table_total)\n'
    wbp__gsvz += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(jpg__nplhk)))
    nxpc__izwqb = {}
    exec(wbp__gsvz, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'sample_table': sample_table, 'arr_info_list_to_table':
        arr_info_list_to_table, 'info_from_table': info_from_table,
        'info_to_array': info_to_array, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, nxpc__izwqb)
    impl = nxpc__izwqb['impl']
    return impl


def drop_duplicates(data, ind_arr, ncols, parallel=False):
    pass


@overload(drop_duplicates, no_unliteral=True)
def overload_drop_duplicates(data, ind_arr, ncols, parallel=False):
    jpg__nplhk = len(data)
    wbp__gsvz = 'def impl(data, ind_arr, ncols, parallel=False):\n'
    wbp__gsvz += '  info_list_total = [{}, array_to_info(ind_arr)]\n'.format(
        ', '.join('array_to_info(data[{}])'.format(x) for x in range(
        jpg__nplhk)))
    wbp__gsvz += '  table_total = arr_info_list_to_table(info_list_total)\n'
    wbp__gsvz += '  keep_i = 0\n'
    wbp__gsvz += """  out_table = drop_duplicates_table(table_total, parallel, ncols, keep_i, False, True)
"""
    for vlo__cxo in range(jpg__nplhk):
        wbp__gsvz += (
            '  out_arr_{} = info_to_array(info_from_table(out_table, {}), data[{}])\n'
            .format(vlo__cxo, vlo__cxo, vlo__cxo))
    wbp__gsvz += (
        '  out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
        .format(jpg__nplhk))
    wbp__gsvz += '  delete_table(out_table)\n'
    wbp__gsvz += '  delete_table(table_total)\n'
    wbp__gsvz += '  return ({},), out_arr_index\n'.format(', '.join(
        'out_arr_{}'.format(i) for i in range(jpg__nplhk)))
    nxpc__izwqb = {}
    exec(wbp__gsvz, {'np': np, 'bodo': bodo, 'array_to_info': array_to_info,
        'drop_duplicates_table': drop_duplicates_table,
        'arr_info_list_to_table': arr_info_list_to_table, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'delete_table_decref_arrays':
        delete_table_decref_arrays}, nxpc__izwqb)
    impl = nxpc__izwqb['impl']
    return impl


def drop_duplicates_array(data_arr, parallel=False):
    pass


@overload(drop_duplicates_array, no_unliteral=True)
def overload_drop_duplicates_array(data_arr, parallel=False):

    def impl(data_arr, parallel=False):
        xajl__inknu = [array_to_info(data_arr)]
        zsrx__iybd = arr_info_list_to_table(xajl__inknu)
        vvr__eepsz = 0
        kxhiq__msjix = drop_duplicates_table(zsrx__iybd, parallel, 1,
            vvr__eepsz, False, True)
        out_arr = info_to_array(info_from_table(kxhiq__msjix, 0), data_arr)
        delete_table(kxhiq__msjix)
        delete_table(zsrx__iybd)
        return out_arr
    return impl


def dropna(data, how, thresh, subset, parallel=False):
    pass


@overload(dropna, no_unliteral=True)
def overload_dropna(data, how, thresh, subset):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.dropna()')
    mke__wyjp = len(data.types)
    mgeec__caj = [('out' + str(i)) for i in range(mke__wyjp)]
    izy__iofxz = get_overload_const_list(subset)
    how = get_overload_const_str(how)
    dhwhq__hgc = ['isna(data[{}], i)'.format(i) for i in izy__iofxz]
    ernh__wciko = 'not ({})'.format(' or '.join(dhwhq__hgc))
    if not is_overload_none(thresh):
        ernh__wciko = '(({}) <= ({}) - thresh)'.format(' + '.join(
            dhwhq__hgc), mke__wyjp - 1)
    elif how == 'all':
        ernh__wciko = 'not ({})'.format(' and '.join(dhwhq__hgc))
    wbp__gsvz = 'def _dropna_imp(data, how, thresh, subset):\n'
    wbp__gsvz += '  old_len = len(data[0])\n'
    wbp__gsvz += '  new_len = 0\n'
    wbp__gsvz += '  for i in range(old_len):\n'
    wbp__gsvz += '    if {}:\n'.format(ernh__wciko)
    wbp__gsvz += '      new_len += 1\n'
    for i, out in enumerate(mgeec__caj):
        if isinstance(data[i], bodo.CategoricalArrayType):
            wbp__gsvz += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, data[{1}], (-1,))\n'
                .format(out, i))
        else:
            wbp__gsvz += (
                '  {0} = bodo.utils.utils.alloc_type(new_len, t{1}, (-1,))\n'
                .format(out, i))
    wbp__gsvz += '  curr_ind = 0\n'
    wbp__gsvz += '  for i in range(old_len):\n'
    wbp__gsvz += '    if {}:\n'.format(ernh__wciko)
    for i in range(mke__wyjp):
        wbp__gsvz += '      if isna(data[{}], i):\n'.format(i)
        wbp__gsvz += '        setna({}, curr_ind)\n'.format(mgeec__caj[i])
        wbp__gsvz += '      else:\n'
        wbp__gsvz += '        {}[curr_ind] = data[{}][i]\n'.format(mgeec__caj
            [i], i)
    wbp__gsvz += '      curr_ind += 1\n'
    wbp__gsvz += '  return {}\n'.format(', '.join(mgeec__caj))
    nxpc__izwqb = {}
    wiand__zyi = {'t{}'.format(i): wtwu__nnm for i, wtwu__nnm in enumerate(
        data.types)}
    wiand__zyi.update({'isna': isna, 'setna': setna, 'init_nested_counts':
        bodo.utils.indexing.init_nested_counts, 'add_nested_counts': bodo.
        utils.indexing.add_nested_counts, 'bodo': bodo})
    exec(wbp__gsvz, wiand__zyi, nxpc__izwqb)
    bsu__geyu = nxpc__izwqb['_dropna_imp']
    return bsu__geyu


def get(arr, ind):
    pass


@overload(get, no_unliteral=True)
def overload_get(arr, ind):
    if isinstance(arr, ArrayItemArrayType):
        mjsii__ghoh = arr.dtype
        wzn__toyt = mjsii__ghoh.dtype

        def get_arr_item(arr, ind):
            n = len(arr)
            vkni__ogo = init_nested_counts(wzn__toyt)
            for k in range(n):
                if bodo.libs.array_kernels.isna(arr, k):
                    continue
                val = arr[k]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    continue
                vkni__ogo = add_nested_counts(vkni__ogo, val[ind])
            out_arr = bodo.utils.utils.alloc_type(n, mjsii__ghoh, vkni__ogo)
            for wen__zvhx in range(n):
                if bodo.libs.array_kernels.isna(arr, wen__zvhx):
                    setna(out_arr, wen__zvhx)
                    continue
                val = arr[wen__zvhx]
                if not len(val) > ind >= -len(val
                    ) or bodo.libs.array_kernels.isna(val, ind):
                    setna(out_arr, wen__zvhx)
                    continue
                out_arr[wen__zvhx] = val[ind]
            return out_arr
        return get_arr_item


def _is_same_categorical_array_type(arr_types):
    from bodo.hiframes.pd_categorical_ext import _to_readonly
    if not isinstance(arr_types, types.BaseTuple) or len(arr_types) == 0:
        return False
    rew__eoj = _to_readonly(arr_types.types[0])
    return all(isinstance(wtwu__nnm, CategoricalArrayType) and _to_readonly
        (wtwu__nnm) == rew__eoj for wtwu__nnm in arr_types.types)


def concat(arr_list):
    pass


@overload(concat, no_unliteral=True)
def concat_overload(arr_list):
    if isinstance(arr_list, bodo.NullableTupleType):
        return lambda arr_list: bodo.libs.array_kernels.concat(arr_list._data)
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, ArrayItemArrayType):
        krjk__tkix = arr_list.dtype.dtype

        def array_item_concat_impl(arr_list):
            bez__ygi = 0
            rqd__dlf = []
            for A in arr_list:
                kzrt__ewaq = len(A)
                bodo.libs.array_item_arr_ext.trim_excess_data(A)
                rqd__dlf.append(bodo.libs.array_item_arr_ext.get_data(A))
                bez__ygi += kzrt__ewaq
            nsq__gxour = np.empty(bez__ygi + 1, offset_type)
            vxyz__kiehb = bodo.libs.array_kernels.concat(rqd__dlf)
            gdbk__kizwc = np.empty(bez__ygi + 7 >> 3, np.uint8)
            ojxy__xyvw = 0
            zyqy__echjk = 0
            for A in arr_list:
                pdsr__bapby = bodo.libs.array_item_arr_ext.get_offsets(A)
                cwm__kzei = bodo.libs.array_item_arr_ext.get_null_bitmap(A)
                kzrt__ewaq = len(A)
                lin__olitq = pdsr__bapby[kzrt__ewaq]
                for i in range(kzrt__ewaq):
                    nsq__gxour[i + ojxy__xyvw] = pdsr__bapby[i] + zyqy__echjk
                    pve__fzzre = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        cwm__kzei, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(gdbk__kizwc, i +
                        ojxy__xyvw, pve__fzzre)
                ojxy__xyvw += kzrt__ewaq
                zyqy__echjk += lin__olitq
            nsq__gxour[ojxy__xyvw] = zyqy__echjk
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                bez__ygi, vxyz__kiehb, nsq__gxour, gdbk__kizwc)
            return out_arr
        return array_item_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.StructArrayType):
        ubjm__zrfli = arr_list.dtype.names
        wbp__gsvz = 'def struct_array_concat_impl(arr_list):\n'
        wbp__gsvz += f'    n_all = 0\n'
        for i in range(len(ubjm__zrfli)):
            wbp__gsvz += f'    concat_list{i} = []\n'
        wbp__gsvz += '    for A in arr_list:\n'
        wbp__gsvz += (
            '        data_tuple = bodo.libs.struct_arr_ext.get_data(A)\n')
        for i in range(len(ubjm__zrfli)):
            wbp__gsvz += f'        concat_list{i}.append(data_tuple[{i}])\n'
        wbp__gsvz += '        n_all += len(A)\n'
        wbp__gsvz += '    n_bytes = (n_all + 7) >> 3\n'
        wbp__gsvz += '    new_mask = np.empty(n_bytes, np.uint8)\n'
        wbp__gsvz += '    curr_bit = 0\n'
        wbp__gsvz += '    for A in arr_list:\n'
        wbp__gsvz += (
            '        old_mask = bodo.libs.struct_arr_ext.get_null_bitmap(A)\n')
        wbp__gsvz += '        for j in range(len(A)):\n'
        wbp__gsvz += (
            '            bit = bodo.libs.int_arr_ext.get_bit_bitmap_arr(old_mask, j)\n'
            )
        wbp__gsvz += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(new_mask, curr_bit, bit)\n'
            )
        wbp__gsvz += '            curr_bit += 1\n'
        wbp__gsvz += '    return bodo.libs.struct_arr_ext.init_struct_arr(\n'
        yoaw__ncc = ', '.join([
            f'bodo.libs.array_kernels.concat(concat_list{i})' for i in
            range(len(ubjm__zrfli))])
        wbp__gsvz += f'        ({yoaw__ncc},),\n'
        wbp__gsvz += '        new_mask,\n'
        wbp__gsvz += f'        {ubjm__zrfli},\n'
        wbp__gsvz += '    )\n'
        nxpc__izwqb = {}
        exec(wbp__gsvz, {'bodo': bodo, 'np': np}, nxpc__izwqb)
        return nxpc__izwqb['struct_array_concat_impl']
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.DatetimeArrayType):
        hdb__lzjoq = arr_list.dtype.tz

        def tz_aware_concat_impl(arr_list):
            gcrx__swea = 0
            for A in arr_list:
                gcrx__swea += len(A)
            nazhk__pna = bodo.libs.pd_datetime_arr_ext.alloc_pd_datetime_array(
                gcrx__swea, hdb__lzjoq)
            ozhmn__ajwe = 0
            for A in arr_list:
                for i in range(len(A)):
                    nazhk__pna[i + ozhmn__ajwe] = A[i]
                ozhmn__ajwe += len(A)
            return nazhk__pna
        return tz_aware_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_date_array_type:

        def datetime_date_array_concat_impl(arr_list):
            gcrx__swea = 0
            for A in arr_list:
                gcrx__swea += len(A)
            nazhk__pna = (bodo.hiframes.datetime_date_ext.
                alloc_datetime_date_array(gcrx__swea))
            ozhmn__ajwe = 0
            for A in arr_list:
                for i in range(len(A)):
                    nazhk__pna._data[i + ozhmn__ajwe] = A._data[i]
                    pve__fzzre = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(nazhk__pna.
                        _null_bitmap, i + ozhmn__ajwe, pve__fzzre)
                ozhmn__ajwe += len(A)
            return nazhk__pna
        return datetime_date_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == datetime_timedelta_array_type:

        def datetime_timedelta_array_concat_impl(arr_list):
            gcrx__swea = 0
            for A in arr_list:
                gcrx__swea += len(A)
            nazhk__pna = (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(gcrx__swea))
            ozhmn__ajwe = 0
            for A in arr_list:
                for i in range(len(A)):
                    nazhk__pna._days_data[i + ozhmn__ajwe] = A._days_data[i]
                    nazhk__pna._seconds_data[i + ozhmn__ajwe
                        ] = A._seconds_data[i]
                    nazhk__pna._microseconds_data[i + ozhmn__ajwe
                        ] = A._microseconds_data[i]
                    pve__fzzre = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(nazhk__pna.
                        _null_bitmap, i + ozhmn__ajwe, pve__fzzre)
                ozhmn__ajwe += len(A)
            return nazhk__pna
        return datetime_timedelta_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, DecimalArrayType):
        ryzqs__tfc = arr_list.dtype.precision
        pifc__ege = arr_list.dtype.scale

        def decimal_array_concat_impl(arr_list):
            gcrx__swea = 0
            for A in arr_list:
                gcrx__swea += len(A)
            nazhk__pna = bodo.libs.decimal_arr_ext.alloc_decimal_array(
                gcrx__swea, ryzqs__tfc, pifc__ege)
            ozhmn__ajwe = 0
            for A in arr_list:
                for i in range(len(A)):
                    nazhk__pna._data[i + ozhmn__ajwe] = A._data[i]
                    pve__fzzre = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, i)
                    bodo.libs.int_arr_ext.set_bit_to_arr(nazhk__pna.
                        _null_bitmap, i + ozhmn__ajwe, pve__fzzre)
                ozhmn__ajwe += len(A)
            return nazhk__pna
        return decimal_array_concat_impl
    if isinstance(arr_list, (types.UniTuple, types.List)) and (is_str_arr_type
        (arr_list.dtype) or arr_list.dtype == bodo.binary_array_type
        ) or isinstance(arr_list, types.BaseTuple) and all(is_str_arr_type(
        wtwu__nnm) for wtwu__nnm in arr_list.types):
        if isinstance(arr_list, types.BaseTuple):
            dpy__rxmh = arr_list.types[0]
            for i in range(len(arr_list)):
                if arr_list.types[i] != bodo.dict_str_arr_type:
                    dpy__rxmh = arr_list.types[i]
                    break
        else:
            dpy__rxmh = arr_list.dtype
        if dpy__rxmh == bodo.dict_str_arr_type:

            def impl_dict_arr(arr_list):
                ojqld__htf = 0
                zmm__tsgzx = 0
                duq__fgv = 0
                for A in arr_list:
                    data_arr = A._data
                    zru__dohat = A._indices
                    duq__fgv += len(zru__dohat)
                    ojqld__htf += len(data_arr)
                    zmm__tsgzx += bodo.libs.str_arr_ext.num_total_chars(
                        data_arr)
                icx__hrhyq = pre_alloc_string_array(ojqld__htf, zmm__tsgzx)
                htxa__zafs = bodo.libs.int_arr_ext.alloc_int_array(duq__fgv,
                    np.int32)
                bodo.libs.str_arr_ext.set_null_bits_to_value(icx__hrhyq, -1)
                fra__iiogb = 0
                ysmxb__hvlp = 0
                zeco__sqdrb = 0
                for A in arr_list:
                    data_arr = A._data
                    zru__dohat = A._indices
                    duq__fgv = len(zru__dohat)
                    bodo.libs.str_arr_ext.set_string_array_range(icx__hrhyq,
                        data_arr, fra__iiogb, ysmxb__hvlp)
                    for i in range(duq__fgv):
                        if bodo.libs.array_kernels.isna(zru__dohat, i
                            ) or bodo.libs.array_kernels.isna(data_arr,
                            zru__dohat[i]):
                            bodo.libs.array_kernels.setna(htxa__zafs, 
                                zeco__sqdrb + i)
                        else:
                            htxa__zafs[zeco__sqdrb + i
                                ] = fra__iiogb + zru__dohat[i]
                    fra__iiogb += len(data_arr)
                    ysmxb__hvlp += bodo.libs.str_arr_ext.num_total_chars(
                        data_arr)
                    zeco__sqdrb += duq__fgv
                out_arr = init_dict_arr(icx__hrhyq, htxa__zafs, False, False)
                tdavw__kpxkq = drop_duplicates_local_dictionary(out_arr, False)
                return tdavw__kpxkq
            return impl_dict_arr

        def impl_str(arr_list):
            arr_list = decode_if_dict_array(arr_list)
            ojqld__htf = 0
            zmm__tsgzx = 0
            for A in arr_list:
                arr = A
                ojqld__htf += len(arr)
                zmm__tsgzx += bodo.libs.str_arr_ext.num_total_chars(arr)
            out_arr = bodo.utils.utils.alloc_type(ojqld__htf, dpy__rxmh, (
                zmm__tsgzx,))
            bodo.libs.str_arr_ext.set_null_bits_to_value(out_arr, -1)
            fra__iiogb = 0
            ysmxb__hvlp = 0
            for A in arr_list:
                arr = A
                bodo.libs.str_arr_ext.set_string_array_range(out_arr, arr,
                    fra__iiogb, ysmxb__hvlp)
                fra__iiogb += len(arr)
                ysmxb__hvlp += bodo.libs.str_arr_ext.num_total_chars(arr)
            return out_arr
        return impl_str
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, IntegerArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(wtwu__nnm.dtype, types.Integer) for
        wtwu__nnm in arr_list.types) and any(isinstance(wtwu__nnm,
        IntegerArrayType) for wtwu__nnm in arr_list.types):

        def impl_int_arr_list(arr_list):
            axfzu__kxb = convert_to_nullable_tup(arr_list)
            wxx__saza = []
            nvxys__izc = 0
            for A in axfzu__kxb:
                wxx__saza.append(A._data)
                nvxys__izc += len(A)
            vxyz__kiehb = bodo.libs.array_kernels.concat(wxx__saza)
            aqd__osic = nvxys__izc + 7 >> 3
            eyx__jlc = np.empty(aqd__osic, np.uint8)
            hhg__oor = 0
            for A in axfzu__kxb:
                otiv__rclo = A._null_bitmap
                for wen__zvhx in range(len(A)):
                    pve__fzzre = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        otiv__rclo, wen__zvhx)
                    bodo.libs.int_arr_ext.set_bit_to_arr(eyx__jlc, hhg__oor,
                        pve__fzzre)
                    hhg__oor += 1
            return bodo.libs.int_arr_ext.init_integer_array(vxyz__kiehb,
                eyx__jlc)
        return impl_int_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)
        ) and arr_list.dtype == boolean_array or isinstance(arr_list, types
        .BaseTuple) and all(wtwu__nnm.dtype == types.bool_ for wtwu__nnm in
        arr_list.types) and any(wtwu__nnm == boolean_array for wtwu__nnm in
        arr_list.types):

        def impl_bool_arr_list(arr_list):
            axfzu__kxb = convert_to_nullable_tup(arr_list)
            wxx__saza = []
            nvxys__izc = 0
            for A in axfzu__kxb:
                wxx__saza.append(A._data)
                nvxys__izc += len(A)
            vxyz__kiehb = bodo.libs.array_kernels.concat(wxx__saza)
            aqd__osic = nvxys__izc + 7 >> 3
            eyx__jlc = np.empty(aqd__osic, np.uint8)
            hhg__oor = 0
            for A in axfzu__kxb:
                otiv__rclo = A._null_bitmap
                for wen__zvhx in range(len(A)):
                    pve__fzzre = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        otiv__rclo, wen__zvhx)
                    bodo.libs.int_arr_ext.set_bit_to_arr(eyx__jlc, hhg__oor,
                        pve__fzzre)
                    hhg__oor += 1
            return bodo.libs.bool_arr_ext.init_bool_array(vxyz__kiehb, eyx__jlc
                )
        return impl_bool_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, FloatingArrayType) or isinstance(arr_list, types.
        BaseTuple) and all(isinstance(wtwu__nnm.dtype, types.Float) for
        wtwu__nnm in arr_list.types) and any(isinstance(wtwu__nnm,
        FloatingArrayType) for wtwu__nnm in arr_list.types):

        def impl_float_arr_list(arr_list):
            axfzu__kxb = convert_to_nullable_tup(arr_list)
            wxx__saza = []
            nvxys__izc = 0
            for A in axfzu__kxb:
                wxx__saza.append(A._data)
                nvxys__izc += len(A)
            vxyz__kiehb = bodo.libs.array_kernels.concat(wxx__saza)
            aqd__osic = nvxys__izc + 7 >> 3
            eyx__jlc = np.empty(aqd__osic, np.uint8)
            hhg__oor = 0
            for A in axfzu__kxb:
                otiv__rclo = A._null_bitmap
                for wen__zvhx in range(len(A)):
                    pve__fzzre = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        otiv__rclo, wen__zvhx)
                    bodo.libs.int_arr_ext.set_bit_to_arr(eyx__jlc, hhg__oor,
                        pve__fzzre)
                    hhg__oor += 1
            return bodo.libs.float_arr_ext.init_float_array(vxyz__kiehb,
                eyx__jlc)
        return impl_float_arr_list
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, CategoricalArrayType):

        def cat_array_concat_impl(arr_list):
            oufuq__wiwe = []
            for A in arr_list:
                oufuq__wiwe.append(A.codes)
            return init_categorical_array(bodo.libs.array_kernels.concat(
                oufuq__wiwe), arr_list[0].dtype)
        return cat_array_concat_impl
    if _is_same_categorical_array_type(arr_list):
        sykb__dkrkl = ', '.join(f'arr_list[{i}].codes' for i in range(len(
            arr_list)))
        wbp__gsvz = 'def impl(arr_list):\n'
        wbp__gsvz += f"""    return init_categorical_array(bodo.libs.array_kernels.concat(({sykb__dkrkl}, )), arr_list[0].dtype)
"""
        faz__uiziy = {}
        exec(wbp__gsvz, {'bodo': bodo, 'init_categorical_array':
            init_categorical_array}, faz__uiziy)
        return faz__uiziy['impl']
    if isinstance(arr_list, types.List) and isinstance(arr_list.dtype,
        types.Array) and arr_list.dtype.ndim == 1:
        dtype = arr_list.dtype.dtype

        def impl_np_arr_list(arr_list):
            nvxys__izc = 0
            for A in arr_list:
                nvxys__izc += len(A)
            out_arr = np.empty(nvxys__izc, dtype)
            igd__vxbv = 0
            for A in arr_list:
                n = len(A)
                out_arr[igd__vxbv:igd__vxbv + n] = A
                igd__vxbv += n
            return out_arr
        return impl_np_arr_list
    if isinstance(arr_list, types.BaseTuple) and any(isinstance(wtwu__nnm,
        (types.Array, IntegerArrayType)) and isinstance(wtwu__nnm.dtype,
        types.Integer) for wtwu__nnm in arr_list.types) and any(isinstance(
        wtwu__nnm, types.Array) and isinstance(wtwu__nnm.dtype, types.Float
        ) for wtwu__nnm in arr_list.types):
        return lambda arr_list: np.concatenate(astype_float_tup(arr_list))
    if isinstance(arr_list, (types.UniTuple, types.List)) and isinstance(
        arr_list.dtype, bodo.MapArrayType):

        def impl_map_arr_list(arr_list):
            lihmk__gdfkb = []
            for A in arr_list:
                lihmk__gdfkb.append(A._data)
            hsrr__oans = bodo.libs.array_kernels.concat(lihmk__gdfkb)
            ymwta__lomk = bodo.libs.map_arr_ext.init_map_arr(hsrr__oans)
            return ymwta__lomk
        return impl_map_arr_list
    if isinstance(arr_list, types.Tuple):
        wfg__pnv = all([(isinstance(ggt__qmjet, bodo.DatetimeArrayType) or 
            isinstance(ggt__qmjet, types.Array) and ggt__qmjet.dtype ==
            bodo.datetime64ns) for ggt__qmjet in arr_list.types])
        if wfg__pnv:
            raise BodoError(
                f'Cannot concatenate the rows of Timestamp data with different timezones. Found types: {arr_list}. Please use pd.Series.tz_convert(None) to remove Timezone information.'
                )
    for ggt__qmjet in arr_list:
        if not isinstance(ggt__qmjet, types.Array):
            raise_bodo_error(f'concat of array types {arr_list} not supported')
    return lambda arr_list: np.concatenate(arr_list)


def astype_float_tup(arr_tup):
    return tuple(wtwu__nnm.astype(np.float64) for wtwu__nnm in arr_tup)


@overload(astype_float_tup, no_unliteral=True)
def overload_astype_float_tup(arr_tup):
    assert isinstance(arr_tup, types.BaseTuple)
    jpg__nplhk = len(arr_tup.types)
    wbp__gsvz = 'def f(arr_tup):\n'
    wbp__gsvz += '  return ({}{})\n'.format(','.join(
        'arr_tup[{}].astype(np.float64)'.format(i) for i in range(
        jpg__nplhk)), ',' if jpg__nplhk == 1 else '')
    nxpc__izwqb = {}
    exec(wbp__gsvz, {'np': np}, nxpc__izwqb)
    xxu__tnlup = nxpc__izwqb['f']
    return xxu__tnlup


def convert_to_nullable_tup(arr_tup):
    pass


@overload(convert_to_nullable_tup, no_unliteral=True)
def overload_convert_to_nullable_tup(arr_tup):
    if isinstance(arr_tup, (types.UniTuple, types.List)) and isinstance(arr_tup
        .dtype, (IntegerArrayType, FloatingArrayType, BooleanArrayType)):
        return lambda arr_tup: arr_tup
    assert isinstance(arr_tup, types.BaseTuple
        ), 'convert_to_nullable_tup: tuple expected'
    jpg__nplhk = len(arr_tup.types)
    zyreo__tbm = find_common_np_dtype(arr_tup.types)
    wzn__toyt = None
    oedzx__wydia = ''
    if isinstance(zyreo__tbm, types.Integer):
        wzn__toyt = bodo.libs.int_arr_ext.IntDtype(zyreo__tbm)
        oedzx__wydia = '.astype(out_dtype, False)'
    if isinstance(zyreo__tbm, types.Float
        ) and bodo.libs.float_arr_ext._use_nullable_float:
        wzn__toyt = bodo.libs.float_arr_ext.FloatDtype(zyreo__tbm)
        oedzx__wydia = '.astype(out_dtype, False)'
    wbp__gsvz = 'def f(arr_tup):\n'
    wbp__gsvz += '  return ({}{})\n'.format(','.join(
        f'bodo.utils.conversion.coerce_to_array(arr_tup[{i}], use_nullable_array=True){oedzx__wydia}'
         for i in range(jpg__nplhk)), ',' if jpg__nplhk == 1 else '')
    nxpc__izwqb = {}
    exec(wbp__gsvz, {'bodo': bodo, 'out_dtype': wzn__toyt}, nxpc__izwqb)
    pky__jvd = nxpc__izwqb['f']
    return pky__jvd


def nunique(A, dropna):
    pass


def nunique_parallel(A, dropna):
    pass


@overload(nunique, no_unliteral=True)
def nunique_overload(A, dropna):

    def nunique_seq(A, dropna):
        s, rmu__ohlpj = build_set_seen_na(A)
        return len(s) + int(not dropna and rmu__ohlpj)
    return nunique_seq


@overload(nunique_parallel, no_unliteral=True)
def nunique_overload_parallel(A, dropna):
    sum_op = bodo.libs.distributed_api.Reduce_Type.Sum.value

    def nunique_par(A, dropna):
        orl__ttlh = bodo.libs.array_kernels.unique(A, dropna, parallel=True)
        wgazl__vcwt = len(orl__ttlh)
        return bodo.libs.distributed_api.dist_reduce(wgazl__vcwt, np.int32(
            sum_op))
    return nunique_par


def unique(A, dropna=False, parallel=False):
    pass


def accum_func(A, func_name, parallel=False):
    pass


@overload(accum_func, no_unliteral=True)
def accum_func_overload(A, func_name, parallel=False):
    assert is_overload_constant_str(func_name
        ), 'accum_func: func_name should be const'
    ccmi__nqmy = get_overload_const_str(func_name)
    assert ccmi__nqmy in ('cumsum', 'cumprod', 'cummin', 'cummax'
        ), 'accum_func: invalid func_name'
    if ccmi__nqmy == 'cumsum':
        ekee__gapf = A.dtype(0)
        fus__zdp = np.int32(Reduce_Type.Sum.value)
        hqe__awslw = np.add
    if ccmi__nqmy == 'cumprod':
        ekee__gapf = A.dtype(1)
        fus__zdp = np.int32(Reduce_Type.Prod.value)
        hqe__awslw = np.multiply
    if ccmi__nqmy == 'cummin':
        if isinstance(A.dtype, types.Float):
            ekee__gapf = np.finfo(A.dtype(1).dtype).max
        else:
            ekee__gapf = np.iinfo(A.dtype(1).dtype).max
        fus__zdp = np.int32(Reduce_Type.Min.value)
        hqe__awslw = min
    if ccmi__nqmy == 'cummax':
        if isinstance(A.dtype, types.Float):
            ekee__gapf = np.finfo(A.dtype(1).dtype).min
        else:
            ekee__gapf = np.iinfo(A.dtype(1).dtype).min
        fus__zdp = np.int32(Reduce_Type.Max.value)
        hqe__awslw = max
    ijrhd__cddq = A

    def impl(A, func_name, parallel=False):
        n = len(A)
        npze__vflr = ekee__gapf
        if parallel:
            for i in range(n):
                if not bodo.libs.array_kernels.isna(A, i):
                    npze__vflr = hqe__awslw(npze__vflr, A[i])
            npze__vflr = bodo.libs.distributed_api.dist_exscan(npze__vflr,
                fus__zdp)
            if bodo.get_rank() == 0:
                npze__vflr = ekee__gapf
        out_arr = bodo.utils.utils.alloc_type(n, ijrhd__cddq, (-1,))
        for i in range(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(out_arr, i)
                continue
            npze__vflr = hqe__awslw(npze__vflr, A[i])
            out_arr[i] = npze__vflr
        return out_arr
    return impl


@overload(unique, no_unliteral=True)
def unique_overload(A, dropna=False, parallel=False):

    def unique_impl(A, dropna=False, parallel=False):
        lsb__nlmve = arr_info_list_to_table([array_to_info(A)])
        mlo__kqhhh = 1
        vvr__eepsz = 0
        kxhiq__msjix = drop_duplicates_table(lsb__nlmve, parallel,
            mlo__kqhhh, vvr__eepsz, dropna, True)
        out_arr = info_to_array(info_from_table(kxhiq__msjix, 0), A)
        delete_table(lsb__nlmve)
        delete_table(kxhiq__msjix)
        return out_arr
    return unique_impl


def explode(arr, index_arr):
    return pd.Series(arr, index_arr).explode()


@overload(explode, no_unliteral=True)
def overload_explode(arr, index_arr):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    krjk__tkix = bodo.utils.typing.to_nullable_type(arr.dtype)
    nfb__cogmz = index_arr
    yzgro__tint = nfb__cogmz.dtype

    def impl(arr, index_arr):
        n = len(arr)
        vkni__ogo = init_nested_counts(krjk__tkix)
        cqz__uvnyn = init_nested_counts(yzgro__tint)
        for i in range(n):
            qmml__dnrjc = index_arr[i]
            if isna(arr, i):
                vkni__ogo = (vkni__ogo[0] + 1,) + vkni__ogo[1:]
                cqz__uvnyn = add_nested_counts(cqz__uvnyn, qmml__dnrjc)
                continue
            ekym__dbpm = arr[i]
            if len(ekym__dbpm) == 0:
                vkni__ogo = (vkni__ogo[0] + 1,) + vkni__ogo[1:]
                cqz__uvnyn = add_nested_counts(cqz__uvnyn, qmml__dnrjc)
                continue
            vkni__ogo = add_nested_counts(vkni__ogo, ekym__dbpm)
            for zpl__grzi in range(len(ekym__dbpm)):
                cqz__uvnyn = add_nested_counts(cqz__uvnyn, qmml__dnrjc)
        out_arr = bodo.utils.utils.alloc_type(vkni__ogo[0], krjk__tkix,
            vkni__ogo[1:])
        avciu__kkgo = bodo.utils.utils.alloc_type(vkni__ogo[0], nfb__cogmz,
            cqz__uvnyn)
        zyqy__echjk = 0
        for i in range(n):
            if isna(arr, i):
                setna(out_arr, zyqy__echjk)
                avciu__kkgo[zyqy__echjk] = index_arr[i]
                zyqy__echjk += 1
                continue
            ekym__dbpm = arr[i]
            lin__olitq = len(ekym__dbpm)
            if lin__olitq == 0:
                setna(out_arr, zyqy__echjk)
                avciu__kkgo[zyqy__echjk] = index_arr[i]
                zyqy__echjk += 1
                continue
            out_arr[zyqy__echjk:zyqy__echjk + lin__olitq] = ekym__dbpm
            avciu__kkgo[zyqy__echjk:zyqy__echjk + lin__olitq] = index_arr[i]
            zyqy__echjk += lin__olitq
        return out_arr, avciu__kkgo
    return impl


def explode_no_index(arr):
    pass


@overload(explode_no_index, no_unliteral=True)
def overload_explode_no_index(arr, counts):
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type
    krjk__tkix = bodo.utils.typing.to_nullable_type(arr.dtype)

    def impl(arr, counts):
        n = len(arr)
        vkni__ogo = init_nested_counts(krjk__tkix)
        for i in range(n):
            if isna(arr, i):
                vkni__ogo = (vkni__ogo[0] + 1,) + vkni__ogo[1:]
                fkjc__eobcs = 1
            else:
                ekym__dbpm = arr[i]
                jik__qadvc = len(ekym__dbpm)
                if jik__qadvc == 0:
                    vkni__ogo = (vkni__ogo[0] + 1,) + vkni__ogo[1:]
                    fkjc__eobcs = 1
                    continue
                else:
                    vkni__ogo = add_nested_counts(vkni__ogo, ekym__dbpm)
                    fkjc__eobcs = jik__qadvc
            if counts[i] != fkjc__eobcs:
                raise ValueError(
                    'DataFrame.explode(): columns must have matching element counts'
                    )
        out_arr = bodo.utils.utils.alloc_type(vkni__ogo[0], krjk__tkix,
            vkni__ogo[1:])
        zyqy__echjk = 0
        for i in range(n):
            if isna(arr, i):
                setna(out_arr, zyqy__echjk)
                zyqy__echjk += 1
                continue
            ekym__dbpm = arr[i]
            lin__olitq = len(ekym__dbpm)
            if lin__olitq == 0:
                setna(out_arr, zyqy__echjk)
                zyqy__echjk += 1
                continue
            out_arr[zyqy__echjk:zyqy__echjk + lin__olitq] = ekym__dbpm
            zyqy__echjk += lin__olitq
        return out_arr
    return impl


def get_arr_lens(arr, na_empty_as_one=True):
    pass


@overload(get_arr_lens, inline='always', no_unliteral=True)
def overload_get_arr_lens(arr, na_empty_as_one=True):
    na_empty_as_one = get_overload_const_bool(na_empty_as_one)
    assert isinstance(arr, ArrayItemArrayType
        ) or arr == string_array_split_view_type or is_str_arr_type(arr
        ) and not na_empty_as_one or is_bin_arr_type(arr
        ) and not na_empty_as_one, f'get_arr_lens: invalid input array type {arr}'
    if na_empty_as_one:
        czvvs__uaosv = 'np.empty(n, np.int64)'
        fhu__fdixm = 'out_arr[i] = 1'
        zjtxc__nln = 'max(len(arr[i]), 1)'
    else:
        czvvs__uaosv = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)'
        fhu__fdixm = 'bodo.libs.array_kernels.setna(out_arr, i)'
        zjtxc__nln = 'len(arr[i])'
    wbp__gsvz = f"""def impl(arr, na_empty_as_one=True):
    numba.parfors.parfor.init_prange()
    n = len(arr)
    out_arr = {czvvs__uaosv}
    for i in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(arr, i):
            {fhu__fdixm}
        else:
            out_arr[i] = {zjtxc__nln}
    return out_arr
    """
    nxpc__izwqb = {}
    exec(wbp__gsvz, {'bodo': bodo, 'numba': numba, 'np': np}, nxpc__izwqb)
    impl = nxpc__izwqb['impl']
    return impl


def explode_str_split(arr, pat, n, index_arr):
    pass


@overload(explode_str_split, no_unliteral=True)
def overload_explode_str_split(arr, pat, n, index_arr):
    assert is_str_arr_type(arr
        ), f'explode_str_split: string array expected, not {arr}'
    nfb__cogmz = index_arr
    yzgro__tint = nfb__cogmz.dtype

    def impl(arr, pat, n, index_arr):
        itcl__iuwtn = pat is not None and len(pat) > 1
        if itcl__iuwtn:
            ndwwh__jfw = re.compile(pat)
            if n == -1:
                n = 0
        elif n == 0:
            n = -1
        afu__gje = len(arr)
        ojqld__htf = 0
        zmm__tsgzx = 0
        cqz__uvnyn = init_nested_counts(yzgro__tint)
        for i in range(afu__gje):
            qmml__dnrjc = index_arr[i]
            if bodo.libs.array_kernels.isna(arr, i):
                ojqld__htf += 1
                cqz__uvnyn = add_nested_counts(cqz__uvnyn, qmml__dnrjc)
                continue
            if itcl__iuwtn:
                tyvz__yntvu = ndwwh__jfw.split(arr[i], maxsplit=n)
            else:
                tyvz__yntvu = arr[i].split(pat, n)
            ojqld__htf += len(tyvz__yntvu)
            for s in tyvz__yntvu:
                cqz__uvnyn = add_nested_counts(cqz__uvnyn, qmml__dnrjc)
                zmm__tsgzx += bodo.libs.str_arr_ext.get_utf8_size(s)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(ojqld__htf,
            zmm__tsgzx)
        avciu__kkgo = bodo.utils.utils.alloc_type(ojqld__htf, nfb__cogmz,
            cqz__uvnyn)
        gbi__zmef = 0
        for wen__zvhx in range(afu__gje):
            if isna(arr, wen__zvhx):
                out_arr[gbi__zmef] = ''
                bodo.libs.array_kernels.setna(out_arr, gbi__zmef)
                avciu__kkgo[gbi__zmef] = index_arr[wen__zvhx]
                gbi__zmef += 1
                continue
            if itcl__iuwtn:
                tyvz__yntvu = ndwwh__jfw.split(arr[wen__zvhx], maxsplit=n)
            else:
                tyvz__yntvu = arr[wen__zvhx].split(pat, n)
            meimz__ekjle = len(tyvz__yntvu)
            out_arr[gbi__zmef:gbi__zmef + meimz__ekjle] = tyvz__yntvu
            avciu__kkgo[gbi__zmef:gbi__zmef + meimz__ekjle] = index_arr[
                wen__zvhx]
            gbi__zmef += meimz__ekjle
        return out_arr, avciu__kkgo
    return impl


def gen_na_array(n, arr):
    pass


@overload(gen_na_array, no_unliteral=True)
def overload_gen_na_array(n, arr, use_dict_arr=False):
    if isinstance(arr, types.TypeRef):
        arr = arr.instance_type
    dtype = arr.dtype
    if not isinstance(arr, (FloatingArrayType, IntegerArrayType)
        ) and isinstance(dtype, (types.Integer, types.Float)):
        dtype = dtype if isinstance(dtype, types.Float) else types.float64

        def impl_float(n, arr, use_dict_arr=False):
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(n, dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                out_arr[i] = np.nan
            return out_arr
        return impl_float
    if arr == bodo.dict_str_arr_type and is_overload_true(use_dict_arr):

        def impl_dict(n, arr, use_dict_arr=False):
            ezrm__for = bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0)
            mipy__ugrpd = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)
            numba.parfors.parfor.init_prange()
            for i in numba.parfors.parfor.internal_prange(n):
                setna(mipy__ugrpd, i)
            return bodo.libs.dict_arr_ext.init_dict_arr(ezrm__for,
                mipy__ugrpd, True, True)
        return impl_dict
    qqaif__zuix = to_str_arr_if_dict_array(arr)

    def impl(n, arr, use_dict_arr=False):
        numba.parfors.parfor.init_prange()
        out_arr = bodo.utils.utils.alloc_type(n, qqaif__zuix, (0,))
        for i in numba.parfors.parfor.internal_prange(n):
            setna(out_arr, i)
        return out_arr
    return impl


def gen_na_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_gen_na_array = (
    gen_na_array_equiv)


def resize_and_copy(A, new_len):
    pass


@overload(resize_and_copy, no_unliteral=True)
def overload_resize_and_copy(A, old_size, new_len):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.resize_and_copy()')
    fxsqb__zbugt = A
    if A == types.Array(types.uint8, 1, 'C'):

        def impl_char(A, old_size, new_len):
            out_arr = bodo.utils.utils.alloc_type(new_len, fxsqb__zbugt)
            bodo.libs.str_arr_ext.str_copy_ptr(out_arr.ctypes, 0, A.ctypes,
                old_size)
            return out_arr
        return impl_char

    def impl(A, old_size, new_len):
        out_arr = bodo.utils.utils.alloc_type(new_len, fxsqb__zbugt, (-1,))
        out_arr[:old_size] = A[:old_size]
        return out_arr
    return impl


@register_jitable
def calc_nitems(start, stop, step):
    xbkw__gzopk = math.ceil((stop - start) / step)
    return int(max(xbkw__gzopk, 0))


def calc_nitems_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    if guard(find_const, self.func_ir, args[0]) == 0 and guard(find_const,
        self.func_ir, args[2]) == 1:
        return ArrayAnalysis.AnalyzeResult(shape=args[1], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_array_kernels_calc_nitems = (
    calc_nitems_equiv)


def arange_parallel_impl(return_type, *args):
    dtype = as_dtype(return_type.dtype)

    def arange_1(stop):
        return np.arange(0, stop, 1, dtype)

    def arange_2(start, stop):
        return np.arange(start, stop, 1, dtype)

    def arange_3(start, stop, step):
        return np.arange(start, stop, step, dtype)
    if any(isinstance(cbgh__msdn, types.Complex) for cbgh__msdn in args):

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            wjdwh__udpcu = (stop - start) / step
            xbkw__gzopk = math.ceil(wjdwh__udpcu.real)
            abhxi__sxyz = math.ceil(wjdwh__udpcu.imag)
            hrzyy__lqwmd = int(max(min(abhxi__sxyz, xbkw__gzopk), 0))
            arr = np.empty(hrzyy__lqwmd, dtype)
            for i in numba.parfors.parfor.internal_prange(hrzyy__lqwmd):
                arr[i] = start + i * step
            return arr
    else:

        def arange_4(start, stop, step, dtype):
            numba.parfors.parfor.init_prange()
            hrzyy__lqwmd = bodo.libs.array_kernels.calc_nitems(start, stop,
                step)
            arr = np.empty(hrzyy__lqwmd, dtype)
            for i in numba.parfors.parfor.internal_prange(hrzyy__lqwmd):
                arr[i] = start + i * step
            return arr
    if len(args) == 1:
        return arange_1
    elif len(args) == 2:
        return arange_2
    elif len(args) == 3:
        return arange_3
    elif len(args) == 4:
        return arange_4
    else:
        raise BodoError('parallel arange with types {}'.format(args))


if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.arange_parallel_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c72b0390b4f3e52dcc5426bd42c6b55ff96bae5a425381900985d36e7527a4bd':
        warnings.warn('numba.parfors.parfor.arange_parallel_impl has changed')
numba.parfors.parfor.swap_functions_map['arange', 'numpy'
    ] = arange_parallel_impl


def sort(arr, ascending, inplace):
    pass


@overload(sort, no_unliteral=True)
def overload_sort(arr, ascending, inplace):

    def impl(arr, ascending, inplace):
        n = len(arr)
        data = np.arange(n),
        lkw__ubqt = arr,
        if not inplace:
            lkw__ubqt = arr.copy(),
        yoxx__iiht = bodo.libs.str_arr_ext.to_list_if_immutable_arr(lkw__ubqt)
        gae__dqba = bodo.libs.str_arr_ext.to_list_if_immutable_arr(data, True)
        bodo.libs.timsort.sort(yoxx__iiht, 0, n, gae__dqba)
        if not ascending:
            bodo.libs.timsort.reverseRange(yoxx__iiht, 0, n, gae__dqba)
        bodo.libs.str_arr_ext.cp_str_list_to_array(lkw__ubqt, yoxx__iiht)
        return lkw__ubqt[0]
    return impl


def overload_array_max(A):
    if isinstance(A, (IntegerArrayType, FloatingArrayType)
        ) or A == boolean_array:

        def impl(A):
            return pd.Series(A).max()
        return impl


overload(np.max, inline='always', no_unliteral=True)(overload_array_max)
overload(max, inline='always', no_unliteral=True)(overload_array_max)


def overload_array_min(A):
    if isinstance(A, (IntegerArrayType, FloatingArrayType)
        ) or A == boolean_array:

        def impl(A):
            return pd.Series(A).min()
        return impl


overload(np.min, inline='always', no_unliteral=True)(overload_array_min)
overload(min, inline='always', no_unliteral=True)(overload_array_min)


def overload_array_sum(A):
    if isinstance(A, (IntegerArrayType, FloatingArrayType)
        ) or A == boolean_array:

        def impl(A):
            return pd.Series(A).sum()
    return impl


overload(np.sum, inline='always', no_unliteral=True)(overload_array_sum)
overload(sum, inline='always', no_unliteral=True)(overload_array_sum)


@overload(np.prod, inline='always', no_unliteral=True)
def overload_array_prod(A):
    if isinstance(A, (IntegerArrayType, FloatingArrayType)
        ) or A == boolean_array:

        def impl(A):
            return pd.Series(A).prod()
    return impl


def nonzero(arr):
    pass


@overload(nonzero, no_unliteral=True)
def nonzero_overload(A, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.nonzero()')
    if not bodo.utils.utils.is_array_typ(A, False):
        return

    def impl(A, parallel=False):
        n = len(A)
        if parallel:
            offset = bodo.libs.distributed_api.dist_exscan(n, Reduce_Type.
                Sum.value)
        else:
            offset = 0
        ymwta__lomk = []
        for i in range(n):
            if A[i]:
                ymwta__lomk.append(i + offset)
        return np.array(ymwta__lomk, np.int64),
    return impl


def ffill_bfill_arr(arr):
    pass


@overload(ffill_bfill_arr, no_unliteral=True)
def ffill_bfill_overload(A, method, parallel=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'bodo.ffill_bfill_arr()')
    fxsqb__zbugt = element_type(A)
    if fxsqb__zbugt == types.unicode_type:
        null_value = '""'
    elif fxsqb__zbugt == types.bool_:
        null_value = 'False'
    elif fxsqb__zbugt == bodo.datetime64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_tz_naive_timestamp(pd.to_datetime(0))'
            )
    elif fxsqb__zbugt == bodo.timedelta64ns:
        null_value = (
            'bodo.utils.conversion.unbox_if_tz_naive_timestamp(pd.to_timedelta(0))'
            )
    else:
        null_value = '0'
    gbi__zmef = 'i'
    xiypl__yiv = False
    yid__rys = get_overload_const_str(method)
    if yid__rys in ('ffill', 'pad'):
        eazhu__vdvz = 'n'
        send_right = True
    elif yid__rys in ('backfill', 'bfill'):
        eazhu__vdvz = 'n-1, -1, -1'
        send_right = False
        if fxsqb__zbugt == types.unicode_type:
            gbi__zmef = '(n - 1) - i'
            xiypl__yiv = True
    wbp__gsvz = 'def impl(A, method, parallel=False):\n'
    wbp__gsvz += '  A = decode_if_dict_array(A)\n'
    wbp__gsvz += '  has_last_value = False\n'
    wbp__gsvz += f'  last_value = {null_value}\n'
    wbp__gsvz += '  if parallel:\n'
    wbp__gsvz += '    rank = bodo.libs.distributed_api.get_rank()\n'
    wbp__gsvz += '    n_pes = bodo.libs.distributed_api.get_size()\n'
    wbp__gsvz += f"""    has_last_value, last_value = null_border_icomm(A, rank, n_pes, {null_value}, {send_right})
"""
    wbp__gsvz += '  n = len(A)\n'
    wbp__gsvz += '  out_arr = bodo.utils.utils.alloc_type(n, A, (-1,))\n'
    wbp__gsvz += f'  for i in range({eazhu__vdvz}):\n'
    wbp__gsvz += (
        '    if (bodo.libs.array_kernels.isna(A, i) and not has_last_value):\n'
        )
    wbp__gsvz += f'      bodo.libs.array_kernels.setna(out_arr, {gbi__zmef})\n'
    wbp__gsvz += '      continue\n'
    wbp__gsvz += '    s = A[i]\n'
    wbp__gsvz += '    if bodo.libs.array_kernels.isna(A, i):\n'
    wbp__gsvz += '      s = last_value\n'
    wbp__gsvz += f'    out_arr[{gbi__zmef}] = s\n'
    wbp__gsvz += '    last_value = s\n'
    wbp__gsvz += '    has_last_value = True\n'
    if xiypl__yiv:
        wbp__gsvz += '  return out_arr[::-1]\n'
    else:
        wbp__gsvz += '  return out_arr\n'
    wpbq__uwxg = {}
    exec(wbp__gsvz, {'bodo': bodo, 'numba': numba, 'pd': pd,
        'null_border_icomm': null_border_icomm, 'decode_if_dict_array':
        decode_if_dict_array}, wpbq__uwxg)
    impl = wpbq__uwxg['impl']
    return impl


@register_jitable(cache=True)
def null_border_icomm(in_arr, rank, n_pes, null_value, send_right=True):
    if send_right:
        scuxf__voec = 0
        ktlpm__zysn = n_pes - 1
        zdfa__zazh = np.int32(rank + 1)
        mvrx__mbppd = np.int32(rank - 1)
        ydg__gzke = len(in_arr) - 1
        ykxh__azmj = -1
        gnsdg__qqv = -1
    else:
        scuxf__voec = n_pes - 1
        ktlpm__zysn = 0
        zdfa__zazh = np.int32(rank - 1)
        mvrx__mbppd = np.int32(rank + 1)
        ydg__gzke = 0
        ykxh__azmj = len(in_arr)
        gnsdg__qqv = 1
    bics__hblbz = np.int32(bodo.hiframes.rolling.comm_border_tag)
    mljgq__ran = np.empty(1, dtype=np.bool_)
    vklw__cxjt = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    cnc__gpam = np.empty(1, dtype=np.bool_)
    udt__oclla = bodo.utils.utils.alloc_type(1, in_arr, (-1,))
    uoakm__tbuqe = False
    sbc__jdfyq = null_value
    for i in range(ydg__gzke, ykxh__azmj, gnsdg__qqv):
        if not isna(in_arr, i):
            uoakm__tbuqe = True
            sbc__jdfyq = in_arr[i]
            break
    if rank != scuxf__voec:
        vomg__yjnz = bodo.libs.distributed_api.irecv(mljgq__ran, 1,
            mvrx__mbppd, bics__hblbz, True)
        bodo.libs.distributed_api.wait(vomg__yjnz, True)
        cwx__vxru = bodo.libs.distributed_api.irecv(vklw__cxjt, 1,
            mvrx__mbppd, bics__hblbz, True)
        bodo.libs.distributed_api.wait(cwx__vxru, True)
        aaf__zcgt = mljgq__ran[0]
        qyy__wsj = vklw__cxjt[0]
    else:
        aaf__zcgt = False
        qyy__wsj = null_value
    if uoakm__tbuqe:
        cnc__gpam[0] = uoakm__tbuqe
        udt__oclla[0] = sbc__jdfyq
    else:
        cnc__gpam[0] = aaf__zcgt
        udt__oclla[0] = qyy__wsj
    if rank != ktlpm__zysn:
        fiv__swc = bodo.libs.distributed_api.isend(cnc__gpam, 1, zdfa__zazh,
            bics__hblbz, True)
        yjr__gdw = bodo.libs.distributed_api.isend(udt__oclla, 1,
            zdfa__zazh, bics__hblbz, True)
    return aaf__zcgt, qyy__wsj


@overload(np.sort, inline='always', no_unliteral=True)
def np_sort(A, axis=-1, kind=None, order=None):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    fmi__xteh = {'axis': axis, 'kind': kind, 'order': order}
    nsxxa__tzkhw = {'axis': -1, 'kind': None, 'order': None}
    check_unsupported_args('np.sort', fmi__xteh, nsxxa__tzkhw, 'numpy')

    def impl(A, axis=-1, kind=None, order=None):
        return pd.Series(A).sort_values().values
    return impl


def repeat_kernel(A, repeats):
    pass


@overload(repeat_kernel, no_unliteral=True)
def repeat_kernel_overload(A, repeats):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'Series.repeat()')
    fxsqb__zbugt = to_str_arr_if_dict_array(A)
    if isinstance(repeats, types.Integer):
        if A == bodo.dict_str_arr_type:

            def impl_dict_int(A, repeats):
                data_arr = A._data.copy()
                zru__dohat = A._indices
                afu__gje = len(zru__dohat)
                htxa__zafs = alloc_int_array(afu__gje * repeats, np.int32)
                for i in range(afu__gje):
                    gbi__zmef = i * repeats
                    if bodo.libs.array_kernels.isna(zru__dohat, i):
                        for wen__zvhx in range(repeats):
                            bodo.libs.array_kernels.setna(htxa__zafs, 
                                gbi__zmef + wen__zvhx)
                    else:
                        htxa__zafs[gbi__zmef:gbi__zmef + repeats] = zru__dohat[
                            i]
                return init_dict_arr(data_arr, htxa__zafs, A.
                    _has_global_dictionary, A._has_deduped_local_dictionary)
            return impl_dict_int

        def impl_int(A, repeats):
            afu__gje = len(A)
            out_arr = bodo.utils.utils.alloc_type(afu__gje * repeats,
                fxsqb__zbugt, (-1,))
            for i in range(afu__gje):
                gbi__zmef = i * repeats
                if bodo.libs.array_kernels.isna(A, i):
                    for wen__zvhx in range(repeats):
                        bodo.libs.array_kernels.setna(out_arr, gbi__zmef +
                            wen__zvhx)
                else:
                    out_arr[gbi__zmef:gbi__zmef + repeats] = A[i]
            return out_arr
        return impl_int
    if A == bodo.dict_str_arr_type:

        def impl_dict_arr(A, repeats):
            data_arr = A._data.copy()
            zru__dohat = A._indices
            afu__gje = len(zru__dohat)
            htxa__zafs = alloc_int_array(repeats.sum(), np.int32)
            gbi__zmef = 0
            for i in range(afu__gje):
                mbo__zrs = repeats[i]
                if mbo__zrs < 0:
                    raise ValueError('repeats may not contain negative values.'
                        )
                if bodo.libs.array_kernels.isna(zru__dohat, i):
                    for wen__zvhx in range(mbo__zrs):
                        bodo.libs.array_kernels.setna(htxa__zafs, gbi__zmef +
                            wen__zvhx)
                else:
                    htxa__zafs[gbi__zmef:gbi__zmef + mbo__zrs] = zru__dohat[i]
                gbi__zmef += mbo__zrs
            return init_dict_arr(data_arr, htxa__zafs, A.
                _has_global_dictionary, A._has_deduped_local_dictionary)
        return impl_dict_arr

    def impl_arr(A, repeats):
        afu__gje = len(A)
        out_arr = bodo.utils.utils.alloc_type(repeats.sum(), fxsqb__zbugt,
            (-1,))
        gbi__zmef = 0
        for i in range(afu__gje):
            mbo__zrs = repeats[i]
            if mbo__zrs < 0:
                raise ValueError('repeats may not contain negative values.')
            if bodo.libs.array_kernels.isna(A, i):
                for wen__zvhx in range(mbo__zrs):
                    bodo.libs.array_kernels.setna(out_arr, gbi__zmef +
                        wen__zvhx)
            else:
                out_arr[gbi__zmef:gbi__zmef + mbo__zrs] = A[i]
            gbi__zmef += mbo__zrs
        return out_arr
    return impl_arr


@overload(np.repeat, inline='always', no_unliteral=True)
def np_repeat(A, repeats):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return
    if not isinstance(repeats, types.Integer):
        raise BodoError(
            'Only integer type supported for repeats in np.repeat()')

    def impl(A, repeats):
        return bodo.libs.array_kernels.repeat_kernel(A, repeats)
    return impl


@numba.generated_jit
def repeat_like(A, dist_like_arr):
    if not bodo.utils.utils.is_array_typ(A, False
        ) or not bodo.utils.utils.is_array_typ(dist_like_arr, False):
        raise BodoError('Both A and dist_like_arr must be array-like.')

    def impl(A, dist_like_arr):
        return bodo.libs.array_kernels.repeat_kernel(A, len(dist_like_arr))
    return impl


@overload(np.unique, inline='always', no_unliteral=True)
def np_unique(A):
    if not bodo.utils.utils.is_array_typ(A, False) or isinstance(A, types.Array
        ):
        return

    def impl(A):
        jiuj__jjnd = bodo.libs.array_kernels.unique(A)
        return bodo.allgatherv(jiuj__jjnd, False)
    return impl


@overload(np.union1d, inline='always', no_unliteral=True)
def overload_union1d(A1, A2):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.union1d()')

    def impl(A1, A2):
        vkvp__ygrej = bodo.libs.array_kernels.concat([A1, A2])
        nmw__cpyc = bodo.libs.array_kernels.unique(vkvp__ygrej)
        return pd.Series(nmw__cpyc).sort_values().values
    return impl


@overload(np.intersect1d, inline='always', no_unliteral=True)
def overload_intersect1d(A1, A2, assume_unique=False, return_indices=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    fmi__xteh = {'assume_unique': assume_unique, 'return_indices':
        return_indices}
    nsxxa__tzkhw = {'assume_unique': False, 'return_indices': False}
    check_unsupported_args('np.intersect1d', fmi__xteh, nsxxa__tzkhw, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.intersect1d()'
            )
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.intersect1d()')

    def impl(A1, A2, assume_unique=False, return_indices=False):
        zfky__wcy = bodo.libs.array_kernels.unique(A1)
        ftgkg__xexuk = bodo.libs.array_kernels.unique(A2)
        vkvp__ygrej = bodo.libs.array_kernels.concat([zfky__wcy, ftgkg__xexuk])
        fdd__dnxu = pd.Series(vkvp__ygrej).sort_values().values
        return slice_array_intersect1d(fdd__dnxu)
    return impl


@register_jitable
def slice_array_intersect1d(arr):
    xfk__fppyd = arr[1:] == arr[:-1]
    return arr[:-1][xfk__fppyd]


@register_jitable(cache=True)
def intersection_mask_comm(arr, rank, n_pes):
    bics__hblbz = np.int32(bodo.hiframes.rolling.comm_border_tag)
    vuym__mioxd = bodo.utils.utils.alloc_type(1, arr, (-1,))
    if rank != 0:
        srg__mhowe = bodo.libs.distributed_api.isend(arr[:1], 1, np.int32(
            rank - 1), bics__hblbz, True)
        bodo.libs.distributed_api.wait(srg__mhowe, True)
    if rank == n_pes - 1:
        return None
    else:
        lgctf__hkn = bodo.libs.distributed_api.irecv(vuym__mioxd, 1, np.
            int32(rank + 1), bics__hblbz, True)
        bodo.libs.distributed_api.wait(lgctf__hkn, True)
        return vuym__mioxd[0]


@register_jitable(cache=True)
def intersection_mask(arr, parallel=False):
    n = len(arr)
    xfk__fppyd = np.full(n, False)
    for i in range(n - 1):
        if arr[i] == arr[i + 1]:
            xfk__fppyd[i] = True
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        icnw__ulpbl = intersection_mask_comm(arr, rank, n_pes)
        if rank != n_pes - 1 and arr[n - 1] == icnw__ulpbl:
            xfk__fppyd[n - 1] = True
    return xfk__fppyd


@overload(np.setdiff1d, inline='always', no_unliteral=True)
def overload_setdiff1d(A1, A2, assume_unique=False):
    if not bodo.utils.utils.is_array_typ(A1, False
        ) or not bodo.utils.utils.is_array_typ(A2, False):
        return
    fmi__xteh = {'assume_unique': assume_unique}
    nsxxa__tzkhw = {'assume_unique': False}
    check_unsupported_args('np.setdiff1d', fmi__xteh, nsxxa__tzkhw, 'numpy')
    if A1 != A2:
        raise BodoError('Both arrays must be the same type in np.setdiff1d()')
    if A1.ndim != 1 or A2.ndim != 1:
        raise BodoError('Only 1D arrays supported in np.setdiff1d()')

    def impl(A1, A2, assume_unique=False):
        zfky__wcy = bodo.libs.array_kernels.unique(A1)
        ftgkg__xexuk = bodo.libs.array_kernels.unique(A2)
        xfk__fppyd = calculate_mask_setdiff1d(zfky__wcy, ftgkg__xexuk)
        return pd.Series(zfky__wcy[xfk__fppyd]).sort_values().values
    return impl


@register_jitable
def calculate_mask_setdiff1d(A1, A2):
    xfk__fppyd = np.ones(len(A1), np.bool_)
    for i in range(len(A2)):
        xfk__fppyd &= A1 != A2[i]
    return xfk__fppyd


@overload(np.linspace, inline='always', no_unliteral=True)
def np_linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=
    None, axis=0):
    fmi__xteh = {'retstep': retstep, 'axis': axis}
    nsxxa__tzkhw = {'retstep': False, 'axis': 0}
    check_unsupported_args('np.linspace', fmi__xteh, nsxxa__tzkhw, 'numpy')
    anbbe__tpqfy = False
    if is_overload_none(dtype):
        fxsqb__zbugt = np.promote_types(np.promote_types(numba.np.
            numpy_support.as_dtype(start), numba.np.numpy_support.as_dtype(
            stop)), numba.np.numpy_support.as_dtype(types.float64)).type
    else:
        if isinstance(dtype.dtype, types.Integer):
            anbbe__tpqfy = True
        fxsqb__zbugt = numba.np.numpy_support.as_dtype(dtype).type
    if anbbe__tpqfy:

        def impl_int(start, stop, num=50, endpoint=True, retstep=False,
            dtype=None, axis=0):
            cknpu__xywjx = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(num, fxsqb__zbugt)
            for i in numba.parfors.parfor.internal_prange(num):
                out_arr[i] = fxsqb__zbugt(np.floor(start + i * cknpu__xywjx))
            return out_arr
        return impl_int
    else:

        def impl(start, stop, num=50, endpoint=True, retstep=False, dtype=
            None, axis=0):
            cknpu__xywjx = np_linspace_get_stepsize(start, stop, num, endpoint)
            numba.parfors.parfor.init_prange()
            out_arr = np.empty(num, fxsqb__zbugt)
            for i in numba.parfors.parfor.internal_prange(num):
                out_arr[i] = fxsqb__zbugt(start + i * cknpu__xywjx)
            return out_arr
        return impl


def np_linspace_get_stepsize(start, stop, num, endpoint):
    return 0


@overload(np_linspace_get_stepsize, no_unliteral=True)
def overload_np_linspace_get_stepsize(start, stop, num, endpoint):

    def impl(start, stop, num, endpoint):
        if num < 0:
            raise ValueError('np.linspace() Num must be >= 0')
        if endpoint:
            num -= 1
        if num > 1:
            return (stop - start) / num
        return 0
    return impl


@overload(operator.contains, no_unliteral=True)
def arr_contains(A, val):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'np.contains()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.dtype == types.
        unliteral(val)):
        return

    def impl(A, val):
        numba.parfors.parfor.init_prange()
        jpg__nplhk = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                jpg__nplhk += A[i] == val
        return jpg__nplhk > 0
    return impl


@overload(np.any, inline='always', no_unliteral=True)
def np_any(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.any()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    fmi__xteh = {'axis': axis, 'out': out, 'keepdims': keepdims}
    nsxxa__tzkhw = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', fmi__xteh, nsxxa__tzkhw, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        jpg__nplhk = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                jpg__nplhk += int(bool(A[i]))
        return jpg__nplhk > 0
    return impl


@overload(np.all, inline='always', no_unliteral=True)
def np_all(A, axis=None, out=None, keepdims=None):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A, 'np.all()')
    if not (bodo.utils.utils.is_array_typ(A, False) and A.ndim == 1):
        return
    fmi__xteh = {'axis': axis, 'out': out, 'keepdims': keepdims}
    nsxxa__tzkhw = {'axis': None, 'out': None, 'keepdims': None}
    check_unsupported_args('np.any', fmi__xteh, nsxxa__tzkhw, 'numpy')

    def impl(A, axis=None, out=None, keepdims=None):
        numba.parfors.parfor.init_prange()
        jpg__nplhk = 0
        n = len(A)
        for i in numba.parfors.parfor.internal_prange(n):
            if not bodo.libs.array_kernels.isna(A, i):
                jpg__nplhk += int(bool(A[i]))
        return jpg__nplhk == n
    return impl


@overload(np.cbrt, inline='always', no_unliteral=True)
def np_cbrt(A, out=None, where=True, casting='same_kind', order='K', dtype=
    None, subok=True):
    if not (isinstance(A, types.Number) or bodo.utils.utils.is_array_typ(A,
        False) and A.ndim == 1 and isinstance(A.dtype, types.Number)):
        return
    fmi__xteh = {'out': out, 'where': where, 'casting': casting, 'order':
        order, 'dtype': dtype, 'subok': subok}
    nsxxa__tzkhw = {'out': None, 'where': True, 'casting': 'same_kind',
        'order': 'K', 'dtype': None, 'subok': True}
    check_unsupported_args('np.cbrt', fmi__xteh, nsxxa__tzkhw, 'numpy')
    if bodo.utils.utils.is_array_typ(A, False):
        vcbn__rrma = np.promote_types(numba.np.numpy_support.as_dtype(A.
            dtype), numba.np.numpy_support.as_dtype(types.float32)).type

        def impl_arr(A, out=None, where=True, casting='same_kind', order=
            'K', dtype=None, subok=True):
            numba.parfors.parfor.init_prange()
            n = len(A)
            out_arr = np.empty(n, vcbn__rrma)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(out_arr, i)
                    continue
                out_arr[i] = np_cbrt_scalar(A[i], vcbn__rrma)
            return out_arr
        return impl_arr
    vcbn__rrma = np.promote_types(numba.np.numpy_support.as_dtype(A), numba
        .np.numpy_support.as_dtype(types.float32)).type

    def impl_scalar(A, out=None, where=True, casting='same_kind', order='K',
        dtype=None, subok=True):
        return np_cbrt_scalar(A, vcbn__rrma)
    return impl_scalar


@register_jitable
def np_cbrt_scalar(x, float_dtype):
    if np.isnan(x):
        return np.nan
    emfvy__uumfp = x < 0
    if emfvy__uumfp:
        x = -x
    res = np.power(float_dtype(x), 1.0 / 3.0)
    if emfvy__uumfp:
        return -res
    return res


@overload(np.hstack, no_unliteral=True)
def np_hstack(tup):
    urp__zbxwx = isinstance(tup, (types.BaseTuple, types.List))
    glg__cxlb = isinstance(tup, (bodo.SeriesType, bodo.hiframes.
        pd_series_ext.HeterogeneousSeriesType)) and isinstance(tup.data, (
        types.BaseTuple, types.List, bodo.NullableTupleType))
    if isinstance(tup, types.BaseTuple):
        for ggt__qmjet in tup.types:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(
                ggt__qmjet, 'numpy.hstack()')
            urp__zbxwx = urp__zbxwx and bodo.utils.utils.is_array_typ(
                ggt__qmjet, False)
    elif isinstance(tup, types.List):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup.dtype,
            'numpy.hstack()')
        urp__zbxwx = bodo.utils.utils.is_array_typ(tup.dtype, False)
    elif glg__cxlb:
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(tup,
            'numpy.hstack()')
        iwujw__qvjjb = tup.data.tuple_typ if isinstance(tup.data, bodo.
            NullableTupleType) else tup.data
        for ggt__qmjet in iwujw__qvjjb.types:
            glg__cxlb = glg__cxlb and bodo.utils.utils.is_array_typ(ggt__qmjet,
                False)
    if not (urp__zbxwx or glg__cxlb):
        return
    if glg__cxlb:

        def impl_series(tup):
            arr_tup = bodo.hiframes.pd_series_ext.get_series_data(tup)
            return bodo.libs.array_kernels.concat(arr_tup)
        return impl_series

    def impl(tup):
        return bodo.libs.array_kernels.concat(tup)
    return impl


@overload(np.random.multivariate_normal, inline='always', no_unliteral=True)
def np_random_multivariate_normal(mean, cov, size=None, check_valid='warn',
    tol=1e-08):
    fmi__xteh = {'check_valid': check_valid, 'tol': tol}
    nsxxa__tzkhw = {'check_valid': 'warn', 'tol': 1e-08}
    check_unsupported_args('np.random.multivariate_normal', fmi__xteh,
        nsxxa__tzkhw, 'numpy')
    if not isinstance(size, types.Integer):
        raise BodoError(
            'np.random.multivariate_normal() size argument is required and must be an integer'
            )
    if not (bodo.utils.utils.is_array_typ(mean, False) and mean.ndim == 1):
        raise BodoError(
            'np.random.multivariate_normal() mean must be a 1 dimensional numpy array'
            )
    if not (bodo.utils.utils.is_array_typ(cov, False) and cov.ndim == 2):
        raise BodoError(
            'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
            )

    def impl(mean, cov, size=None, check_valid='warn', tol=1e-08):
        _validate_multivar_norm(cov)
        pstfb__zuav = mean.shape[0]
        kfqhy__gup = size, pstfb__zuav
        emmoe__axpsn = np.random.standard_normal(kfqhy__gup)
        cov = cov.astype(np.float64)
        mtzt__cjosa, s, wdurg__sus = np.linalg.svd(cov)
        res = np.dot(emmoe__axpsn, np.sqrt(s).reshape(pstfb__zuav, 1) *
            wdurg__sus)
        ehjps__arz = res + mean
        return ehjps__arz
    return impl


def _validate_multivar_norm(cov):
    return


@overload(_validate_multivar_norm, no_unliteral=True)
def _overload_validate_multivar_norm(cov):

    def impl(cov):
        if cov.shape[0] != cov.shape[1]:
            raise ValueError(
                'np.random.multivariate_normal() cov must be a 2 dimensional square, numpy array'
                )
    return impl


def _nan_argmin(arr):
    return


@overload(_nan_argmin, no_unliteral=True)
def _overload_nan_argmin(arr):
    if isinstance(arr, (IntegerArrayType, FloatingArrayType)) or arr in [
        boolean_array, datetime_date_array_type
        ] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            numba.parfors.parfor.init_prange()
            xtq__mup = bodo.hiframes.series_kernels._get_type_max_value(arr)
            lgp__jtetl = typing.builtins.IndexValue(-1, xtq__mup)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                bwje__itcs = typing.builtins.IndexValue(i, arr[i])
                lgp__jtetl = min(lgp__jtetl, bwje__itcs)
            return lgp__jtetl.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        rau__ggs = bodo.hiframes.pd_categorical_ext.get_categories_int_type(arr
            .dtype)

        def impl_cat_arr(arr):
            pwl__fiums = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            xtq__mup = rau__ggs(len(arr.dtype.categories) + 1)
            lgp__jtetl = typing.builtins.IndexValue(-1, xtq__mup)
            for i in numba.parfors.parfor.internal_prange(len(arr)):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                bwje__itcs = typing.builtins.IndexValue(i, pwl__fiums[i])
                lgp__jtetl = min(lgp__jtetl, bwje__itcs)
            return lgp__jtetl.index
        return impl_cat_arr
    return lambda arr: arr.argmin()


def _nan_argmax(arr):
    return


@overload(_nan_argmax, no_unliteral=True)
def _overload_nan_argmax(arr):
    if isinstance(arr, (IntegerArrayType, FloatingArrayType)) or arr in [
        boolean_array, datetime_date_array_type
        ] or arr.dtype == bodo.timedelta64ns:

        def impl_bodo_arr(arr):
            n = len(arr)
            numba.parfors.parfor.init_prange()
            xtq__mup = bodo.hiframes.series_kernels._get_type_min_value(arr)
            lgp__jtetl = typing.builtins.IndexValue(-1, xtq__mup)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                bwje__itcs = typing.builtins.IndexValue(i, arr[i])
                lgp__jtetl = max(lgp__jtetl, bwje__itcs)
            return lgp__jtetl.index
        return impl_bodo_arr
    if isinstance(arr, CategoricalArrayType):
        assert arr.dtype.ordered, 'Categorical Array must be ordered to select an argmin'
        rau__ggs = bodo.hiframes.pd_categorical_ext.get_categories_int_type(arr
            .dtype)

        def impl_cat_arr(arr):
            n = len(arr)
            pwl__fiums = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            xtq__mup = rau__ggs(-1)
            lgp__jtetl = typing.builtins.IndexValue(-1, xtq__mup)
            for i in numba.parfors.parfor.internal_prange(n):
                if bodo.libs.array_kernels.isna(arr, i):
                    continue
                bwje__itcs = typing.builtins.IndexValue(i, pwl__fiums[i])
                lgp__jtetl = max(lgp__jtetl, bwje__itcs)
            return lgp__jtetl.index
        return impl_cat_arr
    return lambda arr: arr.argmax()


@overload_attribute(types.Array, 'nbytes', inline='always')
def overload_dataframe_index(A):
    return lambda A: A.size * bodo.io.np_io.get_dtype_size(A.dtype)
