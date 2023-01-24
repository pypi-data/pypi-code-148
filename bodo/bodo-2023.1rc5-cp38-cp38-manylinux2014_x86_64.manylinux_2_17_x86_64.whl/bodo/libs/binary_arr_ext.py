"""Array implementation for binary (bytes) objects, which are usually immutable.
It is equivalent to string array, except that it stores a 'bytes' object for each
element instead of 'str'.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, overload, overload_attribute, overload_method
import bodo
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, offset_type
from bodo.utils.typing import BodoError, is_list_like_index_type
_bytes_fromhex = types.ExternalFunction('bytes_fromhex', types.int64(types.
    voidptr, types.voidptr, types.uint64))
ll.add_symbol('bytes_to_hex', hstr_ext.bytes_to_hex)
ll.add_symbol('bytes_fromhex', hstr_ext.bytes_fromhex)
bytes_type = types.Bytes(types.uint8, 1, 'C', readonly=True)
ll.add_symbol('setitem_binary_array', hstr_ext.setitem_binary_array)
char_type = types.uint8
setitem_binary_array = types.ExternalFunction('setitem_binary_array', types
    .void(types.CPointer(offset_type), types.CPointer(char_type), types.
    uint64, types.voidptr, types.intp, types.intp))


@overload(len)
def bytes_len_overload(bytes_obj):
    if isinstance(bytes_obj, types.Bytes):
        return lambda bytes_obj: bytes_obj._nitems


@overload(operator.getitem, no_unliteral=True)
def bytes_getitem(byte_obj, ind):
    if not isinstance(byte_obj, types.Bytes):
        return
    if isinstance(ind, types.SliceType):

        def impl(byte_obj, ind):
            arr = cast_bytes_uint8array(byte_obj)
            tdos__ihykl = bodo.utils.conversion.ensure_contig_if_np(arr[ind])
            return cast_uint8array_bytes(tdos__ihykl)
        return impl


class BinaryArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self):
        super(BinaryArrayType, self).__init__(name='BinaryArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return bytes_type

    def copy(self):
        return BinaryArrayType()

    @property
    def iterator_type(self):
        return bodo.utils.typing.BodoArrayIterator(self)


binary_array_type = BinaryArrayType()


@overload(len, no_unliteral=True)
def bin_arr_len_overload(bin_arr):
    if bin_arr == binary_array_type:
        return lambda bin_arr: len(bin_arr._data)


make_attribute_wrapper(types.Bytes, 'nitems', '_nitems')


@overload_attribute(BinaryArrayType, 'size')
def bin_arr_size_overload(bin_arr):
    return lambda bin_arr: len(bin_arr._data)


@overload_attribute(BinaryArrayType, 'shape')
def bin_arr_shape_overload(bin_arr):
    return lambda bin_arr: (len(bin_arr._data),)


@overload_attribute(BinaryArrayType, 'nbytes')
def bin_arr_nbytes_overload(bin_arr):
    return lambda bin_arr: bin_arr._data.nbytes


@overload_attribute(BinaryArrayType, 'ndim')
def overload_bin_arr_ndim(A):
    return lambda A: 1


@overload_attribute(BinaryArrayType, 'dtype')
def overload_bool_arr_dtype(A):
    return lambda A: np.dtype('O')


@numba.njit
def pre_alloc_binary_array(n_bytestrs, n_chars):
    if n_chars is None:
        n_chars = -1
    bin_arr = init_binary_arr(bodo.libs.array_item_arr_ext.
        pre_alloc_array_item_array(np.int64(n_bytestrs), (np.int64(n_chars)
        ,), bodo.libs.str_arr_ext.char_arr_type))
    if n_chars == 0:
        bodo.libs.str_arr_ext.set_all_offsets_to_0(bin_arr)
    return bin_arr


@intrinsic
def init_binary_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, sig, args):
        wdtf__jytlf, = args
        gzrm__evtxn = context.make_helper(builder, binary_array_type)
        gzrm__evtxn.data = wdtf__jytlf
        context.nrt.incref(builder, data_typ, wdtf__jytlf)
        return gzrm__evtxn._getvalue()
    return binary_array_type(data_typ), codegen


@intrinsic
def init_bytes_type(typingctx, data_typ, length_type):
    assert data_typ == types.Array(types.uint8, 1, 'C')
    assert length_type == types.int64

    def codegen(context, builder, sig, args):
        wws__wsu = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        bjja__mnqjj = args[1]
        wjcal__ursl = cgutils.create_struct_proxy(bytes_type)(context, builder)
        wjcal__ursl.meminfo = context.nrt.meminfo_alloc(builder, bjja__mnqjj)
        wjcal__ursl.nitems = bjja__mnqjj
        wjcal__ursl.itemsize = lir.Constant(wjcal__ursl.itemsize.type, 1)
        wjcal__ursl.data = context.nrt.meminfo_data(builder, wjcal__ursl.
            meminfo)
        wjcal__ursl.parent = cgutils.get_null_value(wjcal__ursl.parent.type)
        wjcal__ursl.shape = cgutils.pack_array(builder, [bjja__mnqjj],
            context.get_value_type(types.intp))
        wjcal__ursl.strides = wws__wsu.strides
        cgutils.memcpy(builder, wjcal__ursl.data, wws__wsu.data, bjja__mnqjj)
        return wjcal__ursl._getvalue()
    return bytes_type(data_typ, length_type), codegen


@intrinsic
def cast_bytes_uint8array(typingctx, data_typ):
    assert data_typ == bytes_type

    def codegen(context, builder, sig, args):
        return impl_ret_borrowed(context, builder, sig.return_type, args[0])
    return types.Array(types.uint8, 1, 'C')(data_typ), codegen


@intrinsic
def cast_uint8array_bytes(typingctx, data_typ):
    assert data_typ == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, sig, args):
        return impl_ret_borrowed(context, builder, sig.return_type, args[0])
    return bytes_type(data_typ), codegen


@overload_method(BinaryArrayType, 'copy', no_unliteral=True)
def binary_arr_copy_overload(arr):

    def copy_impl(arr):
        return init_binary_arr(arr._data.copy())
    return copy_impl


@overload_method(types.Bytes, 'hex')
def binary_arr_hex(arr):
    eirmx__aed = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def impl(arr):
        bjja__mnqjj = len(arr) * 2
        output = numba.cpython.unicode._empty_string(eirmx__aed, bjja__mnqjj, 1
            )
        bytes_to_hex(output, arr)
        return output
    return impl


@lower_cast(types.CPointer(types.uint8), types.voidptr)
def cast_uint8_array_to_voidptr(context, builder, fromty, toty, val):
    return val


make_attribute_wrapper(types.Bytes, 'data', '_data')


@overload_method(types.Bytes, '__hash__')
def bytes_hash(arr):

    def impl(arr):
        return numba.cpython.hashing._Py_HashBytes(arr._data, len(arr))
    return impl


@intrinsic
def bytes_to_hex(typingctx, output, arr):

    def codegen(context, builder, sig, args):
        zvtw__lsibc = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        shcjv__bxf = cgutils.create_struct_proxy(sig.args[1])(context,
            builder, value=args[1])
        hcvl__mof = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(64)])
        wbcof__anal = cgutils.get_or_insert_function(builder.module,
            hcvl__mof, name='bytes_to_hex')
        builder.call(wbcof__anal, (zvtw__lsibc.data, shcjv__bxf.data,
            shcjv__bxf.nitems))
    return types.void(output, arr), codegen


@overload(operator.getitem, no_unliteral=True)
def binary_arr_getitem(arr, ind):
    if arr != binary_array_type:
        return
    if isinstance(ind, types.Integer):

        def impl(arr, ind):
            uzi__ohylh = arr._data[ind]
            return init_bytes_type(uzi__ohylh, len(uzi__ohylh))
        return impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind) and (ind.
        dtype == types.bool_ or isinstance(ind.dtype, types.Integer)
        ) or isinstance(ind, types.SliceType):
        return lambda arr, ind: init_binary_arr(arr._data[ind])
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for Binary Array with indexing type {ind} not supported.'
            )


def bytes_fromhex(hex_str):
    pass


@overload(bytes_fromhex)
def overload_bytes_fromhex(hex_str):
    hex_str = types.unliteral(hex_str)
    if hex_str == bodo.string_type:
        eirmx__aed = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(hex_str):
            if not hex_str._is_ascii or hex_str._kind != eirmx__aed:
                raise TypeError(
                    'bytes.fromhex is only supported on ascii strings')
            wdtf__jytlf = np.empty(len(hex_str) // 2, np.uint8)
            bjja__mnqjj = _bytes_fromhex(wdtf__jytlf.ctypes, hex_str._data,
                len(hex_str))
            psm__knh = init_bytes_type(wdtf__jytlf, bjja__mnqjj)
            return psm__knh
        return impl
    raise BodoError(f'bytes.fromhex not supported with argument type {hex_str}'
        )


def binary_list_to_array(binary_list):
    return binary_list


@overload(binary_list_to_array, no_unliteral=True)
def binary_list_to_array_overload(binary_list):
    if isinstance(binary_list, types.List
        ) and binary_list.dtype == bodo.bytes_type:

        def binary_list_impl(binary_list):
            oteez__ppbcc = len(binary_list)
            xmctc__pynfp = pre_alloc_binary_array(oteez__ppbcc, -1)
            for jgc__lhtz in range(oteez__ppbcc):
                uwdcj__ecx = binary_list[jgc__lhtz]
                xmctc__pynfp[jgc__lhtz] = uwdcj__ecx
            return xmctc__pynfp
        return binary_list_impl
    raise BodoError(
        f'Error, binary_list_to_array not supported for type {binary_list}')


@overload(operator.setitem)
def binary_arr_setitem(arr, ind, val):
    from bodo.libs.str_arr_ext import get_data_ptr, get_offset_ptr, getitem_str_offset, num_total_chars, set_string_array_range, str_arr_is_na, str_arr_set_na, str_arr_set_not_na
    if arr != binary_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    calvs__zvc = (
        f'Binary array setitem with index {ind} and value {val} not supported.'
        )
    if isinstance(ind, types.Integer):
        if val != bytes_type:
            raise BodoError(calvs__zvc)
        ciicb__dtxb = numba.njit(lambda a: None)

        def impl(arr, ind, val):
            wdtf__jytlf = arr._data
            snmh__pucfu = cast_bytes_uint8array(val)
            huqlj__bxfy = len(snmh__pucfu)
            stwlg__ply = np.int64(getitem_str_offset(arr, ind))
            snlk__vzc = stwlg__ply + huqlj__bxfy
            bodo.libs.array_item_arr_ext.ensure_data_capacity(wdtf__jytlf,
                stwlg__ply, snlk__vzc)
            setitem_binary_array(get_offset_ptr(arr), get_data_ptr(arr),
                snlk__vzc, snmh__pucfu.ctypes, huqlj__bxfy, ind)
            str_arr_set_not_na(arr, ind)
            ciicb__dtxb(arr)
            ciicb__dtxb(val)
        return impl
    elif isinstance(ind, types.SliceType):
        if val == binary_array_type:

            def impl_slice(arr, ind, val):
                bhww__vnrd = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                vpkqi__hfav = bhww__vnrd.start
                wdtf__jytlf = arr._data
                stwlg__ply = np.int64(getitem_str_offset(arr, vpkqi__hfav))
                snlk__vzc = stwlg__ply + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(wdtf__jytlf,
                    stwlg__ply, snlk__vzc)
                set_string_array_range(arr, val, vpkqi__hfav, stwlg__ply)
                lfp__jqxws = 0
                for jgc__lhtz in range(bhww__vnrd.start, bhww__vnrd.stop,
                    bhww__vnrd.step):
                    if str_arr_is_na(val, lfp__jqxws):
                        str_arr_set_na(arr, jgc__lhtz)
                    else:
                        str_arr_set_not_na(arr, jgc__lhtz)
                    lfp__jqxws += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == bytes_type:

            def impl_slice_list(arr, ind, val):
                jvcm__phw = binary_list_to_array(val)
                arr[ind] = jvcm__phw
            return impl_slice_list
        elif val == bytes_type:

            def impl_slice(arr, ind, val):
                bhww__vnrd = numba.cpython.unicode._normalize_slice(ind,
                    len(arr))
                for jgc__lhtz in range(bhww__vnrd.start, bhww__vnrd.stop,
                    bhww__vnrd.step):
                    arr[jgc__lhtz] = val
            return impl_slice
    raise BodoError(calvs__zvc)


def create_binary_cmp_op_overload(op):

    def overload_binary_cmp(lhs, rhs):
        qqhbw__ewpmb = lhs == binary_array_type
        tgfuz__zsget = rhs == binary_array_type
        kmogj__ktnd = 'lhs' if qqhbw__ewpmb else 'rhs'
        ewxp__issbr = 'def impl(lhs, rhs):\n'
        ewxp__issbr += '  numba.parfors.parfor.init_prange()\n'
        ewxp__issbr += f'  n = len({kmogj__ktnd})\n'
        ewxp__issbr += (
            '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(n)\n')
        ewxp__issbr += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        jci__gom = []
        if qqhbw__ewpmb:
            jci__gom.append('bodo.libs.array_kernels.isna(lhs, i)')
        if tgfuz__zsget:
            jci__gom.append('bodo.libs.array_kernels.isna(rhs, i)')
        ewxp__issbr += f"    if {' or '.join(jci__gom)}:\n"
        ewxp__issbr += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        ewxp__issbr += '      continue\n'
        nnwl__wgkpl = 'lhs[i]' if qqhbw__ewpmb else 'lhs'
        bteig__rlmkr = 'rhs[i]' if tgfuz__zsget else 'rhs'
        ewxp__issbr += f'    out_arr[i] = op({nnwl__wgkpl}, {bteig__rlmkr})\n'
        ewxp__issbr += '  return out_arr\n'
        rvxm__ywn = {}
        exec(ewxp__issbr, {'bodo': bodo, 'numba': numba, 'op': op}, rvxm__ywn)
        return rvxm__ywn['impl']
    return overload_binary_cmp


lower_builtin('getiter', binary_array_type)(numba.np.arrayobj.getiter_array)


def pre_alloc_binary_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


from numba.parfors.array_analysis import ArrayAnalysis
(ArrayAnalysis._analyze_op_call_bodo_libs_binary_arr_ext_pre_alloc_binary_array
    ) = pre_alloc_binary_arr_equiv
