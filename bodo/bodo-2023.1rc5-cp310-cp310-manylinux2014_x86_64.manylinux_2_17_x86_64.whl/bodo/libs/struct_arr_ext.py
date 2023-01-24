"""Array implementation for structs of values.
Corresponds to Spark's StructType: https://spark.apache.org/docs/latest/sql-reference.html
Corresponds to Arrow's Struct arrays: https://arrow.apache.org/docs/format/Columnar.html

The values are stored in contiguous data arrays; one array per field. For example:
A:             ["AA", "B", "C"]
B:             [1, 2, 4]
"""
import operator
import llvmlite.binding as ll
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.extending import NativeValue, box, intrinsic, models, overload, overload_attribute, overload_method, register_model, unbox
from numba.parfors.array_analysis import ArrayAnalysis
from numba.typed.typedobjectutils import _cast
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.time_ext import TimeType
from bodo.libs import array_ext
from bodo.utils.cg_helpers import gen_allocate_array, get_array_elem_counts, get_bitmap_bit, is_na_value, pyarray_setitem, seq_getitem, set_bitmap_bit, to_arr_obj_if_list_obj
from bodo.utils.typing import BodoError, dtype_to_array_type, get_overload_const_int, get_overload_const_str, is_list_like_index_type, is_overload_constant_int, is_overload_constant_str, is_overload_none
ll.add_symbol('struct_array_from_sequence', array_ext.
    struct_array_from_sequence)
ll.add_symbol('np_array_from_struct_array', array_ext.
    np_array_from_struct_array)


class StructArrayType(types.ArrayCompatible):

    def __init__(self, data, names=None):
        assert isinstance(data, tuple) and len(data) > 0 and all(bodo.utils
            .utils.is_array_typ(heo__jqnx, False) for heo__jqnx in data)
        if names is not None:
            assert isinstance(names, tuple) and all(isinstance(heo__jqnx,
                str) for heo__jqnx in names) and len(names) == len(data)
        else:
            names = tuple('f{}'.format(i) for i in range(len(data)))
        self.data = data
        self.names = names
        super(StructArrayType, self).__init__(name=
            'StructArrayType({}, {})'.format(data, names))

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return StructType(tuple(mlhzi__lgnn.dtype for mlhzi__lgnn in self.
            data), self.names)

    @classmethod
    def from_dict(cls, d):
        assert isinstance(d, dict)
        names = tuple(str(heo__jqnx) for heo__jqnx in d.keys())
        data = tuple(dtype_to_array_type(mlhzi__lgnn) for mlhzi__lgnn in d.
            values())
        return StructArrayType(data, names)

    def copy(self):
        return StructArrayType(self.data, self.names)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructArrayPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple) and all(bodo.utils.utils.
            is_array_typ(heo__jqnx, False) for heo__jqnx in data)
        self.data = data
        super(StructArrayPayloadType, self).__init__(name=
            'StructArrayPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructArrayPayloadType)
class StructArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kkg__aux = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, kkg__aux)


@register_model(StructArrayType)
class StructArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructArrayPayloadType(fe_type.data)
        kkg__aux = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, kkg__aux)


def define_struct_arr_dtor(context, builder, struct_arr_type, payload_type):
    prq__jaab = builder.module
    wvvq__nfiuw = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    lnd__bvo = cgutils.get_or_insert_function(prq__jaab, wvvq__nfiuw, name=
        '.dtor.struct_arr.{}.{}.'.format(struct_arr_type.data,
        struct_arr_type.names))
    if not lnd__bvo.is_declaration:
        return lnd__bvo
    lnd__bvo.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(lnd__bvo.append_basic_block())
    lukx__hulh = lnd__bvo.args[0]
    jnttp__sztb = context.get_value_type(payload_type).as_pointer()
    nbl__brpk = builder.bitcast(lukx__hulh, jnttp__sztb)
    lqvpd__ycxij = context.make_helper(builder, payload_type, ref=nbl__brpk)
    context.nrt.decref(builder, types.BaseTuple.from_types(struct_arr_type.
        data), lqvpd__ycxij.data)
    context.nrt.decref(builder, types.Array(types.uint8, 1, 'C'),
        lqvpd__ycxij.null_bitmap)
    builder.ret_void()
    return lnd__bvo


def construct_struct_array(context, builder, struct_arr_type, n_structs,
    n_elems, c=None):
    payload_type = StructArrayPayloadType(struct_arr_type.data)
    hhms__lztnq = context.get_value_type(payload_type)
    mlss__yfry = context.get_abi_sizeof(hhms__lztnq)
    qdbz__vgxgy = define_struct_arr_dtor(context, builder, struct_arr_type,
        payload_type)
    zfwkc__hny = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, mlss__yfry), qdbz__vgxgy)
    skhlk__awfsx = context.nrt.meminfo_data(builder, zfwkc__hny)
    ygn__hqu = builder.bitcast(skhlk__awfsx, hhms__lztnq.as_pointer())
    lqvpd__ycxij = cgutils.create_struct_proxy(payload_type)(context, builder)
    arrs = []
    cfx__wxjym = 0
    for arr_typ in struct_arr_type.data:
        iyjyl__kpy = bodo.utils.transform.get_type_alloc_counts(arr_typ.dtype)
        nwt__bcmnm = cgutils.pack_array(builder, [n_structs] + [builder.
            extract_value(n_elems, i) for i in range(cfx__wxjym, cfx__wxjym +
            iyjyl__kpy)])
        arr = gen_allocate_array(context, builder, arr_typ, nwt__bcmnm, c)
        arrs.append(arr)
        cfx__wxjym += iyjyl__kpy
    lqvpd__ycxij.data = cgutils.pack_array(builder, arrs
        ) if types.is_homogeneous(*struct_arr_type.data
        ) else cgutils.pack_struct(builder, arrs)
    citf__gvidi = builder.udiv(builder.add(n_structs, lir.Constant(lir.
        IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
    qkp__ahmki = bodo.utils.utils._empty_nd_impl(context, builder, types.
        Array(types.uint8, 1, 'C'), [citf__gvidi])
    null_bitmap_ptr = qkp__ahmki.data
    lqvpd__ycxij.null_bitmap = qkp__ahmki._getvalue()
    builder.store(lqvpd__ycxij._getvalue(), ygn__hqu)
    return zfwkc__hny, lqvpd__ycxij.data, null_bitmap_ptr


def _get_C_API_ptrs(c, data_tup, data_typ, names):
    uwi__cwds = []
    assert len(data_typ) > 0
    for i, arr_typ in enumerate(data_typ):
        aidbf__sgrt = c.builder.extract_value(data_tup, i)
        arr = c.context.make_array(arr_typ)(c.context, c.builder, value=
            aidbf__sgrt)
        uwi__cwds.append(arr.data)
    aurmq__fav = cgutils.pack_array(c.builder, uwi__cwds
        ) if types.is_homogeneous(*data_typ) else cgutils.pack_struct(c.
        builder, uwi__cwds)
    wbnb__ycbk = cgutils.alloca_once_value(c.builder, aurmq__fav)
    tmace__jxyxm = [c.context.get_constant(types.int32, bodo.utils.utils.
        numba_to_c_type(heo__jqnx.dtype)) for heo__jqnx in data_typ]
    bpxd__avp = cgutils.alloca_once_value(c.builder, cgutils.pack_array(c.
        builder, tmace__jxyxm))
    ozqfg__cfz = cgutils.pack_array(c.builder, [c.context.
        insert_const_string(c.builder.module, heo__jqnx) for heo__jqnx in
        names])
    wjdzg__snfm = cgutils.alloca_once_value(c.builder, ozqfg__cfz)
    return wbnb__ycbk, bpxd__avp, wjdzg__snfm


@unbox(StructArrayType)
def unbox_struct_array(typ, val, c, is_tuple_array=False):
    from bodo.libs.tuple_arr_ext import TupleArrayType
    n_structs = bodo.utils.utils.object_length(c, val)
    qzkol__dkda = all(isinstance(mlhzi__lgnn, types.Array) and (mlhzi__lgnn
        .dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) or isinstance(mlhzi__lgnn.dtype, TimeType)) for
        mlhzi__lgnn in typ.data)
    if qzkol__dkda:
        n_elems = cgutils.pack_array(c.builder, [], lir.IntType(64))
    else:
        kbgoc__syg = get_array_elem_counts(c, c.builder, c.context, val, 
            TupleArrayType(typ.data) if is_tuple_array else typ)
        n_elems = cgutils.pack_array(c.builder, [c.builder.extract_value(
            kbgoc__syg, i) for i in range(1, kbgoc__syg.type.count)], lir.
            IntType(64))
    zfwkc__hny, data_tup, null_bitmap_ptr = construct_struct_array(c.
        context, c.builder, typ, n_structs, n_elems, c)
    if qzkol__dkda:
        wbnb__ycbk, bpxd__avp, wjdzg__snfm = _get_C_API_ptrs(c, data_tup,
            typ.data, typ.names)
        wvvq__nfiuw = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1)])
        lnd__bvo = cgutils.get_or_insert_function(c.builder.module,
            wvvq__nfiuw, name='struct_array_from_sequence')
        c.builder.call(lnd__bvo, [val, c.context.get_constant(types.int32,
            len(typ.data)), c.builder.bitcast(wbnb__ycbk, lir.IntType(8).
            as_pointer()), null_bitmap_ptr, c.builder.bitcast(bpxd__avp,
            lir.IntType(8).as_pointer()), c.builder.bitcast(wjdzg__snfm,
            lir.IntType(8).as_pointer()), c.context.get_constant(types.
            bool_, is_tuple_array)])
    else:
        _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
            null_bitmap_ptr, is_tuple_array)
    gvt__kjpwr = c.context.make_helper(c.builder, typ)
    gvt__kjpwr.meminfo = zfwkc__hny
    kep__jxwed = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(gvt__kjpwr._getvalue(), is_error=kep__jxwed)


def _unbox_struct_array_generic(typ, val, c, n_structs, data_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    kcewk__kjo = context.insert_const_string(builder.module, 'pandas')
    adtdm__gvyr = c.pyapi.import_module_noblock(kcewk__kjo)
    ugu__vkm = c.pyapi.object_getattr_string(adtdm__gvyr, 'NA')
    with cgutils.for_range(builder, n_structs) as lis__rbz:
        cuat__xauzj = lis__rbz.index
        vqh__jwoai = seq_getitem(builder, context, val, cuat__xauzj)
        set_bitmap_bit(builder, null_bitmap_ptr, cuat__xauzj, 0)
        for dgduq__lbh in range(len(typ.data)):
            arr_typ = typ.data[dgduq__lbh]
            data_arr = builder.extract_value(data_tup, dgduq__lbh)

            def set_na(data_arr, i):
                bodo.libs.array_kernels.setna(data_arr, i)
            sig = types.none(arr_typ, types.int64)
            zmmno__lawao, bid__bmz = c.pyapi.call_jit_code(set_na, sig, [
                data_arr, cuat__xauzj])
        auyq__ekt = is_na_value(builder, context, vqh__jwoai, ugu__vkm)
        byee__tunct = builder.icmp_unsigned('!=', auyq__ekt, lir.Constant(
            auyq__ekt.type, 1))
        with builder.if_then(byee__tunct):
            set_bitmap_bit(builder, null_bitmap_ptr, cuat__xauzj, 1)
            for dgduq__lbh in range(len(typ.data)):
                arr_typ = typ.data[dgduq__lbh]
                if is_tuple_array:
                    lem__pfmd = c.pyapi.tuple_getitem(vqh__jwoai, dgduq__lbh)
                else:
                    lem__pfmd = c.pyapi.dict_getitem_string(vqh__jwoai, typ
                        .names[dgduq__lbh])
                auyq__ekt = is_na_value(builder, context, lem__pfmd, ugu__vkm)
                byee__tunct = builder.icmp_unsigned('!=', auyq__ekt, lir.
                    Constant(auyq__ekt.type, 1))
                with builder.if_then(byee__tunct):
                    lem__pfmd = to_arr_obj_if_list_obj(c, context, builder,
                        lem__pfmd, arr_typ.dtype)
                    field_val = c.pyapi.to_native_value(arr_typ.dtype,
                        lem__pfmd).value
                    data_arr = builder.extract_value(data_tup, dgduq__lbh)

                    def set_data(data_arr, i, field_val):
                        data_arr[i] = field_val
                    sig = types.none(arr_typ, types.int64, arr_typ.dtype)
                    zmmno__lawao, bid__bmz = c.pyapi.call_jit_code(set_data,
                        sig, [data_arr, cuat__xauzj, field_val])
                    c.context.nrt.decref(builder, arr_typ.dtype, field_val)
        c.pyapi.decref(vqh__jwoai)
    c.pyapi.decref(adtdm__gvyr)
    c.pyapi.decref(ugu__vkm)


def _get_struct_arr_payload(context, builder, arr_typ, arr):
    gvt__kjpwr = context.make_helper(builder, arr_typ, arr)
    payload_type = StructArrayPayloadType(arr_typ.data)
    skhlk__awfsx = context.nrt.meminfo_data(builder, gvt__kjpwr.meminfo)
    ygn__hqu = builder.bitcast(skhlk__awfsx, context.get_value_type(
        payload_type).as_pointer())
    lqvpd__ycxij = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(ygn__hqu))
    return lqvpd__ycxij


@box(StructArrayType)
def box_struct_arr(typ, val, c, is_tuple_array=False):
    lqvpd__ycxij = _get_struct_arr_payload(c.context, c.builder, typ, val)
    zmmno__lawao, length = c.pyapi.call_jit_code(lambda A: len(A), types.
        int64(typ), [val])
    null_bitmap_ptr = c.context.make_helper(c.builder, types.Array(types.
        uint8, 1, 'C'), lqvpd__ycxij.null_bitmap).data
    qzkol__dkda = all(isinstance(mlhzi__lgnn, types.Array) and (mlhzi__lgnn
        .dtype in (types.int64, types.float64, types.bool_,
        datetime_date_type) or isinstance(mlhzi__lgnn.dtype, TimeType)) for
        mlhzi__lgnn in typ.data)
    if qzkol__dkda:
        wbnb__ycbk, bpxd__avp, wjdzg__snfm = _get_C_API_ptrs(c,
            lqvpd__ycxij.data, typ.data, typ.names)
        wvvq__nfiuw = lir.FunctionType(c.context.get_argument_type(types.
            pyobject), [lir.IntType(64), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1)])
        rtma__hels = cgutils.get_or_insert_function(c.builder.module,
            wvvq__nfiuw, name='np_array_from_struct_array')
        arr = c.builder.call(rtma__hels, [length, c.context.get_constant(
            types.int32, len(typ.data)), c.builder.bitcast(wbnb__ycbk, lir.
            IntType(8).as_pointer()), null_bitmap_ptr, c.builder.bitcast(
            bpxd__avp, lir.IntType(8).as_pointer()), c.builder.bitcast(
            wjdzg__snfm, lir.IntType(8).as_pointer()), c.context.
            get_constant(types.bool_, is_tuple_array)])
    else:
        arr = _box_struct_array_generic(typ, c, length, lqvpd__ycxij.data,
            null_bitmap_ptr, is_tuple_array)
    c.context.nrt.decref(c.builder, typ, val)
    return arr


def _box_struct_array_generic(typ, c, length, data_arrs_tup,
    null_bitmap_ptr, is_tuple_array=False):
    context = c.context
    builder = c.builder
    kcewk__kjo = context.insert_const_string(builder.module, 'numpy')
    xmpyd__ecsn = c.pyapi.import_module_noblock(kcewk__kjo)
    xtkws__zdf = c.pyapi.object_getattr_string(xmpyd__ecsn, 'object_')
    wrac__bcfui = c.pyapi.long_from_longlong(length)
    acjmc__rzub = c.pyapi.call_method(xmpyd__ecsn, 'ndarray', (wrac__bcfui,
        xtkws__zdf))
    ilaf__ysx = c.pyapi.object_getattr_string(xmpyd__ecsn, 'nan')
    with cgutils.for_range(builder, length) as lis__rbz:
        cuat__xauzj = lis__rbz.index
        pyarray_setitem(builder, context, acjmc__rzub, cuat__xauzj, ilaf__ysx)
        cjfv__nufe = get_bitmap_bit(builder, null_bitmap_ptr, cuat__xauzj)
        uchzi__ulj = builder.icmp_unsigned('!=', cjfv__nufe, lir.Constant(
            lir.IntType(8), 0))
        with builder.if_then(uchzi__ulj):
            if is_tuple_array:
                vqh__jwoai = c.pyapi.tuple_new(len(typ.data))
            else:
                vqh__jwoai = c.pyapi.dict_new(len(typ.data))
            for i, arr_typ in enumerate(typ.data):
                if is_tuple_array:
                    c.pyapi.incref(ilaf__ysx)
                    c.pyapi.tuple_setitem(vqh__jwoai, i, ilaf__ysx)
                else:
                    c.pyapi.dict_setitem_string(vqh__jwoai, typ.names[i],
                        ilaf__ysx)
                data_arr = c.builder.extract_value(data_arrs_tup, i)
                zmmno__lawao, flyvr__bozho = c.pyapi.call_jit_code(lambda
                    data_arr, ind: not bodo.libs.array_kernels.isna(
                    data_arr, ind), types.bool_(arr_typ, types.int64), [
                    data_arr, cuat__xauzj])
                with builder.if_then(flyvr__bozho):
                    zmmno__lawao, field_val = c.pyapi.call_jit_code(lambda
                        data_arr, ind: data_arr[ind], arr_typ.dtype(arr_typ,
                        types.int64), [data_arr, cuat__xauzj])
                    ndyf__akho = c.pyapi.from_native_value(arr_typ.dtype,
                        field_val, c.env_manager)
                    if is_tuple_array:
                        c.pyapi.tuple_setitem(vqh__jwoai, i, ndyf__akho)
                    else:
                        c.pyapi.dict_setitem_string(vqh__jwoai, typ.names[i
                            ], ndyf__akho)
                        c.pyapi.decref(ndyf__akho)
            pyarray_setitem(builder, context, acjmc__rzub, cuat__xauzj,
                vqh__jwoai)
            c.pyapi.decref(vqh__jwoai)
    c.pyapi.decref(xmpyd__ecsn)
    c.pyapi.decref(xtkws__zdf)
    c.pyapi.decref(wrac__bcfui)
    c.pyapi.decref(ilaf__ysx)
    return acjmc__rzub


def _fix_nested_counts(nested_counts, struct_arr_type, nested_counts_type,
    builder):
    kkv__cfnj = bodo.utils.transform.get_type_alloc_counts(struct_arr_type) - 1
    if kkv__cfnj == 0:
        return nested_counts
    if not isinstance(nested_counts_type, types.UniTuple):
        nested_counts = cgutils.pack_array(builder, [lir.Constant(lir.
            IntType(64), -1) for akakd__ynt in range(kkv__cfnj)])
    elif nested_counts_type.count < kkv__cfnj:
        nested_counts = cgutils.pack_array(builder, [builder.extract_value(
            nested_counts, i) for i in range(nested_counts_type.count)] + [
            lir.Constant(lir.IntType(64), -1) for akakd__ynt in range(
            kkv__cfnj - nested_counts_type.count)])
    return nested_counts


@intrinsic
def pre_alloc_struct_array(typingctx, num_structs_typ, nested_counts_typ,
    dtypes_typ, names_typ=None):
    assert isinstance(num_structs_typ, types.Integer) and isinstance(dtypes_typ
        , types.BaseTuple)
    if is_overload_none(names_typ):
        names = tuple(f'f{i}' for i in range(len(dtypes_typ)))
    else:
        names = tuple(get_overload_const_str(mlhzi__lgnn) for mlhzi__lgnn in
            names_typ.types)
    anop__pjhoh = tuple(mlhzi__lgnn.instance_type for mlhzi__lgnn in
        dtypes_typ.types)
    struct_arr_type = StructArrayType(anop__pjhoh, names)

    def codegen(context, builder, sig, args):
        tqvml__mmtyt, nested_counts, akakd__ynt, akakd__ynt = args
        nested_counts_type = sig.args[1]
        nested_counts = _fix_nested_counts(nested_counts, struct_arr_type,
            nested_counts_type, builder)
        zfwkc__hny, akakd__ynt, akakd__ynt = construct_struct_array(context,
            builder, struct_arr_type, tqvml__mmtyt, nested_counts)
        gvt__kjpwr = context.make_helper(builder, struct_arr_type)
        gvt__kjpwr.meminfo = zfwkc__hny
        return gvt__kjpwr._getvalue()
    return struct_arr_type(num_structs_typ, nested_counts_typ, dtypes_typ,
        names_typ), codegen


def pre_alloc_struct_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 4 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_struct_arr_ext_pre_alloc_struct_array
    ) = pre_alloc_struct_array_equiv


class StructType(types.Type):

    def __init__(self, data, names):
        assert isinstance(data, tuple) and len(data) > 0
        assert isinstance(names, tuple) and all(isinstance(heo__jqnx, str) for
            heo__jqnx in names) and len(names) == len(data)
        self.data = data
        self.names = names
        super(StructType, self).__init__(name='StructType({}, {})'.format(
            data, names))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


class StructPayloadType(types.Type):

    def __init__(self, data):
        assert isinstance(data, tuple)
        self.data = data
        super(StructPayloadType, self).__init__(name=
            'StructPayloadType({})'.format(data))

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(StructPayloadType)
class StructPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kkg__aux = [('data', types.BaseTuple.from_types(fe_type.data)), (
            'null_bitmap', types.UniTuple(types.int8, len(fe_type.data)))]
        models.StructModel.__init__(self, dmm, fe_type, kkg__aux)


@register_model(StructType)
class StructModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = StructPayloadType(fe_type.data)
        kkg__aux = [('meminfo', types.MemInfoPointer(payload_type))]
        models.StructModel.__init__(self, dmm, fe_type, kkg__aux)


def define_struct_dtor(context, builder, struct_type, payload_type):
    prq__jaab = builder.module
    wvvq__nfiuw = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    lnd__bvo = cgutils.get_or_insert_function(prq__jaab, wvvq__nfiuw, name=
        '.dtor.struct.{}.{}.'.format(struct_type.data, struct_type.names))
    if not lnd__bvo.is_declaration:
        return lnd__bvo
    lnd__bvo.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(lnd__bvo.append_basic_block())
    lukx__hulh = lnd__bvo.args[0]
    jnttp__sztb = context.get_value_type(payload_type).as_pointer()
    nbl__brpk = builder.bitcast(lukx__hulh, jnttp__sztb)
    lqvpd__ycxij = context.make_helper(builder, payload_type, ref=nbl__brpk)
    for i in range(len(struct_type.data)):
        ppvgz__yhaoh = builder.extract_value(lqvpd__ycxij.null_bitmap, i)
        uchzi__ulj = builder.icmp_unsigned('==', ppvgz__yhaoh, lir.Constant
            (ppvgz__yhaoh.type, 1))
        with builder.if_then(uchzi__ulj):
            val = builder.extract_value(lqvpd__ycxij.data, i)
            context.nrt.decref(builder, struct_type.data[i], val)
    builder.ret_void()
    return lnd__bvo


def _get_struct_payload(context, builder, typ, struct):
    struct = context.make_helper(builder, typ, struct)
    payload_type = StructPayloadType(typ.data)
    skhlk__awfsx = context.nrt.meminfo_data(builder, struct.meminfo)
    ygn__hqu = builder.bitcast(skhlk__awfsx, context.get_value_type(
        payload_type).as_pointer())
    lqvpd__ycxij = cgutils.create_struct_proxy(payload_type)(context,
        builder, builder.load(ygn__hqu))
    return lqvpd__ycxij, ygn__hqu


@unbox(StructType)
def unbox_struct(typ, val, c):
    context = c.context
    builder = c.builder
    kcewk__kjo = context.insert_const_string(builder.module, 'pandas')
    adtdm__gvyr = c.pyapi.import_module_noblock(kcewk__kjo)
    ugu__vkm = c.pyapi.object_getattr_string(adtdm__gvyr, 'NA')
    rjb__jgppp = []
    nulls = []
    for i, mlhzi__lgnn in enumerate(typ.data):
        ndyf__akho = c.pyapi.dict_getitem_string(val, typ.names[i])
        kzi__tkhv = cgutils.alloca_once_value(c.builder, context.
            get_constant(types.uint8, 0))
        zbddk__fxy = cgutils.alloca_once_value(c.builder, cgutils.
            get_null_value(context.get_value_type(mlhzi__lgnn)))
        auyq__ekt = is_na_value(builder, context, ndyf__akho, ugu__vkm)
        uchzi__ulj = builder.icmp_unsigned('!=', auyq__ekt, lir.Constant(
            auyq__ekt.type, 1))
        with builder.if_then(uchzi__ulj):
            builder.store(context.get_constant(types.uint8, 1), kzi__tkhv)
            field_val = c.pyapi.to_native_value(mlhzi__lgnn, ndyf__akho).value
            builder.store(field_val, zbddk__fxy)
        rjb__jgppp.append(builder.load(zbddk__fxy))
        nulls.append(builder.load(kzi__tkhv))
    c.pyapi.decref(adtdm__gvyr)
    c.pyapi.decref(ugu__vkm)
    zfwkc__hny = construct_struct(context, builder, typ, rjb__jgppp, nulls)
    struct = context.make_helper(builder, typ)
    struct.meminfo = zfwkc__hny
    kep__jxwed = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(struct._getvalue(), is_error=kep__jxwed)


@box(StructType)
def box_struct(typ, val, c):
    oew__jze = c.pyapi.dict_new(len(typ.data))
    lqvpd__ycxij, akakd__ynt = _get_struct_payload(c.context, c.builder,
        typ, val)
    assert len(typ.data) > 0
    for i, val_typ in enumerate(typ.data):
        c.pyapi.dict_setitem_string(oew__jze, typ.names[i], c.pyapi.
            borrow_none())
        ppvgz__yhaoh = c.builder.extract_value(lqvpd__ycxij.null_bitmap, i)
        uchzi__ulj = c.builder.icmp_unsigned('==', ppvgz__yhaoh, lir.
            Constant(ppvgz__yhaoh.type, 1))
        with c.builder.if_then(uchzi__ulj):
            kgog__npp = c.builder.extract_value(lqvpd__ycxij.data, i)
            c.context.nrt.incref(c.builder, val_typ, kgog__npp)
            lem__pfmd = c.pyapi.from_native_value(val_typ, kgog__npp, c.
                env_manager)
            c.pyapi.dict_setitem_string(oew__jze, typ.names[i], lem__pfmd)
            c.pyapi.decref(lem__pfmd)
    c.context.nrt.decref(c.builder, typ, val)
    return oew__jze


@intrinsic
def init_struct(typingctx, data_typ, names_typ=None):
    names = tuple(get_overload_const_str(mlhzi__lgnn) for mlhzi__lgnn in
        names_typ.types)
    struct_type = StructType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, xgvm__cvk = args
        payload_type = StructPayloadType(struct_type.data)
        hhms__lztnq = context.get_value_type(payload_type)
        mlss__yfry = context.get_abi_sizeof(hhms__lztnq)
        qdbz__vgxgy = define_struct_dtor(context, builder, struct_type,
            payload_type)
        zfwkc__hny = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, mlss__yfry), qdbz__vgxgy)
        skhlk__awfsx = context.nrt.meminfo_data(builder, zfwkc__hny)
        ygn__hqu = builder.bitcast(skhlk__awfsx, hhms__lztnq.as_pointer())
        lqvpd__ycxij = cgutils.create_struct_proxy(payload_type)(context,
            builder)
        lqvpd__ycxij.data = data
        lqvpd__ycxij.null_bitmap = cgutils.pack_array(builder, [context.
            get_constant(types.uint8, 1) for akakd__ynt in range(len(
            data_typ.types))])
        builder.store(lqvpd__ycxij._getvalue(), ygn__hqu)
        context.nrt.incref(builder, data_typ, data)
        struct = context.make_helper(builder, struct_type)
        struct.meminfo = zfwkc__hny
        return struct._getvalue()
    return struct_type(data_typ, names_typ), codegen


@intrinsic
def get_struct_data(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        lqvpd__ycxij, akakd__ynt = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            lqvpd__ycxij.data)
    return types.BaseTuple.from_types(struct_typ.data)(struct_typ), codegen


@intrinsic
def get_struct_null_bitmap(typingctx, struct_typ=None):
    assert isinstance(struct_typ, StructType)

    def codegen(context, builder, sig, args):
        struct, = args
        lqvpd__ycxij, akakd__ynt = _get_struct_payload(context, builder,
            struct_typ, struct)
        return impl_ret_borrowed(context, builder, sig.return_type,
            lqvpd__ycxij.null_bitmap)
    lbn__qup = types.UniTuple(types.int8, len(struct_typ.data))
    return lbn__qup(struct_typ), codegen


@intrinsic
def set_struct_data(typingctx, struct_typ, field_ind_typ, val_typ=None):
    assert isinstance(struct_typ, StructType) and is_overload_constant_int(
        field_ind_typ)
    field_ind = get_overload_const_int(field_ind_typ)

    def codegen(context, builder, sig, args):
        struct, akakd__ynt, val = args
        lqvpd__ycxij, ygn__hqu = _get_struct_payload(context, builder,
            struct_typ, struct)
        uizq__pnc = lqvpd__ycxij.data
        jrcb__ylw = builder.insert_value(uizq__pnc, val, field_ind)
        pngl__cgxcs = types.BaseTuple.from_types(struct_typ.data)
        context.nrt.decref(builder, pngl__cgxcs, uizq__pnc)
        context.nrt.incref(builder, pngl__cgxcs, jrcb__ylw)
        lqvpd__ycxij.data = jrcb__ylw
        builder.store(lqvpd__ycxij._getvalue(), ygn__hqu)
        return context.get_dummy_value()
    return types.none(struct_typ, field_ind_typ, val_typ), codegen


def _get_struct_field_ind(struct, ind, op):
    if not is_overload_constant_str(ind):
        raise BodoError(
            'structs (from struct array) only support constant strings for {}, not {}'
            .format(op, ind))
    whi__vpyvm = get_overload_const_str(ind)
    if whi__vpyvm not in struct.names:
        raise BodoError('Field {} does not exist in struct {}'.format(
            whi__vpyvm, struct))
    return struct.names.index(whi__vpyvm)


def is_field_value_null(s, field_name):
    pass


@overload(is_field_value_null, no_unliteral=True)
def overload_is_field_value_null(s, field_name):
    field_ind = _get_struct_field_ind(s, field_name, 'element access (getitem)'
        )
    return lambda s, field_name: get_struct_null_bitmap(s)[field_ind] == 0


@overload(operator.getitem, no_unliteral=True)
def struct_getitem(struct, ind):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'element access (getitem)')
    return lambda struct, ind: get_struct_data(struct)[field_ind]


@overload(operator.setitem, no_unliteral=True)
def struct_setitem(struct, ind, val):
    if not isinstance(struct, StructType):
        return
    field_ind = _get_struct_field_ind(struct, ind, 'item assignment (setitem)')
    field_typ = struct.data[field_ind]
    return lambda struct, ind, val: set_struct_data(struct, field_ind,
        _cast(val, field_typ))


@overload(len, no_unliteral=True)
def overload_struct_arr_len(struct):
    if isinstance(struct, StructType):
        num_fields = len(struct.data)
        return lambda struct: num_fields


def construct_struct(context, builder, struct_type, values, nulls):
    payload_type = StructPayloadType(struct_type.data)
    hhms__lztnq = context.get_value_type(payload_type)
    mlss__yfry = context.get_abi_sizeof(hhms__lztnq)
    qdbz__vgxgy = define_struct_dtor(context, builder, struct_type,
        payload_type)
    zfwkc__hny = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, mlss__yfry), qdbz__vgxgy)
    skhlk__awfsx = context.nrt.meminfo_data(builder, zfwkc__hny)
    ygn__hqu = builder.bitcast(skhlk__awfsx, hhms__lztnq.as_pointer())
    lqvpd__ycxij = cgutils.create_struct_proxy(payload_type)(context, builder)
    lqvpd__ycxij.data = cgutils.pack_array(builder, values
        ) if types.is_homogeneous(*struct_type.data) else cgutils.pack_struct(
        builder, values)
    lqvpd__ycxij.null_bitmap = cgutils.pack_array(builder, nulls)
    builder.store(lqvpd__ycxij._getvalue(), ygn__hqu)
    return zfwkc__hny


@intrinsic
def struct_array_get_struct(typingctx, struct_arr_typ, ind_typ=None):
    assert isinstance(struct_arr_typ, StructArrayType) and isinstance(ind_typ,
        types.Integer)
    lczio__nfdmx = tuple(d.dtype for d in struct_arr_typ.data)
    hol__djql = StructType(lczio__nfdmx, struct_arr_typ.names)

    def codegen(context, builder, sig, args):
        ofr__yorqw, ind = args
        lqvpd__ycxij = _get_struct_arr_payload(context, builder,
            struct_arr_typ, ofr__yorqw)
        rjb__jgppp = []
        itl__fwvd = []
        for i, arr_typ in enumerate(struct_arr_typ.data):
            aidbf__sgrt = builder.extract_value(lqvpd__ycxij.data, i)
            hqj__cuzby = context.compile_internal(builder, lambda arr, ind:
                np.uint8(0) if bodo.libs.array_kernels.isna(arr, ind) else
                np.uint8(1), types.uint8(arr_typ, types.int64), [
                aidbf__sgrt, ind])
            itl__fwvd.append(hqj__cuzby)
            jdm__foqbi = cgutils.alloca_once_value(builder, context.
                get_constant_null(arr_typ.dtype))
            uchzi__ulj = builder.icmp_unsigned('==', hqj__cuzby, lir.
                Constant(hqj__cuzby.type, 1))
            with builder.if_then(uchzi__ulj):
                eccpt__xvrd = context.compile_internal(builder, lambda arr,
                    ind: arr[ind], arr_typ.dtype(arr_typ, types.int64), [
                    aidbf__sgrt, ind])
                builder.store(eccpt__xvrd, jdm__foqbi)
            rjb__jgppp.append(builder.load(jdm__foqbi))
        if isinstance(hol__djql, types.DictType):
            wunv__lmvtm = [context.insert_const_string(builder.module,
                fdy__cdbb) for fdy__cdbb in struct_arr_typ.names]
            lsk__nvb = cgutils.pack_array(builder, rjb__jgppp)
            qqwwc__nlel = cgutils.pack_array(builder, wunv__lmvtm)

            def impl(names, vals):
                d = {}
                for i, fdy__cdbb in enumerate(names):
                    d[fdy__cdbb] = vals[i]
                return d
            loc__wzg = context.compile_internal(builder, impl, hol__djql(
                types.Tuple(tuple(types.StringLiteral(fdy__cdbb) for
                fdy__cdbb in struct_arr_typ.names)), types.Tuple(
                lczio__nfdmx)), [qqwwc__nlel, lsk__nvb])
            context.nrt.decref(builder, types.BaseTuple.from_types(
                lczio__nfdmx), lsk__nvb)
            return loc__wzg
        zfwkc__hny = construct_struct(context, builder, hol__djql,
            rjb__jgppp, itl__fwvd)
        struct = context.make_helper(builder, hol__djql)
        struct.meminfo = zfwkc__hny
        return struct._getvalue()
    return hol__djql(struct_arr_typ, ind_typ), codegen


@intrinsic
def get_data(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        lqvpd__ycxij = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            lqvpd__ycxij.data)
    return types.BaseTuple.from_types(arr_typ.data)(arr_typ), codegen


@intrinsic
def get_null_bitmap(typingctx, arr_typ=None):
    assert isinstance(arr_typ, StructArrayType)

    def codegen(context, builder, sig, args):
        arr, = args
        lqvpd__ycxij = _get_struct_arr_payload(context, builder, arr_typ, arr)
        return impl_ret_borrowed(context, builder, sig.return_type,
            lqvpd__ycxij.null_bitmap)
    return types.Array(types.uint8, 1, 'C')(arr_typ), codegen


@intrinsic
def init_struct_arr(typingctx, data_typ, null_bitmap_typ, names_typ=None):
    names = tuple(get_overload_const_str(mlhzi__lgnn) for mlhzi__lgnn in
        names_typ.types)
    struct_arr_type = StructArrayType(data_typ.types, names)

    def codegen(context, builder, sig, args):
        data, qkp__ahmki, xgvm__cvk = args
        payload_type = StructArrayPayloadType(struct_arr_type.data)
        hhms__lztnq = context.get_value_type(payload_type)
        mlss__yfry = context.get_abi_sizeof(hhms__lztnq)
        qdbz__vgxgy = define_struct_arr_dtor(context, builder,
            struct_arr_type, payload_type)
        zfwkc__hny = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, mlss__yfry), qdbz__vgxgy)
        skhlk__awfsx = context.nrt.meminfo_data(builder, zfwkc__hny)
        ygn__hqu = builder.bitcast(skhlk__awfsx, hhms__lztnq.as_pointer())
        lqvpd__ycxij = cgutils.create_struct_proxy(payload_type)(context,
            builder)
        lqvpd__ycxij.data = data
        lqvpd__ycxij.null_bitmap = qkp__ahmki
        builder.store(lqvpd__ycxij._getvalue(), ygn__hqu)
        context.nrt.incref(builder, data_typ, data)
        context.nrt.incref(builder, null_bitmap_typ, qkp__ahmki)
        gvt__kjpwr = context.make_helper(builder, struct_arr_type)
        gvt__kjpwr.meminfo = zfwkc__hny
        return gvt__kjpwr._getvalue()
    return struct_arr_type(data_typ, null_bitmap_typ, names_typ), codegen


@overload(operator.getitem, no_unliteral=True)
def struct_arr_getitem(arr, ind):
    if not isinstance(arr, StructArrayType):
        return
    if isinstance(ind, types.Integer):

        def struct_arr_getitem_impl(arr, ind):
            if ind < 0:
                ind += len(arr)
            return struct_array_get_struct(arr, ind)
        return struct_arr_getitem_impl
    if ind != bodo.boolean_array:
        vmoop__avgg = len(arr.data)
        tdlxd__bzpa = 'def impl(arr, ind):\n'
        tdlxd__bzpa += '  data = get_data(arr)\n'
        tdlxd__bzpa += '  null_bitmap = get_null_bitmap(arr)\n'
        if is_list_like_index_type(ind) and ind.dtype == types.bool_:
            tdlxd__bzpa += """  out_null_bitmap = get_new_null_mask_bool_index(null_bitmap, ind, len(data[0]))
"""
        elif is_list_like_index_type(ind) and isinstance(ind.dtype, types.
            Integer):
            tdlxd__bzpa += """  out_null_bitmap = get_new_null_mask_int_index(null_bitmap, ind, len(data[0]))
"""
        elif isinstance(ind, types.SliceType):
            tdlxd__bzpa += """  out_null_bitmap = get_new_null_mask_slice_index(null_bitmap, ind, len(data[0]))
"""
        else:
            raise BodoError('invalid index {} in struct array indexing'.
                format(ind))
        tdlxd__bzpa += (
            '  return init_struct_arr(({},), out_null_bitmap, ({},))\n'.
            format(', '.join('ensure_contig_if_np(data[{}][ind])'.format(i) for
            i in range(vmoop__avgg)), ', '.join("'{}'".format(fdy__cdbb) for
            fdy__cdbb in arr.names)))
        piyu__hpjj = {}
        exec(tdlxd__bzpa, {'init_struct_arr': init_struct_arr, 'get_data':
            get_data, 'get_null_bitmap': get_null_bitmap,
            'ensure_contig_if_np': bodo.utils.conversion.
            ensure_contig_if_np, 'get_new_null_mask_bool_index': bodo.utils
            .indexing.get_new_null_mask_bool_index,
            'get_new_null_mask_int_index': bodo.utils.indexing.
            get_new_null_mask_int_index, 'get_new_null_mask_slice_index':
            bodo.utils.indexing.get_new_null_mask_slice_index}, piyu__hpjj)
        impl = piyu__hpjj['impl']
        return impl


@overload(operator.setitem, no_unliteral=True)
def struct_arr_setitem(arr, ind, val):
    if not isinstance(arr, StructArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    if isinstance(ind, types.Integer):
        vmoop__avgg = len(arr.data)
        tdlxd__bzpa = 'def impl(arr, ind, val):\n'
        tdlxd__bzpa += '  data = get_data(arr)\n'
        tdlxd__bzpa += '  null_bitmap = get_null_bitmap(arr)\n'
        tdlxd__bzpa += '  set_bit_to_arr(null_bitmap, ind, 1)\n'
        for i in range(vmoop__avgg):
            if isinstance(val, StructType):
                tdlxd__bzpa += "  if is_field_value_null(val, '{}'):\n".format(
                    arr.names[i])
                tdlxd__bzpa += (
                    '    bodo.libs.array_kernels.setna(data[{}], ind)\n'.
                    format(i))
                tdlxd__bzpa += '  else:\n'
                tdlxd__bzpa += "    data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
            else:
                tdlxd__bzpa += "  data[{}][ind] = val['{}']\n".format(i,
                    arr.names[i])
        piyu__hpjj = {}
        exec(tdlxd__bzpa, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'is_field_value_null':
            is_field_value_null}, piyu__hpjj)
        impl = piyu__hpjj['impl']
        return impl
    if isinstance(ind, types.SliceType):
        vmoop__avgg = len(arr.data)
        tdlxd__bzpa = 'def impl(arr, ind, val):\n'
        tdlxd__bzpa += '  data = get_data(arr)\n'
        tdlxd__bzpa += '  null_bitmap = get_null_bitmap(arr)\n'
        tdlxd__bzpa += '  val_data = get_data(val)\n'
        tdlxd__bzpa += '  val_null_bitmap = get_null_bitmap(val)\n'
        tdlxd__bzpa += """  setitem_slice_index_null_bits(null_bitmap, val_null_bitmap, ind, len(arr))
"""
        for i in range(vmoop__avgg):
            tdlxd__bzpa += '  data[{0}][ind] = val_data[{0}]\n'.format(i)
        piyu__hpjj = {}
        exec(tdlxd__bzpa, {'bodo': bodo, 'get_data': get_data,
            'get_null_bitmap': get_null_bitmap, 'set_bit_to_arr': bodo.libs
            .int_arr_ext.set_bit_to_arr, 'setitem_slice_index_null_bits':
            bodo.utils.indexing.setitem_slice_index_null_bits}, piyu__hpjj)
        impl = piyu__hpjj['impl']
        return impl
    raise BodoError(
        'only setitem with scalar/slice index is currently supported for struct arrays'
        )


@overload(len, no_unliteral=True)
def overload_struct_arr_len(A):
    if isinstance(A, StructArrayType):
        return lambda A: len(get_data(A)[0])


@overload_attribute(StructArrayType, 'shape')
def overload_struct_arr_shape(A):
    return lambda A: (len(get_data(A)[0]),)


@overload_attribute(StructArrayType, 'dtype')
def overload_struct_arr_dtype(A):
    return lambda A: np.object_


@overload_attribute(StructArrayType, 'ndim')
def overload_struct_arr_ndim(A):
    return lambda A: 1


@overload_attribute(StructArrayType, 'nbytes')
def overload_struct_arr_nbytes(A):
    tdlxd__bzpa = 'def impl(A):\n'
    tdlxd__bzpa += '  total_nbytes = 0\n'
    tdlxd__bzpa += '  data = get_data(A)\n'
    for i in range(len(A.data)):
        tdlxd__bzpa += f'  total_nbytes += data[{i}].nbytes\n'
    tdlxd__bzpa += '  total_nbytes += get_null_bitmap(A).nbytes\n'
    tdlxd__bzpa += '  return total_nbytes\n'
    piyu__hpjj = {}
    exec(tdlxd__bzpa, {'get_data': get_data, 'get_null_bitmap':
        get_null_bitmap}, piyu__hpjj)
    impl = piyu__hpjj['impl']
    return impl


@overload_method(StructArrayType, 'copy', no_unliteral=True)
def overload_struct_arr_copy(A):
    names = A.names

    def copy_impl(A):
        data = get_data(A)
        qkp__ahmki = get_null_bitmap(A)
        wfif__ypn = bodo.libs.struct_arr_ext.copy_arr_tup(data)
        zjlez__mwxbx = qkp__ahmki.copy()
        return init_struct_arr(wfif__ypn, zjlez__mwxbx, names)
    return copy_impl


def copy_arr_tup(arrs):
    return tuple(heo__jqnx.copy() for heo__jqnx in arrs)


@overload(copy_arr_tup, no_unliteral=True)
def copy_arr_tup_overload(arrs):
    qjhuh__svbe = arrs.count
    tdlxd__bzpa = 'def f(arrs):\n'
    tdlxd__bzpa += '  return ({},)\n'.format(','.join('arrs[{}].copy()'.
        format(i) for i in range(qjhuh__svbe)))
    piyu__hpjj = {}
    exec(tdlxd__bzpa, {}, piyu__hpjj)
    impl = piyu__hpjj['f']
    return impl
