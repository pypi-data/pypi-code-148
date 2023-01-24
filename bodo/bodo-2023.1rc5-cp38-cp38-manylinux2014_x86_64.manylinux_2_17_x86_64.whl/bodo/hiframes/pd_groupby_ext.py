"""Support for Pandas Groupby operations
"""
import operator
from enum import Enum
import numba
import numpy as np
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import AbstractTemplate, bound_function, infer_global, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import NumericIndexType, RangeIndexType
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_table, delete_table_decref_arrays, get_groupby_labels, get_null_shuffle_info, get_shuffle_info, info_from_table, info_to_array, reverse_shuffle_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.decimal_arr_ext import Decimal128Type
from bodo.libs.float_arr_ext import FloatDtype, FloatingArrayType
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import get_call_expr_arg, get_const_func_output_type
from bodo.utils.typing import BodoError, ColNamesMetaType, check_unsupported_args, create_unsupported_overload, dtype_to_array_type, get_index_data_arr_types, get_index_name_types, get_literal_value, get_overload_const_bool, get_overload_const_func, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_constant_dict, get_udf_error_msg, get_udf_out_arr_type, is_dtype_nullable, is_literal_type, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, list_cumulative, raise_bodo_error, to_nullable_type, to_numeric_index_if_range_index, to_str_arr_if_dict_array
from bodo.utils.utils import dt_err, is_expr


class DataFrameGroupByType(types.Type):

    def __init__(self, df_type, keys, selection, as_index, dropna=True,
        explicit_select=False, series_select=False, _num_shuffle_keys=-1):
        self.df_type = df_type
        self.keys = keys
        self.selection = selection
        self.as_index = as_index
        self.dropna = dropna
        self.explicit_select = explicit_select
        self.series_select = series_select
        self._num_shuffle_keys = _num_shuffle_keys
        super(DataFrameGroupByType, self).__init__(name=
            f'DataFrameGroupBy({df_type}, {keys}, {selection}, {as_index}, {dropna}, {explicit_select}, {series_select}, {_num_shuffle_keys})'
            )

    def copy(self):
        return DataFrameGroupByType(self.df_type, self.keys, self.selection,
            self.as_index, self.dropna, self.explicit_select, self.
            series_select, self._num_shuffle_keys)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(DataFrameGroupByType)
class GroupbyModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        zbr__nqydf = [('obj', fe_type.df_type)]
        super(GroupbyModel, self).__init__(dmm, fe_type, zbr__nqydf)


make_attribute_wrapper(DataFrameGroupByType, 'obj', 'obj')


def validate_udf(func_name, func):
    if not isinstance(func, (types.functions.MakeFunctionLiteral, bodo.
        utils.typing.FunctionLiteral, types.Dispatcher, CPUDispatcher)):
        raise_bodo_error(
            f"Groupby.{func_name}: 'func' must be user defined function")


@intrinsic
def init_groupby(typingctx, obj_type, by_type, as_index_type, dropna_type,
    _num_shuffle_keys):

    def codegen(context, builder, signature, args):
        yio__viu = args[0]
        pfmr__eozb = signature.return_type
        skml__itwk = cgutils.create_struct_proxy(pfmr__eozb)(context, builder)
        skml__itwk.obj = yio__viu
        context.nrt.incref(builder, signature.args[0], yio__viu)
        return skml__itwk._getvalue()
    if is_overload_constant_list(by_type):
        keys = tuple(get_overload_const_list(by_type))
    elif is_literal_type(by_type):
        keys = get_literal_value(by_type),
    else:
        assert False, 'Reached unreachable code in init_groupby; there is an validate_groupby_spec'
    selection = list(obj_type.columns)
    for vaiz__kqtzb in keys:
        selection.remove(vaiz__kqtzb)
    if is_overload_constant_bool(as_index_type):
        as_index = is_overload_true(as_index_type)
    else:
        as_index = True
    if is_overload_constant_bool(dropna_type):
        dropna = is_overload_true(dropna_type)
    else:
        dropna = True
    if is_overload_constant_int(_num_shuffle_keys):
        poy__sgfwx = get_overload_const_int(_num_shuffle_keys)
    else:
        poy__sgfwx = -1
    pfmr__eozb = DataFrameGroupByType(obj_type, keys, tuple(selection),
        as_index, dropna, False, _num_shuffle_keys=poy__sgfwx)
    return pfmr__eozb(obj_type, by_type, as_index_type, dropna_type,
        _num_shuffle_keys), codegen


@lower_builtin('groupby.count', types.VarArg(types.Any))
@lower_builtin('groupby.size', types.VarArg(types.Any))
@lower_builtin('groupby.apply', types.VarArg(types.Any))
@lower_builtin('groupby.agg', types.VarArg(types.Any))
def lower_groupby_count_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


@infer
class StaticGetItemDataFrameGroupBy(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        grpby, muwbo__omeu = args
        if isinstance(grpby, DataFrameGroupByType):
            series_select = False
            if isinstance(muwbo__omeu, (tuple, list)):
                if len(set(muwbo__omeu).difference(set(grpby.df_type.columns))
                    ) > 0:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(set(muwbo__omeu).difference(set(grpby.
                        df_type.columns))))
                selection = muwbo__omeu
            else:
                if muwbo__omeu not in grpby.df_type.columns:
                    raise_bodo_error(
                        'groupby: selected column {} not found in dataframe'
                        .format(muwbo__omeu))
                selection = muwbo__omeu,
                series_select = True
            xjzc__ujhu = DataFrameGroupByType(grpby.df_type, grpby.keys,
                selection, grpby.as_index, grpby.dropna, True,
                series_select, _num_shuffle_keys=grpby._num_shuffle_keys)
            return signature(xjzc__ujhu, *args)


@infer_global(operator.getitem)
class GetItemDataFrameGroupBy(AbstractTemplate):

    def generic(self, args, kws):
        grpby, muwbo__omeu = args
        if isinstance(grpby, DataFrameGroupByType) and is_literal_type(
            muwbo__omeu):
            xjzc__ujhu = StaticGetItemDataFrameGroupBy.generic(self, (grpby,
                get_literal_value(muwbo__omeu)), {}).return_type
            return signature(xjzc__ujhu, *args)


GetItemDataFrameGroupBy.prefer_literal = True


@lower_builtin('static_getitem', DataFrameGroupByType, types.Any)
@lower_builtin(operator.getitem, DataFrameGroupByType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


def get_groupby_output_dtype(arr_type, func_name, index_type=None):
    jedz__rpp = arr_type == ArrayItemArrayType(string_array_type)
    dqw__ywq = arr_type.dtype
    if isinstance(dqw__ywq, bodo.hiframes.datetime_timedelta_ext.
        DatetimeTimeDeltaType):
        raise BodoError(
            f"""column type of {dqw__ywq} is not supported in groupby built-in function {func_name}.
{dt_err}"""
            )
    if func_name == 'median' and not isinstance(dqw__ywq, (Decimal128Type,
        types.Float, types.Integer)):
        return (None,
            'For median, only column of integer, float or Decimal type are allowed'
            )
    elif func_name in ('first', 'last', 'sum', 'prod', 'min', 'max',
        'count', 'nunique', 'head') and isinstance(arr_type, (
        TupleArrayType, ArrayItemArrayType)):
        return (None,
            f'column type of list/tuple of {dqw__ywq} is not supported in groupby built-in function {func_name}'
            )
    elif func_name in {'median', 'mean', 'var', 'std'} and isinstance(dqw__ywq,
        (Decimal128Type, types.Integer, types.Float)):
        return dtype_to_array_type(types.float64), 'ok'
    elif func_name == 'boolor_agg':
        if isinstance(dqw__ywq, (Decimal128Type, types.Integer, types.Float,
            types.Boolean)):
            return bodo.boolean_array, 'ok'
        return (None,
            f'For boolor_agg, only columns of type integer, float, Decimal, or boolean type are allowed'
            )
    if not isinstance(dqw__ywq, (types.Integer, types.Float, types.Boolean)):
        if jedz__rpp or dqw__ywq == types.unicode_type:
            if func_name not in {'count', 'nunique', 'min', 'max', 'sum',
                'first', 'last', 'head'}:
                return (None,
                    f'column type of strings or list of strings is not supported in groupby built-in function {func_name}'
                    )
        else:
            if isinstance(dqw__ywq, bodo.PDCategoricalDtype):
                if func_name in ('min', 'max') and not dqw__ywq.ordered:
                    return (None,
                        f'categorical column must be ordered in groupby built-in function {func_name}'
                        )
            if func_name not in {'count', 'nunique', 'min', 'max', 'first',
                'last', 'head'}:
                return (None,
                    f'column type of {dqw__ywq} is not supported in groupby built-in function {func_name}'
                    )
    if isinstance(dqw__ywq, types.Boolean) and func_name in {'cumsum',
        'mean', 'sum', 'std', 'var'}:
        if func_name in {'sum'}:
            return to_nullable_type(dtype_to_array_type(types.int64)), 'ok'
        return (None,
            f'groupby built-in functions {func_name} does not support boolean column'
            )
    elif func_name in {'idxmin', 'idxmax'}:
        return dtype_to_array_type(get_index_data_arr_types(index_type)[0].
            dtype), 'ok'
    elif func_name in {'count', 'nunique'}:
        return dtype_to_array_type(types.int64), 'ok'
    else:
        return arr_type, 'ok'


def get_pivot_output_dtype(arr_type, func_name, index_type=None):
    dqw__ywq = arr_type.dtype
    if func_name in {'count'}:
        return IntDtype(types.int64)
    if func_name in {'sum', 'prod', 'min', 'max'}:
        if func_name in {'sum', 'prod'} and not isinstance(dqw__ywq, (types
            .Integer, types.Float)):
            raise BodoError(
                'pivot_table(): sum and prod operations require integer or float input'
                )
        if isinstance(dqw__ywq, types.Integer):
            return IntDtype(dqw__ywq)
        return dqw__ywq
    if func_name in {'mean', 'var', 'std'}:
        return types.float64
    raise BodoError('invalid pivot operation')


def check_args_kwargs(func_name, len_args, args, kws):
    if len(kws) > 0:
        jfd__azexu = list(kws.keys())[0]
        raise BodoError(
            f"Groupby.{func_name}() got an unexpected keyword argument '{jfd__azexu}'."
            )
    elif len(args) > len_args:
        raise BodoError(
            f'Groupby.{func_name}() takes {len_args + 1} positional argument but {len(args)} were given.'
            )


class ColumnType(Enum):
    KeyColumn = 0
    NumericalColumn = 1
    NonNumericalColumn = 2


def get_keys_not_as_index(grp, out_columns, out_data, out_column_type,
    multi_level_names=False):
    for vaiz__kqtzb in grp.keys:
        if multi_level_names:
            utvaa__fpi = vaiz__kqtzb, ''
        else:
            utvaa__fpi = vaiz__kqtzb
        mzk__fxv = grp.df_type.column_index[vaiz__kqtzb]
        data = grp.df_type.data[mzk__fxv]
        out_columns.append(utvaa__fpi)
        out_data.append(data)
        out_column_type.append(ColumnType.KeyColumn.value)


def get_agg_typ(grp, args, func_name, typing_context, target_context, func=
    None, kws=None, raise_on_any_error=False):
    index = RangeIndexType(types.none)
    out_data = []
    out_columns = []
    out_column_type = []
    if func_name in ('head', 'ngroup'):
        grp.as_index = True
    if not grp.as_index:
        get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
    elif func_name in ('head', 'ngroup'):
        if grp.df_type.index == index:
            index = NumericIndexType(types.int64, types.none)
        else:
            index = grp.df_type.index
    elif len(grp.keys) > 1:
        bhh__rurjt = tuple(grp.df_type.column_index[grp.keys[fxem__vmuqf]] for
            fxem__vmuqf in range(len(grp.keys)))
        zvruf__cxkyy = tuple(grp.df_type.data[mzk__fxv] for mzk__fxv in
            bhh__rurjt)
        index = MultiIndexType(zvruf__cxkyy, tuple(types.StringLiteral(
            vaiz__kqtzb) for vaiz__kqtzb in grp.keys))
    else:
        mzk__fxv = grp.df_type.column_index[grp.keys[0]]
        katn__lta = grp.df_type.data[mzk__fxv]
        index = bodo.hiframes.pd_index_ext.array_type_to_index(katn__lta,
            types.StringLiteral(grp.keys[0]))
    zql__qjy = {}
    hbsgr__ofx = []
    if func_name in ('size', 'count'):
        kws = dict(kws) if kws else {}
        check_args_kwargs(func_name, 0, args, kws)
    if func_name == 'size':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('size')
        zql__qjy[None, 'size'] = 'size'
    elif func_name == 'ngroup':
        out_data.append(types.Array(types.int64, 1, 'C'))
        out_columns.append('ngroup')
        zql__qjy[None, 'ngroup'] = 'ngroup'
        kws = dict(kws) if kws else {}
        ascending = args[0] if len(args) > 0 else kws.pop('ascending', True)
        lqc__vlri = dict(ascending=ascending)
        qpbj__pzvjf = dict(ascending=True)
        check_unsupported_args(f'Groupby.{func_name}', lqc__vlri,
            qpbj__pzvjf, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(func_name, 1, args, kws)
    else:
        columns = (grp.selection if func_name != 'head' or grp.
            explicit_select else grp.df_type.columns)
        for nnfe__ajwv in columns:
            mzk__fxv = grp.df_type.column_index[nnfe__ajwv]
            data = grp.df_type.data[mzk__fxv]
            if func_name in ('sum', 'cumsum'):
                data = to_str_arr_if_dict_array(data)
            eugz__fod = ColumnType.NonNumericalColumn.value
            if isinstance(data, (types.Array, IntegerArrayType,
                FloatingArrayType)) and isinstance(data.dtype, (types.
                Integer, types.Float)):
                eugz__fod = ColumnType.NumericalColumn.value
            if func_name == 'agg':
                try:
                    sqi__qrts = SeriesType(data.dtype, data, None, string_type)
                    csw__cyzlt = get_const_func_output_type(func, (
                        sqi__qrts,), {}, typing_context, target_context)
                    if csw__cyzlt != ArrayItemArrayType(string_array_type):
                        csw__cyzlt = dtype_to_array_type(csw__cyzlt)
                    err_msg = 'ok'
                except:
                    raise_bodo_error(
                        'Groupy.agg()/Groupy.aggregate(): column {col} of type {type} is unsupported/not a valid input type for user defined function'
                        .format(col=nnfe__ajwv, type=data.dtype))
            else:
                if func_name in ('first', 'last', 'min', 'max'):
                    kws = dict(kws) if kws else {}
                    jaj__ahf = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', False)
                    mwvnz__zli = args[1] if len(args) > 1 else kws.pop(
                        'min_count', -1)
                    lqc__vlri = dict(numeric_only=jaj__ahf, min_count=
                        mwvnz__zli)
                    qpbj__pzvjf = dict(numeric_only=False, min_count=-1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        lqc__vlri, qpbj__pzvjf, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('sum', 'prod'):
                    kws = dict(kws) if kws else {}
                    jaj__ahf = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    mwvnz__zli = args[1] if len(args) > 1 else kws.pop(
                        'min_count', 0)
                    lqc__vlri = dict(numeric_only=jaj__ahf, min_count=
                        mwvnz__zli)
                    qpbj__pzvjf = dict(numeric_only=True, min_count=0)
                    check_unsupported_args(f'Groupby.{func_name}',
                        lqc__vlri, qpbj__pzvjf, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('mean', 'median'):
                    kws = dict(kws) if kws else {}
                    jaj__ahf = args[0] if len(args) > 0 else kws.pop(
                        'numeric_only', True)
                    lqc__vlri = dict(numeric_only=jaj__ahf)
                    qpbj__pzvjf = dict(numeric_only=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        lqc__vlri, qpbj__pzvjf, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('idxmin', 'idxmax'):
                    kws = dict(kws) if kws else {}
                    eehaq__rzqc = args[0] if len(args) > 0 else kws.pop('axis',
                        0)
                    qiebh__nqks = args[1] if len(args) > 1 else kws.pop(
                        'skipna', True)
                    lqc__vlri = dict(axis=eehaq__rzqc, skipna=qiebh__nqks)
                    qpbj__pzvjf = dict(axis=0, skipna=True)
                    check_unsupported_args(f'Groupby.{func_name}',
                        lqc__vlri, qpbj__pzvjf, package_name='pandas',
                        module_name='GroupBy')
                elif func_name in ('var', 'std'):
                    kws = dict(kws) if kws else {}
                    yir__iiq = args[0] if len(args) > 0 else kws.pop('ddof', 1)
                    lqc__vlri = dict(ddof=yir__iiq)
                    qpbj__pzvjf = dict(ddof=1)
                    check_unsupported_args(f'Groupby.{func_name}',
                        lqc__vlri, qpbj__pzvjf, package_name='pandas',
                        module_name='GroupBy')
                elif func_name == 'nunique':
                    kws = dict(kws) if kws else {}
                    dropna = args[0] if len(args) > 0 else kws.pop('dropna', 1)
                    check_args_kwargs(func_name, 1, args, kws)
                elif func_name == 'head':
                    if len(args) == 0:
                        kws.pop('n', None)
                csw__cyzlt, err_msg = get_groupby_output_dtype(data,
                    func_name, grp.df_type.index)
            if err_msg == 'ok':
                csw__cyzlt = to_str_arr_if_dict_array(csw__cyzlt
                    ) if func_name in ('sum', 'cumsum') else csw__cyzlt
                out_data.append(csw__cyzlt)
                out_columns.append(nnfe__ajwv)
                if func_name == 'agg':
                    flu__zgl = bodo.ir.aggregate._get_udf_name(bodo.ir.
                        aggregate._get_const_agg_func(func, None))
                    zql__qjy[nnfe__ajwv, flu__zgl] = nnfe__ajwv
                else:
                    zql__qjy[nnfe__ajwv, func_name] = nnfe__ajwv
                out_column_type.append(eugz__fod)
            elif raise_on_any_error:
                raise BodoError(
                    f'Groupby with function {func_name} not supported. Error message: {err_msg}'
                    )
            else:
                hbsgr__ofx.append(err_msg)
    if func_name == 'sum':
        eepi__eztr = any([(drix__mikbg == ColumnType.NumericalColumn.value) for
            drix__mikbg in out_column_type])
        if eepi__eztr:
            out_data = [drix__mikbg for drix__mikbg, irry__wmjjm in zip(
                out_data, out_column_type) if irry__wmjjm != ColumnType.
                NonNumericalColumn.value]
            out_columns = [drix__mikbg for drix__mikbg, irry__wmjjm in zip(
                out_columns, out_column_type) if irry__wmjjm != ColumnType.
                NonNumericalColumn.value]
            zql__qjy = {}
            for nnfe__ajwv in out_columns:
                if grp.as_index is False and nnfe__ajwv in grp.keys:
                    continue
                zql__qjy[nnfe__ajwv, func_name] = nnfe__ajwv
    bkwol__lzem = len(hbsgr__ofx)
    if len(out_data) == 0:
        if bkwol__lzem == 0:
            raise BodoError('No columns in output.')
        else:
            raise BodoError(
                'No columns in output. {} column{} dropped for following reasons: {}'
                .format(bkwol__lzem, ' was' if bkwol__lzem == 1 else
                's were', ','.join(hbsgr__ofx)))
    wbee__spfh = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if (len(grp.selection) == 1 and grp.series_select and grp.as_index or 
        func_name == 'size' and grp.as_index or func_name == 'ngroup'):
        if isinstance(out_data[0], IntegerArrayType):
            bdorl__xig = IntDtype(out_data[0].dtype)
        elif isinstance(out_data[0], FloatingArrayType):
            bdorl__xig = FloatDtype(out_data[0].dtype)
        else:
            bdorl__xig = out_data[0].dtype
        ywd__rvsf = types.none if func_name in ('size', 'ngroup'
            ) else types.StringLiteral(grp.selection[0])
        wbee__spfh = SeriesType(bdorl__xig, data=out_data[0], index=index,
            name_typ=ywd__rvsf)
    return signature(wbee__spfh, *args), zql__qjy


def get_agg_funcname_and_outtyp(grp, col, f_val, typing_context,
    target_context, raise_on_any_error):
    sur__nmwwy = True
    if isinstance(f_val, str):
        sur__nmwwy = False
        pinh__uln = f_val
    elif is_overload_constant_str(f_val):
        sur__nmwwy = False
        pinh__uln = get_overload_const_str(f_val)
    elif bodo.utils.typing.is_builtin_function(f_val):
        sur__nmwwy = False
        pinh__uln = bodo.utils.typing.get_builtin_function_name(f_val)
    if not sur__nmwwy:
        if pinh__uln not in bodo.ir.aggregate.supported_agg_funcs[:-1]:
            raise BodoError(f'unsupported aggregate function {pinh__uln}')
        xjzc__ujhu = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(xjzc__ujhu, (), pinh__uln, typing_context,
            target_context, raise_on_any_error=raise_on_any_error)[0
            ].return_type
    else:
        if is_expr(f_val, 'make_function'):
            ijzzk__enx = types.functions.MakeFunctionLiteral(f_val)
        else:
            ijzzk__enx = f_val
        validate_udf('agg', ijzzk__enx)
        func = get_overload_const_func(ijzzk__enx, None)
        qoui__qmhyz = func.code if hasattr(func, 'code') else func.__code__
        pinh__uln = qoui__qmhyz.co_name
        xjzc__ujhu = DataFrameGroupByType(grp.df_type, grp.keys, (col,),
            grp.as_index, grp.dropna, True, True, _num_shuffle_keys=grp.
            _num_shuffle_keys)
        out_tp = get_agg_typ(xjzc__ujhu, (), 'agg', typing_context,
            target_context, ijzzk__enx, raise_on_any_error=raise_on_any_error)[
            0].return_type
    return pinh__uln, out_tp


def resolve_agg(grp, args, kws, typing_context, target_context):
    func = get_call_expr_arg('agg', args, dict(kws), 0, 'func', default=
        types.none)
    fsk__cep = kws and all(isinstance(arym__tyivt, types.Tuple) and len(
        arym__tyivt) == 2 for arym__tyivt in kws.values())
    raise_on_any_error = fsk__cep
    if is_overload_none(func) and not fsk__cep:
        raise_bodo_error("Groupby.agg()/aggregate(): Must provide 'func'")
    if len(args) > 1 or kws and not fsk__cep:
        raise_bodo_error(
            'Groupby.agg()/aggregate(): passing extra arguments to functions not supported yet.'
            )
    ymw__mttko = False

    def _append_out_type(grp, out_data, out_tp):
        if grp.as_index is False:
            out_data.append(out_tp.data[len(grp.keys)])
        else:
            out_data.append(out_tp.data)
    if fsk__cep or is_overload_constant_dict(func):
        if fsk__cep:
            aih__tozg = [get_literal_value(aoke__ohlua) for aoke__ohlua,
                fjeh__tume in kws.values()]
            dipxy__badyk = [get_literal_value(fel__zndu) for fjeh__tume,
                fel__zndu in kws.values()]
        else:
            txrh__znosi = get_overload_constant_dict(func)
            aih__tozg = tuple(txrh__znosi.keys())
            dipxy__badyk = tuple(txrh__znosi.values())
        for nlcl__mxn in ('head', 'ngroup'):
            if nlcl__mxn in dipxy__badyk:
                raise BodoError(
                    f'Groupby.agg()/aggregate(): {nlcl__mxn} cannot be mixed with other groupby operations.'
                    )
        if any(nnfe__ajwv not in grp.selection and nnfe__ajwv not in grp.
            keys for nnfe__ajwv in aih__tozg):
            raise_bodo_error(
                f'Selected column names {aih__tozg} not all available in dataframe column names {grp.selection}'
                )
        multi_level_names = any(isinstance(f_val, (tuple, list)) for f_val in
            dipxy__badyk)
        if fsk__cep and multi_level_names:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): cannot pass multiple functions in a single pd.NamedAgg()'
                )
        zql__qjy = {}
        out_columns = []
        out_data = []
        out_column_type = []
        zmo__zyduv = []
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data,
                out_column_type, multi_level_names=multi_level_names)
        for jkrcz__whmr, f_val in zip(aih__tozg, dipxy__badyk):
            if isinstance(f_val, (tuple, list)):
                zyra__uvgb = 0
                for ijzzk__enx in f_val:
                    pinh__uln, out_tp = get_agg_funcname_and_outtyp(grp,
                        jkrcz__whmr, ijzzk__enx, typing_context,
                        target_context, raise_on_any_error)
                    ymw__mttko = pinh__uln in list_cumulative
                    if pinh__uln == '<lambda>' and len(f_val) > 1:
                        pinh__uln = '<lambda_' + str(zyra__uvgb) + '>'
                        zyra__uvgb += 1
                    out_columns.append((jkrcz__whmr, pinh__uln))
                    zql__qjy[jkrcz__whmr, pinh__uln] = jkrcz__whmr, pinh__uln
                    _append_out_type(grp, out_data, out_tp)
            else:
                pinh__uln, out_tp = get_agg_funcname_and_outtyp(grp,
                    jkrcz__whmr, f_val, typing_context, target_context,
                    raise_on_any_error)
                ymw__mttko = pinh__uln in list_cumulative
                if multi_level_names:
                    out_columns.append((jkrcz__whmr, pinh__uln))
                    zql__qjy[jkrcz__whmr, pinh__uln] = jkrcz__whmr, pinh__uln
                elif not fsk__cep:
                    out_columns.append(jkrcz__whmr)
                    zql__qjy[jkrcz__whmr, pinh__uln] = jkrcz__whmr
                elif fsk__cep:
                    zmo__zyduv.append(pinh__uln)
                _append_out_type(grp, out_data, out_tp)
        if fsk__cep:
            for fxem__vmuqf, mcx__pgudu in enumerate(kws.keys()):
                out_columns.append(mcx__pgudu)
                zql__qjy[aih__tozg[fxem__vmuqf], zmo__zyduv[fxem__vmuqf]
                    ] = mcx__pgudu
        if ymw__mttko:
            index = grp.df_type.index
        else:
            index = out_tp.index
        wbee__spfh = DataFrameType(tuple(out_data), index, tuple(
            out_columns), is_table_format=True)
        return signature(wbee__spfh, *args), zql__qjy
    if isinstance(func, types.BaseTuple) and not isinstance(func, types.
        LiteralStrKeyDict) or is_overload_constant_list(func):
        if not (len(grp.selection) == 1 and grp.explicit_select):
            raise_bodo_error(
                'Groupby.agg()/aggregate(): must select exactly one column when more than one function is supplied'
                )
        if is_overload_constant_list(func):
            zkr__shoqh = get_overload_const_list(func)
        else:
            zkr__shoqh = func.types
        if len(zkr__shoqh) == 0:
            raise_bodo_error(
                'Groupby.agg()/aggregate(): List of functions must contain at least 1 function'
                )
        out_data = []
        out_columns = []
        out_column_type = []
        zyra__uvgb = 0
        if not grp.as_index:
            get_keys_not_as_index(grp, out_columns, out_data, out_column_type)
        zql__qjy = {}
        qymf__woycr = grp.selection[0]
        for f_val in zkr__shoqh:
            pinh__uln, out_tp = get_agg_funcname_and_outtyp(grp,
                qymf__woycr, f_val, typing_context, target_context,
                raise_on_any_error)
            ymw__mttko = pinh__uln in list_cumulative
            if pinh__uln == '<lambda>' and len(zkr__shoqh) > 1:
                pinh__uln = '<lambda_' + str(zyra__uvgb) + '>'
                zyra__uvgb += 1
            out_columns.append(pinh__uln)
            zql__qjy[qymf__woycr, pinh__uln] = pinh__uln
            _append_out_type(grp, out_data, out_tp)
        if ymw__mttko:
            index = grp.df_type.index
        else:
            index = out_tp.index
        wbee__spfh = DataFrameType(tuple(out_data), index, tuple(
            out_columns), is_table_format=True)
        return signature(wbee__spfh, *args), zql__qjy
    pinh__uln = ''
    if types.unliteral(func) == types.unicode_type:
        pinh__uln = get_overload_const_str(func)
    if bodo.utils.typing.is_builtin_function(func):
        pinh__uln = bodo.utils.typing.get_builtin_function_name(func)
    if pinh__uln:
        args = args[1:]
        kws.pop('func', None)
        return get_agg_typ(grp, args, pinh__uln, typing_context, kws)
    validate_udf('agg', func)
    return get_agg_typ(grp, args, 'agg', typing_context, target_context, func)


def resolve_transformative(grp, args, kws, msg, name_operation):
    index = to_numeric_index_if_range_index(grp.df_type.index)
    if isinstance(index, MultiIndexType):
        raise_bodo_error(
            f'Groupby.{name_operation}: MultiIndex input not supported for groupby operations that use input Index'
            )
    out_columns = []
    out_data = []
    if name_operation in list_cumulative:
        kws = dict(kws) if kws else {}
        eehaq__rzqc = args[0] if len(args) > 0 else kws.pop('axis', 0)
        jaj__ahf = args[1] if len(args) > 1 else kws.pop('numeric_only', False)
        qiebh__nqks = args[2] if len(args) > 2 else kws.pop('skipna', 1)
        lqc__vlri = dict(axis=eehaq__rzqc, numeric_only=jaj__ahf)
        qpbj__pzvjf = dict(axis=0, numeric_only=False)
        check_unsupported_args(f'Groupby.{name_operation}', lqc__vlri,
            qpbj__pzvjf, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 3, args, kws)
    elif name_operation == 'shift':
        dys__undni = args[0] if len(args) > 0 else kws.pop('periods', 1)
        qbug__shx = args[1] if len(args) > 1 else kws.pop('freq', None)
        eehaq__rzqc = args[2] if len(args) > 2 else kws.pop('axis', 0)
        sspjc__nxv = args[3] if len(args) > 3 else kws.pop('fill_value', None)
        lqc__vlri = dict(freq=qbug__shx, axis=eehaq__rzqc, fill_value=
            sspjc__nxv)
        qpbj__pzvjf = dict(freq=None, axis=0, fill_value=None)
        check_unsupported_args(f'Groupby.{name_operation}', lqc__vlri,
            qpbj__pzvjf, package_name='pandas', module_name='GroupBy')
        check_args_kwargs(name_operation, 4, args, kws)
    elif name_operation == 'transform':
        kws = dict(kws)
        uxf__ylb = args[0] if len(args) > 0 else kws.pop('func', None)
        hneto__ymzqs = kws.pop('engine', None)
        yuc__jlpjk = kws.pop('engine_kwargs', None)
        lqc__vlri = dict(engine=hneto__ymzqs, engine_kwargs=yuc__jlpjk)
        qpbj__pzvjf = dict(engine=None, engine_kwargs=None)
        check_unsupported_args(f'Groupby.transform', lqc__vlri, qpbj__pzvjf,
            package_name='pandas', module_name='GroupBy')
    zql__qjy = {}
    for nnfe__ajwv in grp.selection:
        out_columns.append(nnfe__ajwv)
        zql__qjy[nnfe__ajwv, name_operation] = nnfe__ajwv
        mzk__fxv = grp.df_type.column_index[nnfe__ajwv]
        data = grp.df_type.data[mzk__fxv]
        qhwt__fnu = (name_operation if name_operation != 'transform' else
            get_literal_value(uxf__ylb))
        if qhwt__fnu in ('sum', 'cumsum'):
            data = to_str_arr_if_dict_array(data)
        if name_operation == 'cumprod':
            if not isinstance(data.dtype, (types.Integer, types.Float)):
                raise BodoError(msg)
        if name_operation == 'cumsum':
            if data.dtype != types.unicode_type and data != ArrayItemArrayType(
                string_array_type) and not isinstance(data.dtype, (types.
                Integer, types.Float)):
                raise BodoError(msg)
        if name_operation in ('cummin', 'cummax'):
            if not isinstance(data.dtype, types.Integer
                ) and not is_dtype_nullable(data.dtype):
                raise BodoError(msg)
        if name_operation == 'shift':
            if isinstance(data, (TupleArrayType, ArrayItemArrayType)):
                raise BodoError(msg)
            if isinstance(data.dtype, bodo.hiframes.datetime_timedelta_ext.
                DatetimeTimeDeltaType):
                raise BodoError(
                    f"""column type of {data.dtype} is not supported in groupby built-in function shift.
{dt_err}"""
                    )
        if name_operation == 'transform':
            csw__cyzlt, err_msg = get_groupby_output_dtype(data,
                get_literal_value(uxf__ylb), grp.df_type.index)
            if err_msg == 'ok':
                data = csw__cyzlt
            else:
                raise BodoError(
                    f'column type of {data.dtype} is not supported by {args[0]} yet.\n'
                    )
        out_data.append(data)
    if len(out_data) == 0:
        raise BodoError('No columns in output.')
    wbee__spfh = DataFrameType(tuple(out_data), index, tuple(out_columns),
        is_table_format=True)
    if len(grp.selection) == 1 and grp.series_select and grp.as_index:
        wbee__spfh = SeriesType(out_data[0].dtype, data=out_data[0], index=
            index, name_typ=types.StringLiteral(grp.selection[0]))
    return signature(wbee__spfh, *args), zql__qjy


def resolve_gb(grp, args, kws, func_name, typing_context, target_context,
    err_msg=''):
    if func_name in set(list_cumulative) | {'shift', 'transform'}:
        return resolve_transformative(grp, args, kws, err_msg, func_name)
    elif func_name in {'agg', 'aggregate'}:
        return resolve_agg(grp, args, kws, typing_context, target_context)
    else:
        return get_agg_typ(grp, args, func_name, typing_context,
            target_context, kws=kws)


@infer_getattr
class DataframeGroupByAttribute(OverloadedKeyAttributeTemplate):
    key = DataFrameGroupByType
    _attr_set = None

    @bound_function('groupby.agg', no_unliteral=True)
    def resolve_agg(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.aggregate', no_unliteral=True)
    def resolve_aggregate(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'agg', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.sum', no_unliteral=True)
    def resolve_sum(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'sum', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.count', no_unliteral=True)
    def resolve_count(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'count', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.nunique', no_unliteral=True)
    def resolve_nunique(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'nunique', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.median', no_unliteral=True)
    def resolve_median(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'median', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.mean', no_unliteral=True)
    def resolve_mean(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'mean', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.min', no_unliteral=True)
    def resolve_min(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'min', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.max', no_unliteral=True)
    def resolve_max(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'max', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.prod', no_unliteral=True)
    def resolve_prod(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'prod', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.var', no_unliteral=True)
    def resolve_var(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'var', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.std', no_unliteral=True)
    def resolve_std(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'std', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.first', no_unliteral=True)
    def resolve_first(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'first', self.context, numba.core
            .registry.cpu_target.target_context)[0]

    @bound_function('groupby.last', no_unliteral=True)
    def resolve_last(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'last', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmin', no_unliteral=True)
    def resolve_idxmin(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmin', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.idxmax', no_unliteral=True)
    def resolve_idxmax(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'idxmax', self.context, numba.
            core.registry.cpu_target.target_context)[0]

    @bound_function('groupby.size', no_unliteral=True)
    def resolve_size(self, grp, args, kws):
        return resolve_gb(grp, args, kws, 'size', self.context, numba.core.
            registry.cpu_target.target_context)[0]

    @bound_function('groupby.cumsum', no_unliteral=True)
    def resolve_cumsum(self, grp, args, kws):
        msg = (
            'Groupby.cumsum() only supports columns of types integer, float, string or liststring'
            )
        return resolve_gb(grp, args, kws, 'cumsum', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cumprod', no_unliteral=True)
    def resolve_cumprod(self, grp, args, kws):
        msg = (
            'Groupby.cumprod() only supports columns of types integer and float'
            )
        return resolve_gb(grp, args, kws, 'cumprod', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummin', no_unliteral=True)
    def resolve_cummin(self, grp, args, kws):
        msg = (
            'Groupby.cummin() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummin', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.cummax', no_unliteral=True)
    def resolve_cummax(self, grp, args, kws):
        msg = (
            'Groupby.cummax() only supports columns of types integer, float, string, liststring, date, datetime or timedelta'
            )
        return resolve_gb(grp, args, kws, 'cummax', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.shift', no_unliteral=True)
    def resolve_shift(self, grp, args, kws):
        msg = (
            'Column type of list/tuple is not supported in groupby built-in function shift'
            )
        return resolve_gb(grp, args, kws, 'shift', self.context, numba.core
            .registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.pipe', no_unliteral=True)
    def resolve_pipe(self, grp, args, kws):
        return resolve_obj_pipe(self, grp, args, kws, 'GroupBy')

    @bound_function('groupby.transform', no_unliteral=True)
    def resolve_transform(self, grp, args, kws):
        msg = (
            'Groupby.transform() only supports sum, count, min, max, mean, and std operations'
            )
        return resolve_gb(grp, args, kws, 'transform', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.head', no_unliteral=True)
    def resolve_head(self, grp, args, kws):
        msg = 'Unsupported Gropupby head operation.\n'
        return resolve_gb(grp, args, kws, 'head', self.context, numba.core.
            registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.ngroup', no_unliteral=True)
    def resolve_ngroup(self, grp, args, kws):
        msg = 'Unsupported Gropupby head operation.\n'
        return resolve_gb(grp, args, kws, 'ngroup', self.context, numba.
            core.registry.cpu_target.target_context, err_msg=msg)[0]

    @bound_function('groupby.apply', no_unliteral=True)
    def resolve_apply(self, grp, args, kws):
        kws = dict(kws)
        func = args[0] if len(args) > 0 else kws.pop('func', None)
        f_args = tuple(args[1:]) if len(args) > 0 else ()
        ukieg__jteec = _get_groupby_apply_udf_out_type(func, grp, f_args,
            kws, self.context, numba.core.registry.cpu_target.target_context)
        qmmqc__igis = isinstance(ukieg__jteec, (SeriesType,
            HeterogeneousSeriesType)
            ) and ukieg__jteec.const_info is not None or not isinstance(
            ukieg__jteec, (SeriesType, DataFrameType))
        if qmmqc__igis:
            out_data = []
            out_columns = []
            out_column_type = []
            if not grp.as_index:
                get_keys_not_as_index(grp, out_columns, out_data,
                    out_column_type)
                ink__xni = NumericIndexType(types.int64, types.none)
            elif len(grp.keys) > 1:
                bhh__rurjt = tuple(grp.df_type.column_index[grp.keys[
                    fxem__vmuqf]] for fxem__vmuqf in range(len(grp.keys)))
                zvruf__cxkyy = tuple(grp.df_type.data[mzk__fxv] for
                    mzk__fxv in bhh__rurjt)
                ink__xni = MultiIndexType(zvruf__cxkyy, tuple(types.literal
                    (vaiz__kqtzb) for vaiz__kqtzb in grp.keys))
            else:
                mzk__fxv = grp.df_type.column_index[grp.keys[0]]
                katn__lta = grp.df_type.data[mzk__fxv]
                ink__xni = bodo.hiframes.pd_index_ext.array_type_to_index(
                    katn__lta, types.literal(grp.keys[0]))
            out_data = tuple(out_data)
            out_columns = tuple(out_columns)
        else:
            has__drw = tuple(grp.df_type.data[grp.df_type.column_index[
                nnfe__ajwv]] for nnfe__ajwv in grp.keys)
            mct__biv = tuple(types.literal(arym__tyivt) for arym__tyivt in
                grp.keys) + get_index_name_types(ukieg__jteec.index)
            if not grp.as_index:
                has__drw = types.Array(types.int64, 1, 'C'),
                mct__biv = (types.none,) + get_index_name_types(ukieg__jteec
                    .index)
            ink__xni = MultiIndexType(has__drw + get_index_data_arr_types(
                ukieg__jteec.index), mct__biv)
        if qmmqc__igis:
            if isinstance(ukieg__jteec, HeterogeneousSeriesType):
                fjeh__tume, ruirk__tld = ukieg__jteec.const_info
                if isinstance(ukieg__jteec.data, bodo.libs.
                    nullable_tuple_ext.NullableTupleType):
                    gaj__vwuf = ukieg__jteec.data.tuple_typ.types
                elif isinstance(ukieg__jteec.data, types.Tuple):
                    gaj__vwuf = ukieg__jteec.data.types
                idd__gaw = tuple(to_nullable_type(dtype_to_array_type(
                    qiuyw__prert)) for qiuyw__prert in gaj__vwuf)
                bmlc__wvub = DataFrameType(out_data + idd__gaw, ink__xni, 
                    out_columns + ruirk__tld)
            elif isinstance(ukieg__jteec, SeriesType):
                yryrq__dhe, ruirk__tld = ukieg__jteec.const_info
                idd__gaw = tuple(to_nullable_type(dtype_to_array_type(
                    ukieg__jteec.dtype)) for fjeh__tume in range(yryrq__dhe))
                bmlc__wvub = DataFrameType(out_data + idd__gaw, ink__xni, 
                    out_columns + ruirk__tld)
            else:
                dfu__hhraz = get_udf_out_arr_type(ukieg__jteec)
                if not grp.as_index:
                    bmlc__wvub = DataFrameType(out_data + (dfu__hhraz,),
                        ink__xni, out_columns + ('',))
                else:
                    bmlc__wvub = SeriesType(dfu__hhraz.dtype, dfu__hhraz,
                        ink__xni, None)
        elif isinstance(ukieg__jteec, SeriesType):
            bmlc__wvub = SeriesType(ukieg__jteec.dtype, ukieg__jteec.data,
                ink__xni, ukieg__jteec.name_typ)
        else:
            bmlc__wvub = DataFrameType(ukieg__jteec.data, ink__xni,
                ukieg__jteec.columns)
        xomv__ykqh = gen_apply_pysig(len(f_args), kws.keys())
        zyjb__sjvak = (func, *f_args) + tuple(kws.values())
        return signature(bmlc__wvub, *zyjb__sjvak).replace(pysig=xomv__ykqh)

    def generic_resolve(self, grpby, attr):
        if self._is_existing_attr(attr):
            return
        if attr not in grpby.df_type.columns:
            raise_bodo_error(
                f'groupby: invalid attribute {attr} (column not found in dataframe or unsupported function)'
                )
        return DataFrameGroupByType(grpby.df_type, grpby.keys, (attr,),
            grpby.as_index, grpby.dropna, True, True, _num_shuffle_keys=
            grpby._num_shuffle_keys)


def _get_groupby_apply_udf_out_type(func, grp, f_args, kws, typing_context,
    target_context):
    efk__qtd = grp.df_type
    if grp.explicit_select:
        if len(grp.selection) == 1:
            jkrcz__whmr = grp.selection[0]
            dfu__hhraz = efk__qtd.data[efk__qtd.column_index[jkrcz__whmr]]
            zqner__ipa = SeriesType(dfu__hhraz.dtype, dfu__hhraz, efk__qtd.
                index, types.literal(jkrcz__whmr))
        else:
            vjkak__kpx = tuple(efk__qtd.data[efk__qtd.column_index[
                nnfe__ajwv]] for nnfe__ajwv in grp.selection)
            zqner__ipa = DataFrameType(vjkak__kpx, efk__qtd.index, tuple(
                grp.selection))
    else:
        zqner__ipa = efk__qtd
    tkstn__jrfbb = zqner__ipa,
    tkstn__jrfbb += tuple(f_args)
    try:
        ukieg__jteec = get_const_func_output_type(func, tkstn__jrfbb, kws,
            typing_context, target_context)
    except Exception as unt__ykd:
        raise_bodo_error(get_udf_error_msg('GroupBy.apply()', unt__ykd),
            getattr(unt__ykd, 'loc', None))
    return ukieg__jteec


def resolve_obj_pipe(self, grp, args, kws, obj_name):
    kws = dict(kws)
    func = args[0] if len(args) > 0 else kws.pop('func', None)
    f_args = tuple(args[1:]) if len(args) > 0 else ()
    tkstn__jrfbb = (grp,) + f_args
    try:
        ukieg__jteec = get_const_func_output_type(func, tkstn__jrfbb, kws,
            self.context, numba.core.registry.cpu_target.target_context, False)
    except Exception as unt__ykd:
        raise_bodo_error(get_udf_error_msg(f'{obj_name}.pipe()', unt__ykd),
            getattr(unt__ykd, 'loc', None))
    xomv__ykqh = gen_apply_pysig(len(f_args), kws.keys())
    zyjb__sjvak = (func, *f_args) + tuple(kws.values())
    return signature(ukieg__jteec, *zyjb__sjvak).replace(pysig=xomv__ykqh)


def gen_apply_pysig(n_args, kws):
    dhzc__svgzd = ', '.join(f'arg{fxem__vmuqf}' for fxem__vmuqf in range(
        n_args))
    dhzc__svgzd = dhzc__svgzd + ', ' if dhzc__svgzd else ''
    erjze__neecc = ', '.join(f"{abc__ugkqj} = ''" for abc__ugkqj in kws)
    sera__jrok = f'def apply_stub(func, {dhzc__svgzd}{erjze__neecc}):\n'
    sera__jrok += '    pass\n'
    mbly__osxp = {}
    exec(sera__jrok, {}, mbly__osxp)
    pde__vkif = mbly__osxp['apply_stub']
    return numba.core.utils.pysignature(pde__vkif)


def crosstab_dummy(index, columns, _pivot_values):
    return 0


@infer_global(crosstab_dummy)
class CrossTabTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        index, columns, _pivot_values = args
        mta__nxaiw = types.Array(types.int64, 1, 'C')
        htao__wcmge = _pivot_values.meta
        vove__plum = len(htao__wcmge)
        xowf__fbg = bodo.hiframes.pd_index_ext.array_type_to_index(index.
            data, types.StringLiteral('index'))
        ktrlv__ghm = DataFrameType((mta__nxaiw,) * vove__plum, xowf__fbg,
            tuple(htao__wcmge))
        return signature(ktrlv__ghm, *args)


CrossTabTyper._no_unliteral = True


@lower_builtin(crosstab_dummy, types.VarArg(types.Any))
def lower_crosstab_dummy(context, builder, sig, args):
    return context.get_constant_null(sig.return_type)


def get_group_indices(keys, dropna, _is_parallel):
    return np.arange(len(keys))


@overload(get_group_indices)
def get_group_indices_overload(keys, dropna, _is_parallel):
    sera__jrok = 'def impl(keys, dropna, _is_parallel):\n'
    sera__jrok += (
        "    ev = bodo.utils.tracing.Event('get_group_indices', _is_parallel)\n"
        )
    sera__jrok += '    info_list = [{}]\n'.format(', '.join(
        f'array_to_info(keys[{fxem__vmuqf}])' for fxem__vmuqf in range(len(
        keys.types))))
    sera__jrok += '    table = arr_info_list_to_table(info_list)\n'
    sera__jrok += '    group_labels = np.empty(len(keys[0]), np.int64)\n'
    sera__jrok += '    sort_idx = np.empty(len(keys[0]), np.int64)\n'
    sera__jrok += """    ngroups = get_groupby_labels(table, group_labels.ctypes, sort_idx.ctypes, dropna, _is_parallel)
"""
    sera__jrok += '    delete_table_decref_arrays(table)\n'
    sera__jrok += '    ev.finalize()\n'
    sera__jrok += '    return sort_idx, group_labels, ngroups\n'
    mbly__osxp = {}
    exec(sera__jrok, {'bodo': bodo, 'np': np, 'get_groupby_labels':
        get_groupby_labels, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'delete_table_decref_arrays': delete_table_decref_arrays}, mbly__osxp)
    yoiy__hyhyi = mbly__osxp['impl']
    return yoiy__hyhyi


@numba.njit(no_cpython_wrapper=True)
def generate_slices(labels, ngroups):
    ygqnr__ehpnv = len(labels)
    qnxij__nosaf = np.zeros(ngroups, dtype=np.int64)
    haikv__uanl = np.zeros(ngroups, dtype=np.int64)
    fkvo__nwt = 0
    zchza__njgz = 0
    for fxem__vmuqf in range(ygqnr__ehpnv):
        kilxm__agf = labels[fxem__vmuqf]
        if kilxm__agf < 0:
            fkvo__nwt += 1
        else:
            zchza__njgz += 1
            if fxem__vmuqf == ygqnr__ehpnv - 1 or kilxm__agf != labels[
                fxem__vmuqf + 1]:
                qnxij__nosaf[kilxm__agf] = fkvo__nwt
                haikv__uanl[kilxm__agf] = fkvo__nwt + zchza__njgz
                fkvo__nwt += zchza__njgz
                zchza__njgz = 0
    return qnxij__nosaf, haikv__uanl


def shuffle_dataframe(df, keys, _is_parallel):
    return df, keys, _is_parallel


@overload(shuffle_dataframe, prefer_literal=True)
def overload_shuffle_dataframe(df, keys, _is_parallel):
    yoiy__hyhyi, fjeh__tume = gen_shuffle_dataframe(df, keys, _is_parallel)
    return yoiy__hyhyi


def gen_shuffle_dataframe(df, keys, _is_parallel):
    yryrq__dhe = len(df.columns)
    zyyt__cioyw = len(keys.types)
    assert is_overload_constant_bool(_is_parallel
        ), 'shuffle_dataframe: _is_parallel is not a constant'
    sera__jrok = 'def impl(df, keys, _is_parallel):\n'
    if is_overload_false(_is_parallel):
        sera__jrok += '  return df, keys, get_null_shuffle_info()\n'
        mbly__osxp = {}
        exec(sera__jrok, {'get_null_shuffle_info': get_null_shuffle_info},
            mbly__osxp)
        yoiy__hyhyi = mbly__osxp['impl']
        return yoiy__hyhyi
    for fxem__vmuqf in range(yryrq__dhe):
        sera__jrok += f"""  in_arr{fxem__vmuqf} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {fxem__vmuqf})
"""
    sera__jrok += f"""  in_index_arr = bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
    sera__jrok += '  info_list = [{}, {}, {}]\n'.format(', '.join(
        f'array_to_info(keys[{fxem__vmuqf}])' for fxem__vmuqf in range(
        zyyt__cioyw)), ', '.join(f'array_to_info(in_arr{fxem__vmuqf})' for
        fxem__vmuqf in range(yryrq__dhe)), 'array_to_info(in_index_arr)')
    sera__jrok += '  table = arr_info_list_to_table(info_list)\n'
    sera__jrok += (
        f'  out_table = shuffle_table(table, {zyyt__cioyw}, _is_parallel, 1)\n'
        )
    for fxem__vmuqf in range(zyyt__cioyw):
        sera__jrok += f"""  out_key{fxem__vmuqf} = info_to_array(info_from_table(out_table, {fxem__vmuqf}), keys{fxem__vmuqf}_typ)
"""
    for fxem__vmuqf in range(yryrq__dhe):
        sera__jrok += f"""  out_arr{fxem__vmuqf} = info_to_array(info_from_table(out_table, {fxem__vmuqf + zyyt__cioyw}), in_arr{fxem__vmuqf}_typ)
"""
    sera__jrok += f"""  out_arr_index = info_to_array(info_from_table(out_table, {zyyt__cioyw + yryrq__dhe}), ind_arr_typ)
"""
    sera__jrok += '  shuffle_info = get_shuffle_info(out_table)\n'
    sera__jrok += '  delete_table(out_table)\n'
    sera__jrok += '  delete_table(table)\n'
    out_data = ', '.join(f'out_arr{fxem__vmuqf}' for fxem__vmuqf in range(
        yryrq__dhe))
    sera__jrok += (
        '  out_index = bodo.utils.conversion.index_from_array(out_arr_index)\n'
        )
    sera__jrok += f"""  out_df = bodo.hiframes.pd_dataframe_ext.init_dataframe(({out_data},), out_index, __col_name_meta_value_df_shuffle)
"""
    sera__jrok += '  return out_df, ({},), shuffle_info\n'.format(', '.join
        (f'out_key{fxem__vmuqf}' for fxem__vmuqf in range(zyyt__cioyw)))
    vncsj__atkjm = {'bodo': bodo, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_from_table': info_from_table, 'info_to_array':
        info_to_array, 'delete_table': delete_table, 'get_shuffle_info':
        get_shuffle_info, '__col_name_meta_value_df_shuffle':
        ColNamesMetaType(df.columns), 'ind_arr_typ': types.Array(types.
        int64, 1, 'C') if isinstance(df.index, RangeIndexType) else df.
        index.data}
    vncsj__atkjm.update({f'keys{fxem__vmuqf}_typ': keys.types[fxem__vmuqf] for
        fxem__vmuqf in range(zyyt__cioyw)})
    vncsj__atkjm.update({f'in_arr{fxem__vmuqf}_typ': df.data[fxem__vmuqf] for
        fxem__vmuqf in range(yryrq__dhe)})
    mbly__osxp = {}
    exec(sera__jrok, vncsj__atkjm, mbly__osxp)
    yoiy__hyhyi = mbly__osxp['impl']
    return yoiy__hyhyi, vncsj__atkjm


def reverse_shuffle(data, shuffle_info):
    return data


@overload(reverse_shuffle)
def overload_reverse_shuffle(data, shuffle_info):
    if isinstance(data, bodo.hiframes.pd_multi_index_ext.MultiIndexType):
        shsc__uyth = len(data.array_types)
        sera__jrok = 'def impl(data, shuffle_info):\n'
        sera__jrok += '  info_list = [{}]\n'.format(', '.join(
            f'array_to_info(data._data[{fxem__vmuqf}])' for fxem__vmuqf in
            range(shsc__uyth)))
        sera__jrok += '  table = arr_info_list_to_table(info_list)\n'
        sera__jrok += (
            '  out_table = reverse_shuffle_table(table, shuffle_info)\n')
        for fxem__vmuqf in range(shsc__uyth):
            sera__jrok += f"""  out_arr{fxem__vmuqf} = info_to_array(info_from_table(out_table, {fxem__vmuqf}), data._data[{fxem__vmuqf}])
"""
        sera__jrok += '  delete_table(out_table)\n'
        sera__jrok += '  delete_table(table)\n'
        sera__jrok += (
            '  return init_multi_index(({},), data._names, data._name)\n'.
            format(', '.join(f'out_arr{fxem__vmuqf}' for fxem__vmuqf in
            range(shsc__uyth))))
        mbly__osxp = {}
        exec(sera__jrok, {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'reverse_shuffle_table': reverse_shuffle_table,
            'info_from_table': info_from_table, 'info_to_array':
            info_to_array, 'delete_table': delete_table, 'init_multi_index':
            bodo.hiframes.pd_multi_index_ext.init_multi_index}, mbly__osxp)
        yoiy__hyhyi = mbly__osxp['impl']
        return yoiy__hyhyi
    if bodo.hiframes.pd_index_ext.is_index_type(data):

        def impl_index(data, shuffle_info):
            bxs__gca = bodo.utils.conversion.index_to_array(data)
            vbbi__vqb = reverse_shuffle(bxs__gca, shuffle_info)
            return bodo.utils.conversion.index_from_array(vbbi__vqb)
        return impl_index

    def impl_arr(data, shuffle_info):
        zdm__avx = [array_to_info(data)]
        tlj__uadtr = arr_info_list_to_table(zdm__avx)
        qvz__yad = reverse_shuffle_table(tlj__uadtr, shuffle_info)
        vbbi__vqb = info_to_array(info_from_table(qvz__yad, 0), data)
        delete_table(qvz__yad)
        delete_table(tlj__uadtr)
        return vbbi__vqb
    return impl_arr


@overload_method(DataFrameGroupByType, 'value_counts', inline='always',
    no_unliteral=True)
def groupby_value_counts(grp, normalize=False, sort=True, ascending=False,
    bins=None, dropna=True):
    lqc__vlri = dict(normalize=normalize, sort=sort, bins=bins, dropna=dropna)
    qpbj__pzvjf = dict(normalize=False, sort=True, bins=None, dropna=True)
    check_unsupported_args('Groupby.value_counts', lqc__vlri, qpbj__pzvjf,
        package_name='pandas', module_name='GroupBy')
    if len(grp.selection) > 1 or not grp.as_index:
        raise BodoError(
            "'DataFrameGroupBy' object has no attribute 'value_counts'")
    if not is_overload_constant_bool(ascending):
        raise BodoError(
            'Groupby.value_counts() ascending must be a constant boolean')
    hhe__rnv = get_overload_const_bool(ascending)
    ghmm__eqxrk = grp.selection[0]
    sera__jrok = f"""def impl(grp, normalize=False, sort=True, ascending=False, bins=None, dropna=True):
"""
    fsqnh__oomp = (
        f"lambda S: S.value_counts(ascending={hhe__rnv}, _index_name='{ghmm__eqxrk}')"
        )
    sera__jrok += f'    return grp.apply({fsqnh__oomp})\n'
    mbly__osxp = {}
    exec(sera__jrok, {'bodo': bodo}, mbly__osxp)
    yoiy__hyhyi = mbly__osxp['impl']
    return yoiy__hyhyi


groupby_unsupported_attr = {'groups', 'indices'}
groupby_unsupported = {'__iter__', 'get_group', 'all', 'any', 'bfill',
    'backfill', 'cumcount', 'cummax', 'cummin', 'cumprod', 'ffill', 'nth',
    'ohlc', 'pad', 'rank', 'pct_change', 'sem', 'tail', 'corr', 'cov',
    'describe', 'diff', 'fillna', 'filter', 'hist', 'mad', 'plot',
    'quantile', 'resample', 'sample', 'skew', 'take', 'tshift'}
series_only_unsupported_attrs = {'is_monotonic_increasing',
    'is_monotonic_decreasing'}
series_only_unsupported = {'nlargest', 'nsmallest', 'unique'}
dataframe_only_unsupported = {'corrwith', 'boxplot'}


def _install_groupby_unsupported():
    for qra__bbs in groupby_unsupported_attr:
        overload_attribute(DataFrameGroupByType, qra__bbs, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{qra__bbs}'))
    for qra__bbs in groupby_unsupported:
        overload_method(DataFrameGroupByType, qra__bbs, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{qra__bbs}'))
    for qra__bbs in series_only_unsupported_attrs:
        overload_attribute(DataFrameGroupByType, qra__bbs, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{qra__bbs}'))
    for qra__bbs in series_only_unsupported:
        overload_method(DataFrameGroupByType, qra__bbs, no_unliteral=True)(
            create_unsupported_overload(f'SeriesGroupBy.{qra__bbs}'))
    for qra__bbs in dataframe_only_unsupported:
        overload_method(DataFrameGroupByType, qra__bbs, no_unliteral=True)(
            create_unsupported_overload(f'DataFrameGroupBy.{qra__bbs}'))


_install_groupby_unsupported()
