"""Nullable integer array corresponding to Pandas IntegerArray.
However, nulls are stored in bit arrays similar to Arrow's arrays.
"""
import operator
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, type_callable, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs.str_arr_ext import kBitmask
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('mask_arr_to_bitmap', hstr_ext.mask_arr_to_bitmap)
ll.add_symbol('is_pd_int_array', array_ext.is_pd_int_array)
ll.add_symbol('int_array_from_sequence', array_ext.int_array_from_sequence)
from bodo.hiframes.datetime_timedelta_ext import pd_timedelta_type
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, check_unsupported_args, is_iterable_type, is_list_like_index_type, is_overload_false, is_overload_none, is_overload_true, parse_dtype, raise_bodo_error, to_nullable_type


class IntegerArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(IntegerArrayType, self).__init__(name=
            f'IntegerArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntegerArrayType(self.dtype)

    @property
    def get_pandas_scalar_type_instance(self):
        ngowq__nenh = int(np.log2(self.dtype.bitwidth // 8))
        sks__dwsl = 0 if self.dtype.signed else 4
        idx = ngowq__nenh + sks__dwsl
        return pd_int_dtype_classes[idx]()


@register_model(IntegerArrayType)
class IntegerArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qixri__qsavl = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, qixri__qsavl)


make_attribute_wrapper(IntegerArrayType, 'data', '_data')
make_attribute_wrapper(IntegerArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.IntegerArray)
def _typeof_pd_int_array(val, c):
    vqmt__zpwv = 8 * val.dtype.itemsize
    ecnnp__rfv = '' if val.dtype.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(ecnnp__rfv, vqmt__zpwv))
    return IntegerArrayType(dtype)


class IntDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Integer)
        self.dtype = dtype
        rgiq__hwc = '{}Int{}Dtype()'.format('' if dtype.signed else 'U',
            dtype.bitwidth)
        super(IntDtype, self).__init__(rgiq__hwc)


register_model(IntDtype)(models.OpaqueModel)


@box(IntDtype)
def box_intdtype(typ, val, c):
    pxe__meinx = c.context.insert_const_string(c.builder.module, 'pandas')
    oqapg__homu = c.pyapi.import_module_noblock(pxe__meinx)
    trft__xyyjt = c.pyapi.call_method(oqapg__homu, str(typ)[:-2], ())
    c.pyapi.decref(oqapg__homu)
    return trft__xyyjt


@unbox(IntDtype)
def unbox_intdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_int_dtype(val, c):
    vqmt__zpwv = 8 * val.itemsize
    ecnnp__rfv = '' if val.kind == 'i' else 'u'
    dtype = getattr(types, '{}int{}'.format(ecnnp__rfv, vqmt__zpwv))
    return IntDtype(dtype)


def _register_int_dtype(t):
    typeof_impl.register(t)(typeof_pd_int_dtype)
    int_dtype = typeof_pd_int_dtype(t(), None)
    type_callable(t)(lambda c: lambda : int_dtype)
    lower_builtin(t)(lambda c, b, s, a: c.get_dummy_value())


pd_int_dtype_classes = (pd.Int8Dtype, pd.Int16Dtype, pd.Int32Dtype, pd.
    Int64Dtype, pd.UInt8Dtype, pd.UInt16Dtype, pd.UInt32Dtype, pd.UInt64Dtype)
for t in pd_int_dtype_classes:
    _register_int_dtype(t)


@numba.extending.register_jitable
def mask_arr_to_bitmap(mask_arr):
    n = len(mask_arr)
    aefu__pwdj = n + 7 >> 3
    vzdyo__mmx = np.empty(aefu__pwdj, np.uint8)
    for i in range(n):
        nts__jgzkg = i // 8
        vzdyo__mmx[nts__jgzkg] ^= np.uint8(-np.uint8(not mask_arr[i]) ^
            vzdyo__mmx[nts__jgzkg]) & kBitmask[i % 8]
    return vzdyo__mmx


@unbox(IntegerArrayType)
def unbox_int_array(typ, obj, c):
    cegg__gaf = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(cegg__gaf)
    c.pyapi.decref(cegg__gaf)
    zkls__csyw = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    aefu__pwdj = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    qlw__pwveg = bodo.utils.utils._empty_nd_impl(c.context, c.builder,
        types.Array(types.uint8, 1, 'C'), [aefu__pwdj])
    wsfm__rty = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    lxmzl__umrm = cgutils.get_or_insert_function(c.builder.module,
        wsfm__rty, name='is_pd_int_array')
    tmcem__pjn = c.builder.call(lxmzl__umrm, [obj])
    ocx__fjxlm = c.builder.icmp_unsigned('!=', tmcem__pjn, tmcem__pjn.type(0))
    with c.builder.if_else(ocx__fjxlm) as (limqd__fwqk, koqkj__ctvi):
        with limqd__fwqk:
            wnl__xpx = c.pyapi.object_getattr_string(obj, '_data')
            zkls__csyw.data = c.pyapi.to_native_value(types.Array(typ.dtype,
                1, 'C'), wnl__xpx).value
            xnmtd__kqo = c.pyapi.object_getattr_string(obj, '_mask')
            mask_arr = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), xnmtd__kqo).value
            c.pyapi.decref(wnl__xpx)
            c.pyapi.decref(xnmtd__kqo)
            yszeg__twdcj = c.context.make_array(types.Array(types.bool_, 1,
                'C'))(c.context, c.builder, mask_arr)
            wsfm__rty = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            lxmzl__umrm = cgutils.get_or_insert_function(c.builder.module,
                wsfm__rty, name='mask_arr_to_bitmap')
            c.builder.call(lxmzl__umrm, [qlw__pwveg.data, yszeg__twdcj.data, n]
                )
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), mask_arr)
        with koqkj__ctvi:
            nbnfd__fawf = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            wsfm__rty = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            dxmuu__veo = cgutils.get_or_insert_function(c.builder.module,
                wsfm__rty, name='int_array_from_sequence')
            c.builder.call(dxmuu__veo, [obj, c.builder.bitcast(nbnfd__fawf.
                data, lir.IntType(8).as_pointer()), qlw__pwveg.data])
            zkls__csyw.data = nbnfd__fawf._getvalue()
    zkls__csyw.null_bitmap = qlw__pwveg._getvalue()
    dnh__kua = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(zkls__csyw._getvalue(), is_error=dnh__kua)


@box(IntegerArrayType)
def box_int_arr(typ, val, c):
    zkls__csyw = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        zkls__csyw.data, c.env_manager)
    srk__sbc = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, zkls__csyw.null_bitmap).data
    cegg__gaf = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(cegg__gaf)
    pxe__meinx = c.context.insert_const_string(c.builder.module, 'numpy')
    zus__xanq = c.pyapi.import_module_noblock(pxe__meinx)
    zmamg__hab = c.pyapi.object_getattr_string(zus__xanq, 'bool_')
    mask_arr = c.pyapi.call_method(zus__xanq, 'empty', (cegg__gaf, zmamg__hab))
    jkbe__rtx = c.pyapi.object_getattr_string(mask_arr, 'ctypes')
    byl__hhh = c.pyapi.object_getattr_string(jkbe__rtx, 'data')
    rhc__itdam = c.builder.inttoptr(c.pyapi.long_as_longlong(byl__hhh), lir
        .IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as jpfsz__twcp:
        i = jpfsz__twcp.index
        imqu__moa = c.builder.lshr(i, lir.Constant(lir.IntType(64), 3))
        uay__qih = c.builder.load(cgutils.gep(c.builder, srk__sbc, imqu__moa))
        gojr__ifh = c.builder.trunc(c.builder.and_(i, lir.Constant(lir.
            IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(uay__qih, gojr__ifh), lir.
            Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        ddzkg__bazqb = cgutils.gep(c.builder, rhc__itdam, i)
        c.builder.store(val, ddzkg__bazqb)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        zkls__csyw.null_bitmap)
    pxe__meinx = c.context.insert_const_string(c.builder.module, 'pandas')
    oqapg__homu = c.pyapi.import_module_noblock(pxe__meinx)
    hcepb__usu = c.pyapi.object_getattr_string(oqapg__homu, 'arrays')
    trft__xyyjt = c.pyapi.call_method(hcepb__usu, 'IntegerArray', (data,
        mask_arr))
    c.pyapi.decref(oqapg__homu)
    c.pyapi.decref(cegg__gaf)
    c.pyapi.decref(zus__xanq)
    c.pyapi.decref(zmamg__hab)
    c.pyapi.decref(jkbe__rtx)
    c.pyapi.decref(byl__hhh)
    c.pyapi.decref(hcepb__usu)
    c.pyapi.decref(data)
    c.pyapi.decref(mask_arr)
    return trft__xyyjt


@intrinsic
def init_integer_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        rxl__isei, xvtm__tdbi = args
        zkls__csyw = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        zkls__csyw.data = rxl__isei
        zkls__csyw.null_bitmap = xvtm__tdbi
        context.nrt.incref(builder, signature.args[0], rxl__isei)
        context.nrt.incref(builder, signature.args[1], xvtm__tdbi)
        return zkls__csyw._getvalue()
    rnqvx__dmvr = IntegerArrayType(data.dtype)
    awcp__tmee = rnqvx__dmvr(data, null_bitmap)
    return awcp__tmee, codegen


@lower_constant(IntegerArrayType)
def lower_constant_int_arr(context, builder, typ, pyval):
    n = len(pyval)
    imfyc__ecqc = np.empty(n, pyval.dtype.type)
    dbwr__gdow = np.empty(n + 7 >> 3, np.uint8)
    for i, s in enumerate(pyval):
        qok__awszl = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(dbwr__gdow, i, int(not qok__awszl)
            )
        if not qok__awszl:
            imfyc__ecqc[i] = s
    dco__lauh = context.get_constant_generic(builder, types.Array(typ.dtype,
        1, 'C'), imfyc__ecqc)
    apicu__azlb = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), dbwr__gdow)
    return lir.Constant.literal_struct([dco__lauh, apicu__azlb])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_int_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_int_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    nsdzr__wfyh = args[0]
    if equiv_set.has_shape(nsdzr__wfyh):
        return ArrayAnalysis.AnalyzeResult(shape=nsdzr__wfyh, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_get_int_arr_data = (
    get_int_arr_data_equiv)


def init_integer_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    nsdzr__wfyh = args[0]
    if equiv_set.has_shape(nsdzr__wfyh):
        return ArrayAnalysis.AnalyzeResult(shape=nsdzr__wfyh, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_init_integer_array = (
    init_integer_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_integer_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_integer_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_integer_array
numba.core.ir_utils.alias_func_extensions['get_int_arr_data',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_int_arr_bitmap',
    'bodo.libs.int_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_int_array(n, dtype):
    imfyc__ecqc = np.empty(n, dtype)
    hzcy__tyb = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_integer_array(imfyc__ecqc, hzcy__tyb)


def alloc_int_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_libs_int_arr_ext_alloc_int_array = (
    alloc_int_array_equiv)


@numba.extending.register_jitable
def set_bit_to_arr(bits, i, bit_is_set):
    bits[i // 8] ^= np.uint8(-np.uint8(bit_is_set) ^ bits[i // 8]) & kBitmask[
        i % 8]


@numba.extending.register_jitable
def get_bit_bitmap_arr(bits, i):
    return bits[i >> 3] >> (i & 7) & 1


@overload(operator.getitem, no_unliteral=True)
def int_arr_getitem(A, ind):
    if not isinstance(A, IntegerArrayType):
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            ifr__tkg, wpcau__gmg = array_getitem_bool_index(A, ind)
            return init_integer_array(ifr__tkg, wpcau__gmg)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            ifr__tkg, wpcau__gmg = array_getitem_int_index(A, ind)
            return init_integer_array(ifr__tkg, wpcau__gmg)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            ifr__tkg, wpcau__gmg = array_getitem_slice_index(A, ind)
            return init_integer_array(ifr__tkg, wpcau__gmg)
        return impl_slice
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for IntegerArray with indexing type {ind} not supported.'
            )


@overload(operator.setitem, no_unliteral=True)
def int_arr_setitem(A, idx, val):
    if not isinstance(A, IntegerArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    ozkzq__mgny = (
        f"setitem for IntegerArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    hleu__howlv = isinstance(val, (types.Integer, types.Boolean, types.Float))
    if isinstance(idx, types.Integer):
        if hleu__howlv:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(ozkzq__mgny)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean)) or hleu__howlv):
        raise BodoError(ozkzq__mgny)
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
        f'setitem for IntegerArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_int_arr_len(A):
    if isinstance(A, IntegerArrayType):
        return lambda A: len(A._data)


@overload_attribute(IntegerArrayType, 'shape')
def overload_int_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(IntegerArrayType, 'dtype')
def overload_int_arr_dtype(A):
    dtype_class = getattr(pd, '{}Int{}Dtype'.format('' if A.dtype.signed else
        'U', A.dtype.bitwidth))
    return lambda A: dtype_class()


@overload_attribute(IntegerArrayType, 'ndim')
def overload_int_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntegerArrayType, 'nbytes')
def int_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(IntegerArrayType, 'copy', no_unliteral=True)
def overload_int_arr_copy(A, dtype=None):
    if not is_overload_none(dtype):
        return lambda A, dtype=None: A.astype(dtype, copy=True)
    else:
        return lambda A, dtype=None: bodo.libs.int_arr_ext.init_integer_array(
            bodo.libs.int_arr_ext.get_int_arr_data(A).copy(), bodo.libs.
            int_arr_ext.get_int_arr_bitmap(A).copy())


@overload_method(IntegerArrayType, 'astype', no_unliteral=True)
def overload_int_arr_astype(A, dtype, copy=True):
    if isinstance(dtype, types.TypeRef):
        dtype = dtype.instance_type
    if dtype == types.unicode_type:
        raise_bodo_error(
            "IntegerArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.NumberClass):
        dtype = dtype.dtype
    if isinstance(dtype, IntDtype) and A.dtype == dtype.dtype:
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
    if isinstance(dtype, IntDtype):
        np_dtype = dtype.dtype
        return (lambda A, dtype, copy=True: bodo.libs.int_arr_ext.
            init_integer_array(bodo.libs.int_arr_ext.get_int_arr_data(A).
            astype(np_dtype), bodo.libs.int_arr_ext.get_int_arr_bitmap(A).
            copy()))
    nb_dtype = parse_dtype(dtype, 'IntegerArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.int_arr_ext.get_int_arr_data(A)
            n = len(data)
            qcxk__cto = np.empty(n, nb_dtype)
            for i in numba.parfors.parfor.internal_prange(n):
                qcxk__cto[i] = data[i]
                if bodo.libs.array_kernels.isna(A, i):
                    qcxk__cto[i] = np.nan
            return qcxk__cto
        return impl_float
    return lambda A, dtype, copy=True: bodo.libs.int_arr_ext.get_int_arr_data(A
        ).astype(nb_dtype)


ufunc_aliases = {'subtract': 'sub', 'multiply': 'mul', 'floor_divide':
    'floordiv', 'true_divide': 'truediv', 'power': 'pow', 'remainder':
    'mod', 'divide': 'div', 'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    if n_inputs == 1:

        def overload_int_arr_op_nin_1(A):
            if isinstance(A, IntegerArrayType):
                return get_nullable_array_unary_impl(op, A)
        return overload_int_arr_op_nin_1
    elif n_inputs == 2:

        def overload_series_op_nin_2(lhs, rhs):
            if isinstance(lhs, IntegerArrayType) or isinstance(rhs,
                IntegerArrayType):
                return get_nullable_array_binary_impl(op, lhs, rhs)
        return overload_series_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for mktb__agldr in numba.np.ufunc_db.get_ufuncs():
        egj__jaiy = create_op_overload(mktb__agldr, mktb__agldr.nin)
        overload(mktb__agldr, no_unliteral=True)(egj__jaiy)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        egj__jaiy = create_op_overload(op, 2)
        overload(op)(egj__jaiy)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        egj__jaiy = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(egj__jaiy)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        egj__jaiy = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(egj__jaiy)


_install_unary_ops()


@overload_method(IntegerArrayType, 'sum', no_unliteral=True)
def overload_int_arr_sum(A, skipna=True, min_count=0):
    bwhqz__bvju = dict(skipna=skipna, min_count=min_count)
    tuxu__nsesn = dict(skipna=True, min_count=0)
    check_unsupported_args('IntegerArray.sum', bwhqz__bvju, tuxu__nsesn)

    def impl(A, skipna=True, min_count=0):
        numba.parfors.parfor.init_prange()
        s = 0
        for i in numba.parfors.parfor.internal_prange(len(A)):
            val = 0
            if not bodo.libs.array_kernels.isna(A, i):
                val = A[i]
            s += val
        return s
    return impl


@overload_method(IntegerArrayType, 'unique', no_unliteral=True)
def overload_unique(A):
    dtype = A.dtype

    def impl_int_arr(A):
        data = []
        gojr__ifh = []
        hnzyg__ukl = False
        s = set()
        for i in range(len(A)):
            val = A[i]
            if bodo.libs.array_kernels.isna(A, i):
                if not hnzyg__ukl:
                    data.append(dtype(1))
                    gojr__ifh.append(False)
                    hnzyg__ukl = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                gojr__ifh.append(True)
        ifr__tkg = np.array(data)
        n = len(ifr__tkg)
        aefu__pwdj = n + 7 >> 3
        wpcau__gmg = np.empty(aefu__pwdj, np.uint8)
        for fuq__ssunb in range(n):
            set_bit_to_arr(wpcau__gmg, fuq__ssunb, gojr__ifh[fuq__ssunb])
        return init_integer_array(ifr__tkg, wpcau__gmg)
    return impl_int_arr


def get_nullable_array_unary_impl(op, A):
    nru__pblw = numba.core.registry.cpu_target.typing_context
    ilox__dldet = nru__pblw.resolve_function_type(op, (types.Array(A.dtype,
        1, 'C'),), {}).return_type
    ilox__dldet = to_nullable_type(ilox__dldet)

    def impl(A):
        n = len(A)
        ano__yex = bodo.utils.utils.alloc_type(n, ilox__dldet, None)
        for i in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(A, i):
                bodo.libs.array_kernels.setna(ano__yex, i)
                continue
            ano__yex[i] = op(A[i])
        return ano__yex
    return impl


def get_nullable_array_binary_impl(op, lhs, rhs):
    vshos__ede = (op in numba.core.typing.npydecl.
        NumpyRulesInplaceArrayOperator._op_map.keys())
    bvnh__yxxlo = isinstance(lhs, (types.Number, types.Boolean))
    vthkb__bmzbi = isinstance(rhs, (types.Number, types.Boolean))
    xzop__mmqu = types.Array(getattr(lhs, 'dtype', lhs), 1, 'C')
    mji__tooc = types.Array(getattr(rhs, 'dtype', rhs), 1, 'C')
    nru__pblw = numba.core.registry.cpu_target.typing_context
    ilox__dldet = nru__pblw.resolve_function_type(op, (xzop__mmqu,
        mji__tooc), {}).return_type
    ilox__dldet = to_nullable_type(ilox__dldet)
    if op in (operator.truediv, operator.itruediv):
        op = np.true_divide
    elif op in (operator.floordiv, operator.ifloordiv):
        op = np.floor_divide
    ehiuq__yel = 'lhs' if bvnh__yxxlo else 'lhs[i]'
    nxhr__ghh = 'rhs' if vthkb__bmzbi else 'rhs[i]'
    cpd__gnkyf = ('False' if bvnh__yxxlo else
        'bodo.libs.array_kernels.isna(lhs, i)')
    dzgt__fsq = ('False' if vthkb__bmzbi else
        'bodo.libs.array_kernels.isna(rhs, i)')
    jxgju__tatva = 'def impl(lhs, rhs):\n'
    jxgju__tatva += '  n = len({})\n'.format('lhs' if not bvnh__yxxlo else
        'rhs')
    if vshos__ede:
        jxgju__tatva += '  out_arr = {}\n'.format('lhs' if not bvnh__yxxlo else
            'rhs')
    else:
        jxgju__tatva += (
            '  out_arr = bodo.utils.utils.alloc_type(n, ret_dtype, None)\n')
    jxgju__tatva += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    jxgju__tatva += '    if ({}\n'.format(cpd__gnkyf)
    jxgju__tatva += '        or {}):\n'.format(dzgt__fsq)
    jxgju__tatva += '      bodo.libs.array_kernels.setna(out_arr, i)\n'
    jxgju__tatva += '      continue\n'
    jxgju__tatva += (
        """    out_arr[i] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(op({}, {}))
"""
        .format(ehiuq__yel, nxhr__ghh))
    jxgju__tatva += '  return out_arr\n'
    rbvx__tjp = {}
    exec(jxgju__tatva, {'bodo': bodo, 'numba': numba, 'np': np, 'ret_dtype':
        ilox__dldet, 'op': op}, rbvx__tjp)
    impl = rbvx__tjp['impl']
    return impl


def get_int_array_op_pd_td(op):

    def impl(lhs, rhs):
        bvnh__yxxlo = lhs in [pd_timedelta_type]
        vthkb__bmzbi = rhs in [pd_timedelta_type]
        if bvnh__yxxlo:

            def impl(lhs, rhs):
                n = len(rhs)
                ano__yex = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(rhs, i):
                        bodo.libs.array_kernels.setna(ano__yex, i)
                        continue
                    ano__yex[i
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        op(lhs, rhs[i]))
                return ano__yex
            return impl
        elif vthkb__bmzbi:

            def impl(lhs, rhs):
                n = len(lhs)
                ano__yex = np.empty(n, 'timedelta64[ns]')
                for i in numba.parfors.parfor.internal_prange(n):
                    if bodo.libs.array_kernels.isna(lhs, i):
                        bodo.libs.array_kernels.setna(ano__yex, i)
                        continue
                    ano__yex[i
                        ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                        op(lhs[i], rhs))
                return ano__yex
            return impl
    return impl
