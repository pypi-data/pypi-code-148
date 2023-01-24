"""
Collection of utility functions. Needs to be refactored in separate files.
"""
import hashlib
import inspect
import keyword
import re
import warnings
from enum import Enum
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from mpi4py import MPI
from numba.core import cgutils, ir, ir_utils, types
from numba.core.imputils import lower_builtin, lower_constant
from numba.core.ir_utils import find_callname, find_const, get_definition, guard, mk_unique_var, require
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, overload
from numba.np.arrayobj import get_itemsize, make_array, populate_array
from numba.np.numpy_support import as_dtype
import bodo
from bodo.hiframes.time_ext import TimeArrayType
from bodo.libs.binary_arr_ext import bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import num_total_chars, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import string_type
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.typing import NOT_CONSTANT, BodoError, BodoWarning, MetaType, is_str_arr_type
int128_type = types.Integer('int128', 128)


class CTypeEnum(Enum):
    Int8 = 0
    UInt8 = 1
    Int32 = 2
    UInt32 = 3
    Int64 = 4
    UInt64 = 7
    Float32 = 5
    Float64 = 6
    Int16 = 8
    UInt16 = 9
    STRING = 10
    Bool = 11
    Decimal = 12
    Date = 13
    Time = 14
    Datetime = 15
    Timedelta = 16
    Int128 = 17
    LIST = 19
    STRUCT = 20
    BINARY = 21


_numba_to_c_type_map = {types.int8: CTypeEnum.Int8.value, types.uint8:
    CTypeEnum.UInt8.value, types.int32: CTypeEnum.Int32.value, types.uint32:
    CTypeEnum.UInt32.value, types.int64: CTypeEnum.Int64.value, types.
    uint64: CTypeEnum.UInt64.value, types.float32: CTypeEnum.Float32.value,
    types.float64: CTypeEnum.Float64.value, types.NPDatetime('ns'):
    CTypeEnum.Datetime.value, types.NPTimedelta('ns'): CTypeEnum.Timedelta.
    value, types.bool_: CTypeEnum.Bool.value, types.int16: CTypeEnum.Int16.
    value, types.uint16: CTypeEnum.UInt16.value, int128_type: CTypeEnum.
    Int128.value}
numba.core.errors.error_extras = {'unsupported_error': '', 'typing': '',
    'reportable': '', 'interpreter': '', 'constant_inference': ''}
np_alloc_callnames = 'empty', 'zeros', 'ones', 'full'
CONST_DICT_SLOW_WARN_THRESHOLD = 100
CONST_LIST_SLOW_WARN_THRESHOLD = 100000


def unliteral_all(args):
    return tuple(types.unliteral(a) for a in args)


def get_constant(func_ir, var, default=NOT_CONSTANT):
    doo__ggmns = guard(get_definition, func_ir, var)
    if doo__ggmns is None:
        return default
    if isinstance(doo__ggmns, ir.Const):
        return doo__ggmns.value
    if isinstance(doo__ggmns, ir.Var):
        return get_constant(func_ir, doo__ggmns, default)
    return default


def numba_to_c_type(t):
    if isinstance(t, bodo.libs.decimal_arr_ext.Decimal128Type):
        return CTypeEnum.Decimal.value
    if t == bodo.hiframes.datetime_date_ext.datetime_date_type:
        return CTypeEnum.Date.value
    if isinstance(t, bodo.hiframes.time_ext.TimeType):
        return CTypeEnum.Time.value
    return _numba_to_c_type_map[t]


def is_alloc_callname(func_name, mod_name):
    return isinstance(mod_name, str) and (mod_name == 'numpy' and func_name in
        np_alloc_callnames or func_name == 'empty_inferred' and mod_name in
        ('numba.extending', 'numba.np.unsafe.ndarray') or func_name ==
        'pre_alloc_string_array' and mod_name == 'bodo.libs.str_arr_ext' or
        func_name == 'pre_alloc_binary_array' and mod_name ==
        'bodo.libs.binary_arr_ext' or func_name ==
        'alloc_random_access_string_array' and mod_name ==
        'bodo.libs.str_ext' or func_name == 'pre_alloc_array_item_array' and
        mod_name == 'bodo.libs.array_item_arr_ext' or func_name ==
        'pre_alloc_struct_array' and mod_name == 'bodo.libs.struct_arr_ext' or
        func_name == 'pre_alloc_map_array' and mod_name ==
        'bodo.libs.map_arr_ext' or func_name == 'pre_alloc_tuple_array' and
        mod_name == 'bodo.libs.tuple_arr_ext' or func_name ==
        'alloc_bool_array' and mod_name == 'bodo.libs.bool_arr_ext' or 
        func_name == 'alloc_int_array' and mod_name ==
        'bodo.libs.int_arr_ext' or func_name == 'alloc_float_array' and 
        mod_name == 'bodo.libs.float_arr_ext' or func_name ==
        'alloc_datetime_date_array' and mod_name ==
        'bodo.hiframes.datetime_date_ext' or func_name ==
        'alloc_datetime_timedelta_array' and mod_name ==
        'bodo.hiframes.datetime_timedelta_ext' or func_name ==
        'alloc_decimal_array' and mod_name == 'bodo.libs.decimal_arr_ext' or
        func_name == 'alloc_categorical_array' and mod_name ==
        'bodo.hiframes.pd_categorical_ext' or func_name == 'gen_na_array' and
        mod_name == 'bodo.libs.array_kernels' or func_name ==
        'alloc_pd_datetime_array' and mod_name ==
        'bodo.libs.pd_datetime_arr_ext')


def find_build_tuple(func_ir, var):
    require(isinstance(var, (ir.Var, str)))
    cvos__ciyn = get_definition(func_ir, var)
    require(isinstance(cvos__ciyn, ir.Expr))
    require(cvos__ciyn.op == 'build_tuple')
    return cvos__ciyn.items


def cprint(*s):
    print(*s)


@infer_global(cprint)
class CprintInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.none, *unliteral_all(args))


typ_to_format = {types.int32: 'd', types.uint32: 'u', types.int64: 'lld',
    types.uint64: 'llu', types.float32: 'f', types.float64: 'lf', types.
    voidptr: 's'}


@lower_builtin(cprint, types.VarArg(types.Any))
def cprint_lower(context, builder, sig, args):
    for vudx__noggw, val in enumerate(args):
        typ = sig.args[vudx__noggw]
        if isinstance(typ, types.ArrayCTypes):
            cgutils.printf(builder, '%p ', val)
            continue
        jdmd__bha = typ_to_format[typ]
        cgutils.printf(builder, '%{} '.format(jdmd__bha), val)
    cgutils.printf(builder, '\n')
    return context.get_dummy_value()


def is_whole_slice(typemap, func_ir, var, accept_stride=False):
    require(typemap[var.name] == types.slice2_type or accept_stride and 
        typemap[var.name] == types.slice3_type)
    gnx__fmqo = get_definition(func_ir, var)
    require(isinstance(gnx__fmqo, ir.Expr) and gnx__fmqo.op == 'call')
    assert len(gnx__fmqo.args) == 2 or accept_stride and len(gnx__fmqo.args
        ) == 3
    assert find_callname(func_ir, gnx__fmqo) == ('slice', 'builtins')
    dos__sxvx = get_definition(func_ir, gnx__fmqo.args[0])
    izipn__acqw = get_definition(func_ir, gnx__fmqo.args[1])
    require(isinstance(dos__sxvx, ir.Const) and dos__sxvx.value == None)
    require(isinstance(izipn__acqw, ir.Const) and izipn__acqw.value == None)
    return True


def is_slice_equiv_arr(arr_var, index_var, func_ir, equiv_set,
    accept_stride=False):
    pjj__zihc = get_definition(func_ir, index_var)
    require(find_callname(func_ir, pjj__zihc) == ('slice', 'builtins'))
    require(len(pjj__zihc.args) in (2, 3))
    require(find_const(func_ir, pjj__zihc.args[0]) in (0, None))
    require(equiv_set.is_equiv(pjj__zihc.args[1], arr_var.name + '#0'))
    require(accept_stride or len(pjj__zihc.args) == 2 or find_const(func_ir,
        pjj__zihc.args[2]) == 1)
    return True


def get_slice_step(typemap, func_ir, var):
    require(typemap[var.name] == types.slice3_type)
    gnx__fmqo = get_definition(func_ir, var)
    require(isinstance(gnx__fmqo, ir.Expr) and gnx__fmqo.op == 'call')
    assert len(gnx__fmqo.args) == 3
    return gnx__fmqo.args[2]


def is_array_typ(var_typ, include_index_series=True):
    return is_np_array_typ(var_typ) or var_typ in (string_array_type, bodo.
        binary_array_type, bodo.dict_str_arr_type, bodo.hiframes.split_impl
        .string_array_split_view_type, bodo.hiframes.datetime_date_ext.
        datetime_date_array_type, bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_array_type, boolean_array, bodo.libs.str_ext.
        random_access_string_array, bodo.libs.interval_arr_ext.
        IntervalArrayType) or isinstance(var_typ, (IntegerArrayType,
        FloatingArrayType, bodo.libs.decimal_arr_ext.DecimalArrayType, bodo
        .hiframes.pd_categorical_ext.CategoricalArrayType, bodo.libs.
        array_item_arr_ext.ArrayItemArrayType, bodo.libs.struct_arr_ext.
        StructArrayType, bodo.libs.interval_arr_ext.IntervalArrayType, bodo
        .libs.tuple_arr_ext.TupleArrayType, bodo.libs.map_arr_ext.
        MapArrayType, bodo.libs.csr_matrix_ext.CSRMatrixType, bodo.
        DatetimeArrayType, TimeArrayType)) or include_index_series and (
        isinstance(var_typ, (bodo.hiframes.pd_series_ext.SeriesType, bodo.
        hiframes.pd_multi_index_ext.MultiIndexType)) or bodo.hiframes.
        pd_index_ext.is_pd_index_type(var_typ))


def is_np_array_typ(var_typ):
    return isinstance(var_typ, types.Array)


def is_distributable_typ(var_typ):
    return is_array_typ(var_typ) or isinstance(var_typ, bodo.hiframes.table
        .TableType) or isinstance(var_typ, bodo.hiframes.pd_dataframe_ext.
        DataFrameType) or isinstance(var_typ, types.List
        ) and is_distributable_typ(var_typ.dtype) or isinstance(var_typ,
        types.DictType) and is_distributable_typ(var_typ.value_type)


def is_distributable_tuple_typ(var_typ):
    try:
        from bodosql.context_ext import BodoSQLContextType
    except ImportError as tqtgb__ptcq:
        BodoSQLContextType = None
    return isinstance(var_typ, types.BaseTuple) and any(
        is_distributable_typ(t) or is_distributable_tuple_typ(t) for t in
        var_typ.types) or isinstance(var_typ, types.List
        ) and is_distributable_tuple_typ(var_typ.dtype) or isinstance(var_typ,
        types.DictType) and is_distributable_tuple_typ(var_typ.value_type
        ) or isinstance(var_typ, types.iterators.EnumerateType) and (
        is_distributable_typ(var_typ.yield_type[1]) or
        is_distributable_tuple_typ(var_typ.yield_type[1])
        ) or BodoSQLContextType is not None and isinstance(var_typ,
        BodoSQLContextType) and any([is_distributable_typ(jhl__yksu) for
        jhl__yksu in var_typ.dataframes])


@numba.generated_jit(nopython=True, cache=True)
def build_set_seen_na(A):

    def impl(A):
        s = dict()
        shp__iukh = False
        for vudx__noggw in range(len(A)):
            if bodo.libs.array_kernels.isna(A, vudx__noggw):
                shp__iukh = True
                continue
            s[A[vudx__noggw]] = 0
        return s, shp__iukh
    return impl


def empty_like_type(n, arr):
    return np.empty(n, arr.dtype)


@overload(empty_like_type, no_unliteral=True)
def empty_like_type_overload(n, arr):
    if isinstance(arr, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return (lambda n, arr: bodo.hiframes.pd_categorical_ext.
            alloc_categorical_array(n, arr.dtype))
    if isinstance(arr, types.Array):
        return lambda n, arr: np.empty(n, arr.dtype)
    if isinstance(arr, types.List) and arr.dtype == string_type:

        def empty_like_type_str_list(n, arr):
            return [''] * n
        return empty_like_type_str_list
    if isinstance(arr, types.List) and arr.dtype == bytes_type:

        def empty_like_type_binary_list(n, arr):
            return [b''] * n
        return empty_like_type_binary_list
    if isinstance(arr, IntegerArrayType):
        wajrn__lovol = arr.dtype

        def empty_like_type_int_arr(n, arr):
            return bodo.libs.int_arr_ext.alloc_int_array(n, wajrn__lovol)
        return empty_like_type_int_arr
    if isinstance(arr, FloatingArrayType):
        wajrn__lovol = arr.dtype

        def empty_like_type_float_arr(n, arr):
            return bodo.libs.float_arr_ext.alloc_float_array(n, wajrn__lovol)
        return empty_like_type_float_arr
    if arr == boolean_array:

        def empty_like_type_bool_arr(n, arr):
            return bodo.libs.bool_arr_ext.alloc_bool_array(n)
        return empty_like_type_bool_arr
    if arr == bodo.hiframes.datetime_date_ext.datetime_date_array_type:

        def empty_like_type_datetime_date_arr(n, arr):
            return bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(n)
        return empty_like_type_datetime_date_arr
    if isinstance(arr, bodo.hiframes.time_ext.TimeArrayType):
        precision = arr.precision

        def empty_like_type_time_arr(n, arr):
            return bodo.hiframes.time_ext.alloc_time_array(n, precision)
        return empty_like_type_time_arr
    if (arr == bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_array_type):

        def empty_like_type_datetime_timedelta_arr(n, arr):
            return (bodo.hiframes.datetime_timedelta_ext.
                alloc_datetime_timedelta_array(n))
        return empty_like_type_datetime_timedelta_arr
    if isinstance(arr, bodo.libs.decimal_arr_ext.DecimalArrayType):
        precision = arr.precision
        scale = arr.scale

        def empty_like_type_decimal_arr(n, arr):
            return bodo.libs.decimal_arr_ext.alloc_decimal_array(n,
                precision, scale)
        return empty_like_type_decimal_arr
    assert arr == string_array_type

    def empty_like_type_str_arr(n, arr):
        bgdop__swvvh = 20
        if len(arr) != 0:
            bgdop__swvvh = num_total_chars(arr) // len(arr)
        return pre_alloc_string_array(n, n * bgdop__swvvh)
    return empty_like_type_str_arr


def _empty_nd_impl(context, builder, arrtype, shapes):
    acdm__apb = make_array(arrtype)
    qulz__vqb = acdm__apb(context, builder)
    ihxg__xsyzj = context.get_data_type(arrtype.dtype)
    ncrvg__iclff = context.get_constant(types.intp, get_itemsize(context,
        arrtype))
    dvehv__ftj = context.get_constant(types.intp, 1)
    puch__ssjnx = lir.Constant(lir.IntType(1), 0)
    for s in shapes:
        aiyqw__dng = builder.smul_with_overflow(dvehv__ftj, s)
        dvehv__ftj = builder.extract_value(aiyqw__dng, 0)
        puch__ssjnx = builder.or_(puch__ssjnx, builder.extract_value(
            aiyqw__dng, 1))
    if arrtype.ndim == 0:
        kbyg__mbvd = ()
    elif arrtype.layout == 'C':
        kbyg__mbvd = [ncrvg__iclff]
        for mtzld__dbrx in reversed(shapes[1:]):
            kbyg__mbvd.append(builder.mul(kbyg__mbvd[-1], mtzld__dbrx))
        kbyg__mbvd = tuple(reversed(kbyg__mbvd))
    elif arrtype.layout == 'F':
        kbyg__mbvd = [ncrvg__iclff]
        for mtzld__dbrx in shapes[:-1]:
            kbyg__mbvd.append(builder.mul(kbyg__mbvd[-1], mtzld__dbrx))
        kbyg__mbvd = tuple(kbyg__mbvd)
    else:
        raise NotImplementedError(
            "Don't know how to allocate array with layout '{0}'.".format(
            arrtype.layout))
    yca__zizs = builder.smul_with_overflow(dvehv__ftj, ncrvg__iclff)
    gpnl__czedd = builder.extract_value(yca__zizs, 0)
    puch__ssjnx = builder.or_(puch__ssjnx, builder.extract_value(yca__zizs, 1))
    with builder.if_then(puch__ssjnx, likely=False):
        cgutils.printf(builder,
            'array is too big; `arr.size * arr.dtype.itemsize` is larger than the maximum possible size.'
            )
    dtype = arrtype.dtype
    sfz__ufh = context.get_preferred_array_alignment(dtype)
    pqzpr__tslwy = context.get_constant(types.uint32, sfz__ufh)
    jfai__aoiq = context.nrt.meminfo_alloc_aligned(builder, size=
        gpnl__czedd, align=pqzpr__tslwy)
    data = context.nrt.meminfo_data(builder, jfai__aoiq)
    jrnv__rardf = context.get_value_type(types.intp)
    goyba__qpuzl = cgutils.pack_array(builder, shapes, ty=jrnv__rardf)
    dsyex__dnt = cgutils.pack_array(builder, kbyg__mbvd, ty=jrnv__rardf)
    populate_array(qulz__vqb, data=builder.bitcast(data, ihxg__xsyzj.
        as_pointer()), shape=goyba__qpuzl, strides=dsyex__dnt, itemsize=
        ncrvg__iclff, meminfo=jfai__aoiq)
    return qulz__vqb


if bodo.numba_compat._check_numba_change:
    lines = inspect.getsource(numba.np.arrayobj._empty_nd_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b6a998927680caa35917a553c79704e9d813d8f1873d83a5f8513837c159fa29':
        warnings.warn('numba.np.arrayobj._empty_nd_impl has changed')


def alloc_arr_tup(n, arr_tup, init_vals=()):
    hkcnb__scx = []
    for rgp__qfaz in arr_tup:
        hkcnb__scx.append(np.empty(n, rgp__qfaz.dtype))
    return tuple(hkcnb__scx)


@overload(alloc_arr_tup, no_unliteral=True)
def alloc_arr_tup_overload(n, data, init_vals=()):
    vwwa__cvvj = data.count
    rel__ihym = ','.join(['empty_like_type(n, data[{}])'.format(vudx__noggw
        ) for vudx__noggw in range(vwwa__cvvj)])
    if init_vals != ():
        rel__ihym = ','.join(['np.full(n, init_vals[{}], data[{}].dtype)'.
            format(vudx__noggw, vudx__noggw) for vudx__noggw in range(
            vwwa__cvvj)])
    ela__bmbl = 'def f(n, data, init_vals=()):\n'
    ela__bmbl += '  return ({}{})\n'.format(rel__ihym, ',' if vwwa__cvvj ==
        1 else '')
    nznef__vzc = {}
    exec(ela__bmbl, {'empty_like_type': empty_like_type, 'np': np}, nznef__vzc)
    rrz__rsx = nznef__vzc['f']
    return rrz__rsx


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def tuple_to_scalar(n):
    if isinstance(n, types.BaseTuple) and len(n.types) == 1:
        return lambda n: n[0]
    return lambda n: n


def create_categorical_type(categories, data, is_ordered):
    if data == bodo.string_array_type or bodo.utils.typing.is_dtype_nullable(
        data):
        new_cats_arr = pd.CategoricalDtype(pd.array(categories), is_ordered
            ).categories.array
        if isinstance(data.dtype, types.Number):
            new_cats_arr = new_cats_arr.astype(data.
                get_pandas_scalar_type_instance)
    else:
        new_cats_arr = pd.CategoricalDtype(categories, is_ordered
            ).categories.values
        if isinstance(data.dtype, types.Number):
            new_cats_arr = new_cats_arr.astype(as_dtype(data.dtype))
    return new_cats_arr


def alloc_type(n, t, s=None):
    return np.empty(n, t.dtype)


@overload(alloc_type)
def overload_alloc_type(n, t, s=None):
    typ = t.instance_type if isinstance(t, types.TypeRef) else t
    if is_str_arr_type(typ):
        return (lambda n, t, s=None: bodo.libs.str_arr_ext.
            pre_alloc_string_array(n, s[0]))
    if typ == bodo.binary_array_type:
        return (lambda n, t, s=None: bodo.libs.binary_arr_ext.
            pre_alloc_binary_array(n, s[0]))
    if isinstance(typ, bodo.libs.array_item_arr_ext.ArrayItemArrayType):
        dtype = typ.dtype
        return (lambda n, t, s=None: bodo.libs.array_item_arr_ext.
            pre_alloc_array_item_array(n, s, dtype))
    if isinstance(typ, bodo.libs.struct_arr_ext.StructArrayType):
        dtypes = typ.data
        names = typ.names
        return (lambda n, t, s=None: bodo.libs.struct_arr_ext.
            pre_alloc_struct_array(n, s, dtypes, names))
    if isinstance(typ, bodo.libs.map_arr_ext.MapArrayType):
        struct_typ = bodo.libs.struct_arr_ext.StructArrayType((typ.
            key_arr_type, typ.value_arr_type), ('key', 'value'))
        return lambda n, t, s=None: bodo.libs.map_arr_ext.pre_alloc_map_array(n
            , s, struct_typ)
    if isinstance(typ, bodo.libs.tuple_arr_ext.TupleArrayType):
        dtypes = typ.data
        return (lambda n, t, s=None: bodo.libs.tuple_arr_ext.
            pre_alloc_tuple_array(n, s, dtypes))
    if isinstance(typ, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        if isinstance(t, types.TypeRef):
            if typ.dtype.categories is None:
                raise BodoError(
                    'UDFs or Groupbys that return Categorical values must have categories known at compile time.'
                    )
            is_ordered = typ.dtype.ordered
            int_type = typ.dtype.int_type
            new_cats_arr = create_categorical_type(typ.dtype.categories,
                typ.dtype.data.data, is_ordered)
            new_cats_tup = MetaType(tuple(new_cats_arr))
            return (lambda n, t, s=None: bodo.hiframes.pd_categorical_ext.
                alloc_categorical_array(n, bodo.hiframes.pd_categorical_ext
                .init_cat_dtype(bodo.utils.conversion.index_from_array(
                new_cats_arr), is_ordered, int_type, new_cats_tup)))
        else:
            return (lambda n, t, s=None: bodo.hiframes.pd_categorical_ext.
                alloc_categorical_array(n, t.dtype))
    if typ.dtype == bodo.hiframes.datetime_date_ext.datetime_date_type:
        return (lambda n, t, s=None: bodo.hiframes.datetime_date_ext.
            alloc_datetime_date_array(n))
    if isinstance(typ.dtype, bodo.hiframes.time_ext.TimeType):
        precision = typ.dtype.precision
        return lambda n, t, s=None: bodo.hiframes.time_ext.alloc_time_array(n,
            precision)
    if (typ.dtype == bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_type):
        return (lambda n, t, s=None: bodo.hiframes.datetime_timedelta_ext.
            alloc_datetime_timedelta_array(n))
    if isinstance(typ, DecimalArrayType):
        precision = typ.dtype.precision
        scale = typ.dtype.scale
        return (lambda n, t, s=None: bodo.libs.decimal_arr_ext.
            alloc_decimal_array(n, precision, scale))
    if isinstance(typ, bodo.DatetimeArrayType):
        tz_literal = typ.tz
        return (lambda n, t, s=None: bodo.libs.pd_datetime_arr_ext.
            alloc_pd_datetime_array(n, tz_literal))
    dtype = numba.np.numpy_support.as_dtype(typ.dtype)
    if isinstance(typ, IntegerArrayType):
        return lambda n, t, s=None: bodo.libs.int_arr_ext.alloc_int_array(n,
            dtype)
    if isinstance(typ, FloatingArrayType):
        return lambda n, t, s=None: bodo.libs.float_arr_ext.alloc_float_array(n
            , dtype)
    if typ == boolean_array:
        return lambda n, t, s=None: bodo.libs.bool_arr_ext.alloc_bool_array(n)
    return lambda n, t, s=None: np.empty(n, dtype)


def astype(A, t):
    return A.astype(t.dtype)


@overload(astype, no_unliteral=True)
def overload_astype(A, t):
    typ = t.instance_type if isinstance(t, types.TypeRef) else t
    dtype = typ.dtype
    if A == typ:
        return lambda A, t: A
    if isinstance(A, (types.Array, IntegerArrayType, FloatingArrayType)
        ) and isinstance(typ, types.Array):
        return lambda A, t: A.astype(dtype)
    if isinstance(typ, IntegerArrayType):
        return lambda A, t: bodo.libs.int_arr_ext.init_integer_array(A.
            astype(dtype), np.full(len(A) + 7 >> 3, 255, np.uint8))
    if isinstance(typ, FloatingArrayType):
        return lambda A, t: bodo.libs.float_arr_ext.init_float_array(A.
            astype(dtype), np.full(len(A) + 7 >> 3, 255, np.uint8))
    if (A == bodo.libs.dict_arr_ext.dict_str_arr_type and typ == bodo.
        string_array_type):
        return lambda A, t: bodo.utils.typing.decode_if_dict_array(A)
    raise BodoError(f'cannot convert array type {A} to {typ}')


def full_type(n, val, t):
    return np.full(n, val, t.dtype)


@overload(full_type, no_unliteral=True)
def overload_full_type(n, val, t):
    typ = t.instance_type if isinstance(t, types.TypeRef) else t
    if isinstance(typ, types.Array):
        dtype = numba.np.numpy_support.as_dtype(typ.dtype)
        return lambda n, val, t: np.full(n, val, dtype)
    if isinstance(typ, IntegerArrayType):
        dtype = numba.np.numpy_support.as_dtype(typ.dtype)
        return lambda n, val, t: bodo.libs.int_arr_ext.init_integer_array(np
            .full(n, val, dtype), np.full(tuple_to_scalar(n) + 7 >> 3, 255,
            np.uint8))
    if isinstance(typ, FloatingArrayType):
        dtype = numba.np.numpy_support.as_dtype(typ.dtype)
        return lambda n, val, t: bodo.libs.float_arr_ext.init_float_array(np
            .full(n, val, dtype), np.full(tuple_to_scalar(n) + 7 >> 3, 255,
            np.uint8))
    if typ == boolean_array:
        return lambda n, val, t: bodo.libs.bool_arr_ext.init_bool_array(np.
            full(n, val, np.bool_), np.full(tuple_to_scalar(n) + 7 >> 3, 
            255, np.uint8))
    if typ == string_array_type:

        def impl_str(n, val, t):
            wyw__moryq = n * bodo.libs.str_arr_ext.get_utf8_size(val)
            A = pre_alloc_string_array(n, wyw__moryq)
            for vudx__noggw in range(n):
                A[vudx__noggw] = val
            return A
        return impl_str

    def impl(n, val, t):
        A = alloc_type(n, typ, (-1,))
        for vudx__noggw in range(n):
            A[vudx__noggw] = val
        return A
    return impl


@intrinsic
def is_null_pointer(typingctx, ptr_typ=None):

    def codegen(context, builder, signature, args):
        ysg__jyqy, = args
        hyqh__mpie = context.get_constant_null(ptr_typ)
        return builder.icmp_unsigned('==', ysg__jyqy, hyqh__mpie)
    return types.bool_(ptr_typ), codegen


@intrinsic
def is_null_value(typingctx, val_typ=None):

    def codegen(context, builder, signature, args):
        val, = args
        jdlfl__esf = cgutils.alloca_once_value(builder, val)
        csnif__ltxs = cgutils.alloca_once_value(builder, context.
            get_constant_null(val_typ))
        return is_ll_eq(builder, jdlfl__esf, csnif__ltxs)
    return types.bool_(val_typ), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def tuple_list_to_array(A, data, elem_type):
    elem_type = elem_type.instance_type if isinstance(elem_type, types.TypeRef
        ) else elem_type
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(A,
        'tuple_list_to_array()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(elem_type,
        'tuple_list_to_array()')
    ela__bmbl = 'def impl(A, data, elem_type):\n'
    ela__bmbl += '  for i, d in enumerate(data):\n'
    if elem_type == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
        ela__bmbl += (
            '    A[i] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(d)\n'
            )
    else:
        ela__bmbl += '    A[i] = d\n'
    nznef__vzc = {}
    exec(ela__bmbl, {'bodo': bodo}, nznef__vzc)
    impl = nznef__vzc['impl']
    return impl


def object_length(c, obj):
    gzcq__xsno = c.context.get_argument_type(types.pyobject)
    pclu__htg = lir.FunctionType(lir.IntType(64), [gzcq__xsno])
    hlzsw__chpc = cgutils.get_or_insert_function(c.builder.module,
        pclu__htg, name='PyObject_Length')
    return c.builder.call(hlzsw__chpc, (obj,))


@intrinsic
def incref(typingctx, data=None):

    def codegen(context, builder, signature, args):
        exhlq__ynaab, = args
        context.nrt.incref(builder, signature.args[0], exhlq__ynaab)
    return types.void(data), codegen


def gen_getitem(out_var, in_var, ind, calltypes, nodes):
    xymlf__uvvi = out_var.loc
    mmsw__mzabg = ir.Expr.static_getitem(in_var, ind, None, xymlf__uvvi)
    calltypes[mmsw__mzabg] = None
    nodes.append(ir.Assign(mmsw__mzabg, out_var, xymlf__uvvi))


def is_static_getsetitem(node):
    return is_expr(node, 'static_getitem') or isinstance(node, ir.StaticSetItem
        )


def get_getsetitem_index_var(node, typemap, nodes):
    index_var = node.index_var if is_static_getsetitem(node) else node.index
    if index_var is None:
        assert is_static_getsetitem(node)
        try:
            uxetu__ircna = types.literal(node.index)
        except:
            uxetu__ircna = numba.typeof(node.index)
        index_var = ir.Var(node.value.scope, ir_utils.mk_unique_var(
            'dummy_index'), node.loc)
        typemap[index_var.name] = uxetu__ircna
        nodes.append(ir.Assign(ir.Const(node.index, node.loc), index_var,
            node.loc))
    return index_var


import copy
ir.Const.__deepcopy__ = lambda self, memo: ir.Const(self.value, copy.
    deepcopy(self.loc))


def is_call_assign(stmt):
    return isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
        ) and stmt.value.op == 'call'


def is_call(expr) ->bool:
    return isinstance(expr, ir.Expr) and expr.op == 'call'


def is_var_assign(inst):
    return isinstance(inst, ir.Assign) and isinstance(inst.value, ir.Var)


def is_assign(inst) ->bool:
    return isinstance(inst, ir.Assign)


def is_expr(val, op) ->bool:
    return isinstance(val, ir.Expr) and val.op == op


def sanitize_varname(varname):
    if isinstance(varname, (tuple, list)):
        varname = '_'.join(sanitize_varname(v) for v in varname)
    varname = str(varname)
    bkw__yopt = re.sub('\\W+', '_', varname)
    if not bkw__yopt or not bkw__yopt[0].isalpha():
        bkw__yopt = '_' + bkw__yopt
    if not bkw__yopt.isidentifier() or keyword.iskeyword(bkw__yopt):
        bkw__yopt = mk_unique_var('new_name').replace('.', '_')
    return bkw__yopt


def dump_node_list(node_list):
    for n in node_list:
        print('   ', n)


def debug_prints():
    return numba.core.config.DEBUG_ARRAY_OPT == 1


@overload(reversed)
def list_reverse(A):
    if isinstance(A, types.List):

        def impl_reversed(A):
            twbe__qfoc = len(A)
            for vudx__noggw in range(twbe__qfoc):
                yield A[twbe__qfoc - 1 - vudx__noggw]
        return impl_reversed


@numba.njit
def count_nonnan(a):
    return np.count_nonzero(~np.isnan(a))


@numba.njit
def nanvar_ddof1(a):
    jnlhv__rgd = count_nonnan(a)
    if jnlhv__rgd <= 1:
        return np.nan
    return np.nanvar(a) * (jnlhv__rgd / (jnlhv__rgd - 1))


@numba.njit
def nanstd_ddof1(a):
    return np.sqrt(nanvar_ddof1(a))


def has_supported_h5py():
    try:
        import h5py
        from bodo.io import _hdf5
    except ImportError as tqtgb__ptcq:
        xhab__oiwcj = False
    else:
        xhab__oiwcj = h5py.version.hdf5_version_tuple[1] in (10, 12)
    return xhab__oiwcj


def check_h5py():
    if not has_supported_h5py():
        raise BodoError("install 'h5py' package to enable hdf5 support")


def has_pyarrow():
    try:
        import pyarrow
    except ImportError as tqtgb__ptcq:
        lqh__zjqui = False
    else:
        lqh__zjqui = True
    return lqh__zjqui


def has_scipy():
    try:
        import scipy
    except ImportError as tqtgb__ptcq:
        bwq__tgxb = False
    else:
        bwq__tgxb = True
    return bwq__tgxb


@intrinsic
def check_and_propagate_cpp_exception(typingctx):

    def codegen(context, builder, sig, args):
        uehm__jcqru = context.get_python_api(builder)
        gxqns__qqwpj = uehm__jcqru.err_occurred()
        kact__anlfc = cgutils.is_not_null(builder, gxqns__qqwpj)
        with builder.if_then(kact__anlfc):
            builder.ret(numba.core.callconv.RETCODE_EXC)
    return types.void(), codegen


def inlined_check_and_propagate_cpp_exception(context, builder):
    uehm__jcqru = context.get_python_api(builder)
    gxqns__qqwpj = uehm__jcqru.err_occurred()
    kact__anlfc = cgutils.is_not_null(builder, gxqns__qqwpj)
    with builder.if_then(kact__anlfc):
        builder.ret(numba.core.callconv.RETCODE_EXC)


@numba.njit
def check_java_installation(fname):
    with numba.objmode():
        check_java_installation_(fname)


def check_java_installation_(fname):
    if not fname.startswith('hdfs://'):
        return
    import shutil
    if not shutil.which('java'):
        ewiew__iodwn = (
            "Java not found. Make sure openjdk is installed for hdfs. openjdk can be installed by calling 'conda install 'openjdk>=9.0,<12' -c conda-forge'."
            )
        raise BodoError(ewiew__iodwn)


dt_err = """
        If you are trying to set NULL values for timedelta64 in regular Python, 

        consider using np.timedelta64('nat') instead of None
        """


@lower_constant(types.List)
def lower_constant_list(context, builder, typ, pyval):
    if len(pyval) > CONST_LIST_SLOW_WARN_THRESHOLD:
        warnings.warn(BodoWarning(
            'Using large global lists can result in long compilation times. Please pass large lists as arguments to JIT functions or use arrays.'
            ))
    qzeo__yskug = []
    for a in pyval:
        if bodo.typeof(a) != typ.dtype:
            raise BodoError(
                f'Values in list must have the same data type for type stability. Expected: {typ.dtype}, Actual: {bodo.typeof(a)}'
                )
        qzeo__yskug.append(context.get_constant_generic(builder, typ.dtype, a))
    wcj__aoy = context.get_constant_generic(builder, types.int64, len(pyval))
    nzpkv__tmbp = context.get_constant_generic(builder, types.bool_, False)
    gpupe__kup = context.get_constant_null(types.pyobject)
    sxwf__qjhgr = lir.Constant.literal_struct([wcj__aoy, wcj__aoy,
        nzpkv__tmbp] + qzeo__yskug)
    sxwf__qjhgr = cgutils.global_constant(builder, '.const.payload',
        sxwf__qjhgr).bitcast(cgutils.voidptr_t)
    uzuzn__nkpq = context.get_constant(types.int64, -1)
    nlr__whkga = context.get_constant_null(types.voidptr)
    jfai__aoiq = lir.Constant.literal_struct([uzuzn__nkpq, nlr__whkga,
        nlr__whkga, sxwf__qjhgr, uzuzn__nkpq])
    jfai__aoiq = cgutils.global_constant(builder, '.const.meminfo', jfai__aoiq
        ).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([jfai__aoiq, gpupe__kup])


@lower_constant(types.Set)
def lower_constant_set(context, builder, typ, pyval):
    for a in pyval:
        if bodo.typeof(a) != typ.dtype:
            raise BodoError(
                f'Values in set must have the same data type for type stability. Expected: {typ.dtype}, Actual: {bodo.typeof(a)}'
                )
    qxr__brv = types.List(typ.dtype)
    bhdy__tnszh = context.get_constant_generic(builder, qxr__brv, list(pyval))
    mvoo__khgai = context.compile_internal(builder, lambda l: set(l), types
        .Set(typ.dtype)(qxr__brv), [bhdy__tnszh])
    return mvoo__khgai


def lower_const_dict_fast_path(context, builder, typ, pyval):
    from bodo.utils.typing import can_replace
    jqaa__qte = pd.Series(pyval.keys()).values
    tsg__aiu = pd.Series(pyval.values()).values
    cwzh__pgt = bodo.typeof(jqaa__qte)
    atirr__exvmw = bodo.typeof(tsg__aiu)
    require(cwzh__pgt.dtype == typ.key_type or can_replace(typ.key_type,
        cwzh__pgt.dtype))
    require(atirr__exvmw.dtype == typ.value_type or can_replace(typ.
        value_type, atirr__exvmw.dtype))
    pgjx__awakm = context.get_constant_generic(builder, cwzh__pgt, jqaa__qte)
    febli__fxjmc = context.get_constant_generic(builder, atirr__exvmw, tsg__aiu
        )

    def create_dict(keys, vals):
        lsgv__oge = {}
        for k, v in zip(keys, vals):
            lsgv__oge[k] = v
        return lsgv__oge
    zqg__hzp = context.compile_internal(builder, create_dict, typ(cwzh__pgt,
        atirr__exvmw), [pgjx__awakm, febli__fxjmc])
    return zqg__hzp


@lower_constant(types.DictType)
def lower_constant_dict(context, builder, typ, pyval):
    try:
        return lower_const_dict_fast_path(context, builder, typ, pyval)
    except:
        pass
    if len(pyval) > CONST_DICT_SLOW_WARN_THRESHOLD:
        warnings.warn(BodoWarning(
            'Using large global dictionaries can result in long compilation times. Please pass large dictionaries as arguments to JIT functions.'
            ))
    oxu__ljps = typ.key_type
    qglmz__ysmkd = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(oxu__ljps, qglmz__ysmkd)
    zqg__hzp = context.compile_internal(builder, make_dict, typ(), [])

    def set_dict_val(d, k, v):
        d[k] = v
    for k, v in pyval.items():
        urbw__zghh = context.get_constant_generic(builder, oxu__ljps, k)
        kfz__mkfg = context.get_constant_generic(builder, qglmz__ysmkd, v)
        context.compile_internal(builder, set_dict_val, types.none(typ,
            oxu__ljps, qglmz__ysmkd), [zqg__hzp, urbw__zghh, kfz__mkfg])
    return zqg__hzp


def synchronize_error(exception_str, error_message):
    if exception_str == 'ValueError':
        jwilg__scv = ValueError
    else:
        jwilg__scv = RuntimeError
    fqv__dmy = MPI.COMM_WORLD
    if fqv__dmy.allreduce(error_message != '', op=MPI.LOR):
        for error_message in fqv__dmy.allgather(error_message):
            if error_message:
                raise jwilg__scv(error_message)


@numba.njit
def synchronize_error_njit(exception_str, error_message):
    with numba.objmode():
        synchronize_error(exception_str, error_message)
