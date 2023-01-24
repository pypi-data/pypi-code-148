"""
Array of intervals corresponding to IntervalArray of Pandas.
Used for IntervalIndex, which is necessary for Series.value_counts() with 'bins'
argument.
"""
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo


class IntervalType(types.Type):

    def __init__(self):
        super(IntervalType, self).__init__('IntervalType()')


class IntervalArrayType(types.ArrayCompatible):

    def __init__(self, arr_type):
        self.arr_type = arr_type
        self.dtype = IntervalType()
        super(IntervalArrayType, self).__init__(name=
            f'IntervalArrayType({arr_type})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return IntervalArrayType(self.arr_type)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(IntervalArrayType)
class IntervalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zxqg__ctqpv = [('left', fe_type.arr_type), ('right', fe_type.arr_type)]
        models.StructModel.__init__(self, dmm, fe_type, zxqg__ctqpv)


make_attribute_wrapper(IntervalArrayType, 'left', '_left')
make_attribute_wrapper(IntervalArrayType, 'right', '_right')


@typeof_impl.register(pd.arrays.IntervalArray)
def typeof_interval_array(val, c):
    arr_type = bodo.typeof(val._left)
    return IntervalArrayType(arr_type)


@intrinsic
def init_interval_array(typingctx, left, right=None):
    assert left == right, 'Interval left/right array types should be the same'

    def codegen(context, builder, signature, args):
        qep__jmu, dch__kqm = args
        loug__ayys = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        loug__ayys.left = qep__jmu
        loug__ayys.right = dch__kqm
        context.nrt.incref(builder, signature.args[0], qep__jmu)
        context.nrt.incref(builder, signature.args[1], dch__kqm)
        return loug__ayys._getvalue()
    gsgml__jkh = IntervalArrayType(left)
    jzmq__ehho = gsgml__jkh(left, right)
    return jzmq__ehho, codegen


def init_interval_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    bnec__qodj = []
    for vmw__rlyxf in args:
        sql__togn = equiv_set.get_shape(vmw__rlyxf)
        if sql__togn is not None:
            bnec__qodj.append(sql__togn[0])
    if len(bnec__qodj) > 1:
        equiv_set.insert_equiv(*bnec__qodj)
    left = args[0]
    if equiv_set.has_shape(left):
        return ArrayAnalysis.AnalyzeResult(shape=left, pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_libs_interval_arr_ext_init_interval_array
    ) = init_interval_array_equiv


def alias_ext_init_interval_array(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 2
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_interval_array',
    'bodo.libs.int_arr_ext'] = alias_ext_init_interval_array


@box(IntervalArrayType)
def box_interval_arr(typ, val, c):
    loug__ayys = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, typ.arr_type, loug__ayys.left)
    lym__dvt = c.pyapi.from_native_value(typ.arr_type, loug__ayys.left, c.
        env_manager)
    c.context.nrt.incref(c.builder, typ.arr_type, loug__ayys.right)
    mfkzg__gkj = c.pyapi.from_native_value(typ.arr_type, loug__ayys.right,
        c.env_manager)
    zarjv__hlvu = c.context.insert_const_string(c.builder.module, 'pandas')
    ovzx__zqz = c.pyapi.import_module_noblock(zarjv__hlvu)
    kizgm__ltueh = c.pyapi.object_getattr_string(ovzx__zqz, 'arrays')
    lktu__anmig = c.pyapi.object_getattr_string(kizgm__ltueh, 'IntervalArray')
    wsvkv__ubeo = c.pyapi.call_method(lktu__anmig, 'from_arrays', (lym__dvt,
        mfkzg__gkj))
    c.pyapi.decref(lym__dvt)
    c.pyapi.decref(mfkzg__gkj)
    c.pyapi.decref(ovzx__zqz)
    c.pyapi.decref(kizgm__ltueh)
    c.pyapi.decref(lktu__anmig)
    c.context.nrt.decref(c.builder, typ, val)
    return wsvkv__ubeo


@unbox(IntervalArrayType)
def unbox_interval_arr(typ, val, c):
    lym__dvt = c.pyapi.object_getattr_string(val, '_left')
    left = c.pyapi.to_native_value(typ.arr_type, lym__dvt).value
    c.pyapi.decref(lym__dvt)
    mfkzg__gkj = c.pyapi.object_getattr_string(val, '_right')
    right = c.pyapi.to_native_value(typ.arr_type, mfkzg__gkj).value
    c.pyapi.decref(mfkzg__gkj)
    loug__ayys = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    loug__ayys.left = left
    loug__ayys.right = right
    pdeiw__gez = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(loug__ayys._getvalue(), is_error=pdeiw__gez)


@overload(len, no_unliteral=True)
def overload_interval_arr_len(A):
    if isinstance(A, IntervalArrayType):
        return lambda A: len(A._left)


@overload_attribute(IntervalArrayType, 'shape')
def overload_interval_arr_shape(A):
    return lambda A: (len(A._left),)


@overload_attribute(IntervalArrayType, 'ndim')
def overload_interval_arr_ndim(A):
    return lambda A: 1


@overload_attribute(IntervalArrayType, 'nbytes')
def overload_interval_arr_nbytes(A):
    return lambda A: A._left.nbytes + A._right.nbytes


@overload_method(IntervalArrayType, 'copy', no_unliteral=True)
def overload_interval_arr_copy(A):
    return lambda A: bodo.libs.interval_arr_ext.init_interval_array(A._left
        .copy(), A._right.copy())
