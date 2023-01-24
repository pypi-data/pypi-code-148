"""
Implementation of Series attributes and methods using overload.
"""
import operator
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_builtin, overload, overload_attribute, overload_method, register_jitable
import bodo
from bodo.hiframes.datetime_datetime_ext import datetime_datetime_type
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType, datetime_timedelta_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.pd_offsets_ext import is_offsets_type
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType, if_series_to_array_type, is_series_type
from bodo.hiframes.pd_timestamp_ext import PandasTimestampType, convert_val_to_timestamp, pd_timestamp_tz_naive_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.pd_datetime_arr_ext import unwrap_tz_array
from bodo.libs.str_arr_ext import StringArrayType
from bodo.libs.str_ext import string_type
from bodo.utils.transform import is_var_size_item_array_type
from bodo.utils.typing import BodoError, ColNamesMetaType, can_replace, check_unsupported_args, dtype_to_array_type, element_type, get_common_scalar_dtype, get_index_names, get_literal_value, get_overload_const_bytes, get_overload_const_int, get_overload_const_str, is_common_scalar_dtype, is_iterable_type, is_literal_type, is_nullable_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_bytes, is_overload_constant_int, is_overload_constant_nan, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, is_scalar_type, is_str_arr_type, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array


@overload_attribute(HeterogeneousSeriesType, 'index', inline='always')
@overload_attribute(SeriesType, 'index', inline='always')
def overload_series_index(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_index(s)


@overload_attribute(HeterogeneousSeriesType, 'values', inline='always')
@overload_attribute(SeriesType, 'values', inline='always')
def overload_series_values(s):
    if isinstance(s.data, bodo.DatetimeArrayType):

        def impl(s):
            kvgy__xstcd = bodo.hiframes.pd_series_ext.get_series_data(s)
            yco__wzlf = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                kvgy__xstcd)
            return yco__wzlf
        return impl
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s)


@overload_attribute(SeriesType, 'dtype', inline='always')
def overload_series_dtype(s):
    if s.dtype == bodo.string_type:
        raise BodoError('Series.dtype not supported for string Series yet')
    return lambda s: bodo.hiframes.pd_series_ext.get_series_data(s).dtype


@overload_attribute(HeterogeneousSeriesType, 'shape')
@overload_attribute(SeriesType, 'shape')
def overload_series_shape(s):
    return lambda s: (len(bodo.hiframes.pd_series_ext.get_series_data(s)),)


@overload_attribute(HeterogeneousSeriesType, 'ndim', inline='always')
@overload_attribute(SeriesType, 'ndim', inline='always')
def overload_series_ndim(s):
    return lambda s: 1


@overload_attribute(HeterogeneousSeriesType, 'size')
@overload_attribute(SeriesType, 'size')
def overload_series_size(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s))


@overload_attribute(HeterogeneousSeriesType, 'T', inline='always')
@overload_attribute(SeriesType, 'T', inline='always')
def overload_series_T(s):
    return lambda s: s


@overload_attribute(SeriesType, 'hasnans', inline='always')
def overload_series_hasnans(s):
    return lambda s: s.isna().sum() != 0


@overload_attribute(HeterogeneousSeriesType, 'empty')
@overload_attribute(SeriesType, 'empty')
def overload_series_empty(s):
    return lambda s: len(bodo.hiframes.pd_series_ext.get_series_data(s)) == 0


@overload_attribute(SeriesType, 'dtypes', inline='always')
def overload_series_dtypes(s):
    return lambda s: s.dtype


@overload_attribute(HeterogeneousSeriesType, 'name', inline='always')
@overload_attribute(SeriesType, 'name', inline='always')
def overload_series_name(s):
    return lambda s: bodo.hiframes.pd_series_ext.get_series_name(s)


@overload(len, no_unliteral=True)
def overload_series_len(S):
    if isinstance(S, (SeriesType, HeterogeneousSeriesType)):
        return lambda S: len(bodo.hiframes.pd_series_ext.get_series_data(S))


@overload_method(SeriesType, 'copy', inline='always', no_unliteral=True)
def overload_series_copy(S, deep=True):
    if is_overload_true(deep):

        def impl1(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr.copy(),
                index, name)
        return impl1
    if is_overload_false(deep):

        def impl2(S, deep=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl2

    def impl(S, deep=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        if deep:
            arr = arr.copy()
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
    return impl


@overload_method(SeriesType, 'to_list', no_unliteral=True)
@overload_method(SeriesType, 'tolist', no_unliteral=True)
def overload_series_to_list(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.tolist()')
    if isinstance(S.dtype, types.Float):

        def impl_float(S):
            jshmf__pdpa = list()
            for tys__niduj in range(len(S)):
                jshmf__pdpa.append(S.iat[tys__niduj])
            return jshmf__pdpa
        return impl_float

    def impl(S):
        jshmf__pdpa = list()
        for tys__niduj in range(len(S)):
            if bodo.libs.array_kernels.isna(S.values, tys__niduj):
                raise ValueError(
                    'Series.to_list(): Not supported for NA values with non-float dtypes'
                    )
            jshmf__pdpa.append(S.iat[tys__niduj])
        return jshmf__pdpa
    return impl


@overload_method(SeriesType, 'to_numpy', inline='always', no_unliteral=True)
def overload_series_to_numpy(S, dtype=None, copy=False, na_value=None):
    xjc__qmsn = dict(dtype=dtype, copy=copy, na_value=na_value)
    jrco__lxxs = dict(dtype=None, copy=False, na_value=None)
    check_unsupported_args('Series.to_numpy', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')

    def impl(S, dtype=None, copy=False, na_value=None):
        return S.values
    return impl


@overload_method(SeriesType, 'reset_index', inline='always', no_unliteral=True)
def overload_series_reset_index(S, level=None, drop=False, name=None,
    inplace=False):
    xjc__qmsn = dict(name=name, inplace=inplace)
    jrco__lxxs = dict(name=None, inplace=False)
    check_unsupported_args('Series.reset_index', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not bodo.hiframes.dataframe_impl._is_all_levels(S, level):
        raise_bodo_error(
            'Series.reset_index(): only dropping all index levels supported')
    if not is_overload_constant_bool(drop):
        raise_bodo_error(
            "Series.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if is_overload_true(drop):

        def impl_drop(S, level=None, drop=False, name=None, inplace=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_index_ext.init_range_index(0, len(arr),
                1, None)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
        return impl_drop

    def get_name_literal(name_typ, is_index=False, series_name=None):
        if is_overload_none(name_typ):
            if is_index:
                return 'index' if series_name != 'index' else 'level_0'
            return 0
        if is_literal_type(name_typ):
            return get_literal_value(name_typ)
        else:
            raise BodoError(
                'Series.reset_index() not supported for non-literal series names'
                )
    series_name = get_name_literal(S.name_typ)
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        gwfwz__lmnw = ', '.join(['index_arrs[{}]'.format(tys__niduj) for
            tys__niduj in range(S.index.nlevels)])
    else:
        gwfwz__lmnw = '    bodo.utils.conversion.index_to_array(index)\n'
    zltlr__nuh = 'index' if 'index' != series_name else 'level_0'
    areq__ats = get_index_names(S.index, 'Series.reset_index()', zltlr__nuh)
    columns = [name for name in areq__ats]
    columns.append(series_name)
    kld__zjlce = (
        'def _impl(S, level=None, drop=False, name=None, inplace=False):\n')
    kld__zjlce += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    kld__zjlce += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    if isinstance(S.index, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        kld__zjlce += (
            '    index_arrs = bodo.hiframes.pd_index_ext.get_index_data(index)\n'
            )
    kld__zjlce += """    df_index = bodo.hiframes.pd_index_ext.init_range_index(0, len(S), 1, None)
"""
    kld__zjlce += f"""    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({gwfwz__lmnw}, arr), df_index, __col_name_meta_value_series_reset_index)
"""
    ucijt__sjfar = {}
    exec(kld__zjlce, {'bodo': bodo,
        '__col_name_meta_value_series_reset_index': ColNamesMetaType(tuple(
        columns))}, ucijt__sjfar)
    eowel__yoluh = ucijt__sjfar['_impl']
    return eowel__yoluh


@overload_method(SeriesType, 'isna', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'isnull', inline='always', no_unliteral=True)
def overload_series_isna(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        fdno__fbd = bodo.libs.array_ops.array_op_isna(arr)
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index, name)
    return impl


@overload_method(SeriesType, 'round', inline='always', no_unliteral=True)
def overload_series_round(S, decimals=0):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.round()')

    def impl(S, decimals=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        fdno__fbd = bodo.utils.utils.alloc_type(n, arr, (-1,))
        for tys__niduj in numba.parfors.parfor.internal_prange(n):
            if pd.isna(arr[tys__niduj]):
                bodo.libs.array_kernels.setna(fdno__fbd, tys__niduj)
            else:
                fdno__fbd[tys__niduj] = np.round(arr[tys__niduj], decimals)
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index, name)
    return impl


@overload_method(SeriesType, 'sum', inline='always', no_unliteral=True)
def overload_series_sum(S, axis=None, skipna=True, level=None, numeric_only
    =None, min_count=0):
    xjc__qmsn = dict(level=level, numeric_only=numeric_only)
    jrco__lxxs = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sum', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.sum(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.sum(): skipna argument must be a boolean')
    if not is_overload_int(min_count):
        raise BodoError('Series.sum(): min_count argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.sum()'
        )

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_sum(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'prod', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'product', inline='always', no_unliteral=True)
def overload_series_prod(S, axis=None, skipna=True, level=None,
    numeric_only=None, min_count=0):
    xjc__qmsn = dict(level=level, numeric_only=numeric_only)
    jrco__lxxs = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.product', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.product(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.product(): skipna argument must be a boolean')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.product()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None,
        min_count=0):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_prod(arr, skipna, min_count)
    return impl


@overload_method(SeriesType, 'any', inline='always', no_unliteral=True)
def overload_series_any(S, axis=0, bool_only=None, skipna=True, level=None):
    xjc__qmsn = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=level
        )
    jrco__lxxs = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.any', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.any()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_any(A)
    return impl


@overload_method(SeriesType, 'equals', inline='always', no_unliteral=True)
def overload_series_equals(S, other):
    if not isinstance(other, SeriesType):
        raise BodoError("Series.equals() 'other' must be a Series")
    if isinstance(S.data, bodo.ArrayItemArrayType):
        raise BodoError(
            'Series.equals() not supported for Series where each element is an array or list'
            )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.equals()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.equals()')
    if S.data != other.data:
        return lambda S, other: False

    def impl(S, other):
        nrdnh__nttk = bodo.hiframes.pd_series_ext.get_series_data(S)
        kcdcs__xjmu = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        svr__oyarq = 0
        for tys__niduj in numba.parfors.parfor.internal_prange(len(nrdnh__nttk)
            ):
            frmcf__lqzc = 0
            imhut__yte = bodo.libs.array_kernels.isna(nrdnh__nttk, tys__niduj)
            hftu__plc = bodo.libs.array_kernels.isna(kcdcs__xjmu, tys__niduj)
            if imhut__yte and not hftu__plc or not imhut__yte and hftu__plc:
                frmcf__lqzc = 1
            elif not imhut__yte:
                if nrdnh__nttk[tys__niduj] != kcdcs__xjmu[tys__niduj]:
                    frmcf__lqzc = 1
            svr__oyarq += frmcf__lqzc
        return svr__oyarq == 0
    return impl


@overload_method(SeriesType, 'all', inline='always', no_unliteral=True)
def overload_series_all(S, axis=0, bool_only=None, skipna=True, level=None):
    xjc__qmsn = dict(axis=axis, bool_only=bool_only, skipna=skipna, level=level
        )
    jrco__lxxs = dict(axis=0, bool_only=None, skipna=True, level=None)
    check_unsupported_args('Series.all', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.all()'
        )

    def impl(S, axis=0, bool_only=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_all(A)
    return impl


@overload_method(SeriesType, 'mad', inline='always', no_unliteral=True)
def overload_series_mad(S, axis=None, skipna=True, level=None):
    xjc__qmsn = dict(level=level)
    jrco__lxxs = dict(level=None)
    check_unsupported_args('Series.mad', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(skipna):
        raise BodoError("Series.mad(): 'skipna' argument must be a boolean")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mad(): axis argument not supported')
    vyq__ucu = types.float64
    xds__omht = types.float64
    if S.dtype == types.float32:
        vyq__ucu = types.float32
        xds__omht = types.float32
    jtwn__urvk = vyq__ucu(0)
    dilmr__nrvmh = xds__omht(0)
    lhrws__qee = xds__omht(1)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.mad()'
        )

    def impl(S, axis=None, skipna=True, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        agpe__bdm = jtwn__urvk
        svr__oyarq = dilmr__nrvmh
        for tys__niduj in numba.parfors.parfor.internal_prange(len(A)):
            frmcf__lqzc = jtwn__urvk
            mxpmv__iifw = dilmr__nrvmh
            if not bodo.libs.array_kernels.isna(A, tys__niduj) or not skipna:
                frmcf__lqzc = A[tys__niduj]
                mxpmv__iifw = lhrws__qee
            agpe__bdm += frmcf__lqzc
            svr__oyarq += mxpmv__iifw
        lquua__mlrc = bodo.hiframes.series_kernels._mean_handle_nan(agpe__bdm,
            svr__oyarq)
        dexuu__llom = jtwn__urvk
        for tys__niduj in numba.parfors.parfor.internal_prange(len(A)):
            frmcf__lqzc = jtwn__urvk
            if not bodo.libs.array_kernels.isna(A, tys__niduj) or not skipna:
                frmcf__lqzc = abs(A[tys__niduj] - lquua__mlrc)
            dexuu__llom += frmcf__lqzc
        viz__ipufa = bodo.hiframes.series_kernels._mean_handle_nan(dexuu__llom,
            svr__oyarq)
        return viz__ipufa
    return impl


@overload_method(SeriesType, 'mean', inline='always', no_unliteral=True)
def overload_series_mean(S, axis=None, skipna=None, level=None,
    numeric_only=None):
    if not isinstance(S.dtype, types.Number) and S.dtype not in [bodo.
        datetime64ns, types.bool_]:
        raise BodoError(f"Series.mean(): Series with type '{S}' not supported")
    xjc__qmsn = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    jrco__lxxs = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.mean', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.mean(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.mean()')

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_mean(arr)
    return impl


@overload_method(SeriesType, 'sem', inline='always', no_unliteral=True)
def overload_series_sem(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    xjc__qmsn = dict(level=level, numeric_only=numeric_only)
    jrco__lxxs = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.sem', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.sem(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.sem(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.sem(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.sem()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        ngjpm__udm = 0
        hhckz__ujmiz = 0
        svr__oyarq = 0
        for tys__niduj in numba.parfors.parfor.internal_prange(len(A)):
            frmcf__lqzc = 0
            mxpmv__iifw = 0
            if not bodo.libs.array_kernels.isna(A, tys__niduj) or not skipna:
                frmcf__lqzc = A[tys__niduj]
                mxpmv__iifw = 1
            ngjpm__udm += frmcf__lqzc
            hhckz__ujmiz += frmcf__lqzc * frmcf__lqzc
            svr__oyarq += mxpmv__iifw
        atck__sghz = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            ngjpm__udm, hhckz__ujmiz, svr__oyarq, ddof)
        alm__ffwzs = bodo.hiframes.series_kernels._sem_handle_nan(atck__sghz,
            svr__oyarq)
        return alm__ffwzs
    return impl


@overload_method(SeriesType, 'kurt', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'kurtosis', inline='always', no_unliteral=True)
def overload_series_kurt(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    xjc__qmsn = dict(level=level, numeric_only=numeric_only)
    jrco__lxxs = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.kurtosis', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.kurtosis(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError(
            "Series.kurtosis(): 'skipna' argument must be a boolean")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.kurtosis()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        ngjpm__udm = 0.0
        hhckz__ujmiz = 0.0
        obuyv__qjcio = 0.0
        dhk__pwxge = 0.0
        svr__oyarq = 0
        for tys__niduj in numba.parfors.parfor.internal_prange(len(A)):
            frmcf__lqzc = 0.0
            mxpmv__iifw = 0
            if not bodo.libs.array_kernels.isna(A, tys__niduj) or not skipna:
                frmcf__lqzc = np.float64(A[tys__niduj])
                mxpmv__iifw = 1
            ngjpm__udm += frmcf__lqzc
            hhckz__ujmiz += frmcf__lqzc ** 2
            obuyv__qjcio += frmcf__lqzc ** 3
            dhk__pwxge += frmcf__lqzc ** 4
            svr__oyarq += mxpmv__iifw
        atck__sghz = bodo.hiframes.series_kernels.compute_kurt(ngjpm__udm,
            hhckz__ujmiz, obuyv__qjcio, dhk__pwxge, svr__oyarq)
        return atck__sghz
    return impl


@overload_method(SeriesType, 'skew', inline='always', no_unliteral=True)
def overload_series_skew(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    xjc__qmsn = dict(level=level, numeric_only=numeric_only)
    jrco__lxxs = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.skew', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.skew(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.skew(): skipna argument must be a boolean')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.skew()')

    def impl(S, axis=None, skipna=True, level=None, numeric_only=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        numba.parfors.parfor.init_prange()
        ngjpm__udm = 0.0
        hhckz__ujmiz = 0.0
        obuyv__qjcio = 0.0
        svr__oyarq = 0
        for tys__niduj in numba.parfors.parfor.internal_prange(len(A)):
            frmcf__lqzc = 0.0
            mxpmv__iifw = 0
            if not bodo.libs.array_kernels.isna(A, tys__niduj) or not skipna:
                frmcf__lqzc = np.float64(A[tys__niduj])
                mxpmv__iifw = 1
            ngjpm__udm += frmcf__lqzc
            hhckz__ujmiz += frmcf__lqzc ** 2
            obuyv__qjcio += frmcf__lqzc ** 3
            svr__oyarq += mxpmv__iifw
        atck__sghz = bodo.hiframes.series_kernels.compute_skew(ngjpm__udm,
            hhckz__ujmiz, obuyv__qjcio, svr__oyarq)
        return atck__sghz
    return impl


@overload_method(SeriesType, 'var', inline='always', no_unliteral=True)
def overload_series_var(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    xjc__qmsn = dict(level=level, numeric_only=numeric_only)
    jrco__lxxs = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.var', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.var(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.var(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.var(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.var()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_var(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'std', inline='always', no_unliteral=True)
def overload_series_std(S, axis=None, skipna=True, level=None, ddof=1,
    numeric_only=None):
    xjc__qmsn = dict(level=level, numeric_only=numeric_only)
    jrco__lxxs = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.std', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.std(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.std(): skipna argument must be a boolean')
    if not is_overload_int(ddof):
        raise BodoError('Series.std(): ddof argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.std()'
        )

    def impl(S, axis=None, skipna=True, level=None, ddof=1, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_std(arr, skipna, ddof)
    return impl


@overload_method(SeriesType, 'dot', inline='always', no_unliteral=True)
def overload_series_dot(S, other):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.dot()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.dot()')

    def impl(S, other):
        nrdnh__nttk = bodo.hiframes.pd_series_ext.get_series_data(S)
        kcdcs__xjmu = bodo.hiframes.pd_series_ext.get_series_data(other)
        numba.parfors.parfor.init_prange()
        baa__yud = 0
        for tys__niduj in numba.parfors.parfor.internal_prange(len(nrdnh__nttk)
            ):
            iamt__pth = nrdnh__nttk[tys__niduj]
            cylxj__ymwp = kcdcs__xjmu[tys__niduj]
            baa__yud += iamt__pth * cylxj__ymwp
        return baa__yud
    return impl


@overload_method(SeriesType, 'cumsum', inline='always', no_unliteral=True)
def overload_series_cumsum(S, axis=None, skipna=True):
    xjc__qmsn = dict(skipna=skipna)
    jrco__lxxs = dict(skipna=True)
    check_unsupported_args('Series.cumsum', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cumsum(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cumsum()')

    def impl(S, axis=None, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.accum_func(A, 'cumsum'), index, name)
    return impl


@overload_method(SeriesType, 'cumprod', inline='always', no_unliteral=True)
def overload_series_cumprod(S, axis=None, skipna=True):
    xjc__qmsn = dict(skipna=skipna)
    jrco__lxxs = dict(skipna=True)
    check_unsupported_args('Series.cumprod', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cumprod(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cumprod()')

    def impl(S, axis=None, skipna=True):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.accum_func(A, 'cumprod'), index, name)
    return impl


@overload_method(SeriesType, 'cummin', inline='always', no_unliteral=True)
def overload_series_cummin(S, axis=None, skipna=True):
    xjc__qmsn = dict(skipna=skipna)
    jrco__lxxs = dict(skipna=True)
    check_unsupported_args('Series.cummin', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cummin(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cummin()')

    def impl(S, axis=None, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.accum_func(arr, 'cummin'), index, name)
    return impl


@overload_method(SeriesType, 'cummax', inline='always', no_unliteral=True)
def overload_series_cummax(S, axis=None, skipna=True):
    xjc__qmsn = dict(skipna=skipna)
    jrco__lxxs = dict(skipna=True)
    check_unsupported_args('Series.cummax', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.cummax(): axis argument not supported')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.cummax()')

    def impl(S, axis=None, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
            array_kernels.accum_func(arr, 'cummax'), index, name)
    return impl


@overload_method(SeriesType, 'rename', inline='always', no_unliteral=True)
def overload_series_rename(S, index=None, axis=None, copy=True, inplace=
    False, level=None, errors='ignore'):
    if not (index == bodo.string_type or isinstance(index, types.StringLiteral)
        ):
        raise BodoError("Series.rename() 'index' can only be a string")
    xjc__qmsn = dict(copy=copy, inplace=inplace, level=level, errors=errors)
    jrco__lxxs = dict(copy=True, inplace=False, level=None, errors='ignore')
    check_unsupported_args('Series.rename', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')

    def impl(S, index=None, axis=None, copy=True, inplace=False, level=None,
        errors='ignore'):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        nvq__adge = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_series_ext.init_series(A, nvq__adge, index)
    return impl


@overload_method(SeriesType, 'rename_axis', inline='always', no_unliteral=True)
def overload_series_rename_axis(S, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False):
    xjc__qmsn = dict(index=index, columns=columns, axis=axis, copy=copy,
        inplace=inplace)
    jrco__lxxs = dict(index=None, columns=None, axis=None, copy=True,
        inplace=False)
    check_unsupported_args('Series.rename_axis', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if is_overload_none(mapper) or not is_scalar_type(mapper):
        raise BodoError(
            "Series.rename_axis(): 'mapper' is required and must be a scalar type."
            )

    def impl(S, mapper=None, index=None, columns=None, axis=None, copy=True,
        inplace=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        index = index.rename(mapper)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr, index, name)
    return impl


@overload_method(SeriesType, 'abs', inline='always', no_unliteral=True)
def overload_series_abs(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.abs()'
        )
    zgo__vxou = S.data

    def impl(S):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(A)
        fdno__fbd = bodo.utils.utils.alloc_type(n, zgo__vxou, (-1,))
        for tys__niduj in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, tys__niduj):
                bodo.libs.array_kernels.setna(fdno__fbd, tys__niduj)
                continue
            fdno__fbd[tys__niduj] = np.abs(A[tys__niduj])
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index, name)
    return impl


@overload_method(SeriesType, 'count', no_unliteral=True)
def overload_series_count(S, level=None):
    xjc__qmsn = dict(level=level)
    jrco__lxxs = dict(level=None)
    check_unsupported_args('Series.count', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')

    def impl(S, level=None):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_count(A)
    return impl


@overload_method(SeriesType, 'corr', inline='always', no_unliteral=True)
def overload_series_corr(S, other, method='pearson', min_periods=None):
    xjc__qmsn = dict(method=method, min_periods=min_periods)
    jrco__lxxs = dict(method='pearson', min_periods=None)
    check_unsupported_args('Series.corr', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.corr()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.corr()')

    def impl(S, other, method='pearson', min_periods=None):
        n = S.count()
        xksn__fuvy = S.sum()
        zrj__xpy = other.sum()
        a = n * (S * other).sum() - xksn__fuvy * zrj__xpy
        rkio__cncjp = n * (S ** 2).sum() - xksn__fuvy ** 2
        caceq__fuf = n * (other ** 2).sum() - zrj__xpy ** 2
        return a / np.sqrt(rkio__cncjp * caceq__fuf)
    return impl


@overload_method(SeriesType, 'cov', inline='always', no_unliteral=True)
def overload_series_cov(S, other, min_periods=None, ddof=1):
    xjc__qmsn = dict(min_periods=min_periods)
    jrco__lxxs = dict(min_periods=None)
    check_unsupported_args('Series.cov', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S, 'Series.cov()'
        )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'Series.cov()')

    def impl(S, other, min_periods=None, ddof=1):
        xksn__fuvy = S.mean()
        zrj__xpy = other.mean()
        srrc__qymfz = ((S - xksn__fuvy) * (other - zrj__xpy)).sum()
        N = np.float64(S.count() - ddof)
        nonzero_len = S.count() * other.count()
        return _series_cov_helper(srrc__qymfz, N, nonzero_len)
    return impl


def _series_cov_helper(sum_val, N, nonzero_len):
    return


@overload(_series_cov_helper, no_unliteral=True)
def _overload_series_cov_helper(sum_val, N, nonzero_len):

    def impl(sum_val, N, nonzero_len):
        if not nonzero_len:
            return np.nan
        if N <= 0.0:
            fye__bmtk = np.sign(sum_val)
            return np.inf * fye__bmtk
        return sum_val / N
    return impl


@overload_method(SeriesType, 'min', inline='always', no_unliteral=True)
def overload_series_min(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    xjc__qmsn = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    jrco__lxxs = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.min', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.min(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.min(): only ordered categoricals are possible')
    if isinstance(S.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype
        ):
        rfsf__gtd = S.dtype.tz

        def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
            arr = unwrap_tz_array(bodo.hiframes.pd_series_ext.
                get_series_data(S))
            min_val = bodo.libs.array_ops.array_op_min(arr)
            return convert_val_to_timestamp(min_val.value, tz=rfsf__gtd)
        return impl

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_min(arr)
    return impl


@overload(max, no_unliteral=True)
def overload_series_builtins_max(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.max()
        return impl


@overload(min, no_unliteral=True)
def overload_series_builtins_min(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.min()
        return impl


@overload(sum, no_unliteral=True)
def overload_series_builtins_sum(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.sum()
        return impl


@overload(np.prod, inline='always', no_unliteral=True)
def overload_series_np_prod(S):
    if isinstance(S, SeriesType):

        def impl(S):
            return S.prod()
        return impl


@overload_method(SeriesType, 'max', inline='always', no_unliteral=True)
def overload_series_max(S, axis=None, skipna=None, level=None, numeric_only
    =None):
    xjc__qmsn = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    jrco__lxxs = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('Series.max', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.max(): axis argument not supported')
    if isinstance(S.dtype, PDCategoricalDtype):
        if not S.dtype.ordered:
            raise BodoError(
                'Series.max(): only ordered categoricals are possible')
    if isinstance(S.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype
        ):
        rfsf__gtd = S.dtype.tz

        def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
            arr = unwrap_tz_array(bodo.hiframes.pd_series_ext.
                get_series_data(S))
            max_val = bodo.libs.array_ops.array_op_max(arr)
            return convert_val_to_timestamp(max_val.value, tz=rfsf__gtd)
        return impl

    def impl(S, axis=None, skipna=None, level=None, numeric_only=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_ops.array_op_max(arr)
    return impl


@overload_method(SeriesType, 'idxmin', inline='always', no_unliteral=True)
def overload_series_idxmin(S, axis=0, skipna=True):
    xjc__qmsn = dict(axis=axis, skipna=skipna)
    jrco__lxxs = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmin', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.idxmin()')
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.FloatingArrayType, bodo.
        CategoricalArrayType)) or S.data in [bodo.boolean_array, bodo.
        datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmin() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmin(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmin(arr, index)
    return impl


@overload_method(SeriesType, 'idxmax', inline='always', no_unliteral=True)
def overload_series_idxmax(S, axis=0, skipna=True):
    xjc__qmsn = dict(axis=axis, skipna=skipna)
    jrco__lxxs = dict(axis=0, skipna=True)
    check_unsupported_args('Series.idxmax', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.idxmax()')
    if not (S.dtype == types.none or bodo.utils.utils.is_np_array_typ(S.
        data) and (S.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
        isinstance(S.dtype, (types.Number, types.Boolean))) or isinstance(S
        .data, (bodo.IntegerArrayType, bodo.FloatingArrayType, bodo.
        CategoricalArrayType)) or S.data in [bodo.boolean_array, bodo.
        datetime_date_array_type]):
        raise BodoError(
            f'Series.idxmax() only supported for numeric array types. Array type: {S.data} not supported.'
            )
    if isinstance(S.data, bodo.CategoricalArrayType) and not S.dtype.ordered:
        raise BodoError(
            'Series.idxmax(): only ordered categoricals are possible')

    def impl(S, axis=0, skipna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.libs.array_ops.array_op_idxmax(arr, index)
    return impl


@overload_method(SeriesType, 'infer_objects', inline='always')
def overload_series_infer_objects(S):
    return lambda S: S.copy()


@overload_attribute(SeriesType, 'is_monotonic', inline='always')
@overload_attribute(SeriesType, 'is_monotonic_increasing', inline='always')
def overload_series_is_monotonic_increasing(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.is_monotonic_increasing')
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 1)


@overload_attribute(SeriesType, 'is_monotonic_decreasing', inline='always')
def overload_series_is_monotonic_decreasing(S):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.is_monotonic_decreasing')
    return lambda S: bodo.libs.array_kernels.series_monotonicity(bodo.
        hiframes.pd_series_ext.get_series_data(S), 2)


@overload_attribute(SeriesType, 'nbytes', inline='always')
def overload_series_nbytes(S):
    return lambda S: bodo.hiframes.pd_series_ext.get_series_data(S).nbytes


@overload_method(SeriesType, 'autocorr', inline='always', no_unliteral=True)
def overload_series_autocorr(S, lag=1):
    return lambda S, lag=1: bodo.libs.array_kernels.autocorr(bodo.hiframes.
        pd_series_ext.get_series_data(S), lag)


@overload_method(SeriesType, 'median', inline='always', no_unliteral=True)
def overload_series_median(S, axis=None, skipna=True, level=None,
    numeric_only=None):
    xjc__qmsn = dict(level=level, numeric_only=numeric_only)
    jrco__lxxs = dict(level=None, numeric_only=None)
    check_unsupported_args('Series.median', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.median(): axis argument not supported')
    if not is_overload_bool(skipna):
        raise BodoError('Series.median(): skipna argument must be a boolean')
    return (lambda S, axis=None, skipna=True, level=None, numeric_only=None:
        bodo.libs.array_ops.array_op_median(bodo.hiframes.pd_series_ext.
        get_series_data(S), skipna))


def overload_series_head(S, n=5):

    def impl(S, n=5):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        zobc__cays = arr[:n]
        pcunw__xud = index[:n]
        return bodo.hiframes.pd_series_ext.init_series(zobc__cays,
            pcunw__xud, name)
    return impl


@lower_builtin('series.head', SeriesType, types.Integer)
@lower_builtin('series.head', SeriesType, types.Omitted)
def series_head_lower(context, builder, sig, args):
    impl = overload_series_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@numba.extending.register_jitable
def tail_slice(k, n):
    if n == 0:
        return k
    return -n


@overload_method(SeriesType, 'tail', inline='always', no_unliteral=True)
def overload_series_tail(S, n=5):
    if not is_overload_int(n):
        raise BodoError("Series.tail(): 'n' must be an Integer")

    def impl(S, n=5):
        epec__iixwa = tail_slice(len(S), n)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        zobc__cays = arr[epec__iixwa:]
        pcunw__xud = index[epec__iixwa:]
        return bodo.hiframes.pd_series_ext.init_series(zobc__cays,
            pcunw__xud, name)
    return impl


@overload_method(SeriesType, 'first', inline='always', no_unliteral=True)
def overload_series_first(S, offset):
    vxh__ere = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in vxh__ere:
        raise BodoError(
            "Series.first(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.first()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            mluhp__bdibg = index[0]
            rcp__bowl = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                mluhp__bdibg, False))
        else:
            rcp__bowl = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        zobc__cays = arr[:rcp__bowl]
        pcunw__xud = index[:rcp__bowl]
        return bodo.hiframes.pd_series_ext.init_series(zobc__cays,
            pcunw__xud, name)
    return impl


@overload_method(SeriesType, 'last', inline='always', no_unliteral=True)
def overload_series_last(S, offset):
    vxh__ere = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if types.unliteral(offset) not in vxh__ere:
        raise BodoError(
            "Series.last(): 'offset' must be a string or a DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.last()')

    def impl(S, offset):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        if len(index):
            sri__kyshs = index[-1]
            rcp__bowl = (bodo.libs.array_kernels.
                get_valid_entries_from_date_offset(index, offset,
                sri__kyshs, True))
        else:
            rcp__bowl = 0
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        zobc__cays = arr[len(arr) - rcp__bowl:]
        pcunw__xud = index[len(arr) - rcp__bowl:]
        return bodo.hiframes.pd_series_ext.init_series(zobc__cays,
            pcunw__xud, name)
    return impl


@overload_method(SeriesType, 'first_valid_index', inline='always',
    no_unliteral=True)
def overload_series_first_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        wldxr__prmbi = bodo.utils.conversion.index_to_array(index)
        rizck__dpcg, nejhy__ncho = (bodo.libs.array_kernels.
            first_last_valid_index(arr, wldxr__prmbi))
        return nejhy__ncho if rizck__dpcg else None
    return impl


@overload_method(SeriesType, 'last_valid_index', inline='always',
    no_unliteral=True)
def overload_series_last_valid_index(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        wldxr__prmbi = bodo.utils.conversion.index_to_array(index)
        rizck__dpcg, nejhy__ncho = (bodo.libs.array_kernels.
            first_last_valid_index(arr, wldxr__prmbi, False))
        return nejhy__ncho if rizck__dpcg else None
    return impl


@overload_method(SeriesType, 'nlargest', inline='always', no_unliteral=True)
def overload_series_nlargest(S, n=5, keep='first'):
    xjc__qmsn = dict(keep=keep)
    jrco__lxxs = dict(keep='first')
    check_unsupported_args('Series.nlargest', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nlargest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nlargest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        wldxr__prmbi = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        fdno__fbd, guyb__wtuo = bodo.libs.array_kernels.nlargest(arr,
            wldxr__prmbi, n, True, bodo.hiframes.series_kernels.gt_f)
        ngbtj__job = bodo.utils.conversion.convert_to_index(guyb__wtuo)
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
            ngbtj__job, name)
    return impl


@overload_method(SeriesType, 'nsmallest', inline='always', no_unliteral=True)
def overload_series_nsmallest(S, n=5, keep='first'):
    xjc__qmsn = dict(keep=keep)
    jrco__lxxs = dict(keep='first')
    check_unsupported_args('Series.nsmallest', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not is_overload_int(n):
        raise BodoError('Series.nsmallest(): n argument must be an integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.nsmallest()')

    def impl(S, n=5, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        wldxr__prmbi = bodo.utils.conversion.coerce_to_ndarray(index)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        fdno__fbd, guyb__wtuo = bodo.libs.array_kernels.nlargest(arr,
            wldxr__prmbi, n, False, bodo.hiframes.series_kernels.lt_f)
        ngbtj__job = bodo.utils.conversion.convert_to_index(guyb__wtuo)
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
            ngbtj__job, name)
    return impl


@overload_method(SeriesType, 'notnull', inline='always', no_unliteral=True)
@overload_method(SeriesType, 'notna', inline='always', no_unliteral=True)
def overload_series_notna(S):
    return lambda S: S.isna() == False


@overload_method(SeriesType, 'astype', inline='always', no_unliteral=True)
@overload_method(HeterogeneousSeriesType, 'astype', inline='always',
    no_unliteral=True)
def overload_series_astype(S, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True):
    xjc__qmsn = dict(errors=errors)
    jrco__lxxs = dict(errors='raise')
    check_unsupported_args('Series.astype', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "Series.astype(): 'dtype' when passed as string must be a constant value"
            )
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.astype()')

    def impl(S, dtype, copy=True, errors='raise', _bodo_nan_to_str=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        fdno__fbd = bodo.utils.conversion.fix_arr_dtype(arr, dtype, copy,
            nan_to_str=_bodo_nan_to_str, from_series=True)
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index, name)
    return impl


@overload_method(SeriesType, 'take', inline='always', no_unliteral=True)
def overload_series_take(S, indices, axis=0, is_copy=True):
    xjc__qmsn = dict(axis=axis, is_copy=is_copy)
    jrco__lxxs = dict(axis=0, is_copy=True)
    check_unsupported_args('Series.take', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not (is_iterable_type(indices) and isinstance(indices.dtype, types.
        Integer)):
        raise BodoError(
            f"Series.take() 'indices' must be an array-like and contain integers. Found type {indices}."
            )

    def impl(S, indices, axis=0, is_copy=True):
        ozrr__oqzl = bodo.utils.conversion.coerce_to_ndarray(indices)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(arr[ozrr__oqzl],
            index[ozrr__oqzl], name)
    return impl


@overload_method(SeriesType, 'argsort', inline='always', no_unliteral=True)
def overload_series_argsort(S, axis=0, kind='quicksort', order=None):
    xjc__qmsn = dict(axis=axis, kind=kind, order=order)
    jrco__lxxs = dict(axis=0, kind='quicksort', order=None)
    check_unsupported_args('Series.argsort', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')

    def impl(S, axis=0, kind='quicksort', order=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        n = len(arr)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        tqw__pdyp = S.notna().values
        if not tqw__pdyp.all():
            fdno__fbd = np.full(n, -1, np.int64)
            fdno__fbd[tqw__pdyp] = argsort(arr[tqw__pdyp])
        else:
            fdno__fbd = argsort(arr)
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index, name)
    return impl


@overload_method(SeriesType, 'rank', inline='always', no_unliteral=True)
def overload_series_rank(S, axis=0, method='average', numeric_only=None,
    na_option='keep', ascending=True, pct=False):
    xjc__qmsn = dict(axis=axis, numeric_only=numeric_only)
    jrco__lxxs = dict(axis=0, numeric_only=None)
    check_unsupported_args('Series.rank', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not is_overload_constant_str(method):
        raise BodoError(
            "Series.rank(): 'method' argument must be a constant string")
    if not is_overload_constant_str(na_option):
        raise BodoError(
            "Series.rank(): 'na_option' argument must be a constant string")

    def impl(S, axis=0, method='average', numeric_only=None, na_option=
        'keep', ascending=True, pct=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        fdno__fbd = bodo.libs.array_kernels.rank(arr, method=method,
            na_option=na_option, ascending=ascending, pct=pct)
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index, name)
    return impl


@overload_method(SeriesType, 'sort_index', inline='always', no_unliteral=True)
def overload_series_sort_index(S, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    xjc__qmsn = dict(axis=axis, level=level, inplace=inplace, kind=kind,
        sort_remaining=sort_remaining, ignore_index=ignore_index, key=key)
    jrco__lxxs = dict(axis=0, level=None, inplace=False, kind='quicksort',
        sort_remaining=True, ignore_index=False, key=None)
    check_unsupported_args('Series.sort_index', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_index(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_index(): 'na_position' should either be 'first' or 'last'"
            )
    jhp__ouxhs = ColNamesMetaType(('$_bodo_col3_',))

    def impl(S, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        xhyvg__ctg = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, jhp__ouxhs)
        dcrs__xgk = xhyvg__ctg.sort_index(ascending=ascending, inplace=
            inplace, na_position=na_position)
        fdno__fbd = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(dcrs__xgk
            , 0)
        ngbtj__job = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            dcrs__xgk)
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
            ngbtj__job, name)
    return impl


@overload_method(SeriesType, 'sort_values', inline='always', no_unliteral=True)
def overload_series_sort_values(S, axis=0, ascending=True, inplace=False,
    kind='quicksort', na_position='last', ignore_index=False, key=None):
    xjc__qmsn = dict(axis=axis, inplace=inplace, kind=kind, ignore_index=
        ignore_index, key=key)
    jrco__lxxs = dict(axis=0, inplace=False, kind='quicksort', ignore_index
        =False, key=None)
    check_unsupported_args('Series.sort_values', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not is_overload_bool(ascending):
        raise BodoError(
            "Series.sort_values(): 'ascending' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "Series.sort_values(): 'na_position' should either be 'first' or 'last'"
            )
    yzrae__dvs = ColNamesMetaType(('$_bodo_col_',))

    def impl(S, axis=0, ascending=True, inplace=False, kind='quicksort',
        na_position='last', ignore_index=False, key=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        xhyvg__ctg = bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,),
            index, yzrae__dvs)
        dcrs__xgk = xhyvg__ctg.sort_values(['$_bodo_col_'], ascending=
            ascending, inplace=inplace, na_position=na_position)
        fdno__fbd = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(dcrs__xgk
            , 0)
        ngbtj__job = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(
            dcrs__xgk)
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
            ngbtj__job, name)
    return impl


def get_bin_inds(bins, arr):
    return arr


@overload(get_bin_inds, inline='always', no_unliteral=True)
def overload_get_bin_inds(bins, arr, is_nullable=True, include_lowest=True):
    assert is_overload_constant_bool(is_nullable)
    loxny__gdg = is_overload_true(is_nullable)
    kld__zjlce = (
        'def impl(bins, arr, is_nullable=True, include_lowest=True):\n')
    kld__zjlce += '  numba.parfors.parfor.init_prange()\n'
    kld__zjlce += '  n = len(arr)\n'
    if loxny__gdg:
        kld__zjlce += (
            '  out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
    else:
        kld__zjlce += '  out_arr = np.empty(n, np.int64)\n'
    kld__zjlce += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    kld__zjlce += '    if bodo.libs.array_kernels.isna(arr, i):\n'
    if loxny__gdg:
        kld__zjlce += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        kld__zjlce += '      out_arr[i] = -1\n'
    kld__zjlce += '      continue\n'
    kld__zjlce += '    val = arr[i]\n'
    kld__zjlce += '    if include_lowest and val == bins[0]:\n'
    kld__zjlce += '      ind = 1\n'
    kld__zjlce += '    else:\n'
    kld__zjlce += '      ind = np.searchsorted(bins, val)\n'
    kld__zjlce += '    if ind == 0 or ind == len(bins):\n'
    if loxny__gdg:
        kld__zjlce += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    else:
        kld__zjlce += '      out_arr[i] = -1\n'
    kld__zjlce += '    else:\n'
    kld__zjlce += '      out_arr[i] = ind - 1\n'
    kld__zjlce += '  return out_arr\n'
    ucijt__sjfar = {}
    exec(kld__zjlce, {'bodo': bodo, 'np': np, 'numba': numba}, ucijt__sjfar)
    impl = ucijt__sjfar['impl']
    return impl


@register_jitable
def _round_frac(x, precision: int):
    if not np.isfinite(x) or x == 0:
        return x
    else:
        jis__smyym, cfu__nmnij = np.divmod(x, 1)
        if jis__smyym == 0:
            usi__umgi = -int(np.floor(np.log10(abs(cfu__nmnij)))
                ) - 1 + precision
        else:
            usi__umgi = precision
        return np.around(x, usi__umgi)


@register_jitable
def _infer_precision(base_precision: int, bins) ->int:
    for precision in range(base_precision, 20):
        szul__sdwe = np.array([_round_frac(b, precision) for b in bins])
        if len(np.unique(szul__sdwe)) == len(bins):
            return precision
    return base_precision


def get_bin_labels(bins):
    pass


@overload(get_bin_labels, no_unliteral=True)
def overload_get_bin_labels(bins, right=True, include_lowest=True):
    dtype = np.float64 if isinstance(bins.dtype, types.Integer) else bins.dtype
    if dtype == bodo.datetime64ns:
        rpth__fiufg = bodo.timedelta64ns(1)

        def impl_dt64(bins, right=True, include_lowest=True):
            hwh__gkn = bins.copy()
            if right and include_lowest:
                hwh__gkn[0] = hwh__gkn[0] - rpth__fiufg
            wirwh__crd = bodo.libs.interval_arr_ext.init_interval_array(
                hwh__gkn[:-1], hwh__gkn[1:])
            return bodo.hiframes.pd_index_ext.init_interval_index(wirwh__crd,
                None)
        return impl_dt64

    def impl(bins, right=True, include_lowest=True):
        base_precision = 3
        precision = _infer_precision(base_precision, bins)
        hwh__gkn = np.array([_round_frac(b, precision) for b in bins],
            dtype=dtype)
        if right and include_lowest:
            hwh__gkn[0] = hwh__gkn[0] - 10.0 ** -precision
        wirwh__crd = bodo.libs.interval_arr_ext.init_interval_array(hwh__gkn
            [:-1], hwh__gkn[1:])
        return bodo.hiframes.pd_index_ext.init_interval_index(wirwh__crd, None)
    return impl


def get_output_bin_counts(count_series, nbins):
    pass


@overload(get_output_bin_counts, no_unliteral=True)
def overload_get_output_bin_counts(count_series, nbins):

    def impl(count_series, nbins):
        wwo__vjy = bodo.hiframes.pd_series_ext.get_series_data(count_series)
        kvete__gues = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(count_series))
        fdno__fbd = np.zeros(nbins, np.int64)
        for tys__niduj in range(len(wwo__vjy)):
            fdno__fbd[kvete__gues[tys__niduj]] = wwo__vjy[tys__niduj]
        return fdno__fbd
    return impl


def compute_bins(nbins, min_val, max_val):
    pass


@overload(compute_bins, no_unliteral=True)
def overload_compute_bins(nbins, min_val, max_val, right=True):

    def impl(nbins, min_val, max_val, right=True):
        if nbins < 1:
            raise ValueError('`bins` should be a positive integer.')
        min_val = min_val + 0.0
        max_val = max_val + 0.0
        if np.isinf(min_val) or np.isinf(max_val):
            raise ValueError(
                'cannot specify integer `bins` when input data contains infinity'
                )
        elif min_val == max_val:
            min_val -= 0.001 * abs(min_val) if min_val != 0 else 0.001
            max_val += 0.001 * abs(max_val) if max_val != 0 else 0.001
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
        else:
            bins = np.linspace(min_val, max_val, nbins + 1, endpoint=True)
            vfu__azh = (max_val - min_val) * 0.001
            if right:
                bins[0] -= vfu__azh
            else:
                bins[-1] += vfu__azh
        return bins
    return impl


@overload_method(SeriesType, 'value_counts', inline='always', no_unliteral=True
    )
def overload_series_value_counts(S, normalize=False, sort=True, ascending=
    False, bins=None, dropna=True, _index_name=None):
    xjc__qmsn = dict(dropna=dropna)
    jrco__lxxs = dict(dropna=True)
    check_unsupported_args('Series.value_counts', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not is_overload_constant_bool(normalize):
        raise_bodo_error(
            'Series.value_counts(): normalize argument must be a constant boolean'
            )
    if not is_overload_constant_bool(sort):
        raise_bodo_error(
            'Series.value_counts(): sort argument must be a constant boolean')
    if not is_overload_bool(ascending):
        raise_bodo_error(
            'Series.value_counts(): ascending argument must be a constant boolean'
            )
    cfxdf__iysbn = not is_overload_none(bins)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.value_counts()')
    kld__zjlce = 'def impl(\n'
    kld__zjlce += '    S,\n'
    kld__zjlce += '    normalize=False,\n'
    kld__zjlce += '    sort=True,\n'
    kld__zjlce += '    ascending=False,\n'
    kld__zjlce += '    bins=None,\n'
    kld__zjlce += '    dropna=True,\n'
    kld__zjlce += (
        '    _index_name=None,  # bodo argument. See groupby.value_counts\n')
    kld__zjlce += '):\n'
    kld__zjlce += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    kld__zjlce += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    kld__zjlce += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    if cfxdf__iysbn:
        kld__zjlce += '    right = True\n'
        kld__zjlce += _gen_bins_handling(bins, S.dtype)
        kld__zjlce += '    arr = get_bin_inds(bins, arr)\n'
    kld__zjlce += (
        '    in_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
    kld__zjlce += (
        '        (arr,), index, __col_name_meta_value_series_value_counts\n')
    kld__zjlce += '    )\n'
    kld__zjlce += "    count_series = in_df.groupby('$_bodo_col2_').size()\n"
    if cfxdf__iysbn:
        kld__zjlce += """    count_series = bodo.gatherv(count_series, allgather=True, warn_if_rep=False)
"""
        kld__zjlce += (
            '    count_arr = get_output_bin_counts(count_series, len(bins) - 1)\n'
            )
        kld__zjlce += '    index = get_bin_labels(bins)\n'
    else:
        kld__zjlce += (
            '    count_arr = bodo.hiframes.pd_series_ext.get_series_data(count_series)\n'
            )
        kld__zjlce += '    ind_arr = bodo.utils.conversion.coerce_to_array(\n'
        kld__zjlce += (
            '        bodo.hiframes.pd_series_ext.get_series_index(count_series)\n'
            )
        kld__zjlce += '    )\n'
        kld__zjlce += """    index = bodo.utils.conversion.index_from_array(ind_arr, name=_index_name)
"""
    kld__zjlce += (
        '    res = bodo.hiframes.pd_series_ext.init_series(count_arr, index, name)\n'
        )
    if is_overload_true(sort):
        kld__zjlce += '    res = res.sort_values(ascending=ascending)\n'
    if is_overload_true(normalize):
        otcnv__qse = 'len(S)' if cfxdf__iysbn else 'count_arr.sum()'
        kld__zjlce += f'    res = res / float({otcnv__qse})\n'
    kld__zjlce += '    return res\n'
    ucijt__sjfar = {}
    exec(kld__zjlce, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins, '__col_name_meta_value_series_value_counts':
        ColNamesMetaType(('$_bodo_col2_',))}, ucijt__sjfar)
    impl = ucijt__sjfar['impl']
    return impl


def _gen_bins_handling(bins, dtype):
    kld__zjlce = ''
    if isinstance(bins, types.Integer):
        kld__zjlce += '    min_val = bodo.libs.array_ops.array_op_min(arr)\n'
        kld__zjlce += '    max_val = bodo.libs.array_ops.array_op_max(arr)\n'
        if dtype == bodo.datetime64ns:
            kld__zjlce += '    min_val = min_val.value\n'
            kld__zjlce += '    max_val = max_val.value\n'
        kld__zjlce += (
            '    bins = compute_bins(bins, min_val, max_val, right)\n')
        if dtype == bodo.datetime64ns:
            kld__zjlce += (
                "    bins = bins.astype(np.int64).view(np.dtype('datetime64[ns]'))\n"
                )
    else:
        kld__zjlce += (
            '    bins = bodo.utils.conversion.coerce_to_ndarray(bins)\n')
    return kld__zjlce


@overload(pd.cut, inline='always', no_unliteral=True)
def overload_cut(x, bins, right=True, labels=None, retbins=False, precision
    =3, include_lowest=False, duplicates='raise', ordered=True):
    xjc__qmsn = dict(right=right, labels=labels, retbins=retbins, precision
        =precision, duplicates=duplicates, ordered=ordered)
    jrco__lxxs = dict(right=True, labels=None, retbins=False, precision=3,
        duplicates='raise', ordered=True)
    check_unsupported_args('pandas.cut', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='General')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x, 'pandas.cut()'
        )
    kld__zjlce = 'def impl(\n'
    kld__zjlce += '    x,\n'
    kld__zjlce += '    bins,\n'
    kld__zjlce += '    right=True,\n'
    kld__zjlce += '    labels=None,\n'
    kld__zjlce += '    retbins=False,\n'
    kld__zjlce += '    precision=3,\n'
    kld__zjlce += '    include_lowest=False,\n'
    kld__zjlce += "    duplicates='raise',\n"
    kld__zjlce += '    ordered=True\n'
    kld__zjlce += '):\n'
    if isinstance(x, SeriesType):
        kld__zjlce += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(x)\n')
        kld__zjlce += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(x)\n')
        kld__zjlce += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(x)\n')
    else:
        kld__zjlce += '    arr = bodo.utils.conversion.coerce_to_array(x)\n'
    kld__zjlce += _gen_bins_handling(bins, x.dtype)
    kld__zjlce += '    arr = get_bin_inds(bins, arr, False, include_lowest)\n'
    kld__zjlce += (
        '    label_index = get_bin_labels(bins, right, include_lowest)\n')
    kld__zjlce += """    cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(label_index, ordered, None, None)
"""
    kld__zjlce += """    out_arr = bodo.hiframes.pd_categorical_ext.init_categorical_array(arr, cat_dtype)
"""
    if isinstance(x, SeriesType):
        kld__zjlce += (
            '    res = bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        kld__zjlce += '    return res\n'
    else:
        kld__zjlce += '    return out_arr\n'
    ucijt__sjfar = {}
    exec(kld__zjlce, {'bodo': bodo, 'pd': pd, 'np': np, 'get_bin_inds':
        get_bin_inds, 'get_bin_labels': get_bin_labels,
        'get_output_bin_counts': get_output_bin_counts, 'compute_bins':
        compute_bins}, ucijt__sjfar)
    impl = ucijt__sjfar['impl']
    return impl


def _get_q_list(q):
    return q


@overload(_get_q_list, no_unliteral=True)
def get_q_list_overload(q):
    if is_overload_int(q):
        return lambda q: np.linspace(0, 1, q + 1)
    return lambda q: q


@overload(pd.unique, inline='always', no_unliteral=True)
def overload_unique(values):
    if not is_series_type(values) and not (bodo.utils.utils.is_array_typ(
        values, False) and values.ndim == 1):
        raise BodoError(
            "pd.unique(): 'values' must be either a Series or a 1-d array")
    if is_series_type(values):

        def impl(values):
            arr = bodo.hiframes.pd_series_ext.get_series_data(values)
            return bodo.allgatherv(bodo.libs.array_kernels.unique(arr), False)
        return impl
    else:
        return lambda values: bodo.allgatherv(bodo.libs.array_kernels.
            unique(values), False)


@overload(pd.qcut, inline='always', no_unliteral=True)
def overload_qcut(x, q, labels=None, retbins=False, precision=3, duplicates
    ='raise'):
    xjc__qmsn = dict(labels=labels, retbins=retbins, precision=precision,
        duplicates=duplicates)
    jrco__lxxs = dict(labels=None, retbins=False, precision=3, duplicates=
        'raise')
    check_unsupported_args('pandas.qcut', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='General')
    if not (is_overload_int(q) or is_iterable_type(q)):
        raise BodoError(
            "pd.qcut(): 'q' should be an integer or a list of quantiles")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'pandas.qcut()')

    def impl(x, q, labels=None, retbins=False, precision=3, duplicates='raise'
        ):
        mka__ryllw = _get_q_list(q)
        arr = bodo.utils.conversion.coerce_to_array(x)
        bins = bodo.libs.array_ops.array_op_quantile(arr, mka__ryllw)
        return pd.cut(x, bins, include_lowest=True)
    return impl


@overload_method(SeriesType, 'groupby', inline='always', no_unliteral=True)
def overload_series_groupby(S, by=None, axis=0, level=None, as_index=True,
    sort=True, group_keys=True, squeeze=False, observed=True, dropna=True):
    xjc__qmsn = dict(axis=axis, sort=sort, group_keys=group_keys, squeeze=
        squeeze, observed=observed, dropna=dropna)
    jrco__lxxs = dict(axis=0, sort=True, group_keys=True, squeeze=False,
        observed=True, dropna=True)
    check_unsupported_args('Series.groupby', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='GroupBy')
    if not is_overload_true(as_index):
        raise BodoError('as_index=False only valid with DataFrame')
    if is_overload_none(by) and is_overload_none(level):
        raise BodoError("You have to supply one of 'by' and 'level'")
    if not is_overload_none(by) and not is_overload_none(level):
        raise BodoError(
            "Series.groupby(): 'level' argument should be None if 'by' is not None"
            )
    if not is_overload_none(level):
        if not (is_overload_constant_int(level) and get_overload_const_int(
            level) == 0) or isinstance(S.index, bodo.hiframes.
            pd_multi_index_ext.MultiIndexType):
            raise BodoError(
                "Series.groupby(): MultiIndex case or 'level' other than 0 not supported yet"
                )
        zef__roeut = ColNamesMetaType((' ', ''))

        def impl_index(S, by=None, axis=0, level=None, as_index=True, sort=
            True, group_keys=True, squeeze=False, observed=True, dropna=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            dfsp__ylhpq = bodo.utils.conversion.coerce_to_array(index)
            xhyvg__ctg = bodo.hiframes.pd_dataframe_ext.init_dataframe((
                dfsp__ylhpq, arr), index, zef__roeut)
            return xhyvg__ctg.groupby(' ')['']
        return impl_index
    nmnbc__hkdd = by
    if isinstance(by, SeriesType):
        nmnbc__hkdd = by.data
    if isinstance(nmnbc__hkdd, DecimalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with decimal type is not supported yet.'
            )
    if isinstance(by, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        raise BodoError(
            'Series.groupby(): by argument with categorical type is not supported yet.'
            )
    wspkw__kzyd = ColNamesMetaType((' ', ''))

    def impl(S, by=None, axis=0, level=None, as_index=True, sort=True,
        group_keys=True, squeeze=False, observed=True, dropna=True):
        dfsp__ylhpq = bodo.utils.conversion.coerce_to_array(by)
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        xhyvg__ctg = bodo.hiframes.pd_dataframe_ext.init_dataframe((
            dfsp__ylhpq, arr), index, wspkw__kzyd)
        return xhyvg__ctg.groupby(' ')['']
    return impl


@overload_method(SeriesType, 'append', inline='always', no_unliteral=True)
def overload_series_append(S, to_append, ignore_index=False,
    verify_integrity=False):
    xjc__qmsn = dict(verify_integrity=verify_integrity)
    jrco__lxxs = dict(verify_integrity=False)
    check_unsupported_args('Series.append', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(to_append,
        'Series.append()')
    if isinstance(to_append, SeriesType):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S, to_append), ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    if isinstance(to_append, types.BaseTuple):
        return (lambda S, to_append, ignore_index=False, verify_integrity=
            False: pd.concat((S,) + to_append, ignore_index=ignore_index,
            verify_integrity=verify_integrity))
    return (lambda S, to_append, ignore_index=False, verify_integrity=False:
        pd.concat([S] + to_append, ignore_index=ignore_index,
        verify_integrity=verify_integrity))


@overload_method(SeriesType, 'isin', inline='always', no_unliteral=True)
def overload_series_isin(S, values):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.isin()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(values,
        'Series.isin()')
    if bodo.utils.utils.is_array_typ(values):

        def impl_arr(S, values):
            wuhq__zswfl = bodo.utils.conversion.coerce_to_array(values)
            A = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(A)
            fdno__fbd = np.empty(n, np.bool_)
            bodo.libs.array.array_isin(fdno__fbd, A, wuhq__zswfl, False)
            return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index,
                name)
        return impl_arr
    if not isinstance(values, (types.Set, types.List)):
        raise BodoError(
            "Series.isin(): 'values' parameter should be a set or a list")

    def impl(S, values):
        A = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        fdno__fbd = bodo.libs.array_ops.array_op_isin(A, values)
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index, name)
    return impl


@overload_method(SeriesType, 'quantile', inline='always', no_unliteral=True)
def overload_series_quantile(S, q=0.5, interpolation='linear'):
    xjc__qmsn = dict(interpolation=interpolation)
    jrco__lxxs = dict(interpolation='linear')
    check_unsupported_args('Series.quantile', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.quantile()')
    if is_iterable_type(q) and isinstance(q.dtype, types.Number):

        def impl_list(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            fdno__fbd = bodo.libs.array_ops.array_op_quantile(arr, q)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            index = bodo.hiframes.pd_index_ext.init_numeric_index(bodo.
                utils.conversion.coerce_to_array(q), None)
            return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index,
                name)
        return impl_list
    elif isinstance(q, (float, types.Number)) or is_overload_constant_int(q):

        def impl(S, q=0.5, interpolation='linear'):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return bodo.libs.array_ops.array_op_quantile(arr, q)
        return impl
    else:
        raise BodoError(
            f'Series.quantile() q type must be float or iterable of floats only.'
            )


@overload_method(SeriesType, 'nunique', inline='always', no_unliteral=True)
def overload_series_nunique(S, dropna=True):
    if not is_overload_bool(dropna):
        raise BodoError('Series.nunique: dropna must be a boolean value')

    def impl(S, dropna=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        return bodo.libs.array_kernels.nunique(arr, dropna)
    return impl


@overload_method(SeriesType, 'unique', inline='always', no_unliteral=True)
def overload_series_unique(S):

    def impl(S):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        kbv__tkee = bodo.libs.array_kernels.unique(arr)
        return bodo.allgatherv(kbv__tkee, False)
    return impl


@overload_method(SeriesType, 'describe', inline='always', no_unliteral=True)
def overload_series_describe(S, percentiles=None, include=None, exclude=
    None, datetime_is_numeric=True):
    xjc__qmsn = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    jrco__lxxs = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('Series.describe', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.describe()')
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)
        ) and not isinstance(S.data, (IntegerArrayType, FloatingArrayType)):
        raise BodoError(f'describe() column input type {S.data} not supported.'
            )
    if S.data.dtype == bodo.datetime64ns:

        def impl_dt(S, percentiles=None, include=None, exclude=None,
            datetime_is_numeric=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(bodo.libs.
                array_ops.array_op_describe(arr), bodo.utils.conversion.
                convert_to_index(['count', 'mean', 'min', '25%', '50%',
                '75%', 'max']), name)
        return impl_dt

    def impl(S, percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        return bodo.hiframes.pd_series_ext.init_series(bodo.libs.array_ops.
            array_op_describe(arr), bodo.utils.conversion.convert_to_index(
            ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']), name)
    return impl


@overload_method(SeriesType, 'memory_usage', inline='always', no_unliteral=True
    )
def overload_series_memory_usage(S, index=True, deep=False):
    if is_overload_true(index):

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            return arr.nbytes + index.nbytes
        return impl
    else:

        def impl(S, index=True, deep=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            return arr.nbytes
        return impl


def binary_str_fillna_inplace_series_impl(is_binary=False):
    if is_binary:
        xuck__ccik = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        xuck__ccik = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    kld__zjlce = '\n'.join(('def impl(', '    S,', '    value=None,',
        '    method=None,', '    axis=None,', '    inplace=False,',
        '    limit=None,', '    downcast=None,', '):',
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)',
        '    fill_arr = bodo.hiframes.pd_series_ext.get_series_data(value)',
        '    n = len(in_arr)', '    nf = len(fill_arr)',
        "    assert n == nf, 'fillna() requires same length arrays'",
        f'    out_arr = {xuck__ccik}(n, -1)',
        '    for j in numba.parfors.parfor.internal_prange(n):',
        '        s = in_arr[j]',
        '        if bodo.libs.array_kernels.isna(in_arr, j) and not bodo.libs.array_kernels.isna('
        , '            fill_arr, j', '        ):',
        '            s = fill_arr[j]', '        out_arr[j] = s',
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)'
        ))
    ebdl__vtp = dict()
    exec(kld__zjlce, {'bodo': bodo, 'numba': numba}, ebdl__vtp)
    gfx__qelj = ebdl__vtp['impl']
    return gfx__qelj


def binary_str_fillna_inplace_impl(is_binary=False):
    if is_binary:
        xuck__ccik = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
    else:
        xuck__ccik = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
    kld__zjlce = 'def impl(S,\n'
    kld__zjlce += '     value=None,\n'
    kld__zjlce += '    method=None,\n'
    kld__zjlce += '    axis=None,\n'
    kld__zjlce += '    inplace=False,\n'
    kld__zjlce += '    limit=None,\n'
    kld__zjlce += '   downcast=None,\n'
    kld__zjlce += '):\n'
    kld__zjlce += (
        '    in_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    kld__zjlce += '    n = len(in_arr)\n'
    kld__zjlce += f'    out_arr = {xuck__ccik}(n, -1)\n'
    kld__zjlce += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    kld__zjlce += '        s = in_arr[j]\n'
    kld__zjlce += '        if bodo.libs.array_kernels.isna(in_arr, j):\n'
    kld__zjlce += '            s = value\n'
    kld__zjlce += '        out_arr[j] = s\n'
    kld__zjlce += (
        '    bodo.libs.str_arr_ext.move_str_binary_arr_payload(in_arr, out_arr)\n'
        )
    ebdl__vtp = dict()
    exec(kld__zjlce, {'bodo': bodo, 'numba': numba}, ebdl__vtp)
    gfx__qelj = ebdl__vtp['impl']
    return gfx__qelj


def fillna_inplace_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    rpcrf__knhay = bodo.hiframes.pd_series_ext.get_series_data(S)
    nug__bjney = bodo.hiframes.pd_series_ext.get_series_data(value)
    for tys__niduj in numba.parfors.parfor.internal_prange(len(rpcrf__knhay)):
        s = rpcrf__knhay[tys__niduj]
        if bodo.libs.array_kernels.isna(rpcrf__knhay, tys__niduj
            ) and not bodo.libs.array_kernels.isna(nug__bjney, tys__niduj):
            s = nug__bjney[tys__niduj]
        rpcrf__knhay[tys__niduj] = s


def fillna_inplace_impl(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    rpcrf__knhay = bodo.hiframes.pd_series_ext.get_series_data(S)
    for tys__niduj in numba.parfors.parfor.internal_prange(len(rpcrf__knhay)):
        s = rpcrf__knhay[tys__niduj]
        if bodo.libs.array_kernels.isna(rpcrf__knhay, tys__niduj):
            s = value
        rpcrf__knhay[tys__niduj] = s


def str_fillna_alloc_series_impl(S, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    rpcrf__knhay = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    nug__bjney = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(rpcrf__knhay)
    fdno__fbd = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
    for ncith__fneob in numba.parfors.parfor.internal_prange(n):
        s = rpcrf__knhay[ncith__fneob]
        if bodo.libs.array_kernels.isna(rpcrf__knhay, ncith__fneob
            ) and not bodo.libs.array_kernels.isna(nug__bjney, ncith__fneob):
            s = nug__bjney[ncith__fneob]
        fdno__fbd[ncith__fneob] = s
        if bodo.libs.array_kernels.isna(rpcrf__knhay, ncith__fneob
            ) and bodo.libs.array_kernels.isna(nug__bjney, ncith__fneob):
            bodo.libs.array_kernels.setna(fdno__fbd, ncith__fneob)
    return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index, name)


def fillna_series_impl(S, value=None, method=None, axis=None, inplace=False,
    limit=None, downcast=None):
    rpcrf__knhay = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    nug__bjney = bodo.hiframes.pd_series_ext.get_series_data(value)
    n = len(rpcrf__knhay)
    fdno__fbd = bodo.utils.utils.alloc_type(n, rpcrf__knhay.dtype, (-1,))
    for tys__niduj in numba.parfors.parfor.internal_prange(n):
        s = rpcrf__knhay[tys__niduj]
        if bodo.libs.array_kernels.isna(rpcrf__knhay, tys__niduj
            ) and not bodo.libs.array_kernels.isna(nug__bjney, tys__niduj):
            s = nug__bjney[tys__niduj]
        fdno__fbd[tys__niduj] = s
    return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index, name)


@overload_method(SeriesType, 'fillna', no_unliteral=True)
def overload_series_fillna(S, value=None, method=None, axis=None, inplace=
    False, limit=None, downcast=None):
    xjc__qmsn = dict(limit=limit, downcast=downcast)
    jrco__lxxs = dict(limit=None, downcast=None)
    check_unsupported_args('Series.fillna', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    foxuf__fpesg = not is_overload_none(value)
    hmr__tzjx = not is_overload_none(method)
    if foxuf__fpesg and hmr__tzjx:
        raise BodoError(
            "Series.fillna(): Cannot specify both 'value' and 'method'.")
    if not foxuf__fpesg and not hmr__tzjx:
        raise BodoError(
            "Series.fillna(): Must specify one of 'value' and 'method'.")
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error('Series.fillna(): axis argument not supported')
    elif is_iterable_type(value) and not isinstance(value, SeriesType):
        raise BodoError('Series.fillna(): "value" parameter cannot be a list')
    elif is_var_size_item_array_type(S.data
        ) and not S.dtype == bodo.string_type:
        raise BodoError(
            f'Series.fillna() with inplace=True not supported for {S.dtype} values yet.'
            )
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "Series.fillna(): 'inplace' argument must be a constant boolean")
    if hmr__tzjx:
        if is_overload_true(inplace):
            raise BodoError(
                "Series.fillna() with inplace=True not supported with 'method' argument yet."
                )
        svqrl__eghd = (
            "Series.fillna(): 'method' argument if provided must be a constant string and one of ('backfill', 'bfill', 'pad' 'ffill')."
            )
        if not is_overload_constant_str(method):
            raise_bodo_error(svqrl__eghd)
        elif get_overload_const_str(method) not in ('backfill', 'bfill',
            'pad', 'ffill'):
            raise BodoError(svqrl__eghd)
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.fillna()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'Series.fillna()')
    drhgh__qtkt = element_type(S.data)
    dftxl__otz = None
    if foxuf__fpesg:
        dftxl__otz = element_type(types.unliteral(value))
    if dftxl__otz and not can_replace(drhgh__qtkt, dftxl__otz):
        raise BodoError(
            f'Series.fillna(): Cannot use value type {dftxl__otz} with series type {drhgh__qtkt}'
            )
    if is_overload_true(inplace):
        if S.dtype == bodo.string_type:
            if S.data == bodo.dict_str_arr_type:
                raise_bodo_error(
                    "Series.fillna(): 'inplace' not supported for dictionary-encoded string arrays yet."
                    )
            if is_overload_constant_str(value) and get_overload_const_str(value
                ) == '':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=False)
            return binary_str_fillna_inplace_impl(is_binary=False)
        if S.dtype == bodo.bytes_type:
            if is_overload_constant_bytes(value) and get_overload_const_bytes(
                value) == b'':
                return (lambda S, value=None, method=None, axis=None,
                    inplace=False, limit=None, downcast=None: bodo.libs.
                    str_arr_ext.set_null_bits_to_value(bodo.hiframes.
                    pd_series_ext.get_series_data(S), -1))
            if isinstance(value, SeriesType):
                return binary_str_fillna_inplace_series_impl(is_binary=True)
            return binary_str_fillna_inplace_impl(is_binary=True)
        else:
            if isinstance(value, SeriesType):
                return fillna_inplace_series_impl
            return fillna_inplace_impl
    else:
        qmch__xnfc = to_str_arr_if_dict_array(S.data)
        if isinstance(value, SeriesType):

            def fillna_series_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                rpcrf__knhay = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                nug__bjney = bodo.hiframes.pd_series_ext.get_series_data(value)
                n = len(rpcrf__knhay)
                fdno__fbd = bodo.utils.utils.alloc_type(n, qmch__xnfc, (-1,))
                for tys__niduj in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rpcrf__knhay, tys__niduj
                        ) and bodo.libs.array_kernels.isna(nug__bjney,
                        tys__niduj):
                        bodo.libs.array_kernels.setna(fdno__fbd, tys__niduj)
                        continue
                    if bodo.libs.array_kernels.isna(rpcrf__knhay, tys__niduj):
                        fdno__fbd[tys__niduj
                            ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                            nug__bjney[tys__niduj])
                        continue
                    fdno__fbd[tys__niduj
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        rpcrf__knhay[tys__niduj])
                return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                    index, name)
            return fillna_series_impl
        if hmr__tzjx:
            ozvt__htu = (types.unicode_type, types.bool_, bodo.datetime64ns,
                bodo.timedelta64ns)
            if not isinstance(drhgh__qtkt, (types.Integer, types.Float)
                ) and drhgh__qtkt not in ozvt__htu:
                raise BodoError(
                    f"Series.fillna(): series of type {drhgh__qtkt} are not supported with 'method' argument."
                    )

            def fillna_method_impl(S, value=None, method=None, axis=None,
                inplace=False, limit=None, downcast=None):
                rpcrf__knhay = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                fdno__fbd = bodo.libs.array_kernels.ffill_bfill_arr(
                    rpcrf__knhay, method)
                return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                    index, name)
            return fillna_method_impl

        def fillna_impl(S, value=None, method=None, axis=None, inplace=
            False, limit=None, downcast=None):
            value = bodo.utils.conversion.unbox_if_tz_naive_timestamp(value)
            rpcrf__knhay = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            n = len(rpcrf__knhay)
            fdno__fbd = bodo.utils.utils.alloc_type(n, qmch__xnfc, (-1,))
            for tys__niduj in numba.parfors.parfor.internal_prange(n):
                s = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                    rpcrf__knhay[tys__niduj])
                if bodo.libs.array_kernels.isna(rpcrf__knhay, tys__niduj):
                    s = value
                fdno__fbd[tys__niduj] = s
            return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index,
                name)
        return fillna_impl


def create_fillna_specific_method_overload(overload_name):

    def overload_series_fillna_specific_method(S, axis=None, inplace=False,
        limit=None, downcast=None):
        esto__ppphx = {'ffill': 'ffill', 'bfill': 'bfill', 'pad': 'ffill',
            'backfill': 'bfill'}[overload_name]
        xjc__qmsn = dict(limit=limit, downcast=downcast)
        jrco__lxxs = dict(limit=None, downcast=None)
        check_unsupported_args(f'Series.{overload_name}', xjc__qmsn,
            jrco__lxxs, package_name='pandas', module_name='Series')
        if not (is_overload_none(axis) or is_overload_zero(axis)):
            raise BodoError(
                f'Series.{overload_name}(): axis argument not supported')
        drhgh__qtkt = element_type(S.data)
        ozvt__htu = (types.unicode_type, types.bool_, bodo.datetime64ns,
            bodo.timedelta64ns)
        if not isinstance(drhgh__qtkt, (types.Integer, types.Float)
            ) and drhgh__qtkt not in ozvt__htu:
            raise BodoError(
                f'Series.{overload_name}(): series of type {drhgh__qtkt} are not supported.'
                )

        def impl(S, axis=None, inplace=False, limit=None, downcast=None):
            rpcrf__knhay = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            fdno__fbd = bodo.libs.array_kernels.ffill_bfill_arr(rpcrf__knhay,
                esto__ppphx)
            return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index,
                name)
        return impl
    return overload_series_fillna_specific_method


fillna_specific_methods = 'ffill', 'bfill', 'pad', 'backfill'


def _install_fillna_specific_methods():
    for overload_name in fillna_specific_methods:
        yzfyo__lwow = create_fillna_specific_method_overload(overload_name)
        overload_method(SeriesType, overload_name, no_unliteral=True)(
            yzfyo__lwow)


_install_fillna_specific_methods()


def check_unsupported_types(S, to_replace, value):
    if any(bodo.utils.utils.is_array_typ(x, True) for x in [S.dtype,
        to_replace, value]):
        lzwrk__sqdcw = (
            'Series.replace(): only support with Scalar, List, or Dictionary')
        raise BodoError(lzwrk__sqdcw)
    elif isinstance(to_replace, types.DictType) and not is_overload_none(value
        ):
        lzwrk__sqdcw = (
            "Series.replace(): 'value' must be None when 'to_replace' is a dictionary"
            )
        raise BodoError(lzwrk__sqdcw)
    elif any(isinstance(x, (PandasTimestampType, PDTimeDeltaType)) for x in
        [to_replace, value]):
        lzwrk__sqdcw = (
            f'Series.replace(): Not supported for types {to_replace} and {value}'
            )
        raise BodoError(lzwrk__sqdcw)


def series_replace_error_checking(S, to_replace, value, inplace, limit,
    regex, method):
    xjc__qmsn = dict(inplace=inplace, limit=limit, regex=regex, method=method)
    plfbg__tdf = dict(inplace=False, limit=None, regex=False, method='pad')
    check_unsupported_args('Series.replace', xjc__qmsn, plfbg__tdf,
        package_name='pandas', module_name='Series')
    check_unsupported_types(S, to_replace, value)


@overload_method(SeriesType, 'replace', inline='always', no_unliteral=True)
def overload_series_replace(S, to_replace=None, value=None, inplace=False,
    limit=None, regex=False, method='pad'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.replace()')
    series_replace_error_checking(S, to_replace, value, inplace, limit,
        regex, method)
    drhgh__qtkt = element_type(S.data)
    if isinstance(to_replace, types.DictType):
        tmjsr__upbi = element_type(to_replace.key_type)
        dftxl__otz = element_type(to_replace.value_type)
    else:
        tmjsr__upbi = element_type(to_replace)
        dftxl__otz = element_type(value)
    fegi__ycjm = None
    if drhgh__qtkt != types.unliteral(tmjsr__upbi):
        if bodo.utils.typing.equality_always_false(drhgh__qtkt, types.
            unliteral(tmjsr__upbi)
            ) or not bodo.utils.typing.types_equality_exists(drhgh__qtkt,
            tmjsr__upbi):

            def impl(S, to_replace=None, value=None, inplace=False, limit=
                None, regex=False, method='pad'):
                return S.copy()
            return impl
        if isinstance(drhgh__qtkt, (types.Float, types.Integer)
            ) or drhgh__qtkt == np.bool_:
            fegi__ycjm = drhgh__qtkt
    if not can_replace(drhgh__qtkt, types.unliteral(dftxl__otz)):

        def impl(S, to_replace=None, value=None, inplace=False, limit=None,
            regex=False, method='pad'):
            return S.copy()
        return impl
    qwj__ckqg = to_str_arr_if_dict_array(S.data)
    if isinstance(qwj__ckqg, CategoricalArrayType):

        def cat_impl(S, to_replace=None, value=None, inplace=False, limit=
            None, regex=False, method='pad'):
            rpcrf__knhay = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            return bodo.hiframes.pd_series_ext.init_series(rpcrf__knhay.
                replace(to_replace, value), index, name)
        return cat_impl

    def impl(S, to_replace=None, value=None, inplace=False, limit=None,
        regex=False, method='pad'):
        rpcrf__knhay = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        n = len(rpcrf__knhay)
        fdno__fbd = bodo.utils.utils.alloc_type(n, qwj__ckqg, (-1,))
        xrrcz__hvjvz = build_replace_dict(to_replace, value, fegi__ycjm)
        for tys__niduj in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(rpcrf__knhay, tys__niduj):
                bodo.libs.array_kernels.setna(fdno__fbd, tys__niduj)
                continue
            s = rpcrf__knhay[tys__niduj]
            if s in xrrcz__hvjvz:
                s = xrrcz__hvjvz[s]
            fdno__fbd[tys__niduj] = s
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index, name)
    return impl


def build_replace_dict(to_replace, value, key_dtype_conv):
    pass


@overload(build_replace_dict)
def _build_replace_dict(to_replace, value, key_dtype_conv):
    tzrt__eabe = isinstance(to_replace, (types.Number, Decimal128Type)
        ) or to_replace in [bodo.string_type, types.boolean, bodo.bytes_type]
    jmqn__bbqsn = is_iterable_type(to_replace)
    yael__gef = isinstance(value, (types.Number, Decimal128Type)) or value in [
        bodo.string_type, bodo.bytes_type, types.boolean]
    fxh__qnl = is_iterable_type(value)
    if tzrt__eabe and yael__gef:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                xrrcz__hvjvz = {}
                xrrcz__hvjvz[key_dtype_conv(to_replace)] = value
                return xrrcz__hvjvz
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            xrrcz__hvjvz = {}
            xrrcz__hvjvz[to_replace] = value
            return xrrcz__hvjvz
        return impl
    if jmqn__bbqsn and yael__gef:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                xrrcz__hvjvz = {}
                for ono__xik in to_replace:
                    xrrcz__hvjvz[key_dtype_conv(ono__xik)] = value
                return xrrcz__hvjvz
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            xrrcz__hvjvz = {}
            for ono__xik in to_replace:
                xrrcz__hvjvz[ono__xik] = value
            return xrrcz__hvjvz
        return impl
    if jmqn__bbqsn and fxh__qnl:
        if not is_overload_none(key_dtype_conv):

            def impl_cast(to_replace, value, key_dtype_conv):
                xrrcz__hvjvz = {}
                assert len(to_replace) == len(value
                    ), 'To_replace and value lengths must be the same'
                for tys__niduj in range(len(to_replace)):
                    xrrcz__hvjvz[key_dtype_conv(to_replace[tys__niduj])
                        ] = value[tys__niduj]
                return xrrcz__hvjvz
            return impl_cast

        def impl(to_replace, value, key_dtype_conv):
            xrrcz__hvjvz = {}
            assert len(to_replace) == len(value
                ), 'To_replace and value lengths must be the same'
            for tys__niduj in range(len(to_replace)):
                xrrcz__hvjvz[to_replace[tys__niduj]] = value[tys__niduj]
            return xrrcz__hvjvz
        return impl
    if isinstance(to_replace, numba.types.DictType) and is_overload_none(value
        ):
        return lambda to_replace, value, key_dtype_conv: to_replace
    raise BodoError(
        'Series.replace(): Not supported for types to_replace={} and value={}'
        .format(to_replace, value))


@overload_method(SeriesType, 'diff', inline='always', no_unliteral=True)
def overload_series_diff(S, periods=1):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.diff()')
    if not (isinstance(S.data, types.Array) and (isinstance(S.data.dtype,
        types.Number) or S.data.dtype == bodo.datetime64ns)):
        raise BodoError(
            f'Series.diff() column input type {S.data} not supported.')
    if not is_overload_int(periods):
        raise BodoError("Series.diff(): 'periods' input must be an integer.")
    if S.data == types.Array(bodo.datetime64ns, 1, 'C'):

        def impl_datetime(S, periods=1):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            fdno__fbd = bodo.hiframes.series_impl.dt64_arr_sub(arr, bodo.
                hiframes.rolling.shift(arr, periods, False))
            return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index,
                name)
        return impl_datetime

    def impl(S, periods=1):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        fdno__fbd = arr - bodo.hiframes.rolling.shift(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index, name)
    return impl


@overload_method(SeriesType, 'explode', inline='always', no_unliteral=True)
def overload_series_explode(S, ignore_index=False):
    from bodo.hiframes.split_impl import string_array_split_view_type
    xjc__qmsn = dict(ignore_index=ignore_index)
    wdo__xun = dict(ignore_index=False)
    check_unsupported_args('Series.explode', xjc__qmsn, wdo__xun,
        package_name='pandas', module_name='Series')
    if not (isinstance(S.data, ArrayItemArrayType) or S.data ==
        string_array_split_view_type):
        return lambda S, ignore_index=False: S.copy()

    def impl(S, ignore_index=False):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wldxr__prmbi = bodo.utils.conversion.index_to_array(index)
        fdno__fbd, xgku__yiwf = bodo.libs.array_kernels.explode(arr,
            wldxr__prmbi)
        ngbtj__job = bodo.utils.conversion.index_from_array(xgku__yiwf)
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
            ngbtj__job, name)
    return impl


@overload(np.digitize, inline='always', no_unliteral=True)
def overload_series_np_digitize(x, bins, right=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'numpy.digitize()')
    if isinstance(x, SeriesType):

        def impl(x, bins, right=False):
            arr = bodo.hiframes.pd_series_ext.get_series_data(x)
            return np.digitize(arr, bins, right)
        return impl


@overload(np.argmax, inline='always', no_unliteral=True)
def argmax_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            eem__pturn = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for tys__niduj in numba.parfors.parfor.internal_prange(n):
                eem__pturn[tys__niduj] = np.argmax(a[tys__niduj])
            return eem__pturn
        return impl


@overload(np.argmin, inline='always', no_unliteral=True)
def argmin_overload(a, axis=None, out=None):
    if isinstance(a, types.Array) and is_overload_constant_int(axis
        ) and get_overload_const_int(axis) == 1:

        def impl(a, axis=None, out=None):
            hoxd__dgjxp = np.empty(len(a), a.dtype)
            numba.parfors.parfor.init_prange()
            n = len(a)
            for tys__niduj in numba.parfors.parfor.internal_prange(n):
                hoxd__dgjxp[tys__niduj] = np.argmin(a[tys__niduj])
            return hoxd__dgjxp
        return impl


def overload_series_np_dot(a, b, out=None):
    if (isinstance(a, SeriesType) or isinstance(b, SeriesType)
        ) and not is_overload_none(out):
        raise BodoError("np.dot(): 'out' parameter not supported yet")
    if isinstance(a, SeriesType) and isinstance(b, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.utils.conversion.ndarray_if_nullable_arr(bodo.
                hiframes.pd_series_ext.get_series_data(a))
            cpxc__cml = bodo.utils.conversion.ndarray_if_nullable_arr(bodo.
                hiframes.pd_series_ext.get_series_data(b))
            return np.dot(arr, cpxc__cml)
        return impl
    if isinstance(a, SeriesType):

        def impl(a, b, out=None):
            arr = bodo.utils.conversion.ndarray_if_nullable_arr(bodo.
                hiframes.pd_series_ext.get_series_data(a))
            b = bodo.utils.conversion.ndarray_if_nullable_arr(b)
            return np.dot(arr, b)
        return impl
    if isinstance(b, SeriesType):

        def impl(a, b, out=None):
            a = bodo.utils.conversion.ndarray_if_nullable_arr(a)
            arr = bodo.utils.conversion.ndarray_if_nullable_arr(bodo.
                hiframes.pd_series_ext.get_series_data(b))
            return np.dot(a, arr)
        return impl


overload(np.dot, inline='always', no_unliteral=True)(overload_series_np_dot)
overload(operator.matmul, inline='always', no_unliteral=True)(
    overload_series_np_dot)


@overload_method(SeriesType, 'dropna', inline='always', no_unliteral=True)
def overload_series_dropna(S, axis=0, inplace=False, how=None):
    xjc__qmsn = dict(axis=axis, inplace=inplace, how=how)
    sltip__ksd = dict(axis=0, inplace=False, how=None)
    check_unsupported_args('Series.dropna', xjc__qmsn, sltip__ksd,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.dropna()')
    if S.dtype == bodo.string_type:

        def dropna_str_impl(S, axis=0, inplace=False, how=None):
            rpcrf__knhay = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            tqw__pdyp = S.notna().values
            wldxr__prmbi = bodo.utils.conversion.extract_index_array(S)
            ngbtj__job = bodo.utils.conversion.convert_to_index(wldxr__prmbi
                [tqw__pdyp])
            fdno__fbd = (bodo.hiframes.series_kernels.
                _series_dropna_str_alloc_impl_inner(rpcrf__knhay))
            return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                ngbtj__job, name)
        return dropna_str_impl
    else:

        def dropna_impl(S, axis=0, inplace=False, how=None):
            rpcrf__knhay = bodo.hiframes.pd_series_ext.get_series_data(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            wldxr__prmbi = bodo.utils.conversion.extract_index_array(S)
            tqw__pdyp = S.notna().values
            ngbtj__job = bodo.utils.conversion.convert_to_index(wldxr__prmbi
                [tqw__pdyp])
            fdno__fbd = rpcrf__knhay[tqw__pdyp]
            return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                ngbtj__job, name)
        return dropna_impl


@overload_method(SeriesType, 'shift', inline='always', no_unliteral=True)
def overload_series_shift(S, periods=1, freq=None, axis=0, fill_value=None):
    xjc__qmsn = dict(freq=freq, axis=axis)
    jrco__lxxs = dict(freq=None, axis=0)
    check_unsupported_args('Series.shift', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not is_supported_shift_array_type(S.data):
        raise BodoError(
            f"Series.shift(): Series input type '{S.data.dtype}' not supported yet."
            )
    if not is_overload_int(periods):
        raise BodoError("Series.shift(): 'periods' input must be an integer.")

    def impl(S, periods=1, freq=None, axis=0, fill_value=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        fdno__fbd = bodo.hiframes.rolling.shift(arr, periods, False, fill_value
            )
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index, name)
    return impl


@overload_method(SeriesType, 'pct_change', inline='always', no_unliteral=True)
def overload_series_pct_change(S, periods=1, fill_method='pad', limit=None,
    freq=None):
    xjc__qmsn = dict(fill_method=fill_method, limit=limit, freq=freq)
    jrco__lxxs = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('Series.pct_change', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    if not is_overload_int(periods):
        raise BodoError(
            'Series.pct_change(): periods argument must be an Integer')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.pct_change()')

    def impl(S, periods=1, fill_method='pad', limit=None, freq=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        fdno__fbd = bodo.hiframes.rolling.pct_change(arr, periods, False)
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index, name)
    return impl


def create_series_mask_where_overload(func_name):

    def overload_series_mask_where(S, cond, other=np.nan, inplace=False,
        axis=None, level=None, errors='raise', try_cast=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
            f'Series.{func_name}()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
            f'Series.{func_name}()')
        _validate_arguments_mask_where(f'Series.{func_name}', 'Series', S,
            cond, other, inplace, axis, level, errors, try_cast)
        if is_overload_constant_nan(other):
            gzo__nrl = 'None'
        else:
            gzo__nrl = 'other'
        kld__zjlce = """def impl(S, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise',try_cast=False):
"""
        if func_name == 'mask':
            kld__zjlce += '  cond = ~cond\n'
        kld__zjlce += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        kld__zjlce += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        kld__zjlce += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        kld__zjlce += (
            f'  out_arr = bodo.hiframes.series_impl.where_impl(cond, arr, {gzo__nrl})\n'
            )
        kld__zjlce += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        ucijt__sjfar = {}
        exec(kld__zjlce, {'bodo': bodo, 'np': np}, ucijt__sjfar)
        impl = ucijt__sjfar['impl']
        return impl
    return overload_series_mask_where


def _install_series_mask_where_overload():
    for func_name in ('mask', 'where'):
        yzfyo__lwow = create_series_mask_where_overload(func_name)
        overload_method(SeriesType, func_name, no_unliteral=True)(yzfyo__lwow)


_install_series_mask_where_overload()


def _validate_arguments_mask_where(func_name, module_name, S, cond, other,
    inplace, axis, level, errors, try_cast):
    xjc__qmsn = dict(inplace=inplace, level=level, errors=errors, try_cast=
        try_cast)
    jrco__lxxs = dict(inplace=False, level=None, errors='raise', try_cast=False
        )
    check_unsupported_args(f'{func_name}', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name=module_name)
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error(f'{func_name}(): axis argument not supported')
    if isinstance(S, bodo.hiframes.pd_index_ext.RangeIndexType):
        arr = types.Array(types.int64, 1, 'C')
    else:
        arr = S.data
    if isinstance(other, SeriesType):
        _validate_self_other_mask_where(func_name, module_name, arr, other.data
            )
    else:
        _validate_self_other_mask_where(func_name, module_name, arr, other)
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        cond.ndim == 1 and cond.dtype == types.bool_):
        raise BodoError(
            f"{func_name}() 'cond' argument must be a Series or 1-dim array of booleans"
            )


def _validate_self_other_mask_where(func_name, module_name, arr, other,
    max_ndim=1, is_default=False):
    if not (isinstance(arr, types.Array) or isinstance(arr,
        BooleanArrayType) or isinstance(arr, IntegerArrayType) or
        isinstance(arr, FloatingArrayType) or bodo.utils.utils.is_array_typ
        (arr, False) and arr.dtype in [bodo.string_type, bodo.bytes_type] or
        isinstance(arr, bodo.CategoricalArrayType) and arr.dtype.elem_type
         not in [bodo.datetime64ns, bodo.timedelta64ns, bodo.
        pd_timestamp_tz_naive_type, bodo.pd_timedelta_type]):
        raise BodoError(
            f'{func_name}() {module_name} data with type {arr} not yet supported'
            )
    gbsj__wrjl = is_overload_constant_nan(other)
    if not (is_default or gbsj__wrjl or is_scalar_type(other) or isinstance
        (other, types.Array) and other.ndim >= 1 and other.ndim <= max_ndim or
        isinstance(other, SeriesType) and (isinstance(arr, types.Array) or 
        arr.dtype in [bodo.string_type, bodo.bytes_type]) or 
        is_str_arr_type(other) and (arr.dtype == bodo.string_type or 
        isinstance(arr, bodo.CategoricalArrayType) and arr.dtype.elem_type ==
        bodo.string_type) or isinstance(other, BinaryArrayType) and (arr.
        dtype == bodo.bytes_type or isinstance(arr, bodo.
        CategoricalArrayType) and arr.dtype.elem_type == bodo.bytes_type) or
        (not (isinstance(other, (StringArrayType, BinaryArrayType)) or 
        other == bodo.dict_str_arr_type) and (isinstance(arr.dtype, types.
        Integer) and (bodo.utils.utils.is_array_typ(other) and isinstance(
        other.dtype, types.Integer) or is_series_type(other) and isinstance
        (other.dtype, types.Integer))) or (bodo.utils.utils.is_array_typ(
        other) and arr.dtype == other.dtype or is_series_type(other) and 
        arr.dtype == other.dtype)) and (isinstance(arr, BooleanArrayType) or
        isinstance(arr, (IntegerArrayType, FloatingArrayType)))):
        raise BodoError(
            f"{func_name}() 'other' must be a scalar, non-categorical series, 1-dim numpy array or StringArray with a matching type for {module_name}."
            )
    if not is_default:
        if isinstance(arr.dtype, bodo.PDCategoricalDtype):
            ycop__xmu = arr.dtype.elem_type
        else:
            ycop__xmu = arr.dtype
        if is_iterable_type(other):
            hpcie__isqkv = other.dtype
        elif gbsj__wrjl:
            hpcie__isqkv = types.float64
        else:
            hpcie__isqkv = types.unliteral(other)
        if not gbsj__wrjl and not is_common_scalar_dtype([ycop__xmu,
            hpcie__isqkv]):
            raise BodoError(
                f"{func_name}() {module_name.lower()} and 'other' must share a common type."
                )


def create_explicit_binary_op_overload(op):

    def overload_series_explicit_binary_op(S, other, level=None, fill_value
        =None, axis=0):
        xjc__qmsn = dict(level=level, axis=axis)
        jrco__lxxs = dict(level=None, axis=0)
        check_unsupported_args('series.{}'.format(op.__name__), xjc__qmsn,
            jrco__lxxs, package_name='pandas', module_name='Series')
        rdiuk__agdum = other == string_type or is_overload_constant_str(other)
        exrl__wzy = is_iterable_type(other) and other.dtype == string_type
        pkdxl__kgyn = S.dtype == string_type and (op == operator.add and (
            rdiuk__agdum or exrl__wzy) or op == operator.mul and isinstance
            (other, types.Integer))
        idll__pblhj = S.dtype == bodo.timedelta64ns
        uxd__wwfqh = S.dtype == bodo.datetime64ns
        qwpnz__gqfsx = is_iterable_type(other) and (other.dtype ==
            datetime_timedelta_type or other.dtype == bodo.timedelta64ns)
        xkq__sgk = is_iterable_type(other) and (other.dtype ==
            datetime_datetime_type or other.dtype ==
            pd_timestamp_tz_naive_type or other.dtype == bodo.datetime64ns)
        gfwf__btox = idll__pblhj and (qwpnz__gqfsx or xkq__sgk
            ) or uxd__wwfqh and qwpnz__gqfsx
        gfwf__btox = gfwf__btox and op == operator.add
        if not (isinstance(S.dtype, types.Number) or pkdxl__kgyn or gfwf__btox
            ):
            raise BodoError(f'Unsupported types for Series.{op.__name__}')
        zwlb__kdimp = numba.core.registry.cpu_target.typing_context
        if is_scalar_type(other):
            args = S.data, other
            qwj__ckqg = zwlb__kdimp.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
                ) and qwj__ckqg == types.Array(types.bool_, 1, 'C'):
                qwj__ckqg = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                other = bodo.utils.conversion.unbox_if_tz_naive_timestamp(other
                    )
                n = len(arr)
                fdno__fbd = bodo.utils.utils.alloc_type(n, qwj__ckqg, (-1,))
                for tys__niduj in numba.parfors.parfor.internal_prange(n):
                    nwbcg__pquw = bodo.libs.array_kernels.isna(arr, tys__niduj)
                    if nwbcg__pquw:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(fdno__fbd, tys__niduj
                                )
                        else:
                            fdno__fbd[tys__niduj] = op(fill_value, other)
                    else:
                        fdno__fbd[tys__niduj] = op(arr[tys__niduj], other)
                return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                    index, name)
            return impl_scalar
        args = S.data, types.Array(other.dtype, 1, 'C')
        qwj__ckqg = zwlb__kdimp.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
            ) and qwj__ckqg == types.Array(types.bool_, 1, 'C'):
            qwj__ckqg = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            dyo__jdztb = bodo.utils.conversion.coerce_to_array(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            fdno__fbd = bodo.utils.utils.alloc_type(n, qwj__ckqg, (-1,))
            for tys__niduj in numba.parfors.parfor.internal_prange(n):
                nwbcg__pquw = bodo.libs.array_kernels.isna(arr, tys__niduj)
                auy__tiam = bodo.libs.array_kernels.isna(dyo__jdztb, tys__niduj
                    )
                if nwbcg__pquw and auy__tiam:
                    bodo.libs.array_kernels.setna(fdno__fbd, tys__niduj)
                elif nwbcg__pquw:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(fdno__fbd, tys__niduj)
                    else:
                        fdno__fbd[tys__niduj] = op(fill_value, dyo__jdztb[
                            tys__niduj])
                elif auy__tiam:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(fdno__fbd, tys__niduj)
                    else:
                        fdno__fbd[tys__niduj] = op(arr[tys__niduj], fill_value)
                else:
                    fdno__fbd[tys__niduj] = op(arr[tys__niduj], dyo__jdztb[
                        tys__niduj])
            return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index,
                name)
        return impl
    return overload_series_explicit_binary_op


def create_explicit_binary_reverse_op_overload(op):

    def overload_series_explicit_binary_reverse_op(S, other, level=None,
        fill_value=None, axis=0):
        if not is_overload_none(level):
            raise BodoError('level argument not supported')
        if not is_overload_zero(axis):
            raise BodoError('axis argument not supported')
        if not isinstance(S.dtype, types.Number):
            raise BodoError('only numeric values supported')
        zwlb__kdimp = numba.core.registry.cpu_target.typing_context
        if isinstance(other, types.Number):
            args = other, S.data
            qwj__ckqg = zwlb__kdimp.resolve_function_type(op, args, {}
                ).return_type
            if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
                ) and qwj__ckqg == types.Array(types.bool_, 1, 'C'):
                qwj__ckqg = boolean_array

            def impl_scalar(S, other, level=None, fill_value=None, axis=0):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                numba.parfors.parfor.init_prange()
                n = len(arr)
                fdno__fbd = bodo.utils.utils.alloc_type(n, qwj__ckqg, None)
                for tys__niduj in numba.parfors.parfor.internal_prange(n):
                    nwbcg__pquw = bodo.libs.array_kernels.isna(arr, tys__niduj)
                    if nwbcg__pquw:
                        if fill_value is None:
                            bodo.libs.array_kernels.setna(fdno__fbd, tys__niduj
                                )
                        else:
                            fdno__fbd[tys__niduj] = op(other, fill_value)
                    else:
                        fdno__fbd[tys__niduj] = op(other, arr[tys__niduj])
                return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                    index, name)
            return impl_scalar
        args = types.Array(other.dtype, 1, 'C'), S.data
        qwj__ckqg = zwlb__kdimp.resolve_function_type(op, args, {}).return_type
        if isinstance(S.data, (IntegerArrayType, FloatingArrayType)
            ) and qwj__ckqg == types.Array(types.bool_, 1, 'C'):
            qwj__ckqg = boolean_array

        def impl(S, other, level=None, fill_value=None, axis=0):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            dyo__jdztb = bodo.hiframes.pd_series_ext.get_series_data(other)
            numba.parfors.parfor.init_prange()
            n = len(arr)
            fdno__fbd = bodo.utils.utils.alloc_type(n, qwj__ckqg, None)
            for tys__niduj in numba.parfors.parfor.internal_prange(n):
                nwbcg__pquw = bodo.libs.array_kernels.isna(arr, tys__niduj)
                auy__tiam = bodo.libs.array_kernels.isna(dyo__jdztb, tys__niduj
                    )
                fdno__fbd[tys__niduj] = op(dyo__jdztb[tys__niduj], arr[
                    tys__niduj])
                if nwbcg__pquw and auy__tiam:
                    bodo.libs.array_kernels.setna(fdno__fbd, tys__niduj)
                elif nwbcg__pquw:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(fdno__fbd, tys__niduj)
                    else:
                        fdno__fbd[tys__niduj] = op(dyo__jdztb[tys__niduj],
                            fill_value)
                elif auy__tiam:
                    if fill_value is None:
                        bodo.libs.array_kernels.setna(fdno__fbd, tys__niduj)
                    else:
                        fdno__fbd[tys__niduj] = op(fill_value, arr[tys__niduj])
                else:
                    fdno__fbd[tys__niduj] = op(dyo__jdztb[tys__niduj], arr[
                        tys__niduj])
            return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index,
                name)
        return impl
    return overload_series_explicit_binary_reverse_op


explicit_binop_funcs_two_ways = {operator.add: {'add'}, operator.sub: {
    'sub'}, operator.mul: {'mul'}, operator.truediv: {'div', 'truediv'},
    operator.floordiv: {'floordiv'}, operator.mod: {'mod'}, operator.pow: {
    'pow'}}
explicit_binop_funcs_single = {operator.lt: 'lt', operator.gt: 'gt',
    operator.le: 'le', operator.ge: 'ge', operator.ne: 'ne', operator.eq: 'eq'}
explicit_binop_funcs = set()
split_logical_binops_funcs = [operator.or_, operator.and_]


def _install_explicit_binary_ops():
    for op, fgon__ghvl in explicit_binop_funcs_two_ways.items():
        for name in fgon__ghvl:
            yzfyo__lwow = create_explicit_binary_op_overload(op)
            nbjnf__bxmf = create_explicit_binary_reverse_op_overload(op)
            pkv__cnemp = 'r' + name
            overload_method(SeriesType, name, no_unliteral=True)(yzfyo__lwow)
            overload_method(SeriesType, pkv__cnemp, no_unliteral=True)(
                nbjnf__bxmf)
            explicit_binop_funcs.add(name)
    for op, name in explicit_binop_funcs_single.items():
        yzfyo__lwow = create_explicit_binary_op_overload(op)
        overload_method(SeriesType, name, no_unliteral=True)(yzfyo__lwow)
        explicit_binop_funcs.add(name)


_install_explicit_binary_ops()


def create_binary_op_overload(op):

    def overload_series_binary_op(lhs, rhs):
        if (isinstance(lhs, SeriesType) and isinstance(rhs, SeriesType) and
            lhs.dtype == bodo.datetime64ns and rhs.dtype == bodo.
            datetime64ns and op == operator.sub):

            def impl_dt64(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                ylbxu__ckyym = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                fdno__fbd = dt64_arr_sub(arr, ylbxu__ckyym)
                return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                    index, name)
            return impl_dt64
        if op in [operator.add, operator.sub] and isinstance(lhs, SeriesType
            ) and lhs.dtype == bodo.datetime64ns and is_offsets_type(rhs):

            def impl_offsets(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                n = len(lhs)
                fdno__fbd = np.empty(n, np.dtype('datetime64[ns]'))
                for tys__niduj in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(arr, tys__niduj):
                        bodo.libs.array_kernels.setna(fdno__fbd, tys__niduj)
                        continue
                    vzrha__tjm = (bodo.hiframes.pd_timestamp_ext.
                        convert_datetime64_to_timestamp(arr[tys__niduj]))
                    omvfy__oeodq = op(vzrha__tjm, rhs)
                    fdno__fbd[tys__niduj
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        omvfy__oeodq.value)
                return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                    index, name)
            return impl_offsets
        if op == operator.add and is_offsets_type(lhs) and isinstance(rhs,
            SeriesType) and rhs.dtype == bodo.datetime64ns:

            def impl(lhs, rhs):
                return op(rhs, lhs)
            return impl
        if isinstance(lhs, SeriesType):
            if lhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                    ylbxu__ckyym = (bodo.utils.conversion.
                        get_array_if_series_or_index(rhs))
                    fdno__fbd = op(arr, bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(ylbxu__ckyym))
                    return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                ylbxu__ckyym = (bodo.utils.conversion.
                    get_array_if_series_or_index(rhs))
                fdno__fbd = op(arr, ylbxu__ckyym)
                return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                    index, name)
            return impl
        if isinstance(rhs, SeriesType):
            if rhs.dtype in [bodo.datetime64ns, bodo.timedelta64ns]:

                def impl(lhs, rhs):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                    index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                    name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                    lrdvb__nzgbd = (bodo.utils.conversion.
                        get_array_if_series_or_index(lhs))
                    fdno__fbd = op(bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(lrdvb__nzgbd), arr)
                    return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                        index, name)
                return impl

            def impl(lhs, rhs):
                arr = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                index = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                name = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                lrdvb__nzgbd = (bodo.utils.conversion.
                    get_array_if_series_or_index(lhs))
                fdno__fbd = op(lrdvb__nzgbd, arr)
                return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                    index, name)
            return impl
    return overload_series_binary_op


skips = list(explicit_binop_funcs_two_ways.keys()) + list(
    explicit_binop_funcs_single.keys()) + split_logical_binops_funcs


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        yzfyo__lwow = create_binary_op_overload(op)
        overload(op)(yzfyo__lwow)


_install_binary_ops()


def dt64_arr_sub(arg1, arg2):
    return arg1 - arg2


@overload(dt64_arr_sub, no_unliteral=True)
def overload_dt64_arr_sub(arg1, arg2):
    assert arg1 == types.Array(bodo.datetime64ns, 1, 'C'
        ) and arg2 == types.Array(bodo.datetime64ns, 1, 'C')
    tfbp__edb = np.dtype('timedelta64[ns]')

    def impl(arg1, arg2):
        numba.parfors.parfor.init_prange()
        n = len(arg1)
        S = np.empty(n, tfbp__edb)
        for tys__niduj in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg1, tys__niduj
                ) or bodo.libs.array_kernels.isna(arg2, tys__niduj):
                bodo.libs.array_kernels.setna(S, tys__niduj)
                continue
            S[tys__niduj
                ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arg1[
                tys__niduj]) - bodo.hiframes.pd_timestamp_ext.
                dt64_to_integer(arg2[tys__niduj]))
        return S
    return impl


def create_inplace_binary_op_overload(op):

    def overload_series_inplace_binary_op(S, other):
        if isinstance(S, SeriesType) or isinstance(other, SeriesType):

            def impl(S, other):
                arr = bodo.utils.conversion.get_array_if_series_or_index(S)
                dyo__jdztb = (bodo.utils.conversion.
                    get_array_if_series_or_index(other))
                op(arr, dyo__jdztb)
                return S
            return impl
    return overload_series_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        yzfyo__lwow = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(yzfyo__lwow)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_series_unary_op(S):
        if isinstance(S, SeriesType):

            def impl(S):
                arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                index = bodo.hiframes.pd_series_ext.get_series_index(S)
                name = bodo.hiframes.pd_series_ext.get_series_name(S)
                fdno__fbd = op(arr)
                return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                    index, name)
            return impl
    return overload_series_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        yzfyo__lwow = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(yzfyo__lwow)


_install_unary_ops()


def create_ufunc_overload(ufunc):
    if ufunc.nin == 1:

        def overload_series_ufunc_nin_1(S):
            if isinstance(S, SeriesType):

                def impl(S):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S)
                    fdno__fbd = ufunc(arr)
                    return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                        index, name)
                return impl
        return overload_series_ufunc_nin_1
    elif ufunc.nin == 2:

        def overload_series_ufunc_nin_2(S1, S2):
            if isinstance(S1, SeriesType):

                def impl(S1, S2):
                    arr = bodo.hiframes.pd_series_ext.get_series_data(S1)
                    index = bodo.hiframes.pd_series_ext.get_series_index(S1)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S1)
                    dyo__jdztb = (bodo.utils.conversion.
                        get_array_if_series_or_index(S2))
                    fdno__fbd = ufunc(arr, dyo__jdztb)
                    return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                        index, name)
                return impl
            elif isinstance(S2, SeriesType):

                def impl(S1, S2):
                    arr = bodo.utils.conversion.get_array_if_series_or_index(S1
                        )
                    dyo__jdztb = bodo.hiframes.pd_series_ext.get_series_data(S2
                        )
                    index = bodo.hiframes.pd_series_ext.get_series_index(S2)
                    name = bodo.hiframes.pd_series_ext.get_series_name(S2)
                    fdno__fbd = ufunc(arr, dyo__jdztb)
                    return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                        index, name)
                return impl
        return overload_series_ufunc_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for ufunc in numba.np.ufunc_db.get_ufuncs():
        yzfyo__lwow = create_ufunc_overload(ufunc)
        overload(ufunc, no_unliteral=True)(yzfyo__lwow)


_install_np_ufuncs()


def argsort(A):
    return np.argsort(A)


@overload(argsort, no_unliteral=True)
def overload_argsort(A):

    def impl(A):
        n = len(A)
        nqh__qxzv = bodo.libs.str_arr_ext.to_list_if_immutable_arr((A.copy(),))
        kvgy__xstcd = np.arange(n),
        bodo.libs.timsort.sort(nqh__qxzv, 0, n, kvgy__xstcd)
        return kvgy__xstcd[0]
    return impl


@overload(pd.to_numeric, inline='always', no_unliteral=True)
def overload_to_numeric(arg_a, errors='raise', downcast=None):
    if not is_overload_none(downcast) and not (is_overload_constant_str(
        downcast) and get_overload_const_str(downcast) in ('integer',
        'signed', 'unsigned', 'float')):
        raise BodoError(
            'pd.to_numeric(): invalid downcasting method provided {}'.
            format(downcast))
    out_dtype = types.float64
    if not is_overload_none(downcast):
        lkhaj__axb = get_overload_const_str(downcast)
        if lkhaj__axb in ('integer', 'signed'):
            out_dtype = types.int64
        elif lkhaj__axb == 'unsigned':
            out_dtype = types.uint64
        else:
            assert lkhaj__axb == 'float'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(arg_a,
        'pandas.to_numeric()')
    if isinstance(arg_a, (types.Array, IntegerArrayType)):
        return lambda arg_a, errors='raise', downcast=None: arg_a.astype(
            out_dtype)
    if isinstance(arg_a, SeriesType):

        def impl_series(arg_a, errors='raise', downcast=None):
            rpcrf__knhay = bodo.hiframes.pd_series_ext.get_series_data(arg_a)
            index = bodo.hiframes.pd_series_ext.get_series_index(arg_a)
            name = bodo.hiframes.pd_series_ext.get_series_name(arg_a)
            fdno__fbd = pd.to_numeric(rpcrf__knhay, errors, downcast)
            return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index,
                name)
        return impl_series
    if not is_str_arr_type(arg_a):
        raise BodoError(f'pd.to_numeric(): invalid argument type {arg_a}')
    if arg_a == bodo.dict_str_arr_type:
        return (lambda arg_a, errors='raise', downcast=None: bodo.libs.
            dict_arr_ext.dict_arr_to_numeric(arg_a, errors, downcast))
    jjn__gpqeh = types.Array(types.float64, 1, 'C'
        ) if out_dtype == types.float64 else IntegerArrayType(types.int64)

    def to_numeric_impl(arg_a, errors='raise', downcast=None):
        numba.parfors.parfor.init_prange()
        n = len(arg_a)
        vvjsj__pnw = bodo.utils.utils.alloc_type(n, jjn__gpqeh, (-1,))
        for tys__niduj in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arg_a, tys__niduj):
                bodo.libs.array_kernels.setna(vvjsj__pnw, tys__niduj)
            else:
                bodo.libs.str_arr_ext.str_arr_item_to_numeric(vvjsj__pnw,
                    tys__niduj, arg_a, tys__niduj)
        return vvjsj__pnw
    return to_numeric_impl


def series_filter_bool(arr, bool_arr):
    return arr[bool_arr]


@infer_global(series_filter_bool)
class SeriesFilterBoolInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        juljx__nxk = if_series_to_array_type(args[0])
        if isinstance(juljx__nxk, types.Array) and isinstance(juljx__nxk.
            dtype, types.Integer):
            juljx__nxk = types.Array(types.float64, 1, 'C')
        return juljx__nxk(*args)


def where_impl_one_arg(c):
    return np.where(c)


@overload(where_impl_one_arg, no_unliteral=True)
def overload_where_unsupported_one_arg(condition):
    if isinstance(condition, SeriesType) or bodo.utils.utils.is_array_typ(
        condition, False):
        return lambda condition: np.where(condition)


def overload_np_where_one_arg(condition):
    if isinstance(condition, SeriesType):

        def impl_series(condition):
            condition = bodo.hiframes.pd_series_ext.get_series_data(condition)
            return bodo.libs.array_kernels.nonzero(condition)
        return impl_series
    elif bodo.utils.utils.is_array_typ(condition, False):

        def impl(condition):
            return bodo.libs.array_kernels.nonzero(condition)
        return impl


overload(np.where, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)
overload(where_impl_one_arg, inline='always', no_unliteral=True)(
    overload_np_where_one_arg)


def where_impl(c, x, y):
    return np.where(c, x, y)


@overload(where_impl, no_unliteral=True)
def overload_where_unsupported(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return lambda condition, x, y: np.where(condition, x, y)


@overload(where_impl, no_unliteral=True)
@overload(np.where, no_unliteral=True)
def overload_np_where(condition, x, y):
    if not isinstance(condition, (SeriesType, types.Array, BooleanArrayType)
        ) or condition.ndim != 1:
        return
    assert condition.dtype == types.bool_, 'invalid condition dtype'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(x,
        'numpy.where()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(y,
        'numpy.where()')
    mlwb__mfnyl = bodo.utils.utils.is_array_typ(x, True)
    drg__kmpdq = bodo.utils.utils.is_array_typ(y, True)
    kld__zjlce = 'def _impl(condition, x, y):\n'
    if isinstance(condition, SeriesType):
        kld__zjlce += (
            '  condition = bodo.hiframes.pd_series_ext.get_series_data(condition)\n'
            )
    if mlwb__mfnyl and not bodo.utils.utils.is_array_typ(x, False):
        kld__zjlce += '  x = bodo.utils.conversion.coerce_to_array(x)\n'
    if drg__kmpdq and not bodo.utils.utils.is_array_typ(y, False):
        kld__zjlce += '  y = bodo.utils.conversion.coerce_to_array(y)\n'
    kld__zjlce += '  n = len(condition)\n'
    pmhp__dzmm = x.dtype if mlwb__mfnyl else types.unliteral(x)
    orjp__sqktl = y.dtype if drg__kmpdq else types.unliteral(y)
    if not isinstance(x, CategoricalArrayType):
        pmhp__dzmm = element_type(x)
    if not isinstance(y, CategoricalArrayType):
        orjp__sqktl = element_type(y)

    def get_data(x):
        if isinstance(x, SeriesType):
            return x.data
        elif isinstance(x, types.Array):
            return x
        return types.unliteral(x)
    omufb__cqm = get_data(x)
    kbibu__eid = get_data(y)
    is_nullable = any(bodo.utils.typing.is_nullable(kvgy__xstcd) for
        kvgy__xstcd in [omufb__cqm, kbibu__eid])
    if kbibu__eid == types.none:
        if isinstance(pmhp__dzmm, types.Number):
            out_dtype = types.Array(types.float64, 1, 'C')
        else:
            out_dtype = to_nullable_type(x)
    elif omufb__cqm == kbibu__eid and not is_nullable:
        out_dtype = dtype_to_array_type(pmhp__dzmm)
    elif pmhp__dzmm == string_type or orjp__sqktl == string_type:
        out_dtype = bodo.string_array_type
    elif omufb__cqm == bytes_type or (mlwb__mfnyl and pmhp__dzmm == bytes_type
        ) and (kbibu__eid == bytes_type or drg__kmpdq and orjp__sqktl ==
        bytes_type):
        out_dtype = binary_array_type
    elif isinstance(pmhp__dzmm, bodo.PDCategoricalDtype):
        out_dtype = None
    elif pmhp__dzmm in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(pmhp__dzmm, 1, 'C')
    elif orjp__sqktl in [bodo.timedelta64ns, bodo.datetime64ns]:
        out_dtype = types.Array(orjp__sqktl, 1, 'C')
    else:
        out_dtype = numba.from_dtype(np.promote_types(numba.np.
            numpy_support.as_dtype(pmhp__dzmm), numba.np.numpy_support.
            as_dtype(orjp__sqktl)))
        out_dtype = types.Array(out_dtype, 1, 'C')
        if is_nullable:
            out_dtype = bodo.utils.typing.to_nullable_type(out_dtype)
    if isinstance(pmhp__dzmm, bodo.PDCategoricalDtype):
        vpnlv__ruqkm = 'x'
    else:
        vpnlv__ruqkm = 'out_dtype'
    kld__zjlce += (
        f'  out_arr = bodo.utils.utils.alloc_type(n, {vpnlv__ruqkm}, (-1,))\n')
    if isinstance(pmhp__dzmm, bodo.PDCategoricalDtype):
        kld__zjlce += """  out_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(out_arr)
"""
        kld__zjlce += (
            '  x_codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(x)\n'
            )
    kld__zjlce += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    kld__zjlce += (
        '    if not bodo.libs.array_kernels.isna(condition, j) and condition[j]:\n'
        )
    if mlwb__mfnyl:
        kld__zjlce += '      if bodo.libs.array_kernels.isna(x, j):\n'
        kld__zjlce += '        setna(out_arr, j)\n'
        kld__zjlce += '        continue\n'
    if isinstance(pmhp__dzmm, bodo.PDCategoricalDtype):
        kld__zjlce += '      out_codes[j] = x_codes[j]\n'
    else:
        kld__zjlce += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_tz_naive_timestamp({})\n'
            .format('x[j]' if mlwb__mfnyl else 'x'))
    kld__zjlce += '    else:\n'
    if drg__kmpdq:
        kld__zjlce += '      if bodo.libs.array_kernels.isna(y, j):\n'
        kld__zjlce += '        setna(out_arr, j)\n'
        kld__zjlce += '        continue\n'
    if kbibu__eid == types.none:
        if isinstance(pmhp__dzmm, bodo.PDCategoricalDtype):
            kld__zjlce += '      out_codes[j] = -1\n'
        else:
            kld__zjlce += '      setna(out_arr, j)\n'
    else:
        kld__zjlce += (
            '      out_arr[j] = bodo.utils.conversion.unbox_if_tz_naive_timestamp({})\n'
            .format('y[j]' if drg__kmpdq else 'y'))
    kld__zjlce += '  return out_arr\n'
    ucijt__sjfar = {}
    exec(kld__zjlce, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'out_dtype': out_dtype}, ucijt__sjfar)
    eowel__yoluh = ucijt__sjfar['_impl']
    return eowel__yoluh


def _verify_np_select_arg_typs(condlist, choicelist, default):
    if isinstance(condlist, (types.List, types.UniTuple)):
        if not (bodo.utils.utils.is_np_array_typ(condlist.dtype) and 
            condlist.dtype.dtype == types.bool_):
            raise BodoError(
                "np.select(): 'condlist' argument must be list or tuple of boolean ndarrays. If passing a Series, please convert with pd.Series.to_numpy()."
                )
    else:
        raise BodoError(
            "np.select(): 'condlist' argument must be list or tuple of boolean ndarrays. If passing a Series, please convert with pd.Series.to_numpy()."
            )
    if not isinstance(choicelist, (types.List, types.UniTuple, types.BaseTuple)
        ):
        raise BodoError(
            "np.select(): 'choicelist' argument must be list or tuple type")
    if isinstance(choicelist, (types.List, types.UniTuple)):
        hpe__icg = choicelist.dtype
        if not bodo.utils.utils.is_array_typ(hpe__icg, True):
            raise BodoError(
                "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                )
        if is_series_type(hpe__icg):
            xdn__jshjp = hpe__icg.data.dtype
        else:
            xdn__jshjp = hpe__icg.dtype
        if isinstance(xdn__jshjp, bodo.PDCategoricalDtype):
            raise BodoError(
                'np.select(): data with choicelist of type Categorical not yet supported'
                )
        xanz__ujh = hpe__icg
    else:
        psec__wsn = []
        for hpe__icg in choicelist:
            if not bodo.utils.utils.is_array_typ(hpe__icg, True):
                raise BodoError(
                    "np.select(): 'choicelist' argument must be list or tuple of series/arrays types"
                    )
            if is_series_type(hpe__icg):
                xdn__jshjp = hpe__icg.data.dtype
            else:
                xdn__jshjp = hpe__icg.dtype
            if isinstance(xdn__jshjp, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            psec__wsn.append(xdn__jshjp)
        if not is_common_scalar_dtype(psec__wsn):
            raise BodoError(
                f"np.select(): 'choicelist' items must be arrays with a commmon data type. Found a tuple with the following data types {choicelist}."
                )
        xanz__ujh = choicelist[0]
    if is_series_type(xanz__ujh):
        xanz__ujh = xanz__ujh.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        pass
    else:
        if not is_scalar_type(default):
            raise BodoError(
                "np.select(): 'default' argument must be scalar type")
        if not (is_common_scalar_dtype([default, xanz__ujh.dtype]) or 
            default == types.none or is_overload_constant_nan(default)):
            raise BodoError(
                f"np.select(): 'default' is not type compatible with the array types in choicelist. Choicelist type: {choicelist}, Default type: {default}"
                )
    if not (isinstance(xanz__ujh, types.Array) or isinstance(xanz__ujh,
        BooleanArrayType) or isinstance(xanz__ujh, IntegerArrayType) or
        isinstance(xanz__ujh, FloatingArrayType) or bodo.utils.utils.
        is_array_typ(xanz__ujh, False) and xanz__ujh.dtype in [bodo.
        string_type, bodo.bytes_type]):
        raise BodoError(
            f'np.select(): data with choicelist of type {xanz__ujh} not yet supported'
            )


@overload(np.select)
def overload_np_select(condlist, choicelist, default=0):
    _verify_np_select_arg_typs(condlist, choicelist, default)
    ybxwj__ohf = isinstance(choicelist, (types.List, types.UniTuple)
        ) and isinstance(condlist, (types.List, types.UniTuple))
    if isinstance(choicelist, (types.List, types.UniTuple)):
        vxpvo__hox = choicelist.dtype
    else:
        dwa__nilhj = False
        psec__wsn = []
        for hpe__icg in choicelist:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(hpe__icg,
                'numpy.select()')
            if is_nullable_type(hpe__icg):
                dwa__nilhj = True
            if is_series_type(hpe__icg):
                xdn__jshjp = hpe__icg.data.dtype
            else:
                xdn__jshjp = hpe__icg.dtype
            if isinstance(xdn__jshjp, bodo.PDCategoricalDtype):
                raise BodoError(
                    'np.select(): data with choicelist of type Categorical not yet supported'
                    )
            psec__wsn.append(xdn__jshjp)
        fii__syqq, jfidl__ums = get_common_scalar_dtype(psec__wsn)
        if not jfidl__ums:
            raise BodoError('Internal error in overload_np_select')
        nsqi__camp = dtype_to_array_type(fii__syqq)
        if dwa__nilhj:
            nsqi__camp = to_nullable_type(nsqi__camp)
        vxpvo__hox = nsqi__camp
    if isinstance(vxpvo__hox, SeriesType):
        vxpvo__hox = vxpvo__hox.data
    if is_overload_constant_int(default) and get_overload_const_int(default
        ) == 0:
        kkzg__dkggl = True
    else:
        kkzg__dkggl = False
    sbyws__jjzv = False
    bggk__dfoul = False
    if kkzg__dkggl:
        if isinstance(vxpvo__hox.dtype, types.Number):
            pass
        elif vxpvo__hox.dtype == types.bool_:
            bggk__dfoul = True
        else:
            sbyws__jjzv = True
            vxpvo__hox = to_nullable_type(vxpvo__hox)
    elif default == types.none or is_overload_constant_nan(default):
        sbyws__jjzv = True
        vxpvo__hox = to_nullable_type(vxpvo__hox)
    kld__zjlce = 'def np_select_impl(condlist, choicelist, default=0):\n'
    kld__zjlce += '  if len(condlist) != len(choicelist):\n'
    kld__zjlce += """    raise ValueError('list of cases must be same length as list of conditions')
"""
    kld__zjlce += '  output_len = len(choicelist[0])\n'
    kld__zjlce += (
        '  out = bodo.utils.utils.alloc_type(output_len, alloc_typ, (-1,))\n')
    kld__zjlce += '  for i in range(output_len):\n'
    if sbyws__jjzv:
        kld__zjlce += '    bodo.libs.array_kernels.setna(out, i)\n'
    elif bggk__dfoul:
        kld__zjlce += '    out[i] = False\n'
    else:
        kld__zjlce += '    out[i] = default\n'
    if ybxwj__ohf:
        kld__zjlce += '  for i in range(len(condlist) - 1, -1, -1):\n'
        kld__zjlce += '    cond = condlist[i]\n'
        kld__zjlce += '    choice = choicelist[i]\n'
        kld__zjlce += '    out = np.where(cond, choice, out)\n'
    else:
        for tys__niduj in range(len(choicelist) - 1, -1, -1):
            kld__zjlce += f'  cond = condlist[{tys__niduj}]\n'
            kld__zjlce += f'  choice = choicelist[{tys__niduj}]\n'
            kld__zjlce += f'  out = np.where(cond, choice, out)\n'
    kld__zjlce += '  return out'
    ucijt__sjfar = dict()
    exec(kld__zjlce, {'bodo': bodo, 'numba': numba, 'setna': bodo.libs.
        array_kernels.setna, 'np': np, 'alloc_typ': vxpvo__hox}, ucijt__sjfar)
    impl = ucijt__sjfar['np_select_impl']
    return impl


@overload_method(SeriesType, 'duplicated', inline='always', no_unliteral=True)
def overload_series_duplicated(S, keep='first'):

    def impl(S, keep='first'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        fdno__fbd = bodo.libs.array_kernels.duplicated((arr,))
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index, name)
    return impl


@overload_method(SeriesType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_series_drop_duplicates(S, subset=None, keep='first', inplace=False
    ):
    xjc__qmsn = dict(subset=subset, keep=keep, inplace=inplace)
    jrco__lxxs = dict(subset=None, keep='first', inplace=False)
    check_unsupported_args('Series.drop_duplicates', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')

    def impl(S, subset=None, keep='first', inplace=False):
        crm__gdy = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        (crm__gdy,), wldxr__prmbi = bodo.libs.array_kernels.drop_duplicates((
            crm__gdy,), index, 1)
        index = bodo.utils.conversion.index_from_array(wldxr__prmbi)
        return bodo.hiframes.pd_series_ext.init_series(crm__gdy, index, name)
    return impl


@overload_method(SeriesType, 'between', inline='always', no_unliteral=True)
def overload_series_between(S, left, right, inclusive='both'):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(left,
        'Series.between()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(right,
        'Series.between()')
    mwpgh__gtqzz = element_type(S.data)
    if not is_common_scalar_dtype([mwpgh__gtqzz, left]):
        raise_bodo_error(
            "Series.between(): 'left' must be compariable with the Series data"
            )
    if not is_common_scalar_dtype([mwpgh__gtqzz, right]):
        raise_bodo_error(
            "Series.between(): 'right' must be compariable with the Series data"
            )
    if not is_overload_constant_str(inclusive) or get_overload_const_str(
        inclusive) not in ('both', 'neither'):
        raise_bodo_error(
            "Series.between(): 'inclusive' must be a constant string and one of ('both', 'neither')"
            )

    def impl(S, left, right, inclusive='both'):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(arr)
        fdno__fbd = bodo.libs.bool_arr_ext.alloc_bool_array(n)
        for tys__niduj in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(arr, tys__niduj):
                bodo.libs.array_kernels.setna(fdno__fbd, tys__niduj)
                continue
            frmcf__lqzc = bodo.utils.conversion.box_if_dt64(arr[tys__niduj])
            if inclusive == 'both':
                fdno__fbd[tys__niduj
                    ] = frmcf__lqzc <= right and frmcf__lqzc >= left
            else:
                fdno__fbd[tys__niduj
                    ] = frmcf__lqzc < right and frmcf__lqzc > left
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd, index, name)
    return impl


@overload_method(SeriesType, 'repeat', inline='always', no_unliteral=True)
def overload_series_repeat(S, repeats, axis=None):
    xjc__qmsn = dict(axis=axis)
    jrco__lxxs = dict(axis=None)
    check_unsupported_args('Series.repeat', xjc__qmsn, jrco__lxxs,
        package_name='pandas', module_name='Series')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S,
        'Series.repeat()')
    if not (isinstance(repeats, types.Integer) or is_iterable_type(repeats) and
        isinstance(repeats.dtype, types.Integer)):
        raise BodoError(
            "Series.repeat(): 'repeats' should be an integer or array of integers"
            )
    if isinstance(repeats, types.Integer):

        def impl_int(S, repeats, axis=None):
            arr = bodo.hiframes.pd_series_ext.get_series_data(S)
            index = bodo.hiframes.pd_series_ext.get_series_index(S)
            name = bodo.hiframes.pd_series_ext.get_series_name(S)
            wldxr__prmbi = bodo.utils.conversion.index_to_array(index)
            fdno__fbd = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
            xgku__yiwf = bodo.libs.array_kernels.repeat_kernel(wldxr__prmbi,
                repeats)
            ngbtj__job = bodo.utils.conversion.index_from_array(xgku__yiwf)
            return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
                ngbtj__job, name)
        return impl_int

    def impl_arr(S, repeats, axis=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        name = bodo.hiframes.pd_series_ext.get_series_name(S)
        wldxr__prmbi = bodo.utils.conversion.index_to_array(index)
        repeats = bodo.utils.conversion.coerce_to_array(repeats)
        fdno__fbd = bodo.libs.array_kernels.repeat_kernel(arr, repeats)
        xgku__yiwf = bodo.libs.array_kernels.repeat_kernel(wldxr__prmbi,
            repeats)
        ngbtj__job = bodo.utils.conversion.index_from_array(xgku__yiwf)
        return bodo.hiframes.pd_series_ext.init_series(fdno__fbd,
            ngbtj__job, name)
    return impl_arr


@overload_method(SeriesType, 'to_dict', no_unliteral=True)
def overload_to_dict(S, into=None):

    def impl(S, into=None):
        kvgy__xstcd = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.utils.conversion.index_to_array(bodo.hiframes.
            pd_series_ext.get_series_index(S))
        n = len(kvgy__xstcd)
        tnpnj__fbh = {}
        for tys__niduj in range(n):
            frmcf__lqzc = bodo.utils.conversion.box_if_dt64(kvgy__xstcd[
                tys__niduj])
            tnpnj__fbh[index[tys__niduj]] = frmcf__lqzc
        return tnpnj__fbh
    return impl


@overload_method(SeriesType, 'to_frame', inline='always', no_unliteral=True)
def overload_series_to_frame(S, name=None):
    svqrl__eghd = (
        "Series.to_frame(): output column name should be known at compile time. Set 'name' to a constant value."
        )
    if is_overload_none(name):
        if is_literal_type(S.name_typ):
            eily__kzjw = get_literal_value(S.name_typ)
        else:
            raise_bodo_error(svqrl__eghd)
    elif is_literal_type(name):
        eily__kzjw = get_literal_value(name)
    else:
        raise_bodo_error(svqrl__eghd)
    eily__kzjw = 0 if eily__kzjw is None else eily__kzjw
    dpnos__pjn = ColNamesMetaType((eily__kzjw,))

    def impl(S, name=None):
        arr = bodo.hiframes.pd_series_ext.get_series_data(S)
        index = bodo.hiframes.pd_series_ext.get_series_index(S)
        return bodo.hiframes.pd_dataframe_ext.init_dataframe((arr,), index,
            dpnos__pjn)
    return impl


@overload_method(SeriesType, 'keys', inline='always', no_unliteral=True)
def overload_series_keys(S):

    def impl(S):
        return bodo.hiframes.pd_series_ext.get_series_index(S)
    return impl
