import atexit
import datetime
import sys
import time
import warnings
from collections import defaultdict
from decimal import Decimal
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from mpi4py import MPI
from numba.core import cgutils, ir_utils, types
from numba.core.typing import signature
from numba.core.typing.builtins import IndexValueType
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, overload, register_jitable
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.libs import hdist
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType, set_bit_to_arr
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.pd_datetime_arr_ext import DatetimeArrayType
from bodo.libs.str_arr_ext import convert_len_arr_to_offset, get_bit_bitmap, get_data_ptr, get_null_bitmap_ptr, get_offset_ptr, num_total_chars, pre_alloc_string_array, set_bit_to, string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, BodoWarning, ColNamesMetaType, decode_if_dict_array, is_overload_false, is_overload_none, is_str_arr_type
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, empty_like_type, is_array_typ, numba_to_c_type
ll.add_symbol('dist_get_time', hdist.dist_get_time)
ll.add_symbol('get_time', hdist.get_time)
ll.add_symbol('dist_reduce', hdist.dist_reduce)
ll.add_symbol('dist_arr_reduce', hdist.dist_arr_reduce)
ll.add_symbol('dist_exscan', hdist.dist_exscan)
ll.add_symbol('dist_irecv', hdist.dist_irecv)
ll.add_symbol('dist_isend', hdist.dist_isend)
ll.add_symbol('dist_wait', hdist.dist_wait)
ll.add_symbol('dist_get_item_pointer', hdist.dist_get_item_pointer)
ll.add_symbol('get_dummy_ptr', hdist.get_dummy_ptr)
ll.add_symbol('allgather', hdist.allgather)
ll.add_symbol('oneD_reshape_shuffle', hdist.oneD_reshape_shuffle)
ll.add_symbol('permutation_int', hdist.permutation_int)
ll.add_symbol('permutation_array_index', hdist.permutation_array_index)
ll.add_symbol('c_get_rank', hdist.dist_get_rank)
ll.add_symbol('c_get_size', hdist.dist_get_size)
ll.add_symbol('c_barrier', hdist.barrier)
ll.add_symbol('c_alltoall', hdist.c_alltoall)
ll.add_symbol('c_gather_scalar', hdist.c_gather_scalar)
ll.add_symbol('c_gatherv', hdist.c_gatherv)
ll.add_symbol('c_scatterv', hdist.c_scatterv)
ll.add_symbol('c_allgatherv', hdist.c_allgatherv)
ll.add_symbol('c_bcast', hdist.c_bcast)
ll.add_symbol('c_recv', hdist.dist_recv)
ll.add_symbol('c_send', hdist.dist_send)
mpi_req_numba_type = getattr(types, 'int' + str(8 * hdist.mpi_req_num_bytes))
MPI_ROOT = 0
ANY_SOURCE = np.int32(hdist.ANY_SOURCE)


class Reduce_Type(Enum):
    Sum = 0
    Prod = 1
    Min = 2
    Max = 3
    Argmin = 4
    Argmax = 5
    Or = 6
    Concat = 7
    No_Op = 8


_get_rank = types.ExternalFunction('c_get_rank', types.int32())
_get_size = types.ExternalFunction('c_get_size', types.int32())
_barrier = types.ExternalFunction('c_barrier', types.int32())


@numba.njit
def get_rank():
    return _get_rank()


@numba.njit
def get_size():
    return _get_size()


@numba.njit
def barrier():
    _barrier()


_get_time = types.ExternalFunction('get_time', types.float64())
dist_time = types.ExternalFunction('dist_get_time', types.float64())


@overload(time.time, no_unliteral=True)
def overload_time_time():
    return lambda : _get_time()


@numba.generated_jit(nopython=True)
def get_type_enum(arr):
    arr = arr.instance_type if isinstance(arr, types.TypeRef) else arr
    dtype = arr.dtype
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        dtype = bodo.hiframes.pd_categorical_ext.get_categories_int_type(dtype)
    typ_val = numba_to_c_type(dtype)
    return lambda arr: np.int32(typ_val)


INT_MAX = np.iinfo(np.int32).max
_send = types.ExternalFunction('c_send', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def send(val, rank, tag):
    send_arr = np.full(1, val)
    mvqxp__oizp = get_type_enum(send_arr)
    _send(send_arr.ctypes, 1, mvqxp__oizp, rank, tag)


_recv = types.ExternalFunction('c_recv', types.void(types.voidptr, types.
    int32, types.int32, types.int32, types.int32))


@numba.njit
def recv(dtype, rank, tag):
    recv_arr = np.empty(1, dtype)
    mvqxp__oizp = get_type_enum(recv_arr)
    _recv(recv_arr.ctypes, 1, mvqxp__oizp, rank, tag)
    return recv_arr[0]


_isend = types.ExternalFunction('dist_isend', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def isend(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            mvqxp__oizp = get_type_enum(arr)
            return _isend(arr.ctypes, size, mvqxp__oizp, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or arr in (boolean_array, datetime_date_array_type):
        mvqxp__oizp = np.int32(numba_to_c_type(arr.dtype))
        mya__ddsoq = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            bxl__qrom = size + 7 >> 3
            kgnko__nfsn = _isend(arr._data.ctypes, size, mvqxp__oizp, pe,
                tag, cond)
            hxzx__xqxi = _isend(arr._null_bitmap.ctypes, bxl__qrom,
                mya__ddsoq, pe, tag, cond)
            return kgnko__nfsn, hxzx__xqxi
        return impl_nullable
    if isinstance(arr, DatetimeArrayType):

        def impl_tz_arr(arr, size, pe, tag, cond=True):
            gjlb__kgen = arr._data
            mvqxp__oizp = get_type_enum(gjlb__kgen)
            return _isend(gjlb__kgen.ctypes, size, mvqxp__oizp, pe, tag, cond)
        return impl_tz_arr
    if is_str_arr_type(arr) or arr == binary_array_type:
        tmbs__twhd = np.int32(numba_to_c_type(offset_type))
        mya__ddsoq = np.int32(numba_to_c_type(types.uint8))

        def impl_str_arr(arr, size, pe, tag, cond=True):
            arr = decode_if_dict_array(arr)
            mhr__bqgar = np.int64(bodo.libs.str_arr_ext.num_total_chars(arr))
            send(mhr__bqgar, pe, tag - 1)
            bxl__qrom = size + 7 >> 3
            _send(bodo.libs.str_arr_ext.get_offset_ptr(arr), size + 1,
                tmbs__twhd, pe, tag)
            _send(bodo.libs.str_arr_ext.get_data_ptr(arr), mhr__bqgar,
                mya__ddsoq, pe, tag)
            _send(bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr), bxl__qrom,
                mya__ddsoq, pe, tag)
            return None
        return impl_str_arr
    typ_enum = numba_to_c_type(types.uint8)

    def impl_voidptr(arr, size, pe, tag, cond=True):
        return _isend(arr, size, typ_enum, pe, tag, cond)
    return impl_voidptr


_irecv = types.ExternalFunction('dist_irecv', mpi_req_numba_type(types.
    voidptr, types.int32, types.int32, types.int32, types.int32, types.bool_))


@numba.generated_jit(nopython=True)
def irecv(arr, size, pe, tag, cond=True):
    if isinstance(arr, types.Array):

        def impl(arr, size, pe, tag, cond=True):
            mvqxp__oizp = get_type_enum(arr)
            return _irecv(arr.ctypes, size, mvqxp__oizp, pe, tag, cond)
        return impl
    if isinstance(arr, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or arr in (boolean_array, datetime_date_array_type):
        mvqxp__oizp = np.int32(numba_to_c_type(arr.dtype))
        mya__ddsoq = np.int32(numba_to_c_type(types.uint8))

        def impl_nullable(arr, size, pe, tag, cond=True):
            bxl__qrom = size + 7 >> 3
            kgnko__nfsn = _irecv(arr._data.ctypes, size, mvqxp__oizp, pe,
                tag, cond)
            hxzx__xqxi = _irecv(arr._null_bitmap.ctypes, bxl__qrom,
                mya__ddsoq, pe, tag, cond)
            return kgnko__nfsn, hxzx__xqxi
        return impl_nullable
    if isinstance(arr, DatetimeArrayType):

        def impl_tz_arr(arr, size, pe, tag, cond=True):
            gjlb__kgen = arr._data
            mvqxp__oizp = get_type_enum(gjlb__kgen)
            return _irecv(gjlb__kgen.ctypes, size, mvqxp__oizp, pe, tag, cond)
        return impl_tz_arr
    if arr in [binary_array_type, string_array_type]:
        tmbs__twhd = np.int32(numba_to_c_type(offset_type))
        mya__ddsoq = np.int32(numba_to_c_type(types.uint8))
        if arr == binary_array_type:
            gsq__znxfz = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            gsq__znxfz = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        vjw__ihym = f"""def impl(arr, size, pe, tag, cond=True):
            # recv the number of string characters and resize buffer to proper size
            n_chars = bodo.libs.distributed_api.recv(np.int64, pe, tag - 1)
            new_arr = {gsq__znxfz}(size, n_chars)
            bodo.libs.str_arr_ext.move_str_binary_arr_payload(arr, new_arr)

            n_bytes = (size + 7) >> 3
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_offset_ptr(arr),
                size + 1,
                offset_typ_enum,
                pe,
                tag,
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_data_ptr(arr), n_chars, char_typ_enum, pe, tag
            )
            bodo.libs.distributed_api._recv(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(arr),
                n_bytes,
                char_typ_enum,
                pe,
                tag,
            )
            return None"""
        hopjt__xqm = dict()
        exec(vjw__ihym, {'bodo': bodo, 'np': np, 'offset_typ_enum':
            tmbs__twhd, 'char_typ_enum': mya__ddsoq}, hopjt__xqm)
        impl = hopjt__xqm['impl']
        return impl
    raise BodoError(f'irecv(): array type {arr} not supported yet')


_alltoall = types.ExternalFunction('c_alltoall', types.void(types.voidptr,
    types.voidptr, types.int32, types.int32))


@numba.njit
def alltoall(send_arr, recv_arr, count):
    assert count < INT_MAX
    mvqxp__oizp = get_type_enum(send_arr)
    _alltoall(send_arr.ctypes, recv_arr.ctypes, np.int32(count), mvqxp__oizp)


@numba.generated_jit(nopython=True)
def gather_scalar(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    data = types.unliteral(data)
    typ_val = numba_to_c_type(data)
    dtype = data

    def gather_scalar_impl(data, allgather=False, warn_if_rep=True, root=
        MPI_ROOT):
        n_pes = bodo.libs.distributed_api.get_size()
        rank = bodo.libs.distributed_api.get_rank()
        send = np.full(1, data, dtype)
        elyr__wzyyk = n_pes if rank == root or allgather else 0
        hcxb__tsmcd = np.empty(elyr__wzyyk, dtype)
        c_gather_scalar(send.ctypes, hcxb__tsmcd.ctypes, np.int32(typ_val),
            allgather, np.int32(root))
        return hcxb__tsmcd
    return gather_scalar_impl


c_gather_scalar = types.ExternalFunction('c_gather_scalar', types.void(
    types.voidptr, types.voidptr, types.int32, types.bool_, types.int32))
c_gatherv = types.ExternalFunction('c_gatherv', types.void(types.voidptr,
    types.int32, types.voidptr, types.voidptr, types.voidptr, types.int32,
    types.bool_, types.int32))
c_scatterv = types.ExternalFunction('c_scatterv', types.void(types.voidptr,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.int32))


@intrinsic
def value_to_ptr(typingctx, val_tp=None):

    def codegen(context, builder, sig, args):
        bwr__ptlc = cgutils.alloca_once(builder, args[0].type)
        builder.store(args[0], bwr__ptlc)
        return builder.bitcast(bwr__ptlc, lir.IntType(8).as_pointer())
    return types.voidptr(val_tp), codegen


@intrinsic
def load_val_ptr(typingctx, ptr_tp, val_tp=None):

    def codegen(context, builder, sig, args):
        bwr__ptlc = builder.bitcast(args[0], args[1].type.as_pointer())
        return builder.load(bwr__ptlc)
    return val_tp(ptr_tp, val_tp), codegen


_dist_reduce = types.ExternalFunction('dist_reduce', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))
_dist_arr_reduce = types.ExternalFunction('dist_arr_reduce', types.void(
    types.voidptr, types.int64, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_reduce(value, reduce_op):
    if isinstance(value, types.Array):
        typ_enum = np.int32(numba_to_c_type(value.dtype))

        def impl_arr(value, reduce_op):
            A = np.ascontiguousarray(value)
            _dist_arr_reduce(A.ctypes, A.size, reduce_op, typ_enum)
            return A
        return impl_arr
    gafk__fmydn = types.unliteral(value)
    if isinstance(gafk__fmydn, IndexValueType):
        gafk__fmydn = gafk__fmydn.val_typ
        gbkh__jws = [types.bool_, types.uint8, types.int8, types.uint16,
            types.int16, types.uint32, types.int32, types.float32, types.
            float64]
        if not sys.platform.startswith('win'):
            gbkh__jws.append(types.int64)
            gbkh__jws.append(bodo.datetime64ns)
            gbkh__jws.append(bodo.timedelta64ns)
            gbkh__jws.append(bodo.datetime_date_type)
            gbkh__jws.append(bodo.TimeType)
        if gafk__fmydn not in gbkh__jws:
            raise BodoError('argmin/argmax not supported for type {}'.
                format(gafk__fmydn))
    typ_enum = np.int32(numba_to_c_type(gafk__fmydn))

    def impl(value, reduce_op):
        gkt__hzz = value_to_ptr(value)
        zeqqg__hpl = value_to_ptr(value)
        _dist_reduce(gkt__hzz, zeqqg__hpl, reduce_op, typ_enum)
        return load_val_ptr(zeqqg__hpl, value)
    return impl


_dist_exscan = types.ExternalFunction('dist_exscan', types.void(types.
    voidptr, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def dist_exscan(value, reduce_op):
    gafk__fmydn = types.unliteral(value)
    typ_enum = np.int32(numba_to_c_type(gafk__fmydn))
    odt__zmu = gafk__fmydn(0)

    def impl(value, reduce_op):
        gkt__hzz = value_to_ptr(value)
        zeqqg__hpl = value_to_ptr(odt__zmu)
        _dist_exscan(gkt__hzz, zeqqg__hpl, reduce_op, typ_enum)
        return load_val_ptr(zeqqg__hpl, value)
    return impl


@numba.njit
def get_bit(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@numba.njit
def copy_gathered_null_bytes(null_bitmap_ptr, tmp_null_bytes,
    recv_counts_nulls, recv_counts):
    gel__kuyde = 0
    ppaq__mdgsl = 0
    for i in range(len(recv_counts)):
        yjwtd__sdm = recv_counts[i]
        bxl__qrom = recv_counts_nulls[i]
        pbuod__amxey = tmp_null_bytes[gel__kuyde:gel__kuyde + bxl__qrom]
        for gyvj__ntb in range(yjwtd__sdm):
            set_bit_to(null_bitmap_ptr, ppaq__mdgsl, get_bit(pbuod__amxey,
                gyvj__ntb))
            ppaq__mdgsl += 1
        gel__kuyde += bxl__qrom


@numba.generated_jit(nopython=True)
def gatherv(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
    from bodo.libs.csr_matrix_ext import CSRMatrixType
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.gatherv()')
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            scpym__yfihh = bodo.gatherv(data.codes, allgather, root=root)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                scpym__yfihh, data.dtype)
        return impl_cat
    if isinstance(data, types.Array):
        typ_val = numba_to_c_type(data.dtype)

        def gatherv_impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            data = np.ascontiguousarray(data)
            rank = bodo.libs.distributed_api.get_rank()
            emcjo__hsb = data.size
            recv_counts = gather_scalar(np.int32(emcjo__hsb), allgather,
                root=root)
            qbm__uajfc = recv_counts.sum()
            egkr__zmtx = empty_like_type(qbm__uajfc, data)
            gxlu__scn = np.empty(1, np.int32)
            if rank == root or allgather:
                gxlu__scn = bodo.ir.join.calc_disp(recv_counts)
            c_gatherv(data.ctypes, np.int32(emcjo__hsb), egkr__zmtx.ctypes,
                recv_counts.ctypes, gxlu__scn.ctypes, np.int32(typ_val),
                allgather, np.int32(root))
            return egkr__zmtx.reshape((-1,) + data.shape[1:])
        return gatherv_impl
    if is_str_arr_type(data):

        def gatherv_str_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            data = decode_if_dict_array(data)
            egkr__zmtx = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.str_arr_ext.init_str_arr(egkr__zmtx)
        return gatherv_str_arr_impl
    if data == binary_array_type:

        def gatherv_binary_arr_impl(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            egkr__zmtx = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(egkr__zmtx)
        return gatherv_binary_arr_impl
    if data == datetime_timedelta_array_type:
        typ_val = numba_to_c_type(types.int64)
        mya__ddsoq = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            emcjo__hsb = len(data)
            bxl__qrom = emcjo__hsb + 7 >> 3
            recv_counts = gather_scalar(np.int32(emcjo__hsb), allgather,
                root=root)
            qbm__uajfc = recv_counts.sum()
            egkr__zmtx = empty_like_type(qbm__uajfc, data)
            gxlu__scn = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            mzq__ypb = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                gxlu__scn = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                mzq__ypb = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._days_data.ctypes, np.int32(emcjo__hsb),
                egkr__zmtx._days_data.ctypes, recv_counts.ctypes, gxlu__scn
                .ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._seconds_data.ctypes, np.int32(emcjo__hsb),
                egkr__zmtx._seconds_data.ctypes, recv_counts.ctypes,
                gxlu__scn.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._microseconds_data.ctypes, np.int32(emcjo__hsb),
                egkr__zmtx._microseconds_data.ctypes, recv_counts.ctypes,
                gxlu__scn.ctypes, np.int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(bxl__qrom),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, mzq__ypb.
                ctypes, mya__ddsoq, allgather, np.int32(root))
            copy_gathered_null_bytes(egkr__zmtx._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return egkr__zmtx
        return gatherv_impl_int_arr
    if isinstance(data, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, bodo.TimeArrayType)) or data in (boolean_array,
        datetime_date_array_type):
        typ_val = numba_to_c_type(data.dtype)
        mya__ddsoq = np.int32(numba_to_c_type(types.uint8))

        def gatherv_impl_int_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            emcjo__hsb = len(data)
            bxl__qrom = emcjo__hsb + 7 >> 3
            recv_counts = gather_scalar(np.int32(emcjo__hsb), allgather,
                root=root)
            qbm__uajfc = recv_counts.sum()
            egkr__zmtx = empty_like_type(qbm__uajfc, data)
            gxlu__scn = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            mzq__ypb = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                gxlu__scn = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                mzq__ypb = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(data._data.ctypes, np.int32(emcjo__hsb), egkr__zmtx.
                _data.ctypes, recv_counts.ctypes, gxlu__scn.ctypes, np.
                int32(typ_val), allgather, np.int32(root))
            c_gatherv(data._null_bitmap.ctypes, np.int32(bxl__qrom),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, mzq__ypb.
                ctypes, mya__ddsoq, allgather, np.int32(root))
            copy_gathered_null_bytes(egkr__zmtx._null_bitmap.ctypes,
                tmp_null_bytes, recv_counts_nulls, recv_counts)
            return egkr__zmtx
        return gatherv_impl_int_arr
    if isinstance(data, DatetimeArrayType):
        xcz__jek = data.tz

        def impl_pd_datetime_arr(data, allgather=False, warn_if_rep=True,
            root=MPI_ROOT):
            wxe__jxt = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.pd_datetime_arr_ext.init_pandas_datetime_array(
                wxe__jxt, xcz__jek)
        return impl_pd_datetime_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, allgather=False, warn_if_rep=True, root
            =MPI_ROOT):
            ehyb__gvglc = bodo.gatherv(data._left, allgather, warn_if_rep, root
                )
            aaami__fcf = bodo.gatherv(data._right, allgather, warn_if_rep, root
                )
            return bodo.libs.interval_arr_ext.init_interval_array(ehyb__gvglc,
                aaami__fcf)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            hecf__iprf = bodo.hiframes.pd_series_ext.get_series_name(data)
            out_arr = bodo.libs.distributed_api.gatherv(arr, allgather,
                warn_if_rep, root)
            lrb__dnmcg = bodo.gatherv(index, allgather, warn_if_rep, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                lrb__dnmcg, hecf__iprf)
        return impl
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):
        tmtb__sofy = np.iinfo(np.int64).max
        miciu__caph = np.iinfo(np.int64).min

        def impl_range_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            vxkg__tfead = data._start
            irywn__job = data._stop
            if len(data) == 0:
                vxkg__tfead = tmtb__sofy
                irywn__job = miciu__caph
            vxkg__tfead = bodo.libs.distributed_api.dist_reduce(vxkg__tfead,
                np.int32(Reduce_Type.Min.value))
            irywn__job = bodo.libs.distributed_api.dist_reduce(irywn__job,
                np.int32(Reduce_Type.Max.value))
            total_len = bodo.libs.distributed_api.dist_reduce(len(data), np
                .int32(Reduce_Type.Sum.value))
            if vxkg__tfead == tmtb__sofy and irywn__job == miciu__caph:
                vxkg__tfead = 0
                irywn__job = 0
            vlnd__tdq = max(0, -(-(irywn__job - vxkg__tfead) // data._step))
            if vlnd__tdq < total_len:
                irywn__job = vxkg__tfead + data._step * total_len
            if bodo.get_rank() != root and not allgather:
                vxkg__tfead = 0
                irywn__job = 0
            return bodo.hiframes.pd_index_ext.init_range_index(vxkg__tfead,
                irywn__job, data._step, data._name)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        from bodo.hiframes.pd_index_ext import PeriodIndexType
        if isinstance(data, PeriodIndexType):
            smney__rqq = data.freq

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.hiframes.pd_index_ext.init_period_index(arr,
                    data._name, smney__rqq)
        else:

            def impl_pd_index(data, allgather=False, warn_if_rep=True, root
                =MPI_ROOT):
                arr = bodo.libs.distributed_api.gatherv(data._data,
                    allgather, root=root)
                return bodo.utils.conversion.index_from_array(arr, data._name)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            egkr__zmtx = bodo.gatherv(data._data, allgather, root=root)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(egkr__zmtx
                , data._names, data._name)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.table.TableType):
        fkn__gnw = {'bodo': bodo, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like, 'init_table': bodo.hiframes.table.init_table,
            'decode_if_dict_ary': bodo.hiframes.table.init_table}
        vjw__ihym = (
            f'def impl_table(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):\n'
            )
        vjw__ihym += '  T = data\n'
        vjw__ihym += '  T2 = init_table(T, True)\n'
        kdv__hmqq = bodo.hiframes.table.get_init_table_output_type(data, True)
        owm__ixdgk = (bodo.string_array_type in data.type_to_blk and bodo.
            dict_str_arr_type in data.type_to_blk)
        if owm__ixdgk:
            vjw__ihym += (bodo.hiframes.table.
                gen_str_and_dict_enc_cols_to_one_block_fn_txt(data,
                kdv__hmqq, fkn__gnw, True))
        for hipt__kjw, ayrf__xjt in data.type_to_blk.items():
            if owm__ixdgk and hipt__kjw in (bodo.string_array_type, bodo.
                dict_str_arr_type):
                continue
            elif hipt__kjw == bodo.dict_str_arr_type:
                assert bodo.string_array_type in kdv__hmqq.type_to_blk, 'Error in gatherv: If encoded string type is present in the input, then non-encoded string type should be present in the output'
                xvze__ruum = kdv__hmqq.type_to_blk[bodo.string_array_type]
            else:
                assert hipt__kjw in kdv__hmqq.type_to_blk, 'Error in gatherv: All non-encoded string types present in the input should be present in the output'
                xvze__ruum = kdv__hmqq.type_to_blk[hipt__kjw]
            fkn__gnw[f'arr_inds_{ayrf__xjt}'] = np.array(data.
                block_to_arr_ind[ayrf__xjt], dtype=np.int64)
            vjw__ihym += (
                f'  arr_list_{ayrf__xjt} = get_table_block(T, {ayrf__xjt})\n')
            vjw__ihym += f"""  out_arr_list_{ayrf__xjt} = alloc_list_like(arr_list_{ayrf__xjt}, len(arr_list_{ayrf__xjt}), True)
"""
            vjw__ihym += f'  for i in range(len(arr_list_{ayrf__xjt})):\n'
            vjw__ihym += f'    arr_ind_{ayrf__xjt} = arr_inds_{ayrf__xjt}[i]\n'
            vjw__ihym += f"""    ensure_column_unboxed(T, arr_list_{ayrf__xjt}, i, arr_ind_{ayrf__xjt})
"""
            vjw__ihym += f"""    out_arr_{ayrf__xjt} = bodo.gatherv(arr_list_{ayrf__xjt}[i], allgather, warn_if_rep, root)
"""
            vjw__ihym += (
                f'    out_arr_list_{ayrf__xjt}[i] = out_arr_{ayrf__xjt}\n')
            vjw__ihym += (
                f'  T2 = set_table_block(T2, out_arr_list_{ayrf__xjt}, {xvze__ruum})\n'
                )
        vjw__ihym += (
            f'  length = T._len if bodo.get_rank() == root or allgather else 0\n'
            )
        vjw__ihym += f'  T2 = set_table_len(T2, length)\n'
        vjw__ihym += f'  return T2\n'
        hopjt__xqm = {}
        exec(vjw__ihym, fkn__gnw, hopjt__xqm)
        svnmr__jkm = hopjt__xqm['impl_table']
        return svnmr__jkm
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        dbyid__mvh = len(data.columns)
        if dbyid__mvh == 0:
            urts__lmw = ColNamesMetaType(())

            def impl(data, allgather=False, warn_if_rep=True, root=MPI_ROOT):
                index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data
                    )
                nlj__kvxtu = bodo.gatherv(index, allgather, warn_if_rep, root)
                return bodo.hiframes.pd_dataframe_ext.init_dataframe((),
                    nlj__kvxtu, urts__lmw)
            return impl
        ibro__lbf = ', '.join(f'g_data_{i}' for i in range(dbyid__mvh))
        vjw__ihym = (
            'def impl_df(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        if data.is_table_format:
            from bodo.transforms.distributed_analysis import Distribution
            cqum__sbsgd = bodo.hiframes.pd_dataframe_ext.DataFrameType(data
                .data, data.index, data.columns, Distribution.REP, True)
            ibro__lbf = 'T2'
            vjw__ihym += (
                '  T = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            vjw__ihym += (
                '  T2 = bodo.gatherv(T, allgather, warn_if_rep, root)\n')
        else:
            for i in range(dbyid__mvh):
                vjw__ihym += (
                    """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                    .format(i, i))
                vjw__ihym += (
                    '  g_data_{} = bodo.gatherv(data_{}, allgather, warn_if_rep, root)\n'
                    .format(i, i))
        vjw__ihym += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        vjw__ihym += (
            '  g_index = bodo.gatherv(index, allgather, warn_if_rep, root)\n')
        vjw__ihym += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_gatherv_with_cols)
"""
            .format(ibro__lbf))
        hopjt__xqm = {}
        fkn__gnw = {'bodo': bodo, '__col_name_meta_value_gatherv_with_cols':
            ColNamesMetaType(data.columns)}
        exec(vjw__ihym, fkn__gnw, hopjt__xqm)
        fmdl__jega = hopjt__xqm['impl_df']
        return fmdl__jega
    if isinstance(data, ArrayItemArrayType):
        tjzvu__hwmxp = np.int32(numba_to_c_type(types.int32))
        mya__ddsoq = np.int32(numba_to_c_type(types.uint8))

        def gatherv_array_item_arr_impl(data, allgather=False, warn_if_rep=
            True, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            pcu__cpiiz = bodo.libs.array_item_arr_ext.get_offsets(data)
            gjlb__kgen = bodo.libs.array_item_arr_ext.get_data(data)
            gjlb__kgen = gjlb__kgen[:pcu__cpiiz[-1]]
            hwhfa__wbosx = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            emcjo__hsb = len(data)
            scmo__vfefq = np.empty(emcjo__hsb, np.uint32)
            bxl__qrom = emcjo__hsb + 7 >> 3
            for i in range(emcjo__hsb):
                scmo__vfefq[i] = pcu__cpiiz[i + 1] - pcu__cpiiz[i]
            recv_counts = gather_scalar(np.int32(emcjo__hsb), allgather,
                root=root)
            qbm__uajfc = recv_counts.sum()
            gxlu__scn = np.empty(1, np.int32)
            recv_counts_nulls = np.empty(1, np.int32)
            mzq__ypb = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                gxlu__scn = bodo.ir.join.calc_disp(recv_counts)
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for qtpm__xku in range(len(recv_counts)):
                    recv_counts_nulls[qtpm__xku] = recv_counts[qtpm__xku
                        ] + 7 >> 3
                mzq__ypb = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            qgxxf__lobau = np.empty(qbm__uajfc + 1, np.uint32)
            yfosh__vulhn = bodo.gatherv(gjlb__kgen, allgather, warn_if_rep,
                root)
            oin__ifh = np.empty(qbm__uajfc + 7 >> 3, np.uint8)
            c_gatherv(scmo__vfefq.ctypes, np.int32(emcjo__hsb),
                qgxxf__lobau.ctypes, recv_counts.ctypes, gxlu__scn.ctypes,
                tjzvu__hwmxp, allgather, np.int32(root))
            c_gatherv(hwhfa__wbosx.ctypes, np.int32(bxl__qrom),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, mzq__ypb.
                ctypes, mya__ddsoq, allgather, np.int32(root))
            dummy_use(data)
            crnhp__atwgv = np.empty(qbm__uajfc + 1, np.uint64)
            convert_len_arr_to_offset(qgxxf__lobau.ctypes, crnhp__atwgv.
                ctypes, qbm__uajfc)
            copy_gathered_null_bytes(oin__ifh.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            out_arr = bodo.libs.array_item_arr_ext.init_array_item_array(
                qbm__uajfc, yfosh__vulhn, crnhp__atwgv, oin__ifh)
            return out_arr
        return gatherv_array_item_arr_impl
    if isinstance(data, StructArrayType):
        jtvzv__tcbq = data.names
        mya__ddsoq = np.int32(numba_to_c_type(types.uint8))

        def impl_struct_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            puv__wslj = bodo.libs.struct_arr_ext.get_data(data)
            tqlds__evj = bodo.libs.struct_arr_ext.get_null_bitmap(data)
            otixe__qygkg = bodo.gatherv(puv__wslj, allgather=allgather,
                root=root)
            rank = bodo.libs.distributed_api.get_rank()
            emcjo__hsb = len(data)
            bxl__qrom = emcjo__hsb + 7 >> 3
            recv_counts = gather_scalar(np.int32(emcjo__hsb), allgather,
                root=root)
            qbm__uajfc = recv_counts.sum()
            gfwmx__afbo = np.empty(qbm__uajfc + 7 >> 3, np.uint8)
            recv_counts_nulls = np.empty(1, np.int32)
            mzq__ypb = np.empty(1, np.int32)
            tmp_null_bytes = np.empty(1, np.uint8)
            if rank == root or allgather:
                recv_counts_nulls = np.empty(len(recv_counts), np.int32)
                for i in range(len(recv_counts)):
                    recv_counts_nulls[i] = recv_counts[i] + 7 >> 3
                mzq__ypb = bodo.ir.join.calc_disp(recv_counts_nulls)
                tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)
            c_gatherv(tqlds__evj.ctypes, np.int32(bxl__qrom),
                tmp_null_bytes.ctypes, recv_counts_nulls.ctypes, mzq__ypb.
                ctypes, mya__ddsoq, allgather, np.int32(root))
            copy_gathered_null_bytes(gfwmx__afbo.ctypes, tmp_null_bytes,
                recv_counts_nulls, recv_counts)
            return bodo.libs.struct_arr_ext.init_struct_arr(otixe__qygkg,
                gfwmx__afbo, jtvzv__tcbq)
        return impl_struct_arr
    if data == binary_array_type:

        def impl_bin_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            egkr__zmtx = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.binary_arr_ext.init_binary_arr(egkr__zmtx)
        return impl_bin_arr
    if isinstance(data, TupleArrayType):

        def impl_tuple_arr(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            egkr__zmtx = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.tuple_arr_ext.init_tuple_arr(egkr__zmtx)
        return impl_tuple_arr
    if isinstance(data, MapArrayType):

        def impl_map_arr(data, allgather=False, warn_if_rep=True, root=MPI_ROOT
            ):
            egkr__zmtx = bodo.gatherv(data._data, allgather, warn_if_rep, root)
            return bodo.libs.map_arr_ext.init_map_arr(egkr__zmtx)
        return impl_map_arr
    if isinstance(data, CSRMatrixType):

        def impl_csr_matrix(data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT):
            egkr__zmtx = bodo.gatherv(data.data, allgather, warn_if_rep, root)
            xmgno__exc = bodo.gatherv(data.indices, allgather, warn_if_rep,
                root)
            dfyr__ewga = bodo.gatherv(data.indptr, allgather, warn_if_rep, root
                )
            zbs__ubapk = gather_scalar(data.shape[0], allgather, root=root)
            rgla__sso = zbs__ubapk.sum()
            dbyid__mvh = bodo.libs.distributed_api.dist_reduce(data.shape[1
                ], np.int32(Reduce_Type.Max.value))
            ggh__focc = np.empty(rgla__sso + 1, np.int64)
            xmgno__exc = xmgno__exc.astype(np.int64)
            ggh__focc[0] = 0
            knsz__juz = 1
            vmq__rld = 0
            for eeyef__dmt in zbs__ubapk:
                for wxp__ywd in range(eeyef__dmt):
                    efugx__mtfu = dfyr__ewga[vmq__rld + 1] - dfyr__ewga[
                        vmq__rld]
                    ggh__focc[knsz__juz] = ggh__focc[knsz__juz - 1
                        ] + efugx__mtfu
                    knsz__juz += 1
                    vmq__rld += 1
                vmq__rld += 1
            return bodo.libs.csr_matrix_ext.init_csr_matrix(egkr__zmtx,
                xmgno__exc, ggh__focc, (rgla__sso, dbyid__mvh))
        return impl_csr_matrix
    if isinstance(data, types.BaseTuple):
        vjw__ihym = (
            'def impl_tuple(data, allgather=False, warn_if_rep=True, root={}):\n'
            .format(MPI_ROOT))
        vjw__ihym += '  return ({}{})\n'.format(', '.join(
            'bodo.gatherv(data[{}], allgather, warn_if_rep, root)'.format(i
            ) for i in range(len(data))), ',' if len(data) > 0 else '')
        hopjt__xqm = {}
        exec(vjw__ihym, {'bodo': bodo}, hopjt__xqm)
        rqzcf__gnmr = hopjt__xqm['impl_tuple']
        return rqzcf__gnmr
    if data is types.none:
        return (lambda data, allgather=False, warn_if_rep=True, root=
            MPI_ROOT: None)
    try:
        import bodosql
        from bodosql.context_ext import BodoSQLContextType
    except ImportError as jarc__guxe:
        BodoSQLContextType = None
    if BodoSQLContextType is not None and isinstance(data, BodoSQLContextType):
        vjw__ihym = f"""def impl_bodosql_context(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        piza__vko = ', '.join([f"'{hecf__iprf}'" for hecf__iprf in data.names])
        dalu__sgjy = ', '.join([
            f'bodo.gatherv(data.dataframes[{i}], allgather, warn_if_rep, root)'
             for i in range(len(data.dataframes))])
        vjw__ihym += f"""  return bodosql.context_ext.init_sql_context(({piza__vko}, ), ({dalu__sgjy}, ), data.catalog)
"""
        hopjt__xqm = {}
        exec(vjw__ihym, {'bodo': bodo, 'bodosql': bodosql}, hopjt__xqm)
        mth__sin = hopjt__xqm['impl_bodosql_context']
        return mth__sin
    try:
        import bodosql
        from bodosql import TablePathType
    except ImportError as jarc__guxe:
        TablePathType = None
    if TablePathType is not None and isinstance(data, TablePathType):
        vjw__ihym = f"""def impl_table_path(data, allgather=False, warn_if_rep=True, root={MPI_ROOT}):
"""
        vjw__ihym += f'  return data\n'
        hopjt__xqm = {}
        exec(vjw__ihym, {}, hopjt__xqm)
        ssplu__mkyql = hopjt__xqm['impl_table_path']
        return ssplu__mkyql
    raise BodoError('gatherv() not available for {}'.format(data))


@numba.generated_jit(nopython=True)
def rebalance(data, dests=None, random=False, random_seed=None, parallel=False
    ):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.rebalance()')
    vjw__ihym = (
        'def impl(data, dests=None, random=False, random_seed=None, parallel=False):\n'
        )
    vjw__ihym += '    if random:\n'
    vjw__ihym += '        if random_seed is None:\n'
    vjw__ihym += '            random = 1\n'
    vjw__ihym += '        else:\n'
    vjw__ihym += '            random = 2\n'
    vjw__ihym += '    if random_seed is None:\n'
    vjw__ihym += '        random_seed = -1\n'
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        pgzfo__cokhz = data
        dbyid__mvh = len(pgzfo__cokhz.columns)
        for i in range(dbyid__mvh):
            vjw__ihym += f"""    data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
        vjw__ihym += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data))
"""
        ibro__lbf = ', '.join(f'data_{i}' for i in range(dbyid__mvh))
        vjw__ihym += ('    info_list_total = [{}, array_to_info(ind_arr)]\n'
            .format(', '.join('array_to_info(data_{})'.format(qfkz__ewgbi) for
            qfkz__ewgbi in range(dbyid__mvh))))
        vjw__ihym += (
            '    table_total = arr_info_list_to_table(info_list_total)\n')
        vjw__ihym += '    if dests is None:\n'
        vjw__ihym += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        vjw__ihym += '    else:\n'
        vjw__ihym += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        for hxax__bcyse in range(dbyid__mvh):
            vjw__ihym += (
                """    out_arr_{0} = info_to_array(info_from_table(out_table, {0}), data_{0})
"""
                .format(hxax__bcyse))
        vjw__ihym += (
            '    out_arr_index = info_to_array(info_from_table(out_table, {}), ind_arr)\n'
            .format(dbyid__mvh))
        vjw__ihym += '    delete_table(out_table)\n'
        vjw__ihym += '    if parallel:\n'
        vjw__ihym += '        delete_table(table_total)\n'
        ibro__lbf = ', '.join('out_arr_{}'.format(i) for i in range(dbyid__mvh)
            )
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        vjw__ihym += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), {}, __col_name_meta_value_rebalance)
"""
            .format(ibro__lbf, index))
    elif isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):
        vjw__ihym += (
            '    data_0 = bodo.hiframes.pd_series_ext.get_series_data(data)\n')
        vjw__ihym += """    ind_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(data))
"""
        vjw__ihym += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(data)\n')
        vjw__ihym += """    table_total = arr_info_list_to_table([array_to_info(data_0), array_to_info(ind_arr)])
"""
        vjw__ihym += '    if dests is None:\n'
        vjw__ihym += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        vjw__ihym += '    else:\n'
        vjw__ihym += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        vjw__ihym += (
            '    out_arr_0 = info_to_array(info_from_table(out_table, 0), data_0)\n'
            )
        vjw__ihym += (
            '    out_arr_index = info_to_array(info_from_table(out_table, 1), ind_arr)\n'
            )
        vjw__ihym += '    delete_table(out_table)\n'
        vjw__ihym += '    if parallel:\n'
        vjw__ihym += '        delete_table(table_total)\n'
        index = 'bodo.utils.conversion.index_from_array(out_arr_index)'
        vjw__ihym += f"""    return bodo.hiframes.pd_series_ext.init_series(out_arr_0, {index}, name)
"""
    elif isinstance(data, types.Array):
        assert is_overload_false(random
            ), 'Call random_shuffle instead of rebalance'
        vjw__ihym += '    if not parallel:\n'
        vjw__ihym += '        return data\n'
        vjw__ihym += """    dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        vjw__ihym += '    if dests is None:\n'
        vjw__ihym += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        vjw__ihym += '    elif bodo.get_rank() not in dests:\n'
        vjw__ihym += '        dim0_local_size = 0\n'
        vjw__ihym += '    else:\n'
        vjw__ihym += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, len(dests), dests.index(bodo.get_rank()))
"""
        vjw__ihym += """    out = np.empty((dim0_local_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        vjw__ihym += """    bodo.libs.distributed_api.dist_oneD_reshape_shuffle(out, data, dim0_global_size, dests)
"""
        vjw__ihym += '    return out\n'
    elif bodo.utils.utils.is_array_typ(data, False):
        vjw__ihym += (
            '    table_total = arr_info_list_to_table([array_to_info(data)])\n'
            )
        vjw__ihym += '    if dests is None:\n'
        vjw__ihym += """        out_table = shuffle_renormalization(table_total, random, random_seed, parallel)
"""
        vjw__ihym += '    else:\n'
        vjw__ihym += """        out_table = shuffle_renormalization_group(table_total, random, random_seed, parallel, len(dests), np.array(dests, dtype=np.int32).ctypes)
"""
        vjw__ihym += (
            '    out_arr = info_to_array(info_from_table(out_table, 0), data)\n'
            )
        vjw__ihym += '    delete_table(out_table)\n'
        vjw__ihym += '    if parallel:\n'
        vjw__ihym += '        delete_table(table_total)\n'
        vjw__ihym += '    return out_arr\n'
    else:
        raise BodoError(f'Type {data} not supported for bodo.rebalance')
    hopjt__xqm = {}
    fkn__gnw = {'np': np, 'bodo': bodo, 'array_to_info': bodo.libs.array.
        array_to_info, 'shuffle_renormalization': bodo.libs.array.
        shuffle_renormalization, 'shuffle_renormalization_group': bodo.libs
        .array.shuffle_renormalization_group, 'arr_info_list_to_table':
        bodo.libs.array.arr_info_list_to_table, 'info_from_table': bodo.
        libs.array.info_from_table, 'info_to_array': bodo.libs.array.
        info_to_array, 'delete_table': bodo.libs.array.delete_table}
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        fkn__gnw.update({'__col_name_meta_value_rebalance':
            ColNamesMetaType(pgzfo__cokhz.columns)})
    exec(vjw__ihym, fkn__gnw, hopjt__xqm)
    impl = hopjt__xqm['impl']
    return impl


@numba.generated_jit(nopython=True)
def random_shuffle(data, seed=None, dests=None, n_samples=None, parallel=False
    ):
    vjw__ihym = (
        'def impl(data, seed=None, dests=None, n_samples=None, parallel=False):\n'
        )
    if isinstance(data, types.Array):
        if not is_overload_none(dests):
            raise BodoError('not supported')
        vjw__ihym += '    if seed is None:\n'
        vjw__ihym += """        seed = bodo.libs.distributed_api.bcast_scalar(np.random.randint(0, 2**31))
"""
        vjw__ihym += '    np.random.seed(seed)\n'
        vjw__ihym += '    if not parallel:\n'
        vjw__ihym += '        data = data.copy()\n'
        vjw__ihym += '        np.random.shuffle(data)\n'
        if not is_overload_none(n_samples):
            vjw__ihym += '        data = data[:n_samples]\n'
        vjw__ihym += '        return data\n'
        vjw__ihym += '    else:\n'
        vjw__ihym += """        dim0_global_size = bodo.libs.distributed_api.dist_reduce(data.shape[0], np.int32(bodo.libs.distributed_api.Reduce_Type.Sum.value))
"""
        vjw__ihym += '        permutation = np.arange(dim0_global_size)\n'
        vjw__ihym += '        np.random.shuffle(permutation)\n'
        if not is_overload_none(n_samples):
            vjw__ihym += (
                '        n_samples = max(0, min(dim0_global_size, n_samples))\n'
                )
        else:
            vjw__ihym += '        n_samples = dim0_global_size\n'
        vjw__ihym += """        dim0_local_size = bodo.libs.distributed_api.get_node_portion(dim0_global_size, bodo.get_size(), bodo.get_rank())
"""
        vjw__ihym += """        dim0_output_size = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
        vjw__ihym += """        output = np.empty((dim0_output_size,) + tuple(data.shape[1:]), dtype=data.dtype)
"""
        vjw__ihym += (
            '        dtype_size = bodo.io.np_io.get_dtype_size(data.dtype)\n')
        vjw__ihym += """        bodo.libs.distributed_api.dist_permutation_array_index(output, dim0_global_size, dtype_size, data, permutation, len(permutation), n_samples)
"""
        vjw__ihym += '        return output\n'
    else:
        vjw__ihym += """    output = bodo.libs.distributed_api.rebalance(data, dests=dests, random=True, random_seed=seed, parallel=parallel)
"""
        if not is_overload_none(n_samples):
            vjw__ihym += """    local_n_samples = bodo.libs.distributed_api.get_node_portion(n_samples, bodo.get_size(), bodo.get_rank())
"""
            vjw__ihym += '    output = output[:local_n_samples]\n'
        vjw__ihym += '    return output\n'
    hopjt__xqm = {}
    exec(vjw__ihym, {'np': np, 'bodo': bodo}, hopjt__xqm)
    impl = hopjt__xqm['impl']
    return impl


@numba.generated_jit(nopython=True)
def allgatherv(data, warn_if_rep=True, root=MPI_ROOT):
    return lambda data, warn_if_rep=True, root=MPI_ROOT: gatherv(data, True,
        warn_if_rep, root)


@numba.njit
def get_scatter_null_bytes_buff(null_bitmap_ptr, sendcounts, sendcounts_nulls):
    if bodo.get_rank() != MPI_ROOT:
        return np.empty(1, np.uint8)
    qhigi__logc = np.empty(sendcounts_nulls.sum(), np.uint8)
    gel__kuyde = 0
    ppaq__mdgsl = 0
    for uyhd__bel in range(len(sendcounts)):
        yjwtd__sdm = sendcounts[uyhd__bel]
        bxl__qrom = sendcounts_nulls[uyhd__bel]
        pbuod__amxey = qhigi__logc[gel__kuyde:gel__kuyde + bxl__qrom]
        for gyvj__ntb in range(yjwtd__sdm):
            set_bit_to_arr(pbuod__amxey, gyvj__ntb, get_bit_bitmap(
                null_bitmap_ptr, ppaq__mdgsl))
            ppaq__mdgsl += 1
        gel__kuyde += bxl__qrom
    return qhigi__logc


def _bcast_dtype(data, root=MPI_ROOT):
    try:
        from mpi4py import MPI
    except:
        raise BodoError('mpi4py is required for scatterv')
    hldnx__ywx = MPI.COMM_WORLD
    data = hldnx__ywx.bcast(data, root)
    return data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_scatterv_send_counts(send_counts, n_pes, n):
    if not is_overload_none(send_counts):
        return lambda send_counts, n_pes, n: send_counts

    def impl(send_counts, n_pes, n):
        send_counts = np.empty(n_pes, np.int32)
        for i in range(n_pes):
            send_counts[i] = get_node_portion(n, n_pes, i)
        return send_counts
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _scatterv_np(data, send_counts=None, warn_if_dist=True):
    typ_val = numba_to_c_type(data.dtype)
    pjak__bzc = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    kbiz__rzfap = (0,) * pjak__bzc

    def scatterv_arr_impl(data, send_counts=None, warn_if_dist=True):
        rank = bodo.libs.distributed_api.get_rank()
        n_pes = bodo.libs.distributed_api.get_size()
        mgf__cuura = np.ascontiguousarray(data)
        pfd__xfwge = data.ctypes
        nrl__udday = kbiz__rzfap
        if rank == MPI_ROOT:
            nrl__udday = mgf__cuura.shape
        nrl__udday = bcast_tuple(nrl__udday)
        bicnb__tbukk = get_tuple_prod(nrl__udday[1:])
        send_counts = _get_scatterv_send_counts(send_counts, n_pes,
            nrl__udday[0])
        send_counts *= bicnb__tbukk
        emcjo__hsb = send_counts[rank]
        ihmp__nfsqd = np.empty(emcjo__hsb, dtype)
        gxlu__scn = bodo.ir.join.calc_disp(send_counts)
        c_scatterv(pfd__xfwge, send_counts.ctypes, gxlu__scn.ctypes,
            ihmp__nfsqd.ctypes, np.int32(emcjo__hsb), np.int32(typ_val))
        return ihmp__nfsqd.reshape((-1,) + nrl__udday[1:])
    return scatterv_arr_impl


def _get_name_value_for_type(name_typ):
    assert isinstance(name_typ, (types.UnicodeType, types.StringLiteral)
        ) or name_typ == types.none
    return None if name_typ == types.none else '_' + str(ir_utils.next_label())


def get_value_for_type(dtype):
    if isinstance(dtype, types.Array):
        return np.zeros((1,) * dtype.ndim, numba.np.numpy_support.as_dtype(
            dtype.dtype))
    if dtype == string_array_type:
        return pd.array(['A'], 'string')
    if dtype == bodo.dict_str_arr_type:
        import pyarrow as pa
        return pa.array(['a'], type=pa.dictionary(pa.int32(), pa.string()))
    if dtype == binary_array_type:
        return np.array([b'A'], dtype=object)
    if isinstance(dtype, IntegerArrayType):
        qyf__foiv = '{}Int{}'.format('' if dtype.dtype.signed else 'U',
            dtype.dtype.bitwidth)
        return pd.array([3], qyf__foiv)
    if isinstance(dtype, FloatingArrayType):
        qyf__foiv = 'Float{}'.format(dtype.dtype.bitwidth)
        return pd.array([3.0], qyf__foiv)
    if dtype == boolean_array:
        return pd.array([True], 'boolean')
    if isinstance(dtype, DecimalArrayType):
        return np.array([Decimal('32.1')])
    if dtype == datetime_date_array_type:
        return np.array([datetime.date(2011, 8, 9)])
    if dtype == datetime_timedelta_array_type:
        return np.array([datetime.timedelta(33)])
    if bodo.hiframes.pd_index_ext.is_pd_index_type(dtype):
        hecf__iprf = _get_name_value_for_type(dtype.name_typ)
        if isinstance(dtype, bodo.hiframes.pd_index_ext.RangeIndexType):
            return pd.RangeIndex(1, name=hecf__iprf)
        grib__ngyxw = bodo.utils.typing.get_index_data_arr_types(dtype)[0]
        arr = get_value_for_type(grib__ngyxw)
        return pd.Index(arr, name=hecf__iprf)
    if isinstance(dtype, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        import pyarrow as pa
        hecf__iprf = _get_name_value_for_type(dtype.name_typ)
        jtvzv__tcbq = tuple(_get_name_value_for_type(t) for t in dtype.
            names_typ)
        bdzpa__aqfl = tuple(get_value_for_type(t) for t in dtype.array_types)
        bdzpa__aqfl = tuple(a.to_numpy(False) if isinstance(a, pa.Array) else
            a for a in bdzpa__aqfl)
        val = pd.MultiIndex.from_arrays(bdzpa__aqfl, names=jtvzv__tcbq)
        val.name = hecf__iprf
        return val
    if isinstance(dtype, bodo.hiframes.pd_series_ext.SeriesType):
        hecf__iprf = _get_name_value_for_type(dtype.name_typ)
        arr = get_value_for_type(dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.Series(arr, index, name=hecf__iprf)
    if isinstance(dtype, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        bdzpa__aqfl = tuple(get_value_for_type(t) for t in dtype.data)
        index = get_value_for_type(dtype.index)
        return pd.DataFrame({hecf__iprf: arr for hecf__iprf, arr in zip(
            dtype.columns, bdzpa__aqfl)}, index)
    if isinstance(dtype, CategoricalArrayType):
        return pd.Categorical.from_codes([0], dtype.dtype.categories)
    if isinstance(dtype, types.BaseTuple):
        return tuple(get_value_for_type(t) for t in dtype.types)
    if isinstance(dtype, ArrayItemArrayType):
        return pd.Series([get_value_for_type(dtype.dtype),
            get_value_for_type(dtype.dtype)]).values
    if isinstance(dtype, IntervalArrayType):
        grib__ngyxw = get_value_for_type(dtype.arr_type)
        return pd.arrays.IntervalArray([pd.Interval(grib__ngyxw[0],
            grib__ngyxw[0])])
    raise BodoError(f'get_value_for_type(dtype): Missing data type {dtype}')


def scatterv(data, send_counts=None, warn_if_dist=True):
    rank = bodo.libs.distributed_api.get_rank()
    if rank != MPI_ROOT and data is not None:
        warnings.warn(BodoWarning(
            "bodo.scatterv(): A non-None value for 'data' was found on a rank other than the root. This data won't be sent to any other ranks and will be overwritten with data from rank 0."
            ))
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return scatterv_impl(data, send_counts)


@overload(scatterv)
def scatterv_overload(data, send_counts=None, warn_if_dist=True):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.scatterv()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'bodo.scatterv()')
    return lambda data, send_counts=None, warn_if_dist=True: scatterv_impl(data
        , send_counts)


@numba.generated_jit(nopython=True)
def scatterv_impl(data, send_counts=None, warn_if_dist=True):
    if isinstance(data, types.Array):
        return lambda data, send_counts=None, warn_if_dist=True: _scatterv_np(
            data, send_counts)
    if data in (string_array_type, binary_array_type):
        tjzvu__hwmxp = np.int32(numba_to_c_type(types.int32))
        mya__ddsoq = np.int32(numba_to_c_type(types.uint8))
        if data == binary_array_type:
            gsq__znxfz = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
        else:
            gsq__znxfz = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
        vjw__ihym = f"""def impl(
            data, send_counts=None, warn_if_dist=True
        ):  # pragma: no cover
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            n_all = bodo.libs.distributed_api.bcast_scalar(len(data))

            # convert offsets to lengths of strings
            send_arr_lens = np.empty(
                len(data), np.uint32
            )  # XXX offset type is offset_type, lengths for comm are uint32
            for i in range(len(data)):
                send_arr_lens[i] = bodo.libs.str_arr_ext.get_str_arr_item_length(
                    data, i
                )

            # ------- calculate buffer counts -------

            send_counts = bodo.libs.distributed_api._get_scatterv_send_counts(send_counts, n_pes, n_all)

            # displacements
            displs = bodo.ir.join.calc_disp(send_counts)

            # compute send counts for characters
            send_counts_char = np.empty(n_pes, np.int32)
            if rank == 0:
                curr_str = 0
                for i in range(n_pes):
                    c = 0
                    for _ in range(send_counts[i]):
                        c += send_arr_lens[curr_str]
                        curr_str += 1
                    send_counts_char[i] = c

            bodo.libs.distributed_api.bcast(send_counts_char)

            # displacements for characters
            displs_char = bodo.ir.join.calc_disp(send_counts_char)

            # compute send counts for nulls
            send_counts_nulls = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                send_counts_nulls[i] = (send_counts[i] + 7) >> 3

            # displacements for nulls
            displs_nulls = bodo.ir.join.calc_disp(send_counts_nulls)

            # alloc output array
            n_loc = send_counts[rank]  # total number of elements on this PE
            n_loc_char = send_counts_char[rank]
            recv_arr = {gsq__znxfz}(n_loc, n_loc_char)

            # ----- string lengths -----------

            recv_lens = np.empty(n_loc, np.uint32)
            bodo.libs.distributed_api.c_scatterv(
                send_arr_lens.ctypes,
                send_counts.ctypes,
                displs.ctypes,
                recv_lens.ctypes,
                np.int32(n_loc),
                int32_typ_enum,
            )

            # TODO: don't hardcode offset type. Also, if offset is 32 bit we can
            # use the same buffer
            bodo.libs.str_arr_ext.convert_len_arr_to_offset(recv_lens.ctypes, bodo.libs.str_arr_ext.get_offset_ptr(recv_arr), n_loc)

            # ----- string characters -----------

            bodo.libs.distributed_api.c_scatterv(
                bodo.libs.str_arr_ext.get_data_ptr(data),
                send_counts_char.ctypes,
                displs_char.ctypes,
                bodo.libs.str_arr_ext.get_data_ptr(recv_arr),
                np.int32(n_loc_char),
                char_typ_enum,
            )

            # ----------- null bitmap -------------

            n_recv_bytes = (n_loc + 7) >> 3

            send_null_bitmap = bodo.libs.distributed_api.get_scatter_null_bytes_buff(
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(data), send_counts, send_counts_nulls
            )

            bodo.libs.distributed_api.c_scatterv(
                send_null_bitmap.ctypes,
                send_counts_nulls.ctypes,
                displs_nulls.ctypes,
                bodo.libs.str_arr_ext.get_null_bitmap_ptr(recv_arr),
                np.int32(n_recv_bytes),
                char_typ_enum,
            )

            return recv_arr"""
        hopjt__xqm = dict()
        exec(vjw__ihym, {'bodo': bodo, 'np': np, 'int32_typ_enum':
            tjzvu__hwmxp, 'char_typ_enum': mya__ddsoq,
            'decode_if_dict_array': decode_if_dict_array}, hopjt__xqm)
        impl = hopjt__xqm['impl']
        return impl
    if isinstance(data, ArrayItemArrayType):
        tjzvu__hwmxp = np.int32(numba_to_c_type(types.int32))
        mya__ddsoq = np.int32(numba_to_c_type(types.uint8))

        def scatterv_array_item_impl(data, send_counts=None, warn_if_dist=True
            ):
            bnkzl__ggqam = bodo.libs.array_item_arr_ext.get_offsets(data)
            hsujf__jqk = bodo.libs.array_item_arr_ext.get_data(data)
            hsujf__jqk = hsujf__jqk[:bnkzl__ggqam[-1]]
            bzu__attqb = bodo.libs.array_item_arr_ext.get_null_bitmap(data)
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            xwoj__izhy = bcast_scalar(len(data))
            jtfd__hbi = np.empty(len(data), np.uint32)
            for i in range(len(data)):
                jtfd__hbi[i] = bnkzl__ggqam[i + 1] - bnkzl__ggqam[i]
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                xwoj__izhy)
            gxlu__scn = bodo.ir.join.calc_disp(send_counts)
            gftxb__ynkky = np.empty(n_pes, np.int32)
            if rank == 0:
                winq__cwp = 0
                for i in range(n_pes):
                    coeqw__xjzte = 0
                    for wxp__ywd in range(send_counts[i]):
                        coeqw__xjzte += jtfd__hbi[winq__cwp]
                        winq__cwp += 1
                    gftxb__ynkky[i] = coeqw__xjzte
            bcast(gftxb__ynkky)
            cey__pausr = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                cey__pausr[i] = send_counts[i] + 7 >> 3
            mzq__ypb = bodo.ir.join.calc_disp(cey__pausr)
            emcjo__hsb = send_counts[rank]
            ltvj__vabsx = np.empty(emcjo__hsb + 1, np_offset_type)
            rsbjx__bbad = bodo.libs.distributed_api.scatterv_impl(hsujf__jqk,
                gftxb__ynkky)
            uaeoc__ais = emcjo__hsb + 7 >> 3
            lsqs__muvr = np.empty(uaeoc__ais, np.uint8)
            qhbg__tuejs = np.empty(emcjo__hsb, np.uint32)
            c_scatterv(jtfd__hbi.ctypes, send_counts.ctypes, gxlu__scn.
                ctypes, qhbg__tuejs.ctypes, np.int32(emcjo__hsb), tjzvu__hwmxp)
            convert_len_arr_to_offset(qhbg__tuejs.ctypes, ltvj__vabsx.
                ctypes, emcjo__hsb)
            dqwax__vqdn = get_scatter_null_bytes_buff(bzu__attqb.ctypes,
                send_counts, cey__pausr)
            c_scatterv(dqwax__vqdn.ctypes, cey__pausr.ctypes, mzq__ypb.
                ctypes, lsqs__muvr.ctypes, np.int32(uaeoc__ais), mya__ddsoq)
            return bodo.libs.array_item_arr_ext.init_array_item_array(
                emcjo__hsb, rsbjx__bbad, ltvj__vabsx, lsqs__muvr)
        return scatterv_array_item_impl
    if isinstance(data, (IntegerArrayType, FloatingArrayType, DecimalArrayType)
        ) or data in (boolean_array, datetime_date_array_type):
        mya__ddsoq = np.int32(numba_to_c_type(types.uint8))
        if isinstance(data, IntegerArrayType):
            npx__xkbc = bodo.libs.int_arr_ext.init_integer_array
        if isinstance(data, FloatingArrayType):
            npx__xkbc = bodo.libs.float_arr_ext.init_float_array
        if isinstance(data, DecimalArrayType):
            precision = data.precision
            scale = data.scale
            npx__xkbc = numba.njit(no_cpython_wrapper=True)(lambda d, b:
                bodo.libs.decimal_arr_ext.init_decimal_array(d, b,
                precision, scale))
        if data == boolean_array:
            npx__xkbc = bodo.libs.bool_arr_ext.init_bool_array
        if data == datetime_date_array_type:
            npx__xkbc = (bodo.hiframes.datetime_date_ext.
                init_datetime_date_array)

        def scatterv_impl_int_arr(data, send_counts=None, warn_if_dist=True):
            n_pes = bodo.libs.distributed_api.get_size()
            mgf__cuura = data._data
            tqlds__evj = data._null_bitmap
            pqxfm__wyn = len(mgf__cuura)
            bim__iacu = _scatterv_np(mgf__cuura, send_counts)
            xwoj__izhy = bcast_scalar(pqxfm__wyn)
            onjr__wbcr = len(bim__iacu) + 7 >> 3
            nfdv__ykmnx = np.empty(onjr__wbcr, np.uint8)
            send_counts = _get_scatterv_send_counts(send_counts, n_pes,
                xwoj__izhy)
            cey__pausr = np.empty(n_pes, np.int32)
            for i in range(n_pes):
                cey__pausr[i] = send_counts[i] + 7 >> 3
            mzq__ypb = bodo.ir.join.calc_disp(cey__pausr)
            dqwax__vqdn = get_scatter_null_bytes_buff(tqlds__evj.ctypes,
                send_counts, cey__pausr)
            c_scatterv(dqwax__vqdn.ctypes, cey__pausr.ctypes, mzq__ypb.
                ctypes, nfdv__ykmnx.ctypes, np.int32(onjr__wbcr), mya__ddsoq)
            return npx__xkbc(bim__iacu, nfdv__ykmnx)
        return scatterv_impl_int_arr
    if isinstance(data, IntervalArrayType):

        def impl_interval_arr(data, send_counts=None, warn_if_dist=True):
            zchod__bfi = bodo.libs.distributed_api.scatterv_impl(data._left,
                send_counts)
            gqbq__ktlp = bodo.libs.distributed_api.scatterv_impl(data.
                _right, send_counts)
            return bodo.libs.interval_arr_ext.init_interval_array(zchod__bfi,
                gqbq__ktlp)
        return impl_interval_arr
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, send_counts=None, warn_if_dist=True):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            vxkg__tfead = data._start
            irywn__job = data._stop
            vhxqt__flx = data._step
            hecf__iprf = data._name
            hecf__iprf = bcast_scalar(hecf__iprf)
            vxkg__tfead = bcast_scalar(vxkg__tfead)
            irywn__job = bcast_scalar(irywn__job)
            vhxqt__flx = bcast_scalar(vhxqt__flx)
            irtz__aki = bodo.libs.array_kernels.calc_nitems(vxkg__tfead,
                irywn__job, vhxqt__flx)
            chunk_start = bodo.libs.distributed_api.get_start(irtz__aki,
                n_pes, rank)
            jki__qln = bodo.libs.distributed_api.get_node_portion(irtz__aki,
                n_pes, rank)
            fnyx__nrzv = vxkg__tfead + vhxqt__flx * chunk_start
            cnlgx__okt = vxkg__tfead + vhxqt__flx * (chunk_start + jki__qln)
            cnlgx__okt = min(cnlgx__okt, irywn__job)
            return bodo.hiframes.pd_index_ext.init_range_index(fnyx__nrzv,
                cnlgx__okt, vhxqt__flx, hecf__iprf)
        return impl_range_index
    if isinstance(data, bodo.hiframes.pd_index_ext.PeriodIndexType):
        smney__rqq = data.freq

        def impl_period_index(data, send_counts=None, warn_if_dist=True):
            mgf__cuura = data._data
            hecf__iprf = data._name
            hecf__iprf = bcast_scalar(hecf__iprf)
            arr = bodo.libs.distributed_api.scatterv_impl(mgf__cuura,
                send_counts)
            return bodo.hiframes.pd_index_ext.init_period_index(arr,
                hecf__iprf, smney__rqq)
        return impl_period_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, send_counts=None, warn_if_dist=True):
            mgf__cuura = data._data
            hecf__iprf = data._name
            hecf__iprf = bcast_scalar(hecf__iprf)
            arr = bodo.libs.distributed_api.scatterv_impl(mgf__cuura,
                send_counts)
            return bodo.utils.conversion.index_from_array(arr, hecf__iprf)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):

        def impl_multi_index(data, send_counts=None, warn_if_dist=True):
            egkr__zmtx = bodo.libs.distributed_api.scatterv_impl(data._data,
                send_counts)
            hecf__iprf = bcast_scalar(data._name)
            jtvzv__tcbq = bcast_tuple(data._names)
            return bodo.hiframes.pd_multi_index_ext.init_multi_index(egkr__zmtx
                , jtvzv__tcbq, hecf__iprf)
        return impl_multi_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, send_counts=None, warn_if_dist=True):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            hecf__iprf = bodo.hiframes.pd_series_ext.get_series_name(data)
            pnebi__vmdgp = bcast_scalar(hecf__iprf)
            out_arr = bodo.libs.distributed_api.scatterv_impl(arr, send_counts)
            lrb__dnmcg = bodo.libs.distributed_api.scatterv_impl(index,
                send_counts)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                lrb__dnmcg, pnebi__vmdgp)
        return impl_series
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        dbyid__mvh = len(data.columns)
        fffbz__ouec = ColNamesMetaType(data.columns)
        vjw__ihym = 'def impl_df(data, send_counts=None, warn_if_dist=True):\n'
        if data.is_table_format:
            vjw__ihym += (
                '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(data)\n'
                )
            vjw__ihym += """  g_table = bodo.libs.distributed_api.scatterv_impl(table, send_counts)
"""
            ibro__lbf = 'g_table'
        else:
            for i in range(dbyid__mvh):
                vjw__ihym += f"""  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i})
"""
                vjw__ihym += f"""  g_data_{i} = bodo.libs.distributed_api.scatterv_impl(data_{i}, send_counts)
"""
            ibro__lbf = ', '.join(f'g_data_{i}' for i in range(dbyid__mvh))
        vjw__ihym += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        vjw__ihym += (
            '  g_index = bodo.libs.distributed_api.scatterv_impl(index, send_counts)\n'
            )
        vjw__ihym += f"""  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({ibro__lbf},), g_index, __col_name_meta_scaterv_impl)
"""
        hopjt__xqm = {}
        exec(vjw__ihym, {'bodo': bodo, '__col_name_meta_scaterv_impl':
            fffbz__ouec}, hopjt__xqm)
        fmdl__jega = hopjt__xqm['impl_df']
        return fmdl__jega
    if isinstance(data, bodo.TableType):
        vjw__ihym = (
            'def impl_table(data, send_counts=None, warn_if_dist=True):\n')
        vjw__ihym += '  T = data\n'
        vjw__ihym += '  T2 = init_table(T, False)\n'
        vjw__ihym += '  l = 0\n'
        fkn__gnw = {}
        for ubt__kaj in data.type_to_blk.values():
            fkn__gnw[f'arr_inds_{ubt__kaj}'] = np.array(data.
                block_to_arr_ind[ubt__kaj], dtype=np.int64)
            vjw__ihym += (
                f'  arr_list_{ubt__kaj} = get_table_block(T, {ubt__kaj})\n')
            vjw__ihym += f"""  out_arr_list_{ubt__kaj} = alloc_list_like(arr_list_{ubt__kaj}, len(arr_list_{ubt__kaj}), False)
"""
            vjw__ihym += f'  for i in range(len(arr_list_{ubt__kaj})):\n'
            vjw__ihym += f'    arr_ind_{ubt__kaj} = arr_inds_{ubt__kaj}[i]\n'
            vjw__ihym += f"""    ensure_column_unboxed(T, arr_list_{ubt__kaj}, i, arr_ind_{ubt__kaj})
"""
            vjw__ihym += f"""    out_arr_{ubt__kaj} = bodo.libs.distributed_api.scatterv_impl(arr_list_{ubt__kaj}[i], send_counts)
"""
            vjw__ihym += (
                f'    out_arr_list_{ubt__kaj}[i] = out_arr_{ubt__kaj}\n')
            vjw__ihym += f'    l = len(out_arr_{ubt__kaj})\n'
            vjw__ihym += (
                f'  T2 = set_table_block(T2, out_arr_list_{ubt__kaj}, {ubt__kaj})\n'
                )
        vjw__ihym += f'  T2 = set_table_len(T2, l)\n'
        vjw__ihym += f'  return T2\n'
        fkn__gnw.update({'bodo': bodo, 'init_table': bodo.hiframes.table.
            init_table, 'get_table_block': bodo.hiframes.table.
            get_table_block, 'ensure_column_unboxed': bodo.hiframes.table.
            ensure_column_unboxed, 'set_table_block': bodo.hiframes.table.
            set_table_block, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'alloc_list_like': bodo.hiframes.table.
            alloc_list_like})
        hopjt__xqm = {}
        exec(vjw__ihym, fkn__gnw, hopjt__xqm)
        return hopjt__xqm['impl_table']
    if data == bodo.dict_str_arr_type:

        def impl_dict_arr(data, send_counts=None, warn_if_dist=True):
            if bodo.get_rank() == 0:
                wtmt__ziiq = data._data
                bodo.libs.distributed_api.bcast_scalar(len(wtmt__ziiq))
                bodo.libs.distributed_api.bcast_scalar(np.int64(bodo.libs.
                    str_arr_ext.num_total_chars(wtmt__ziiq)))
            else:
                vlnd__tdq = bodo.libs.distributed_api.bcast_scalar(0)
                mhr__bqgar = bodo.libs.distributed_api.bcast_scalar(0)
                wtmt__ziiq = bodo.libs.str_arr_ext.pre_alloc_string_array(
                    vlnd__tdq, mhr__bqgar)
            bodo.libs.distributed_api.bcast(wtmt__ziiq)
            lfzzr__yivk = bodo.libs.distributed_api.scatterv_impl(data.
                _indices, send_counts)
            return bodo.libs.dict_arr_ext.init_dict_arr(wtmt__ziiq,
                lfzzr__yivk, True, data._has_deduped_local_dictionary)
        return impl_dict_arr
    if isinstance(data, CategoricalArrayType):

        def impl_cat(data, send_counts=None, warn_if_dist=True):
            scpym__yfihh = bodo.libs.distributed_api.scatterv_impl(data.
                codes, send_counts)
            return bodo.hiframes.pd_categorical_ext.init_categorical_array(
                scpym__yfihh, data.dtype)
        return impl_cat
    if isinstance(data, types.BaseTuple):
        vjw__ihym = (
            'def impl_tuple(data, send_counts=None, warn_if_dist=True):\n')
        vjw__ihym += '  return ({}{})\n'.format(', '.join(
            f'bodo.libs.distributed_api.scatterv_impl(data[{i}], send_counts)'
             for i in range(len(data))), ',' if len(data) > 0 else '')
        hopjt__xqm = {}
        exec(vjw__ihym, {'bodo': bodo}, hopjt__xqm)
        rqzcf__gnmr = hopjt__xqm['impl_tuple']
        return rqzcf__gnmr
    if data is types.none:
        return lambda data, send_counts=None, warn_if_dist=True: None
    raise BodoError('scatterv() not available for {}'.format(data))


@intrinsic
def cptr_to_voidptr(typingctx, cptr_tp=None):

    def codegen(context, builder, sig, args):
        return builder.bitcast(args[0], lir.IntType(8).as_pointer())
    return types.voidptr(cptr_tp), codegen


def bcast(data, root=MPI_ROOT):
    return


@overload(bcast, no_unliteral=True)
def bcast_overload(data, root=MPI_ROOT):
    if isinstance(data, types.Array):

        def bcast_impl(data, root=MPI_ROOT):
            typ_enum = get_type_enum(data)
            count = data.size
            assert count < INT_MAX
            c_bcast(data.ctypes, np.int32(count), typ_enum, np.array([-1]).
                ctypes, 0, np.int32(root))
            return
        return bcast_impl
    if isinstance(data, DecimalArrayType):

        def bcast_decimal_arr(data, root=MPI_ROOT):
            count = data._data.size
            assert count < INT_MAX
            c_bcast(data._data.ctypes, np.int32(count), CTypeEnum.Int128.
                value, np.array([-1]).ctypes, 0, np.int32(root))
            bcast(data._null_bitmap, root)
            return
        return bcast_decimal_arr
    if isinstance(data, (IntegerArrayType, FloatingArrayType)) or data in (
        boolean_array, datetime_date_array_type):

        def bcast_impl_int_arr(data, root=MPI_ROOT):
            bcast(data._data, root)
            bcast(data._null_bitmap, root)
            return
        return bcast_impl_int_arr
    if isinstance(data, DatetimeArrayType):

        def bcast_impl_tz_arr(data, root=MPI_ROOT):
            bcast(data._data, root)
            return
        return bcast_impl_tz_arr
    if is_str_arr_type(data) or data == binary_array_type:
        tmbs__twhd = np.int32(numba_to_c_type(offset_type))
        mya__ddsoq = np.int32(numba_to_c_type(types.uint8))

        def bcast_str_impl(data, root=MPI_ROOT):
            data = decode_if_dict_array(data)
            emcjo__hsb = len(data)
            srrkp__ixacu = num_total_chars(data)
            assert emcjo__hsb < INT_MAX
            assert srrkp__ixacu < INT_MAX
            moz__fsaw = get_offset_ptr(data)
            pfd__xfwge = get_data_ptr(data)
            null_bitmap_ptr = get_null_bitmap_ptr(data)
            bxl__qrom = emcjo__hsb + 7 >> 3
            c_bcast(moz__fsaw, np.int32(emcjo__hsb + 1), tmbs__twhd, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(pfd__xfwge, np.int32(srrkp__ixacu), mya__ddsoq, np.
                array([-1]).ctypes, 0, np.int32(root))
            c_bcast(null_bitmap_ptr, np.int32(bxl__qrom), mya__ddsoq, np.
                array([-1]).ctypes, 0, np.int32(root))
        return bcast_str_impl


c_bcast = types.ExternalFunction('c_bcast', types.void(types.voidptr, types
    .int32, types.int32, types.voidptr, types.int32, types.int32))


@numba.generated_jit(nopython=True)
def bcast_scalar(val, root=MPI_ROOT):
    val = types.unliteral(val)
    if not (isinstance(val, (types.Integer, types.Float)) or val in [bodo.
        datetime64ns, bodo.timedelta64ns, bodo.string_type, types.none,
        types.bool_]):
        raise BodoError(
            f'bcast_scalar requires an argument of type Integer, Float, datetime64ns, timedelta64ns, string, None, or Bool. Found type {val}'
            )
    if val == types.none:
        return lambda val, root=MPI_ROOT: None
    if val == bodo.string_type:
        mya__ddsoq = np.int32(numba_to_c_type(types.uint8))

        def impl_str(val, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            if rank != root:
                bfcdx__ulg = 0
                kan__fuj = np.empty(0, np.uint8).ctypes
            else:
                kan__fuj, bfcdx__ulg = (bodo.libs.str_ext.
                    unicode_to_utf8_and_len(val))
            bfcdx__ulg = bodo.libs.distributed_api.bcast_scalar(bfcdx__ulg,
                root)
            if rank != root:
                fgl__eolp = np.empty(bfcdx__ulg + 1, np.uint8)
                fgl__eolp[bfcdx__ulg] = 0
                kan__fuj = fgl__eolp.ctypes
            c_bcast(kan__fuj, np.int32(bfcdx__ulg), mya__ddsoq, np.array([-
                1]).ctypes, 0, np.int32(root))
            return bodo.libs.str_arr_ext.decode_utf8(kan__fuj, bfcdx__ulg)
        return impl_str
    typ_val = numba_to_c_type(val)
    vjw__ihym = f"""def bcast_scalar_impl(val, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = val
  c_bcast(send.ctypes, np.int32(1), np.int32({typ_val}), np.array([-1]).ctypes, 0, np.int32(root))
  return send[0]
"""
    dtype = numba.np.numpy_support.as_dtype(val)
    hopjt__xqm = {}
    exec(vjw__ihym, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast, 'dtype':
        dtype}, hopjt__xqm)
    xje__pwn = hopjt__xqm['bcast_scalar_impl']
    return xje__pwn


@numba.generated_jit(nopython=True)
def bcast_tuple(val, root=MPI_ROOT):
    assert isinstance(val, types.BaseTuple
        ), 'Internal Error: Argument to bcast tuple must be of type tuple'
    kzkyz__pet = len(val)
    vjw__ihym = f'def bcast_tuple_impl(val, root={MPI_ROOT}):\n'
    vjw__ihym += '  return ({}{})'.format(','.join(
        'bcast_scalar(val[{}], root)'.format(i) for i in range(kzkyz__pet)),
        ',' if kzkyz__pet else '')
    hopjt__xqm = {}
    exec(vjw__ihym, {'bcast_scalar': bcast_scalar}, hopjt__xqm)
    pca__znfdo = hopjt__xqm['bcast_tuple_impl']
    return pca__znfdo


def prealloc_str_for_bcast(arr, root=MPI_ROOT):
    return arr


@overload(prealloc_str_for_bcast, no_unliteral=True)
def prealloc_str_for_bcast_overload(arr, root=MPI_ROOT):
    if arr == string_array_type:

        def prealloc_impl(arr, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            emcjo__hsb = bcast_scalar(len(arr), root)
            zyzt__vorgt = bcast_scalar(np.int64(num_total_chars(arr)), root)
            if rank != root:
                arr = pre_alloc_string_array(emcjo__hsb, zyzt__vorgt)
            return arr
        return prealloc_impl
    return lambda arr, root=MPI_ROOT: arr


def get_local_slice(idx, arr_start, total_len):
    return idx


@overload(get_local_slice, no_unliteral=True, jit_options={'cache': True,
    'no_cpython_wrapper': True})
def get_local_slice_overload(idx, arr_start, total_len):
    if not idx.has_step:

        def impl(idx, arr_start, total_len):
            slice_index = numba.cpython.unicode._normalize_slice(idx, total_len
                )
            fnyx__nrzv = max(arr_start, slice_index.start) - arr_start
            cnlgx__okt = max(slice_index.stop - arr_start, 0)
            return slice(fnyx__nrzv, cnlgx__okt)
    else:

        def impl(idx, arr_start, total_len):
            slice_index = numba.cpython.unicode._normalize_slice(idx, total_len
                )
            vxkg__tfead = slice_index.start
            vhxqt__flx = slice_index.step
            dhuhl__dhqae = (0 if vhxqt__flx == 1 or vxkg__tfead > arr_start
                 else abs(vhxqt__flx - arr_start % vhxqt__flx) % vhxqt__flx)
            fnyx__nrzv = max(arr_start, slice_index.start
                ) - arr_start + dhuhl__dhqae
            cnlgx__okt = max(slice_index.stop - arr_start, 0)
            return slice(fnyx__nrzv, cnlgx__okt, vhxqt__flx)
    return impl


def slice_getitem(arr, slice_index, arr_start, total_len):
    return arr[slice_index]


@overload(slice_getitem, no_unliteral=True, jit_options={'cache': True})
def slice_getitem_overload(arr, slice_index, arr_start, total_len):

    def getitem_impl(arr, slice_index, arr_start, total_len):
        xvmt__dax = get_local_slice(slice_index, arr_start, total_len)
        return bodo.utils.conversion.ensure_contig_if_np(arr[xvmt__dax])
    return getitem_impl


dummy_use = numba.njit(lambda a: None)


def int_getitem(arr, ind, arr_start, total_len, is_1D):
    return arr[ind]


def transform_str_getitem_output(data, length):
    pass


@overload(transform_str_getitem_output)
def overload_transform_str_getitem_output(data, length):
    if data == bodo.string_type:
        return lambda data, length: bodo.libs.str_arr_ext.decode_utf8(data.
            _data, length)
    if data == types.Array(types.uint8, 1, 'C'):
        return lambda data, length: bodo.libs.binary_arr_ext.init_bytes_type(
            data, length)
    raise BodoError(
        f'Internal Error: Expected String or Uint8 Array, found {data}')


@overload(int_getitem, no_unliteral=True)
def int_getitem_overload(arr, ind, arr_start, total_len, is_1D):
    if is_str_arr_type(arr) or arr == bodo.binary_array_type:
        jggqx__wtba = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND
        mya__ddsoq = np.int32(numba_to_c_type(types.uint8))
        umiul__vjg = arr.dtype

        def str_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            arr = decode_if_dict_array(arr)
            ind = ind % total_len
            root = np.int32(0)
            aps__wbod = np.int32(10)
            tag = np.int32(11)
            rnjp__jsk = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                ind = ind - arr_start
                gjlb__kgen = arr._data
                vqwzk__iunc = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    gjlb__kgen, ind)
                hyydz__szkyc = bodo.libs.array_item_arr_ext.get_offsets_ind(
                    gjlb__kgen, ind + 1)
                length = hyydz__szkyc - vqwzk__iunc
                bwr__ptlc = gjlb__kgen[ind]
                rnjp__jsk[0] = length
                isend(rnjp__jsk, np.int32(1), root, aps__wbod, True)
                isend(bwr__ptlc, np.int32(length), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(umiul__vjg
                , jggqx__wtba, 0, 1)
            vlnd__tdq = 0
            if rank == root:
                vlnd__tdq = recv(np.int64, ANY_SOURCE, aps__wbod)
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    umiul__vjg, jggqx__wtba, vlnd__tdq, 1)
                pfd__xfwge = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
                _recv(pfd__xfwge, np.int32(vlnd__tdq), mya__ddsoq,
                    ANY_SOURCE, tag)
            dummy_use(rnjp__jsk)
            vlnd__tdq = bcast_scalar(vlnd__tdq)
            dummy_use(arr)
            if rank != root:
                val = bodo.libs.str_ext.alloc_empty_bytes_or_string_data(
                    umiul__vjg, jggqx__wtba, vlnd__tdq, 1)
            pfd__xfwge = bodo.libs.str_ext.get_unicode_or_numpy_data(val)
            c_bcast(pfd__xfwge, np.int32(vlnd__tdq), mya__ddsoq, np.array([
                -1]).ctypes, 0, np.int32(root))
            val = transform_str_getitem_output(val, vlnd__tdq)
            return val
        return str_getitem_impl
    if isinstance(arr, bodo.CategoricalArrayType):
        ylbs__rxen = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            arr.dtype)

        def cat_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, ylbs__rxen)
            if arr_start <= ind < arr_start + len(arr):
                scpym__yfihh = (bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(arr))
                data = scpym__yfihh[ind - arr_start]
                send_arr = np.full(1, data, ylbs__rxen)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = ylbs__rxen(-1)
            if rank == root:
                val = recv(ylbs__rxen, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            via__ctr = arr.dtype.categories[max(val, 0)]
            return via__ctr
        return cat_getitem_impl
    if isinstance(arr, bodo.libs.pd_datetime_arr_ext.DatetimeArrayType):
        runs__pzteq = arr.tz

        def tz_aware_getitem_impl(arr, ind, arr_start, total_len, is_1D):
            if ind >= total_len:
                raise IndexError('index out of bounds')
            ind = ind % total_len
            root = np.int32(0)
            tag = np.int32(11)
            send_arr = np.zeros(1, np.int64)
            if arr_start <= ind < arr_start + len(arr):
                data = arr[ind - arr_start].value
                send_arr = np.full(1, data)
                isend(send_arr, np.int32(1), root, tag, True)
            rank = bodo.libs.distributed_api.get_rank()
            val = 0
            if rank == root:
                val = recv(np.int64, ANY_SOURCE, tag)
            dummy_use(send_arr)
            val = bcast_scalar(val)
            return bodo.hiframes.pd_timestamp_ext.convert_val_to_timestamp(val,
                runs__pzteq)
        return tz_aware_getitem_impl
    ljsnz__rcf = arr.dtype

    def getitem_impl(arr, ind, arr_start, total_len, is_1D):
        if ind >= total_len:
            raise IndexError('index out of bounds')
        ind = ind % total_len
        root = np.int32(0)
        tag = np.int32(11)
        send_arr = np.zeros(1, ljsnz__rcf)
        if arr_start <= ind < arr_start + len(arr):
            data = arr[ind - arr_start]
            send_arr = np.full(1, data)
            isend(send_arr, np.int32(1), root, tag, True)
        rank = bodo.libs.distributed_api.get_rank()
        val = np.zeros(1, ljsnz__rcf)[0]
        if rank == root:
            val = recv(ljsnz__rcf, ANY_SOURCE, tag)
        dummy_use(send_arr)
        val = bcast_scalar(val)
        return val
    return getitem_impl


def get_chunk_bounds(A):
    pass


@overload(get_chunk_bounds, jit_options={'cache': True})
def get_chunk_bounds_overload(A):
    if not (isinstance(A, types.Array) and isinstance(A.dtype, types.Integer)):
        raise BodoError(
            'get_chunk_bounds() only supports Numpy int input currently.')

    def impl(A):
        n_pes = get_size()
        vnomn__sgxbh = np.empty(n_pes, np.int64)
        fxyst__cot = np.empty(n_pes, np.int8)
        val = numba.cpython.builtins.get_type_min_value(numba.core.types.int64)
        orl__msq = 1
        if len(A) != 0:
            val = A[-1]
            orl__msq = 0
        allgather(vnomn__sgxbh, np.int64(val))
        allgather(fxyst__cot, orl__msq)
        for i, orl__msq in enumerate(fxyst__cot):
            if orl__msq and i != 0:
                vnomn__sgxbh[i] = vnomn__sgxbh[i - 1]
        return vnomn__sgxbh
    return impl


c_alltoallv = types.ExternalFunction('c_alltoallv', types.void(types.
    voidptr, types.voidptr, types.voidptr, types.voidptr, types.voidptr,
    types.voidptr, types.int32))


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def alltoallv(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    typ_enum = get_type_enum(send_data)
    tdl__lllw = get_type_enum(out_data)
    assert typ_enum == tdl__lllw
    if isinstance(send_data, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType)) or send_data in (boolean_array,
        datetime_date_array_type):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data._data.ctypes,
            out_data._data.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    if isinstance(send_data, bodo.CategoricalArrayType):
        return (lambda send_data, out_data, send_counts, recv_counts,
            send_disp, recv_disp: c_alltoallv(send_data.codes.ctypes,
            out_data.codes.ctypes, send_counts.ctypes, recv_counts.ctypes,
            send_disp.ctypes, recv_disp.ctypes, typ_enum))
    return (lambda send_data, out_data, send_counts, recv_counts, send_disp,
        recv_disp: c_alltoallv(send_data.ctypes, out_data.ctypes,
        send_counts.ctypes, recv_counts.ctypes, send_disp.ctypes, recv_disp
        .ctypes, typ_enum))


def alltoallv_tup(send_data, out_data, send_counts, recv_counts, send_disp,
    recv_disp):
    return


@overload(alltoallv_tup, no_unliteral=True)
def alltoallv_tup_overload(send_data, out_data, send_counts, recv_counts,
    send_disp, recv_disp):
    count = send_data.count
    assert out_data.count == count
    vjw__ihym = (
        'def f(send_data, out_data, send_counts, recv_counts, send_disp, recv_disp):\n'
        )
    for i in range(count):
        vjw__ihym += (
            """  alltoallv(send_data[{}], out_data[{}], send_counts, recv_counts, send_disp, recv_disp)
"""
            .format(i, i))
    vjw__ihym += '  return\n'
    hopjt__xqm = {}
    exec(vjw__ihym, {'alltoallv': alltoallv}, hopjt__xqm)
    mpt__bbx = hopjt__xqm['f']
    return mpt__bbx


@numba.njit
def get_start_count(n):
    rank = bodo.libs.distributed_api.get_rank()
    n_pes = bodo.libs.distributed_api.get_size()
    vxkg__tfead = bodo.libs.distributed_api.get_start(n, n_pes, rank)
    count = bodo.libs.distributed_api.get_node_portion(n, n_pes, rank)
    return vxkg__tfead, count


@numba.njit
def get_start(total_size, pes, rank):
    hcxb__tsmcd = total_size % pes
    mnk__nmd = (total_size - hcxb__tsmcd) // pes
    return rank * mnk__nmd + min(rank, hcxb__tsmcd)


@numba.njit
def get_end(total_size, pes, rank):
    hcxb__tsmcd = total_size % pes
    mnk__nmd = (total_size - hcxb__tsmcd) // pes
    return (rank + 1) * mnk__nmd + min(rank + 1, hcxb__tsmcd)


@numba.njit
def get_node_portion(total_size, pes, rank):
    hcxb__tsmcd = total_size % pes
    mnk__nmd = (total_size - hcxb__tsmcd) // pes
    if rank < hcxb__tsmcd:
        return mnk__nmd + 1
    else:
        return mnk__nmd


@numba.generated_jit(nopython=True)
def dist_cumsum(in_arr, out_arr):
    odt__zmu = in_arr.dtype(0)
    levu__lziud = np.int32(Reduce_Type.Sum.value)

    def cumsum_impl(in_arr, out_arr):
        coeqw__xjzte = odt__zmu
        for eonkc__ejx in np.nditer(in_arr):
            coeqw__xjzte += eonkc__ejx.item()
        ziybw__ltkn = dist_exscan(coeqw__xjzte, levu__lziud)
        for i in range(in_arr.size):
            ziybw__ltkn += in_arr[i]
            out_arr[i] = ziybw__ltkn
        return 0
    return cumsum_impl


@numba.generated_jit(nopython=True)
def dist_cumprod(in_arr, out_arr):
    ieaz__aqyu = in_arr.dtype(1)
    levu__lziud = np.int32(Reduce_Type.Prod.value)

    def cumprod_impl(in_arr, out_arr):
        coeqw__xjzte = ieaz__aqyu
        for eonkc__ejx in np.nditer(in_arr):
            coeqw__xjzte *= eonkc__ejx.item()
        ziybw__ltkn = dist_exscan(coeqw__xjzte, levu__lziud)
        if get_rank() == 0:
            ziybw__ltkn = ieaz__aqyu
        for i in range(in_arr.size):
            ziybw__ltkn *= in_arr[i]
            out_arr[i] = ziybw__ltkn
        return 0
    return cumprod_impl


@numba.generated_jit(nopython=True)
def dist_cummin(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        ieaz__aqyu = np.finfo(in_arr.dtype(1).dtype).max
    else:
        ieaz__aqyu = np.iinfo(in_arr.dtype(1).dtype).max
    levu__lziud = np.int32(Reduce_Type.Min.value)

    def cummin_impl(in_arr, out_arr):
        coeqw__xjzte = ieaz__aqyu
        for eonkc__ejx in np.nditer(in_arr):
            coeqw__xjzte = min(coeqw__xjzte, eonkc__ejx.item())
        ziybw__ltkn = dist_exscan(coeqw__xjzte, levu__lziud)
        if get_rank() == 0:
            ziybw__ltkn = ieaz__aqyu
        for i in range(in_arr.size):
            ziybw__ltkn = min(ziybw__ltkn, in_arr[i])
            out_arr[i] = ziybw__ltkn
        return 0
    return cummin_impl


@numba.generated_jit(nopython=True)
def dist_cummax(in_arr, out_arr):
    if isinstance(in_arr.dtype, types.Float):
        ieaz__aqyu = np.finfo(in_arr.dtype(1).dtype).min
    else:
        ieaz__aqyu = np.iinfo(in_arr.dtype(1).dtype).min
    ieaz__aqyu = in_arr.dtype(1)
    levu__lziud = np.int32(Reduce_Type.Max.value)

    def cummax_impl(in_arr, out_arr):
        coeqw__xjzte = ieaz__aqyu
        for eonkc__ejx in np.nditer(in_arr):
            coeqw__xjzte = max(coeqw__xjzte, eonkc__ejx.item())
        ziybw__ltkn = dist_exscan(coeqw__xjzte, levu__lziud)
        if get_rank() == 0:
            ziybw__ltkn = ieaz__aqyu
        for i in range(in_arr.size):
            ziybw__ltkn = max(ziybw__ltkn, in_arr[i])
            out_arr[i] = ziybw__ltkn
        return 0
    return cummax_impl


_allgather = types.ExternalFunction('allgather', types.void(types.voidptr,
    types.int32, types.voidptr, types.int32))


@numba.njit
def allgather(arr, val):
    mvqxp__oizp = get_type_enum(arr)
    _allgather(arr.ctypes, 1, value_to_ptr(val), mvqxp__oizp)


def dist_return(A):
    return A


def rep_return(A):
    return A


def dist_return_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    xcvgj__tbt = args[0]
    if equiv_set.has_shape(xcvgj__tbt):
        return ArrayAnalysis.AnalyzeResult(shape=xcvgj__tbt, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_distributed_api_dist_return = (
    dist_return_equiv)
ArrayAnalysis._analyze_op_call_bodo_libs_distributed_api_rep_return = (
    dist_return_equiv)


def threaded_return(A):
    return A


@numba.njit
def set_arr_local(arr, ind, val):
    arr[ind] = val


@numba.njit
def local_alloc_size(n, in_arr):
    return n


@infer_global(threaded_return)
@infer_global(dist_return)
@infer_global(rep_return)
class ThreadedRetTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        return signature(args[0], *args)


@numba.njit
def parallel_print(*args):
    print(*args)


@numba.njit
def single_print(*args):
    if bodo.libs.distributed_api.get_rank() == 0:
        print(*args)


def print_if_not_empty(args):
    pass


@overload(print_if_not_empty)
def overload_print_if_not_empty(*args):
    svqax__xusm = '(' + ' or '.join(['False'] + [f'len(args[{i}]) != 0' for
        i, jbq__qwo in enumerate(args) if is_array_typ(jbq__qwo) or
        isinstance(jbq__qwo, bodo.hiframes.pd_dataframe_ext.DataFrameType)]
        ) + ')'
    vjw__ihym = f"""def impl(*args):
    if {svqax__xusm} or bodo.get_rank() == 0:
        print(*args)"""
    hopjt__xqm = {}
    exec(vjw__ihym, globals(), hopjt__xqm)
    impl = hopjt__xqm['impl']
    return impl


_wait = types.ExternalFunction('dist_wait', types.void(mpi_req_numba_type,
    types.bool_))


@numba.generated_jit(nopython=True)
def wait(req, cond=True):
    if isinstance(req, types.BaseTuple):
        count = len(req.types)
        vcooq__fnu = ','.join(f'_wait(req[{i}], cond)' for i in range(count))
        vjw__ihym = 'def f(req, cond=True):\n'
        vjw__ihym += f'  return {vcooq__fnu}\n'
        hopjt__xqm = {}
        exec(vjw__ihym, {'_wait': _wait}, hopjt__xqm)
        impl = hopjt__xqm['f']
        return impl
    if is_overload_none(req):
        return lambda req, cond=True: None
    return lambda req, cond=True: _wait(req, cond)


@register_jitable
def _set_if_in_range(A, val, index, chunk_start):
    if index >= chunk_start and index < chunk_start + len(A):
        A[index - chunk_start] = val


@register_jitable
def _root_rank_select(old_val, new_val):
    if get_rank() == 0:
        return old_val
    return new_val


def get_tuple_prod(t):
    return np.prod(t)


@overload(get_tuple_prod, no_unliteral=True)
def get_tuple_prod_overload(t):
    if t == numba.core.types.containers.Tuple(()):
        return lambda t: 1

    def get_tuple_prod_impl(t):
        hcxb__tsmcd = 1
        for a in t:
            hcxb__tsmcd *= a
        return hcxb__tsmcd
    return get_tuple_prod_impl


sig = types.void(types.voidptr, types.voidptr, types.intp, types.intp,
    types.intp, types.intp, types.int32, types.voidptr)
oneD_reshape_shuffle = types.ExternalFunction('oneD_reshape_shuffle', sig)


@numba.njit(no_cpython_wrapper=True, cache=True)
def dist_oneD_reshape_shuffle(lhs, in_arr, new_dim0_global_len, dest_ranks=None
    ):
    cuih__cqse = np.ascontiguousarray(in_arr)
    cif__ize = get_tuple_prod(cuih__cqse.shape[1:])
    cppep__gbpi = get_tuple_prod(lhs.shape[1:])
    if dest_ranks is not None:
        jnw__fqc = np.array(dest_ranks, dtype=np.int32)
    else:
        jnw__fqc = np.empty(0, dtype=np.int32)
    dtype_size = bodo.io.np_io.get_dtype_size(in_arr.dtype)
    oneD_reshape_shuffle(lhs.ctypes, cuih__cqse.ctypes, new_dim0_global_len,
        len(in_arr), dtype_size * cppep__gbpi, dtype_size * cif__ize, len(
        jnw__fqc), jnw__fqc.ctypes)
    check_and_propagate_cpp_exception()


permutation_int = types.ExternalFunction('permutation_int', types.void(
    types.voidptr, types.intp))


@numba.njit
def dist_permutation_int(lhs, n):
    permutation_int(lhs.ctypes, n)


permutation_array_index = types.ExternalFunction('permutation_array_index',
    types.void(types.voidptr, types.intp, types.intp, types.voidptr, types.
    int64, types.voidptr, types.intp, types.int64))


@numba.njit
def dist_permutation_array_index(lhs, lhs_len, dtype_size, rhs, p, p_len,
    n_samples):
    fgxp__lmb = np.ascontiguousarray(rhs)
    jcy__xtakj = get_tuple_prod(fgxp__lmb.shape[1:])
    vgv__zyi = dtype_size * jcy__xtakj
    permutation_array_index(lhs.ctypes, lhs_len, vgv__zyi, fgxp__lmb.ctypes,
        fgxp__lmb.shape[0], p.ctypes, p_len, n_samples)
    check_and_propagate_cpp_exception()


from bodo.io import fsspec_reader, hdfs_reader
ll.add_symbol('finalize', hdist.finalize)
finalize = types.ExternalFunction('finalize', types.int32())
ll.add_symbol('finalize_fsspec', fsspec_reader.finalize_fsspec)
finalize_fsspec = types.ExternalFunction('finalize_fsspec', types.int32())
ll.add_symbol('disconnect_hdfs', hdfs_reader.disconnect_hdfs)
disconnect_hdfs = types.ExternalFunction('disconnect_hdfs', types.int32())


def _check_for_cpp_errors():
    pass


@overload(_check_for_cpp_errors)
def overload_check_for_cpp_errors():
    return lambda : check_and_propagate_cpp_exception()


@numba.njit
def disconnect_hdfs_njit():
    disconnect_hdfs()


@numba.njit
def call_finalize():
    finalize()
    finalize_fsspec()
    _check_for_cpp_errors()
    disconnect_hdfs()


def flush_stdout():
    if not sys.stdout.closed:
        sys.stdout.flush()


atexit.register(call_finalize)
atexit.register(flush_stdout)


def bcast_comm(data, comm_ranks, nranks, root=MPI_ROOT):
    rank = bodo.libs.distributed_api.get_rank()
    dtype = bodo.typeof(data)
    dtype = _bcast_dtype(dtype, root)
    if rank != MPI_ROOT:
        data = get_value_for_type(dtype)
    return bcast_comm_impl(data, comm_ranks, nranks, root)


@overload(bcast_comm)
def bcast_comm_overload(data, comm_ranks, nranks, root=MPI_ROOT):
    return lambda data, comm_ranks, nranks, root=MPI_ROOT: bcast_comm_impl(data
        , comm_ranks, nranks, root)


@numba.generated_jit(nopython=True)
def bcast_comm_impl(data, comm_ranks, nranks, root=MPI_ROOT):
    bodo.hiframes.pd_dataframe_ext.check_runtime_cols_unsupported(data,
        'bodo.bcast_comm()')
    if isinstance(data, (types.Integer, types.Float)):
        typ_val = numba_to_c_type(data)
        vjw__ihym = (
            f"""def bcast_scalar_impl(data, comm_ranks, nranks, root={MPI_ROOT}):
  send = np.empty(1, dtype)
  send[0] = data
  c_bcast(send.ctypes, np.int32(1), np.int32({{}}), comm_ranks,ctypes, np.int32({{}}), np.int32(root))
  return send[0]
"""
            .format(typ_val, nranks))
        dtype = numba.np.numpy_support.as_dtype(data)
        hopjt__xqm = {}
        exec(vjw__ihym, {'bodo': bodo, 'np': np, 'c_bcast': c_bcast,
            'dtype': dtype}, hopjt__xqm)
        xje__pwn = hopjt__xqm['bcast_scalar_impl']
        return xje__pwn
    if isinstance(data, types.Array):
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: _bcast_np(data,
            comm_ranks, nranks, root)
    if isinstance(data, bodo.hiframes.pd_dataframe_ext.DataFrameType):
        dbyid__mvh = len(data.columns)
        ibro__lbf = ', '.join('g_data_{}'.format(i) for i in range(dbyid__mvh))
        yiogr__bposr = ColNamesMetaType(data.columns)
        vjw__ihym = (
            f'def impl_df(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        for i in range(dbyid__mvh):
            vjw__ihym += (
                """  data_{} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {})
"""
                .format(i, i))
            vjw__ihym += (
                """  g_data_{} = bodo.libs.distributed_api.bcast_comm_impl(data_{}, comm_ranks, nranks, root)
"""
                .format(i, i))
        vjw__ihym += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)\n'
            )
        vjw__ihym += """  g_index = bodo.libs.distributed_api.bcast_comm_impl(index, comm_ranks, nranks, root)
"""
        vjw__ihym += (
            """  return bodo.hiframes.pd_dataframe_ext.init_dataframe(({},), g_index, __col_name_meta_value_bcast_comm)
"""
            .format(ibro__lbf))
        hopjt__xqm = {}
        exec(vjw__ihym, {'bodo': bodo, '__col_name_meta_value_bcast_comm':
            yiogr__bposr}, hopjt__xqm)
        fmdl__jega = hopjt__xqm['impl_df']
        return fmdl__jega
    if isinstance(data, bodo.hiframes.pd_index_ext.RangeIndexType):

        def impl_range_index(data, comm_ranks, nranks, root=MPI_ROOT):
            rank = bodo.libs.distributed_api.get_rank()
            n_pes = bodo.libs.distributed_api.get_size()
            vxkg__tfead = data._start
            irywn__job = data._stop
            vhxqt__flx = data._step
            hecf__iprf = data._name
            hecf__iprf = bcast_scalar(hecf__iprf, root)
            vxkg__tfead = bcast_scalar(vxkg__tfead, root)
            irywn__job = bcast_scalar(irywn__job, root)
            vhxqt__flx = bcast_scalar(vhxqt__flx, root)
            irtz__aki = bodo.libs.array_kernels.calc_nitems(vxkg__tfead,
                irywn__job, vhxqt__flx)
            chunk_start = bodo.libs.distributed_api.get_start(irtz__aki,
                n_pes, rank)
            jki__qln = bodo.libs.distributed_api.get_node_portion(irtz__aki,
                n_pes, rank)
            fnyx__nrzv = vxkg__tfead + vhxqt__flx * chunk_start
            cnlgx__okt = vxkg__tfead + vhxqt__flx * (chunk_start + jki__qln)
            cnlgx__okt = min(cnlgx__okt, irywn__job)
            return bodo.hiframes.pd_index_ext.init_range_index(fnyx__nrzv,
                cnlgx__okt, vhxqt__flx, hecf__iprf)
        return impl_range_index
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):

        def impl_pd_index(data, comm_ranks, nranks, root=MPI_ROOT):
            mgf__cuura = data._data
            hecf__iprf = data._name
            arr = bodo.libs.distributed_api.bcast_comm_impl(mgf__cuura,
                comm_ranks, nranks, root)
            return bodo.utils.conversion.index_from_array(arr, hecf__iprf)
        return impl_pd_index
    if isinstance(data, bodo.hiframes.pd_series_ext.SeriesType):

        def impl_series(data, comm_ranks, nranks, root=MPI_ROOT):
            arr = bodo.hiframes.pd_series_ext.get_series_data(data)
            index = bodo.hiframes.pd_series_ext.get_series_index(data)
            hecf__iprf = bodo.hiframes.pd_series_ext.get_series_name(data)
            pnebi__vmdgp = bodo.libs.distributed_api.bcast_comm_impl(hecf__iprf
                , comm_ranks, nranks, root)
            out_arr = bodo.libs.distributed_api.bcast_comm_impl(arr,
                comm_ranks, nranks, root)
            lrb__dnmcg = bodo.libs.distributed_api.bcast_comm_impl(index,
                comm_ranks, nranks, root)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                lrb__dnmcg, pnebi__vmdgp)
        return impl_series
    if isinstance(data, types.BaseTuple):
        vjw__ihym = (
            f'def impl_tuple(data, comm_ranks, nranks, root={MPI_ROOT}):\n')
        vjw__ihym += '  return ({}{})\n'.format(', '.join(
            'bcast_comm_impl(data[{}], comm_ranks, nranks, root)'.format(i) for
            i in range(len(data))), ',' if len(data) > 0 else '')
        hopjt__xqm = {}
        exec(vjw__ihym, {'bcast_comm_impl': bcast_comm_impl}, hopjt__xqm)
        rqzcf__gnmr = hopjt__xqm['impl_tuple']
        return rqzcf__gnmr
    if data is types.none:
        return lambda data, comm_ranks, nranks, root=MPI_ROOT: None


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _bcast_np(data, comm_ranks, nranks, root=MPI_ROOT):
    typ_val = numba_to_c_type(data.dtype)
    pjak__bzc = data.ndim
    dtype = data.dtype
    if dtype == types.NPDatetime('ns'):
        dtype = np.dtype('datetime64[ns]')
    elif dtype == types.NPTimedelta('ns'):
        dtype = np.dtype('timedelta64[ns]')
    kbiz__rzfap = (0,) * pjak__bzc

    def bcast_arr_impl(data, comm_ranks, nranks, root=MPI_ROOT):
        rank = bodo.libs.distributed_api.get_rank()
        mgf__cuura = np.ascontiguousarray(data)
        pfd__xfwge = data.ctypes
        nrl__udday = kbiz__rzfap
        if rank == root:
            nrl__udday = mgf__cuura.shape
        nrl__udday = bcast_tuple(nrl__udday, root)
        bicnb__tbukk = get_tuple_prod(nrl__udday[1:])
        send_counts = nrl__udday[0] * bicnb__tbukk
        ihmp__nfsqd = np.empty(send_counts, dtype)
        if rank == MPI_ROOT:
            c_bcast(pfd__xfwge, np.int32(send_counts), np.int32(typ_val),
                comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return data
        else:
            c_bcast(ihmp__nfsqd.ctypes, np.int32(send_counts), np.int32(
                typ_val), comm_ranks.ctypes, np.int32(nranks), np.int32(root))
            return ihmp__nfsqd.reshape((-1,) + nrl__udday[1:])
    return bcast_arr_impl


node_ranks = None


def get_host_ranks():
    global node_ranks
    if node_ranks is None:
        hldnx__ywx = MPI.COMM_WORLD
        sppng__bet = MPI.Get_processor_name()
        yio__yyr = hldnx__ywx.allgather(sppng__bet)
        node_ranks = defaultdict(list)
        for i, hvk__qui in enumerate(yio__yyr):
            node_ranks[hvk__qui].append(i)
    return node_ranks


def create_subcomm_mpi4py(comm_ranks):
    hldnx__ywx = MPI.COMM_WORLD
    jtmx__aal = hldnx__ywx.Get_group()
    lxq__fxmtl = jtmx__aal.Incl(comm_ranks)
    hyg__bups = hldnx__ywx.Create_group(lxq__fxmtl)
    return hyg__bups


def get_nodes_first_ranks():
    jozj__ech = get_host_ranks()
    return np.array([qujre__ecyp[0] for qujre__ecyp in jozj__ech.values()],
        dtype='int32')


def get_num_nodes():
    return len(get_host_ranks())
