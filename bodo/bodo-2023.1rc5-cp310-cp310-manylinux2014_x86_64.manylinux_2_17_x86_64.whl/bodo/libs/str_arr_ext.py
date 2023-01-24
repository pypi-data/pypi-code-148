"""Array implementation for string objects, which are usually immutable.
The characters are stored in a contiguous data array, and an offsets array marks the
the individual strings. For example:
value:             ['a', 'bc', '', 'abc', None, 'bb']
data:              [a, b, c, a, b, c, b, b]
offsets:           [0, 1, 3, 3, 6, 6, 8]
"""
import glob
import operator
import numba
import numba.core.typing.typeof
import numpy as np
import pandas as pd
import pyarrow as pa
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.unsafe.bytes import memcpy_region
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, type_callable, typeof_impl, unbox
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, np_offset_type, offset_type
from bodo.libs.binary_arr_ext import BinaryArrayType, binary_array_type, pre_alloc_binary_array
from bodo.libs.str_ext import memcmp, string_type, unicode_to_utf8_and_len
from bodo.utils.typing import BodoArrayIterator, BodoError, is_list_like_index_type, is_overload_constant_int, is_overload_none, is_overload_true, is_str_arr_type, parse_dtype, raise_bodo_error
use_pd_string_array = False
use_pd_pyarrow_string_array = True
char_type = types.uint8
char_arr_type = types.Array(char_type, 1, 'C')
offset_arr_type = types.Array(offset_type, 1, 'C')
null_bitmap_arr_type = types.Array(types.uint8, 1, 'C')
data_ctypes_type = types.ArrayCTypes(char_arr_type)
offset_ctypes_type = types.ArrayCTypes(offset_arr_type)


class StringArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self):
        super(StringArrayType, self).__init__(name='StringArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_type

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    def copy(self):
        return StringArrayType()


string_array_type = StringArrayType()


@typeof_impl.register(pd.arrays.StringArray)
def typeof_string_array(val, c):
    return string_array_type


@typeof_impl.register(pd.arrays.ArrowStringArray)
def typeof_pyarrow_string_array(val, c):
    if pa.types.is_dictionary(val._data.combine_chunks().type):
        return bodo.dict_str_arr_type
    return string_array_type


@register_model(BinaryArrayType)
@register_model(StringArrayType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        bfzrg__zvbt = ArrayItemArrayType(char_arr_type)
        cjhb__jvech = [('data', bfzrg__zvbt)]
        models.StructModel.__init__(self, dmm, fe_type, cjhb__jvech)


make_attribute_wrapper(StringArrayType, 'data', '_data')
make_attribute_wrapper(BinaryArrayType, 'data', '_data')
lower_builtin('getiter', string_array_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_str_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType
        ) and data_typ.dtype == types.Array(char_type, 1, 'C')

    def codegen(context, builder, sig, args):
        kmhi__mzcus, = args
        ejjk__iuuie = context.make_helper(builder, string_array_type)
        ejjk__iuuie.data = kmhi__mzcus
        context.nrt.incref(builder, data_typ, kmhi__mzcus)
        return ejjk__iuuie._getvalue()
    return string_array_type(data_typ), codegen


class StringDtype(types.Number):

    def __init__(self):
        super(StringDtype, self).__init__('StringDtype')


string_dtype = StringDtype()
register_model(StringDtype)(models.OpaqueModel)


@box(StringDtype)
def box_string_dtype(typ, val, c):
    onib__emvv = c.context.insert_const_string(c.builder.module, 'pandas')
    hrsk__siu = c.pyapi.import_module_noblock(onib__emvv)
    kzw__unjvk = c.pyapi.call_method(hrsk__siu, 'StringDtype', ())
    c.pyapi.decref(hrsk__siu)
    return kzw__unjvk


@unbox(StringDtype)
def unbox_string_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.StringDtype)(lambda a, b: string_dtype)
type_callable(pd.StringDtype)(lambda c: lambda : string_dtype)
lower_builtin(pd.StringDtype)(lambda c, b, s, a: c.get_dummy_value())


def create_binary_op_overload(op):

    def overload_string_array_binary_op(lhs, rhs):
        jgmwm__jzaho = bodo.libs.dict_arr_ext.get_binary_op_overload(op,
            lhs, rhs)
        if jgmwm__jzaho is not None:
            return jgmwm__jzaho
        if is_str_arr_type(lhs) and is_str_arr_type(rhs):

            def impl_both(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ayeab__hrzt = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(ayeab__hrzt)
                for i in numba.parfors.parfor.internal_prange(ayeab__hrzt):
                    if bodo.libs.array_kernels.isna(lhs, i
                        ) or bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_both
        if is_str_arr_type(lhs) and types.unliteral(rhs) == string_type:

            def impl_left(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ayeab__hrzt = len(lhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(ayeab__hrzt)
                for i in numba.parfors.parfor.internal_prange(ayeab__hrzt):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs[i], rhs)
                    out_arr[i] = val
                return out_arr
            return impl_left
        if types.unliteral(lhs) == string_type and is_str_arr_type(rhs):

            def impl_right(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ayeab__hrzt = len(rhs)
                out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(ayeab__hrzt)
                for i in numba.parfors.parfor.internal_prange(ayeab__hrzt):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(out_arr, i)
                        continue
                    val = op(lhs, rhs[i])
                    out_arr[i] = val
                return out_arr
            return impl_right
        raise_bodo_error(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_string_array_binary_op


def overload_add_operator_string_array(lhs, rhs):
    utn__mwef = is_str_arr_type(lhs) or isinstance(lhs, types.Array
        ) and lhs.dtype == string_type
    uolg__cfmsl = is_str_arr_type(rhs) or isinstance(rhs, types.Array
        ) and rhs.dtype == string_type
    if is_str_arr_type(lhs) and uolg__cfmsl or utn__mwef and is_str_arr_type(
        rhs):

        def impl_both(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j
                    ) or bodo.libs.array_kernels.isna(rhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] + rhs[j]
            return out_arr
        return impl_both
    if is_str_arr_type(lhs) and types.unliteral(rhs) == string_type:

        def impl_left(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] + rhs
            return out_arr
        return impl_left
    if types.unliteral(lhs) == string_type and is_str_arr_type(rhs):

        def impl_right(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(rhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(rhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs + rhs[j]
            return out_arr
        return impl_right


def overload_mul_operator_str_arr(lhs, rhs):
    if is_str_arr_type(lhs) and isinstance(rhs, types.Integer):

        def impl(lhs, rhs):
            numba.parfors.parfor.init_prange()
            l = len(lhs)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
            for j in numba.parfors.parfor.internal_prange(l):
                if bodo.libs.array_kernels.isna(lhs, j):
                    out_arr[j] = ''
                    bodo.libs.array_kernels.setna(out_arr, j)
                else:
                    out_arr[j] = lhs[j] * rhs
            return out_arr
        return impl
    if isinstance(lhs, types.Integer) and is_str_arr_type(rhs):

        def impl(lhs, rhs):
            return rhs * lhs
        return impl


def _get_str_binary_arr_payload(context, builder, arr_value, arr_typ):
    assert arr_typ == string_array_type or arr_typ == binary_array_type
    hpda__rwi = context.make_helper(builder, arr_typ, arr_value)
    bfzrg__zvbt = ArrayItemArrayType(char_arr_type)
    udgc__kxpt = _get_array_item_arr_payload(context, builder, bfzrg__zvbt,
        hpda__rwi.data)
    return udgc__kxpt


@intrinsic
def num_strings(typingctx, str_arr_typ=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        udgc__kxpt = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        return udgc__kxpt.n_arrays
    return types.int64(string_array_type), codegen


def _get_num_total_chars(builder, offsets, num_strings):
    return builder.zext(builder.load(builder.gep(offsets, [num_strings])),
        lir.IntType(64))


@numba.njit
def check_offsets(str_arr):
    offsets = bodo.libs.array_item_arr_ext.get_offsets(str_arr._data)
    n_chars = bodo.libs.str_arr_ext.num_total_chars(str_arr)
    for i in range(bodo.libs.array_item_arr_ext.get_n_arrays(str_arr._data)):
        if offsets[i] > n_chars or offsets[i + 1] - offsets[i] < 0:
            print('wrong offset found', i, offsets[i])
            break


@intrinsic
def num_total_chars(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        udgc__kxpt = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        leq__cokmr = context.make_helper(builder, offset_arr_type,
            udgc__kxpt.offsets).data
        return _get_num_total_chars(builder, leq__cokmr, udgc__kxpt.n_arrays)
    return types.uint64(in_arr_typ), codegen


@intrinsic
def get_offset_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        udgc__kxpt = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        pgar__rmt = context.make_helper(builder, offset_arr_type,
            udgc__kxpt.offsets)
        edvot__yns = context.make_helper(builder, offset_ctypes_type)
        edvot__yns.data = builder.bitcast(pgar__rmt.data, lir.IntType(
            offset_type.bitwidth).as_pointer())
        edvot__yns.meminfo = pgar__rmt.meminfo
        kzw__unjvk = edvot__yns._getvalue()
        return impl_ret_borrowed(context, builder, offset_ctypes_type,
            kzw__unjvk)
    return offset_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        udgc__kxpt = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        kmhi__mzcus = context.make_helper(builder, char_arr_type,
            udgc__kxpt.data)
        edvot__yns = context.make_helper(builder, data_ctypes_type)
        edvot__yns.data = kmhi__mzcus.data
        edvot__yns.meminfo = kmhi__mzcus.meminfo
        kzw__unjvk = edvot__yns._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, kzw__unjvk
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def get_data_ptr_ind(typingctx, in_arr_typ, int_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        zfc__ttveh, ind = args
        udgc__kxpt = _get_str_binary_arr_payload(context, builder,
            zfc__ttveh, sig.args[0])
        kmhi__mzcus = context.make_helper(builder, char_arr_type,
            udgc__kxpt.data)
        edvot__yns = context.make_helper(builder, data_ctypes_type)
        edvot__yns.data = builder.gep(kmhi__mzcus.data, [ind])
        edvot__yns.meminfo = kmhi__mzcus.meminfo
        kzw__unjvk = edvot__yns._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, kzw__unjvk
            )
    return data_ctypes_type(in_arr_typ, types.intp), codegen


@intrinsic
def copy_single_char(typingctx, dst_ptr_t, dst_ind_t, src_ptr_t, src_ind_t=None
    ):

    def codegen(context, builder, sig, args):
        rnx__nnhx, psp__isql, oecp__frn, rln__neia = args
        crw__anan = builder.bitcast(builder.gep(rnx__nnhx, [psp__isql]),
            lir.IntType(8).as_pointer())
        zxihn__vqkds = builder.bitcast(builder.gep(oecp__frn, [rln__neia]),
            lir.IntType(8).as_pointer())
        osbl__cdib = builder.load(zxihn__vqkds)
        builder.store(osbl__cdib, crw__anan)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@intrinsic
def get_null_bitmap_ptr(typingctx, in_arr_typ=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        udgc__kxpt = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        dljnf__wpyp = context.make_helper(builder, null_bitmap_arr_type,
            udgc__kxpt.null_bitmap)
        edvot__yns = context.make_helper(builder, data_ctypes_type)
        edvot__yns.data = dljnf__wpyp.data
        edvot__yns.meminfo = dljnf__wpyp.meminfo
        kzw__unjvk = edvot__yns._getvalue()
        return impl_ret_borrowed(context, builder, data_ctypes_type, kzw__unjvk
            )
    return data_ctypes_type(in_arr_typ), codegen


@intrinsic
def getitem_str_offset(typingctx, in_arr_typ, ind_t=None):
    assert in_arr_typ in [binary_array_type, string_array_type]

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        udgc__kxpt = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        leq__cokmr = context.make_helper(builder, offset_arr_type,
            udgc__kxpt.offsets).data
        return builder.load(builder.gep(leq__cokmr, [ind]))
    return offset_type(in_arr_typ, ind_t), codegen


@intrinsic
def setitem_str_offset(typingctx, str_arr_typ, ind_t, val_t=None):
    assert str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        in_str_arr, ind, val = args
        udgc__kxpt = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, udgc__kxpt.
            offsets).data
        builder.store(val, builder.gep(offsets, [ind]))
        return context.get_dummy_value()
    return types.void(string_array_type, ind_t, offset_type), codegen


@intrinsic
def getitem_str_bitmap(typingctx, in_bitmap_typ, ind_t=None):

    def codegen(context, builder, sig, args):
        oigxa__nzoxw, ind = args
        if in_bitmap_typ == data_ctypes_type:
            edvot__yns = context.make_helper(builder, data_ctypes_type,
                oigxa__nzoxw)
            oigxa__nzoxw = edvot__yns.data
        return builder.load(builder.gep(oigxa__nzoxw, [ind]))
    return char_type(in_bitmap_typ, ind_t), codegen


@intrinsic
def setitem_str_bitmap(typingctx, in_bitmap_typ, ind_t, val_t=None):

    def codegen(context, builder, sig, args):
        oigxa__nzoxw, ind, val = args
        if in_bitmap_typ == data_ctypes_type:
            edvot__yns = context.make_helper(builder, data_ctypes_type,
                oigxa__nzoxw)
            oigxa__nzoxw = edvot__yns.data
        builder.store(val, builder.gep(oigxa__nzoxw, [ind]))
        return context.get_dummy_value()
    return types.void(in_bitmap_typ, ind_t, char_type), codegen


@intrinsic
def copy_str_arr_slice(typingctx, out_str_arr_typ, in_str_arr_typ, ind_t=None):
    assert out_str_arr_typ == string_array_type and in_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr, ind = args
        rki__ojboo = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        bkdy__dxey = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        qoiu__xifd = context.make_helper(builder, offset_arr_type,
            rki__ojboo.offsets).data
        uefu__dzqn = context.make_helper(builder, offset_arr_type,
            bkdy__dxey.offsets).data
        kykrb__ewz = context.make_helper(builder, char_arr_type, rki__ojboo
            .data).data
        zug__klldi = context.make_helper(builder, char_arr_type, bkdy__dxey
            .data).data
        iud__ylpy = context.make_helper(builder, null_bitmap_arr_type,
            rki__ojboo.null_bitmap).data
        qjk__qkia = context.make_helper(builder, null_bitmap_arr_type,
            bkdy__dxey.null_bitmap).data
        dao__verp = builder.add(ind, context.get_constant(types.intp, 1))
        cgutils.memcpy(builder, uefu__dzqn, qoiu__xifd, dao__verp)
        cgutils.memcpy(builder, zug__klldi, kykrb__ewz, builder.load(
            builder.gep(qoiu__xifd, [ind])))
        kzv__ggrui = builder.add(ind, lir.Constant(lir.IntType(64), 7))
        jbp__ofoc = builder.lshr(kzv__ggrui, lir.Constant(lir.IntType(64), 3))
        cgutils.memcpy(builder, qjk__qkia, iud__ylpy, jbp__ofoc)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type, ind_t), codegen


@intrinsic
def copy_data(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        rki__ojboo = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        bkdy__dxey = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        qoiu__xifd = context.make_helper(builder, offset_arr_type,
            rki__ojboo.offsets).data
        kykrb__ewz = context.make_helper(builder, char_arr_type, rki__ojboo
            .data).data
        zug__klldi = context.make_helper(builder, char_arr_type, bkdy__dxey
            .data).data
        num_total_chars = _get_num_total_chars(builder, qoiu__xifd,
            rki__ojboo.n_arrays)
        cgutils.memcpy(builder, zug__klldi, kykrb__ewz, num_total_chars)
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def copy_non_null_offsets(typingctx, str_arr_typ, out_str_arr_typ=None):
    assert str_arr_typ == string_array_type and out_str_arr_typ == string_array_type

    def codegen(context, builder, sig, args):
        out_str_arr, in_str_arr = args
        rki__ojboo = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        bkdy__dxey = _get_str_binary_arr_payload(context, builder,
            out_str_arr, string_array_type)
        qoiu__xifd = context.make_helper(builder, offset_arr_type,
            rki__ojboo.offsets).data
        uefu__dzqn = context.make_helper(builder, offset_arr_type,
            bkdy__dxey.offsets).data
        iud__ylpy = context.make_helper(builder, null_bitmap_arr_type,
            rki__ojboo.null_bitmap).data
        ayeab__hrzt = rki__ojboo.n_arrays
        ged__grtq = context.get_constant(offset_type, 0)
        wdx__djlu = cgutils.alloca_once_value(builder, ged__grtq)
        with cgutils.for_range(builder, ayeab__hrzt) as tfu__pzrjd:
            bnyzj__corr = lower_is_na(context, builder, iud__ylpy,
                tfu__pzrjd.index)
            with cgutils.if_likely(builder, builder.not_(bnyzj__corr)):
                xrh__opja = builder.load(builder.gep(qoiu__xifd, [
                    tfu__pzrjd.index]))
                gdp__luwy = builder.load(wdx__djlu)
                builder.store(xrh__opja, builder.gep(uefu__dzqn, [gdp__luwy]))
                builder.store(builder.add(gdp__luwy, lir.Constant(context.
                    get_value_type(offset_type), 1)), wdx__djlu)
        gdp__luwy = builder.load(wdx__djlu)
        xrh__opja = builder.load(builder.gep(qoiu__xifd, [ayeab__hrzt]))
        builder.store(xrh__opja, builder.gep(uefu__dzqn, [gdp__luwy]))
        return context.get_dummy_value()
    return types.void(string_array_type, string_array_type), codegen


@intrinsic
def str_copy(typingctx, buff_arr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        fob__cjsnl, ind, str, myvnp__iyj = args
        fob__cjsnl = context.make_array(sig.args[0])(context, builder,
            fob__cjsnl)
        ocqk__qiq = builder.gep(fob__cjsnl.data, [ind])
        cgutils.raw_memcpy(builder, ocqk__qiq, str, myvnp__iyj, 1)
        return context.get_dummy_value()
    return types.void(null_bitmap_arr_type, types.intp, types.voidptr,
        types.intp), codegen


@intrinsic
def str_copy_ptr(typingctx, ptr_typ, ind_typ, str_typ, len_typ=None):

    def codegen(context, builder, sig, args):
        ocqk__qiq, ind, rkbp__ngtwv, myvnp__iyj = args
        ocqk__qiq = builder.gep(ocqk__qiq, [ind])
        cgutils.raw_memcpy(builder, ocqk__qiq, rkbp__ngtwv, myvnp__iyj, 1)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.intp, types.voidptr, types.intp
        ), codegen


@numba.generated_jit(nopython=True)
def get_str_arr_item_length(A, i):
    if A == bodo.dict_str_arr_type:

        def impl(A, i):
            idx = A._indices[i]
            baihe__ord = A._data
            return np.int64(getitem_str_offset(baihe__ord, idx + 1) -
                getitem_str_offset(baihe__ord, idx))
        return impl
    else:
        return lambda A, i: np.int64(getitem_str_offset(A, i + 1) -
            getitem_str_offset(A, i))


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_str_length(A, i):
    kzinh__znuid = np.int64(getitem_str_offset(A, i))
    pqo__xfs = np.int64(getitem_str_offset(A, i + 1))
    l = pqo__xfs - kzinh__znuid
    vrnge__hvvn = get_data_ptr_ind(A, kzinh__znuid)
    for j in range(l):
        if bodo.hiframes.split_impl.getitem_c_arr(vrnge__hvvn, j) >= 128:
            return len(A[i])
    return l


@numba.njit(no_cpython_wrapper=True)
def get_str_arr_item_ptr(A, i):
    return get_data_ptr_ind(A, getitem_str_offset(A, i))


@numba.generated_jit(no_cpython_wrapper=True, nopython=True)
def get_str_arr_item_copy(B, j, A, i):
    if B != string_array_type:
        raise BodoError(
            'get_str_arr_item_copy(): Output array must be a string array')
    if not is_str_arr_type(A):
        raise BodoError(
            'get_str_arr_item_copy(): Input array must be a string array or dictionary encoded array'
            )
    if A == bodo.dict_str_arr_type:
        nop__wop = 'in_str_arr = A._data'
        hiay__xin = 'input_index = A._indices[i]'
    else:
        nop__wop = 'in_str_arr = A'
        hiay__xin = 'input_index = i'
    nxjx__grx = f"""def impl(B, j, A, i):
        if j == 0:
            setitem_str_offset(B, 0, 0)

        {nop__wop}
        {hiay__xin}

        # set NA
        if bodo.libs.array_kernels.isna(A, i):
            str_arr_set_na(B, j)
            return
        else:
            str_arr_set_not_na(B, j)

        # get input array offsets
        in_start_offset = getitem_str_offset(in_str_arr, input_index)
        in_end_offset = getitem_str_offset(in_str_arr, input_index + 1)
        val_len = in_end_offset - in_start_offset

        # set output offset
        out_start_offset = getitem_str_offset(B, j)
        out_end_offset = out_start_offset + val_len
        setitem_str_offset(B, j + 1, out_end_offset)

        # copy data
        if val_len != 0:
            # ensure required space in output array
            data_arr = B._data
            bodo.libs.array_item_arr_ext.ensure_data_capacity(
                data_arr, np.int64(out_start_offset), np.int64(out_end_offset)
            )
            out_data_ptr = get_data_ptr(B).data
            in_data_ptr = get_data_ptr(in_str_arr).data
            memcpy_region(
                out_data_ptr,
                out_start_offset,
                in_data_ptr,
                in_start_offset,
                val_len,
                1,
            )"""
    hfwkf__kgdb = {}
    exec(nxjx__grx, {'setitem_str_offset': setitem_str_offset,
        'memcpy_region': memcpy_region, 'getitem_str_offset':
        getitem_str_offset, 'str_arr_set_na': str_arr_set_na,
        'str_arr_set_not_na': str_arr_set_not_na, 'get_data_ptr':
        get_data_ptr, 'bodo': bodo, 'np': np}, hfwkf__kgdb)
    impl = hfwkf__kgdb['impl']
    return impl


@numba.njit(no_cpython_wrapper=True)
def get_str_null_bools(str_arr):
    ayeab__hrzt = len(str_arr)
    fxqqe__biomw = np.empty(ayeab__hrzt, np.bool_)
    for i in range(ayeab__hrzt):
        fxqqe__biomw[i] = bodo.libs.array_kernels.isna(str_arr, i)
    return fxqqe__biomw


def to_list_if_immutable_arr(arr, str_null_bools=None):
    return arr


@overload(to_list_if_immutable_arr, no_unliteral=True)
def to_list_if_immutable_arr_overload(data, str_null_bools=None):
    if is_str_arr_type(data) or data == binary_array_type:

        def to_list_impl(data, str_null_bools=None):
            ayeab__hrzt = len(data)
            l = []
            for i in range(ayeab__hrzt):
                l.append(data[i])
            return l
        return to_list_impl
    if isinstance(data, types.BaseTuple):
        bqhy__xvvk = data.count
        ewi__xnu = ['to_list_if_immutable_arr(data[{}])'.format(i) for i in
            range(bqhy__xvvk)]
        if is_overload_true(str_null_bools):
            ewi__xnu += ['get_str_null_bools(data[{}])'.format(i) for i in
                range(bqhy__xvvk) if is_str_arr_type(data.types[i]) or data
                .types[i] == binary_array_type]
        nxjx__grx = 'def f(data, str_null_bools=None):\n'
        nxjx__grx += '  return ({}{})\n'.format(', '.join(ewi__xnu), ',' if
            bqhy__xvvk == 1 else '')
        hfwkf__kgdb = {}
        exec(nxjx__grx, {'to_list_if_immutable_arr':
            to_list_if_immutable_arr, 'get_str_null_bools':
            get_str_null_bools, 'bodo': bodo}, hfwkf__kgdb)
        sgk__kwi = hfwkf__kgdb['f']
        return sgk__kwi
    return lambda data, str_null_bools=None: data


def cp_str_list_to_array(str_arr, str_list, str_null_bools=None):
    return


@overload(cp_str_list_to_array, no_unliteral=True)
def cp_str_list_to_array_overload(str_arr, list_data, str_null_bools=None):
    if str_arr == string_array_type:
        if is_overload_none(str_null_bools):

            def cp_str_list_impl(str_arr, list_data, str_null_bools=None):
                ayeab__hrzt = len(list_data)
                for i in range(ayeab__hrzt):
                    rkbp__ngtwv = list_data[i]
                    str_arr[i] = rkbp__ngtwv
            return cp_str_list_impl
        else:

            def cp_str_list_impl_null(str_arr, list_data, str_null_bools=None):
                ayeab__hrzt = len(list_data)
                for i in range(ayeab__hrzt):
                    rkbp__ngtwv = list_data[i]
                    str_arr[i] = rkbp__ngtwv
                    if str_null_bools[i]:
                        str_arr_set_na(str_arr, i)
                    else:
                        str_arr_set_not_na(str_arr, i)
            return cp_str_list_impl_null
    if isinstance(str_arr, types.BaseTuple):
        bqhy__xvvk = str_arr.count
        izlwn__wtob = 0
        nxjx__grx = 'def f(str_arr, list_data, str_null_bools=None):\n'
        for i in range(bqhy__xvvk):
            if is_overload_true(str_null_bools) and str_arr.types[i
                ] == string_array_type:
                nxjx__grx += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}], list_data[{}])\n'
                    .format(i, i, bqhy__xvvk + izlwn__wtob))
                izlwn__wtob += 1
            else:
                nxjx__grx += (
                    '  cp_str_list_to_array(str_arr[{}], list_data[{}])\n'.
                    format(i, i))
        nxjx__grx += '  return\n'
        hfwkf__kgdb = {}
        exec(nxjx__grx, {'cp_str_list_to_array': cp_str_list_to_array},
            hfwkf__kgdb)
        xwus__migr = hfwkf__kgdb['f']
        return xwus__migr
    return lambda str_arr, list_data, str_null_bools=None: None


def str_list_to_array(str_list):
    return str_list


@overload(str_list_to_array, no_unliteral=True)
def str_list_to_array_overload(str_list):
    if isinstance(str_list, types.List) and str_list.dtype == bodo.string_type:

        def str_list_impl(str_list):
            ayeab__hrzt = len(str_list)
            str_arr = pre_alloc_string_array(ayeab__hrzt, -1)
            for i in range(ayeab__hrzt):
                rkbp__ngtwv = str_list[i]
                str_arr[i] = rkbp__ngtwv
            return str_arr
        return str_list_impl
    return lambda str_list: str_list


def get_num_total_chars(A):
    pass


@overload(get_num_total_chars)
def overload_get_num_total_chars(A):
    if isinstance(A, types.List) and A.dtype == string_type:

        def str_list_impl(A):
            ayeab__hrzt = len(A)
            ibpn__venxw = 0
            for i in range(ayeab__hrzt):
                rkbp__ngtwv = A[i]
                ibpn__venxw += get_utf8_size(rkbp__ngtwv)
            return ibpn__venxw
        return str_list_impl
    assert A == string_array_type
    return lambda A: num_total_chars(A)


@overload_method(StringArrayType, 'copy', no_unliteral=True)
def str_arr_copy_overload(arr):

    def copy_impl(arr):
        ayeab__hrzt = len(arr)
        n_chars = num_total_chars(arr)
        bfxlb__xnx = pre_alloc_string_array(ayeab__hrzt, np.int64(n_chars))
        copy_str_arr_slice(bfxlb__xnx, arr, ayeab__hrzt)
        return bfxlb__xnx
    return copy_impl


@overload(len, no_unliteral=True)
def str_arr_len_overload(str_arr):
    if str_arr == string_array_type:

        def str_arr_len(str_arr):
            return str_arr.size
        return str_arr_len


@overload_attribute(StringArrayType, 'size')
def str_arr_size_overload(str_arr):
    return lambda str_arr: len(str_arr._data)


@overload_attribute(StringArrayType, 'shape')
def str_arr_shape_overload(str_arr):
    return lambda str_arr: (str_arr.size,)


@overload_attribute(StringArrayType, 'nbytes')
def str_arr_nbytes_overload(str_arr):
    return lambda str_arr: str_arr._data.nbytes


@overload_method(types.Array, 'tolist', no_unliteral=True)
@overload_method(StringArrayType, 'tolist', no_unliteral=True)
def overload_to_list(arr):
    return lambda arr: list(arr)


import llvmlite.binding as ll
from llvmlite import ir as lir
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('get_str_len', hstr_ext.get_str_len)
ll.add_symbol('setitem_string_array', hstr_ext.setitem_string_array)
ll.add_symbol('is_na', hstr_ext.is_na)
ll.add_symbol('string_array_from_sequence', array_ext.
    string_array_from_sequence)
ll.add_symbol('pd_array_from_string_array', hstr_ext.pd_array_from_string_array
    )
ll.add_symbol('np_array_from_string_array', hstr_ext.np_array_from_string_array
    )
ll.add_symbol('pd_pyarrow_array_from_string_array', hstr_ext.
    pd_pyarrow_array_from_string_array)
ll.add_symbol('convert_len_arr_to_offset32', hstr_ext.
    convert_len_arr_to_offset32)
ll.add_symbol('convert_len_arr_to_offset', hstr_ext.convert_len_arr_to_offset)
ll.add_symbol('set_string_array_range', hstr_ext.set_string_array_range)
ll.add_symbol('str_arr_to_int64', hstr_ext.str_arr_to_int64)
ll.add_symbol('str_arr_to_float64', hstr_ext.str_arr_to_float64)
ll.add_symbol('get_utf8_size', hstr_ext.get_utf8_size)
ll.add_symbol('print_str_arr', hstr_ext.print_str_arr)
ll.add_symbol('inplace_int64_to_str', hstr_ext.inplace_int64_to_str)
ll.add_symbol('str_to_dict_str_array', hstr_ext.str_to_dict_str_array)
inplace_int64_to_str = types.ExternalFunction('inplace_int64_to_str', types
    .void(types.voidptr, types.int64, types.int64))
convert_len_arr_to_offset32 = types.ExternalFunction(
    'convert_len_arr_to_offset32', types.void(types.voidptr, types.intp))
convert_len_arr_to_offset = types.ExternalFunction('convert_len_arr_to_offset',
    types.void(types.voidptr, types.voidptr, types.intp))
setitem_string_array = types.ExternalFunction('setitem_string_array', types
    .void(types.CPointer(offset_type), types.CPointer(char_type), types.
    uint64, types.voidptr, types.intp, offset_type, offset_type, types.intp))
_get_utf8_size = types.ExternalFunction('get_utf8_size', types.intp(types.
    voidptr, types.intp, offset_type))
_print_str_arr = types.ExternalFunction('print_str_arr', types.void(types.
    uint64, types.uint64, types.CPointer(offset_type), types.CPointer(
    char_type)))


@numba.generated_jit(nopython=True)
def empty_str_arr(in_seq):
    nxjx__grx = 'def f(in_seq):\n'
    nxjx__grx += '    n_strs = len(in_seq)\n'
    nxjx__grx += '    A = pre_alloc_string_array(n_strs, -1)\n'
    nxjx__grx += '    return A\n'
    hfwkf__kgdb = {}
    exec(nxjx__grx, {'pre_alloc_string_array': pre_alloc_string_array},
        hfwkf__kgdb)
    dte__lfzo = hfwkf__kgdb['f']
    return dte__lfzo


@numba.generated_jit(nopython=True)
def str_arr_from_sequence(in_seq):
    in_seq = types.unliteral(in_seq)
    if in_seq.dtype == bodo.bytes_type:
        jez__htghx = 'pre_alloc_binary_array'
    else:
        jez__htghx = 'pre_alloc_string_array'
    nxjx__grx = 'def f(in_seq):\n'
    nxjx__grx += '    n_strs = len(in_seq)\n'
    nxjx__grx += f'    A = {jez__htghx}(n_strs, -1)\n'
    nxjx__grx += '    for i in range(n_strs):\n'
    nxjx__grx += '        A[i] = in_seq[i]\n'
    nxjx__grx += '    return A\n'
    hfwkf__kgdb = {}
    exec(nxjx__grx, {'pre_alloc_string_array': pre_alloc_string_array,
        'pre_alloc_binary_array': pre_alloc_binary_array}, hfwkf__kgdb)
    dte__lfzo = hfwkf__kgdb['f']
    return dte__lfzo


@intrinsic
def set_all_offsets_to_0(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_all_offsets_to_0 requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        udgc__kxpt = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        evi__lguk = builder.add(udgc__kxpt.n_arrays, lir.Constant(lir.
            IntType(64), 1))
        coyf__zlrzb = builder.lshr(lir.Constant(lir.IntType(64),
            offset_type.bitwidth), lir.Constant(lir.IntType(64), 3))
        jbp__ofoc = builder.mul(evi__lguk, coyf__zlrzb)
        prqt__fuitg = context.make_array(offset_arr_type)(context, builder,
            udgc__kxpt.offsets).data
        cgutils.memset(builder, prqt__fuitg, jbp__ofoc, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@intrinsic
def set_bitmap_all_NA(typingctx, arr_typ=None):
    assert arr_typ in (string_array_type, binary_array_type
        ), 'set_bitmap_all_NA requires a string or binary array'

    def codegen(context, builder, sig, args):
        in_str_arr, = args
        udgc__kxpt = _get_str_binary_arr_payload(context, builder,
            in_str_arr, sig.args[0])
        aiu__tyzdb = udgc__kxpt.n_arrays
        jbp__ofoc = builder.lshr(builder.add(aiu__tyzdb, lir.Constant(lir.
            IntType(64), 7)), lir.Constant(lir.IntType(64), 3))
        reuvg__axs = context.make_array(null_bitmap_arr_type)(context,
            builder, udgc__kxpt.null_bitmap).data
        cgutils.memset(builder, reuvg__axs, jbp__ofoc, 0)
        return context.get_dummy_value()
    return types.none(arr_typ), codegen


@numba.njit
def pre_alloc_string_array(n_strs, n_chars):
    if n_chars is None:
        n_chars = -1
    str_arr = init_str_arr(bodo.libs.array_item_arr_ext.
        pre_alloc_array_item_array(np.int64(n_strs), (np.int64(n_chars),),
        char_arr_type))
    if n_chars == 0:
        set_all_offsets_to_0(str_arr)
    return str_arr


@register_jitable
def gen_na_str_array_lens(n_strs, total_len, len_arr):
    str_arr = pre_alloc_string_array(n_strs, total_len)
    set_bitmap_all_NA(str_arr)
    offsets = bodo.libs.array_item_arr_ext.get_offsets(str_arr._data)
    fhd__bwxq = 0
    if total_len == 0:
        for i in range(len(offsets)):
            offsets[i] = 0
    else:
        lmrs__ueve = len(len_arr)
        for i in range(lmrs__ueve):
            offsets[i] = fhd__bwxq
            fhd__bwxq += len_arr[i]
        offsets[lmrs__ueve] = fhd__bwxq
    return str_arr


kBitmask = np.array([1, 2, 4, 8, 16, 32, 64, 128], dtype=np.uint8)


@numba.njit
def set_bit_to(bits, i, bit_is_set):
    fyyi__bawn = i // 8
    gmx__hao = getitem_str_bitmap(bits, fyyi__bawn)
    gmx__hao ^= np.uint8(-np.uint8(bit_is_set) ^ gmx__hao) & kBitmask[i % 8]
    setitem_str_bitmap(bits, fyyi__bawn, gmx__hao)


@numba.njit
def get_bit_bitmap(bits, i):
    return getitem_str_bitmap(bits, i >> 3) >> (i & 7) & 1


@numba.njit
def copy_nulls_range(out_str_arr, in_str_arr, out_start):
    nean__nbb = get_null_bitmap_ptr(out_str_arr)
    oaql__ksvpu = get_null_bitmap_ptr(in_str_arr)
    for j in range(len(in_str_arr)):
        tisi__bfiph = get_bit_bitmap(oaql__ksvpu, j)
        set_bit_to(nean__nbb, out_start + j, tisi__bfiph)


@intrinsic
def set_string_array_range(typingctx, out_typ, in_typ, curr_str_typ,
    curr_chars_typ=None):
    assert out_typ == string_array_type and in_typ == string_array_type or out_typ == binary_array_type and in_typ == binary_array_type, 'set_string_array_range requires string or binary arrays'
    assert isinstance(curr_str_typ, types.Integer) and isinstance(
        curr_chars_typ, types.Integer
        ), 'set_string_array_range requires integer indices'

    def codegen(context, builder, sig, args):
        out_arr, zfc__ttveh, ctfwu__vuocx, slmq__bwocf = args
        rki__ojboo = _get_str_binary_arr_payload(context, builder,
            zfc__ttveh, string_array_type)
        bkdy__dxey = _get_str_binary_arr_payload(context, builder, out_arr,
            string_array_type)
        qoiu__xifd = context.make_helper(builder, offset_arr_type,
            rki__ojboo.offsets).data
        uefu__dzqn = context.make_helper(builder, offset_arr_type,
            bkdy__dxey.offsets).data
        kykrb__ewz = context.make_helper(builder, char_arr_type, rki__ojboo
            .data).data
        zug__klldi = context.make_helper(builder, char_arr_type, bkdy__dxey
            .data).data
        num_total_chars = _get_num_total_chars(builder, qoiu__xifd,
            rki__ojboo.n_arrays)
        cfwt__pnk = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(64), lir.IntType(64),
            lir.IntType(64)])
        naq__vqf = cgutils.get_or_insert_function(builder.module, cfwt__pnk,
            name='set_string_array_range')
        builder.call(naq__vqf, [uefu__dzqn, zug__klldi, qoiu__xifd,
            kykrb__ewz, ctfwu__vuocx, slmq__bwocf, rki__ojboo.n_arrays,
            num_total_chars])
        tspc__vtpbe = context.typing_context.resolve_value_type(
            copy_nulls_range)
        pkh__uhmlt = tspc__vtpbe.get_call_type(context.typing_context, (
            string_array_type, string_array_type, types.int64), {})
        hepv__msro = context.get_function(tspc__vtpbe, pkh__uhmlt)
        hepv__msro(builder, (out_arr, zfc__ttveh, ctfwu__vuocx))
        return context.get_dummy_value()
    sig = types.void(out_typ, in_typ, types.intp, types.intp)
    return sig, codegen


@box(BinaryArrayType)
@box(StringArrayType)
def box_str_arr(typ, val, c):
    assert typ in [binary_array_type, string_array_type]
    wioq__pen = c.context.make_helper(c.builder, typ, val)
    bfzrg__zvbt = ArrayItemArrayType(char_arr_type)
    udgc__kxpt = _get_array_item_arr_payload(c.context, c.builder,
        bfzrg__zvbt, wioq__pen.data)
    ypwwo__bcbg = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    hal__esl = 'np_array_from_string_array'
    if use_pd_string_array and typ != binary_array_type:
        hal__esl = 'pd_array_from_string_array'
    if use_pd_pyarrow_string_array and typ != binary_array_type:
        from bodo.libs.array import array_info_type, array_to_info_codegen
        vwhnr__renjb = array_to_info_codegen(c.context, c.builder,
            array_info_type(typ), (val,), incref=False)
        cfwt__pnk = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(8).
            as_pointer()])
        hal__esl = 'pd_pyarrow_array_from_string_array'
        orgf__rsqd = cgutils.get_or_insert_function(c.builder.module,
            cfwt__pnk, name=hal__esl)
        arr = c.builder.call(orgf__rsqd, [vwhnr__renjb])
        c.context.nrt.decref(c.builder, typ, val)
        return arr
    cfwt__pnk = lir.FunctionType(c.context.get_argument_type(types.pyobject
        ), [lir.IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
        lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
        IntType(32)])
    orgf__rsqd = cgutils.get_or_insert_function(c.builder.module, cfwt__pnk,
        name=hal__esl)
    leq__cokmr = c.context.make_array(offset_arr_type)(c.context, c.builder,
        udgc__kxpt.offsets).data
    vrnge__hvvn = c.context.make_array(char_arr_type)(c.context, c.builder,
        udgc__kxpt.data).data
    reuvg__axs = c.context.make_array(null_bitmap_arr_type)(c.context, c.
        builder, udgc__kxpt.null_bitmap).data
    arr = c.builder.call(orgf__rsqd, [udgc__kxpt.n_arrays, leq__cokmr,
        vrnge__hvvn, reuvg__axs, ypwwo__bcbg])
    c.context.nrt.decref(c.builder, typ, val)
    return arr


@intrinsic
def str_arr_is_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in (string_array_type, binary_array_type
        ), 'str_arr_is_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        udgc__kxpt = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        reuvg__axs = context.make_array(null_bitmap_arr_type)(context,
            builder, udgc__kxpt.null_bitmap).data
        nfr__pkv = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        rqmy__kphlx = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        gmx__hao = builder.load(builder.gep(reuvg__axs, [nfr__pkv],
            inbounds=True))
        irev__ips = lir.ArrayType(lir.IntType(8), 8)
        zbbz__trslo = cgutils.alloca_once_value(builder, lir.Constant(
            irev__ips, (1, 2, 4, 8, 16, 32, 64, 128)))
        vkt__jjdwd = builder.load(builder.gep(zbbz__trslo, [lir.Constant(
            lir.IntType(64), 0), rqmy__kphlx], inbounds=True))
        return builder.icmp_unsigned('==', builder.and_(gmx__hao,
            vkt__jjdwd), lir.Constant(lir.IntType(8), 0))
    return types.bool_(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in [string_array_type, binary_array_type
        ], 'str_arr_set_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        udgc__kxpt = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        nfr__pkv = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        rqmy__kphlx = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        reuvg__axs = context.make_array(null_bitmap_arr_type)(context,
            builder, udgc__kxpt.null_bitmap).data
        offsets = context.make_helper(builder, offset_arr_type, udgc__kxpt.
            offsets).data
        fmyp__casy = builder.gep(reuvg__axs, [nfr__pkv], inbounds=True)
        gmx__hao = builder.load(fmyp__casy)
        irev__ips = lir.ArrayType(lir.IntType(8), 8)
        zbbz__trslo = cgutils.alloca_once_value(builder, lir.Constant(
            irev__ips, (1, 2, 4, 8, 16, 32, 64, 128)))
        vkt__jjdwd = builder.load(builder.gep(zbbz__trslo, [lir.Constant(
            lir.IntType(64), 0), rqmy__kphlx], inbounds=True))
        vkt__jjdwd = builder.xor(vkt__jjdwd, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(gmx__hao, vkt__jjdwd), fmyp__casy)
        vrukw__nch = builder.add(ind, lir.Constant(lir.IntType(64), 1))
        ndmw__enqf = builder.icmp_unsigned('!=', vrukw__nch, udgc__kxpt.
            n_arrays)
        with builder.if_then(ndmw__enqf):
            builder.store(builder.load(builder.gep(offsets, [ind])),
                builder.gep(offsets, [vrukw__nch]))
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def str_arr_set_not_na(typingctx, str_arr_typ, ind_typ=None):
    assert str_arr_typ in [binary_array_type, string_array_type
        ], 'str_arr_set_not_na: string/binary array expected'

    def codegen(context, builder, sig, args):
        in_str_arr, ind = args
        udgc__kxpt = _get_str_binary_arr_payload(context, builder,
            in_str_arr, str_arr_typ)
        nfr__pkv = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
        rqmy__kphlx = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
        reuvg__axs = context.make_array(null_bitmap_arr_type)(context,
            builder, udgc__kxpt.null_bitmap).data
        fmyp__casy = builder.gep(reuvg__axs, [nfr__pkv], inbounds=True)
        gmx__hao = builder.load(fmyp__casy)
        irev__ips = lir.ArrayType(lir.IntType(8), 8)
        zbbz__trslo = cgutils.alloca_once_value(builder, lir.Constant(
            irev__ips, (1, 2, 4, 8, 16, 32, 64, 128)))
        vkt__jjdwd = builder.load(builder.gep(zbbz__trslo, [lir.Constant(
            lir.IntType(64), 0), rqmy__kphlx], inbounds=True))
        builder.store(builder.or_(gmx__hao, vkt__jjdwd), fmyp__casy)
        return context.get_dummy_value()
    return types.void(str_arr_typ, types.intp), codegen


@intrinsic
def set_null_bits_to_value(typingctx, arr_typ, value_typ=None):
    assert (arr_typ == string_array_type or arr_typ == binary_array_type
        ) and is_overload_constant_int(value_typ)

    def codegen(context, builder, sig, args):
        in_str_arr, value = args
        udgc__kxpt = _get_str_binary_arr_payload(context, builder,
            in_str_arr, string_array_type)
        jbp__ofoc = builder.udiv(builder.add(udgc__kxpt.n_arrays, lir.
            Constant(lir.IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
        reuvg__axs = context.make_array(null_bitmap_arr_type)(context,
            builder, udgc__kxpt.null_bitmap).data
        cgutils.memset(builder, reuvg__axs, jbp__ofoc, value)
        return context.get_dummy_value()
    return types.none(arr_typ, types.int8), codegen


def _get_str_binary_arr_data_payload_ptr(context, builder, str_arr):
    ovgs__amvp = context.make_helper(builder, string_array_type, str_arr)
    bfzrg__zvbt = ArrayItemArrayType(char_arr_type)
    umk__wokvj = context.make_helper(builder, bfzrg__zvbt, ovgs__amvp.data)
    shjzx__jcu = ArrayItemArrayPayloadType(bfzrg__zvbt)
    rwm__eaucg = context.nrt.meminfo_data(builder, umk__wokvj.meminfo)
    bdz__woijf = builder.bitcast(rwm__eaucg, context.get_value_type(
        shjzx__jcu).as_pointer())
    return bdz__woijf


@intrinsic
def move_str_binary_arr_payload(typingctx, to_arr_typ, from_arr_typ=None):
    assert to_arr_typ == string_array_type and from_arr_typ == string_array_type or to_arr_typ == binary_array_type and from_arr_typ == binary_array_type

    def codegen(context, builder, sig, args):
        ftln__vpqt, cnfb__uyvvb = args
        cihy__nuvn = _get_str_binary_arr_data_payload_ptr(context, builder,
            cnfb__uyvvb)
        emum__gxn = _get_str_binary_arr_data_payload_ptr(context, builder,
            ftln__vpqt)
        fqxl__etai = _get_str_binary_arr_payload(context, builder,
            cnfb__uyvvb, sig.args[1])
        cxy__jsvce = _get_str_binary_arr_payload(context, builder,
            ftln__vpqt, sig.args[0])
        context.nrt.incref(builder, char_arr_type, fqxl__etai.data)
        context.nrt.incref(builder, offset_arr_type, fqxl__etai.offsets)
        context.nrt.incref(builder, null_bitmap_arr_type, fqxl__etai.
            null_bitmap)
        context.nrt.decref(builder, char_arr_type, cxy__jsvce.data)
        context.nrt.decref(builder, offset_arr_type, cxy__jsvce.offsets)
        context.nrt.decref(builder, null_bitmap_arr_type, cxy__jsvce.
            null_bitmap)
        builder.store(builder.load(cihy__nuvn), emum__gxn)
        return context.get_dummy_value()
    return types.none(to_arr_typ, from_arr_typ), codegen


dummy_use = numba.njit(lambda a: None)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_utf8_size(s):
    if isinstance(s, types.StringLiteral):
        l = len(s.literal_value.encode())
        return lambda s: l

    def impl(s):
        if s is None:
            return 0
        s = bodo.utils.indexing.unoptional(s)
        if s._is_ascii == 1:
            return len(s)
        ayeab__hrzt = _get_utf8_size(s._data, s._length, s._kind)
        dummy_use(s)
        return ayeab__hrzt
    return impl


@intrinsic
def setitem_str_arr_ptr(typingctx, str_arr_t, ind_t, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        arr, ind, ocqk__qiq, jlz__ayr = args
        udgc__kxpt = _get_str_binary_arr_payload(context, builder, arr, sig
            .args[0])
        offsets = context.make_helper(builder, offset_arr_type, udgc__kxpt.
            offsets).data
        data = context.make_helper(builder, char_arr_type, udgc__kxpt.data
            ).data
        cfwt__pnk = lir.FunctionType(lir.VoidType(), [lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64),
            lir.IntType(32), lir.IntType(32), lir.IntType(64)])
        rqw__ngwxe = cgutils.get_or_insert_function(builder.module,
            cfwt__pnk, name='setitem_string_array')
        bpjct__gmk = context.get_constant(types.int32, -1)
        seodh__gxjen = context.get_constant(types.int32, 1)
        num_total_chars = _get_num_total_chars(builder, offsets, udgc__kxpt
            .n_arrays)
        builder.call(rqw__ngwxe, [offsets, data, num_total_chars, builder.
            extract_value(ocqk__qiq, 0), jlz__ayr, bpjct__gmk, seodh__gxjen,
            ind])
        return context.get_dummy_value()
    return types.void(str_arr_t, ind_t, ptr_t, len_t), codegen


def lower_is_na(context, builder, bull_bitmap, ind):
    cfwt__pnk = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer
        (), lir.IntType(64)])
    mqbev__zipq = cgutils.get_or_insert_function(builder.module, cfwt__pnk,
        name='is_na')
    return builder.call(mqbev__zipq, [bull_bitmap, ind])


@intrinsic
def _memcpy(typingctx, dest_t, src_t, count_t, item_size_t=None):

    def codegen(context, builder, sig, args):
        crw__anan, zxihn__vqkds, bqhy__xvvk, ueiq__pic = args
        cgutils.raw_memcpy(builder, crw__anan, zxihn__vqkds, bqhy__xvvk,
            ueiq__pic)
        return context.get_dummy_value()
    return types.void(types.voidptr, types.voidptr, types.intp, types.intp
        ), codegen


@numba.njit
def print_str_arr(arr):
    _print_str_arr(num_strings(arr), num_total_chars(arr), get_offset_ptr(
        arr), get_data_ptr(arr))


def inplace_eq(A, i, val):
    return A[i] == val


@overload(inplace_eq)
def inplace_eq_overload(A, ind, val):

    def impl(A, ind, val):
        djid__kgui, yyqp__pbi = unicode_to_utf8_and_len(val)
        egdnh__clq = getitem_str_offset(A, ind)
        wwisw__cbw = getitem_str_offset(A, ind + 1)
        icvlo__yotd = wwisw__cbw - egdnh__clq
        if icvlo__yotd != yyqp__pbi:
            return False
        ocqk__qiq = get_data_ptr_ind(A, egdnh__clq)
        return memcmp(ocqk__qiq, djid__kgui, yyqp__pbi) == 0
    return impl


def str_arr_setitem_int_to_str(A, ind, value):
    A[ind] = str(value)


@overload(str_arr_setitem_int_to_str)
def overload_str_arr_setitem_int_to_str(A, ind, val):

    def impl(A, ind, val):
        egdnh__clq = getitem_str_offset(A, ind)
        icvlo__yotd = bodo.libs.str_ext.int_to_str_len(val)
        myy__drx = egdnh__clq + icvlo__yotd
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            egdnh__clq, myy__drx)
        ocqk__qiq = get_data_ptr_ind(A, egdnh__clq)
        inplace_int64_to_str(ocqk__qiq, icvlo__yotd, val)
        setitem_str_offset(A, ind + 1, egdnh__clq + icvlo__yotd)
        str_arr_set_not_na(A, ind)
    return impl


@intrinsic
def inplace_set_NA_str(typingctx, ptr_typ=None):

    def codegen(context, builder, sig, args):
        ocqk__qiq, = args
        bko__hklep = context.insert_const_string(builder.module, '<NA>')
        jqkq__zahz = lir.Constant(lir.IntType(64), len('<NA>'))
        cgutils.raw_memcpy(builder, ocqk__qiq, bko__hklep, jqkq__zahz, 1)
    return types.none(types.voidptr), codegen


def str_arr_setitem_NA_str(A, ind):
    A[ind] = '<NA>'


@overload(str_arr_setitem_NA_str)
def overload_str_arr_setitem_NA_str(A, ind):
    djv__jfj = len('<NA>')

    def impl(A, ind):
        egdnh__clq = getitem_str_offset(A, ind)
        myy__drx = egdnh__clq + djv__jfj
        bodo.libs.array_item_arr_ext.ensure_data_capacity(A._data,
            egdnh__clq, myy__drx)
        ocqk__qiq = get_data_ptr_ind(A, egdnh__clq)
        inplace_set_NA_str(ocqk__qiq)
        setitem_str_offset(A, ind + 1, egdnh__clq + djv__jfj)
        str_arr_set_not_na(A, ind)
    return impl


@overload(operator.getitem, no_unliteral=True)
def str_arr_getitem_int(A, ind):
    if A != string_array_type:
        return
    if isinstance(ind, types.Integer):

        def str_arr_getitem_impl(A, ind):
            if ind < 0:
                ind += A.size
            egdnh__clq = getitem_str_offset(A, ind)
            wwisw__cbw = getitem_str_offset(A, ind + 1)
            jlz__ayr = wwisw__cbw - egdnh__clq
            ocqk__qiq = get_data_ptr_ind(A, egdnh__clq)
            cuue__cqeu = decode_utf8(ocqk__qiq, jlz__ayr)
            return cuue__cqeu
        return str_arr_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def bool_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            ayeab__hrzt = len(A)
            n_strs = 0
            n_chars = 0
            for i in range(ayeab__hrzt):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    n_strs += 1
                    n_chars += get_str_arr_item_length(A, i)
            out_arr = pre_alloc_string_array(n_strs, n_chars)
            vkvma__qszi = get_data_ptr(out_arr).data
            ywej__oki = get_data_ptr(A).data
            izlwn__wtob = 0
            gdp__luwy = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(ayeab__hrzt):
                if not bodo.libs.array_kernels.isna(ind, i) and ind[i]:
                    prq__qpnk = get_str_arr_item_length(A, i)
                    if prq__qpnk == 0:
                        pass
                    elif prq__qpnk == 1:
                        copy_single_char(vkvma__qszi, gdp__luwy, ywej__oki,
                            getitem_str_offset(A, i))
                    else:
                        memcpy_region(vkvma__qszi, gdp__luwy, ywej__oki,
                            getitem_str_offset(A, i), prq__qpnk, 1)
                    gdp__luwy += prq__qpnk
                    setitem_str_offset(out_arr, izlwn__wtob + 1, gdp__luwy)
                    if str_arr_is_na(A, i):
                        str_arr_set_na(out_arr, izlwn__wtob)
                    else:
                        str_arr_set_not_na(out_arr, izlwn__wtob)
                    izlwn__wtob += 1
            return out_arr
        return bool_impl
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def str_arr_arr_impl(A, ind):
            ind = bodo.utils.conversion.coerce_to_array(ind)
            ayeab__hrzt = len(ind)
            n_chars = 0
            for i in range(ayeab__hrzt):
                n_chars += get_str_arr_item_length(A, ind[i])
            out_arr = pre_alloc_string_array(ayeab__hrzt, n_chars)
            vkvma__qszi = get_data_ptr(out_arr).data
            ywej__oki = get_data_ptr(A).data
            gdp__luwy = 0
            setitem_str_offset(out_arr, 0, 0)
            for i in range(ayeab__hrzt):
                if bodo.libs.array_kernels.isna(ind, i):
                    raise ValueError(
                        'Cannot index with an integer indexer containing NA values'
                        )
                gpkj__boaaf = ind[i]
                prq__qpnk = get_str_arr_item_length(A, gpkj__boaaf)
                if prq__qpnk == 0:
                    pass
                elif prq__qpnk == 1:
                    copy_single_char(vkvma__qszi, gdp__luwy, ywej__oki,
                        getitem_str_offset(A, gpkj__boaaf))
                else:
                    memcpy_region(vkvma__qszi, gdp__luwy, ywej__oki,
                        getitem_str_offset(A, gpkj__boaaf), prq__qpnk, 1)
                gdp__luwy += prq__qpnk
                setitem_str_offset(out_arr, i + 1, gdp__luwy)
                if str_arr_is_na(A, gpkj__boaaf):
                    str_arr_set_na(out_arr, i)
                else:
                    str_arr_set_not_na(out_arr, i)
            return out_arr
        return str_arr_arr_impl
    if isinstance(ind, types.SliceType):

        def str_arr_slice_impl(A, ind):
            ayeab__hrzt = len(A)
            bywr__ctmyo = numba.cpython.unicode._normalize_slice(ind,
                ayeab__hrzt)
            disrj__lpeqw = numba.cpython.unicode._slice_span(bywr__ctmyo)
            if bywr__ctmyo.step == 1:
                egdnh__clq = getitem_str_offset(A, bywr__ctmyo.start)
                wwisw__cbw = getitem_str_offset(A, bywr__ctmyo.stop)
                n_chars = wwisw__cbw - egdnh__clq
                bfxlb__xnx = pre_alloc_string_array(disrj__lpeqw, np.int64(
                    n_chars))
                for i in range(disrj__lpeqw):
                    bfxlb__xnx[i] = A[bywr__ctmyo.start + i]
                    if str_arr_is_na(A, bywr__ctmyo.start + i):
                        str_arr_set_na(bfxlb__xnx, i)
                return bfxlb__xnx
            else:
                bfxlb__xnx = pre_alloc_string_array(disrj__lpeqw, -1)
                for i in range(disrj__lpeqw):
                    bfxlb__xnx[i] = A[bywr__ctmyo.start + i * bywr__ctmyo.step]
                    if str_arr_is_na(A, bywr__ctmyo.start + i * bywr__ctmyo
                        .step):
                        str_arr_set_na(bfxlb__xnx, i)
                return bfxlb__xnx
        return str_arr_slice_impl
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for StringArray with indexing type {ind} not supported.')


dummy_use = numba.njit(lambda a: None)


@overload(operator.setitem)
def str_arr_setitem(A, idx, val):
    if A != string_array_type:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    xyms__znxx = (
        f'StringArray setitem with index {idx} and value {val} not supported yet.'
        )
    if isinstance(idx, types.Integer):
        if val != string_type:
            raise BodoError(xyms__znxx)
        fzbze__cpl = 4

        def impl_scalar(A, idx, val):
            hbgnw__cvrir = (val._length if val._is_ascii else fzbze__cpl *
                val._length)
            kmhi__mzcus = A._data
            egdnh__clq = np.int64(getitem_str_offset(A, idx))
            myy__drx = egdnh__clq + hbgnw__cvrir
            bodo.libs.array_item_arr_ext.ensure_data_capacity(kmhi__mzcus,
                egdnh__clq, myy__drx)
            setitem_string_array(get_offset_ptr(A), get_data_ptr(A),
                myy__drx, val._data, val._length, val._kind, val._is_ascii, idx
                )
            str_arr_set_not_na(A, idx)
            dummy_use(A)
            dummy_use(val)
        return impl_scalar
    if isinstance(idx, types.SliceType):
        if val == string_array_type:

            def impl_slice(A, idx, val):
                bywr__ctmyo = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                kzinh__znuid = bywr__ctmyo.start
                kmhi__mzcus = A._data
                egdnh__clq = np.int64(getitem_str_offset(A, kzinh__znuid))
                myy__drx = egdnh__clq + np.int64(num_total_chars(val))
                bodo.libs.array_item_arr_ext.ensure_data_capacity(kmhi__mzcus,
                    egdnh__clq, myy__drx)
                set_string_array_range(A, val, kzinh__znuid, egdnh__clq)
                dol__lnrvw = 0
                for i in range(bywr__ctmyo.start, bywr__ctmyo.stop,
                    bywr__ctmyo.step):
                    if str_arr_is_na(val, dol__lnrvw):
                        str_arr_set_na(A, i)
                    else:
                        str_arr_set_not_na(A, i)
                    dol__lnrvw += 1
            return impl_slice
        elif isinstance(val, types.List) and val.dtype == string_type:

            def impl_slice_list(A, idx, val):
                suyi__xnk = str_list_to_array(val)
                A[idx] = suyi__xnk
            return impl_slice_list
        elif val == string_type:

            def impl_slice(A, idx, val):
                bywr__ctmyo = numba.cpython.unicode._normalize_slice(idx,
                    len(A))
                for i in range(bywr__ctmyo.start, bywr__ctmyo.stop,
                    bywr__ctmyo.step):
                    A[i] = val
            return impl_slice
        else:
            raise BodoError(xyms__znxx)
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        if val == string_type:

            def impl_bool_scalar(A, idx, val):
                ayeab__hrzt = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx)
                out_arr = pre_alloc_string_array(ayeab__hrzt, -1)
                for i in numba.parfors.parfor.internal_prange(ayeab__hrzt):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        out_arr[i] = val
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_scalar
        elif val == string_array_type or isinstance(val, types.Array
            ) and isinstance(val.dtype, types.UnicodeCharSeq):

            def impl_bool_arr(A, idx, val):
                ayeab__hrzt = len(A)
                idx = bodo.utils.conversion.coerce_to_array(idx,
                    use_nullable_array=True)
                out_arr = pre_alloc_string_array(ayeab__hrzt, -1)
                znhx__dwxt = 0
                for i in numba.parfors.parfor.internal_prange(ayeab__hrzt):
                    if not bodo.libs.array_kernels.isna(idx, i) and idx[i]:
                        if bodo.libs.array_kernels.isna(val, znhx__dwxt):
                            out_arr[i] = ''
                            str_arr_set_na(out_arr, znhx__dwxt)
                        else:
                            out_arr[i] = str(val[znhx__dwxt])
                        znhx__dwxt += 1
                    elif bodo.libs.array_kernels.isna(A, i):
                        out_arr[i] = ''
                        str_arr_set_na(out_arr, i)
                    else:
                        get_str_arr_item_copy(out_arr, i, A, i)
                move_str_binary_arr_payload(A, out_arr)
            return impl_bool_arr
        else:
            raise BodoError(xyms__znxx)
    raise BodoError(xyms__znxx)


@overload_attribute(StringArrayType, 'dtype')
def overload_str_arr_dtype(A):
    return lambda A: pd.StringDtype()


@overload_attribute(StringArrayType, 'ndim')
def overload_str_arr_ndim(A):
    return lambda A: 1


@overload_method(StringArrayType, 'astype', no_unliteral=True)
def overload_str_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "StringArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.Function) and dtype.key[0] == str:
        return lambda A, dtype, copy=True: A
    jxk__jkmz = parse_dtype(dtype, 'StringArray.astype')
    if A == jxk__jkmz:
        return lambda A, dtype, copy=True: A
    if not isinstance(jxk__jkmz, (types.Float, types.Integer)
        ) and jxk__jkmz not in (types.bool_, bodo.libs.bool_arr_ext.
        boolean_dtype, bodo.dict_str_arr_type):
        raise BodoError('invalid dtype in StringArray.astype()')
    if isinstance(jxk__jkmz, types.Float):

        def impl_float(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            ayeab__hrzt = len(A)
            B = np.empty(ayeab__hrzt, jxk__jkmz)
            for i in numba.parfors.parfor.internal_prange(ayeab__hrzt):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = np.nan
                else:
                    B[i] = float(A[i])
            return B
        return impl_float
    elif jxk__jkmz == types.bool_:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            ayeab__hrzt = len(A)
            B = np.empty(ayeab__hrzt, jxk__jkmz)
            for i in numba.parfors.parfor.internal_prange(ayeab__hrzt):
                if bodo.libs.array_kernels.isna(A, i):
                    B[i] = False
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif jxk__jkmz == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            ayeab__hrzt = len(A)
            B = np.empty(ayeab__hrzt, jxk__jkmz)
            for i in numba.parfors.parfor.internal_prange(ayeab__hrzt):
                if bodo.libs.array_kernels.isna(A, i):
                    bodo.libs.array_kernels.setna(B, i)
                else:
                    B[i] = bool(A[i])
            return B
        return impl_bool
    elif jxk__jkmz == bodo.dict_str_arr_type:

        def impl_dict_str(A, dtype, copy=True):
            return str_arr_to_dict_str_arr(A)
        return impl_dict_str
    else:

        def impl_int(A, dtype, copy=True):
            numba.parfors.parfor.init_prange()
            ayeab__hrzt = len(A)
            B = np.empty(ayeab__hrzt, jxk__jkmz)
            for i in numba.parfors.parfor.internal_prange(ayeab__hrzt):
                B[i] = int(A[i])
            return B
        return impl_int


@numba.jit
def str_arr_to_dict_str_arr(A):
    return str_arr_to_dict_str_arr_cpp(A)


@intrinsic
def str_arr_to_dict_str_arr_cpp(typingctx, str_arr_t):

    def codegen(context, builder, sig, args):
        str_arr, = args
        ntnyx__ofj = bodo.libs.array.array_to_info_codegen(context, builder,
            bodo.libs.array.array_info_type(sig.args[0]), (str_arr,), False)
        cfwt__pnk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        pfcx__irzz = cgutils.get_or_insert_function(builder.module,
            cfwt__pnk, name='str_to_dict_str_array')
        unn__eeltc = builder.call(pfcx__irzz, [ntnyx__ofj])
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        baihe__ord = bodo.libs.array.info_to_array_codegen(context, builder,
            sig.return_type(bodo.libs.array.array_info_type, sig.
            return_type), (unn__eeltc, context.get_constant_null(sig.
            return_type)))
        return baihe__ord
    assert str_arr_t == bodo.string_array_type, 'str_arr_to_dict_str_arr: Input Array is not a Bodo String Array'
    sig = bodo.dict_str_arr_type(bodo.string_array_type)
    return sig, codegen


@intrinsic
def decode_utf8(typingctx, ptr_t, len_t=None):

    def codegen(context, builder, sig, args):
        ocqk__qiq, jlz__ayr = args
        yef__fpbm = context.get_python_api(builder)
        rufxn__rpao = yef__fpbm.string_from_string_and_size(ocqk__qiq, jlz__ayr
            )
        sdu__xat = yef__fpbm.to_native_value(string_type, rufxn__rpao).value
        aqk__fbrp = cgutils.create_struct_proxy(string_type)(context,
            builder, sdu__xat)
        aqk__fbrp.hash = aqk__fbrp.hash.type(-1)
        yef__fpbm.decref(rufxn__rpao)
        return aqk__fbrp._getvalue()
    return string_type(types.voidptr, types.intp), codegen


def get_arr_data_ptr(arr, ind):
    return arr


@overload(get_arr_data_ptr, no_unliteral=True)
def overload_get_arr_data_ptr(arr, ind):
    assert isinstance(types.unliteral(ind), types.Integer)
    if isinstance(arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(arr, ind):
            return bodo.hiframes.split_impl.get_c_arr_ptr(arr._data.ctypes, ind
                )
        return impl_int
    assert isinstance(arr, types.Array)

    def impl_np(arr, ind):
        return bodo.hiframes.split_impl.get_c_arr_ptr(arr.ctypes, ind)
    return impl_np


def set_to_numeric_out_na_err(out_arr, out_ind, err_code):
    pass


@overload(set_to_numeric_out_na_err)
def set_to_numeric_out_na_err_overload(out_arr, out_ind, err_code):
    if isinstance(out_arr, bodo.libs.int_arr_ext.IntegerArrayType):

        def impl_int(out_arr, out_ind, err_code):
            bodo.libs.int_arr_ext.set_bit_to_arr(out_arr._null_bitmap,
                out_ind, 0 if err_code == -1 else 1)
        return impl_int
    assert isinstance(out_arr, types.Array)
    if isinstance(out_arr.dtype, types.Float):

        def impl_np(out_arr, out_ind, err_code):
            if err_code == -1:
                out_arr[out_ind] = np.nan
        return impl_np
    return lambda out_arr, out_ind, err_code: None


@numba.njit(no_cpython_wrapper=True)
def str_arr_item_to_numeric(out_arr, out_ind, str_arr, ind):
    err_code = _str_arr_item_to_numeric(get_arr_data_ptr(out_arr, out_ind),
        str_arr, ind, out_arr.dtype)
    set_to_numeric_out_na_err(out_arr, out_ind, err_code)


@intrinsic
def _str_arr_item_to_numeric(typingctx, out_ptr_t, str_arr_t, ind_t,
    out_dtype_t=None):
    assert str_arr_t == string_array_type, '_str_arr_item_to_numeric: str arr expected'
    assert ind_t == types.int64, '_str_arr_item_to_numeric: integer index expected'

    def codegen(context, builder, sig, args):
        nhl__kqhp, arr, ind, cmq__ouw = args
        udgc__kxpt = _get_str_binary_arr_payload(context, builder, arr,
            string_array_type)
        offsets = context.make_helper(builder, offset_arr_type, udgc__kxpt.
            offsets).data
        data = context.make_helper(builder, char_arr_type, udgc__kxpt.data
            ).data
        cfwt__pnk = lir.FunctionType(lir.IntType(32), [nhl__kqhp.type, lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64)])
        vfsw__smv = 'str_arr_to_int64'
        if sig.args[3].dtype == types.float64:
            vfsw__smv = 'str_arr_to_float64'
        else:
            assert sig.args[3].dtype == types.int64
        xzl__yvz = cgutils.get_or_insert_function(builder.module, cfwt__pnk,
            vfsw__smv)
        return builder.call(xzl__yvz, [nhl__kqhp, offsets, data, ind])
    return types.int32(out_ptr_t, string_array_type, types.int64, out_dtype_t
        ), codegen


@unbox(BinaryArrayType)
@unbox(StringArrayType)
def unbox_str_series(typ, val, c):
    ypwwo__bcbg = c.context.get_constant(types.int32, int(typ ==
        binary_array_type))
    cfwt__pnk = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType(
        8).as_pointer(), lir.IntType(32)])
    hzvob__uxlsy = cgutils.get_or_insert_function(c.builder.module,
        cfwt__pnk, name='string_array_from_sequence')
    ddkc__cwsp = c.builder.call(hzvob__uxlsy, [val, ypwwo__bcbg])
    bfzrg__zvbt = ArrayItemArrayType(char_arr_type)
    umk__wokvj = c.context.make_helper(c.builder, bfzrg__zvbt)
    umk__wokvj.meminfo = ddkc__cwsp
    ovgs__amvp = c.context.make_helper(c.builder, typ)
    kmhi__mzcus = umk__wokvj._getvalue()
    ovgs__amvp.data = kmhi__mzcus
    sgobc__ngyvs = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ovgs__amvp._getvalue(), is_error=sgobc__ngyvs)


@lower_constant(BinaryArrayType)
@lower_constant(StringArrayType)
def lower_constant_str_arr(context, builder, typ, pyval):
    ayeab__hrzt = len(pyval)
    gdp__luwy = 0
    rzcnl__bpwc = np.empty(ayeab__hrzt + 1, np_offset_type)
    znalc__tisd = []
    ojwf__jsr = np.empty(ayeab__hrzt + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        rzcnl__bpwc[i] = gdp__luwy
        nnx__qzc = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(ojwf__jsr, i, int(not nnx__qzc))
        if nnx__qzc:
            continue
        fvnmn__emr = list(s.encode()) if isinstance(s, str) else list(s)
        znalc__tisd.extend(fvnmn__emr)
        gdp__luwy += len(fvnmn__emr)
    rzcnl__bpwc[ayeab__hrzt] = gdp__luwy
    qcdb__xomfv = np.array(znalc__tisd, np.uint8)
    isjla__ishsj = context.get_constant(types.int64, ayeab__hrzt)
    lam__kgud = context.get_constant_generic(builder, char_arr_type,
        qcdb__xomfv)
    iape__czz = context.get_constant_generic(builder, offset_arr_type,
        rzcnl__bpwc)
    nxeih__hqwkj = context.get_constant_generic(builder,
        null_bitmap_arr_type, ojwf__jsr)
    udgc__kxpt = lir.Constant.literal_struct([isjla__ishsj, lam__kgud,
        iape__czz, nxeih__hqwkj])
    udgc__kxpt = cgutils.global_constant(builder, '.const.payload', udgc__kxpt
        ).bitcast(cgutils.voidptr_t)
    wofns__gzc = context.get_constant(types.int64, -1)
    six__zzbtg = context.get_constant_null(types.voidptr)
    wdy__ofbp = lir.Constant.literal_struct([wofns__gzc, six__zzbtg,
        six__zzbtg, udgc__kxpt, wofns__gzc])
    wdy__ofbp = cgutils.global_constant(builder, '.const.meminfo', wdy__ofbp
        ).bitcast(cgutils.voidptr_t)
    kmhi__mzcus = lir.Constant.literal_struct([wdy__ofbp])
    ovgs__amvp = lir.Constant.literal_struct([kmhi__mzcus])
    return ovgs__amvp


def pre_alloc_str_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


from numba.parfors.array_analysis import ArrayAnalysis
(ArrayAnalysis._analyze_op_call_bodo_libs_str_arr_ext_pre_alloc_string_array
    ) = pre_alloc_str_arr_equiv


@overload(glob.glob, no_unliteral=True)
def overload_glob_glob(pathname, recursive=False):

    def _glob_glob_impl(pathname, recursive=False):
        with numba.objmode(l='list_str_type'):
            l = glob.glob(pathname, recursive=recursive)
        return l
    return _glob_glob_impl
