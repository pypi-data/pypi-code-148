"""
Implements array operations for usage by DataFrames and Series
such as count and max.
"""
import numba
import numpy as np
import pandas as pd
from numba import generated_jit
from numba.core import types
from numba.extending import overload
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.utils import tracing
from bodo.utils.typing import element_type, is_hashable_type, is_iterable_type, is_overload_true, is_overload_zero, is_str_arr_type


def array_op_any(arr, skipna=True):
    pass


@overload(array_op_any)
def overload_array_op_any(A, skipna=True):
    if isinstance(A, types.Array) and isinstance(A.dtype, types.Integer
        ) or isinstance(A, bodo.libs.int_arr_ext.IntegerArrayType):
        lgwzu__emgsw = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        lgwzu__emgsw = False
    elif A == bodo.string_array_type:
        lgwzu__emgsw = ''
    elif A == bodo.binary_array_type:
        lgwzu__emgsw = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform any with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        rwob__fap = 0
        for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, kuqk__dryfh):
                if A[kuqk__dryfh] != lgwzu__emgsw:
                    rwob__fap += 1
        return rwob__fap != 0
    return impl


def array_op_all(arr, skipna=True):
    pass


@overload(array_op_all)
def overload_array_op_all(A, skipna=True):
    if isinstance(A, types.Array) and isinstance(A.dtype, types.Integer
        ) or isinstance(A, bodo.libs.int_arr_ext.IntegerArrayType):
        lgwzu__emgsw = 0
    elif isinstance(A, bodo.libs.bool_arr_ext.BooleanArrayType) or isinstance(A
        , types.Array) and A.dtype == types.bool_:
        lgwzu__emgsw = False
    elif A == bodo.string_array_type:
        lgwzu__emgsw = ''
    elif A == bodo.binary_array_type:
        lgwzu__emgsw = b''
    else:
        raise bodo.utils.typing.BodoError(
            f'Cannot perform all with this array type: {A}')

    def impl(A, skipna=True):
        numba.parfors.parfor.init_prange()
        rwob__fap = 0
        for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(A)):
            if not bodo.libs.array_kernels.isna(A, kuqk__dryfh):
                if A[kuqk__dryfh] == lgwzu__emgsw:
                    rwob__fap += 1
        return rwob__fap == 0
    return impl


@numba.njit
def array_op_median(arr, skipna=True, parallel=False):
    cjpge__rxpw = np.empty(1, types.float64)
    bodo.libs.array_kernels.median_series_computation(cjpge__rxpw.ctypes,
        arr, parallel, skipna)
    return cjpge__rxpw[0]


def array_op_isna(arr):
    pass


@overload(array_op_isna)
def overload_array_op_isna(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        mpzg__cphvu = len(arr)
        hxxz__vdoa = np.empty(mpzg__cphvu, np.bool_)
        for kuqk__dryfh in numba.parfors.parfor.internal_prange(mpzg__cphvu):
            hxxz__vdoa[kuqk__dryfh] = bodo.libs.array_kernels.isna(arr,
                kuqk__dryfh)
        return hxxz__vdoa
    return impl


def array_op_count(arr):
    pass


@overload(array_op_count)
def overload_array_op_count(arr):

    def impl(arr):
        numba.parfors.parfor.init_prange()
        rwob__fap = 0
        for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(arr)):
            cdj__wpov = 0
            if not bodo.libs.array_kernels.isna(arr, kuqk__dryfh):
                cdj__wpov = 1
            rwob__fap += cdj__wpov
        cjpge__rxpw = rwob__fap
        return cjpge__rxpw
    return impl


def array_op_describe(arr):
    pass


def array_op_describe_impl(arr):
    adqp__xugga = array_op_count(arr)
    qjdbq__qcuob = array_op_min(arr)
    xaam__dyg = array_op_max(arr)
    qbgmh__uvmln = array_op_mean(arr)
    pdw__wkhzf = array_op_std(arr)
    rvq__oclxq = array_op_quantile(arr, 0.25)
    byrr__yjsf = array_op_quantile(arr, 0.5)
    pgp__lfw = array_op_quantile(arr, 0.75)
    return (adqp__xugga, qbgmh__uvmln, pdw__wkhzf, qjdbq__qcuob, rvq__oclxq,
        byrr__yjsf, pgp__lfw, xaam__dyg)


def array_op_describe_dt_impl(arr):
    adqp__xugga = array_op_count(arr)
    qjdbq__qcuob = array_op_min(arr)
    xaam__dyg = array_op_max(arr)
    qbgmh__uvmln = array_op_mean(arr)
    rvq__oclxq = array_op_quantile(arr, 0.25)
    byrr__yjsf = array_op_quantile(arr, 0.5)
    pgp__lfw = array_op_quantile(arr, 0.75)
    return (adqp__xugga, qbgmh__uvmln, qjdbq__qcuob, rvq__oclxq, byrr__yjsf,
        pgp__lfw, xaam__dyg)


@overload(array_op_describe)
def overload_array_op_describe(arr):
    if arr.dtype == bodo.datetime64ns:
        return array_op_describe_dt_impl
    return array_op_describe_impl


@generated_jit(nopython=True)
def array_op_nbytes(arr):
    return array_op_nbytes_impl


def array_op_nbytes_impl(arr):
    return arr.nbytes


def array_op_min(arr):
    pass


@overload(array_op_min)
def overload_array_op_min(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            pyzdw__qteij = numba.cpython.builtins.get_type_max_value(np.int64)
            rwob__fap = 0
            for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(arr)):
                fnyd__yqkxj = pyzdw__qteij
                cdj__wpov = 0
                if not bodo.libs.array_kernels.isna(arr, kuqk__dryfh):
                    fnyd__yqkxj = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[kuqk__dryfh]))
                    cdj__wpov = 1
                pyzdw__qteij = min(pyzdw__qteij, fnyd__yqkxj)
                rwob__fap += cdj__wpov
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(pyzdw__qteij,
                rwob__fap)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            pyzdw__qteij = numba.cpython.builtins.get_type_max_value(np.int64)
            rwob__fap = 0
            for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(arr)):
                fnyd__yqkxj = pyzdw__qteij
                cdj__wpov = 0
                if not bodo.libs.array_kernels.isna(arr, kuqk__dryfh):
                    fnyd__yqkxj = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[kuqk__dryfh]))
                    cdj__wpov = 1
                pyzdw__qteij = min(pyzdw__qteij, fnyd__yqkxj)
                rwob__fap += cdj__wpov
            return bodo.hiframes.pd_index_ext._dti_val_finalize(pyzdw__qteij,
                rwob__fap)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            bat__clit = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            pyzdw__qteij = numba.cpython.builtins.get_type_max_value(np.int64)
            rwob__fap = 0
            for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(
                bat__clit)):
                naco__jrp = bat__clit[kuqk__dryfh]
                if naco__jrp == -1:
                    continue
                pyzdw__qteij = min(pyzdw__qteij, naco__jrp)
                rwob__fap += 1
            cjpge__rxpw = bodo.hiframes.series_kernels._box_cat_val(
                pyzdw__qteij, arr.dtype, rwob__fap)
            return cjpge__rxpw
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            pyzdw__qteij = bodo.hiframes.series_kernels._get_date_max_value()
            rwob__fap = 0
            for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(arr)):
                fnyd__yqkxj = pyzdw__qteij
                cdj__wpov = 0
                if not bodo.libs.array_kernels.isna(arr, kuqk__dryfh):
                    fnyd__yqkxj = arr[kuqk__dryfh]
                    cdj__wpov = 1
                pyzdw__qteij = min(pyzdw__qteij, fnyd__yqkxj)
                rwob__fap += cdj__wpov
            cjpge__rxpw = bodo.hiframes.series_kernels._sum_handle_nan(
                pyzdw__qteij, rwob__fap)
            return cjpge__rxpw
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        pyzdw__qteij = bodo.hiframes.series_kernels._get_type_max_value(arr
            .dtype)
        rwob__fap = 0
        for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(arr)):
            fnyd__yqkxj = pyzdw__qteij
            cdj__wpov = 0
            if not bodo.libs.array_kernels.isna(arr, kuqk__dryfh):
                fnyd__yqkxj = arr[kuqk__dryfh]
                cdj__wpov = 1
            pyzdw__qteij = min(pyzdw__qteij, fnyd__yqkxj)
            rwob__fap += cdj__wpov
        cjpge__rxpw = bodo.hiframes.series_kernels._sum_handle_nan(pyzdw__qteij
            , rwob__fap)
        return cjpge__rxpw
    return impl


def array_op_max(arr):
    pass


@overload(array_op_max)
def overload_array_op_max(arr):
    if arr.dtype == bodo.timedelta64ns:

        def impl_td64(arr):
            numba.parfors.parfor.init_prange()
            pyzdw__qteij = numba.cpython.builtins.get_type_min_value(np.int64)
            rwob__fap = 0
            for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(arr)):
                fnyd__yqkxj = pyzdw__qteij
                cdj__wpov = 0
                if not bodo.libs.array_kernels.isna(arr, kuqk__dryfh):
                    fnyd__yqkxj = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(arr[kuqk__dryfh]))
                    cdj__wpov = 1
                pyzdw__qteij = max(pyzdw__qteij, fnyd__yqkxj)
                rwob__fap += cdj__wpov
            return bodo.hiframes.pd_index_ext._tdi_val_finalize(pyzdw__qteij,
                rwob__fap)
        return impl_td64
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr):
            numba.parfors.parfor.init_prange()
            pyzdw__qteij = numba.cpython.builtins.get_type_min_value(np.int64)
            rwob__fap = 0
            for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(arr)):
                fnyd__yqkxj = pyzdw__qteij
                cdj__wpov = 0
                if not bodo.libs.array_kernels.isna(arr, kuqk__dryfh):
                    fnyd__yqkxj = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(arr[kuqk__dryfh]))
                    cdj__wpov = 1
                pyzdw__qteij = max(pyzdw__qteij, fnyd__yqkxj)
                rwob__fap += cdj__wpov
            return bodo.hiframes.pd_index_ext._dti_val_finalize(pyzdw__qteij,
                rwob__fap)
        return impl_dt64
    if isinstance(arr, CategoricalArrayType):

        def impl_cat(arr):
            bat__clit = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(arr))
            numba.parfors.parfor.init_prange()
            pyzdw__qteij = -1
            for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(
                bat__clit)):
                pyzdw__qteij = max(pyzdw__qteij, bat__clit[kuqk__dryfh])
            cjpge__rxpw = bodo.hiframes.series_kernels._box_cat_val(
                pyzdw__qteij, arr.dtype, 1)
            return cjpge__rxpw
        return impl_cat
    if arr == datetime_date_array_type:

        def impl_date(arr):
            numba.parfors.parfor.init_prange()
            pyzdw__qteij = bodo.hiframes.series_kernels._get_date_min_value()
            rwob__fap = 0
            for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(arr)):
                fnyd__yqkxj = pyzdw__qteij
                cdj__wpov = 0
                if not bodo.libs.array_kernels.isna(arr, kuqk__dryfh):
                    fnyd__yqkxj = arr[kuqk__dryfh]
                    cdj__wpov = 1
                pyzdw__qteij = max(pyzdw__qteij, fnyd__yqkxj)
                rwob__fap += cdj__wpov
            cjpge__rxpw = bodo.hiframes.series_kernels._sum_handle_nan(
                pyzdw__qteij, rwob__fap)
            return cjpge__rxpw
        return impl_date

    def impl(arr):
        numba.parfors.parfor.init_prange()
        pyzdw__qteij = bodo.hiframes.series_kernels._get_type_min_value(arr
            .dtype)
        rwob__fap = 0
        for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(arr)):
            fnyd__yqkxj = pyzdw__qteij
            cdj__wpov = 0
            if not bodo.libs.array_kernels.isna(arr, kuqk__dryfh):
                fnyd__yqkxj = arr[kuqk__dryfh]
                cdj__wpov = 1
            pyzdw__qteij = max(pyzdw__qteij, fnyd__yqkxj)
            rwob__fap += cdj__wpov
        cjpge__rxpw = bodo.hiframes.series_kernels._sum_handle_nan(pyzdw__qteij
            , rwob__fap)
        return cjpge__rxpw
    return impl


def array_op_mean(arr):
    pass


@overload(array_op_mean)
def overload_array_op_mean(arr):
    if arr.dtype == bodo.datetime64ns:

        def impl(arr):
            return pd.Timestamp(types.int64(bodo.libs.array_ops.
                array_op_mean(arr.view(np.int64))))
        return impl
    gtrjx__fzetw = types.float64
    ohn__zivd = types.float64
    if isinstance(arr, types.Array) and arr.dtype == types.float32:
        gtrjx__fzetw = types.float32
        ohn__zivd = types.float32
    nimko__wdkp = gtrjx__fzetw(0)
    paq__ntsq = ohn__zivd(0)
    jxfk__zjhy = ohn__zivd(1)

    def impl(arr):
        numba.parfors.parfor.init_prange()
        pyzdw__qteij = nimko__wdkp
        rwob__fap = paq__ntsq
        for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(arr)):
            fnyd__yqkxj = nimko__wdkp
            cdj__wpov = paq__ntsq
            if not bodo.libs.array_kernels.isna(arr, kuqk__dryfh):
                fnyd__yqkxj = arr[kuqk__dryfh]
                cdj__wpov = jxfk__zjhy
            pyzdw__qteij += fnyd__yqkxj
            rwob__fap += cdj__wpov
        cjpge__rxpw = bodo.hiframes.series_kernels._mean_handle_nan(
            pyzdw__qteij, rwob__fap)
        return cjpge__rxpw
    return impl


def array_op_var(arr, skipna, ddof):
    pass


@overload(array_op_var)
def overload_array_op_var(arr, skipna, ddof):

    def impl(arr, skipna, ddof):
        numba.parfors.parfor.init_prange()
        imz__bdnmb = 0.0
        wxgm__awla = 0.0
        rwob__fap = 0
        for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(arr)):
            fnyd__yqkxj = 0.0
            cdj__wpov = 0
            if not bodo.libs.array_kernels.isna(arr, kuqk__dryfh
                ) or not skipna:
                fnyd__yqkxj = arr[kuqk__dryfh]
                cdj__wpov = 1
            imz__bdnmb += fnyd__yqkxj
            wxgm__awla += fnyd__yqkxj * fnyd__yqkxj
            rwob__fap += cdj__wpov
        cjpge__rxpw = bodo.hiframes.series_kernels._compute_var_nan_count_ddof(
            imz__bdnmb, wxgm__awla, rwob__fap, ddof)
        return cjpge__rxpw
    return impl


def array_op_std(arr, skipna=True, ddof=1):
    pass


@overload(array_op_std)
def overload_array_op_std(arr, skipna=True, ddof=1):
    if arr.dtype == bodo.datetime64ns:

        def impl_dt64(arr, skipna=True, ddof=1):
            return pd.Timedelta(types.int64(array_op_var(arr.view(np.int64),
                skipna, ddof) ** 0.5))
        return impl_dt64
    return lambda arr, skipna=True, ddof=1: array_op_var(arr, skipna, ddof
        ) ** 0.5


def array_op_quantile(arr, q):
    pass


@overload(array_op_quantile)
def overload_array_op_quantile(arr, q):
    if is_iterable_type(q):
        if arr.dtype == bodo.datetime64ns:

            def _impl_list_dt(arr, q):
                hxxz__vdoa = np.empty(len(q), np.int64)
                for kuqk__dryfh in range(len(q)):
                    csed__shgcq = np.float64(q[kuqk__dryfh])
                    hxxz__vdoa[kuqk__dryfh] = bodo.libs.array_kernels.quantile(
                        arr.view(np.int64), csed__shgcq)
                return hxxz__vdoa.view(np.dtype('datetime64[ns]'))
            return _impl_list_dt

        def impl_list(arr, q):
            hxxz__vdoa = np.empty(len(q), np.float64)
            for kuqk__dryfh in range(len(q)):
                csed__shgcq = np.float64(q[kuqk__dryfh])
                hxxz__vdoa[kuqk__dryfh] = bodo.libs.array_kernels.quantile(arr,
                    csed__shgcq)
            return hxxz__vdoa
        return impl_list
    if arr.dtype == bodo.datetime64ns:

        def _impl_dt(arr, q):
            return pd.Timestamp(bodo.libs.array_kernels.quantile(arr.view(
                np.int64), np.float64(q)))
        return _impl_dt

    def impl(arr, q):
        return bodo.libs.array_kernels.quantile(arr, np.float64(q))
    return impl


def array_op_sum(arr, skipna, min_count):
    pass


@overload(array_op_sum, no_unliteral=True)
def overload_array_op_sum(arr, skipna, min_count):
    if isinstance(arr.dtype, types.Integer):
        ixi__eqyzd = types.intp
    elif arr.dtype == types.bool_:
        ixi__eqyzd = np.int64
    else:
        ixi__eqyzd = arr.dtype
    jlw__gtu = ixi__eqyzd(0)
    if isinstance(arr.dtype, types.Float) and (not is_overload_true(skipna) or
        not is_overload_zero(min_count)):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            pyzdw__qteij = jlw__gtu
            mpzg__cphvu = len(arr)
            rwob__fap = 0
            for kuqk__dryfh in numba.parfors.parfor.internal_prange(mpzg__cphvu
                ):
                fnyd__yqkxj = jlw__gtu
                cdj__wpov = 0
                if not bodo.libs.array_kernels.isna(arr, kuqk__dryfh
                    ) or not skipna:
                    fnyd__yqkxj = arr[kuqk__dryfh]
                    cdj__wpov = 1
                pyzdw__qteij += fnyd__yqkxj
                rwob__fap += cdj__wpov
            cjpge__rxpw = bodo.hiframes.series_kernels._var_handle_mincount(
                pyzdw__qteij, rwob__fap, min_count)
            return cjpge__rxpw
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            pyzdw__qteij = jlw__gtu
            mpzg__cphvu = len(arr)
            for kuqk__dryfh in numba.parfors.parfor.internal_prange(mpzg__cphvu
                ):
                fnyd__yqkxj = jlw__gtu
                if not bodo.libs.array_kernels.isna(arr, kuqk__dryfh):
                    fnyd__yqkxj = arr[kuqk__dryfh]
                pyzdw__qteij += fnyd__yqkxj
            return pyzdw__qteij
    return impl


def array_op_prod(arr, skipna, min_count):
    pass


@overload(array_op_prod)
def overload_array_op_prod(arr, skipna, min_count):
    wlw__ghxyv = arr.dtype(1)
    if arr.dtype == types.bool_:
        wlw__ghxyv = 1
    if isinstance(arr.dtype, types.Float):

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            pyzdw__qteij = wlw__ghxyv
            rwob__fap = 0
            for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(arr)):
                fnyd__yqkxj = wlw__ghxyv
                cdj__wpov = 0
                if not bodo.libs.array_kernels.isna(arr, kuqk__dryfh
                    ) or not skipna:
                    fnyd__yqkxj = arr[kuqk__dryfh]
                    cdj__wpov = 1
                rwob__fap += cdj__wpov
                pyzdw__qteij *= fnyd__yqkxj
            cjpge__rxpw = bodo.hiframes.series_kernels._var_handle_mincount(
                pyzdw__qteij, rwob__fap, min_count)
            return cjpge__rxpw
    else:

        def impl(arr, skipna, min_count):
            numba.parfors.parfor.init_prange()
            pyzdw__qteij = wlw__ghxyv
            for kuqk__dryfh in numba.parfors.parfor.internal_prange(len(arr)):
                fnyd__yqkxj = wlw__ghxyv
                if not bodo.libs.array_kernels.isna(arr, kuqk__dryfh):
                    fnyd__yqkxj = arr[kuqk__dryfh]
                pyzdw__qteij *= fnyd__yqkxj
            return pyzdw__qteij
    return impl


def array_op_idxmax(arr, index):
    pass


@overload(array_op_idxmax, inline='always')
def overload_array_op_idxmax(arr, index):

    def impl(arr, index):
        kuqk__dryfh = bodo.libs.array_kernels._nan_argmax(arr)
        return index[kuqk__dryfh]
    return impl


def array_op_idxmin(arr, index):
    pass


@overload(array_op_idxmin, inline='always')
def overload_array_op_idxmin(arr, index):

    def impl(arr, index):
        kuqk__dryfh = bodo.libs.array_kernels._nan_argmin(arr)
        return index[kuqk__dryfh]
    return impl


def _convert_isin_values(values, use_hash_impl):
    pass


@overload(_convert_isin_values, no_unliteral=True)
def overload_convert_isin_values(values, use_hash_impl):
    if is_overload_true(use_hash_impl):

        def impl(values, use_hash_impl):
            hsrq__ask = {}
            for oqmq__wjh in values:
                hsrq__ask[bodo.utils.conversion.box_if_dt64(oqmq__wjh)] = 0
            return hsrq__ask
        return impl
    else:

        def impl(values, use_hash_impl):
            return values
        return impl


def array_op_isin(arr, values):
    pass


@overload(array_op_isin, inline='always')
def overload_array_op_isin(arr, values):
    use_hash_impl = element_type(values) == element_type(arr
        ) and is_hashable_type(element_type(values))

    def impl(arr, values):
        values = bodo.libs.array_ops._convert_isin_values(values, use_hash_impl
            )
        numba.parfors.parfor.init_prange()
        mpzg__cphvu = len(arr)
        hxxz__vdoa = np.empty(mpzg__cphvu, np.bool_)
        for kuqk__dryfh in numba.parfors.parfor.internal_prange(mpzg__cphvu):
            hxxz__vdoa[kuqk__dryfh] = bodo.utils.conversion.box_if_dt64(arr
                [kuqk__dryfh]) in values
        return hxxz__vdoa
    return impl


@generated_jit(nopython=True)
def array_unique_vector_map(in_arr_tup):
    gjt__qqsx = len(in_arr_tup) != 1
    vfyr__ftgn = list(in_arr_tup.types)
    hgf__kdd = 'def impl(in_arr_tup):\n'
    hgf__kdd += (
        "  ev = tracing.Event('array_unique_vector_map', is_parallel=False)\n")
    hgf__kdd += '  n = len(in_arr_tup[0])\n'
    if gjt__qqsx:
        gjnwb__hwt = ', '.join([f'in_arr_tup[{kuqk__dryfh}][unused]' for
            kuqk__dryfh in range(len(in_arr_tup))])
        dvxfx__dtwa = ', '.join(['False' for eidrl__xwkcf in range(len(
            in_arr_tup))])
        hgf__kdd += f"""  arr_map = {{bodo.libs.nullable_tuple_ext.build_nullable_tuple(({gjnwb__hwt},), ({dvxfx__dtwa},)): 0 for unused in range(0)}}
"""
        hgf__kdd += '  map_vector = np.empty(n, np.int64)\n'
        for kuqk__dryfh, vhv__esply in enumerate(vfyr__ftgn):
            hgf__kdd += f'  in_lst_{kuqk__dryfh} = []\n'
            if is_str_arr_type(vhv__esply):
                hgf__kdd += f'  total_len_{kuqk__dryfh} = 0\n'
            hgf__kdd += f'  null_in_lst_{kuqk__dryfh} = []\n'
        hgf__kdd += '  for i in range(n):\n'
        osyqx__ilg = ', '.join([f'in_arr_tup[{kuqk__dryfh}][i]' for
            kuqk__dryfh in range(len(vfyr__ftgn))])
        mqr__exr = ', '.join([
            f'bodo.libs.array_kernels.isna(in_arr_tup[{kuqk__dryfh}], i)' for
            kuqk__dryfh in range(len(vfyr__ftgn))])
        hgf__kdd += f"""    data_val = bodo.libs.nullable_tuple_ext.build_nullable_tuple(({osyqx__ilg},), ({mqr__exr},))
"""
        hgf__kdd += '    if data_val not in arr_map:\n'
        hgf__kdd += '      set_val = len(arr_map)\n'
        hgf__kdd += '      values_tup = data_val._data\n'
        hgf__kdd += '      nulls_tup = data_val._null_values\n'
        for kuqk__dryfh, vhv__esply in enumerate(vfyr__ftgn):
            hgf__kdd += (
                f'      in_lst_{kuqk__dryfh}.append(values_tup[{kuqk__dryfh}])\n'
                )
            hgf__kdd += (
                f'      null_in_lst_{kuqk__dryfh}.append(nulls_tup[{kuqk__dryfh}])\n'
                )
            if is_str_arr_type(vhv__esply):
                hgf__kdd += f"""      total_len_{kuqk__dryfh}  += nulls_tup[{kuqk__dryfh}] * bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr_tup[{kuqk__dryfh}], i)
"""
        hgf__kdd += '      arr_map[data_val] = len(arr_map)\n'
        hgf__kdd += '    else:\n'
        hgf__kdd += '      set_val = arr_map[data_val]\n'
        hgf__kdd += '    map_vector[i] = set_val\n'
        hgf__kdd += '  n_rows = len(arr_map)\n'
        for kuqk__dryfh, vhv__esply in enumerate(vfyr__ftgn):
            if is_str_arr_type(vhv__esply):
                hgf__kdd += f"""  out_arr_{kuqk__dryfh} = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len_{kuqk__dryfh})
"""
            else:
                hgf__kdd += f"""  out_arr_{kuqk__dryfh} = bodo.utils.utils.alloc_type(n_rows, in_arr_tup[{kuqk__dryfh}], (-1,))
"""
        hgf__kdd += '  for j in range(len(arr_map)):\n'
        for kuqk__dryfh in range(len(vfyr__ftgn)):
            hgf__kdd += f'    if null_in_lst_{kuqk__dryfh}[j]:\n'
            hgf__kdd += (
                f'      bodo.libs.array_kernels.setna(out_arr_{kuqk__dryfh}, j)\n'
                )
            hgf__kdd += '    else:\n'
            hgf__kdd += (
                f'      out_arr_{kuqk__dryfh}[j] = in_lst_{kuqk__dryfh}[j]\n')
        vkau__fts = ', '.join([f'out_arr_{kuqk__dryfh}' for kuqk__dryfh in
            range(len(vfyr__ftgn))])
        hgf__kdd += "  ev.add_attribute('n_map_entries', n_rows)\n"
        hgf__kdd += '  ev.finalize()\n'
        hgf__kdd += f'  return ({vkau__fts},), map_vector\n'
    else:
        hgf__kdd += '  in_arr = in_arr_tup[0]\n'
        hgf__kdd += (
            f'  arr_map = {{in_arr[unused]: 0 for unused in range(0)}}\n')
        hgf__kdd += '  map_vector = np.empty(n, np.int64)\n'
        hgf__kdd += '  is_na = 0\n'
        hgf__kdd += '  in_lst = []\n'
        hgf__kdd += '  na_idxs = []\n'
        if is_str_arr_type(vfyr__ftgn[0]):
            hgf__kdd += '  total_len = 0\n'
        hgf__kdd += '  for i in range(n):\n'
        hgf__kdd += '    if bodo.libs.array_kernels.isna(in_arr, i):\n'
        hgf__kdd += '      is_na = 1\n'
        hgf__kdd += '      # Always put NA in the last location.\n'
        hgf__kdd += '      # We use -1 as a placeholder\n'
        hgf__kdd += '      set_val = -1\n'
        hgf__kdd += '      na_idxs.append(i)\n'
        hgf__kdd += '    else:\n'
        hgf__kdd += '      data_val = in_arr[i]\n'
        hgf__kdd += '      if data_val not in arr_map:\n'
        hgf__kdd += '        set_val = len(arr_map)\n'
        hgf__kdd += '        in_lst.append(data_val)\n'
        if is_str_arr_type(vfyr__ftgn[0]):
            hgf__kdd += """        total_len += bodo.libs.str_arr_ext.get_str_arr_item_length(in_arr, i)
"""
        hgf__kdd += '        arr_map[data_val] = len(arr_map)\n'
        hgf__kdd += '      else:\n'
        hgf__kdd += '        set_val = arr_map[data_val]\n'
        hgf__kdd += '    map_vector[i] = set_val\n'
        hgf__kdd += '  map_vector[na_idxs] = len(arr_map)\n'
        hgf__kdd += '  n_rows = len(arr_map) + is_na\n'
        if is_str_arr_type(vfyr__ftgn[0]):
            hgf__kdd += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_rows, total_len)
"""
        else:
            hgf__kdd += (
                '  out_arr = bodo.utils.utils.alloc_type(n_rows, in_arr, (-1,))\n'
                )
        hgf__kdd += '  for j in range(len(arr_map)):\n'
        hgf__kdd += '    out_arr[j] = in_lst[j]\n'
        hgf__kdd += '  if is_na:\n'
        hgf__kdd += '    bodo.libs.array_kernels.setna(out_arr, n_rows - 1)\n'
        hgf__kdd += "  ev.add_attribute('n_map_entries', n_rows)\n"
        hgf__kdd += '  ev.finalize()\n'
        hgf__kdd += f'  return (out_arr,), map_vector\n'
    qxrin__has = {}
    exec(hgf__kdd, {'bodo': bodo, 'np': np, 'tracing': tracing}, qxrin__has)
    impl = qxrin__has['impl']
    return impl
