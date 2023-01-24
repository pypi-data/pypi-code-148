"""implementations of rolling window functions (sequential and parallel)
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_builtin, overload, register_jitable
import bodo
from bodo.libs.distributed_api import Reduce_Type
from bodo.utils.typing import BodoError, decode_if_dict_array, get_overload_const_func, get_overload_const_str, is_const_func_type, is_overload_constant_bool, is_overload_constant_str, is_overload_none, is_overload_true
from bodo.utils.utils import unliteral_all
supported_rolling_funcs = ('sum', 'mean', 'var', 'std', 'count', 'median',
    'min', 'max', 'cov', 'corr', 'apply')
unsupported_rolling_methods = ['skew', 'kurt', 'aggregate', 'quantile', 'sem']


def rolling_fixed(arr, win):
    return arr


def rolling_variable(arr, on_arr, win):
    return arr


def rolling_cov(arr, arr2, win):
    return arr


def rolling_corr(arr, arr2, win):
    return arr


@infer_global(rolling_cov)
@infer_global(rolling_corr)
class RollingCovType(AbstractTemplate):

    def generic(self, args, kws):
        arr = args[0]
        ehmw__qak = arr.copy(dtype=types.float64)
        return signature(ehmw__qak, *unliteral_all(args))


@lower_builtin(rolling_corr, types.VarArg(types.Any))
@lower_builtin(rolling_cov, types.VarArg(types.Any))
def lower_rolling_corr_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


@overload(rolling_fixed, no_unliteral=True)
def overload_rolling_fixed(arr, index_arr, win, minp, center, fname, raw=
    True, parallel=False):
    assert is_overload_constant_bool(raw
        ), 'raw argument should be constant bool'
    if is_const_func_type(fname):
        func = _get_apply_func(fname)
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, func, raw))
    assert is_overload_constant_str(fname)
    gmtdl__hll = get_overload_const_str(fname)
    if gmtdl__hll not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (fixed window) function {}'.format
            (gmtdl__hll))
    if gmtdl__hll in ('median', 'min', 'max'):
        gbcw__pmmm = 'def kernel_func(A):\n'
        gbcw__pmmm += '  if np.isnan(A).sum() != 0: return np.nan\n'
        gbcw__pmmm += '  return np.{}(A)\n'.format(gmtdl__hll)
        ujyyq__mkha = {}
        exec(gbcw__pmmm, {'np': np}, ujyyq__mkha)
        kernel_func = register_jitable(ujyyq__mkha['kernel_func'])
        return (lambda arr, index_arr, win, minp, center, fname, raw=True,
            parallel=False: roll_fixed_apply(arr, index_arr, win, minp,
            center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        gmtdl__hll]
    return (lambda arr, index_arr, win, minp, center, fname, raw=True,
        parallel=False: roll_fixed_linear_generic(arr, win, minp, center,
        parallel, init_kernel, add_kernel, remove_kernel, calc_kernel))


@overload(rolling_variable, no_unliteral=True)
def overload_rolling_variable(arr, on_arr, index_arr, win, minp, center,
    fname, raw=True, parallel=False):
    assert is_overload_constant_bool(raw)
    if is_const_func_type(fname):
        func = _get_apply_func(fname)
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, func, raw))
    assert is_overload_constant_str(fname)
    gmtdl__hll = get_overload_const_str(fname)
    if gmtdl__hll not in ('sum', 'mean', 'var', 'std', 'count', 'median',
        'min', 'max'):
        raise BodoError('invalid rolling (variable window) function {}'.
            format(gmtdl__hll))
    if gmtdl__hll in ('median', 'min', 'max'):
        gbcw__pmmm = 'def kernel_func(A):\n'
        gbcw__pmmm += '  arr  = dropna(A)\n'
        gbcw__pmmm += '  if len(arr) == 0: return np.nan\n'
        gbcw__pmmm += '  return np.{}(arr)\n'.format(gmtdl__hll)
        ujyyq__mkha = {}
        exec(gbcw__pmmm, {'np': np, 'dropna': _dropna}, ujyyq__mkha)
        kernel_func = register_jitable(ujyyq__mkha['kernel_func'])
        return (lambda arr, on_arr, index_arr, win, minp, center, fname,
            raw=True, parallel=False: roll_variable_apply(arr, on_arr,
            index_arr, win, minp, center, parallel, kernel_func))
    init_kernel, add_kernel, remove_kernel, calc_kernel = linear_kernels[
        gmtdl__hll]
    return (lambda arr, on_arr, index_arr, win, minp, center, fname, raw=
        True, parallel=False: roll_var_linear_generic(arr, on_arr, win,
        minp, center, parallel, init_kernel, add_kernel, remove_kernel,
        calc_kernel))


def _get_apply_func(f_type):
    func = get_overload_const_func(f_type, None)
    return bodo.compiler.udf_jit(func)


comm_border_tag = 22


@register_jitable
def roll_fixed_linear_generic(in_arr, win, minp, center, parallel,
    init_data, add_obs, remove_obs, calc_out):
    _validate_roll_fixed_args(win, minp)
    in_arr = prep_values(in_arr)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    if parallel:
        halo_size = np.int32(win // 2) if center else np.int32(win - 1)
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data(in_arr, win, minp, center, rank,
                n_pes, init_data, add_obs, remove_obs, calc_out)
        daj__iei = _border_icomm(in_arr, rank, n_pes, halo_size, True, center)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            xyk__vbijp) = daj__iei
    output, data = roll_fixed_linear_generic_seq(in_arr, win, minp, center,
        init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(xyk__vbijp, True)
            for avi__epohz in range(0, halo_size):
                data = add_obs(r_recv_buff[avi__epohz], *data)
                ffq__blthd = in_arr[N + avi__epohz - win]
                data = remove_obs(ffq__blthd, *data)
                output[N + avi__epohz - offset] = calc_out(minp, *data)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            data = init_data()
            for avi__epohz in range(0, halo_size):
                data = add_obs(l_recv_buff[avi__epohz], *data)
            for avi__epohz in range(0, win - 1):
                data = add_obs(in_arr[avi__epohz], *data)
                if avi__epohz > offset:
                    ffq__blthd = l_recv_buff[avi__epohz - offset - 1]
                    data = remove_obs(ffq__blthd, *data)
                if avi__epohz >= offset:
                    output[avi__epohz - offset] = calc_out(minp, *data)
    return output


@register_jitable
def roll_fixed_linear_generic_seq(in_arr, win, minp, center, init_data,
    add_obs, remove_obs, calc_out):
    data = init_data()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    output = np.empty(N, dtype=np.float64)
    sodub__hgwa = max(minp, 1) - 1
    sodub__hgwa = min(sodub__hgwa, N)
    for avi__epohz in range(0, sodub__hgwa):
        data = add_obs(in_arr[avi__epohz], *data)
        if avi__epohz >= offset:
            output[avi__epohz - offset] = calc_out(minp, *data)
    for avi__epohz in range(sodub__hgwa, N):
        val = in_arr[avi__epohz]
        data = add_obs(val, *data)
        if avi__epohz > win - 1:
            ffq__blthd = in_arr[avi__epohz - win]
            data = remove_obs(ffq__blthd, *data)
        output[avi__epohz - offset] = calc_out(minp, *data)
    pfuy__wozid = data
    for avi__epohz in range(N, N + offset):
        if avi__epohz > win - 1:
            ffq__blthd = in_arr[avi__epohz - win]
            data = remove_obs(ffq__blthd, *data)
        output[avi__epohz - offset] = calc_out(minp, *data)
    return output, pfuy__wozid


def roll_fixed_apply(in_arr, index_arr, win, minp, center, parallel,
    kernel_func, raw=True):
    pass


@overload(roll_fixed_apply, no_unliteral=True)
def overload_roll_fixed_apply(in_arr, index_arr, win, minp, center,
    parallel, kernel_func, raw=True):
    assert is_overload_constant_bool(raw)
    return roll_fixed_apply_impl


def roll_fixed_apply_impl(in_arr, index_arr, win, minp, center, parallel,
    kernel_func, raw=True):
    _validate_roll_fixed_args(win, minp)
    in_arr = prep_values(in_arr)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    N = len(in_arr)
    offset = (win - 1) // 2 if center else 0
    index_arr = fix_index_arr(index_arr)
    if parallel:
        halo_size = np.int32(win // 2) if center else np.int32(win - 1)
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_apply(in_arr, index_arr, win, minp,
                center, rank, n_pes, kernel_func, raw)
        daj__iei = _border_icomm(in_arr, rank, n_pes, halo_size, True, center)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            xyk__vbijp) = daj__iei
        if raw == False:
            ulsbu__wxuo = _border_icomm(index_arr, rank, n_pes, halo_size, 
                True, center)
            (l_recv_buff_idx, r_recv_buff_idx, fvne__niu, uuww__pjpq,
                vfgek__uaes, cfoo__cwm) = ulsbu__wxuo
    output = roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
        kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, center)
        if raw == False:
            _border_send_wait(uuww__pjpq, fvne__niu, rank, n_pes, True, center)
        if center and rank != n_pes - 1:
            bodo.libs.distributed_api.wait(xyk__vbijp, True)
            if raw == False:
                bodo.libs.distributed_api.wait(cfoo__cwm, True)
            recv_right_compute(output, in_arr, index_arr, N, win, minp,
                offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            if raw == False:
                bodo.libs.distributed_api.wait(vfgek__uaes, True)
            recv_left_compute(output, in_arr, index_arr, win, minp, offset,
                l_recv_buff, l_recv_buff_idx, kernel_func, raw)
    return output


def recv_right_compute(output, in_arr, index_arr, N, win, minp, offset,
    r_recv_buff, r_recv_buff_idx, kernel_func, raw):
    pass


@overload(recv_right_compute, no_unliteral=True)
def overload_recv_right_compute(output, in_arr, index_arr, N, win, minp,
    offset, r_recv_buff, r_recv_buff_idx, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, N, win, minp, offset,
            r_recv_buff, r_recv_buff_idx, kernel_func, raw):
            pfuy__wozid = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
            fwt__jfey = 0
            for avi__epohz in range(max(N - offset, 0), N):
                data = pfuy__wozid[fwt__jfey:fwt__jfey + win]
                if win - np.isnan(data).sum() < minp:
                    output[avi__epohz] = np.nan
                else:
                    output[avi__epohz] = kernel_func(data)
                fwt__jfey += 1
        return impl

    def impl_series(output, in_arr, index_arr, N, win, minp, offset,
        r_recv_buff, r_recv_buff_idx, kernel_func, raw):
        pfuy__wozid = np.concatenate((in_arr[N - win + 1:], r_recv_buff))
        auchc__rvj = np.concatenate((index_arr[N - win + 1:], r_recv_buff_idx))
        fwt__jfey = 0
        for avi__epohz in range(max(N - offset, 0), N):
            data = pfuy__wozid[fwt__jfey:fwt__jfey + win]
            if win - np.isnan(data).sum() < minp:
                output[avi__epohz] = np.nan
            else:
                output[avi__epohz] = kernel_func(pd.Series(data, auchc__rvj
                    [fwt__jfey:fwt__jfey + win]))
            fwt__jfey += 1
    return impl_series


def recv_left_compute(output, in_arr, index_arr, win, minp, offset,
    l_recv_buff, l_recv_buff_idx, kernel_func, raw):
    pass


@overload(recv_left_compute, no_unliteral=True)
def overload_recv_left_compute(output, in_arr, index_arr, win, minp, offset,
    l_recv_buff, l_recv_buff_idx, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, win, minp, offset, l_recv_buff,
            l_recv_buff_idx, kernel_func, raw):
            pfuy__wozid = np.concatenate((l_recv_buff, in_arr[:win - 1]))
            for avi__epohz in range(0, win - offset - 1):
                data = pfuy__wozid[avi__epohz:avi__epohz + win]
                if win - np.isnan(data).sum() < minp:
                    output[avi__epohz] = np.nan
                else:
                    output[avi__epohz] = kernel_func(data)
        return impl

    def impl_series(output, in_arr, index_arr, win, minp, offset,
        l_recv_buff, l_recv_buff_idx, kernel_func, raw):
        pfuy__wozid = np.concatenate((l_recv_buff, in_arr[:win - 1]))
        auchc__rvj = np.concatenate((l_recv_buff_idx, index_arr[:win - 1]))
        for avi__epohz in range(0, win - offset - 1):
            data = pfuy__wozid[avi__epohz:avi__epohz + win]
            if win - np.isnan(data).sum() < minp:
                output[avi__epohz] = np.nan
            else:
                output[avi__epohz] = kernel_func(pd.Series(data, auchc__rvj
                    [avi__epohz:avi__epohz + win]))
    return impl_series


def roll_fixed_apply_seq(in_arr, index_arr, win, minp, center, kernel_func,
    raw=True):
    pass


@overload(roll_fixed_apply_seq, no_unliteral=True)
def overload_roll_fixed_apply_seq(in_arr, index_arr, win, minp, center,
    kernel_func, raw=True):
    assert is_overload_constant_bool(raw), "'raw' should be constant bool"

    def roll_fixed_apply_seq_impl(in_arr, index_arr, win, minp, center,
        kernel_func, raw=True):
        N = len(in_arr)
        output = np.empty(N, dtype=np.float64)
        offset = (win - 1) // 2 if center else 0
        for avi__epohz in range(0, N):
            start = max(avi__epohz - win + 1 + offset, 0)
            end = min(avi__epohz + 1 + offset, N)
            data = in_arr[start:end]
            if end - start - np.isnan(data).sum() < minp:
                output[avi__epohz] = np.nan
            else:
                output[avi__epohz] = apply_func(kernel_func, data,
                    index_arr, start, end, raw)
        return output
    return roll_fixed_apply_seq_impl


def apply_func(kernel_func, data, index_arr, start, end, raw):
    return kernel_func(data)


@overload(apply_func, no_unliteral=True)
def overload_apply_func(kernel_func, data, index_arr, start, end, raw):
    assert is_overload_constant_bool(raw), "'raw' should be constant bool"
    if is_overload_true(raw):
        return (lambda kernel_func, data, index_arr, start, end, raw:
            kernel_func(data))
    return lambda kernel_func, data, index_arr, start, end, raw: kernel_func(pd
        .Series(data, index_arr[start:end]))


def fix_index_arr(A):
    return A


@overload(fix_index_arr)
def overload_fix_index_arr(A):
    if is_overload_none(A):
        return lambda A: np.zeros(3)
    return lambda A: A


def get_offset_nanos(w):
    out = status = 0
    try:
        out = pd.tseries.frequencies.to_offset(w).nanos
    except:
        status = 1
    return out, status


def offset_to_nanos(w):
    return w


@overload(offset_to_nanos)
def overload_offset_to_nanos(w):
    if isinstance(w, types.Integer):
        return lambda w: w

    def impl(w):
        with numba.objmode(out='int64', status='int64'):
            out, status = get_offset_nanos(w)
        if status != 0:
            raise ValueError('Invalid offset value')
        return out
    return impl


@register_jitable
def roll_var_linear_generic(in_arr, on_arr_dt, win, minp, center, parallel,
    init_data, add_obs, remove_obs, calc_out):
    _validate_roll_var_args(minp, center)
    in_arr = prep_values(in_arr)
    win = offset_to_nanos(win)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    on_arr = cast_dt64_arr_to_int(on_arr_dt)
    N = len(in_arr)
    left_closed = False
    right_closed = True
    if parallel:
        if _is_small_for_parallel_variable(on_arr, win):
            return _handle_small_data_variable(in_arr, on_arr, win, minp,
                rank, n_pes, init_data, add_obs, remove_obs, calc_out)
        daj__iei = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, izqyk__htvbw, l_recv_req,
            tzl__hgsog) = daj__iei
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start,
        end, init_data, add_obs, remove_obs, calc_out)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(izqyk__htvbw, izqyk__htvbw, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(tzl__hgsog, True)
            num_zero_starts = 0
            for avi__epohz in range(0, N):
                if start[avi__epohz] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            data = init_data()
            for nsly__axpgg in range(recv_starts[0], len(l_recv_t_buff)):
                data = add_obs(l_recv_buff[nsly__axpgg], *data)
            if right_closed:
                data = add_obs(in_arr[0], *data)
            output[0] = calc_out(minp, *data)
            for avi__epohz in range(1, num_zero_starts):
                s = recv_starts[avi__epohz]
                jlosd__ggx = end[avi__epohz]
                for nsly__axpgg in range(recv_starts[avi__epohz - 1], s):
                    data = remove_obs(l_recv_buff[nsly__axpgg], *data)
                for nsly__axpgg in range(end[avi__epohz - 1], jlosd__ggx):
                    data = add_obs(in_arr[nsly__axpgg], *data)
                output[avi__epohz] = calc_out(minp, *data)
    return output


@register_jitable(cache=True)
def _get_var_recv_starts(on_arr, l_recv_t_buff, num_zero_starts, win):
    recv_starts = np.zeros(num_zero_starts, np.int64)
    halo_size = len(l_recv_t_buff)
    evad__knyy = cast_dt64_arr_to_int(on_arr)
    left_closed = False
    hiy__nwgen = evad__knyy[0] - win
    if left_closed:
        hiy__nwgen -= 1
    recv_starts[0] = halo_size
    for nsly__axpgg in range(0, halo_size):
        if l_recv_t_buff[nsly__axpgg] > hiy__nwgen:
            recv_starts[0] = nsly__axpgg
            break
    for avi__epohz in range(1, num_zero_starts):
        hiy__nwgen = evad__knyy[avi__epohz] - win
        if left_closed:
            hiy__nwgen -= 1
        recv_starts[avi__epohz] = halo_size
        for nsly__axpgg in range(recv_starts[avi__epohz - 1], halo_size):
            if l_recv_t_buff[nsly__axpgg] > hiy__nwgen:
                recv_starts[avi__epohz] = nsly__axpgg
                break
    return recv_starts


@register_jitable
def roll_var_linear_generic_seq(in_arr, on_arr, win, minp, start, end,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    output = np.empty(N, np.float64)
    data = init_data()
    for nsly__axpgg in range(start[0], end[0]):
        data = add_obs(in_arr[nsly__axpgg], *data)
    output[0] = calc_out(minp, *data)
    for avi__epohz in range(1, N):
        s = start[avi__epohz]
        jlosd__ggx = end[avi__epohz]
        for nsly__axpgg in range(start[avi__epohz - 1], s):
            data = remove_obs(in_arr[nsly__axpgg], *data)
        for nsly__axpgg in range(end[avi__epohz - 1], jlosd__ggx):
            data = add_obs(in_arr[nsly__axpgg], *data)
        output[avi__epohz] = calc_out(minp, *data)
    return output


def roll_variable_apply(in_arr, on_arr_dt, index_arr, win, minp, center,
    parallel, kernel_func, raw=True):
    pass


@overload(roll_variable_apply, no_unliteral=True)
def overload_roll_variable_apply(in_arr, on_arr_dt, index_arr, win, minp,
    center, parallel, kernel_func, raw=True):
    assert is_overload_constant_bool(raw)
    return roll_variable_apply_impl


def roll_variable_apply_impl(in_arr, on_arr_dt, index_arr, win, minp,
    center, parallel, kernel_func, raw=True):
    _validate_roll_var_args(minp, center)
    in_arr = prep_values(in_arr)
    win = offset_to_nanos(win)
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    on_arr = cast_dt64_arr_to_int(on_arr_dt)
    index_arr = fix_index_arr(index_arr)
    N = len(in_arr)
    left_closed = False
    right_closed = True
    if parallel:
        if _is_small_for_parallel_variable(on_arr, win):
            return _handle_small_data_variable_apply(in_arr, on_arr,
                index_arr, win, minp, rank, n_pes, kernel_func, raw)
        daj__iei = _border_icomm_var(in_arr, on_arr, rank, n_pes, win)
        (l_recv_buff, l_recv_t_buff, r_send_req, izqyk__htvbw, l_recv_req,
            tzl__hgsog) = daj__iei
        if raw == False:
            ulsbu__wxuo = _border_icomm_var(index_arr, on_arr, rank, n_pes, win
                )
            (l_recv_buff_idx, ttc__akovh, uuww__pjpq, woz__gqrix,
                vfgek__uaes, tsx__fcxtm) = ulsbu__wxuo
    start, end = _build_indexer(on_arr, N, win, left_closed, right_closed)
    output = roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
        start, end, kernel_func, raw)
    if parallel:
        _border_send_wait(r_send_req, r_send_req, rank, n_pes, True, False)
        _border_send_wait(izqyk__htvbw, izqyk__htvbw, rank, n_pes, True, False)
        if raw == False:
            _border_send_wait(uuww__pjpq, uuww__pjpq, rank, n_pes, True, False)
            _border_send_wait(woz__gqrix, woz__gqrix, rank, n_pes, True, False)
        if rank != 0:
            bodo.libs.distributed_api.wait(l_recv_req, True)
            bodo.libs.distributed_api.wait(tzl__hgsog, True)
            if raw == False:
                bodo.libs.distributed_api.wait(vfgek__uaes, True)
                bodo.libs.distributed_api.wait(tsx__fcxtm, True)
            num_zero_starts = 0
            for avi__epohz in range(0, N):
                if start[avi__epohz] != 0:
                    break
                num_zero_starts += 1
            if num_zero_starts == 0:
                return output
            recv_starts = _get_var_recv_starts(on_arr, l_recv_t_buff,
                num_zero_starts, win)
            recv_left_var_compute(output, in_arr, index_arr,
                num_zero_starts, recv_starts, l_recv_buff, l_recv_buff_idx,
                minp, kernel_func, raw)
    return output


def recv_left_var_compute(output, in_arr, index_arr, num_zero_starts,
    recv_starts, l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
    pass


@overload(recv_left_var_compute)
def overload_recv_left_var_compute(output, in_arr, index_arr,
    num_zero_starts, recv_starts, l_recv_buff, l_recv_buff_idx, minp,
    kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):

        def impl(output, in_arr, index_arr, num_zero_starts, recv_starts,
            l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
            for avi__epohz in range(0, num_zero_starts):
                xxsqn__njvwj = recv_starts[avi__epohz]
                cpvhc__ksca = np.concatenate((l_recv_buff[xxsqn__njvwj:],
                    in_arr[:avi__epohz + 1]))
                if len(cpvhc__ksca) - np.isnan(cpvhc__ksca).sum() >= minp:
                    output[avi__epohz] = kernel_func(cpvhc__ksca)
                else:
                    output[avi__epohz] = np.nan
        return impl

    def impl_series(output, in_arr, index_arr, num_zero_starts, recv_starts,
        l_recv_buff, l_recv_buff_idx, minp, kernel_func, raw):
        for avi__epohz in range(0, num_zero_starts):
            xxsqn__njvwj = recv_starts[avi__epohz]
            cpvhc__ksca = np.concatenate((l_recv_buff[xxsqn__njvwj:],
                in_arr[:avi__epohz + 1]))
            jim__qbwy = np.concatenate((l_recv_buff_idx[xxsqn__njvwj:],
                index_arr[:avi__epohz + 1]))
            if len(cpvhc__ksca) - np.isnan(cpvhc__ksca).sum() >= minp:
                output[avi__epohz] = kernel_func(pd.Series(cpvhc__ksca,
                    jim__qbwy))
            else:
                output[avi__epohz] = np.nan
    return impl_series


def roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp, start,
    end, kernel_func, raw):
    pass


@overload(roll_variable_apply_seq)
def overload_roll_variable_apply_seq(in_arr, on_arr, index_arr, win, minp,
    start, end, kernel_func, raw):
    assert is_overload_constant_bool(raw)
    if is_overload_true(raw):
        return roll_variable_apply_seq_impl
    return roll_variable_apply_seq_impl_series


def roll_variable_apply_seq_impl(in_arr, on_arr, index_arr, win, minp,
    start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for avi__epohz in range(0, N):
        s = start[avi__epohz]
        jlosd__ggx = end[avi__epohz]
        data = in_arr[s:jlosd__ggx]
        if jlosd__ggx - s - np.isnan(data).sum() >= minp:
            output[avi__epohz] = kernel_func(data)
        else:
            output[avi__epohz] = np.nan
    return output


def roll_variable_apply_seq_impl_series(in_arr, on_arr, index_arr, win,
    minp, start, end, kernel_func, raw):
    N = len(in_arr)
    output = np.empty(N, dtype=np.float64)
    for avi__epohz in range(0, N):
        s = start[avi__epohz]
        jlosd__ggx = end[avi__epohz]
        data = in_arr[s:jlosd__ggx]
        if jlosd__ggx - s - np.isnan(data).sum() >= minp:
            output[avi__epohz] = kernel_func(pd.Series(data, index_arr[s:
                jlosd__ggx]))
        else:
            output[avi__epohz] = np.nan
    return output


@register_jitable(cache=True)
def _build_indexer(on_arr, N, win, left_closed, right_closed):
    evad__knyy = cast_dt64_arr_to_int(on_arr)
    start = np.empty(N, np.int64)
    end = np.empty(N, np.int64)
    start[0] = 0
    if right_closed:
        end[0] = 1
    else:
        end[0] = 0
    for avi__epohz in range(1, N):
        qmkks__kur = evad__knyy[avi__epohz]
        hiy__nwgen = evad__knyy[avi__epohz] - win
        if left_closed:
            hiy__nwgen -= 1
        start[avi__epohz] = avi__epohz
        for nsly__axpgg in range(start[avi__epohz - 1], avi__epohz):
            if evad__knyy[nsly__axpgg] > hiy__nwgen:
                start[avi__epohz] = nsly__axpgg
                break
        if evad__knyy[end[avi__epohz - 1]] <= qmkks__kur:
            end[avi__epohz] = avi__epohz + 1
        else:
            end[avi__epohz] = end[avi__epohz - 1]
        if not right_closed:
            end[avi__epohz] -= 1
    return start, end


@register_jitable
def init_data_sum():
    return 0, 0.0


@register_jitable
def add_sum(val, nobs, sum_x):
    if not np.isnan(val):
        nobs += 1
        sum_x += val
    return nobs, sum_x


@register_jitable
def remove_sum(val, nobs, sum_x):
    if not np.isnan(val):
        nobs -= 1
        sum_x -= val
    return nobs, sum_x


@register_jitable
def calc_sum(minp, nobs, sum_x):
    return sum_x if nobs >= minp else np.nan


@register_jitable
def init_data_mean():
    return 0, 0.0, 0


@register_jitable
def add_mean(val, nobs, sum_x, neg_ct):
    if not np.isnan(val):
        nobs += 1
        sum_x += val
        if val < 0:
            neg_ct += 1
    return nobs, sum_x, neg_ct


@register_jitable
def remove_mean(val, nobs, sum_x, neg_ct):
    if not np.isnan(val):
        nobs -= 1
        sum_x -= val
        if val < 0:
            neg_ct -= 1
    return nobs, sum_x, neg_ct


@register_jitable
def calc_mean(minp, nobs, sum_x, neg_ct):
    if nobs >= minp:
        zlsb__sai = sum_x / nobs
        if neg_ct == 0 and zlsb__sai < 0.0:
            zlsb__sai = 0
        elif neg_ct == nobs and zlsb__sai > 0.0:
            zlsb__sai = 0
    else:
        zlsb__sai = np.nan
    return zlsb__sai


@register_jitable
def init_data_var():
    return 0, 0.0, 0.0


@register_jitable
def add_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs += 1
        gbh__ort = val - mean_x
        mean_x += gbh__ort / nobs
        ssqdm_x += (nobs - 1) * gbh__ort ** 2 / nobs
    return nobs, mean_x, ssqdm_x


@register_jitable
def remove_var(val, nobs, mean_x, ssqdm_x):
    if not np.isnan(val):
        nobs -= 1
        if nobs != 0:
            gbh__ort = val - mean_x
            mean_x -= gbh__ort / nobs
            ssqdm_x -= (nobs + 1) * gbh__ort ** 2 / nobs
        else:
            mean_x = 0.0
            ssqdm_x = 0.0
    return nobs, mean_x, ssqdm_x


@register_jitable
def calc_var(minp, nobs, mean_x, ssqdm_x):
    wot__rscb = 1.0
    zlsb__sai = np.nan
    if nobs >= minp and nobs > wot__rscb:
        if nobs == 1:
            zlsb__sai = 0.0
        else:
            zlsb__sai = ssqdm_x / (nobs - wot__rscb)
            if zlsb__sai < 0.0:
                zlsb__sai = 0.0
    return zlsb__sai


@register_jitable
def calc_std(minp, nobs, mean_x, ssqdm_x):
    jnjlz__qrlv = calc_var(minp, nobs, mean_x, ssqdm_x)
    return np.sqrt(jnjlz__qrlv)


@register_jitable
def init_data_count():
    return 0.0,


@register_jitable
def add_count(val, count_x):
    if not np.isnan(val):
        count_x += 1.0
    return count_x,


@register_jitable
def remove_count(val, count_x):
    if not np.isnan(val):
        count_x -= 1.0
    return count_x,


@register_jitable
def calc_count(minp, count_x):
    return count_x


@register_jitable
def calc_count_var(minp, count_x):
    return count_x if count_x >= minp else np.nan


linear_kernels = {'sum': (init_data_sum, add_sum, remove_sum, calc_sum),
    'mean': (init_data_mean, add_mean, remove_mean, calc_mean), 'var': (
    init_data_var, add_var, remove_var, calc_var), 'std': (init_data_var,
    add_var, remove_var, calc_std), 'count': (init_data_count, add_count,
    remove_count, calc_count)}


def shift(in_arr, shift, parallel, default_fill_value=None):
    return


@overload(shift, jit_options={'cache': True})
def shift_overload(in_arr, shift, parallel, default_fill_value=None):
    if not isinstance(parallel, types.Literal):
        return shift_impl


def shift_impl(in_arr, shift, parallel, default_fill_value=None):
    N = len(in_arr)
    in_arr = decode_if_dict_array(in_arr)
    output = alloc_shift(N, in_arr, (-1,), fill_value=default_fill_value)
    send_right = shift > 0
    send_left = shift <= 0
    is_parallel_str = False
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        halo_size = np.int32(abs(shift))
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_shift(in_arr, shift, rank, n_pes,
                default_fill_value)
        daj__iei = _border_icomm(in_arr, rank, n_pes, halo_size, send_right,
            send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            xyk__vbijp) = daj__iei
        if send_right and is_str_binary_array(in_arr):
            is_parallel_str = True
            shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
                l_recv_req, l_recv_buff, output)
    shift_seq(in_arr, shift, output, is_parallel_str, default_fill_value)
    if parallel:
        if send_right:
            if not is_str_binary_array(in_arr):
                shift_left_recv(r_send_req, l_send_req, rank, n_pes,
                    halo_size, l_recv_req, l_recv_buff, output)
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(xyk__vbijp, True)
                for avi__epohz in range(0, halo_size):
                    if bodo.libs.array_kernels.isna(r_recv_buff, avi__epohz):
                        bodo.libs.array_kernels.setna(output, N - halo_size +
                            avi__epohz)
                        continue
                    output[N - halo_size + avi__epohz] = r_recv_buff[avi__epohz
                        ]
    return output


@register_jitable(cache=True)
def shift_seq(in_arr, shift, output, is_parallel_str=False,
    default_fill_value=None):
    N = len(in_arr)
    fhnu__ves = 1 if shift > 0 else -1
    shift = fhnu__ves * min(abs(shift), N)
    if shift > 0 and (not is_parallel_str or bodo.get_rank() == 0):
        if default_fill_value is None:
            bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
        else:
            for avi__epohz in range(shift):
                output[avi__epohz
                    ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                    default_fill_value)
    start = max(shift, 0)
    end = min(N, N + shift)
    for avi__epohz in range(start, end):
        if bodo.libs.array_kernels.isna(in_arr, avi__epohz - shift):
            bodo.libs.array_kernels.setna(output, avi__epohz)
            continue
        output[avi__epohz] = in_arr[avi__epohz - shift]
    if shift < 0:
        if default_fill_value is None:
            bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
        else:
            for avi__epohz in range(end, N):
                output[avi__epohz
                    ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                    default_fill_value)
    return output


@register_jitable
def shift_left_recv(r_send_req, l_send_req, rank, n_pes, halo_size,
    l_recv_req, l_recv_buff, output):
    _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
    if rank != 0:
        bodo.libs.distributed_api.wait(l_recv_req, True)
        for avi__epohz in range(0, halo_size):
            if bodo.libs.array_kernels.isna(l_recv_buff, avi__epohz):
                bodo.libs.array_kernels.setna(output, avi__epohz)
                continue
            output[avi__epohz] = l_recv_buff[avi__epohz]


def is_str_binary_array(arr):
    return False


@overload(is_str_binary_array)
def overload_is_str_binary_array(arr):
    if arr in [bodo.string_array_type, bodo.binary_array_type]:
        return lambda arr: True
    return lambda arr: False


def is_supported_shift_array_type(arr_type):
    return isinstance(arr_type, types.Array) and (isinstance(arr_type.dtype,
        types.Number) or arr_type.dtype in [bodo.datetime64ns, bodo.
        timedelta64ns]) or isinstance(arr_type, (bodo.IntegerArrayType,
        bodo.FloatingArrayType, bodo.DecimalArrayType, bodo.DatetimeArrayType)
        ) or arr_type in (bodo.boolean_array, bodo.datetime_date_array_type,
        bodo.string_array_type, bodo.binary_array_type, bodo.dict_str_arr_type)


def pct_change():
    return


@overload(pct_change, jit_options={'cache': True})
def pct_change_overload(in_arr, shift, parallel):
    if not isinstance(parallel, types.Literal):
        return pct_change_impl


def pct_change_impl(in_arr, shift, parallel):
    N = len(in_arr)
    send_right = shift > 0
    send_left = shift <= 0
    if parallel:
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        halo_size = np.int32(abs(shift))
        if _is_small_for_parallel(N, halo_size):
            return _handle_small_data_pct_change(in_arr, shift, rank, n_pes)
        daj__iei = _border_icomm(in_arr, rank, n_pes, halo_size, send_right,
            send_left)
        (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
            xyk__vbijp) = daj__iei
    output = pct_change_seq(in_arr, shift)
    if parallel:
        if send_right:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, True, False)
            if rank != 0:
                bodo.libs.distributed_api.wait(l_recv_req, True)
                for avi__epohz in range(0, halo_size):
                    dkps__nye = l_recv_buff[avi__epohz]
                    output[avi__epohz] = (in_arr[avi__epohz] - dkps__nye
                        ) / dkps__nye
        else:
            _border_send_wait(r_send_req, l_send_req, rank, n_pes, False, True)
            if rank != n_pes - 1:
                bodo.libs.distributed_api.wait(xyk__vbijp, True)
                for avi__epohz in range(0, halo_size):
                    dkps__nye = r_recv_buff[avi__epohz]
                    output[N - halo_size + avi__epohz] = (in_arr[N -
                        halo_size + avi__epohz] - dkps__nye) / dkps__nye
    return output


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_first_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[0]
    assert isinstance(arr.dtype, types.Float)
    fxkn__fvd = np.nan
    if arr.dtype == types.float32:
        fxkn__fvd = np.float32('nan')

    def impl(arr):
        for avi__epohz in range(len(arr)):
            if not bodo.libs.array_kernels.isna(arr, avi__epohz):
                return arr[avi__epohz]
        return fxkn__fvd
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_last_non_na(arr):
    if isinstance(arr.dtype, (types.Integer, types.Boolean)):
        zero = arr.dtype(0)
        return lambda arr: zero if len(arr) == 0 else arr[-1]
    assert isinstance(arr.dtype, types.Float)
    fxkn__fvd = np.nan
    if arr.dtype == types.float32:
        fxkn__fvd = np.float32('nan')

    def impl(arr):
        bpbzz__reua = len(arr)
        for avi__epohz in range(len(arr)):
            fwt__jfey = bpbzz__reua - avi__epohz - 1
            if not bodo.libs.array_kernels.isna(arr, fwt__jfey):
                return arr[fwt__jfey]
        return fxkn__fvd
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_one_from_arr_dtype(arr):
    one = arr.dtype(1)
    return lambda arr: one


@register_jitable(cache=True)
def pct_change_seq(in_arr, shift):
    N = len(in_arr)
    output = alloc_pct_change(N, in_arr)
    fhnu__ves = 1 if shift > 0 else -1
    shift = fhnu__ves * min(abs(shift), N)
    if shift > 0:
        bodo.libs.array_kernels.setna_slice(output, slice(None, shift))
    else:
        bodo.libs.array_kernels.setna_slice(output, slice(shift, None))
    if shift > 0:
        aerfn__moknz = get_first_non_na(in_arr[:shift])
        kjqc__shyk = get_last_non_na(in_arr[:shift])
    else:
        aerfn__moknz = get_last_non_na(in_arr[:-shift])
        kjqc__shyk = get_first_non_na(in_arr[:-shift])
    one = get_one_from_arr_dtype(output)
    start = max(shift, 0)
    end = min(N, N + shift)
    for avi__epohz in range(start, end):
        dkps__nye = in_arr[avi__epohz - shift]
        if np.isnan(dkps__nye):
            dkps__nye = aerfn__moknz
        else:
            aerfn__moknz = dkps__nye
        val = in_arr[avi__epohz]
        if np.isnan(val):
            val = kjqc__shyk
        else:
            kjqc__shyk = val
        output[avi__epohz] = val / dkps__nye - one
    return output


@register_jitable(cache=True)
def _border_icomm(in_arr, rank, n_pes, halo_size, send_right=True,
    send_left=False):
    eyl__ncjo = np.int32(comm_border_tag)
    l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    r_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr, (-1,))
    if send_right and rank != n_pes - 1:
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            halo_size, np.int32(rank + 1), eyl__ncjo, True)
    if send_right and rank != 0:
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, halo_size,
            np.int32(rank - 1), eyl__ncjo, True)
    if send_left and rank != 0:
        l_send_req = bodo.libs.distributed_api.isend(in_arr[:halo_size],
            halo_size, np.int32(rank - 1), eyl__ncjo, True)
    if send_left and rank != n_pes - 1:
        xyk__vbijp = bodo.libs.distributed_api.irecv(r_recv_buff, halo_size,
            np.int32(rank + 1), eyl__ncjo, True)
    return (l_recv_buff, r_recv_buff, l_send_req, r_send_req, l_recv_req,
        xyk__vbijp)


@register_jitable(cache=True)
def _border_icomm_var(in_arr, on_arr, rank, n_pes, win_size):
    eyl__ncjo = np.int32(comm_border_tag)
    N = len(on_arr)
    halo_size = N
    end = on_arr[-1]
    for nsly__axpgg in range(-2, -N, -1):
        euy__maeoy = on_arr[nsly__axpgg]
        if end - euy__maeoy >= win_size:
            halo_size = -nsly__axpgg
            break
    if rank != n_pes - 1:
        bodo.libs.distributed_api.send(halo_size, np.int32(rank + 1), eyl__ncjo
            )
        r_send_req = bodo.libs.distributed_api.isend(in_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), eyl__ncjo, True)
        izqyk__htvbw = bodo.libs.distributed_api.isend(on_arr[-halo_size:],
            np.int32(halo_size), np.int32(rank + 1), eyl__ncjo, True)
    if rank != 0:
        halo_size = bodo.libs.distributed_api.recv(np.int64, np.int32(rank -
            1), eyl__ncjo)
        l_recv_buff = bodo.utils.utils.alloc_type(halo_size, in_arr)
        l_recv_req = bodo.libs.distributed_api.irecv(l_recv_buff, np.int32(
            halo_size), np.int32(rank - 1), eyl__ncjo, True)
        l_recv_t_buff = np.empty(halo_size, np.int64)
        tzl__hgsog = bodo.libs.distributed_api.irecv(l_recv_t_buff, np.
            int32(halo_size), np.int32(rank - 1), eyl__ncjo, True)
    return (l_recv_buff, l_recv_t_buff, r_send_req, izqyk__htvbw,
        l_recv_req, tzl__hgsog)


@register_jitable
def _border_send_wait(r_send_req, l_send_req, rank, n_pes, right, left):
    if right and rank != n_pes - 1:
        bodo.libs.distributed_api.wait(r_send_req, True)
    if left and rank != 0:
        bodo.libs.distributed_api.wait(l_send_req, True)


@register_jitable
def _is_small_for_parallel(N, halo_size):
    ith__qgsbc = bodo.libs.distributed_api.dist_reduce(int(N <= 2 *
        halo_size + 1), np.int32(Reduce_Type.Sum.value))
    return ith__qgsbc != 0


@register_jitable
def _handle_small_data(in_arr, win, minp, center, rank, n_pes, init_data,
    add_obs, remove_obs, calc_out):
    N = len(in_arr)
    ybn__scm = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.int32(
        Reduce_Type.Sum.value))
    bcdlx__exv = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        djv__bevhy, wci__kugk = roll_fixed_linear_generic_seq(bcdlx__exv,
            win, minp, center, init_data, add_obs, remove_obs, calc_out)
    else:
        djv__bevhy = np.empty(ybn__scm, np.float64)
    bodo.libs.distributed_api.bcast(djv__bevhy)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return djv__bevhy[start:end]


@register_jitable
def _handle_small_data_apply(in_arr, index_arr, win, minp, center, rank,
    n_pes, kernel_func, raw=True):
    N = len(in_arr)
    ybn__scm = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.int32(
        Reduce_Type.Sum.value))
    bcdlx__exv = bodo.libs.distributed_api.gatherv(in_arr)
    dgi__thprh = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        djv__bevhy = roll_fixed_apply_seq(bcdlx__exv, dgi__thprh, win, minp,
            center, kernel_func, raw)
    else:
        djv__bevhy = np.empty(ybn__scm, np.float64)
    bodo.libs.distributed_api.bcast(djv__bevhy)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return djv__bevhy[start:end]


def bcast_n_chars_if_str_binary_arr(arr):
    pass


@overload(bcast_n_chars_if_str_binary_arr)
def overload_bcast_n_chars_if_str_binary_arr(arr):
    if arr in [bodo.binary_array_type, bodo.string_array_type]:

        def impl(arr):
            return bodo.libs.distributed_api.bcast_scalar(np.int64(bodo.
                libs.str_arr_ext.num_total_chars(arr)))
        return impl
    return lambda arr: -1


@register_jitable
def _handle_small_data_shift(in_arr, shift, rank, n_pes, default_fill_value):
    N = len(in_arr)
    ybn__scm = bodo.libs.distributed_api.dist_reduce(len(in_arr), np.int32(
        Reduce_Type.Sum.value))
    bcdlx__exv = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        djv__bevhy = alloc_shift(len(bcdlx__exv), bcdlx__exv, (-1,),
            fill_value=default_fill_value)
        shift_seq(bcdlx__exv, shift, djv__bevhy, default_fill_value=
            default_fill_value)
        urjmv__xglkj = bcast_n_chars_if_str_binary_arr(djv__bevhy)
    else:
        urjmv__xglkj = bcast_n_chars_if_str_binary_arr(in_arr)
        djv__bevhy = alloc_shift(ybn__scm, in_arr, (urjmv__xglkj,),
            fill_value=default_fill_value)
    bodo.libs.distributed_api.bcast(djv__bevhy)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return djv__bevhy[start:end]


@register_jitable
def _handle_small_data_pct_change(in_arr, shift, rank, n_pes):
    N = len(in_arr)
    ybn__scm = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    bcdlx__exv = bodo.libs.distributed_api.gatherv(in_arr)
    if rank == 0:
        djv__bevhy = pct_change_seq(bcdlx__exv, shift)
    else:
        djv__bevhy = alloc_pct_change(ybn__scm, in_arr)
    bodo.libs.distributed_api.bcast(djv__bevhy)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return djv__bevhy[start:end]


def cast_dt64_arr_to_int(arr):
    return arr


@infer_global(cast_dt64_arr_to_int)
class DtArrToIntType(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        assert args[0] == types.Array(types.NPDatetime('ns'), 1, 'C') or args[0
            ] == types.Array(types.int64, 1, 'C')
        return signature(types.Array(types.int64, 1, 'C'), *args)


@lower_builtin(cast_dt64_arr_to_int, types.Array(types.NPDatetime('ns'), 1,
    'C'))
@lower_builtin(cast_dt64_arr_to_int, types.Array(types.int64, 1, 'C'))
def lower_cast_dt64_arr_to_int(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@register_jitable
def _is_small_for_parallel_variable(on_arr, win_size):
    if len(on_arr) < 2:
        zsrhd__pvzz = 1
    else:
        start = on_arr[0]
        end = on_arr[-1]
        cbd__qubo = end - start
        zsrhd__pvzz = int(cbd__qubo <= win_size)
    ith__qgsbc = bodo.libs.distributed_api.dist_reduce(zsrhd__pvzz, np.
        int32(Reduce_Type.Sum.value))
    return ith__qgsbc != 0


@register_jitable
def _handle_small_data_variable(in_arr, on_arr, win, minp, rank, n_pes,
    init_data, add_obs, remove_obs, calc_out):
    N = len(in_arr)
    ybn__scm = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    bcdlx__exv = bodo.libs.distributed_api.gatherv(in_arr)
    paop__otr = bodo.libs.distributed_api.gatherv(on_arr)
    if rank == 0:
        start, end = _build_indexer(paop__otr, ybn__scm, win, False, True)
        djv__bevhy = roll_var_linear_generic_seq(bcdlx__exv, paop__otr, win,
            minp, start, end, init_data, add_obs, remove_obs, calc_out)
    else:
        djv__bevhy = np.empty(ybn__scm, np.float64)
    bodo.libs.distributed_api.bcast(djv__bevhy)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return djv__bevhy[start:end]


@register_jitable
def _handle_small_data_variable_apply(in_arr, on_arr, index_arr, win, minp,
    rank, n_pes, kernel_func, raw):
    N = len(in_arr)
    ybn__scm = bodo.libs.distributed_api.dist_reduce(N, np.int32(
        Reduce_Type.Sum.value))
    bcdlx__exv = bodo.libs.distributed_api.gatherv(in_arr)
    paop__otr = bodo.libs.distributed_api.gatherv(on_arr)
    dgi__thprh = bodo.libs.distributed_api.gatherv(index_arr)
    if rank == 0:
        start, end = _build_indexer(paop__otr, ybn__scm, win, False, True)
        djv__bevhy = roll_variable_apply_seq(bcdlx__exv, paop__otr,
            dgi__thprh, win, minp, start, end, kernel_func, raw)
    else:
        djv__bevhy = np.empty(ybn__scm, np.float64)
    bodo.libs.distributed_api.bcast(djv__bevhy)
    start = bodo.libs.distributed_api.dist_exscan(N, np.int32(Reduce_Type.
        Sum.value))
    end = start + N
    return djv__bevhy[start:end]


@register_jitable(cache=True)
def _dropna(arr):
    myqld__obw = len(arr)
    uul__vgdm = myqld__obw - np.isnan(arr).sum()
    A = np.empty(uul__vgdm, arr.dtype)
    mbrpj__urtce = 0
    for avi__epohz in range(myqld__obw):
        val = arr[avi__epohz]
        if not np.isnan(val):
            A[mbrpj__urtce] = val
            mbrpj__urtce += 1
    return A


def alloc_shift(n, A, s=None, fill_value=None):
    return np.empty(n, A.dtype)


@overload(alloc_shift, no_unliteral=True)
def alloc_shift_overload(n, A, s=None, fill_value=None):
    if not isinstance(A, types.Array):
        return (lambda n, A, s=None, fill_value=None: bodo.utils.utils.
            alloc_type(n, A, s))
    if isinstance(A.dtype, types.Integer) and not isinstance(fill_value,
        types.Integer):
        return lambda n, A, s=None, fill_value=None: np.empty(n, np.float64)
    return lambda n, A, s=None, fill_value=None: np.empty(n, A.dtype)


def alloc_pct_change(n, A):
    return np.empty(n, A.dtype)


@overload(alloc_pct_change, no_unliteral=True)
def alloc_pct_change_overload(n, A):
    if isinstance(A.dtype, types.Integer):
        return lambda n, A: np.empty(n, np.float64)
    return lambda n, A: bodo.utils.utils.alloc_type(n, A, (-1,))


def prep_values(A):
    return A.astype('float64')


@overload(prep_values, no_unliteral=True)
def prep_values_overload(A):
    if A == types.Array(types.float64, 1, 'C'):
        return lambda A: A
    return lambda A: A.astype(np.float64)


@register_jitable
def _validate_roll_fixed_args(win, minp):
    if win < 0:
        raise ValueError('window must be non-negative')
    if minp < 0:
        raise ValueError('min_periods must be >= 0')
    if minp > win:
        raise ValueError('min_periods must be <= window')


@register_jitable
def _validate_roll_var_args(minp, center):
    if minp < 0:
        raise ValueError('min_periods must be >= 0')
    if center:
        raise NotImplementedError(
            'rolling: center is not implemented for datetimelike and offset based windows'
            )
