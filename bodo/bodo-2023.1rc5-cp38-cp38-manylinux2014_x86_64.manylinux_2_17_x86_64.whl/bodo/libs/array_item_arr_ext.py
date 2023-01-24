"""Array implementation for variable-size array items.
Corresponds to Spark's ArrayType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Variable-size List: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in a contingous data array, while an offsets array marks the
individual arrays. For example:
value:             [[1, 2], [3], None, [5, 4, 6], []]
data:              [1, 2, 3, 5, 4, 6]
offsets:           [0, 2, 3, 3, 6, 6]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, is_iterable_type, is_list_like_index_type
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('array_item_array_from_sequence', array_ext.
    array_item_array_from_sequence)
ll.add_symbol('np_array_from_array_item_array', array_ext.
    np_array_from_array_item_array)
offset_type = types.uint64
np_offset_type = numba.np.numpy_support.as_dtype(offset_type)


class ArrayItemArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        assert bodo.utils.utils.is_array_typ(dtype, False)
        self.dtype = dtype
        super(ArrayItemArrayType, self).__init__(name=
            'ArrayItemArrayType({})'.format(dtype))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return ArrayItemArrayType(self.dtype)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class ArrayItemArrayPayloadType(types.Type):

    def __init__(self, array_type):
        self.array_type = array_type
        super(ArrayItemArrayPayloadType, self).__init__(name=
            'ArrayItemArrayPayloadType({})'.format(array_type))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(ArrayItemArrayPayloadType)
class ArrayItemArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        iltfb__leri = [('n_arrays', types.int64), ('data', fe_type.
            array_type.dtype), ('offsets', types.Array(offset_type, 1, 'C')
            ), ('null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, iltfb__leri)


@register_model(ArrayItemArrayType)
class ArrayItemArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = ArrayItemArrayPayloadType(fe_type)
        iltfb__leri = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, iltfb__leri)


def define_array_item_dtor(context, builder, array_item_type, payload_type):
    kqig__oix = builder.module
    mklc__bmw = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    kzin__izx = cgutils.get_or_insert_function(kqig__oix, mklc__bmw, name=
        '.dtor.array_item.{}'.format(array_item_type.dtype))
    if not kzin__izx.is_declaration:
        return kzin__izx
    kzin__izx.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(kzin__izx.append_basic_block())
    hri__sgflc = kzin__izx.args[0]
    pgzh__ysqr = context.get_value_type(payload_type).as_pointer()
    xwr__krbt = builder.bitcast(hri__sgflc, pgzh__ysqr)
    egj__dph = context.make_helper(builder, payload_type, ref=xwr__krbt)
    context.nrt.decref(builder, array_item_type.dtype, egj__dph.data)
    context.nrt.decref(builder, types.Array(offset_type, 1, 'C'), egj__dph.
        offsets)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'), egj__dph.
        null_bitmap)
    builder.ret_void()
    return kzin__izx


def construct_array_item_array(context, builder, array_item_type, n_arrays,
    n_elems, c=None):
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    klg__rua = context.get_value_type(payload_type)
    xln__zfy = context.get_abi_sizeof(klg__rua)
    uwze__kmld = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    shlfe__dvmd = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, xln__zfy), uwze__kmld)
    abm__apq = context.nrt.meminfo_data(builder, shlfe__dvmd)
    epo__bvyz = builder.bitcast(abm__apq, klg__rua.as_pointer())
    egj__dph = cgutils.create_struct_proxy(payload_type)(context, builder)
    egj__dph.n_arrays = n_arrays
    brz__jwmq = n_elems.type.count
    wrx__rxgl = builder.extract_value(n_elems, 0)
    ksx__pbatm = cgutils.alloca_once_value(builder, wrx__rxgl)
    plxiz__pttda = builder.icmp_signed('==', wrx__rxgl, lir.Constant(
        wrx__rxgl.type, -1))
    with builder.if_then(plxiz__pttda):
        builder.store(n_arrays, ksx__pbatm)
    n_elems = cgutils.pack_array(builder, [builder.load(ksx__pbatm)] + [
        builder.extract_value(n_elems, kwi__tlo) for kwi__tlo in range(1,
        brz__jwmq)])
    egj__dph.data = gen_allocate_array(context, builder, array_item_type.
        dtype, n_elems, c)
    yzi__mgi = builder.add(n_arrays, lir.Constant(lir.IntType(64), 1))
    lbvl__snxkh = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(offset_type, 1, 'C'), [yzi__mgi])
    offsets_ptr = lbvl__snxkh.data
    builder.store(context.get_constant(offset_type, 0), offsets_ptr)
    builder.store(builder.trunc(builder.extract_value(n_elems, 0), lir.
        IntType(offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    egj__dph.offsets = lbvl__snxkh._getvalue()
    toa__qody = builder.udiv(builder.add(n_arrays, lir.Constant(lir.IntType
        (64), 7)), lir.Constant(lir.IntType(64), 8))
    pyc__pnh = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [toa__qody])
    null_bitmap_ptr = pyc__pnh.data
    egj__dph.null_bitmap = pyc__pnh._getvalue()
    builder.store(egj__dph._getvalue(), epo__bvyz)
    return shlfe__dvmd, egj__dph.data, offsets_ptr, null_bitmap_ptr


def _unbox_array_item_array_copy_data(arr_typ, arr_obj, c, data_arr,
    item_ind, n_items):
    context = c.context
    builder = c.builder
    arr_obj = to_arr_obj_if_list_obj(c, context, builder, arr_obj, arr_typ)
    arr_val = c.pyapi.to_native_value(arr_typ, arr_obj).value
    sig = types.none(arr_typ, types.int64, types.int64, arr_typ)

    def copy_data(data_arr, item_ind, n_items, arr_val):
        data_arr[item_ind:item_ind + n_items] = arr_val
    wma__mhrn, dxt__lxwn = c.pyapi.call_jit_code(copy_data, sig, [data_arr,
        item_ind, n_items, arr_val])
    c.context.nrt.decref(builder, arr_typ, arr_val)


def _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
    offsets_ptr, null_bitmap_ptr):
    context = c.context
    builder = c.builder
    xqofu__ojp = context.insert_const_string(builder.module, 'pandas')
    saw__negw = c.pyapi.import_module_noblock(xqofu__ojp)
    ksta__ydept = c.pyapi.object_getattr_string(saw__negw, 'NA')
    kvcqh__rfxr = c.context.get_constant(offset_type, 0)
    builder.store(kvcqh__rfxr, offsets_ptr)
    qgsdo__ylm = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_arrays) as yymc__aim:
        xwn__mteq = yymc__aim.index
        item_ind = builder.load(qgsdo__ylm)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [xwn__mteq]))
        arr_obj = seq_getitem(builder, context, val, xwn__mteq)
        set_bitmap_bit(builder, null_bitmap_ptr, xwn__mteq, 0)
        lomb__vxjw = is_na_value(builder, context, arr_obj, ksta__ydept)
        lweo__qooo = builder.icmp_unsigned('!=', lomb__vxjw, lir.Constant(
            lomb__vxjw.type, 1))
        with builder.if_then(lweo__qooo):
            set_bitmap_bit(builder, null_bitmap_ptr, xwn__mteq, 1)
            n_items = bodo.utils.utils.object_length(c, arr_obj)
            _unbox_array_item_array_copy_data(typ.dtype, arr_obj, c,
                data_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), qgsdo__ylm)
        c.pyapi.decref(arr_obj)
    builder.store(builder.trunc(builder.load(qgsdo__ylm), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_arrays]))
    c.pyapi.decref(saw__negw)
    c.pyapi.decref(ksta__ydept)


@unbox(ArrayItemArrayType)
def unbox_array_item_array(typ, val, c):
    drx__zaqq = isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (
        types.int64, types.float64, types.bool_, datetime_date_type)
    n_arrays = bodo.utils.utils.object_length(c, val)
    if drx__zaqq:
        mklc__bmw = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        wue__wzeu = cgutils.get_or_insert_function(c.builder.module,
            mklc__bmw, name='count_total_elems_list_array')
        n_elems = cgutils.pack_array(c.builder, [c.builder.call(wue__wzeu,
            [val])])
    else:
        eobjz__qbj = get_array_elem_counts(c, c.builder, c.context, val, typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            eobjz__qbj, kwi__tlo) for kwi__tlo in range(1, eobjz__qbj.type.
            count)])
    shlfe__dvmd, data_arr, offsets_ptr, null_bitmap_ptr = (
        construct_array_item_array(c.context, c.builder, typ, n_arrays,
        n_elems, c))
    if drx__zaqq:
        umvhy__canx = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        wpqrf__jicp = c.context.make_array(typ.dtype)(c.context, c.builder,
            data_arr).data
        mklc__bmw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(
            offset_type.bitwidth).as_pointer(), lir.IntType(8).as_pointer(),
            lir.IntType(32)])
        kzin__izx = cgutils.get_or_insert_function(c.builder.module,
            mklc__bmw, name='array_item_array_from_sequence')
        c.builder.call(kzin__izx, [val, c.builder.bitcast(wpqrf__jicp, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), umvhy__canx)])
    else:
        _unbox_array_item_array_generic(typ, val, c, n_arrays, data_arr,
            offsets_ptr, null_bitmap_ptr)
    tbg__rjaj = c.context.make_helper(c.builder, typ)
    tbg__rjaj.meminfo = shlfe__dvmd
    yxymq__nat = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(tbg__rjaj._getvalue(), is_error=yxymq__nat)


def _get_array_item_arr_payload(context, builder, arr_typ, arr):
    tbg__rjaj = context.make_helper(builder, arr_typ, arr)
    payload_type = ArrayItemArrayPayloadType(arr_typ)
    abm__apq = context.nrt.meminfo_data(builder, tbg__rjaj.meminfo)
    epo__bvyz = builder.bitcast(abm__apq, context.get_value_type(
        payload_type).as_pointer())
    egj__dph = cgutils.create_struct_proxy(payload_type)(context, builder,
        builder.load(epo__bvyz))
    return egj__dph


def _box_array_item_array_generic(typ, c, n_arrays, data_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    xqofu__ojp = context.insert_const_string(builder.module, 'numpy')
    xvl__rdmi = c.pyapi.import_module_noblock(xqofu__ojp)
    qgnf__ccpc = c.pyapi.object_getattr_string(xvl__rdmi, 'object_')
    yecpb__urqh = c.pyapi.long_from_longlong(n_arrays)
    bkbk__ovcdx = c.pyapi.call_method(xvl__rdmi, 'ndarray', (yecpb__urqh,
        qgnf__ccpc))
    hkkdp__olyf = c.pyapi.object_getattr_string(xvl__rdmi, 'nan')
    qgsdo__ylm = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_arrays) as yymc__aim:
        xwn__mteq = yymc__aim.index
        pyarray_setitem(builder, context, bkbk__ovcdx, xwn__mteq, hkkdp__olyf)
        nxrf__roxq = get_bitmap_bit(builder, null_bitmap_ptr, xwn__mteq)
        akz__wnte = builder.icmp_unsigned('!=', nxrf__roxq, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(akz__wnte):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(xwn__mteq, lir.Constant(xwn__mteq
                .type, 1))])), builder.load(builder.gep(offsets_ptr, [
                xwn__mteq]))), lir.IntType(64))
            item_ind = builder.load(qgsdo__ylm)
            wma__mhrn, mqap__yxddy = c.pyapi.call_jit_code(lambda data_arr,
                item_ind, n_items: data_arr[item_ind:item_ind + n_items],
                typ.dtype(typ.dtype, types.int64, types.int64), [data_arr,
                item_ind, n_items])
            builder.store(builder.add(item_ind, n_items), qgsdo__ylm)
            arr_obj = c.pyapi.from_native_value(typ.dtype, mqap__yxddy, c.
                env_manager)
            pyarray_setitem(builder, context, bkbk__ovcdx, xwn__mteq, arr_obj)
            c.pyapi.decref(arr_obj)
    c.pyapi.decref(xvl__rdmi)
    c.pyapi.decref(qgnf__ccpc)
    c.pyapi.decref(yecpb__urqh)
    c.pyapi.decref(hkkdp__olyf)
    return bkbk__ovcdx


@box(ArrayItemArrayType)
def box_array_item_arr(typ, val, c):
    egj__dph = _get_array_item_arr_payload(c.context, c.builder, typ, val)
    data_arr = egj__dph.data
    offsets_ptr = c.context.make_helper(c.builder, types.Array(offset_type,
        1, 'C'), egj__dph.offsets).data
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), egj__dph.null_bitmap).data
    if isinstance(typ.dtype, types.Array) and typ.dtype.dtype in (types.
        int64, types.float64, types.bool_, datetime_date_type):
        umvhy__canx = bodo.utils.utils.numba_to_c_type(typ.dtype.dtype)
        wpqrf__jicp = c.context.make_helper(c.builder, typ.dtype, data_arr
            ).data
        mklc__bmw = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32)])
        ngmwm__syc = cgutils.get_or_insert_function(c.builder.module,
            mklc__bmw, name='np_array_from_array_item_array')
        arr = c.builder.call(ngmwm__syc, [egj__dph.n_arrays, c.builder.
            bitcast(wpqrf__jicp, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), umvhy__canx)])
    else:
        arr = _box_array_item_array_generic(typ, c, egj__dph.n_arrays,
            data_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def lower_pre_alloc_array_item_array(context, builder, sig, args):
    array_item_type = sig.return_type
    qof__myt, lhzz__tgn, emltv__wdvul = args
    xxza__kkn = bodo.utils.transform.get_type_alloc_counts(array_item_type.
        dtype)
    upcjf__fuivj = sig.args[1]
    if not isinstance(upcjf__fuivj, types.UniTuple):
        lhzz__tgn = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), -1) for emltv__wdvul in range(xxza__kkn)])
    elif upcjf__fuivj.count < xxza__kkn:
        lhzz__tgn = cgutils.pack_array(builder, [builder.extract_value(
            lhzz__tgn, kwi__tlo) for kwi__tlo in range(upcjf__fuivj.count)] +
            [lir.Constant(lir.IntType(64), -1) for emltv__wdvul in range(
            xxza__kkn - upcjf__fuivj.count)])
    shlfe__dvmd, emltv__wdvul, emltv__wdvul, emltv__wdvul = (
        construct_array_item_array(context, builder, array_item_type,
        qof__myt, lhzz__tgn))
    tbg__rjaj = context.make_helper(builder, array_item_type)
    tbg__rjaj.meminfo = shlfe__dvmd
    return tbg__rjaj._getvalue()


@intrinsic
def pre_alloc_array_item_array(typingctx, num_arrs_typ, num_values_typ,
    dtype_typ=None):
    assert isinstance(num_arrs_typ, types.Integer)
    array_item_type = ArrayItemArrayType(dtype_typ.instance_type)
    num_values_typ = types.unliteral(num_values_typ)
    return array_item_type(types.int64, num_values_typ, dtype_typ
        ), lower_pre_alloc_array_item_array


def pre_alloc_array_item_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_array_item_arr_ext_pre_alloc_array_item_array
    ) = pre_alloc_array_item_array_equiv


def init_array_item_array_codegen(context, builder, signature, args):
    n_arrays, blffl__mxnlg, lbvl__snxkh, pyc__pnh = args
    array_item_type = signature.return_type
    payload_type = ArrayItemArrayPayloadType(array_item_type)
    klg__rua = context.get_value_type(payload_type)
    xln__zfy = context.get_abi_sizeof(klg__rua)
    uwze__kmld = define_array_item_dtor(context, builder, array_item_type,
        payload_type)
    shlfe__dvmd = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, xln__zfy), uwze__kmld)
    abm__apq = context.nrt.meminfo_data(builder, shlfe__dvmd)
    epo__bvyz = builder.bitcast(abm__apq, klg__rua.as_pointer())
    egj__dph = cgutils.create_struct_proxy(payload_type)(context, builder)
    egj__dph.n_arrays = n_arrays
    egj__dph.data = blffl__mxnlg
    egj__dph.offsets = lbvl__snxkh
    egj__dph.null_bitmap = pyc__pnh
    builder.store(egj__dph._getvalue(), epo__bvyz)
    context.nrt.incref(builder, signature.args[1], blffl__mxnlg)
    context.nrt.incref(builder, signature.args[2], lbvl__snxkh)
    context.nrt.incref(builder, signature.args[3], pyc__pnh)
    tbg__rjaj = context.make_helper(builder, array_item_type)
    tbg__rjaj.meminfo = shlfe__dvmd
    return tbg__rjaj._getvalue()


@intrinsic
def init_array_item_array(typingctx, n_arrays_typ, data_type, offsets_typ,
    null_bitmap_typ=None):
    assert null_bitmap_typ == types.Array(types.uint8, 1, 'C')
    kogvu__ojk = ArrayItemArrayType(data_type)
    sig = kogvu__ojk(types.int64, data_type, offsets_typ, null_bitmap_typ)
    return sig, init_array_item_array_codegen


@intrinsic
def get_offsets(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        egj__dph = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            egj__dph.offsets)
    return types.Array(offset_type, 1, 'C')(arr_typ), codegen


@intrinsic
def get_offsets_ind(typingctx, arr_typ, ind_t=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, ind = args
        egj__dph = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        wpqrf__jicp = context.make_array(types.Array(offset_type, 1, 'C'))(
            context, builder, egj__dph.offsets).data
        lbvl__snxkh = builder.bitcast(wpqrf__jicp, lir.IntType(offset_type.
            bitwidth).as_pointer())
        return builder.load(builder.gep(lbvl__snxkh, [ind]))
    return offset_type(arr_typ, types.int64), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        egj__dph = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            egj__dph.data)
    return arr_typ.dtype(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        egj__dph = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            egj__dph.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


def alias_ext_single_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_offsets',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array
numba.core.ir_utils.alias_func_extensions['get_data',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array
numba.core.ir_utils.alias_func_extensions['get_null_bitmap',
    'bodo.libs.array_item_arr_ext'] = alias_ext_single_array


@intrinsic
def get_n_arrays(typingctx, arr_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        egj__dph = _get_array_item_arr_payload(context, builder, arr_typ, arr)
        return egj__dph.n_arrays
    return types.int64(arr_typ), codegen


@intrinsic
def replace_data_arr(typingctx, arr_typ, data_typ=None):
    assert isinstance(arr_typ, ArrayItemArrayType
        ) and data_typ == arr_typ.dtype

    def codegen(context, builder, sig, args):
        arr, ndlay__kkqbd = args
        tbg__rjaj = context.make_helper(builder, arr_typ, arr)
        payload_type = ArrayItemArrayPayloadType(arr_typ)
        abm__apq = context.nrt.meminfo_data(builder, tbg__rjaj.meminfo)
        epo__bvyz = builder.bitcast(abm__apq, context.get_value_type(
            payload_type).as_pointer())
        egj__dph = cgutils.create_struct_proxy(payload_type)(context,
            builder, builder.load(epo__bvyz))
        context.nrt.decref(builder, data_typ, egj__dph.data)
        egj__dph.data = ndlay__kkqbd
        context.nrt.incref(builder, data_typ, ndlay__kkqbd)
        builder.store(egj__dph._getvalue(), epo__bvyz)
    return types.none(arr_typ, data_typ), codegen


@numba.njit(no_cpython_wrapper=True)
def ensure_data_capacity(arr, old_size, new_size):
    blffl__mxnlg = get_data(arr)
    epen__auzpv = len(blffl__mxnlg)
    if epen__auzpv < new_size:
        xelgi__apmut = max(2 * epen__auzpv, new_size)
        ndlay__kkqbd = bodo.libs.array_kernels.resize_and_copy(blffl__mxnlg,
            old_size, xelgi__apmut)
        replace_data_arr(arr, ndlay__kkqbd)


@numba.njit(no_cpython_wrapper=True)
def trim_excess_data(arr):
    blffl__mxnlg = get_data(arr)
    lbvl__snxkh = get_offsets(arr)
    ecatf__qcl = len(blffl__mxnlg)
    hwcwz__eckrb = lbvl__snxkh[-1]
    if ecatf__qcl != hwcwz__eckrb:
        ndlay__kkqbd = bodo.libs.array_kernels.resize_and_copy(blffl__mxnlg,
            hwcwz__eckrb, hwcwz__eckrb)
        replace_data_arr(arr, ndlay__kkqbd)


@overload(len, no_unliteral=True)
def overload_array_item_arr_len(A):
    if isinstance(A, ArrayItemArrayType):
        return lambda A: get_n_arrays(A)


@overload_attribute(ArrayItemArrayType, 'shape')
def overload_array_item_arr_shape(A):
    return lambda A: (get_n_arrays(A),)


@overload_attribute(ArrayItemArrayType, 'dtype')
def overload_array_item_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(ArrayItemArrayType, 'ndim')
def overload_array_item_arr_ndim(A):
    return lambda A: 1


@overload_attribute(ArrayItemArrayType, 'nbytes')
def overload_array_item_arr_nbytes(A):
    return lambda A: get_data(A).nbytes + get_offsets(A
        ).nbytes + get_null_bitmap(A).nbytes


@overload(operator.getitem, no_unliteral=True)
def array_item_arr_getitem_array(arr, ind):
    if not isinstance(arr, ArrayItemArrayType):
        return
    if isinstance(ind, types.Integer):

        def array_item_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            lbvl__snxkh = get_offsets(arr)
            blffl__mxnlg = get_data(arr)
            sookf__smjlm = lbvl__snxkh[ind]
            epoec__aafo = lbvl__snxkh[ind + 1]
            return blffl__mxnlg[sookf__smjlm:epoec__aafo]
        return array_item_arr_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:
        obwpz__bqp = arr.dtype

        def impl_bool(arr, ind):
            vqd__kgiht = len(arr)
            if vqd__kgiht != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            pyc__pnh = get_null_bitmap(arr)
            n_arrays = 0
            ajk__vrtgy = init_nested_counts(obwpz__bqp)
            for kwi__tlo in range(vqd__kgiht):
                if ind[kwi__tlo]:
                    n_arrays += 1
                    cwy__mfav = arr[kwi__tlo]
                    ajk__vrtgy = add_nested_counts(ajk__vrtgy, cwy__mfav)
            bkbk__ovcdx = pre_alloc_array_item_array(n_arrays, ajk__vrtgy,
                obwpz__bqp)
            gld__kwty = get_null_bitmap(bkbk__ovcdx)
            fea__gif = 0
            for grx__kycvg in range(vqd__kgiht):
                if ind[grx__kycvg]:
                    bkbk__ovcdx[fea__gif] = arr[grx__kycvg]
                    hwvnu__oejlt = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                        pyc__pnh, grx__kycvg)
                    bodo.libs.int_arr_ext.set_bit_to_arr(gld__kwty,
                        fea__gif, hwvnu__oejlt)
                    fea__gif += 1
            return bkbk__ovcdx
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        obwpz__bqp = arr.dtype

        def impl_int(arr, ind):
            pyc__pnh = get_null_bitmap(arr)
            vqd__kgiht = len(ind)
            n_arrays = vqd__kgiht
            ajk__vrtgy = init_nested_counts(obwpz__bqp)
            for vnyhe__bdcf in range(vqd__kgiht):
                kwi__tlo = ind[vnyhe__bdcf]
                cwy__mfav = arr[kwi__tlo]
                ajk__vrtgy = add_nested_counts(ajk__vrtgy, cwy__mfav)
            bkbk__ovcdx = pre_alloc_array_item_array(n_arrays, ajk__vrtgy,
                obwpz__bqp)
            gld__kwty = get_null_bitmap(bkbk__ovcdx)
            for krd__mnx in range(vqd__kgiht):
                grx__kycvg = ind[krd__mnx]
                bkbk__ovcdx[krd__mnx] = arr[grx__kycvg]
                hwvnu__oejlt = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    pyc__pnh, grx__kycvg)
                bodo.libs.int_arr_ext.set_bit_to_arr(gld__kwty, krd__mnx,
                    hwvnu__oejlt)
            return bkbk__ovcdx
        return impl_int
    if isinstance(ind, types.SliceType):

        def impl_slice(arr, ind):
            vqd__kgiht = len(arr)
            daljv__kzud = numba.cpython.unicode._normalize_slice(ind,
                vqd__kgiht)
            svs__jlho = np.arange(daljv__kzud.start, daljv__kzud.stop,
                daljv__kzud.step)
            return arr[svs__jlho]
        return impl_slice


@overload(operator.setitem)
def array_item_arr_setitem(A, idx, val):
    if not isinstance(A, ArrayItemArrayType):
        return
    if isinstance(idx, types.Integer):

        def impl_scalar(A, idx, val):
            lbvl__snxkh = get_offsets(A)
            pyc__pnh = get_null_bitmap(A)
            if idx == 0:
                lbvl__snxkh[0] = 0
            n_items = len(val)
            mnxk__fid = lbvl__snxkh[idx] + n_items
            ensure_data_capacity(A, lbvl__snxkh[idx], mnxk__fid)
            blffl__mxnlg = get_data(A)
            lbvl__snxkh[idx + 1] = lbvl__snxkh[idx] + n_items
            blffl__mxnlg[lbvl__snxkh[idx]:lbvl__snxkh[idx + 1]] = val
            bodo.libs.int_arr_ext.set_bit_to_arr(pyc__pnh, idx, 1)
        return impl_scalar
    if isinstance(idx, types.SliceType) and A.dtype == val:

        def impl_slice_elem(A, idx, val):
            daljv__kzud = numba.cpython.unicode._normalize_slice(idx, len(A))
            for kwi__tlo in range(daljv__kzud.start, daljv__kzud.stop,
                daljv__kzud.step):
                A[kwi__tlo] = val
        return impl_slice_elem
    if isinstance(idx, types.SliceType) and is_iterable_type(val):

        def impl_slice(A, idx, val):
            val = bodo.utils.conversion.coerce_to_array(val,
                use_nullable_array=True)
            lbvl__snxkh = get_offsets(A)
            pyc__pnh = get_null_bitmap(A)
            ndn__wmgc = get_offsets(val)
            snjf__arv = get_data(val)
            ywrxu__mpt = get_null_bitmap(val)
            vqd__kgiht = len(A)
            daljv__kzud = numba.cpython.unicode._normalize_slice(idx,
                vqd__kgiht)
            adth__ezvvc, hwti__mqz = daljv__kzud.start, daljv__kzud.stop
            assert daljv__kzud.step == 1
            if adth__ezvvc == 0:
                lbvl__snxkh[adth__ezvvc] = 0
            pxsko__uog = lbvl__snxkh[adth__ezvvc]
            mnxk__fid = pxsko__uog + len(snjf__arv)
            ensure_data_capacity(A, pxsko__uog, mnxk__fid)
            blffl__mxnlg = get_data(A)
            blffl__mxnlg[pxsko__uog:pxsko__uog + len(snjf__arv)] = snjf__arv
            lbvl__snxkh[adth__ezvvc:hwti__mqz + 1] = ndn__wmgc + pxsko__uog
            ccn__hdegc = 0
            for kwi__tlo in range(adth__ezvvc, hwti__mqz):
                hwvnu__oejlt = bodo.libs.int_arr_ext.get_bit_bitmap_arr(
                    ywrxu__mpt, ccn__hdegc)
                bodo.libs.int_arr_ext.set_bit_to_arr(pyc__pnh, kwi__tlo,
                    hwvnu__oejlt)
                ccn__hdegc += 1
        return impl_slice
    raise BodoError(
        'only setitem with scalar index is currently supported for list arrays'
        )


@overload_method(ArrayItemArrayType, 'copy', no_unliteral=True)
def overload_array_item_arr_copy(A):

    def copy_impl(A):
        return init_array_item_array(len(A), get_data(A).copy(),
            get_offsets(A).copy(), get_null_bitmap(A).copy())
    return copy_impl
