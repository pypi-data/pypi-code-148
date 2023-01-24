import operator
import llvmlite.binding as ll
import numba
import numba.core.typing.typeof
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, impl_ret_new_ref
from numba.extending import box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import offset_type
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, _memcpy, char_arr_type, get_data_ptr, null_bitmap_arr_type, offset_arr_type, string_array_type
ll.add_symbol('array_setitem', hstr_ext.array_setitem)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
ll.add_symbol('dtor_str_arr_split_view', hstr_ext.dtor_str_arr_split_view)
ll.add_symbol('str_arr_split_view_impl', hstr_ext.str_arr_split_view_impl)
ll.add_symbol('str_arr_split_view_alloc', hstr_ext.str_arr_split_view_alloc)
char_typ = types.uint8
data_ctypes_type = types.ArrayCTypes(types.Array(char_typ, 1, 'C'))
offset_ctypes_type = types.ArrayCTypes(types.Array(offset_type, 1, 'C'))


class StringArraySplitViewType(types.ArrayCompatible):

    def __init__(self):
        super(StringArraySplitViewType, self).__init__(name=
            'StringArraySplitViewType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_array_type

    def copy(self):
        return StringArraySplitViewType()


string_array_split_view_type = StringArraySplitViewType()


class StringArraySplitViewPayloadType(types.Type):

    def __init__(self):
        super(StringArraySplitViewPayloadType, self).__init__(name=
            'StringArraySplitViewPayloadType()')


str_arr_split_view_payload_type = StringArraySplitViewPayloadType()


@register_model(StringArraySplitViewPayloadType)
class StringArrayPayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        dndv__aamyv = [('index_offsets', types.CPointer(offset_type)), (
            'data_offsets', types.CPointer(offset_type)), ('null_bitmap',
            types.CPointer(char_typ))]
        models.StructModel.__init__(self, dmm, fe_type, dndv__aamyv)


str_arr_model_members = [('num_items', types.uint64), ('index_offsets',
    types.CPointer(offset_type)), ('data_offsets', types.CPointer(
    offset_type)), ('data', data_ctypes_type), ('null_bitmap', types.
    CPointer(char_typ)), ('meminfo', types.MemInfoPointer(
    str_arr_split_view_payload_type))]


@register_model(StringArraySplitViewType)
class StringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        models.StructModel.__init__(self, dmm, fe_type, str_arr_model_members)


make_attribute_wrapper(StringArraySplitViewType, 'num_items', '_num_items')
make_attribute_wrapper(StringArraySplitViewType, 'index_offsets',
    '_index_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data_offsets',
    '_data_offsets')
make_attribute_wrapper(StringArraySplitViewType, 'data', '_data')
make_attribute_wrapper(StringArraySplitViewType, 'null_bitmap', '_null_bitmap')


def construct_str_arr_split_view(context, builder):
    hcmif__czyw = context.get_value_type(str_arr_split_view_payload_type)
    bvcwp__ekz = context.get_abi_sizeof(hcmif__czyw)
    juasz__lqol = context.get_value_type(types.voidptr)
    ghce__ekz = context.get_value_type(types.uintp)
    zkbll__insh = lir.FunctionType(lir.VoidType(), [juasz__lqol, ghce__ekz,
        juasz__lqol])
    zxnk__uzfx = cgutils.get_or_insert_function(builder.module, zkbll__insh,
        name='dtor_str_arr_split_view')
    jqyi__rju = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, bvcwp__ekz), zxnk__uzfx)
    ztymo__hqy = context.nrt.meminfo_data(builder, jqyi__rju)
    xqozl__tpl = builder.bitcast(ztymo__hqy, hcmif__czyw.as_pointer())
    return jqyi__rju, xqozl__tpl


@intrinsic
def compute_split_view(typingctx, str_arr_typ, sep_typ=None):
    assert str_arr_typ == string_array_type and isinstance(sep_typ, types.
        StringLiteral)

    def codegen(context, builder, sig, args):
        ifym__emp, wvasd__gor = args
        jqyi__rju, xqozl__tpl = construct_str_arr_split_view(context, builder)
        maho__lcn = _get_str_binary_arr_payload(context, builder, ifym__emp,
            string_array_type)
        bmph__qvd = lir.FunctionType(lir.VoidType(), [xqozl__tpl.type, lir.
            IntType(64), lir.IntType(offset_type.bitwidth).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8)])
        spclq__fvnws = cgutils.get_or_insert_function(builder.module,
            bmph__qvd, name='str_arr_split_view_impl')
        mwu__cis = context.make_helper(builder, offset_arr_type, maho__lcn.
            offsets).data
        yeji__sqr = context.make_helper(builder, char_arr_type, maho__lcn.data
            ).data
        zksf__lzg = context.make_helper(builder, null_bitmap_arr_type,
            maho__lcn.null_bitmap).data
        dcfvq__urjlh = context.get_constant(types.int8, ord(sep_typ.
            literal_value))
        builder.call(spclq__fvnws, [xqozl__tpl, maho__lcn.n_arrays,
            mwu__cis, yeji__sqr, zksf__lzg, dcfvq__urjlh])
        uypiu__ctbfz = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(xqozl__tpl))
        hzcth__vfq = context.make_helper(builder, string_array_split_view_type)
        hzcth__vfq.num_items = maho__lcn.n_arrays
        hzcth__vfq.index_offsets = uypiu__ctbfz.index_offsets
        hzcth__vfq.data_offsets = uypiu__ctbfz.data_offsets
        hzcth__vfq.data = context.compile_internal(builder, lambda S:
            get_data_ptr(S), data_ctypes_type(string_array_type), [ifym__emp])
        hzcth__vfq.null_bitmap = uypiu__ctbfz.null_bitmap
        hzcth__vfq.meminfo = jqyi__rju
        rmbxb__irbu = hzcth__vfq._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, rmbxb__irbu)
    return string_array_split_view_type(string_array_type, sep_typ), codegen


@box(StringArraySplitViewType)
def box_str_arr_split_view(typ, val, c):
    context = c.context
    builder = c.builder
    tkxs__nwkiy = context.make_helper(builder, string_array_split_view_type,
        val)
    pkyxi__vqs = context.insert_const_string(builder.module, 'numpy')
    lbfn__lrvu = c.pyapi.import_module_noblock(pkyxi__vqs)
    dtype = c.pyapi.object_getattr_string(lbfn__lrvu, 'object_')
    pqxks__ovpn = builder.sext(tkxs__nwkiy.num_items, c.pyapi.longlong)
    epwu__zvns = c.pyapi.long_from_longlong(pqxks__ovpn)
    aelga__euxiz = c.pyapi.call_method(lbfn__lrvu, 'ndarray', (epwu__zvns,
        dtype))
    ifs__fprys = lir.FunctionType(lir.IntType(8).as_pointer(), [c.pyapi.
        pyobj, c.pyapi.py_ssize_t])
    xzuyk__vhum = c.pyapi._get_function(ifs__fprys, name='array_getptr1')
    aoxgc__qsc = lir.FunctionType(lir.VoidType(), [c.pyapi.pyobj, lir.
        IntType(8).as_pointer(), c.pyapi.pyobj])
    qezi__dyaov = c.pyapi._get_function(aoxgc__qsc, name='array_setitem')
    dqos__bauco = c.pyapi.object_getattr_string(lbfn__lrvu, 'nan')
    with cgutils.for_range(builder, tkxs__nwkiy.num_items) as mjqbk__duv:
        str_ind = mjqbk__duv.index
        tzr__cfmzs = builder.sext(builder.load(builder.gep(tkxs__nwkiy.
            index_offsets, [str_ind])), lir.IntType(64))
        qmmpu__mue = builder.sext(builder.load(builder.gep(tkxs__nwkiy.
            index_offsets, [builder.add(str_ind, str_ind.type(1))])), lir.
            IntType(64))
        xfdvf__ijk = builder.lshr(str_ind, lir.Constant(lir.IntType(64), 3))
        qak__cdbg = builder.gep(tkxs__nwkiy.null_bitmap, [xfdvf__ijk])
        vecuf__epev = builder.load(qak__cdbg)
        xeu__qxvz = builder.trunc(builder.and_(str_ind, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = builder.and_(builder.lshr(vecuf__epev, xeu__qxvz), lir.
            Constant(lir.IntType(8), 1))
        epxn__ybqi = builder.sub(qmmpu__mue, tzr__cfmzs)
        epxn__ybqi = builder.sub(epxn__ybqi, epxn__ybqi.type(1))
        tvaqh__jpsz = builder.call(xzuyk__vhum, [aelga__euxiz, str_ind])
        bnx__jvidc = c.builder.icmp_unsigned('!=', val, val.type(0))
        with c.builder.if_else(bnx__jvidc) as (ezxzy__qziky, pot__ubhv):
            with ezxzy__qziky:
                gpt__szj = c.pyapi.list_new(epxn__ybqi)
                with c.builder.if_then(cgutils.is_not_null(c.builder,
                    gpt__szj), likely=True):
                    with cgutils.for_range(c.builder, epxn__ybqi
                        ) as mjqbk__duv:
                        eqjl__lpo = builder.add(tzr__cfmzs, mjqbk__duv.index)
                        data_start = builder.load(builder.gep(tkxs__nwkiy.
                            data_offsets, [eqjl__lpo]))
                        data_start = builder.add(data_start, data_start.type(1)
                            )
                        crnqc__xpvy = builder.load(builder.gep(tkxs__nwkiy.
                            data_offsets, [builder.add(eqjl__lpo, eqjl__lpo
                            .type(1))]))
                        wccn__plem = builder.gep(builder.extract_value(
                            tkxs__nwkiy.data, 0), [data_start])
                        okds__gii = builder.sext(builder.sub(crnqc__xpvy,
                            data_start), lir.IntType(64))
                        wut__zfpo = c.pyapi.string_from_string_and_size(
                            wccn__plem, okds__gii)
                        c.pyapi.list_setitem(gpt__szj, mjqbk__duv.index,
                            wut__zfpo)
                builder.call(qezi__dyaov, [aelga__euxiz, tvaqh__jpsz, gpt__szj]
                    )
            with pot__ubhv:
                builder.call(qezi__dyaov, [aelga__euxiz, tvaqh__jpsz,
                    dqos__bauco])
    c.pyapi.decref(lbfn__lrvu)
    c.pyapi.decref(dtype)
    c.pyapi.decref(dqos__bauco)
    return aelga__euxiz


@intrinsic
def pre_alloc_str_arr_view(typingctx, num_items_t, num_offsets_t, data_t=None):
    assert num_items_t == types.intp and num_offsets_t == types.intp

    def codegen(context, builder, sig, args):
        vhd__yqu, ychpt__oxsm, wccn__plem = args
        jqyi__rju, xqozl__tpl = construct_str_arr_split_view(context, builder)
        bmph__qvd = lir.FunctionType(lir.VoidType(), [xqozl__tpl.type, lir.
            IntType(64), lir.IntType(64)])
        spclq__fvnws = cgutils.get_or_insert_function(builder.module,
            bmph__qvd, name='str_arr_split_view_alloc')
        builder.call(spclq__fvnws, [xqozl__tpl, vhd__yqu, ychpt__oxsm])
        uypiu__ctbfz = cgutils.create_struct_proxy(
            str_arr_split_view_payload_type)(context, builder, value=
            builder.load(xqozl__tpl))
        hzcth__vfq = context.make_helper(builder, string_array_split_view_type)
        hzcth__vfq.num_items = vhd__yqu
        hzcth__vfq.index_offsets = uypiu__ctbfz.index_offsets
        hzcth__vfq.data_offsets = uypiu__ctbfz.data_offsets
        hzcth__vfq.data = wccn__plem
        hzcth__vfq.null_bitmap = uypiu__ctbfz.null_bitmap
        context.nrt.incref(builder, data_t, wccn__plem)
        hzcth__vfq.meminfo = jqyi__rju
        rmbxb__irbu = hzcth__vfq._getvalue()
        return impl_ret_new_ref(context, builder,
            string_array_split_view_type, rmbxb__irbu)
    return string_array_split_view_type(types.intp, types.intp, data_t
        ), codegen


@intrinsic
def get_c_arr_ptr(typingctx, c_arr, ind_t=None):
    assert isinstance(c_arr, (types.CPointer, types.ArrayCTypes))

    def codegen(context, builder, sig, args):
        amovc__hui, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            amovc__hui = builder.extract_value(amovc__hui, 0)
        return builder.bitcast(builder.gep(amovc__hui, [ind]), lir.IntType(
            8).as_pointer())
    return types.voidptr(c_arr, ind_t), codegen


@intrinsic
def getitem_c_arr(typingctx, c_arr, ind_t=None):

    def codegen(context, builder, sig, args):
        amovc__hui, ind = args
        if isinstance(sig.args[0], types.ArrayCTypes):
            amovc__hui = builder.extract_value(amovc__hui, 0)
        return builder.load(builder.gep(amovc__hui, [ind]))
    return c_arr.dtype(c_arr, ind_t), codegen


@intrinsic
def setitem_c_arr(typingctx, c_arr, ind_t, item_t=None):

    def codegen(context, builder, sig, args):
        amovc__hui, ind, msb__rfucw = args
        fis__plt = builder.gep(amovc__hui, [ind])
        builder.store(msb__rfucw, fis__plt)
    return types.void(c_arr, ind_t, c_arr.dtype), codegen


@intrinsic
def get_array_ctypes_ptr(typingctx, arr_ctypes_t, ind_t=None):

    def codegen(context, builder, sig, args):
        rcc__bik, ind = args
        yvzn__dhqhv = context.make_helper(builder, arr_ctypes_t, rcc__bik)
        lpuyu__gnhue = context.make_helper(builder, arr_ctypes_t)
        lpuyu__gnhue.data = builder.gep(yvzn__dhqhv.data, [ind])
        lpuyu__gnhue.meminfo = yvzn__dhqhv.meminfo
        gofw__wnb = lpuyu__gnhue._getvalue()
        return impl_ret_borrowed(context, builder, arr_ctypes_t, gofw__wnb)
    return arr_ctypes_t(arr_ctypes_t, ind_t), codegen


@numba.njit(no_cpython_wrapper=True)
def get_split_view_index(arr, item_ind, str_ind):
    fotui__syk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr._null_bitmap,
        item_ind)
    if not fotui__syk:
        return 0, 0, 0
    eqjl__lpo = getitem_c_arr(arr._index_offsets, item_ind)
    wpfnc__njbug = getitem_c_arr(arr._index_offsets, item_ind + 1) - 1
    wxodg__yfcm = wpfnc__njbug - eqjl__lpo
    if str_ind >= wxodg__yfcm:
        return 0, 0, 0
    data_start = getitem_c_arr(arr._data_offsets, eqjl__lpo + str_ind)
    data_start += 1
    if eqjl__lpo + str_ind == 0:
        data_start = 0
    crnqc__xpvy = getitem_c_arr(arr._data_offsets, eqjl__lpo + str_ind + 1)
    kqch__bwwh = crnqc__xpvy - data_start
    return 1, data_start, kqch__bwwh


@numba.njit(no_cpython_wrapper=True)
def get_split_view_data_ptr(arr, data_start):
    return get_array_ctypes_ptr(arr._data, data_start)


@overload(len, no_unliteral=True)
def str_arr_split_view_len_overload(arr):
    if arr == string_array_split_view_type:
        return lambda arr: np.int64(arr._num_items)


@overload_attribute(StringArraySplitViewType, 'shape')
def overload_split_view_arr_shape(A):
    return lambda A: (np.int64(A._num_items),)


@overload(operator.getitem, no_unliteral=True)
def str_arr_split_view_getitem_overload(A, ind):
    if A != string_array_split_view_type:
        return
    if A == string_array_split_view_type and isinstance(ind, types.Integer):
        ervuk__efdqw = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def _impl(A, ind):
            eqjl__lpo = getitem_c_arr(A._index_offsets, ind)
            wpfnc__njbug = getitem_c_arr(A._index_offsets, ind + 1)
            mqep__czxv = wpfnc__njbug - eqjl__lpo - 1
            ifym__emp = bodo.libs.str_arr_ext.pre_alloc_string_array(mqep__czxv
                , -1)
            for aydx__mwlk in range(mqep__czxv):
                data_start = getitem_c_arr(A._data_offsets, eqjl__lpo +
                    aydx__mwlk)
                data_start += 1
                if eqjl__lpo + aydx__mwlk == 0:
                    data_start = 0
                crnqc__xpvy = getitem_c_arr(A._data_offsets, eqjl__lpo +
                    aydx__mwlk + 1)
                kqch__bwwh = crnqc__xpvy - data_start
                fis__plt = get_array_ctypes_ptr(A._data, data_start)
                hzen__kjqua = bodo.libs.str_arr_ext.decode_utf8(fis__plt,
                    kqch__bwwh)
                ifym__emp[aydx__mwlk] = hzen__kjqua
            return ifym__emp
        return _impl
    if A == string_array_split_view_type and ind == types.Array(types.bool_,
        1, 'C'):
        axt__kds = offset_type.bitwidth // 8

        def _impl(A, ind):
            mqep__czxv = len(A)
            if mqep__czxv != len(ind):
                raise IndexError(
                    'boolean index did not match indexed array along dimension 0'
                    )
            vhd__yqu = 0
            ychpt__oxsm = 0
            for aydx__mwlk in range(mqep__czxv):
                if ind[aydx__mwlk]:
                    vhd__yqu += 1
                    eqjl__lpo = getitem_c_arr(A._index_offsets, aydx__mwlk)
                    wpfnc__njbug = getitem_c_arr(A._index_offsets, 
                        aydx__mwlk + 1)
                    ychpt__oxsm += wpfnc__njbug - eqjl__lpo
            aelga__euxiz = pre_alloc_str_arr_view(vhd__yqu, ychpt__oxsm, A.
                _data)
            item_ind = 0
            rlv__vtgfn = 0
            for aydx__mwlk in range(mqep__czxv):
                if ind[aydx__mwlk]:
                    eqjl__lpo = getitem_c_arr(A._index_offsets, aydx__mwlk)
                    wpfnc__njbug = getitem_c_arr(A._index_offsets, 
                        aydx__mwlk + 1)
                    xpe__oii = wpfnc__njbug - eqjl__lpo
                    setitem_c_arr(aelga__euxiz._index_offsets, item_ind,
                        rlv__vtgfn)
                    fis__plt = get_c_arr_ptr(A._data_offsets, eqjl__lpo)
                    bigky__mtv = get_c_arr_ptr(aelga__euxiz._data_offsets,
                        rlv__vtgfn)
                    _memcpy(bigky__mtv, fis__plt, xpe__oii, axt__kds)
                    fotui__syk = bodo.libs.int_arr_ext.get_bit_bitmap_arr(A
                        ._null_bitmap, aydx__mwlk)
                    bodo.libs.int_arr_ext.set_bit_to_arr(aelga__euxiz.
                        _null_bitmap, item_ind, fotui__syk)
                    item_ind += 1
                    rlv__vtgfn += xpe__oii
            setitem_c_arr(aelga__euxiz._index_offsets, item_ind, rlv__vtgfn)
            return aelga__euxiz
        return _impl
