"""Nullable float array corresponding to Pandas FloatingArray.
However, nulls are stored in bit arrays similar to Arrow's arrays.
"""
import operator
import os
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
from bodo.libs import array_ext, hstr_ext
ll.add_symbol('is_pd_float_array', array_ext.is_pd_float_array)
ll.add_symbol('float_array_from_sequence', array_ext.float_array_from_sequence)
from bodo.utils.indexing import array_getitem_bool_index, array_getitem_int_index, array_getitem_slice_index, array_setitem_bool_index, array_setitem_int_index, array_setitem_slice_index
from bodo.utils.typing import BodoError, check_unsupported_args, is_iterable_type, is_list_like_index_type, is_overload_false, is_overload_none, is_overload_true, parse_dtype, raise_bodo_error
_use_nullable_float = int(os.environ.get('BODO_USE_NULLABLE_FLOAT', '0'))


class FloatingArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(FloatingArrayType, self).__init__(name=
            f'FloatingArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return FloatingArrayType(self.dtype)

    @property
    def get_pandas_scalar_type_instance(self):
        return pd.Float64Dtype(
            ) if self.dtype == types.float64 else pd.Float32Dtype()


@register_model(FloatingArrayType)
class FloatingArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        epsb__cpe = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'null_bitmap', types.Array(types.uint8, 1, 'C'))]
        models.StructModel.__init__(self, dmm, fe_type, epsb__cpe)


make_attribute_wrapper(FloatingArrayType, 'data', '_data')
make_attribute_wrapper(FloatingArrayType, 'null_bitmap', '_null_bitmap')


@typeof_impl.register(pd.arrays.FloatingArray)
def _typeof_pd_float_array(val, c):
    dtype = types.float32 if val.dtype == pd.Float32Dtype() else types.float64
    return FloatingArrayType(dtype)


class FloatDtype(types.Number):

    def __init__(self, dtype):
        assert isinstance(dtype, types.Float)
        self.dtype = dtype
        opou__fasxu = f'Float{dtype.bitwidth}Dtype()'
        super(FloatDtype, self).__init__(opou__fasxu)


register_model(FloatDtype)(models.OpaqueModel)


@box(FloatDtype)
def box_floatdtype(typ, val, c):
    ixlfp__gmqv = c.context.insert_const_string(c.builder.module, 'pandas')
    dfm__tjbh = c.pyapi.import_module_noblock(ixlfp__gmqv)
    ywqt__gwit = c.pyapi.call_method(dfm__tjbh, str(typ)[:-2], ())
    c.pyapi.decref(dfm__tjbh)
    return ywqt__gwit


@unbox(FloatDtype)
def unbox_floatdtype(typ, val, c):
    return NativeValue(c.context.get_dummy_value())


def typeof_pd_float_dtype(val, c):
    dtype = types.float32 if val == pd.Float32Dtype() else types.float64
    return FloatDtype(dtype)


def _register_float_dtype(t):
    typeof_impl.register(t)(typeof_pd_float_dtype)
    float_dtype = typeof_pd_float_dtype(t(), None)
    type_callable(t)(lambda c: lambda : float_dtype)
    lower_builtin(t)(lambda c, b, s, a: c.get_dummy_value())


_register_float_dtype(pd.Float32Dtype)
_register_float_dtype(pd.Float64Dtype)


@unbox(FloatingArrayType)
def unbox_float_array(typ, obj, c):
    visg__dqa = c.pyapi.call_method(obj, '__len__', ())
    n = c.pyapi.long_as_longlong(visg__dqa)
    c.pyapi.decref(visg__dqa)
    cuwk__cfd = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    zonr__bkjfd = c.builder.udiv(c.builder.add(n, lir.Constant(lir.IntType(
        64), 7)), lir.Constant(lir.IntType(64), 8))
    xnoe__jcq = bodo.utils.utils._empty_nd_impl(c.context, c.builder, types
        .Array(types.uint8, 1, 'C'), [zonr__bkjfd])
    fxf__ubhj = lir.FunctionType(lir.IntType(32), [lir.IntType(8).as_pointer()]
        )
    srrq__urrbi = cgutils.get_or_insert_function(c.builder.module,
        fxf__ubhj, name='is_pd_float_array')
    hmtti__ezr = c.builder.call(srrq__urrbi, [obj])
    oqic__blfb = c.builder.icmp_unsigned('!=', hmtti__ezr, hmtti__ezr.type(0))
    with c.builder.if_else(oqic__blfb) as (nrnmg__aay, vrwa__zfikw):
        with nrnmg__aay:
            lgo__hjer = c.pyapi.object_getattr_string(obj, '_data')
            cuwk__cfd.data = c.pyapi.to_native_value(types.Array(typ.dtype,
                1, 'C'), lgo__hjer).value
            iwlde__dzns = c.pyapi.object_getattr_string(obj, '_mask')
            ilzn__ovgg = c.pyapi.to_native_value(types.Array(types.bool_, 1,
                'C'), iwlde__dzns).value
            c.pyapi.decref(lgo__hjer)
            c.pyapi.decref(iwlde__dzns)
            pyd__ghxg = c.context.make_array(types.Array(types.bool_, 1, 'C'))(
                c.context, c.builder, ilzn__ovgg)
            fxf__ubhj = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
            srrq__urrbi = cgutils.get_or_insert_function(c.builder.module,
                fxf__ubhj, name='mask_arr_to_bitmap')
            c.builder.call(srrq__urrbi, [xnoe__jcq.data, pyd__ghxg.data, n])
            c.context.nrt.decref(c.builder, types.Array(types.bool_, 1, 'C'
                ), ilzn__ovgg)
        with vrwa__zfikw:
            eqyp__uflb = bodo.utils.utils._empty_nd_impl(c.context, c.
                builder, types.Array(typ.dtype, 1, 'C'), [n])
            fxf__ubhj = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
                as_pointer()])
            kdzo__xbsm = cgutils.get_or_insert_function(c.builder.module,
                fxf__ubhj, name='float_array_from_sequence')
            c.builder.call(kdzo__xbsm, [obj, c.builder.bitcast(eqyp__uflb.
                data, lir.IntType(8).as_pointer()), xnoe__jcq.data])
            cuwk__cfd.data = eqyp__uflb._getvalue()
    cuwk__cfd.null_bitmap = xnoe__jcq._getvalue()
    kloco__lcm = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cuwk__cfd._getvalue(), is_error=kloco__lcm)


@box(FloatingArrayType)
def box_float_array(typ, val, c):
    cuwk__cfd = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    data = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        cuwk__cfd.data, c.env_manager)
    uttan__idqk = c.context.make_array(types.Array(types.uint8, 1, 'C'))(c.
        context, c.builder, cuwk__cfd.null_bitmap).data
    visg__dqa = c.pyapi.call_method(data, '__len__', ())
    n = c.pyapi.long_as_longlong(visg__dqa)
    ixlfp__gmqv = c.context.insert_const_string(c.builder.module, 'numpy')
    jdv__hua = c.pyapi.import_module_noblock(ixlfp__gmqv)
    ios__ehq = c.pyapi.object_getattr_string(jdv__hua, 'bool_')
    ilzn__ovgg = c.pyapi.call_method(jdv__hua, 'empty', (visg__dqa, ios__ehq))
    njrcm__byo = c.pyapi.object_getattr_string(ilzn__ovgg, 'ctypes')
    cxbjk__bksm = c.pyapi.object_getattr_string(njrcm__byo, 'data')
    yexsx__lbkmx = c.builder.inttoptr(c.pyapi.long_as_longlong(cxbjk__bksm),
        lir.IntType(8).as_pointer())
    with cgutils.for_range(c.builder, n) as ypaxl__reoog:
        sdv__jkq = ypaxl__reoog.index
        wzkfv__dxrp = c.builder.lshr(sdv__jkq, lir.Constant(lir.IntType(64), 3)
            )
        xtule__isyx = c.builder.load(cgutils.gep(c.builder, uttan__idqk,
            wzkfv__dxrp))
        wrbyk__elfjm = c.builder.trunc(c.builder.and_(sdv__jkq, lir.
            Constant(lir.IntType(64), 7)), lir.IntType(8))
        val = c.builder.and_(c.builder.lshr(xtule__isyx, wrbyk__elfjm), lir
            .Constant(lir.IntType(8), 1))
        val = c.builder.xor(val, lir.Constant(lir.IntType(8), 1))
        luzfv__ownt = cgutils.gep(c.builder, yexsx__lbkmx, sdv__jkq)
        c.builder.store(val, luzfv__ownt)
    c.context.nrt.decref(c.builder, types.Array(types.uint8, 1, 'C'),
        cuwk__cfd.null_bitmap)
    ixlfp__gmqv = c.context.insert_const_string(c.builder.module, 'pandas')
    dfm__tjbh = c.pyapi.import_module_noblock(ixlfp__gmqv)
    rxdj__gmw = c.pyapi.object_getattr_string(dfm__tjbh, 'arrays')
    ywqt__gwit = c.pyapi.call_method(rxdj__gmw, 'FloatingArray', (data,
        ilzn__ovgg))
    c.pyapi.decref(dfm__tjbh)
    c.pyapi.decref(visg__dqa)
    c.pyapi.decref(jdv__hua)
    c.pyapi.decref(ios__ehq)
    c.pyapi.decref(njrcm__byo)
    c.pyapi.decref(cxbjk__bksm)
    c.pyapi.decref(rxdj__gmw)
    c.pyapi.decref(data)
    c.pyapi.decref(ilzn__ovgg)
    return ywqt__gwit


@intrinsic
def init_float_array(typingctx, data, null_bitmap=None):
    assert isinstance(data, types.Array)
    assert null_bitmap == types.Array(types.uint8, 1, 'C')

    def codegen(context, builder, signature, args):
        amr__pmyk, sdj__oace = args
        cuwk__cfd = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        cuwk__cfd.data = amr__pmyk
        cuwk__cfd.null_bitmap = sdj__oace
        context.nrt.incref(builder, signature.args[0], amr__pmyk)
        context.nrt.incref(builder, signature.args[1], sdj__oace)
        return cuwk__cfd._getvalue()
    ggcf__wcl = FloatingArrayType(data.dtype)
    xeqgm__lzh = ggcf__wcl(data, null_bitmap)
    return xeqgm__lzh, codegen


@lower_constant(FloatingArrayType)
def lower_constant_float_arr(context, builder, typ, pyval):
    n = len(pyval)
    zjla__dye = np.empty(n, pyval.dtype.type)
    bog__wts = np.empty(n + 7 >> 3, np.uint8)
    for sdv__jkq, s in enumerate(pyval):
        cba__ubq = pd.isna(s)
        bodo.libs.int_arr_ext.set_bit_to_arr(bog__wts, sdv__jkq, int(not
            cba__ubq))
        if not cba__ubq:
            zjla__dye[sdv__jkq] = s
    dnnj__gxwj = context.get_constant_generic(builder, types.Array(typ.
        dtype, 1, 'C'), zjla__dye)
    lsdkt__ecp = context.get_constant_generic(builder, types.Array(types.
        uint8, 1, 'C'), bog__wts)
    return lir.Constant.literal_struct([dnnj__gxwj, lsdkt__ecp])


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_float_arr_data(A):
    return lambda A: A._data


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_float_arr_bitmap(A):
    return lambda A: A._null_bitmap


def get_float_arr_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    pvuzx__xfmpo = args[0]
    if equiv_set.has_shape(pvuzx__xfmpo):
        return ArrayAnalysis.AnalyzeResult(shape=pvuzx__xfmpo, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_float_arr_ext_get_float_arr_data
    ) = get_float_arr_data_equiv


def init_float_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    pvuzx__xfmpo = args[0]
    if equiv_set.has_shape(pvuzx__xfmpo):
        return ArrayAnalysis.AnalyzeResult(shape=pvuzx__xfmpo, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_libs_float_arr_ext_init_float_array = (
    init_float_array_equiv)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


def alias_ext_init_float_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_float_array',
    'bodo.libs.float_arr_ext'] = alias_ext_init_float_array
numba.core.ir_utils.alias_func_extensions['get_float_arr_data',
    'bodo.libs.float_arr_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_float_arr_bitmap',
    'bodo.libs.float_arr_ext'] = alias_ext_dummy_func


@numba.njit(no_cpython_wrapper=True)
def alloc_float_array(n, dtype):
    zjla__dye = np.empty(n, dtype)
    zxvi__aagy = np.empty(n + 7 >> 3, dtype=np.uint8)
    return init_float_array(zjla__dye, zxvi__aagy)


def alloc_float_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis._analyze_op_call_bodo_libs_float_arr_ext_alloc_float_array
    ) = alloc_float_array_equiv


@overload(operator.getitem, no_unliteral=True)
def float_arr_getitem(A, ind):
    if not isinstance(A, FloatingArrayType):
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) and ind.dtype == types.bool_:

        def impl_bool(A, ind):
            alq__fhtj, psh__gkv = array_getitem_bool_index(A, ind)
            return init_float_array(alq__fhtj, psh__gkv)
        return impl_bool
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):

        def impl(A, ind):
            alq__fhtj, psh__gkv = array_getitem_int_index(A, ind)
            return init_float_array(alq__fhtj, psh__gkv)
        return impl
    if isinstance(ind, types.SliceType):

        def impl_slice(A, ind):
            alq__fhtj, psh__gkv = array_getitem_slice_index(A, ind)
            return init_float_array(alq__fhtj, psh__gkv)
        return impl_slice
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for IntegerArray with indexing type {ind} not supported.'
            )


@overload(operator.setitem, no_unliteral=True)
def float_arr_setitem(A, idx, val):
    if not isinstance(A, FloatingArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    yqe__ufzz = (
        f"setitem for FloatingArray with indexing type {idx} received an incorrect 'value' type {val}."
        )
    rwul__trr = isinstance(val, (types.Integer, types.Boolean, types.Float))
    if isinstance(idx, types.Integer):
        if rwul__trr:

            def impl_scalar(A, idx, val):
                A._data[idx] = val
                bodo.libs.int_arr_ext.set_bit_to_arr(A._null_bitmap, idx, 1)
            return impl_scalar
        else:
            raise BodoError(yqe__ufzz)
    if not (is_iterable_type(val) and isinstance(val.dtype, (types.Integer,
        types.Boolean, types.Float)) or rwul__trr):
        raise BodoError(yqe__ufzz)
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
        f'setitem for FloatingArray with indexing type {idx} not supported.')


@overload(len, no_unliteral=True)
def overload_float_arr_len(A):
    if isinstance(A, FloatingArrayType):
        return lambda A: len(A._data)


@overload_attribute(FloatingArrayType, 'shape')
def overload_float_arr_shape(A):
    return lambda A: (len(A._data),)


@overload_attribute(FloatingArrayType, 'dtype')
def overload_float_arr_dtype(A):
    dtype_class = (pd.Float32Dtype if A.dtype == types.float32 else pd.
        Float64Dtype)
    return lambda A: dtype_class()


@overload_attribute(FloatingArrayType, 'ndim')
def overload_float_arr_ndim(A):
    return lambda A: 1


@overload_attribute(FloatingArrayType, 'size')
def overload_float_size(A):
    return lambda A: len(A._data)


@overload_attribute(FloatingArrayType, 'nbytes')
def float_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._null_bitmap.nbytes


@overload_method(FloatingArrayType, 'copy', no_unliteral=True)
def overload_float_arr_copy(A, dtype=None):
    if not is_overload_none(dtype):
        return lambda A, dtype=None: A.astype(dtype, copy=True)
    else:
        return lambda A, dtype=None: bodo.libs.float_arr_ext.init_float_array(
            bodo.libs.float_arr_ext.get_float_arr_data(A).copy(), bodo.libs
            .float_arr_ext.get_float_arr_bitmap(A).copy())


@overload_method(FloatingArrayType, 'astype', no_unliteral=True)
def overload_float_arr_astype(A, dtype, copy=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "FloatingArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    if isinstance(dtype, types.NumberClass):
        dtype = dtype.dtype
    if isinstance(dtype, FloatDtype) and A.dtype == dtype.dtype:
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
    if isinstance(dtype, FloatDtype):
        np_dtype = dtype.dtype
        return (lambda A, dtype, copy=True: bodo.libs.float_arr_ext.
            init_float_array(bodo.libs.float_arr_ext.get_float_arr_data(A).
            astype(np_dtype), bodo.libs.float_arr_ext.get_float_arr_bitmap(
            A).copy()))
    if isinstance(dtype, bodo.libs.int_arr_ext.IntDtype):
        np_dtype = dtype.dtype
        return (lambda A, dtype, copy=True: bodo.libs.int_arr_ext.
            init_integer_array(bodo.libs.float_arr_ext.get_float_arr_data(A
            ).astype(np_dtype), bodo.libs.float_arr_ext.
            get_float_arr_bitmap(A).copy()))
    nb_dtype = parse_dtype(dtype, 'FloatingArray.astype')
    if isinstance(nb_dtype, types.Float):

        def impl_float(A, dtype, copy=True):
            data = bodo.libs.float_arr_ext.get_float_arr_data(A)
            n = len(data)
            bgaku__iec = np.empty(n, nb_dtype)
            for sdv__jkq in numba.parfors.parfor.internal_prange(n):
                bgaku__iec[sdv__jkq] = data[sdv__jkq]
                if bodo.libs.array_kernels.isna(A, sdv__jkq):
                    bgaku__iec[sdv__jkq] = np.nan
            return bgaku__iec
        return impl_float
    return (lambda A, dtype, copy=True: bodo.libs.float_arr_ext.
        get_float_arr_data(A).astype(nb_dtype))


ufunc_aliases = {'subtract': 'sub', 'multiply': 'mul', 'floor_divide':
    'floordiv', 'true_divide': 'truediv', 'power': 'pow', 'remainder':
    'mod', 'divide': 'div', 'equal': 'eq', 'not_equal': 'ne', 'less': 'lt',
    'less_equal': 'le', 'greater': 'gt', 'greater_equal': 'ge'}


def create_op_overload(op, n_inputs):
    if n_inputs == 1:

        def overload_float_arr_op_nin_1(A):
            if isinstance(A, FloatingArrayType):
                return bodo.libs.int_arr_ext.get_nullable_array_unary_impl(op,
                    A)
        return overload_float_arr_op_nin_1
    elif n_inputs == 2:

        def overload_series_op_nin_2(lhs, rhs):
            if isinstance(lhs, FloatingArrayType) or isinstance(rhs,
                FloatingArrayType):
                return bodo.libs.int_arr_ext.get_nullable_array_binary_impl(op,
                    lhs, rhs)
        return overload_series_op_nin_2
    else:
        raise RuntimeError(
            "Don't know how to register ufuncs from ufunc_db with arity > 2")


def _install_np_ufuncs():
    import numba.np.ufunc_db
    for suci__cqahc in numba.np.ufunc_db.get_ufuncs():
        xirn__rtev = create_op_overload(suci__cqahc, suci__cqahc.nin)
        overload(suci__cqahc, no_unliteral=True)(xirn__rtev)


_install_np_ufuncs()
skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesArrayOperator._op_map.keys():
        if op in skips:
            continue
        xirn__rtev = create_op_overload(op, 2)
        overload(op)(xirn__rtev)


_install_binary_ops()


def _install_inplace_binary_ops():
    for op in numba.core.typing.npydecl.NumpyRulesInplaceArrayOperator._op_map.keys(
        ):
        xirn__rtev = create_op_overload(op, 2)
        overload(op, no_unliteral=True)(xirn__rtev)


_install_inplace_binary_ops()


def _install_unary_ops():
    for op in (operator.neg, operator.invert, operator.pos):
        xirn__rtev = create_op_overload(op, 1)
        overload(op, no_unliteral=True)(xirn__rtev)


_install_unary_ops()


@overload_method(FloatingArrayType, 'sum', no_unliteral=True)
def overload_float_arr_sum(A, skipna=True, min_count=0):
    daan__svulg = dict(skipna=skipna, min_count=min_count)
    zsrnr__dzhzc = dict(skipna=True, min_count=0)
    check_unsupported_args('FloatingArray.sum', daan__svulg, zsrnr__dzhzc)

    def impl(A, skipna=True, min_count=0):
        numba.parfors.parfor.init_prange()
        s = 0.0
        for sdv__jkq in numba.parfors.parfor.internal_prange(len(A)):
            val = 0.0
            if not bodo.libs.array_kernels.isna(A, sdv__jkq):
                val = A[sdv__jkq]
            s += val
        return s
    return impl


@overload_method(FloatingArrayType, 'unique', no_unliteral=True)
def overload_unique(A):
    dtype = A.dtype

    def impl_float_arr(A):
        data = []
        wrbyk__elfjm = []
        sddma__dxsk = False
        s = set()
        for sdv__jkq in range(len(A)):
            val = A[sdv__jkq]
            if bodo.libs.array_kernels.isna(A, sdv__jkq):
                if not sddma__dxsk:
                    data.append(dtype(1))
                    wrbyk__elfjm.append(False)
                    sddma__dxsk = True
                continue
            if val not in s:
                s.add(val)
                data.append(val)
                wrbyk__elfjm.append(True)
        alq__fhtj = np.array(data)
        n = len(alq__fhtj)
        zonr__bkjfd = n + 7 >> 3
        psh__gkv = np.empty(zonr__bkjfd, np.uint8)
        for seuam__drk in range(n):
            bodo.libs.int_arr_ext.set_bit_to_arr(psh__gkv, seuam__drk,
                wrbyk__elfjm[seuam__drk])
        return init_float_array(alq__fhtj, psh__gkv)
    return impl_float_arr
