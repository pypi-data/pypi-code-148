"""Array implementation for map values.
Corresponds to Spark's MapType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Map arrays: https://github.com/apache/arrow/blob/master/format/Schema.fbs

The implementation uses an array(struct) array underneath similar to Spark and Arrow.
For example: [{1: 2.1, 3: 1.1}, {5: -1.0}]
[[{"key": 1, "value" 2.1}, {"key": 3, "value": 1.1}], [{"key": 5, "value": -1.0}]]
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, _get_array_item_arr_payload, offset_type
from bodo.libs.struct_arr_ext import StructArrayType, _get_struct_arr_payload
from bodo.utils.cg_helpers import dict_keys, dict_merge_from_seq2, dict_values, gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit
from bodo.utils.typing import BodoError
from bodo.libs import array_ext, hdist
ll.add_symbol('count_total_elems_list_array', array_ext.
    count_total_elems_list_array)
ll.add_symbol('map_array_from_sequence', array_ext.map_array_from_sequence)
ll.add_symbol('np_array_from_map_array', array_ext.np_array_from_map_array)


class MapArrayType(types.ArrayCompatible):

    def __init__(self, key_arr_type, value_arr_type):
        self.key_arr_type = key_arr_type
        self.value_arr_type = value_arr_type
        super(MapArrayType, self).__init__(name='MapArrayType({}, {})'.
            format(key_arr_type, value_arr_type))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.DictType(self.key_arr_type.dtype, self.value_arr_type.
            dtype)

    def copy(self):
        return MapArrayType(self.key_arr_type, self.value_arr_type)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_map_arr_data_type(map_type):
    tot__gkgwc = StructArrayType((map_type.key_arr_type, map_type.
        value_arr_type), ('key', 'value'))
    return ArrayItemArrayType(tot__gkgwc)


@register_model(MapArrayType)
class MapArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xigq__pvsv = _get_map_arr_data_type(fe_type)
        udg__zwq = [('data', xigq__pvsv)]
        models.StructModel.__init__(self, dmm, fe_type, udg__zwq)


make_attribute_wrapper(MapArrayType, 'data', '_data')


@unbox(MapArrayType)
def unbox_map_array(typ, val, c):
    n_maps = bodo.utils.utils.object_length(c, val)
    ncx__oqo = all(isinstance(rlcx__qhp, types.Array) and rlcx__qhp.dtype in
        (types.int64, types.float64, types.bool_, datetime_date_type) for
        rlcx__qhp in (typ.key_arr_type, typ.value_arr_type))
    if ncx__oqo:
        lrwkh__gupz = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer()])
        isl__brjqb = cgutils.get_or_insert_function(c.builder.module,
            lrwkh__gupz, name='count_total_elems_list_array')
        fqa__dcd = cgutils.pack_array(c.builder, [n_maps, c.builder.call(
            isl__brjqb, [val])])
    else:
        fqa__dcd = get_array_elem_counts(c, c.builder, c.context, val, typ)
    xigq__pvsv = _get_map_arr_data_type(typ)
    data_arr = gen_allocate_array(c.context, c.builder, xigq__pvsv, fqa__dcd, c
        )
    jvl__uzys = _get_array_item_arr_payload(c.context, c.builder,
        xigq__pvsv, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, jvl__uzys.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, jvl__uzys.offsets).data
    ofved__zfj = _get_struct_arr_payload(c.context, c.builder, xigq__pvsv.
        dtype, jvl__uzys.data)
    key_arr = c.builder.extract_value(ofved__zfj.data, 0)
    value_arr = c.builder.extract_value(ofved__zfj.data, 1)
    sig = types.none(types.Array(types.uint8, 1, 'C'))
    djpnd__tcklo, grc__qcw = c.pyapi.call_jit_code(lambda A: A.fill(255),
        sig, [ofved__zfj.null_bitmap])
    if ncx__oqo:
        nai__gbf = c.context.make_array(xigq__pvsv.dtype.data[0])(c.context,
            c.builder, key_arr).data
        egvyz__hsq = c.context.make_array(xigq__pvsv.dtype.data[1])(c.
            context, c.builder, value_arr).data
        lrwkh__gupz = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(32), lir.IntType(32)])
        lnxkh__jdl = cgutils.get_or_insert_function(c.builder.module,
            lrwkh__gupz, name='map_array_from_sequence')
        kpo__rejiv = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        dxkdg__isbr = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype
            )
        c.builder.call(lnxkh__jdl, [val, c.builder.bitcast(nai__gbf, lir.
            IntType(8).as_pointer()), c.builder.bitcast(egvyz__hsq, lir.
            IntType(8).as_pointer()), offsets_ptr, null_bitmap_ptr, lir.
            Constant(lir.IntType(32), kpo__rejiv), lir.Constant(lir.IntType
            (32), dxkdg__isbr)])
    else:
        _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
            offsets_ptr, null_bitmap_ptr)
    ijl__zqc = c.context.make_helper(c.builder, typ)
    ijl__zqc.data = data_arr
    thqfx__krj = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(ijl__zqc._getvalue(), is_error=thqfx__krj)


def _unbox_map_array_generic(typ, val, c, n_maps, key_arr, value_arr,
    offsets_ptr, null_bitmap_ptr):
    from bodo.libs.array_item_arr_ext import _unbox_array_item_array_copy_data
    context = c.context
    builder = c.builder
    dxzzm__ktq = context.insert_const_string(builder.module, 'pandas')
    zgo__adm = c.pyapi.import_module_noblock(dxzzm__ktq)
    ucea__fzvdq = c.pyapi.object_getattr_string(zgo__adm, 'NA')
    def__kymg = c.context.get_constant(offset_type, 0)
    builder.store(def__kymg, offsets_ptr)
    tyhqi__yeny = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with cgutils.for_range(builder, n_maps) as yaznz__qskq:
        qreyp__cwign = yaznz__qskq.index
        item_ind = builder.load(tyhqi__yeny)
        builder.store(builder.trunc(item_ind, lir.IntType(offset_type.
            bitwidth)), builder.gep(offsets_ptr, [qreyp__cwign]))
        slw__yiyk = seq_getitem(builder, context, val, qreyp__cwign)
        set_bitmap_bit(builder, null_bitmap_ptr, qreyp__cwign, 0)
        vjbd__jggt = is_na_value(builder, context, slw__yiyk, ucea__fzvdq)
        uroc__jaxwn = builder.icmp_unsigned('!=', vjbd__jggt, lir.Constant(
            vjbd__jggt.type, 1))
        with builder.if_then(uroc__jaxwn):
            set_bitmap_bit(builder, null_bitmap_ptr, qreyp__cwign, 1)
            qnh__rmyql = dict_keys(builder, context, slw__yiyk)
            xkuz__oarc = dict_values(builder, context, slw__yiyk)
            n_items = bodo.utils.utils.object_length(c, qnh__rmyql)
            _unbox_array_item_array_copy_data(typ.key_arr_type, qnh__rmyql,
                c, key_arr, item_ind, n_items)
            _unbox_array_item_array_copy_data(typ.value_arr_type,
                xkuz__oarc, c, value_arr, item_ind, n_items)
            builder.store(builder.add(item_ind, n_items), tyhqi__yeny)
            c.pyapi.decref(qnh__rmyql)
            c.pyapi.decref(xkuz__oarc)
        c.pyapi.decref(slw__yiyk)
    builder.store(builder.trunc(builder.load(tyhqi__yeny), lir.IntType(
        offset_type.bitwidth)), builder.gep(offsets_ptr, [n_maps]))
    c.pyapi.decref(zgo__adm)
    c.pyapi.decref(ucea__fzvdq)


@box(MapArrayType)
def box_map_arr(typ, val, c):
    ijl__zqc = c.context.make_helper(c.builder, typ, val)
    data_arr = ijl__zqc.data
    xigq__pvsv = _get_map_arr_data_type(typ)
    jvl__uzys = _get_array_item_arr_payload(c.context, c.builder,
        xigq__pvsv, data_arr)
    null_bitmap_ptr = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c
        .context, c.builder, jvl__uzys.null_bitmap).data
    offsets_ptr = c.context.make_array(types.Array(offset_type, 1, 'C'))(c.
        context, c.builder, jvl__uzys.offsets).data
    ofved__zfj = _get_struct_arr_payload(c.context, c.builder, xigq__pvsv.
        dtype, jvl__uzys.data)
    key_arr = c.builder.extract_value(ofved__zfj.data, 0)
    value_arr = c.builder.extract_value(ofved__zfj.data, 1)
    if all(isinstance(rlcx__qhp, types.Array) and rlcx__qhp.dtype in (types
        .int64, types.float64, types.bool_, datetime_date_type) for
        rlcx__qhp in (typ.key_arr_type, typ.value_arr_type)):
        nai__gbf = c.context.make_array(xigq__pvsv.dtype.data[0])(c.context,
            c.builder, key_arr).data
        egvyz__hsq = c.context.make_array(xigq__pvsv.dtype.data[1])(c.
            context, c.builder, value_arr).data
        lrwkh__gupz = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(offset_type.bitwidth).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(32)])
        vveux__raj = cgutils.get_or_insert_function(c.builder.module,
            lrwkh__gupz, name='np_array_from_map_array')
        kpo__rejiv = bodo.utils.utils.numba_to_c_type(typ.key_arr_type.dtype)
        dxkdg__isbr = bodo.utils.utils.numba_to_c_type(typ.value_arr_type.dtype
            )
        arr = c.builder.call(vveux__raj, [jvl__uzys.n_arrays, c.builder.
            bitcast(nai__gbf, lir.IntType(8).as_pointer()), c.builder.
            bitcast(egvyz__hsq, lir.IntType(8).as_pointer()), offsets_ptr,
            null_bitmap_ptr, lir.Constant(lir.IntType(32), kpo__rejiv), lir
            .Constant(lir.IntType(32), dxkdg__isbr)])
    else:
        arr = _box_map_array_generic(typ, c, jvl__uzys.n_arrays, key_arr,
            value_arr, offsets_ptr, null_bitmap_ptr)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_map_array_generic(typ, c, n_maps, key_arr, value_arr, offsets_ptr,
    null_bitmap_ptr):
    context = c.context
    builder = c.builder
    dxzzm__ktq = context.insert_const_string(builder.module, 'numpy')
    odfv__draca = c.pyapi.import_module_noblock(dxzzm__ktq)
    nawx__mazkk = c.pyapi.object_getattr_string(odfv__draca, 'object_')
    zqq__allok = c.pyapi.long_from_longlong(n_maps)
    ehmmz__orvch = c.pyapi.call_method(odfv__draca, 'ndarray', (zqq__allok,
        nawx__mazkk))
    qafb__wlwi = c.pyapi.object_getattr_string(odfv__draca, 'nan')
    aysy__qohg = c.pyapi.unserialize(c.pyapi.serialize_object(zip))
    tyhqi__yeny = cgutils.alloca_once_value(builder, lir.Constant(lir.
        IntType(64), 0))
    with cgutils.for_range(builder, n_maps) as yaznz__qskq:
        pnxyi__ipyyv = yaznz__qskq.index
        pyarray_setitem(builder, context, ehmmz__orvch, pnxyi__ipyyv,
            qafb__wlwi)
        pbx__cnqag = get_bitmap_bit(builder, null_bitmap_ptr, pnxyi__ipyyv)
        szy__wct = builder.icmp_unsigned('!=', pbx__cnqag, lir.Constant(lir
            .IntType(8), 0))
        with builder.if_then(szy__wct):
            n_items = builder.sext(builder.sub(builder.load(builder.gep(
                offsets_ptr, [builder.add(pnxyi__ipyyv, lir.Constant(
                pnxyi__ipyyv.type, 1))])), builder.load(builder.gep(
                offsets_ptr, [pnxyi__ipyyv]))), lir.IntType(64))
            item_ind = builder.load(tyhqi__yeny)
            slw__yiyk = c.pyapi.dict_new()
            cohcq__gudql = lambda data_arr, item_ind, n_items: data_arr[
                item_ind:item_ind + n_items]
            djpnd__tcklo, mtoxc__iwic = c.pyapi.call_jit_code(cohcq__gudql,
                typ.key_arr_type(typ.key_arr_type, types.int64, types.int64
                ), [key_arr, item_ind, n_items])
            djpnd__tcklo, zcxi__wmn = c.pyapi.call_jit_code(cohcq__gudql,
                typ.value_arr_type(typ.value_arr_type, types.int64, types.
                int64), [value_arr, item_ind, n_items])
            igdhy__mjrv = c.pyapi.from_native_value(typ.key_arr_type,
                mtoxc__iwic, c.env_manager)
            iwpi__qzas = c.pyapi.from_native_value(typ.value_arr_type,
                zcxi__wmn, c.env_manager)
            hzs__mizhd = c.pyapi.call_function_objargs(aysy__qohg, (
                igdhy__mjrv, iwpi__qzas))
            dict_merge_from_seq2(builder, context, slw__yiyk, hzs__mizhd)
            builder.store(builder.add(item_ind, n_items), tyhqi__yeny)
            pyarray_setitem(builder, context, ehmmz__orvch, pnxyi__ipyyv,
                slw__yiyk)
            c.pyapi.decref(hzs__mizhd)
            c.pyapi.decref(igdhy__mjrv)
            c.pyapi.decref(iwpi__qzas)
            c.pyapi.decref(slw__yiyk)
    c.pyapi.decref(aysy__qohg)
    c.pyapi.decref(odfv__draca)
    c.pyapi.decref(nawx__mazkk)
    c.pyapi.decref(zqq__allok)
    c.pyapi.decref(qafb__wlwi)
    return ehmmz__orvch


def init_map_arr_codegen(context, builder, sig, args):
    data_arr, = args
    ijl__zqc = context.make_helper(builder, sig.return_type)
    ijl__zqc.data = data_arr
    context.nrt.incref(builder, sig.args[0], data_arr)
    return ijl__zqc._getvalue()


@intrinsic
def init_map_arr(typingctx, data_typ=None):
    assert isinstance(data_typ, ArrayItemArrayType) and isinstance(data_typ
        .dtype, StructArrayType)
    ysbr__kxi = MapArrayType(data_typ.dtype.data[0], data_typ.dtype.data[1])
    return ysbr__kxi(data_typ), init_map_arr_codegen


def alias_ext_init_map_arr(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_map_arr',
    'bodo.libs.map_arr_ext'] = alias_ext_init_map_arr


@numba.njit
def pre_alloc_map_array(num_maps, nested_counts, struct_typ):
    ijw__fsn = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(num_maps
        , nested_counts, struct_typ)
    return init_map_arr(ijw__fsn)


def pre_alloc_map_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 3 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_map_arr_ext_pre_alloc_map_array
    ) = pre_alloc_map_array_equiv


@overload(len, no_unliteral=True)
def overload_map_arr_len(A):
    if isinstance(A, MapArrayType):
        return lambda A: len(A._data)


@overload_attribute(MapArrayType, 'shape')
def overload_map_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(MapArrayType, 'dtype')
def overload_map_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(MapArrayType, 'ndim')
def overload_map_arr_ndim(A):
    return lambda A: 1


@overload_attribute(MapArrayType, 'nbytes')
def overload_map_arr_nbytes(A):
    return lambda A: A._data.nbytes


@overload_method(MapArrayType, 'copy')
def overload_map_arr_copy(A):
    return lambda A: init_map_arr(A._data.copy())


@overload(operator.setitem, no_unliteral=True)
def map_arr_setitem(arr, ind, val):
    if not isinstance(arr, MapArrayType):
        return
    pyxv__qhq = arr.key_arr_type, arr.value_arr_type
    if isinstance(ind, types.Integer):

        def map_arr_setitem_impl(arr, ind, val):
            urmv__knyl = val.keys()
            qofxp__ckm = bodo.libs.struct_arr_ext.pre_alloc_struct_array(len
                (val), (-1,), pyxv__qhq, ('key', 'value'))
            for rgu__wots, crmey__hqic in enumerate(urmv__knyl):
                qofxp__ckm[rgu__wots] = bodo.libs.struct_arr_ext.init_struct((
                    crmey__hqic, val[crmey__hqic]), ('key', 'value'))
            arr._data[ind] = qofxp__ckm
        return map_arr_setitem_impl
    raise BodoError(
        'operator.setitem with MapArrays is only supported with an integer index.'
        )


@overload(operator.getitem, no_unliteral=True)
def map_arr_getitem(arr, ind):
    if not isinstance(arr, MapArrayType):
        return
    if isinstance(ind, types.Integer):

        def map_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            ephlc__uekj = dict()
            dnbke__wttvz = bodo.libs.array_item_arr_ext.get_offsets(arr._data)
            qofxp__ckm = bodo.libs.array_item_arr_ext.get_data(arr._data)
            efo__itve, pfau__gxla = bodo.libs.struct_arr_ext.get_data(
                qofxp__ckm)
            qetrv__fcw = dnbke__wttvz[ind]
            nblwa__mcqb = dnbke__wttvz[ind + 1]
            for rgu__wots in range(qetrv__fcw, nblwa__mcqb):
                ephlc__uekj[efo__itve[rgu__wots]] = pfau__gxla[rgu__wots]
            return ephlc__uekj
        return map_arr_getitem_impl
    raise BodoError(
        'operator.getitem with MapArrays is only supported with an integer index.'
        )
