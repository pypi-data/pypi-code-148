"""Nullable boolean array that stores data in Numpy format (1 byte per value)
but nulls are stored in bit arrays (1 bit per value) similar to Arrow's nulls.
Pandas converts boolean array to object when NAs are introduced.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import NativeValue, box, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hstr_ext
from bodo.libs.str_arr_ext import string_array_type
from bodo.utils.typing import is_list_like_index_type
ll.add_symbol('is_bool_array', hstr_ext.is_bool_array)
ll.add_symbol('is_pd_boolean_array', hstr_ext.is_pd_boolean_array)
ll.add_symbol('unbox_bool_array_obj', hstr_ext.unbox_bool_array_obj)
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, is_iterable_type, is_overload_false, is_overload_true, parse_dtype, raise_bodo_error


class BooleanArrayType(types.ArrayCompatible):

    def __init__(self):
        super(BooleanArrayType, self).__init__(name='BooleanArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return types.bool_

    def copy(self):
        return BooleanArrayType()


boolean_array = BooleanArrayType()


@typeof_impl.register(pd.arrays.BooleanArray)
def typeof_boolean_array(val, c):
    return boolean_array


data_type = types.Array(types.bool_, 1, 'C')
nulls_type = types.Array(types.uint8, 1, 'C')


@register_model(BooleanArrayType)
class BooleanArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ivstz__yegtp = [('data', data_type), ('null_bitmap', nulls_type)]
        models.StructModel.__init__(self, dmm, fe_type, ivstz__yegtp)


make_attribute_wrapper(BooleanArrayType, 'data', '_data')
make_attribute_wrapper(BooleanArrayType, 'null_bitmap', '_null_bitmap')


class BooleanDtype(types.Number):

    def __init__(self):
        self.dtype = types.bool_
        super(BooleanDtype, self).__init__('BooleanDtype')


boolean_dtype = BooleanDtype()
register_model(BooleanDtype)(models.OpaqueModel)


@box(BooleanDtype)
def box_boolean_dtype(typ, val, c):
    dnkbi__tfq = c.context.insert_const_string(c.builder.module, 'pandas')
    wqwvr__tbv = c.pyapi.import_module_noblock(dnkbi__tfq)
    fine__efxoi = c.pyapi.call_method(wqwvr__tbv, 'BooleanDtype', ())
    c.pyapi.decref(wqwvr__tbv)
    return fine__efxoi


@unbox(BooleanDtype)
def unbox_boolean_dtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


typeof_impl.register(pd.BooleanDtype)(lambda a, b: boolean_dtype)
type_callable(pd.BooleanDtype)(lambda c: lambda : boolean_dtype)
lower_builtin(pd.BooleanDtype)(lambda c, b, s, a: c.get_dummy_value())


@numba.njit
def gen_full_bitmap(n):
    xkyyu__bgw = n + 7 >> 3
    return np.full(xkyyu__bgw, 255, np.uint8)


def call_func_in_unbox(func, args, arg_typs, c):
    ybtdd__eccnh = c.context.typing_context.resolve_value_type(func)
    hwn__muws = ybtdd__eccnh.get_call_type(c.context.typing_context,
        arg_typs, {})
    opqg__eqiy = c.context.get_function(ybtdd__eccnh, hwn__muws)
    vftpj__wwnqc = c.context.call_conv.get_function_type(hwn__muws.
        return_type, hwn__muws.args)
    syr__pvxg = c.builder.module
    ltjk__uwa = lir.Function(syr__pvxg, vftpj__wwnqc, name=syr__pvxg.
        get_unique_name('.func_conv'))
    ltjk__uwa.linkage = 'internal'
    ebk__fsjx = lir.IRBuilder(ltjk__uwa.append_basic_block())
    skqdz__uvy = c.context.call_conv.decode_arguments(ebk__fsjx, hwn__muws.
        args, ltjk__uwa)
    nrt__nmga = opqg__eqiy(ebk__fsjx, skqdz__uvy)
    c.context.call_conv.return_value(ebk__fsjx, nrt__nmga)
    rvj__ufpbc, nmxim__notgv = c.context.call_conv.call_function(c.builder,
        ltjk__uwa, hwn__muws.return_type, hwn__muws.args, args)
    return nmxim__notgv


@unbox(BooleanArrayType)
def unbox_bool_array(typ, obj, c):
    baa__ghdqi = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(baa__ghdqi)
    c.pyapi.decref(baa__ghdqi)
    vftpj__wwnqc = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    memg__lqy = cgutils.get_or_insert_function(c.builder.module,
        vftpj__wwnqc, name='is_bool_array')
    vftpj__wwnqc = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
        as_pointer()])
    ltjk__uwa = cgutils.get_or_insert_function(c.builder.module,
        vftpj__wwnqc, name='is_pd_boolean_array')
    ocv__auw = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    clnm__nbim = c.builder.call(ltjk__uwa, [obj])
    mbmki__mzeeq = c.builder.icmp_unsigned('!=', clnm__nbim, clnm__nbim.type(0)
        )
    with c.builder.if_else(mbmki__mzeeq) as (ffmwt__yukg, wun__ijux):
        with ffmwt__yukg:
            qrzsx__twxr = c.pyapi.object_getattr_string(obj, '_data')
            ocv__auw.data = c.pyapi.to_native_value(types.Array(types.bool_,
                1, 'C'), qrzsx__twxr).value
            pcd__ptu = c.pyapi.object_getattr_string(obj, '_mask')
            dytgp__aph = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), pcd__ptu).value
            xkyyu__bgw = c.builder.udiv(c.builder.add(n, lir.Constant(lir.
                IntType(64), 7)), lir.Constant(lir.IntType(64), 8))
            bhxie__tcf = c.context.make_array(types.Array(types.bool_, 1, 'C')
                )(c.context, c.builder, dytgp__aph)
            kup__dgkk = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(types.uint8, 1, 'C'), [xkyyu__bgw])
            vftpj__wwnqc = lir.FunctionType(lir.VoidType(), [lir.IntType(8)
                .as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            ltjk__uwa = cgutils.get_or_insert_function(c.builder.module,
                vftpj__wwnqc, name='mask_arr_to_bitmap')
            c.builder.call(ltjk__uwa, [kup__dgkk.data, bhxie__tcf.data, n])
            ocv__auw.null_bitmap = kup__dgkk._getvalue()
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), dytgp__aph)
            c.pyapi.decref(qrzsx__twxr)
            c.pyapi.decref(pcd__ptu)
        with wun__ijux:
            zecqs__sxgd = c.builder.call(memg__lqy, [obj])
            mdot__adja = c.builder.icmp_unsigned('!=', zecqs__sxgd,
                zecqs__sxgd.type(0))
            with c.builder.if_else(mdot__adja) as (klcs__xtuvt, jscnc__jldip):
                with klcs__xtuvt:
                    ocv__auw.data = c.pyapi.to_native_value(types.Array(
                        types.bool_, 1, 'C'), obj).value
                    ocv__auw.null_bitmap = call_func_in_unbox(gen_full_bitmap,
                        (n,), (types.int64,), c)
                with jscnc__jldip:
                    ocv__auw.data = bodo.utils.utils._empty_nd_impl(c.
                        context, c.builder, types.Array(types.bool_, 1, 'C'
                        ), [n])._getvalue()
                    xkyyu__bgw = c.builder.udiv(c.builder.add(n, lir.
                        Constant(lir.IntType(64), 7)), lir.Constant(lir.
                        IntType(64), 8))
                    ocv__auw.null_bitmap = bodo.utils.utils._empty_nd_impl(c
                        .context, c.builder, types.Array(types.uint8, 1,
                        'C'), [xkyyu__bgw])._getvalue()
                    jixz__hxl = c.context.make_array(types.Array(types.
                        bool_, 1, 'C'))(c.context, c.builder, ocv__auw.data
                        ).data
                    uyy__elfas = c.context.make_array(types.Array(types.
                        uint8, 1, 'C'))(c.context, c.builder, ocv__auw.
                        null_bitmap).data
                    vftpj__wwnqc = lir.FunctionType(lir.VoidType(), [lir.
                        IntType(8).as_pointer(), lir.IntType(8).as_pointer(
                        ), lir.IntType(8).as_pointer(), lir.IntType(64)])
                    ltjk__uwa = cgutils.get_or_insert_function(c.builder.
                        module, vftpj__wwnqc, name='unbox_bool_array_obj')
                    c.builder.call(ltjk__uwa, [obj, jixz__hxl, uyy__elfas, n])
    return NativeValue(ocv__auw._getvalue())


@box(BooleanArrayType)
def box_bool_arr(typ, val, c):
    ocv__auw = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        ocv__auw.data, c.env_manager)
    iqdg__skvpx = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, ocv__auw.null_bitmap).data
    baa__ghdqi = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(baa__ghdqi)
    dnkbi__tfq = c.context.insert_const_string(c.builder.module, 'numpy')
    ekzy__cruu = c.pyapi.import_module_noblock(dnkbi__tfq)
    hwwp__hzbey = c.pyapi.object_getattr_string(ekzy__cruu, 'bool_')
    dytgp__aph = c.pyapi.call_method(ekzy__cruu, 'empty', (baa__ghdqi,
        hwwp__hzbey))
    nce__yfv = c.pyapi.object_getattr_string(dytgp__aph, 'ctypes')
    kfeo__pjc = c.pyapi.object_getattr_string(nce__yfv, 'data')
    znw__ajss = c.builder.inttoptr(c.pyapi.long_as_longlong(kfeo__pjc), lir
        .IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as bflbf__ajuw:
        jodlh__uxu = bflbf__ajuw.index
        gkjxh__crqfq = c.builder.lshr(jodlh__uxu, lir.Constant(lir.IntType(
            64), 3))
        oed__gornr = c.builder.load(cgutils.gep(c.builder, iqdg__skvpx,
            gkjxh__crqfq))
        nesrj__gehk = c.builder.trunc(c.builder.and_(jodlh__uxu, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(oed__gornr, nesrj__gehk), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        nyjol__kkkn = cgutils.gep(c.builder, znw__ajss, jodlh__uxu)
        c.builder.store(val, nyjol__kkkn)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        ocv__auw.null_bitmap)
    dnkbi__tfq = c.context.insert_const_string(c.builder.module, 'pandas')
    wqwvr__tbv = c.pyapi.import_module_noblock(dnkbi__tfq)
    aspt__voit = c.pyapi.object_getattr_string(wqwvr__tbv, 'arrays')
    fine__efxoi = c.pyapi.call_method(aspt__voit, 'BooleanArray', (data,
        dytgp__aph))
    c.pyapi.decref(wqwvr__tbv)
    c.pyapi.decref(baa__ghdqi)
    c.pyapi.decref(ekzy__cruu)
    c.pyapi.decref(hwwp__hzbey)
    c.pyapi.decref(nce__yfv)
    c.pyapi.decref(kfeo__pjc)
    c.pyapi.decref(aspt__voit)
    c.pyapi.decref(data)
    c.pyapi.decref(dytgp__aph)
    return fine__efxoi


@lower_constant(BooleanArrayType)
def lower_constant_bool_arr(context, builder, typ, pyval):
    n = len(pyval)
    vyat__oypu = np.empty(n, np.bool_)
    gxnf__wsbuj = np.empty(n + 7 >> 3, np.uint8)
    for jodlh__uxu, s in enumerate(pyval):
        zuips__jtl = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(gxnf__wsbuj, jodlh__uxu, int(
            not zuips__jtl))
        if not zuips__jtl:
            vyat__oypu[jodlh__uxu] = s
    rwdp__xsf = context.get_constant_generic(builder, data_type, vyat__oypu)
    qzk__rjh = context.get_constant_generic(builder, nulls_type, gxnf__wsbuj)
    return lir.Constant.literal_struct([rwdp__xsf, qzk__rjh])


def lower_init_bool_array(context, builder, signature, args):
    utfb__ulsnw, ksbpu__soz = args
    ocv__auw = cgutils.create_struct_proxy(signature.return_type)(context,
        builder)
    ocv__auw.data = utfb__ulsnw
    ocv__auw.null_bitmap = ksbpu__soz
    context.nrt.incref(builder, signature.args[0], utfb__ulsnw)
    context.nrt.incref(builder, signature.args[1], ksbpu__soz)
    return ocv__auw._getvalue()


@intrinsic
def init_bool_array(typingctx, data, null_bitmap=None):
    assert data == types.Array(types.bool_, 1, 'C')
    assert null_bitmap == types.Array(types.uint8, 1, 'C')
    sig = boolean_array(data, null_bitmap)
    return sig, lower_init_bool_array


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_bool_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_bool_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    ouznu__nlqjr = args[0]
    if equiv_set.has_shape(ouznu__nlqjr):
        return ArrayAnalysis.AnalyzeResult(shape=ouznu__nlqjr, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_get_bool_arr_data = (
    get_bool_arr_data_equiv)


def init_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    ouznu__nlqjr = args[0]
    if equiv_set.has_shape(ouznu__nlqjr):
        return ArrayAnalysis.AnalyzeResult(shape=ouznu__nlqjr, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_init_bool_array = (
    init_bool_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_bool_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_bool_array',
    'bodo.libs.bool_arr_ext'] = alias_ext_init_bool_array
numba.core.ir_utils.alias_func_extensions['get_bool_arr_data',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_bool_arr_bitmap',
    'bodo.libs.bool_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_bool_array(n):
    vyat__oypu = np.empty(n, dtype=np.bool_)
    lwj__fedd = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_bool_array(vyat__oypu, lwj__fedd)


def alloc_bool_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_bool_arr_ext_alloc_bool_array = (
    alloc_bool_array_equiv)


@overload(operator.getitem, no_unliteral=True)
def bool_arr_getitem(A, ind):
    if A != boolean_array:
        return
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda A, ind: A._data[ind]
    if ind != boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            ziyi__jbn, etrx__ffe = array_getitem_bool_index(A, ind)
            return init_bool_array(ziyi__jbn, etrx__ffe)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            ziyi__jbn, etrx__ffe = array_getitem_int_index(A, ind)
            return init_bool_array(ziyi__jbn, etrx__ffe)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            ziyi__jbn, etrx__ffe = array_getitem_slice_index(A, ind)
            return init_bool_array(ziyi__jbn, etrx__ffe)
        return impl_slice
    if ind != boolean_array:
        raise BodoError(
            f'getitem for BooleanArray with indexing type {ind} not supported.'
            )


@overload(operator.setitem, no_unliteral=True)
def bool_arr_setitem(A, idx, val):
    if A != boolean_array:
        return
    if val == types.none or isinstance(val, types.optional):
        return
    oxh__oxd = (
        f"setitem for BooleanArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    if isinstance(idx, types.Integer):
        if types.unliteral(val) == types.bool_:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(oxh__oxd)
    if not (is_iterable_type(val) and val.dtype == types.bool_ or types.
        unliteral(val) == types.bool_):
        raise BodoError(oxh__oxd)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, types.Integer):

        def impl_arr_ind_mask(A, idx, val):
            array_setitem_int_index(A, idx, val)
        return impl_arr_ind_mask
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:

        def impl_bool_ind_mask(A, idx, val):
            array_setitem_bool_index(A, idx, val)
        return impl_bool_ind_mask
    if isinstance(idx, types.SliceType):

        def impl_slice_mask(A, idx, val):
            array_setitem_slice_index(A, idx, val)
        return impl_slice_mask
    raise BodoError(
        f'setitem for BooleanArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_bool_arr_len(A):
    if A == boolean_array:
        return lambda A: len(A._data)


@overload_attribute(BooleanArrayType, 'size')
def overload_bool_arr_size(A):
    return lambda A: len(A._data)


@overload_attribute(BooleanArrayType, 'shape')
def overload_bool_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(BooleanArrayType, 'dtype')
def overload_bool_arr_dtype(A):
    return lambda A: pd.BooleanDtype()


@overload_attribute(BooleanArrayType, 'ndim')
def overload_bool_arr_ndim(A):
    return lambda A: 1


@overload_attribute(BooleanArrayType, 'nbytes')
def bool_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(BooleanArrayType, 'copy', no_unliteral=True)
def overload_bool_arr_copy(A):
    return lambda A: bodo.libs.bool_arr_ext.init_bool_array(bodo.libs.
        bool_arr_ext.get_bool_arr_data(A).copy(), bodo.libs.bool_arr_ext.
        get_bool_arr_bitmap(A).copy())


@overload_method(BooleanArrayType, 'sum', no_unliteral=True, inline='always')
def overload_bool_sum(A):

    def impl(A):
        numba.parfors.parfor.init_prange()
        s = 0
        for jodlh__uxu in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, jodlh__uxu):
                val = A[jodlh__uxu]
            s += val
        return s
    return impl


@overload_method(BooleanArrayType, 'astype', no_unliteral=True)
def overload_bool_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "BooleanArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if dtype == types.bool_:
        if is_overload_false(copy):
            return lambda A, dtype, copy=True: A
        elif is_overload_true(copy):
            return lambda A, dtype, copy=True: A.copy()
        else:

            def impl(A, dtype, copy=True):
                if copy:
                    return A.copy()
                else:
                    return A
            return impl
    nb_dtype = parse_dtype(dtype, 'BooleanArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
            n = len(data)
            hfqyx__jqr = np.empty(n, nb_dtype)
            for jodlh__uxu in numba.parfors.parfor.internal_prange(n):
                hfqyx__jqr[jodlh__uxu] = data[jodlh__uxu]
                if bodo.libs.array_kernels.isna(A, jodlh__uxu):
                    hfqyx__jqr[jodlh__uxu] = np.nan
            return hfqyx__jqr
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.bool_arr_ext.
        get_bool_arr_data(A).astype(nb_dtype))


@overload_method(BooleanArrayType, 'fillna', no_unliteral=True)
def overload_bool_fillna(A, value=None, method=None, limit=None):

    def impl(A, value=None, method=None, limit=None):
        data = bodo.libs.bool_arr_ext.get_bool_arr_data(A)
        n = len(data)
        hfqyx__jqr = np.empty(n, dtype=np.bool_)
        for jodlh__uxu in numba.parfors.parfor.internal_prange(n):
            hfqyx__jqr[jodlh__uxu] = data[jodlh__uxu]
            if bodo.libs.array_kernels.isna(A, jodlh__uxu):
                hfqyx__jqr[jodlh__uxu] = value
        return hfqyx__jqr
    return impl


@overload(str, no_unliteral=True)
def overload_str_bool(val):
    if val == types.bool_:

        def impl(val):
            if val:
                return 'True'
            return 'False'
        return impl


ufunc_aliases = {'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    tak__uyw = op.__name__
    tak__uyw = ufunc_aliases.get(tak__uyw, tak__uyw)
    if n_inputs == 1:

        def overload_bool_arr_op_nin_1(A):
            if isinstance(A, BooleanArrayType):
                return bodo.libs.int_arr_ext.get_nullable_array_unary_impl(op,
                    A)
        return overload_bool_arr_op_nin_1
    elif n_inputs == 2:

        def overload_bool_arr_op_nin_2(lhs, rhs):
            if lhs == boolean_array or rhs == boolean_array:
                return bodo.libs.int_arr_ext.get_nullable_array_binary_impl(op,
                    lhs, rhs)
        return overload_bool_arr_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for epza__vic in numba.np.ufunc_db.get_ufuncs():
        cthcl__dqjcp = create_op_overload(epza__vic, epza__vic.nin)
        overload(epza__vic, no_unliteral=True)(cthcl__dqjcp)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod, operator.or_, operator.and_]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        cthcl__dqjcp = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(cthcl__dqjcp)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        cthcl__dqjcp = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(cthcl__dqjcp)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        cthcl__dqjcp = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(cthcl__dqjcp)


_install_unary_ops()


@overload_method(BooleanArrayType, 'unique', no_unliteral=True)
def overload_unique(A):

    def impl_bool_arr(A):
        data = []
        nesrj__gehk = []
        bqopb__euf = False
        roch__zlf = False
        zxdtv__vpa = False
        for jodlh__uxu in range(len(A)):
            if bodo.libs.array_kernels.isna(A, jodlh__uxu):
                if not bqopb__euf:
                    data.append(False)
                    nesrj__gehk.append(False)
                    bqopb__euf = True
                continue
            val = A[jodlh__uxu]
            if val and not roch__zlf:
                data.append(True)
                nesrj__gehk.append(True)
                roch__zlf = True
            if not val and not zxdtv__vpa:
                data.append(False)
                nesrj__gehk.append(True)
                zxdtv__vpa = True
            if bqopb__euf and roch__zlf and zxdtv__vpa:
                break
        ziyi__jbn = np.array(data)
        n = len(ziyi__jbn)
        xkyyu__bgw = 1
        etrx__ffe = np.empty(xkyyu__bgw, np.uint8)
        for wzc__bmi in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(etrx__ffe, wzc__bmi,
                nesrj__gehk[wzc__bmi])
        return init_bool_array(ziyi__jbn, etrx__ffe)
    return impl_bool_arr


@overload(operator.getitem, no_unliteral=True)
def bool_arr_ind_getitem(A, ind):
    if ind == boolean_array and (isinstance(A, (types.Array, bodo.libs.
        int_arr_ext.IntegerArrayType, bodo.libs.float_arr_ext.
        FloatingArrayType, bodo.libs.struct_arr_ext.StructArrayType, bodo.
        libs.array_item_arr_ext.ArrayItemArrayType, bodo.libs.map_arr_ext.
        MapArrayType, bodo.libs.tuple_arr_ext.TupleArrayType, bodo.
        CategoricalArrayType, bodo.TimeArrayType, bodo.DecimalArrayType,
        bodo.DatetimeArrayType)) or A in (string_array_type, bodo.hiframes.
        split_impl.string_array_split_view_type, boolean_array, bodo.
        datetime_date_array_type, bodo.datetime_timedelta_array_type, bodo.
        binary_array_type)):

        def impl(A, ind):
            pwl__zxt = bodo.utils.conversion.nullable_bool_to_bool_na_false(ind
                )
            return A[pwl__zxt]
        return impl


@lower_cast(types.Array(types.bool_, 1, 'C'), boolean_array)
def cast_np_bool_arr_to_bool_arr(context, builder, fromty, toty, val):
    func = lambda A: bodo.libs.bool_arr_ext.init_bool_array(A, np.full(len(
        A) + 7 >> 3, 255, np.uint8))
    fine__efxoi = context.compile_internal(builder, func, toty(fromty), [val])
    return impl_ret_borrowed(context, builder, toty, fine__efxoi)


@overload(operator.setitem, no_unliteral=True)
def overload_np_array_setitem_bool_arr(A, idx, val):
    if isinstance(A, types.Array) and idx == boolean_array:

        def impl(A, idx, val):
            A[idx._data] = val
        return impl


def create_nullable_logical_op_overload(op):
    jjxyx__chix = op == operator.or_

    def bool_array_impl(val1, val2):
        if not is_valid_boolean_array_logical_op(val1, val2):
            return
        fvxai__xfy = bodo.utils.utils.is_array_typ(val1, False)
        eee__eaaom = bodo.utils.utils.is_array_typ(val2, False)
        rew__dfz = 'val1' if fvxai__xfy else 'val2'
        xubh__sec = 'def impl(val1, val2):\n'
        xubh__sec += f'  n = len({rew__dfz})\n'
        xubh__sec += (
            '  out_arr = bodo.utils.utils.alloc_type(n, bodo.boolean_array, (-1,))\n'
            )
        xubh__sec += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if fvxai__xfy:
            null1 = 'bodo.libs.array_kernels.isna(val1, i)\n'
            kjlv__cjjae = 'val1[i]'
        else:
            null1 = 'False\n'
            kjlv__cjjae = 'val1'
        if eee__eaaom:
            null2 = 'bodo.libs.array_kernels.isna(val2, i)\n'
            pix__sjz = 'val2[i]'
        else:
            null2 = 'False\n'
            pix__sjz = 'val2'
        if jjxyx__chix:
            xubh__sec += f"""    result, isna_val = compute_or_body({null1}, {null2}, {kjlv__cjjae}, {pix__sjz})
"""
        else:
            xubh__sec += f"""    result, isna_val = compute_and_body({null1}, {null2}, {kjlv__cjjae}, {pix__sjz})
"""
        xubh__sec += '    out_arr[i] = result\n'
        xubh__sec += '    if isna_val:\n'
        xubh__sec += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
        xubh__sec += '      continue\n'
        xubh__sec += '  return out_arr\n'
        thw__fpv = {}
        exec(xubh__sec, {'bodo': bodo, 'numba': numba, 'compute_and_body':
            compute_and_body, 'compute_or_body': compute_or_body}, thw__fpv)
        impl = thw__fpv['impl']
        return impl
    return bool_array_impl


def compute_or_body(null1, null2, val1, val2):
    pass


@overload(compute_or_body)
def overload_compute_or_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == False
        elif null2:
            return val1, val1 == False
        else:
            return val1 | val2, False
    return impl


def compute_and_body(null1, null2, val1, val2):
    pass


@overload(compute_and_body)
def overload_compute_and_body(null1, null2, val1, val2):

    def impl(null1, null2, val1, val2):
        if null1 and null2:
            return False, True
        elif null1:
            return val2, val2 == True
        elif null2:
            return val1, val1 == True
        else:
            return val1 & val2, False
    return impl


def create_boolean_array_logical_lower_impl(op):

    def logical_lower_impl(context, builder, sig, args):
        impl = create_nullable_logical_op_overload(op)(*sig.args)
        return context.compile_internal(builder, impl, sig, args)
    return logical_lower_impl


class BooleanArrayLogicalOperatorTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert len(args) == 2
        assert not kws
        if not is_valid_boolean_array_logical_op(args[0], args[1]):
            return
        wwlst__jrp = boolean_array
        return wwlst__jrp(*args)


def is_valid_boolean_array_logical_op(typ1, typ2):
    mmpz__iwfq = (typ1 == bodo.boolean_array or typ2 == bodo.boolean_array
        ) and (bodo.utils.utils.is_array_typ(typ1, False) and typ1.dtype ==
        types.bool_ or typ1 == types.bool_) and (bodo.utils.utils.
        is_array_typ(typ2, False) and typ2.dtype == types.bool_ or typ2 ==
        types.bool_)
    return mmpz__iwfq


def _install_nullable_logical_lowering():
    for op in (operator.and_, operator.or_):
        jxftr__yoito = create_boolean_array_logical_lower_impl(op)
        infer_global(op)(BooleanArrayLogicalOperatorTemplate)
        for typ1, typ2 in [(boolean_array, boolean_array), (boolean_array,
            types.bool_), (boolean_array, types.Array(types.bool_, 1, 'C'))]:
            lower_builtin(op, typ1, typ2)(jxftr__yoito)
            if typ1 != typ2:
                lower_builtin(op, typ2, typ1)(jxftr__yoito)


_install_nullable_logical_lowering()
