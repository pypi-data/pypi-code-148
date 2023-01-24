"""
Implements window/aggregation array kernels that are specific to BodoSQL.
Specifically, window/aggregation array kernels that do not concern window
frames.
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import get_overload_const_bool, get_overload_const_str, is_overload_constant_bool, is_overload_constant_str, raise_bodo_error


def rank_sql(arr_tup, method='average', pct=False):
    return


@overload(rank_sql, no_unliteral=True)
def overload_rank_sql(arr_tup, method='average', pct=False):
    if not is_overload_constant_str(method):
        raise_bodo_error(
            "Series.rank(): 'method' argument must be a constant string")
    method = get_overload_const_str(method)
    if not is_overload_constant_bool(pct):
        raise_bodo_error(
            "Series.rank(): 'pct' argument must be a constant boolean")
    pct = get_overload_const_bool(pct)
    otby__fxaz = 'def impl(arr_tup, method="average", pct=False):\n'
    if method == 'first':
        otby__fxaz += '  ret = np.arange(1, n + 1, 1, np.float64)\n'
    else:
        otby__fxaz += (
            '  obs = bodo.libs.array_kernels._rank_detect_ties(arr_tup[0])\n')
        for wku__mgkh in range(1, len(arr_tup)):
            otby__fxaz += f"""  obs = obs | bodo.libs.array_kernels._rank_detect_ties(arr_tup[{wku__mgkh}]) 
"""
        otby__fxaz += '  dense = obs.cumsum()\n'
        if method == 'dense':
            otby__fxaz += '  ret = bodo.utils.conversion.fix_arr_dtype(\n'
            otby__fxaz += '    dense,\n'
            otby__fxaz += '    new_dtype=np.float64,\n'
            otby__fxaz += '    copy=True,\n'
            otby__fxaz += '    nan_to_str=False,\n'
            otby__fxaz += '    from_series=True,\n'
            otby__fxaz += '  )\n'
        else:
            otby__fxaz += (
                '  count = np.concatenate((np.nonzero(obs)[0], np.array([len(obs)])))\n'
                )
            otby__fxaz += """  count_float = bodo.utils.conversion.fix_arr_dtype(count, new_dtype=np.float64, copy=True, nan_to_str=False, from_series=True)
"""
            if method == 'max':
                otby__fxaz += '  ret = count_float[dense]\n'
            elif method == 'min':
                otby__fxaz += '  ret = count_float[dense - 1] + 1\n'
            else:
                otby__fxaz += (
                    '  ret = 0.5 * (count_float[dense] + count_float[dense - 1] + 1)\n'
                    )
    if pct:
        if method == 'dense':
            otby__fxaz += '  div_val = np.max(ret)\n'
        else:
            otby__fxaz += '  div_val = len(arr_tup[0])\n'
        otby__fxaz += '  for i in range(len(ret)):\n'
        otby__fxaz += '    ret[i] = ret[i] / div_val\n'
    otby__fxaz += '  return ret\n'
    pdpzx__glit = {}
    exec(otby__fxaz, {'np': np, 'pd': pd, 'bodo': bodo}, pdpzx__glit)
    return pdpzx__glit['impl']


@numba.generated_jit(nopython=True)
def change_event(S):

    def impl(S):
        kxajh__brwt = bodo.hiframes.pd_series_ext.get_series_data(S)
        dcspw__tdzvm = len(kxajh__brwt)
        eprik__yevc = bodo.utils.utils.alloc_type(dcspw__tdzvm, types.
            uint64, -1)
        jkz__oxcq = -1
        for wku__mgkh in range(dcspw__tdzvm):
            eprik__yevc[wku__mgkh] = 0
            if not bodo.libs.array_kernels.isna(kxajh__brwt, wku__mgkh):
                jkz__oxcq = wku__mgkh
                break
        if jkz__oxcq != -1:
            evg__lsfwv = kxajh__brwt[jkz__oxcq]
            for wku__mgkh in range(jkz__oxcq + 1, dcspw__tdzvm):
                if bodo.libs.array_kernels.isna(kxajh__brwt, wku__mgkh
                    ) or kxajh__brwt[wku__mgkh] == evg__lsfwv:
                    eprik__yevc[wku__mgkh] = eprik__yevc[wku__mgkh - 1]
                else:
                    evg__lsfwv = kxajh__brwt[wku__mgkh]
                    eprik__yevc[wku__mgkh] = eprik__yevc[wku__mgkh - 1] + 1
        return bodo.hiframes.pd_series_ext.init_series(eprik__yevc, bodo.
            hiframes.pd_index_ext.init_range_index(0, dcspw__tdzvm, 1), None)
    return impl


@numba.generated_jit(nopython=True)
def windowed_sum(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_sum', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    hqcp__bvd = 'res[i] = total'
    qemk__fcwie = 'constant_value = S.sum()'
    rrrq__cmu = 'total = 0'
    btpst__yitz = 'total += elem'
    zpfl__falc = 'total -= elem'
    if isinstance(S.dtype, types.Integer):
        ueyww__bur = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    else:
        ueyww__bur = types.Array(bodo.float64, 1, 'C')
    return gen_windowed(hqcp__bvd, qemk__fcwie, ueyww__bur, setup_block=
        rrrq__cmu, enter_block=btpst__yitz, exit_block=zpfl__falc)


@numba.generated_jit(nopython=True)
def windowed_count(S, lower_bound, upper_bound):
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    hqcp__bvd = 'res[i] = in_window'
    qemk__fcwie = 'constant_value = S.count()'
    rlhp__gsd = 'res[i] = 0'
    ueyww__bur = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_windowed(hqcp__bvd, qemk__fcwie, ueyww__bur, empty_block=
        rlhp__gsd)


@numba.generated_jit(nopython=True)
def windowed_avg(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_avg', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    hqcp__bvd = 'res[i] = total / in_window'
    qemk__fcwie = 'constant_value = S.mean()'
    ueyww__bur = types.Array(bodo.float64, 1, 'C')
    rrrq__cmu = 'total = 0'
    btpst__yitz = 'total += elem'
    zpfl__falc = 'total -= elem'
    return gen_windowed(hqcp__bvd, qemk__fcwie, ueyww__bur, setup_block=
        rrrq__cmu, enter_block=btpst__yitz, exit_block=zpfl__falc)


@numba.generated_jit(nopython=True)
def windowed_median(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'windowed_median', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    hqcp__bvd = 'res[i] = np.median(arr2)'
    qemk__fcwie = 'constant_value = S.median()'
    ueyww__bur = types.Array(bodo.float64, 1, 'C')
    rrrq__cmu = 'arr2 = np.zeros(0, dtype=np.float64)'
    btpst__yitz = 'arr2 = np.append(arr2, elem)'
    zpfl__falc = 'arr2 = np.delete(arr2, np.argwhere(arr2 == elem)[0])'
    return gen_windowed(hqcp__bvd, qemk__fcwie, ueyww__bur, setup_block=
        rrrq__cmu, enter_block=btpst__yitz, exit_block=zpfl__falc)


@numba.generated_jit(nopython=True)
def windowed_mode(S, lower_bound, upper_bound):
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    if isinstance(S, bodo.SeriesType):
        ueyww__bur = S.data
    else:
        ueyww__bur = S
    hqcp__bvd = 'bestVal, bestCount = None, 0\n'
    hqcp__bvd += 'for key in counts:\n'
    hqcp__bvd += '   if counts[key] > bestCount:\n'
    hqcp__bvd += '      bestVal, bestCount = key, counts[key]\n'
    hqcp__bvd += 'res[i] = bestVal'
    qemk__fcwie = 'counts = {arr[0]: 0}\n'
    qemk__fcwie += 'for i in range(len(S)):\n'
    qemk__fcwie += '   if not bodo.libs.array_kernels.isna(arr, i):\n'
    qemk__fcwie += '      counts[arr[i]] = counts.get(arr[i], 0) + 1\n'
    qemk__fcwie += hqcp__bvd.replace('res[i]', 'constant_value')
    rrrq__cmu = 'counts = {arr[0]: 0}'
    btpst__yitz = 'counts[elem] = counts.get(elem, 0) + 1'
    zpfl__falc = 'counts[elem] = counts.get(elem, 0) - 1'
    return gen_windowed(hqcp__bvd, qemk__fcwie, ueyww__bur, setup_block=
        rrrq__cmu, enter_block=btpst__yitz, exit_block=zpfl__falc)


@numba.generated_jit(nopython=True)
def windowed_ratio_to_report(S, lower_bound, upper_bound):
    verify_int_float_arg(S, 'ratio_to_report', S)
    if not bodo.utils.utils.is_array_typ(S, True):
        raise_bodo_error('Input must be an array type')
    hqcp__bvd = 'if total == 0 or bodo.libs.array_kernels.isna(arr, i):\n'
    hqcp__bvd += '   bodo.libs.array_kernels.setna(res, i)\n'
    hqcp__bvd += 'else:\n'
    hqcp__bvd += '   res[i] = arr[i] / total'
    qemk__fcwie = None
    ueyww__bur = types.Array(bodo.float64, 1, 'C')
    rrrq__cmu = 'total = 0'
    btpst__yitz = 'total += elem'
    zpfl__falc = 'total -= elem'
    return gen_windowed(hqcp__bvd, qemk__fcwie, ueyww__bur, setup_block=
        rrrq__cmu, enter_block=btpst__yitz, exit_block=zpfl__falc)
