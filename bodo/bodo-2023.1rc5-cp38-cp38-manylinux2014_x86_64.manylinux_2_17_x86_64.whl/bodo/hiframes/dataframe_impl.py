"""
Implementation of DataFrame attributes and methods using overload.
"""
import operator
import re
import warnings
from collections import namedtuple
from typing import Tuple
import numba
import numpy as np
import pandas as pd
from numba.core import cgutils, ir, types
from numba.core.imputils import RefType, impl_ret_borrowed, impl_ret_new_ref, iternext_impl, lower_builtin
from numba.core.ir_utils import mk_unique_var, next_label
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import lower_getattr, models, overload, overload_attribute, overload_method, register_model, type_callable
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import _no_input, datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported, handle_inplace_df_type_change
from bodo.hiframes.pd_index_ext import DatetimeIndexType, RangeIndexType, StringIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import SeriesType, if_series_to_array_type
from bodo.hiframes.pd_timestamp_ext import pd_timestamp_tz_naive_type
from bodo.hiframes.rolling import is_supported_shift_array_type
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.hiframes.time_ext import TimeArrayType
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.transform import bodo_types_with_params, gen_const_tup, no_side_effect_call_tuples
from bodo.utils.typing import BodoError, BodoWarning, ColNamesMetaType, check_unsupported_args, dtype_to_array_type, ensure_constant_arg, ensure_constant_values, get_castable_arr_dtype, get_index_data_arr_types, get_index_names, get_literal_value, get_nullable_and_non_nullable_types, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_tuple, get_overload_constant_dict, get_overload_constant_series, is_common_scalar_dtype, is_literal_type, is_overload_bool, is_overload_bool_list, is_overload_constant_bool, is_overload_constant_dict, is_overload_constant_int, is_overload_constant_list, is_overload_constant_series, is_overload_constant_str, is_overload_constant_tuple, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_overload_zero, is_scalar_type, parse_dtype, raise_bodo_error, unliteral_val
from bodo.utils.utils import is_array_typ


@overload_attribute(DataFrameType, 'index', inline='always')
def overload_dataframe_index(df):
    return lambda df: bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)


def generate_col_to_index_func_text(col_names: Tuple):
    if all(isinstance(a, str) for a in col_names) or all(isinstance(a,
        bytes) for a in col_names):
        vwxto__xaddo = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return (
            f'bodo.hiframes.pd_index_ext.init_binary_str_index({vwxto__xaddo})\n'
            )
    elif all(isinstance(a, (int, float)) for a in col_names):
        arr = f'bodo.utils.conversion.coerce_to_array({col_names})'
        return f'bodo.hiframes.pd_index_ext.init_numeric_index({arr})\n'
    else:
        return f'bodo.hiframes.pd_index_ext.init_heter_index({col_names})\n'


@overload_attribute(DataFrameType, 'columns', inline='always')
def overload_dataframe_columns(df):
    dvhz__hbzun = 'def impl(df):\n'
    if df.has_runtime_cols:
        dvhz__hbzun += (
            '  return bodo.hiframes.pd_dataframe_ext.get_dataframe_column_names(df)\n'
            )
    else:
        gctc__qzcve = (bodo.hiframes.dataframe_impl.
            generate_col_to_index_func_text(df.columns))
        dvhz__hbzun += f'  return {gctc__qzcve}'
    unozl__xox = {}
    exec(dvhz__hbzun, {'bodo': bodo}, unozl__xox)
    impl = unozl__xox['impl']
    return impl


@overload_attribute(DataFrameType, 'values')
def overload_dataframe_values(df):
    check_runtime_cols_unsupported(df, 'DataFrame.values')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.values')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.values: only supported for dataframes containing numeric values'
            )
    zlzx__dvfjm = len(df.columns)
    srb__fkv = set(i for i in range(zlzx__dvfjm) if isinstance(df.data[i],
        IntegerArrayType))
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(i, '.astype(float)' if i in srb__fkv else '') for i in range
        (zlzx__dvfjm))
    dvhz__hbzun = 'def f(df):\n'.format()
    dvhz__hbzun += '    return np.stack(({},), 1)\n'.format(data_args)
    unozl__xox = {}
    exec(dvhz__hbzun, {'bodo': bodo, 'np': np}, unozl__xox)
    sgpj__kqmpb = unozl__xox['f']
    return sgpj__kqmpb


@overload_method(DataFrameType, 'to_numpy', inline='always', no_unliteral=True)
def overload_dataframe_to_numpy(df, dtype=None, copy=False, na_value=_no_input
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.to_numpy()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.to_numpy()')
    if not is_df_values_numpy_supported_dftyp(df):
        raise_bodo_error(
            'DataFrame.to_numpy(): only supported for dataframes containing numeric values'
            )
    zzfx__trn = {'dtype': dtype, 'na_value': na_value}
    nwf__nku = {'dtype': None, 'na_value': _no_input}
    check_unsupported_args('DataFrame.to_numpy', zzfx__trn, nwf__nku,
        package_name='pandas', module_name='DataFrame')

    def impl(df, dtype=None, copy=False, na_value=_no_input):
        return df.values
    return impl


@overload_attribute(DataFrameType, 'ndim', inline='always')
def overload_dataframe_ndim(df):
    return lambda df: 2


@overload_attribute(DataFrameType, 'size')
def overload_dataframe_size(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            vcbh__wjibz = bodo.hiframes.table.compute_num_runtime_columns(t)
            return vcbh__wjibz * len(t)
        return impl
    ncols = len(df.columns)
    return lambda df: ncols * len(df)


@lower_getattr(DataFrameType, 'shape')
def lower_dataframe_shape(context, builder, typ, val):
    impl = overload_dataframe_shape(typ)
    return context.compile_internal(builder, impl, types.Tuple([types.int64,
        types.int64])(typ), (val,))


def overload_dataframe_shape(df):
    if df.has_runtime_cols:

        def impl(df):
            t = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            vcbh__wjibz = bodo.hiframes.table.compute_num_runtime_columns(t)
            return len(t), vcbh__wjibz
        return impl
    ncols = len(df.columns)
    return lambda df: (len(df), ncols)


@overload_attribute(DataFrameType, 'dtypes')
def overload_dataframe_dtypes(df):
    check_runtime_cols_unsupported(df, 'DataFrame.dtypes')
    dvhz__hbzun = 'def impl(df):\n'
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype\n'
         for i in range(len(df.columns)))
    mvg__sza = ',' if len(df.columns) == 1 else ''
    index = f'bodo.hiframes.pd_index_ext.init_heter_index({df.columns})'
    dvhz__hbzun += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}{mvg__sza}), {index}, None)
"""
    unozl__xox = {}
    exec(dvhz__hbzun, {'bodo': bodo}, unozl__xox)
    impl = unozl__xox['impl']
    return impl


@overload_attribute(DataFrameType, 'empty')
def overload_dataframe_empty(df):
    check_runtime_cols_unsupported(df, 'DataFrame.empty')
    if len(df.columns) == 0:
        return lambda df: True
    return lambda df: len(df) == 0


@overload_method(DataFrameType, 'assign', no_unliteral=True)
def overload_dataframe_assign(df, **kwargs):
    check_runtime_cols_unsupported(df, 'DataFrame.assign()')
    raise_bodo_error('Invalid df.assign() call')


@overload_method(DataFrameType, 'insert', no_unliteral=True)
def overload_dataframe_insert(df, loc, column, value, allow_duplicates=False):
    check_runtime_cols_unsupported(df, 'DataFrame.insert()')
    raise_bodo_error('Invalid df.insert() call')


def _get_dtype_str(dtype):
    if isinstance(dtype, types.Function):
        if dtype.key[0] == str:
            return "'str'"
        elif dtype.key[0] == float:
            return 'float'
        elif dtype.key[0] == int:
            return 'int'
        elif dtype.key[0] == bool:
            return 'bool'
        else:
            raise BodoError(f'invalid dtype: {dtype}')
    if type(dtype) in bodo.libs.int_arr_ext.pd_int_dtype_classes:
        return dtype.name
    if isinstance(dtype, types.DTypeSpec):
        dtype = dtype.dtype
    if isinstance(dtype, types.functions.NumberClass):
        return f"'{dtype.key}'"
    if isinstance(dtype, types.PyObject) or dtype in (object, 'object'):
        return "'object'"
    if dtype in (bodo.libs.str_arr_ext.string_dtype, pd.StringDtype()):
        return 'str'
    return f"'{dtype}'"


@overload_method(DataFrameType, 'astype', inline='always', no_unliteral=True)
def overload_dataframe_astype(df, dtype, copy=True, errors='raise',
    _bodo_nan_to_str=True, _bodo_object_typeref=None):
    check_runtime_cols_unsupported(df, 'DataFrame.astype()')
    zzfx__trn = {'errors': errors}
    nwf__nku = {'errors': 'raise'}
    check_unsupported_args('df.astype', zzfx__trn, nwf__nku, package_name=
        'pandas', module_name='DataFrame')
    if dtype == types.unicode_type:
        raise_bodo_error(
            "DataFrame.astype(): 'dtype' when passed as string must be a constant value"
            )
    if not is_overload_bool(copy):
        raise BodoError("DataFrame.astype(): 'copy' must be a boolean value")
    extra_globals = None
    header = """def impl(df, dtype, copy=True, errors='raise', _bodo_nan_to_str=True, _bodo_object_typeref=None):
"""
    if df.is_table_format:
        extra_globals = {}
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        gmq__kdrpz = []
    if _bodo_object_typeref is not None:
        assert isinstance(_bodo_object_typeref, types.TypeRef
            ), 'Bodo schema used in DataFrame.astype should be a TypeRef'
        qkzrd__fuy = _bodo_object_typeref.instance_type
        assert isinstance(qkzrd__fuy, DataFrameType
            ), 'Bodo schema used in DataFrame.astype is only supported for DataFrame schemas'
        if df.is_table_format:
            for i, name in enumerate(df.columns):
                if name in qkzrd__fuy.column_index:
                    idx = qkzrd__fuy.column_index[name]
                    arr_typ = qkzrd__fuy.data[idx]
                else:
                    arr_typ = df.data[i]
                gmq__kdrpz.append(arr_typ)
        else:
            extra_globals = {}
            rzby__kuspg = {}
            for i, name in enumerate(qkzrd__fuy.columns):
                arr_typ = qkzrd__fuy.data[i]
                extra_globals[f'_bodo_schema{i}'] = get_castable_arr_dtype(
                    arr_typ)
                rzby__kuspg[name] = f'_bodo_schema{i}'
            data_args = ', '.join(
                f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {rzby__kuspg[ibfb__ifl]}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
                 if ibfb__ifl in rzby__kuspg else
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
                 for i, ibfb__ifl in enumerate(df.columns))
    elif is_overload_constant_dict(dtype) or is_overload_constant_series(dtype
        ):
        qsq__pphlb = get_overload_constant_dict(dtype
            ) if is_overload_constant_dict(dtype) else dict(
            get_overload_constant_series(dtype))
        if df.is_table_format:
            qsq__pphlb = {name: dtype_to_array_type(parse_dtype(dtype)) for
                name, dtype in qsq__pphlb.items()}
            for i, name in enumerate(df.columns):
                if name in qsq__pphlb:
                    arr_typ = qsq__pphlb[name]
                else:
                    arr_typ = df.data[i]
                gmq__kdrpz.append(arr_typ)
        else:
            data_args = ', '.join(
                f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {_get_dtype_str(qsq__pphlb[ibfb__ifl])}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
                 if ibfb__ifl in qsq__pphlb else
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
                 for i, ibfb__ifl in enumerate(df.columns))
    elif df.is_table_format:
        arr_typ = dtype_to_array_type(parse_dtype(dtype))
        gmq__kdrpz = [arr_typ] * len(df.columns)
    else:
        data_args = ', '.join(
            f'bodo.utils.conversion.fix_arr_dtype(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dtype, copy, nan_to_str=_bodo_nan_to_str, from_series=True)'
             for i in range(len(df.columns)))
    if df.is_table_format:
        bayni__vifk = bodo.TableType(tuple(gmq__kdrpz))
        extra_globals['out_table_typ'] = bayni__vifk
        data_args = (
            'bodo.utils.table_utils.table_astype(table, out_table_typ, copy, _bodo_nan_to_str)'
            )
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'copy', inline='always', no_unliteral=True)
def overload_dataframe_copy(df, deep=True):
    check_runtime_cols_unsupported(df, 'DataFrame.copy()')
    header = 'def impl(df, deep=True):\n'
    extra_globals = None
    if df.is_table_format:
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        xfbp__nlbf = types.none
        extra_globals = {'output_arr_typ': xfbp__nlbf}
        if is_overload_false(deep):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
        elif is_overload_true(deep):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' + 'True)')
        else:
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' +
                'True) if deep else bodo.utils.table_utils.generate_mappable_table_func('
                 + 'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
    else:
        jataz__lzvg = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(deep):
                jataz__lzvg.append(arr + '.copy()')
            elif is_overload_false(deep):
                jataz__lzvg.append(arr)
            else:
                jataz__lzvg.append(f'{arr}.copy() if deep else {arr}')
        data_args = ', '.join(jataz__lzvg)
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'rename', inline='always', no_unliteral=True)
def overload_dataframe_rename(df, mapper=None, index=None, columns=None,
    axis=None, copy=True, inplace=False, level=None, errors='ignore',
    _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.rename()')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'rename')
    zzfx__trn = {'index': index, 'level': level, 'errors': errors}
    nwf__nku = {'index': None, 'level': None, 'errors': 'ignore'}
    check_unsupported_args('DataFrame.rename', zzfx__trn, nwf__nku,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.rename(): 'inplace' keyword only supports boolean constant assignment"
            )
    if not is_overload_none(mapper):
        if not is_overload_none(columns):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'mapper' and 'columns'"
                )
        if not (is_overload_constant_int(axis) and get_overload_const_int(
            axis) == 1):
            raise BodoError(
                "DataFrame.rename(): 'mapper' only supported with axis=1")
        if not is_overload_constant_dict(mapper):
            raise_bodo_error(
                "'mapper' argument to DataFrame.rename() should be a constant dictionary"
                )
        qgkyu__cmtdh = get_overload_constant_dict(mapper)
    elif not is_overload_none(columns):
        if not is_overload_none(axis):
            raise BodoError(
                "DataFrame.rename(): Cannot specify both 'axis' and 'columns'")
        if not is_overload_constant_dict(columns):
            raise_bodo_error(
                "'columns' argument to DataFrame.rename() should be a constant dictionary"
                )
        qgkyu__cmtdh = get_overload_constant_dict(columns)
    else:
        raise_bodo_error(
            "DataFrame.rename(): must pass columns either via 'mapper' and 'axis'=1 or 'columns'"
            )
    jixx__ebagc = tuple([qgkyu__cmtdh.get(df.columns[i], df.columns[i]) for
        i in range(len(df.columns))])
    header = """def impl(df, mapper=None, index=None, columns=None, axis=None, copy=True, inplace=False, level=None, errors='ignore', _bodo_transformed=False):
"""
    extra_globals = None
    lna__mkroj = None
    if df.is_table_format:
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        lna__mkroj = df.copy(columns=jixx__ebagc)
        xfbp__nlbf = types.none
        extra_globals = {'output_arr_typ': xfbp__nlbf}
        if is_overload_false(copy):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
        elif is_overload_true(copy):
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' + 'True)')
        else:
            data_args = (
                'bodo.utils.table_utils.generate_mappable_table_func(' +
                'table, ' + "'copy', " + 'output_arr_typ, ' +
                'True) if copy else bodo.utils.table_utils.generate_mappable_table_func('
                 + 'table, ' + 'None, ' + 'output_arr_typ, ' + 'True)')
    else:
        jataz__lzvg = []
        for i in range(len(df.columns)):
            arr = f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
            if is_overload_true(copy):
                jataz__lzvg.append(arr + '.copy()')
            elif is_overload_false(copy):
                jataz__lzvg.append(arr)
            else:
                jataz__lzvg.append(f'{arr}.copy() if copy else {arr}')
        data_args = ', '.join(jataz__lzvg)
    return _gen_init_df(header, jixx__ebagc, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'filter', no_unliteral=True)
def overload_dataframe_filter(df, items=None, like=None, regex=None, axis=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.filter()')
    rmsuf__cues = not is_overload_none(items)
    ngggl__cty = not is_overload_none(like)
    vjl__ffwp = not is_overload_none(regex)
    myin__qnxb = rmsuf__cues ^ ngggl__cty ^ vjl__ffwp
    acny__rmpeb = not (rmsuf__cues or ngggl__cty or vjl__ffwp)
    if acny__rmpeb:
        raise BodoError(
            'DataFrame.filter(): one of keyword arguments `items`, `like`, and `regex` must be supplied'
            )
    if not myin__qnxb:
        raise BodoError(
            'DataFrame.filter(): keyword arguments `items`, `like`, and `regex` are mutually exclusive'
            )
    if is_overload_none(axis):
        axis = 'columns'
    if is_overload_constant_str(axis):
        axis = get_overload_const_str(axis)
        if axis not in {'index', 'columns'}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either "index" or "columns" if string'
                )
        xzou__jmjip = 0 if axis == 'index' else 1
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
        if axis not in {0, 1}:
            raise_bodo_error(
                'DataFrame.filter(): keyword arguments `axis` must be either 0 or 1 if integer'
                )
        xzou__jmjip = axis
    else:
        raise_bodo_error(
            'DataFrame.filter(): keyword arguments `axis` must be constant string or integer'
            )
    assert xzou__jmjip in {0, 1}
    dvhz__hbzun = (
        'def impl(df, items=None, like=None, regex=None, axis=None):\n')
    if xzou__jmjip == 0:
        raise BodoError(
            'DataFrame.filter(): filtering based on index is not supported.')
    if xzou__jmjip == 1:
        tbrx__zqhmz = []
        cfbzh__peyu = []
        hbwk__jzh = []
        if rmsuf__cues:
            if is_overload_constant_list(items):
                ygn__dfbec = get_overload_const_list(items)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'items' must be a list of constant strings."
                    )
        if ngggl__cty:
            if is_overload_constant_str(like):
                lso__sxq = get_overload_const_str(like)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'like' must be a constant string."
                    )
        if vjl__ffwp:
            if is_overload_constant_str(regex):
                lyt__lslv = get_overload_const_str(regex)
                gqjin__ymb = re.compile(lyt__lslv)
            else:
                raise BodoError(
                    "Dataframe.filter(): argument 'regex' must be a constant string."
                    )
        for i, ibfb__ifl in enumerate(df.columns):
            if not is_overload_none(items
                ) and ibfb__ifl in ygn__dfbec or not is_overload_none(like
                ) and lso__sxq in str(ibfb__ifl) or not is_overload_none(regex
                ) and gqjin__ymb.search(str(ibfb__ifl)):
                cfbzh__peyu.append(ibfb__ifl)
                hbwk__jzh.append(i)
        for i in hbwk__jzh:
            var_name = f'data_{i}'
            tbrx__zqhmz.append(var_name)
            dvhz__hbzun += f"""  {var_name} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})
"""
        data_args = ', '.join(tbrx__zqhmz)
        return _gen_init_df(dvhz__hbzun, cfbzh__peyu, data_args)


@overload_method(DataFrameType, 'isna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'isnull', inline='always', no_unliteral=True)
def overload_dataframe_isna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.isna()')
    header = 'def impl(df):\n'
    extra_globals = None
    lna__mkroj = None
    if df.is_table_format:
        xfbp__nlbf = types.Array(types.bool_, 1, 'C')
        lna__mkroj = DataFrameType(tuple([xfbp__nlbf] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': xfbp__nlbf}
        data_args = ('bodo.utils.table_utils.generate_mappable_table_func(' +
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), ' +
            "'bodo.libs.array_ops.array_op_isna', " + 'output_arr_typ, ' +
            'False)')
    else:
        data_args = ', '.join(
            f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


@overload_method(DataFrameType, 'select_dtypes', inline='always',
    no_unliteral=True)
def overload_dataframe_select_dtypes(df, include=None, exclude=None):
    check_runtime_cols_unsupported(df, 'DataFrame.select_dtypes')
    uzla__vky = is_overload_none(include)
    qxkgu__pbphp = is_overload_none(exclude)
    sjed__uxekl = 'DataFrame.select_dtypes'
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.select_dtypes()')
    if uzla__vky and qxkgu__pbphp:
        raise_bodo_error(
            'DataFrame.select_dtypes() At least one of include or exclude must not be none'
            )

    def is_legal_input(elem):
        return is_overload_constant_str(elem) or isinstance(elem, types.
            DTypeSpec) or isinstance(elem, types.Function)
    if not uzla__vky:
        if is_overload_constant_list(include):
            include = get_overload_const_list(include)
            iqwv__sfgjx = [dtype_to_array_type(parse_dtype(elem,
                sjed__uxekl)) for elem in include]
        elif is_legal_input(include):
            iqwv__sfgjx = [dtype_to_array_type(parse_dtype(include,
                sjed__uxekl))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        iqwv__sfgjx = get_nullable_and_non_nullable_types(iqwv__sfgjx)
        lsh__zfnwl = tuple(ibfb__ifl for i, ibfb__ifl in enumerate(df.
            columns) if df.data[i] in iqwv__sfgjx)
    else:
        lsh__zfnwl = df.columns
    if not qxkgu__pbphp:
        if is_overload_constant_list(exclude):
            exclude = get_overload_const_list(exclude)
            ogyfo__wxv = [dtype_to_array_type(parse_dtype(elem, sjed__uxekl
                )) for elem in exclude]
        elif is_legal_input(exclude):
            ogyfo__wxv = [dtype_to_array_type(parse_dtype(exclude,
                sjed__uxekl))]
        else:
            raise_bodo_error(
                'DataFrame.select_dtypes() only supports constant strings or types as arguments'
                )
        ogyfo__wxv = get_nullable_and_non_nullable_types(ogyfo__wxv)
        lsh__zfnwl = tuple(ibfb__ifl for ibfb__ifl in lsh__zfnwl if df.data
            [df.column_index[ibfb__ifl]] not in ogyfo__wxv)
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[ibfb__ifl]})'
         for ibfb__ifl in lsh__zfnwl)
    header = 'def impl(df, include=None, exclude=None):\n'
    return _gen_init_df(header, lsh__zfnwl, data_args)


@overload_method(DataFrameType, 'notna', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'notnull', inline='always', no_unliteral=True)
def overload_dataframe_notna(df):
    check_runtime_cols_unsupported(df, 'DataFrame.notna()')
    header = 'def impl(df):\n'
    extra_globals = None
    lna__mkroj = None
    if df.is_table_format:
        xfbp__nlbf = types.Array(types.bool_, 1, 'C')
        lna__mkroj = DataFrameType(tuple([xfbp__nlbf] * len(df.data)), df.
            index, df.columns, df.dist, is_table_format=True)
        extra_globals = {'output_arr_typ': xfbp__nlbf}
        data_args = ('bodo.utils.table_utils.generate_mappable_table_func(' +
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), ' +
            "'~bodo.libs.array_ops.array_op_isna', " + 'output_arr_typ, ' +
            'False)')
    else:
        data_args = ', '.join(
            f'bodo.libs.array_ops.array_op_isna(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})) == False'
             for i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args, extra_globals=
        extra_globals)


def overload_dataframe_head(df, n=5):
    if df.is_table_format:
        data_args = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[:n]')
    else:
        data_args = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:n]'
             for i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:n]'
    return _gen_init_df(header, df.columns, data_args, index)


@lower_builtin('df.head', DataFrameType, types.Integer)
@lower_builtin('df.head', DataFrameType, types.Omitted)
def dataframe_head_lower(context, builder, sig, args):
    impl = overload_dataframe_head(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'tail', inline='always', no_unliteral=True)
def overload_dataframe_tail(df, n=5):
    check_runtime_cols_unsupported(df, 'DataFrame.tail()')
    if not is_overload_int(n):
        raise BodoError("Dataframe.tail(): 'n' must be an Integer")
    if df.is_table_format:
        data_args = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[m:]')
    else:
        data_args = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[m:]'
             for i in range(len(df.columns)))
    header = 'def impl(df, n=5):\n'
    header += '  m = bodo.hiframes.series_impl.tail_slice(len(df), n)\n'
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[m:]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'first', inline='always', no_unliteral=True)
def overload_dataframe_first(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.first()')
    pyhms__caso = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError(
            'DataFrame.first(): only supports a DatetimeIndex index')
    if types.unliteral(offset) not in pyhms__caso:
        raise BodoError(
            "DataFrame.first(): 'offset' must be an string or DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.first()')
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[:valid_entries]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[:valid_entries]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    start_date = df_index[0]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, start_date, False)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'last', inline='always', no_unliteral=True)
def overload_dataframe_last(df, offset):
    check_runtime_cols_unsupported(df, 'DataFrame.last()')
    pyhms__caso = (types.unicode_type, bodo.month_begin_type, bodo.
        month_end_type, bodo.week_type, bodo.date_offset_type)
    if not isinstance(df.index, DatetimeIndexType):
        raise BodoError('DataFrame.last(): only supports a DatetimeIndex index'
            )
    if types.unliteral(offset) not in pyhms__caso:
        raise BodoError(
            "DataFrame.last(): 'offset' must be an string or DateOffset")
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.last()')
    index = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[len(df)-valid_entries:]'
        )
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})[len(df)-valid_entries:]'
         for i in range(len(df.columns)))
    header = 'def impl(df, offset):\n'
    header += (
        '  df_index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
        )
    header += '  if len(df_index):\n'
    header += '    final_date = df_index[-1]\n'
    header += """    valid_entries = bodo.libs.array_kernels.get_valid_entries_from_date_offset(df_index, offset, final_date, True)
"""
    header += '  else:\n'
    header += '    valid_entries = 0\n'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'to_string', no_unliteral=True)
def to_string_overload(df, buf=None, columns=None, col_space=None, header=
    True, index=True, na_rep='NaN', formatters=None, float_format=None,
    sparsify=None, index_names=True, justify=None, max_rows=None, min_rows=
    None, max_cols=None, show_dimensions=False, decimal='.', line_width=
    None, max_colwidth=None, encoding=None):
    check_runtime_cols_unsupported(df, 'DataFrame.to_string()')

    def impl(df, buf=None, columns=None, col_space=None, header=True, index
        =True, na_rep='NaN', formatters=None, float_format=None, sparsify=
        None, index_names=True, justify=None, max_rows=None, min_rows=None,
        max_cols=None, show_dimensions=False, decimal='.', line_width=None,
        max_colwidth=None, encoding=None):
        with numba.objmode(res='string'):
            res = df.to_string(buf=buf, columns=columns, col_space=
                col_space, header=header, index=index, na_rep=na_rep,
                formatters=formatters, float_format=float_format, sparsify=
                sparsify, index_names=index_names, justify=justify,
                max_rows=max_rows, min_rows=min_rows, max_cols=max_cols,
                show_dimensions=show_dimensions, decimal=decimal,
                line_width=line_width, max_colwidth=max_colwidth, encoding=
                encoding)
        return res
    return impl


@overload_method(DataFrameType, 'isin', inline='always', no_unliteral=True)
def overload_dataframe_isin(df, values):
    check_runtime_cols_unsupported(df, 'DataFrame.isin()')
    from bodo.utils.typing import is_iterable_type
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.isin()')
    dvhz__hbzun = 'def impl(df, values):\n'
    vdqs__bfr = {}
    wffu__aauvd = False
    if isinstance(values, DataFrameType):
        wffu__aauvd = True
        for i, ibfb__ifl in enumerate(df.columns):
            if ibfb__ifl in values.column_index:
                vufsi__nuv = 'val{}'.format(i)
                dvhz__hbzun += f"""  {vufsi__nuv} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(values, {values.column_index[ibfb__ifl]})
"""
                vdqs__bfr[ibfb__ifl] = vufsi__nuv
    elif is_iterable_type(values) and not isinstance(values, SeriesType):
        vdqs__bfr = {ibfb__ifl: 'values' for ibfb__ifl in df.columns}
    else:
        raise_bodo_error(f'pd.isin(): not supported for type {values}')
    data = []
    for i in range(len(df.columns)):
        vufsi__nuv = 'data{}'.format(i)
        dvhz__hbzun += (
            '  {} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})\n'
            .format(vufsi__nuv, i))
        data.append(vufsi__nuv)
    fgpl__bvn = ['out{}'.format(i) for i in range(len(df.columns))]
    tewg__vstgw = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  m = len({1})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] == {1}[i] if i < m else False
"""
    figz__mgkhw = """
  numba.parfors.parfor.init_prange()
  n = len({0})
  {2} = np.empty(n, np.bool_)
  for i in numba.parfors.parfor.internal_prange(n):
    {2}[i] = {0}[i] in {1}
"""
    hsv__bwwn = '  {} = np.zeros(len(df), np.bool_)\n'
    for i, (cname, ybbmk__khlc) in enumerate(zip(df.columns, data)):
        if cname in vdqs__bfr:
            jdja__gteik = vdqs__bfr[cname]
            if wffu__aauvd:
                dvhz__hbzun += tewg__vstgw.format(ybbmk__khlc, jdja__gteik,
                    fgpl__bvn[i])
            else:
                dvhz__hbzun += figz__mgkhw.format(ybbmk__khlc, jdja__gteik,
                    fgpl__bvn[i])
        else:
            dvhz__hbzun += hsv__bwwn.format(fgpl__bvn[i])
    return _gen_init_df(dvhz__hbzun, df.columns, ','.join(fgpl__bvn))


@overload_method(DataFrameType, 'abs', inline='always', no_unliteral=True)
def overload_dataframe_abs(df):
    check_runtime_cols_unsupported(df, 'DataFrame.abs()')
    for arr_typ in df.data:
        if not (isinstance(arr_typ.dtype, types.Number) or arr_typ.dtype ==
            bodo.timedelta64ns):
            raise_bodo_error(
                f'DataFrame.abs(): Only supported for numeric and Timedelta. Encountered array with dtype {arr_typ.dtype}'
                )
    zlzx__dvfjm = len(df.columns)
    data_args = ', '.join(
        'np.abs(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
        .format(i) for i in range(zlzx__dvfjm))
    header = 'def impl(df):\n'
    return _gen_init_df(header, df.columns, data_args)


def overload_dataframe_corr(df, method='pearson', min_periods=1):
    zmynk__yylt = [ibfb__ifl for ibfb__ifl, uibz__fawu in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(uibz__fawu.
        dtype)]
    assert len(zmynk__yylt) != 0
    ydiu__ntel = ''
    if not any(uibz__fawu == types.float64 for uibz__fawu in df.data):
        ydiu__ntel = '.astype(np.float64)'
    yju__olmtq = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[ibfb__ifl], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[ibfb__ifl]], IntegerArrayType) or
        df.data[df.column_index[ibfb__ifl]] == boolean_array else '') for
        ibfb__ifl in zmynk__yylt)
    tzdy__diqiq = 'np.stack(({},), 1){}'.format(yju__olmtq, ydiu__ntel)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        zmynk__yylt)))
    index = f'{generate_col_to_index_func_text(zmynk__yylt)}\n'
    header = "def impl(df, method='pearson', min_periods=1):\n"
    header += '  mat = {}\n'.format(tzdy__diqiq)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 0, min_periods)\n'
    return _gen_init_df(header, zmynk__yylt, data_args, index)


@lower_builtin('df.corr', DataFrameType, types.VarArg(types.Any))
def dataframe_corr_lower(context, builder, sig, args):
    impl = overload_dataframe_corr(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@overload_method(DataFrameType, 'cov', inline='always', no_unliteral=True)
def overload_dataframe_cov(df, min_periods=None, ddof=1):
    check_runtime_cols_unsupported(df, 'DataFrame.cov()')
    hwzb__jnck = dict(ddof=ddof)
    szrb__ldodx = dict(ddof=1)
    check_unsupported_args('DataFrame.cov', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    dhdx__hilh = '1' if is_overload_none(min_periods) else 'min_periods'
    zmynk__yylt = [ibfb__ifl for ibfb__ifl, uibz__fawu in zip(df.columns,
        df.data) if bodo.utils.typing._is_pandas_numeric_dtype(uibz__fawu.
        dtype)]
    if len(zmynk__yylt) == 0:
        raise_bodo_error('DataFrame.cov(): requires non-empty dataframe')
    ydiu__ntel = ''
    if not any(uibz__fawu == types.float64 for uibz__fawu in df.data):
        ydiu__ntel = '.astype(np.float64)'
    yju__olmtq = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[ibfb__ifl], '.astype(np.float64)' if 
        isinstance(df.data[df.column_index[ibfb__ifl]], IntegerArrayType) or
        df.data[df.column_index[ibfb__ifl]] == boolean_array else '') for
        ibfb__ifl in zmynk__yylt)
    tzdy__diqiq = 'np.stack(({},), 1){}'.format(yju__olmtq, ydiu__ntel)
    data_args = ', '.join('res[:,{}]'.format(i) for i in range(len(
        zmynk__yylt)))
    index = f'pd.Index({zmynk__yylt})\n'
    header = 'def impl(df, min_periods=None, ddof=1):\n'
    header += '  mat = {}\n'.format(tzdy__diqiq)
    header += '  res = bodo.libs.array_kernels.nancorr(mat, 1, {})\n'.format(
        dhdx__hilh)
    return _gen_init_df(header, zmynk__yylt, data_args, index)


@overload_method(DataFrameType, 'count', inline='always', no_unliteral=True)
def overload_dataframe_count(df, axis=0, level=None, numeric_only=False):
    check_runtime_cols_unsupported(df, 'DataFrame.count()')
    hwzb__jnck = dict(axis=axis, level=level, numeric_only=numeric_only)
    szrb__ldodx = dict(axis=0, level=None, numeric_only=False)
    check_unsupported_args('DataFrame.count', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
         for i in range(len(df.columns)))
    dvhz__hbzun = 'def impl(df, axis=0, level=None, numeric_only=False):\n'
    dvhz__hbzun += '  data = np.array([{}])\n'.format(data_args)
    gctc__qzcve = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    dvhz__hbzun += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {gctc__qzcve})\n'
        )
    unozl__xox = {}
    exec(dvhz__hbzun, {'bodo': bodo, 'np': np}, unozl__xox)
    impl = unozl__xox['impl']
    return impl


@overload_method(DataFrameType, 'nunique', inline='always', no_unliteral=True)
def overload_dataframe_nunique(df, axis=0, dropna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.unique()')
    hwzb__jnck = dict(axis=axis)
    szrb__ldodx = dict(axis=0)
    if not is_overload_bool(dropna):
        raise BodoError('DataFrame.nunique: dropna must be a boolean value')
    check_unsupported_args('DataFrame.nunique', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'bodo.libs.array_kernels.nunique(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), dropna)'
         for i in range(len(df.columns)))
    dvhz__hbzun = 'def impl(df, axis=0, dropna=True):\n'
    dvhz__hbzun += '  data = np.asarray(({},))\n'.format(data_args)
    gctc__qzcve = bodo.hiframes.dataframe_impl.generate_col_to_index_func_text(
        df.columns)
    dvhz__hbzun += (
        f'  return bodo.hiframes.pd_series_ext.init_series(data, {gctc__qzcve})\n'
        )
    unozl__xox = {}
    exec(dvhz__hbzun, {'bodo': bodo, 'np': np}, unozl__xox)
    impl = unozl__xox['impl']
    return impl


@overload_method(DataFrameType, 'prod', inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'product', inline='always', no_unliteral=True)
def overload_dataframe_prod(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.prod()')
    hwzb__jnck = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    szrb__ldodx = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.prod', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.product()')
    return _gen_reduce_impl(df, 'prod', axis=axis)


@overload_method(DataFrameType, 'sum', inline='always', no_unliteral=True)
def overload_dataframe_sum(df, axis=None, skipna=None, level=None,
    numeric_only=None, min_count=0):
    check_runtime_cols_unsupported(df, 'DataFrame.sum()')
    hwzb__jnck = dict(skipna=skipna, level=level, numeric_only=numeric_only,
        min_count=min_count)
    szrb__ldodx = dict(skipna=None, level=None, numeric_only=None, min_count=0)
    check_unsupported_args('DataFrame.sum', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sum()')
    return _gen_reduce_impl(df, 'sum', axis=axis)


@overload_method(DataFrameType, 'max', inline='always', no_unliteral=True)
def overload_dataframe_max(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.max()')
    hwzb__jnck = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    szrb__ldodx = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.max', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.max()')
    return _gen_reduce_impl(df, 'max', axis=axis)


@overload_method(DataFrameType, 'min', inline='always', no_unliteral=True)
def overload_dataframe_min(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.min()')
    hwzb__jnck = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    szrb__ldodx = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.min', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.min()')
    return _gen_reduce_impl(df, 'min', axis=axis)


@overload_method(DataFrameType, 'mean', inline='always', no_unliteral=True)
def overload_dataframe_mean(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.mean()')
    hwzb__jnck = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    szrb__ldodx = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.mean', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.mean()')
    return _gen_reduce_impl(df, 'mean', axis=axis)


@overload_method(DataFrameType, 'var', inline='always', no_unliteral=True)
def overload_dataframe_var(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.var()')
    hwzb__jnck = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    szrb__ldodx = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.var', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.var()')
    return _gen_reduce_impl(df, 'var', axis=axis)


@overload_method(DataFrameType, 'std', inline='always', no_unliteral=True)
def overload_dataframe_std(df, axis=None, skipna=None, level=None, ddof=1,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.std()')
    hwzb__jnck = dict(skipna=skipna, level=level, ddof=ddof, numeric_only=
        numeric_only)
    szrb__ldodx = dict(skipna=None, level=None, ddof=1, numeric_only=None)
    check_unsupported_args('DataFrame.std', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.std()')
    return _gen_reduce_impl(df, 'std', axis=axis)


@overload_method(DataFrameType, 'median', inline='always', no_unliteral=True)
def overload_dataframe_median(df, axis=None, skipna=None, level=None,
    numeric_only=None):
    check_runtime_cols_unsupported(df, 'DataFrame.median()')
    hwzb__jnck = dict(skipna=skipna, level=level, numeric_only=numeric_only)
    szrb__ldodx = dict(skipna=None, level=None, numeric_only=None)
    check_unsupported_args('DataFrame.median', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.median()')
    return _gen_reduce_impl(df, 'median', axis=axis)


@overload_method(DataFrameType, 'quantile', inline='always', no_unliteral=True)
def overload_dataframe_quantile(df, q=0.5, axis=0, numeric_only=True,
    interpolation='linear'):
    check_runtime_cols_unsupported(df, 'DataFrame.quantile()')
    hwzb__jnck = dict(numeric_only=numeric_only, interpolation=interpolation)
    szrb__ldodx = dict(numeric_only=True, interpolation='linear')
    check_unsupported_args('DataFrame.quantile', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.quantile()')
    return _gen_reduce_impl(df, 'quantile', 'q', axis=axis)


@overload_method(DataFrameType, 'idxmax', inline='always', no_unliteral=True)
def overload_dataframe_idxmax(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmax()')
    hwzb__jnck = dict(axis=axis, skipna=skipna)
    szrb__ldodx = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmax', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmax()')
    for hql__tfjnp in df.data:
        if not (bodo.utils.utils.is_np_array_typ(hql__tfjnp) and (
            hql__tfjnp.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(hql__tfjnp.dtype, (types.Number, types.Boolean))) or
            isinstance(hql__tfjnp, (bodo.IntegerArrayType, bodo.
            FloatingArrayType, bodo.CategoricalArrayType)) or hql__tfjnp in
            [bodo.boolean_array, bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmax() only supported for numeric column types. Column type: {hql__tfjnp} not supported.'
                )
        if isinstance(hql__tfjnp, bodo.CategoricalArrayType
            ) and not hql__tfjnp.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmax(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmax', axis=axis)


@overload_method(DataFrameType, 'idxmin', inline='always', no_unliteral=True)
def overload_dataframe_idxmin(df, axis=0, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.idxmin()')
    hwzb__jnck = dict(axis=axis, skipna=skipna)
    szrb__ldodx = dict(axis=0, skipna=True)
    check_unsupported_args('DataFrame.idxmin', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.idxmin()')
    for hql__tfjnp in df.data:
        if not (bodo.utils.utils.is_np_array_typ(hql__tfjnp) and (
            hql__tfjnp.dtype in [bodo.datetime64ns, bodo.timedelta64ns] or
            isinstance(hql__tfjnp.dtype, (types.Number, types.Boolean))) or
            isinstance(hql__tfjnp, (bodo.IntegerArrayType, bodo.
            FloatingArrayType, bodo.CategoricalArrayType)) or hql__tfjnp in
            [bodo.boolean_array, bodo.datetime_date_array_type]):
            raise BodoError(
                f'DataFrame.idxmin() only supported for numeric column types. Column type: {hql__tfjnp} not supported.'
                )
        if isinstance(hql__tfjnp, bodo.CategoricalArrayType
            ) and not hql__tfjnp.dtype.ordered:
            raise BodoError(
                'DataFrame.idxmin(): categorical columns must be ordered')
    return _gen_reduce_impl(df, 'idxmin', axis=axis)


@overload_method(DataFrameType, 'infer_objects', inline='always')
def overload_dataframe_infer_objects(df):
    check_runtime_cols_unsupported(df, 'DataFrame.infer_objects()')
    return lambda df: df.copy()


def _gen_reduce_impl(df, func_name, args=None, axis=None):
    args = '' if is_overload_none(args) else args
    if is_overload_none(axis):
        axis = 0
    elif is_overload_constant_int(axis):
        axis = get_overload_const_int(axis)
    else:
        raise_bodo_error(
            f'DataFrame.{func_name}: axis must be a constant Integer')
    assert axis in (0, 1), f'invalid axis argument for DataFrame.{func_name}'
    if func_name in ('idxmax', 'idxmin'):
        out_colnames = df.columns
    else:
        zmynk__yylt = tuple(ibfb__ifl for ibfb__ifl, uibz__fawu in zip(df.
            columns, df.data) if bodo.utils.typing._is_pandas_numeric_dtype
            (uibz__fawu.dtype))
        out_colnames = zmynk__yylt
    assert len(out_colnames) != 0
    try:
        if func_name in ('idxmax', 'idxmin') and axis == 0:
            comm_dtype = None
        else:
            fbd__sjtz = [numba.np.numpy_support.as_dtype(df.data[df.
                column_index[ibfb__ifl]].dtype) for ibfb__ifl in out_colnames]
            comm_dtype = numba.np.numpy_support.from_dtype(np.
                find_common_type(fbd__sjtz, []))
    except NotImplementedError as zbo__xhegc:
        raise BodoError(
            f'Dataframe.{func_name}() with column types: {df.data} could not be merged to a common type.'
            )
    wemo__xqu = ''
    if func_name in ('sum', 'prod'):
        wemo__xqu = ', min_count=0'
    ddof = ''
    if func_name in ('var', 'std'):
        ddof = 'ddof=1, '
    dvhz__hbzun = (
        'def impl(df, axis=None, skipna=None, level=None,{} numeric_only=None{}):\n'
        .format(ddof, wemo__xqu))
    if func_name == 'quantile':
        dvhz__hbzun = (
            "def impl(df, q=0.5, axis=0, numeric_only=True, interpolation='linear'):\n"
            )
    if func_name in ('idxmax', 'idxmin'):
        dvhz__hbzun = 'def impl(df, axis=0, skipna=True):\n'
    if axis == 0:
        dvhz__hbzun += _gen_reduce_impl_axis0(df, func_name, out_colnames,
            comm_dtype, args)
    else:
        dvhz__hbzun += _gen_reduce_impl_axis1(func_name, out_colnames,
            comm_dtype, df)
    unozl__xox = {}
    exec(dvhz__hbzun, {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba},
        unozl__xox)
    impl = unozl__xox['impl']
    return impl


def _gen_reduce_impl_axis0(df, func_name, out_colnames, comm_dtype, args):
    qmje__oiw = ''
    if func_name in ('min', 'max'):
        qmje__oiw = ', dtype=np.{}'.format(comm_dtype)
    if comm_dtype == types.float32 and func_name in ('sum', 'prod', 'mean',
        'var', 'std', 'median'):
        qmje__oiw = ', dtype=np.float32'
    yqawb__awj = f'bodo.libs.array_ops.array_op_{func_name}'
    wsvds__fwm = ''
    if func_name in ['sum', 'prod']:
        wsvds__fwm = 'True, min_count'
    elif func_name in ['idxmax', 'idxmin']:
        wsvds__fwm = 'index'
    elif func_name == 'quantile':
        wsvds__fwm = 'q'
    elif func_name in ['std', 'var']:
        wsvds__fwm = 'True, ddof'
    elif func_name == 'median':
        wsvds__fwm = 'True'
    data_args = ', '.join(
        f'{yqawb__awj}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[ibfb__ifl]}), {wsvds__fwm})'
         for ibfb__ifl in out_colnames)
    dvhz__hbzun = ''
    if func_name in ('idxmax', 'idxmin'):
        dvhz__hbzun += (
            '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        dvhz__hbzun += (
            '  data = bodo.utils.conversion.coerce_to_array(({},))\n'.
            format(data_args))
    else:
        dvhz__hbzun += '  data = np.asarray(({},){})\n'.format(data_args,
            qmje__oiw)
    dvhz__hbzun += f"""  return bodo.hiframes.pd_series_ext.init_series(data, pd.Index({out_colnames}))
"""
    return dvhz__hbzun


def _gen_reduce_impl_axis1(func_name, out_colnames, comm_dtype, df_type):
    xiro__gzz = [df_type.column_index[ibfb__ifl] for ibfb__ifl in out_colnames]
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    data_args = '\n    '.join(
        'arr_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
        .format(i) for i in xiro__gzz)
    ixdtc__qds = '\n        '.join(f'row[{i}] = arr_{xiro__gzz[i]}[i]' for
        i in range(len(out_colnames)))
    assert len(data_args) > 0, f'empty dataframe in DataFrame.{func_name}()'
    gva__dbs = f'len(arr_{xiro__gzz[0]})'
    vgwn__umofq = {'max': 'np.nanmax', 'min': 'np.nanmin', 'sum':
        'np.nansum', 'prod': 'np.nanprod', 'mean': 'np.nanmean', 'median':
        'np.nanmedian', 'var': 'bodo.utils.utils.nanvar_ddof1', 'std':
        'bodo.utils.utils.nanstd_ddof1'}
    if func_name in vgwn__umofq:
        beh__shn = vgwn__umofq[func_name]
        gtljt__fpd = 'float64' if func_name in ['mean', 'median', 'std', 'var'
            ] else comm_dtype
        dvhz__hbzun = f"""
    {data_args}
    numba.parfors.parfor.init_prange()
    n = {gva__dbs}
    row = np.empty({len(out_colnames)}, np.{comm_dtype})
    A = np.empty(n, np.{gtljt__fpd})
    for i in numba.parfors.parfor.internal_prange(n):
        {ixdtc__qds}
        A[i] = {beh__shn}(row)
    return bodo.hiframes.pd_series_ext.init_series(A, {index})
"""
        return dvhz__hbzun
    else:
        raise BodoError(f'DataFrame.{func_name}(): Not supported for axis=1')


@overload_method(DataFrameType, 'pct_change', inline='always', no_unliteral
    =True)
def overload_dataframe_pct_change(df, periods=1, fill_method='pad', limit=
    None, freq=None):
    check_runtime_cols_unsupported(df, 'DataFrame.pct_change()')
    hwzb__jnck = dict(fill_method=fill_method, limit=limit, freq=freq)
    szrb__ldodx = dict(fill_method='pad', limit=None, freq=None)
    check_unsupported_args('DataFrame.pct_change', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.pct_change()')
    data_args = ', '.join(
        f'bodo.hiframes.rolling.pct_change(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False)'
         for i in range(len(df.columns)))
    header = (
        "def impl(df, periods=1, fill_method='pad', limit=None, freq=None):\n")
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumprod', inline='always', no_unliteral=True)
def overload_dataframe_cumprod(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumprod()')
    hwzb__jnck = dict(axis=axis, skipna=skipna)
    szrb__ldodx = dict(axis=None, skipna=True)
    check_unsupported_args('DataFrame.cumprod', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.cumprod()')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumprod()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'cumsum', inline='always', no_unliteral=True)
def overload_dataframe_cumsum(df, axis=None, skipna=True):
    check_runtime_cols_unsupported(df, 'DataFrame.cumsum()')
    hwzb__jnck = dict(skipna=skipna)
    szrb__ldodx = dict(skipna=True)
    check_unsupported_args('DataFrame.cumsum', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.cumsum()')
    data_args = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).cumsum()'
         for i in range(len(df.columns)))
    header = 'def impl(df, axis=None, skipna=True):\n'
    return _gen_init_df(header, df.columns, data_args)


def _is_describe_type(data):
    return isinstance(data, (IntegerArrayType, FloatingArrayType)
        ) or isinstance(data, types.Array) and isinstance(data.dtype, types
        .Number) or data.dtype == bodo.datetime64ns


@overload_method(DataFrameType, 'describe', inline='always', no_unliteral=True)
def overload_dataframe_describe(df, percentiles=None, include=None, exclude
    =None, datetime_is_numeric=True):
    check_runtime_cols_unsupported(df, 'DataFrame.describe()')
    hwzb__jnck = dict(percentiles=percentiles, include=include, exclude=
        exclude, datetime_is_numeric=datetime_is_numeric)
    szrb__ldodx = dict(percentiles=None, include=None, exclude=None,
        datetime_is_numeric=True)
    check_unsupported_args('DataFrame.describe', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.describe()')
    zmynk__yylt = [ibfb__ifl for ibfb__ifl, uibz__fawu in zip(df.columns,
        df.data) if _is_describe_type(uibz__fawu)]
    if len(zmynk__yylt) == 0:
        raise BodoError('df.describe() only supports numeric columns')
    ltdk__vdnw = sum(df.data[df.column_index[ibfb__ifl]].dtype == bodo.
        datetime64ns for ibfb__ifl in zmynk__yylt)

    def _get_describe(col_ind):
        qrkpg__jzula = df.data[col_ind].dtype == bodo.datetime64ns
        if ltdk__vdnw and ltdk__vdnw != len(zmynk__yylt):
            if qrkpg__jzula:
                return f'des_{col_ind} + (np.nan,)'
            return (
                f'des_{col_ind}[:2] + des_{col_ind}[3:] + (des_{col_ind}[2],)')
        return f'des_{col_ind}'
    header = """def impl(df, percentiles=None, include=None, exclude=None, datetime_is_numeric=True):
"""
    for ibfb__ifl in zmynk__yylt:
        col_ind = df.column_index[ibfb__ifl]
        header += f"""  des_{col_ind} = bodo.libs.array_ops.array_op_describe(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {col_ind}))
"""
    data_args = ', '.join(_get_describe(df.column_index[ibfb__ifl]) for
        ibfb__ifl in zmynk__yylt)
    jln__law = "['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']"
    if ltdk__vdnw == len(zmynk__yylt):
        jln__law = "['count', 'mean', 'min', '25%', '50%', '75%', 'max']"
    elif ltdk__vdnw:
        jln__law = (
            "['count', 'mean', 'min', '25%', '50%', '75%', 'max', 'std']")
    index = f'bodo.utils.conversion.convert_to_index({jln__law})'
    return _gen_init_df(header, zmynk__yylt, data_args, index)


@overload_method(DataFrameType, 'take', inline='always', no_unliteral=True)
def overload_dataframe_take(df, indices, axis=0, convert=None, is_copy=True):
    check_runtime_cols_unsupported(df, 'DataFrame.take()')
    hwzb__jnck = dict(axis=axis, convert=convert, is_copy=is_copy)
    szrb__ldodx = dict(axis=0, convert=None, is_copy=True)
    check_unsupported_args('DataFrame.take', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})[indices_t]'
        .format(i) for i in range(len(df.columns)))
    header = 'def impl(df, indices, axis=0, convert=None, is_copy=True):\n'
    header += (
        '  indices_t = bodo.utils.conversion.coerce_to_ndarray(indices)\n')
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[indices_t]'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'shift', inline='always', no_unliteral=True)
def overload_dataframe_shift(df, periods=1, freq=None, axis=0, fill_value=None
    ):
    check_runtime_cols_unsupported(df, 'DataFrame.shift()')
    hwzb__jnck = dict(freq=freq, axis=axis)
    szrb__ldodx = dict(freq=None, axis=0)
    check_unsupported_args('DataFrame.shift', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.shift()')
    for jpms__zkqjv in df.data:
        if not is_supported_shift_array_type(jpms__zkqjv):
            raise BodoError(
                f'Dataframe.shift() column input type {jpms__zkqjv.dtype} not supported yet.'
                )
    if not is_overload_int(periods):
        raise BodoError(
            "DataFrame.shift(): 'periods' input must be an integer.")
    data_args = ', '.join(
        f'bodo.hiframes.rolling.shift(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), periods, False, fill_value)'
         for i in range(len(df.columns)))
    header = 'def impl(df, periods=1, freq=None, axis=0, fill_value=None):\n'
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'diff', inline='always', no_unliteral=True)
def overload_dataframe_diff(df, periods=1, axis=0):
    check_runtime_cols_unsupported(df, 'DataFrame.diff()')
    hwzb__jnck = dict(axis=axis)
    szrb__ldodx = dict(axis=0)
    check_unsupported_args('DataFrame.diff', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.diff()')
    for jpms__zkqjv in df.data:
        if not (isinstance(jpms__zkqjv, types.Array) and (isinstance(
            jpms__zkqjv.dtype, types.Number) or jpms__zkqjv.dtype == bodo.
            datetime64ns)):
            raise BodoError(
                f'DataFrame.diff() column input type {jpms__zkqjv.dtype} not supported.'
                )
    if not is_overload_int(periods):
        raise BodoError("DataFrame.diff(): 'periods' input must be an integer."
            )
    header = 'def impl(df, periods=1, axis= 0):\n'
    for i in range(len(df.columns)):
        header += (
            f'  data_{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    data_args = ', '.join(
        f'bodo.hiframes.series_impl.dt64_arr_sub(data_{i}, bodo.hiframes.rolling.shift(data_{i}, periods, False))'
         if df.data[i] == types.Array(bodo.datetime64ns, 1, 'C') else
        f'data_{i} - bodo.hiframes.rolling.shift(data_{i}, periods, False)' for
        i in range(len(df.columns)))
    return _gen_init_df(header, df.columns, data_args)


@overload_method(DataFrameType, 'explode', inline='always', no_unliteral=True)
def overload_dataframe_explode(df, column, ignore_index=False):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.explode()')
    xosbs__ngs = (
        "DataFrame.explode(): 'column' must a constant label or list of labels"
        )
    if not is_literal_type(column):
        raise_bodo_error(xosbs__ngs)
    if is_overload_constant_list(column) or is_overload_constant_tuple(column):
        pfh__esug = get_overload_const_list(column)
    else:
        pfh__esug = [get_literal_value(column)]
    csu__pchee = [df.column_index[ibfb__ifl] for ibfb__ifl in pfh__esug]
    for i in csu__pchee:
        if not isinstance(df.data[i], ArrayItemArrayType) and df.data[i
            ].dtype != string_array_split_view_type:
            raise BodoError(
                f'DataFrame.explode(): columns must have array-like entries')
    n = len(df.columns)
    header = 'def impl(df, column, ignore_index=False):\n'
    header += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    header += '  index_arr = bodo.utils.conversion.index_to_array(index)\n'
    for i in range(n):
        header += (
            f'  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    header += (
        f'  counts = bodo.libs.array_kernels.get_arr_lens(data{csu__pchee[0]})\n'
        )
    for i in range(n):
        if i in csu__pchee:
            header += (
                f'  out_data{i} = bodo.libs.array_kernels.explode_no_index(data{i}, counts)\n'
                )
        else:
            header += (
                f'  out_data{i} = bodo.libs.array_kernels.repeat_kernel(data{i}, counts)\n'
                )
    header += (
        '  new_index = bodo.libs.array_kernels.repeat_kernel(index_arr, counts)\n'
        )
    data_args = ', '.join(f'out_data{i}' for i in range(n))
    index = 'bodo.utils.conversion.convert_to_index(new_index)'
    return _gen_init_df(header, df.columns, data_args, index)


@overload_method(DataFrameType, 'set_index', inline='always', no_unliteral=True
    )
def overload_dataframe_set_index(df, keys, drop=True, append=False, inplace
    =False, verify_integrity=False):
    check_runtime_cols_unsupported(df, 'DataFrame.set_index()')
    zzfx__trn = {'inplace': inplace, 'append': append, 'verify_integrity':
        verify_integrity}
    nwf__nku = {'inplace': False, 'append': False, 'verify_integrity': False}
    check_unsupported_args('DataFrame.set_index', zzfx__trn, nwf__nku,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_constant_str(keys):
        raise_bodo_error(
            "DataFrame.set_index(): 'keys' must be a constant string")
    col_name = get_overload_const_str(keys)
    col_ind = df.columns.index(col_name)
    header = """def impl(df, keys, drop=True, append=False, inplace=False, verify_integrity=False):
"""
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'.format(
        i) for i in range(len(df.columns)) if i != col_ind)
    columns = tuple(ibfb__ifl for ibfb__ifl in df.columns if ibfb__ifl !=
        col_name)
    index = (
        'bodo.utils.conversion.index_from_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}), {})'
        .format(col_ind, f"'{col_name}'" if isinstance(col_name, str) else
        col_name))
    return _gen_init_df(header, columns, data_args, index)


@overload_method(DataFrameType, 'query', no_unliteral=True)
def overload_dataframe_query(df, expr, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.query()')
    zzfx__trn = {'inplace': inplace}
    nwf__nku = {'inplace': False}
    check_unsupported_args('query', zzfx__trn, nwf__nku, package_name=
        'pandas', module_name='DataFrame')
    if not isinstance(expr, (types.StringLiteral, types.UnicodeType)):
        raise BodoError('query(): expr argument should be a string')

    def impl(df, expr, inplace=False):
        nfyyb__nxfq = bodo.hiframes.pd_dataframe_ext.query_dummy(df, expr)
        return df[nfyyb__nxfq]
    return impl


@overload_method(DataFrameType, 'duplicated', inline='always', no_unliteral
    =True)
def overload_dataframe_duplicated(df, subset=None, keep='first'):
    check_runtime_cols_unsupported(df, 'DataFrame.duplicated()')
    zzfx__trn = {'subset': subset, 'keep': keep}
    nwf__nku = {'subset': None, 'keep': 'first'}
    check_unsupported_args('DataFrame.duplicated', zzfx__trn, nwf__nku,
        package_name='pandas', module_name='DataFrame')
    zlzx__dvfjm = len(df.columns)
    dvhz__hbzun = "def impl(df, subset=None, keep='first'):\n"
    for i in range(zlzx__dvfjm):
        dvhz__hbzun += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    ykteb__icg = ', '.join(f'data_{i}' for i in range(zlzx__dvfjm))
    ykteb__icg += ',' if zlzx__dvfjm == 1 else ''
    dvhz__hbzun += (
        f'  duplicated = bodo.libs.array_kernels.duplicated(({ykteb__icg}))\n')
    dvhz__hbzun += (
        '  index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n')
    dvhz__hbzun += (
        '  return bodo.hiframes.pd_series_ext.init_series(duplicated, index)\n'
        )
    unozl__xox = {}
    exec(dvhz__hbzun, {'bodo': bodo}, unozl__xox)
    impl = unozl__xox['impl']
    return impl


@overload_method(DataFrameType, 'drop_duplicates', inline='always',
    no_unliteral=True)
def overload_dataframe_drop_duplicates(df, subset=None, keep='first',
    inplace=False, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop_duplicates()')
    zzfx__trn = {'keep': keep, 'inplace': inplace, 'ignore_index': ignore_index
        }
    nwf__nku = {'keep': 'first', 'inplace': False, 'ignore_index': False}
    zcrlv__cfti = []
    if is_overload_constant_list(subset):
        zcrlv__cfti = get_overload_const_list(subset)
    elif is_overload_constant_str(subset):
        zcrlv__cfti = [get_overload_const_str(subset)]
    elif is_overload_constant_int(subset):
        zcrlv__cfti = [get_overload_const_int(subset)]
    elif not is_overload_none(subset):
        raise_bodo_error(
            'DataFrame.drop_duplicates(): subset must be a constant column name, constant list of column names or None'
            )
    vghk__nfsp = []
    for col_name in zcrlv__cfti:
        if col_name not in df.column_index:
            raise BodoError(
                'DataFrame.drop_duplicates(): All subset columns must be found in the DataFrame.'
                 +
                f'Column {col_name} not found in DataFrame columns {df.columns}'
                )
        vghk__nfsp.append(df.column_index[col_name])
    check_unsupported_args('DataFrame.drop_duplicates', zzfx__trn, nwf__nku,
        package_name='pandas', module_name='DataFrame')
    dmxj__khwr = []
    if vghk__nfsp:
        for boqi__fvt in vghk__nfsp:
            if isinstance(df.data[boqi__fvt], bodo.MapArrayType):
                dmxj__khwr.append(df.columns[boqi__fvt])
    else:
        for i, col_name in enumerate(df.columns):
            if isinstance(df.data[i], bodo.MapArrayType):
                dmxj__khwr.append(col_name)
    if dmxj__khwr:
        raise BodoError(
            f'DataFrame.drop_duplicates(): Columns {dmxj__khwr} ' +
            f'have dictionary types which cannot be used to drop duplicates. '
             +
            "Please consider using the 'subset' argument to skip these columns."
            )
    zlzx__dvfjm = len(df.columns)
    htm__mbihp = ['data_{}'.format(i) for i in vghk__nfsp]
    chx__dttn = ['data_{}'.format(i) for i in range(zlzx__dvfjm) if i not in
        vghk__nfsp]
    if htm__mbihp:
        bmf__hurya = len(htm__mbihp)
    else:
        bmf__hurya = zlzx__dvfjm
    ktr__wye = ', '.join(htm__mbihp + chx__dttn)
    data_args = ', '.join('data_{}'.format(i) for i in range(zlzx__dvfjm))
    dvhz__hbzun = (
        "def impl(df, subset=None, keep='first', inplace=False, ignore_index=False):\n"
        )
    for i in range(zlzx__dvfjm):
        dvhz__hbzun += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    dvhz__hbzun += (
        """  ({0},), index_arr = bodo.libs.array_kernels.drop_duplicates(({0},), {1}, {2})
"""
        .format(ktr__wye, index, bmf__hurya))
    dvhz__hbzun += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(dvhz__hbzun, df.columns, data_args, 'index')


def create_dataframe_mask_where_overload(func_name):

    def overload_dataframe_mask_where(df, cond, other=np.nan, inplace=False,
        axis=None, level=None, errors='raise', try_cast=False):
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
            f'DataFrame.{func_name}()')
        _validate_arguments_mask_where(f'DataFrame.{func_name}', df, cond,
            other, inplace, axis, level, errors, try_cast)
        header = """def impl(df, cond, other=np.nan, inplace=False, axis=None, level=None, errors='raise', try_cast=False):
"""
        if func_name == 'mask':
            header += '  cond = ~cond\n'
        gen_all_false = [False]
        if cond.ndim == 1:
            cond_str = lambda i, _: 'cond'
        elif cond.ndim == 2:
            if isinstance(cond, DataFrameType):

                def cond_str(i, gen_all_false):
                    if df.columns[i] in cond.column_index:
                        return (
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(cond, {cond.column_index[df.columns[i]]})'
                            )
                    else:
                        gen_all_false[0] = True
                        return 'all_false'
            elif isinstance(cond, types.Array):
                cond_str = lambda i, _: f'cond[:,{i}]'
        if not hasattr(other, 'ndim') or other.ndim == 1:
            oua__vmf = lambda i: 'other'
        elif other.ndim == 2:
            if isinstance(other, DataFrameType):
                oua__vmf = (lambda i: 
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {other.column_index[df.columns[i]]})'
                     if df.columns[i] in other.column_index else 'None')
            elif isinstance(other, types.Array):
                oua__vmf = lambda i: f'other[:,{i}]'
        zlzx__dvfjm = len(df.columns)
        data_args = ', '.join(
            f'bodo.hiframes.series_impl.where_impl({cond_str(i, gen_all_false)}, bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}), {oua__vmf(i)})'
             for i in range(zlzx__dvfjm))
        if gen_all_false[0]:
            header += '  all_false = np.zeros(len(df), dtype=bool)\n'
        return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_mask_where


def _install_dataframe_mask_where_overload():
    for func_name in ('mask', 'where'):
        eia__kad = create_dataframe_mask_where_overload(func_name)
        overload_method(DataFrameType, func_name, no_unliteral=True)(eia__kad)


_install_dataframe_mask_where_overload()


def _validate_arguments_mask_where(func_name, df, cond, other, inplace,
    axis, level, errors, try_cast):
    hwzb__jnck = dict(inplace=inplace, level=level, errors=errors, try_cast
        =try_cast)
    szrb__ldodx = dict(inplace=False, level=None, errors='raise', try_cast=
        False)
    check_unsupported_args(f'{func_name}', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise_bodo_error(f'{func_name}(): axis argument not supported')
    if not (isinstance(cond, (SeriesType, types.Array, BooleanArrayType)) and
        (cond.ndim == 1 or cond.ndim == 2) and cond.dtype == types.bool_
        ) and not (isinstance(cond, DataFrameType) and cond.ndim == 2 and
        all(cond.data[i].dtype == types.bool_ for i in range(len(df.columns)))
        ):
        raise BodoError(
            f"{func_name}(): 'cond' argument must be a DataFrame, Series, 1- or 2-dimensional array of booleans"
            )
    zlzx__dvfjm = len(df.columns)
    if hasattr(other, 'ndim') and (other.ndim != 1 or other.ndim != 2):
        if other.ndim == 2:
            if not isinstance(other, (DataFrameType, types.Array)):
                raise BodoError(
                    f"{func_name}(): 'other', if 2-dimensional, must be a DataFrame or array."
                    )
        elif other.ndim != 1:
            raise BodoError(
                f"{func_name}(): 'other' must be either 1 or 2-dimensional")
    if isinstance(other, DataFrameType):
        for i in range(zlzx__dvfjm):
            if df.columns[i] in other.column_index:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, 'Series', df.data[i], other.data[other.
                    column_index[df.columns[i]]])
            else:
                bodo.hiframes.series_impl._validate_self_other_mask_where(
                    func_name, 'Series', df.data[i], None, is_default=True)
    elif isinstance(other, SeriesType):
        for i in range(zlzx__dvfjm):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , 'Series', df.data[i], other.data)
    else:
        for i in range(zlzx__dvfjm):
            bodo.hiframes.series_impl._validate_self_other_mask_where(func_name
                , 'Series', df.data[i], other, max_ndim=2)


def _gen_init_df(header, columns, data_args, index=None, extra_globals=None):
    if index is None:
        index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    if extra_globals is None:
        extra_globals = {}
    whoqj__ssgil = ColNamesMetaType(tuple(columns))
    data_args = '({}{})'.format(data_args, ',' if data_args else '')
    dvhz__hbzun = f"""{header}  return bodo.hiframes.pd_dataframe_ext.init_dataframe({data_args}, {index}, __col_name_meta_value_gen_init_df)
"""
    unozl__xox = {}
    vzx__ufk = {'bodo': bodo, 'np': np, 'pd': pd, 'numba': numba,
        '__col_name_meta_value_gen_init_df': whoqj__ssgil}
    vzx__ufk.update(extra_globals)
    exec(dvhz__hbzun, vzx__ufk, unozl__xox)
    impl = unozl__xox['impl']
    return impl


def _get_binop_columns(lhs, rhs, is_inplace=False):
    if lhs.columns != rhs.columns:
        sgh__mgdgv = pd.Index(lhs.columns)
        airv__osf = pd.Index(rhs.columns)
        hstam__rpsc, dqv__jonrd, ypkv__djhg = sgh__mgdgv.join(airv__osf,
            how='left' if is_inplace else 'outer', level=None,
            return_indexers=True)
        return tuple(hstam__rpsc), dqv__jonrd, ypkv__djhg
    return lhs.columns, range(len(lhs.columns)), range(len(lhs.columns))


def create_binary_op_overload(op):

    def overload_dataframe_binary_op(lhs, rhs):
        znj__psnr = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        iqvhj__zacwq = operator.eq, operator.ne
        check_runtime_cols_unsupported(lhs, znj__psnr)
        check_runtime_cols_unsupported(rhs, znj__psnr)
        if isinstance(lhs, DataFrameType):
            if isinstance(rhs, DataFrameType):
                hstam__rpsc, dqv__jonrd, ypkv__djhg = _get_binop_columns(lhs,
                    rhs)
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {jmn__dba}) {znj__psnr}bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {yybj__zwtg})'
                     if jmn__dba != -1 and yybj__zwtg != -1 else
                    f'bodo.libs.array_kernels.gen_na_array(len(lhs), float64_arr_type)'
                     for jmn__dba, yybj__zwtg in zip(dqv__jonrd, ypkv__djhg))
                header = 'def impl(lhs, rhs):\n'
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)')
                return _gen_init_df(header, hstam__rpsc, data_args, index,
                    extra_globals={'float64_arr_type': types.Array(types.
                    float64, 1, 'C')})
            elif isinstance(rhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            vkhgx__qcqp = []
            czrf__ettfj = []
            if op in iqvhj__zacwq:
                for i, mtkif__qzfuw in enumerate(lhs.data):
                    if is_common_scalar_dtype([mtkif__qzfuw.dtype, rhs]):
                        vkhgx__qcqp.append(
                            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {znj__psnr} rhs'
                            )
                    else:
                        rbrc__txtzf = f'arr{i}'
                        czrf__ettfj.append(rbrc__txtzf)
                        vkhgx__qcqp.append(rbrc__txtzf)
                data_args = ', '.join(vkhgx__qcqp)
            else:
                data_args = ', '.join(
                    f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(lhs, {i}) {znj__psnr} rhs'
                     for i in range(len(lhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(czrf__ettfj) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(lhs)\n'
                header += ''.join(
                    f'  {rbrc__txtzf} = np.empty(n, dtype=np.bool_)\n' for
                    rbrc__txtzf in czrf__ettfj)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(rbrc__txtzf, 
                    op == operator.ne) for rbrc__txtzf in czrf__ettfj)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(lhs)'
            return _gen_init_df(header, lhs.columns, data_args, index)
        if isinstance(rhs, DataFrameType):
            if isinstance(lhs, SeriesType):
                raise_bodo_error(
                    'Comparison operation between Dataframe and Series is not supported yet.'
                    )
            vkhgx__qcqp = []
            czrf__ettfj = []
            if op in iqvhj__zacwq:
                for i, mtkif__qzfuw in enumerate(rhs.data):
                    if is_common_scalar_dtype([lhs, mtkif__qzfuw.dtype]):
                        vkhgx__qcqp.append(
                            f'lhs {znj__psnr} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {i})'
                            )
                    else:
                        rbrc__txtzf = f'arr{i}'
                        czrf__ettfj.append(rbrc__txtzf)
                        vkhgx__qcqp.append(rbrc__txtzf)
                data_args = ', '.join(vkhgx__qcqp)
            else:
                data_args = ', '.join(
                    'lhs {1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(rhs, {0})'
                    .format(i, znj__psnr) for i in range(len(rhs.columns)))
            header = 'def impl(lhs, rhs):\n'
            if len(czrf__ettfj) > 0:
                header += '  numba.parfors.parfor.init_prange()\n'
                header += '  n = len(rhs)\n'
                header += ''.join('  {0} = np.empty(n, dtype=np.bool_)\n'.
                    format(rbrc__txtzf) for rbrc__txtzf in czrf__ettfj)
                header += (
                    '  for i in numba.parfors.parfor.internal_prange(n):\n')
                header += ''.join('    {0}[i] = {1}\n'.format(rbrc__txtzf, 
                    op == operator.ne) for rbrc__txtzf in czrf__ettfj)
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(rhs)'
            return _gen_init_df(header, rhs.columns, data_args, index)
    return overload_dataframe_binary_op


skips = [operator.lt, operator.le, operator.eq, operator.ne, operator.gt,
    operator.ge, operator.add, operator.sub, operator.mul, operator.truediv,
    operator.floordiv, operator.pow, operator.mod]


def _install_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_binary_ops:
        if op in skips:
            continue
        eia__kad = create_binary_op_overload(op)
        overload(op)(eia__kad)


_install_binary_ops()


def create_inplace_binary_op_overload(op):

    def overload_dataframe_inplace_binary_op(left, right):
        znj__psnr = numba.core.utils.OPERATORS_TO_BUILTINS[op]
        check_runtime_cols_unsupported(left, znj__psnr)
        check_runtime_cols_unsupported(right, znj__psnr)
        if isinstance(left, DataFrameType):
            if isinstance(right, DataFrameType):
                hstam__rpsc, _, ypkv__djhg = _get_binop_columns(left, right,
                    True)
                dvhz__hbzun = 'def impl(left, right):\n'
                for i, yybj__zwtg in enumerate(ypkv__djhg):
                    if yybj__zwtg == -1:
                        dvhz__hbzun += f"""  df_arr{i} = bodo.libs.array_kernels.gen_na_array(len(left), float64_arr_type)
"""
                        continue
                    dvhz__hbzun += f"""  df_arr{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {i})
"""
                    dvhz__hbzun += f"""  df_arr{i} {znj__psnr} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(right, {yybj__zwtg})
"""
                data_args = ', '.join(f'df_arr{i}' for i in range(len(
                    hstam__rpsc)))
                index = (
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)')
                return _gen_init_df(dvhz__hbzun, hstam__rpsc, data_args,
                    index, extra_globals={'float64_arr_type': types.Array(
                    types.float64, 1, 'C')})
            dvhz__hbzun = 'def impl(left, right):\n'
            for i in range(len(left.columns)):
                dvhz__hbzun += (
                    """  df_arr{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(left, {0})
"""
                    .format(i))
                dvhz__hbzun += '  df_arr{0} {1} right\n'.format(i, znj__psnr)
            data_args = ', '.join('df_arr{}'.format(i) for i in range(len(
                left.columns)))
            index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(left)'
            return _gen_init_df(dvhz__hbzun, left.columns, data_args, index)
    return overload_dataframe_inplace_binary_op


def _install_inplace_binary_ops():
    for op in bodo.hiframes.pd_series_ext.series_inplace_binary_ops:
        eia__kad = create_inplace_binary_op_overload(op)
        overload(op, no_unliteral=True)(eia__kad)


_install_inplace_binary_ops()


def create_unary_op_overload(op):

    def overload_dataframe_unary_op(df):
        if isinstance(df, DataFrameType):
            znj__psnr = numba.core.utils.OPERATORS_TO_BUILTINS[op]
            check_runtime_cols_unsupported(df, znj__psnr)
            data_args = ', '.join(
                '{1} bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})'
                .format(i, znj__psnr) for i in range(len(df.columns)))
            header = 'def impl(df):\n'
            return _gen_init_df(header, df.columns, data_args)
    return overload_dataframe_unary_op


def _install_unary_ops():
    for op in bodo.hiframes.pd_series_ext.series_unary_ops:
        eia__kad = create_unary_op_overload(op)
        overload(op, no_unliteral=True)(eia__kad)


_install_unary_ops()


def overload_isna(obj):
    check_runtime_cols_unsupported(obj, 'pd.isna()')
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj):
        return lambda obj: obj.isna()
    if is_array_typ(obj):

        def impl(obj):
            numba.parfors.parfor.init_prange()
            n = len(obj)
            tdyd__viq = np.empty(n, np.bool_)
            for i in numba.parfors.parfor.internal_prange(n):
                tdyd__viq[i] = bodo.libs.array_kernels.isna(obj, i)
            return tdyd__viq
        return impl


overload(pd.isna, inline='always')(overload_isna)
overload(pd.isnull, inline='always')(overload_isna)


@overload(pd.isna)
@overload(pd.isnull)
def overload_isna_scalar(obj):
    if isinstance(obj, (DataFrameType, SeriesType)
        ) or bodo.hiframes.pd_index_ext.is_pd_index_type(obj) or is_array_typ(
        obj):
        return
    if isinstance(obj, (types.List, types.UniTuple)):

        def impl(obj):
            n = len(obj)
            tdyd__viq = np.empty(n, np.bool_)
            for i in range(n):
                tdyd__viq[i] = pd.isna(obj[i])
            return tdyd__viq
        return impl
    obj = types.unliteral(obj)
    if obj == bodo.string_type:
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Integer):
        return lambda obj: unliteral_val(False)
    if isinstance(obj, types.Float):
        return lambda obj: np.isnan(obj)
    if isinstance(obj, (types.NPDatetime, types.NPTimedelta)):
        return lambda obj: np.isnat(obj)
    if obj == types.none:
        return lambda obj: unliteral_val(True)
    if isinstance(obj, bodo.hiframes.pd_timestamp_ext.PandasTimestampType):
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_dt64(obj.value))
    if obj == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        return lambda obj: np.isnat(bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(obj.value))
    if isinstance(obj, types.Optional):
        return lambda obj: obj is None
    return lambda obj: unliteral_val(False)


@overload(operator.setitem, no_unliteral=True)
def overload_setitem_arr_none(A, idx, val):
    if is_array_typ(A, False) and isinstance(idx, types.Integer
        ) and val == types.none:
        return lambda A, idx, val: bodo.libs.array_kernels.setna(A, idx)


def overload_notna(obj):
    check_runtime_cols_unsupported(obj, 'pd.notna()')
    if isinstance(obj, (DataFrameType, SeriesType)):
        return lambda obj: obj.notna()
    if isinstance(obj, (types.List, types.UniTuple)) or is_array_typ(obj,
        include_index_series=True):
        return lambda obj: ~pd.isna(obj)
    return lambda obj: not pd.isna(obj)


overload(pd.notna, inline='always', no_unliteral=True)(overload_notna)
overload(pd.notnull, inline='always', no_unliteral=True)(overload_notna)


def _get_pd_dtype_str(t):
    if t.dtype == types.NPDatetime('ns'):
        return "'datetime64[ns]'"
    return bodo.ir.csv_ext._get_pd_dtype_str(t)


@overload_method(DataFrameType, 'replace', inline='always', no_unliteral=True)
def overload_dataframe_replace(df, to_replace=None, value=None, inplace=
    False, limit=None, regex=False, method='pad'):
    check_runtime_cols_unsupported(df, 'DataFrame.replace()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.replace()')
    if is_overload_none(to_replace):
        raise BodoError('replace(): to_replace value of None is not supported')
    zzfx__trn = {'inplace': inplace, 'limit': limit, 'regex': regex,
        'method': method}
    nwf__nku = {'inplace': False, 'limit': None, 'regex': False, 'method':
        'pad'}
    check_unsupported_args('replace', zzfx__trn, nwf__nku, package_name=
        'pandas', module_name='DataFrame')
    data_args = ', '.join(
        f'df.iloc[:, {i}].replace(to_replace, value).values' for i in range
        (len(df.columns)))
    header = """def impl(df, to_replace=None, value=None, inplace=False, limit=None, regex=False, method='pad'):
"""
    return _gen_init_df(header, df.columns, data_args)


def _is_col_access(expr_node):
    bpbvl__dyby = str(expr_node)
    return bpbvl__dyby.startswith('(left.') or bpbvl__dyby.startswith('(right.'
        )


def _insert_NA_cond(expr_node, left_columns, left_data, right_columns,
    right_data):
    zvuwg__kww = {'left': 0, 'right': 0, 'NOT_NA': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (zvuwg__kww,))
    vyt__zyg = pd.core.computation.parsing.clean_column_name

    def append_null_checks(expr_node, null_set):
        if not null_set:
            return expr_node
        ajp__wlpgi = ' & '.join([('NOT_NA.`' + x + '`') for x in null_set])
        acvhm__swg = {('NOT_NA', vyt__zyg(mtkif__qzfuw)): mtkif__qzfuw for
            mtkif__qzfuw in null_set}
        xoy__qfqx, _, _ = _parse_query_expr(ajp__wlpgi, env, [], [], None,
            join_cleaned_cols=acvhm__swg)
        bzp__urqav = (pd.core.computation.ops.BinOp.
            _disallow_scalar_only_bool_ops)
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        try:
            hhs__wkobb = pd.core.computation.ops.BinOp('&', xoy__qfqx,
                expr_node)
        finally:
            (pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
                ) = bzp__urqav
        return hhs__wkobb

    def _insert_NA_cond_body(expr_node, null_set):
        if isinstance(expr_node, pd.core.computation.ops.BinOp):
            if expr_node.op == '|':
                nzpa__kaqeo = set()
                smgqp__umsj = set()
                dwwpz__grk = _insert_NA_cond_body(expr_node.lhs, nzpa__kaqeo)
                hfj__eaw = _insert_NA_cond_body(expr_node.rhs, smgqp__umsj)
                hqpx__yhe = nzpa__kaqeo.intersection(smgqp__umsj)
                nzpa__kaqeo.difference_update(hqpx__yhe)
                smgqp__umsj.difference_update(hqpx__yhe)
                null_set.update(hqpx__yhe)
                expr_node.lhs = append_null_checks(dwwpz__grk, nzpa__kaqeo)
                expr_node.rhs = append_null_checks(hfj__eaw, smgqp__umsj)
                expr_node.operands = expr_node.lhs, expr_node.rhs
            else:
                expr_node.lhs = _insert_NA_cond_body(expr_node.lhs, null_set)
                expr_node.rhs = _insert_NA_cond_body(expr_node.rhs, null_set)
        elif _is_col_access(expr_node):
            lalg__rbyy = expr_node.name
            uei__wkq, col_name = lalg__rbyy.split('.')
            if uei__wkq == 'left':
                snebn__tbwk = left_columns
                data = left_data
            else:
                snebn__tbwk = right_columns
                data = right_data
            grsg__cis = data[snebn__tbwk.index(col_name)]
            if bodo.utils.typing.is_nullable(grsg__cis):
                null_set.add(expr_node.name)
        return expr_node
    null_set = set()
    mhny__jaf = _insert_NA_cond_body(expr_node, null_set)
    return append_null_checks(expr_node, null_set)


def _extract_equal_conds(expr_node):
    if not hasattr(expr_node, 'op'):
        return [], [], expr_node
    if expr_node.op == '==' and _is_col_access(expr_node.lhs
        ) and _is_col_access(expr_node.rhs):
        oyxtp__cizt = str(expr_node.lhs)
        skqki__wkmdb = str(expr_node.rhs)
        if oyxtp__cizt.startswith('(left.') and skqki__wkmdb.startswith(
            '(left.') or oyxtp__cizt.startswith('(right.'
            ) and skqki__wkmdb.startswith('(right.'):
            return [], [], expr_node
        left_on = [oyxtp__cizt.split('.')[1][:-1]]
        right_on = [skqki__wkmdb.split('.')[1][:-1]]
        if oyxtp__cizt.startswith('(right.'):
            return right_on, left_on, None
        return left_on, right_on, None
    if expr_node.op == '&':
        gpak__cobe, tvwy__zsdvi, moend__aheyi = _extract_equal_conds(expr_node
            .lhs)
        znyp__rfe, hred__nmxti, caa__sex = _extract_equal_conds(expr_node.rhs)
        left_on = gpak__cobe + znyp__rfe
        right_on = tvwy__zsdvi + hred__nmxti
        if moend__aheyi is None:
            return left_on, right_on, caa__sex
        if caa__sex is None:
            return left_on, right_on, moend__aheyi
        expr_node.lhs = moend__aheyi
        expr_node.rhs = caa__sex
        expr_node.operands = expr_node.lhs, expr_node.rhs
        return left_on, right_on, expr_node
    return [], [], expr_node


def _parse_merge_cond(on_str, left_columns, left_data, right_columns,
    right_data):
    zvuwg__kww = {'left': 0, 'right': 0}
    env = pd.core.computation.scope.ensure_scope(2, {}, {}, (zvuwg__kww,))
    qgkyu__cmtdh = dict()
    vyt__zyg = pd.core.computation.parsing.clean_column_name
    for name, bwiz__bknwv in (('left', left_columns), ('right', right_columns)
        ):
        for mtkif__qzfuw in bwiz__bknwv:
            ksdn__jeys = vyt__zyg(mtkif__qzfuw)
            onrvw__wupnr = name, ksdn__jeys
            if onrvw__wupnr in qgkyu__cmtdh:
                raise_bodo_error(
                    f"pd.merge(): {name} table contains two columns that are escaped to the same Python identifier '{mtkif__qzfuw}' and '{qgkyu__cmtdh[ksdn__jeys]}' Please rename one of these columns. To avoid this issue, please use names that are valid Python identifiers."
                    )
            qgkyu__cmtdh[onrvw__wupnr] = mtkif__qzfuw
    nma__clkv, _, _ = _parse_query_expr(on_str, env, [], [], None,
        join_cleaned_cols=qgkyu__cmtdh)
    left_on, right_on, pyitl__mwa = _extract_equal_conds(nma__clkv.terms)
    return left_on, right_on, _insert_NA_cond(pyitl__mwa, left_columns,
        left_data, right_columns, right_data)


@overload_method(DataFrameType, 'merge', inline='always', no_unliteral=True)
@overload(pd.merge, inline='always', no_unliteral=True)
def overload_dataframe_merge(left, right, how='inner', on=None, left_on=
    None, right_on=None, left_index=False, right_index=False, sort=False,
    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None,
    _bodo_na_equal=True):
    check_runtime_cols_unsupported(left, 'DataFrame.merge()')
    check_runtime_cols_unsupported(right, 'DataFrame.merge()')
    hwzb__jnck = dict(sort=sort, copy=copy, validate=validate)
    szrb__ldodx = dict(sort=False, copy=True, validate=None)
    check_unsupported_args('DataFrame.merge', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
        right_index, sort, suffixes, copy, indicator, validate)
    how = get_overload_const_str(how)
    nyo__oxa = tuple(sorted(set(left.columns) & set(right.columns), key=lambda
        k: str(k)))
    nsd__zfl = ''
    if not is_overload_none(on):
        left_on = right_on = on
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            if on_str not in nyo__oxa and ('left.' in on_str or 'right.' in
                on_str):
                left_on, right_on, qobhf__yvr = _parse_merge_cond(on_str,
                    left.columns, left.data, right.columns, right.data)
                if qobhf__yvr is None:
                    nsd__zfl = ''
                else:
                    nsd__zfl = str(qobhf__yvr)
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = nyo__oxa
        right_keys = nyo__oxa
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    if not is_overload_bool(indicator):
        raise_bodo_error(
            'DataFrame.merge(): indicator must be a constant boolean')
    indicator_val = get_overload_const_bool(indicator)
    if not is_overload_bool(_bodo_na_equal):
        raise_bodo_error(
            'DataFrame.merge(): bodo extension _bodo_na_equal must be a constant boolean'
            )
    opyiz__ybxy = get_overload_const_bool(_bodo_na_equal)
    validate_keys_length(left_index, right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    if is_overload_constant_tuple(suffixes):
        muht__wrdou = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        muht__wrdou = list(get_overload_const_list(suffixes))
    suffix_x = muht__wrdou[0]
    suffix_y = muht__wrdou[1]
    validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
        right_keys, left.columns, right.columns, indicator_val)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    dvhz__hbzun = (
        "def _impl(left, right, how='inner', on=None, left_on=None,\n")
    dvhz__hbzun += (
        '    right_on=None, left_index=False, right_index=False, sort=False,\n'
        )
    dvhz__hbzun += """    suffixes=('_x', '_y'), copy=True, indicator=False, validate=None, _bodo_na_equal=True):
"""
    dvhz__hbzun += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, '{}', '{}', '{}', False, {}, {}, '{}')
"""
        .format(left_keys, right_keys, how, suffix_x, suffix_y,
        indicator_val, opyiz__ybxy, nsd__zfl))
    unozl__xox = {}
    exec(dvhz__hbzun, {'bodo': bodo}, unozl__xox)
    _impl = unozl__xox['_impl']
    return _impl


def common_validate_merge_merge_asof_spec(name_func, left, right, on,
    left_on, right_on, left_index, right_index, suffixes):
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError(name_func + '() requires dataframe inputs')
    valid_dataframe_column_types = (ArrayItemArrayType, MapArrayType,
        StructArrayType, CategoricalArrayType, types.Array,
        IntegerArrayType, FloatingArrayType, DecimalArrayType,
        IntervalArrayType, bodo.DatetimeArrayType, TimeArrayType)
    uek__ndla = {string_array_type, dict_str_arr_type, binary_array_type,
        datetime_date_array_type, datetime_timedelta_array_type, boolean_array}
    xhl__npnyl = {get_overload_const_str(zlf__svv) for zlf__svv in (left_on,
        right_on, on) if is_overload_constant_str(zlf__svv)}
    for df in (left, right):
        for i, mtkif__qzfuw in enumerate(df.data):
            if not isinstance(mtkif__qzfuw, valid_dataframe_column_types
                ) and mtkif__qzfuw not in uek__ndla:
                raise BodoError(
                    f'{name_func}(): use of column with {type(mtkif__qzfuw)} in merge unsupported'
                    )
            if df.columns[i] in xhl__npnyl and isinstance(mtkif__qzfuw,
                MapArrayType):
                raise BodoError(
                    f'{name_func}(): merge on MapArrayType unsupported')
    ensure_constant_arg(name_func, 'left_index', left_index, bool)
    ensure_constant_arg(name_func, 'right_index', right_index, bool)
    if not is_overload_constant_tuple(suffixes
        ) and not is_overload_constant_list(suffixes):
        raise_bodo_error(name_func +
            "(): suffixes parameters should be ['_left', '_right']")
    if is_overload_constant_tuple(suffixes):
        muht__wrdou = get_overload_const_tuple(suffixes)
    if is_overload_constant_list(suffixes):
        muht__wrdou = list(get_overload_const_list(suffixes))
    if len(muht__wrdou) != 2:
        raise BodoError(name_func +
            '(): The number of suffixes should be exactly 2')
    nyo__oxa = tuple(set(left.columns) & set(right.columns))
    if not is_overload_none(on):
        pozn__xrz = False
        if is_overload_constant_str(on):
            on_str = get_overload_const_str(on)
            pozn__xrz = on_str not in nyo__oxa and ('left.' in on_str or 
                'right.' in on_str)
        if len(nyo__oxa) == 0 and not pozn__xrz:
            raise_bodo_error(name_func +
                '(): No common columns to perform merge on. Merge options: left_on={lon}, right_on={ron}, left_index={lidx}, right_index={ridx}'
                .format(lon=is_overload_true(left_on), ron=is_overload_true
                (right_on), lidx=is_overload_true(left_index), ridx=
                is_overload_true(right_index)))
        if not is_overload_none(left_on) or not is_overload_none(right_on):
            raise BodoError(name_func +
                '(): Can only pass argument "on" OR "left_on" and "right_on", not a combination of both.'
                )
    if (is_overload_true(left_index) or not is_overload_none(left_on)
        ) and is_overload_none(right_on) and not is_overload_true(right_index):
        raise BodoError(name_func +
            '(): Must pass right_on or right_index=True')
    if (is_overload_true(right_index) or not is_overload_none(right_on)
        ) and is_overload_none(left_on) and not is_overload_true(left_index):
        raise BodoError(name_func + '(): Must pass left_on or left_index=True')


def validate_merge_spec(left, right, how, on, left_on, right_on, left_index,
    right_index, sort, suffixes, copy, indicator, validate):
    common_validate_merge_merge_asof_spec('merge', left, right, on, left_on,
        right_on, left_index, right_index, suffixes)
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner', 'cross'))


def validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
    right_index, by, left_by, right_by, suffixes, tolerance,
    allow_exact_matches, direction):
    common_validate_merge_merge_asof_spec('merge_asof', left, right, on,
        left_on, right_on, left_index, right_index, suffixes)
    if not is_overload_true(allow_exact_matches):
        raise BodoError(
            'merge_asof(): allow_exact_matches parameter only supports default value True'
            )
    if not is_overload_none(tolerance):
        raise BodoError(
            'merge_asof(): tolerance parameter only supports default value None'
            )
    if not is_overload_none(by):
        raise BodoError(
            'merge_asof(): by parameter only supports default value None')
    if not is_overload_none(left_by):
        raise BodoError(
            'merge_asof(): left_by parameter only supports default value None')
    if not is_overload_none(right_by):
        raise BodoError(
            'merge_asof(): right_by parameter only supports default value None'
            )
    if not is_overload_constant_str(direction):
        raise BodoError(
            'merge_asof(): direction parameter should be of type str')
    else:
        direction = get_overload_const_str(direction)
        if direction != 'backward':
            raise BodoError(
                "merge_asof(): direction parameter only supports default value 'backward'"
                )


def validate_merge_asof_keys_length(left_on, right_on, left_index,
    right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if not is_overload_none(left_on) and is_overload_true(right_index):
        raise BodoError(
            'merge(): right_index = True and specifying left_on is not suppported yet.'
            )
    if not is_overload_none(right_on) and is_overload_true(left_index):
        raise BodoError(
            'merge(): left_index = True and specifying right_on is not suppported yet.'
            )


def validate_keys_length(left_index, right_index, left_keys, right_keys):
    if not is_overload_true(left_index) and not is_overload_true(right_index):
        if len(right_keys) != len(left_keys):
            raise BodoError('merge(): len(right_on) must equal len(left_on)')
    if is_overload_true(right_index):
        if len(left_keys) != 1:
            raise BodoError(
                'merge(): len(left_on) must equal the number of levels in the index of "right", which is 1'
                )
    if is_overload_true(left_index):
        if len(right_keys) != 1:
            raise BodoError(
                'merge(): len(right_on) must equal the number of levels in the index of "left", which is 1'
                )


def validate_keys_dtypes(left, right, left_index, right_index, left_keys,
    right_keys):
    dfv__hwgyj = numba.core.registry.cpu_target.typing_context
    if is_overload_true(left_index) or is_overload_true(right_index):
        if is_overload_true(left_index) and is_overload_true(right_index):
            rxh__fjfed = left.index
            pfjma__zslyb = isinstance(rxh__fjfed, StringIndexType)
            jwr__brgkz = right.index
            njt__puaax = isinstance(jwr__brgkz, StringIndexType)
        elif is_overload_true(left_index):
            rxh__fjfed = left.index
            pfjma__zslyb = isinstance(rxh__fjfed, StringIndexType)
            jwr__brgkz = right.data[right.columns.index(right_keys[0])]
            njt__puaax = jwr__brgkz.dtype == string_type
        elif is_overload_true(right_index):
            rxh__fjfed = left.data[left.columns.index(left_keys[0])]
            pfjma__zslyb = rxh__fjfed.dtype == string_type
            jwr__brgkz = right.index
            njt__puaax = isinstance(jwr__brgkz, StringIndexType)
        if pfjma__zslyb and njt__puaax:
            return
        rxh__fjfed = rxh__fjfed.dtype
        jwr__brgkz = jwr__brgkz.dtype
        try:
            tfd__nhtqx = dfv__hwgyj.resolve_function_type(operator.eq, (
                rxh__fjfed, jwr__brgkz), {})
        except:
            raise_bodo_error(
                'merge: You are trying to merge on {lk_dtype} and {rk_dtype} columns. If you wish to proceed you should use pd.concat'
                .format(lk_dtype=rxh__fjfed, rk_dtype=jwr__brgkz))
    else:
        for fxrtm__pus, oyxi__zord in zip(left_keys, right_keys):
            rxh__fjfed = left.data[left.columns.index(fxrtm__pus)].dtype
            hmj__bfyrt = left.data[left.columns.index(fxrtm__pus)]
            jwr__brgkz = right.data[right.columns.index(oyxi__zord)].dtype
            fcls__qkucl = right.data[right.columns.index(oyxi__zord)]
            if hmj__bfyrt == fcls__qkucl:
                continue
            ckqgd__cslkv = (
                'merge: You are trying to merge on column {lk} of {lk_dtype} and column {rk} of {rk_dtype}. If you wish to proceed you should use pd.concat'
                .format(lk=fxrtm__pus, lk_dtype=rxh__fjfed, rk=oyxi__zord,
                rk_dtype=jwr__brgkz))
            embzs__rjh = rxh__fjfed == string_type
            hqu__xsfv = jwr__brgkz == string_type
            if embzs__rjh ^ hqu__xsfv:
                raise_bodo_error(ckqgd__cslkv)
            try:
                tfd__nhtqx = dfv__hwgyj.resolve_function_type(operator.eq,
                    (rxh__fjfed, jwr__brgkz), {})
            except:
                raise_bodo_error(ckqgd__cslkv)


def validate_keys(keys, df):
    kcviw__qfo = set(keys).difference(set(df.columns))
    if len(kcviw__qfo) > 0:
        if is_overload_constant_str(df.index.name_typ
            ) and get_overload_const_str(df.index.name_typ) in kcviw__qfo:
            raise_bodo_error(
                f'merge(): use of index {df.index.name_typ} as key for on/left_on/right_on is unsupported'
                )
        raise_bodo_error(
            f"""merge(): invalid key {kcviw__qfo} for on/left_on/right_on
merge supports only valid column names {df.columns}"""
            )


@overload_method(DataFrameType, 'join', inline='always', no_unliteral=True)
def overload_dataframe_join(left, other, on=None, how='left', lsuffix='',
    rsuffix='', sort=False):
    check_runtime_cols_unsupported(left, 'DataFrame.join()')
    check_runtime_cols_unsupported(other, 'DataFrame.join()')
    hwzb__jnck = dict(lsuffix=lsuffix, rsuffix=rsuffix)
    szrb__ldodx = dict(lsuffix='', rsuffix='')
    check_unsupported_args('DataFrame.join', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort)
    how = get_overload_const_str(how)
    if not is_overload_none(on):
        left_keys = get_overload_const_list(on)
    else:
        left_keys = ['$_bodo_index_']
    right_keys = ['$_bodo_index_']
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    dvhz__hbzun = "def _impl(left, other, on=None, how='left',\n"
    dvhz__hbzun += "    lsuffix='', rsuffix='', sort=False):\n"
    dvhz__hbzun += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, other, {}, {}, '{}', '{}', '{}', True, False, True, '')
"""
        .format(left_keys, right_keys, how, lsuffix, rsuffix))
    unozl__xox = {}
    exec(dvhz__hbzun, {'bodo': bodo}, unozl__xox)
    _impl = unozl__xox['_impl']
    return _impl


def validate_join_spec(left, other, on, how, lsuffix, rsuffix, sort):
    if not isinstance(other, DataFrameType):
        raise BodoError('join() requires dataframe inputs')
    ensure_constant_values('merge', 'how', how, ('left', 'right', 'outer',
        'inner'))
    if not is_overload_none(on) and len(get_overload_const_list(on)) != 1:
        raise BodoError('join(): len(on) must equals to 1 when specified.')
    if not is_overload_none(on):
        fsg__pnz = get_overload_const_list(on)
        validate_keys(fsg__pnz, left)
    if not is_overload_false(sort):
        raise BodoError(
            'join(): sort parameter only supports default value False')
    nyo__oxa = tuple(set(left.columns) & set(other.columns))
    if len(nyo__oxa) > 0:
        raise_bodo_error(
            'join(): not supporting joining on overlapping columns:{cols} Use DataFrame.merge() instead.'
            .format(cols=nyo__oxa))


def validate_unicity_output_column_names(suffix_x, suffix_y, left_keys,
    right_keys, left_columns, right_columns, indicator_val):
    rxx__sfjsp = set(left_keys) & set(right_keys)
    uoyzj__dlc = set(left_columns) & set(right_columns)
    naev__izhqf = uoyzj__dlc - rxx__sfjsp
    selsb__fhh = set(left_columns) - uoyzj__dlc
    duqkv__jkop = set(right_columns) - uoyzj__dlc
    qfc__mhx = {}

    def insertOutColumn(col_name):
        if col_name in qfc__mhx:
            raise_bodo_error(
                'join(): two columns happen to have the same name : {}'.
                format(col_name))
        qfc__mhx[col_name] = 0
    for rst__thqef in rxx__sfjsp:
        insertOutColumn(rst__thqef)
    for rst__thqef in naev__izhqf:
        jbo__dglmh = str(rst__thqef) + suffix_x
        uth__rzifg = str(rst__thqef) + suffix_y
        insertOutColumn(jbo__dglmh)
        insertOutColumn(uth__rzifg)
    for rst__thqef in selsb__fhh:
        insertOutColumn(rst__thqef)
    for rst__thqef in duqkv__jkop:
        insertOutColumn(rst__thqef)
    if indicator_val:
        insertOutColumn('_merge')


@overload(pd.merge_asof, inline='always', no_unliteral=True)
def overload_dataframe_merge_asof(left, right, on=None, left_on=None,
    right_on=None, left_index=False, right_index=False, by=None, left_by=
    None, right_by=None, suffixes=('_x', '_y'), tolerance=None,
    allow_exact_matches=True, direction='backward'):
    raise BodoError('pandas.merge_asof() not support yet')
    validate_merge_asof_spec(left, right, on, left_on, right_on, left_index,
        right_index, by, left_by, right_by, suffixes, tolerance,
        allow_exact_matches, direction)
    if not isinstance(left, DataFrameType) or not isinstance(right,
        DataFrameType):
        raise BodoError('merge_asof() requires dataframe inputs')
    nyo__oxa = tuple(sorted(set(left.columns) & set(right.columns), key=lambda
        k: str(k)))
    if not is_overload_none(on):
        left_on = right_on = on
    if is_overload_none(on) and is_overload_none(left_on) and is_overload_none(
        right_on) and is_overload_false(left_index) and is_overload_false(
        right_index):
        left_keys = nyo__oxa
        right_keys = nyo__oxa
    else:
        if is_overload_true(left_index):
            left_keys = ['$_bodo_index_']
        else:
            left_keys = get_overload_const_list(left_on)
            validate_keys(left_keys, left)
        if is_overload_true(right_index):
            right_keys = ['$_bodo_index_']
        else:
            right_keys = get_overload_const_list(right_on)
            validate_keys(right_keys, right)
    validate_merge_asof_keys_length(left_on, right_on, left_index,
        right_index, left_keys, right_keys)
    validate_keys_dtypes(left, right, left_index, right_index, left_keys,
        right_keys)
    left_keys = gen_const_tup(left_keys)
    right_keys = gen_const_tup(right_keys)
    if isinstance(suffixes, tuple):
        muht__wrdou = suffixes
    if is_overload_constant_list(suffixes):
        muht__wrdou = list(get_overload_const_list(suffixes))
    if isinstance(suffixes, types.Omitted):
        muht__wrdou = suffixes.value
    suffix_x = muht__wrdou[0]
    suffix_y = muht__wrdou[1]
    dvhz__hbzun = (
        'def _impl(left, right, on=None, left_on=None, right_on=None,\n')
    dvhz__hbzun += (
        '    left_index=False, right_index=False, by=None, left_by=None,\n')
    dvhz__hbzun += (
        "    right_by=None, suffixes=('_x', '_y'), tolerance=None,\n")
    dvhz__hbzun += "    allow_exact_matches=True, direction='backward'):\n"
    dvhz__hbzun += '  suffix_x = suffixes[0]\n'
    dvhz__hbzun += '  suffix_y = suffixes[1]\n'
    dvhz__hbzun += (
        """  return bodo.hiframes.pd_dataframe_ext.join_dummy(left, right, {}, {}, 'asof', '{}', '{}', False, False, True, '')
"""
        .format(left_keys, right_keys, suffix_x, suffix_y))
    unozl__xox = {}
    exec(dvhz__hbzun, {'bodo': bodo}, unozl__xox)
    _impl = unozl__xox['_impl']
    return _impl


@overload_method(DataFrameType, 'groupby', inline='always', no_unliteral=True)
def overload_dataframe_groupby(df, by=None, axis=0, level=None, as_index=
    True, sort=False, group_keys=True, squeeze=False, observed=True, dropna
    =True, _bodo_num_shuffle_keys=-1):
    check_runtime_cols_unsupported(df, 'DataFrame.groupby()')
    validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
        squeeze, observed, dropna, _bodo_num_shuffle_keys)

    def _impl(df, by=None, axis=0, level=None, as_index=True, sort=False,
        group_keys=True, squeeze=False, observed=True, dropna=True,
        _bodo_num_shuffle_keys=-1):
        return bodo.hiframes.pd_groupby_ext.init_groupby(df, by, as_index,
            dropna, _bodo_num_shuffle_keys)
    return _impl


def validate_groupby_spec(df, by, axis, level, as_index, sort, group_keys,
    squeeze, observed, dropna, _num_shuffle_keys):
    if is_overload_none(by):
        raise BodoError("groupby(): 'by' must be supplied.")
    if not is_overload_zero(axis):
        raise BodoError(
            "groupby(): 'axis' parameter only supports integer value 0.")
    if not is_overload_none(level):
        raise BodoError(
            "groupby(): 'level' is not supported since MultiIndex is not supported."
            )
    if not is_literal_type(by) and not is_overload_constant_list(by):
        raise_bodo_error(
            f"groupby(): 'by' parameter only supports a constant column label or column labels, not {by}."
            )
    if len(set(get_overload_const_list(by)).difference(set(df.columns))) > 0:
        raise_bodo_error(
            "groupby(): invalid key {} for 'by' (not available in columns {})."
            .format(get_overload_const_list(by), df.columns))
    if not is_overload_constant_bool(as_index):
        raise_bodo_error(
            "groupby(): 'as_index' parameter must be a constant bool, not {}."
            .format(as_index))
    if not is_overload_constant_bool(dropna):
        raise_bodo_error(
            "groupby(): 'dropna' parameter must be a constant bool, not {}."
            .format(dropna))
    if not is_overload_constant_int(_num_shuffle_keys):
        raise_bodo_error(
            f"groupby(): '_num_shuffle_keys' parameter must be a constant integer, not {_num_shuffle_keys}."
            )
    hwzb__jnck = dict(sort=sort, group_keys=group_keys, squeeze=squeeze,
        observed=observed)
    pkp__ylulp = dict(sort=False, group_keys=True, squeeze=False, observed=True
        )
    check_unsupported_args('Dataframe.groupby', hwzb__jnck, pkp__ylulp,
        package_name='pandas', module_name='GroupBy')


def pivot_error_checking(df, index, columns, values, func_name):
    fgjuk__bng = func_name == 'DataFrame.pivot_table'
    if fgjuk__bng:
        if is_overload_none(index) or not is_literal_type(index):
            raise_bodo_error(
                f"DataFrame.pivot_table(): 'index' argument is required and must be constant column labels"
                )
    elif not is_overload_none(index) and not is_literal_type(index):
        raise_bodo_error(
            f"{func_name}(): if 'index' argument is provided it must be constant column labels"
            )
    if is_overload_none(columns) or not is_literal_type(columns):
        raise_bodo_error(
            f"{func_name}(): 'columns' argument is required and must be a constant column label"
            )
    if not is_overload_none(values) and not is_literal_type(values):
        raise_bodo_error(
            f"{func_name}(): if 'values' argument is provided it must be constant column labels"
            )
    piu__dsf = get_literal_value(columns)
    if isinstance(piu__dsf, (list, tuple)):
        if len(piu__dsf) > 1:
            raise BodoError(
                f"{func_name}(): 'columns' argument must be a constant column label not a {piu__dsf}"
                )
        piu__dsf = piu__dsf[0]
    if piu__dsf not in df.columns:
        raise BodoError(
            f"{func_name}(): 'columns' column {piu__dsf} not found in DataFrame {df}."
            )
    sno__dmenh = df.column_index[piu__dsf]
    if is_overload_none(index):
        ehbc__ncdt = []
        usrc__ygewi = []
    else:
        usrc__ygewi = get_literal_value(index)
        if not isinstance(usrc__ygewi, (list, tuple)):
            usrc__ygewi = [usrc__ygewi]
        ehbc__ncdt = []
        for index in usrc__ygewi:
            if index not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'index' column {index} not found in DataFrame {df}."
                    )
            ehbc__ncdt.append(df.column_index[index])
    if not (all(isinstance(ibfb__ifl, int) for ibfb__ifl in usrc__ygewi) or
        all(isinstance(ibfb__ifl, str) for ibfb__ifl in usrc__ygewi)):
        raise BodoError(
            f"{func_name}(): column names selected for 'index' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    if is_overload_none(values):
        xkk__vyrl = []
        yfzkb__uzits = []
        spwdc__mnpyz = ehbc__ncdt + [sno__dmenh]
        for i, ibfb__ifl in enumerate(df.columns):
            if i not in spwdc__mnpyz:
                xkk__vyrl.append(i)
                yfzkb__uzits.append(ibfb__ifl)
    else:
        yfzkb__uzits = get_literal_value(values)
        if not isinstance(yfzkb__uzits, (list, tuple)):
            yfzkb__uzits = [yfzkb__uzits]
        xkk__vyrl = []
        for val in yfzkb__uzits:
            if val not in df.column_index:
                raise BodoError(
                    f"{func_name}(): 'values' column {val} not found in DataFrame {df}."
                    )
            xkk__vyrl.append(df.column_index[val])
    bvf__jks = set(xkk__vyrl) | set(ehbc__ncdt) | {sno__dmenh}
    if len(bvf__jks) != len(xkk__vyrl) + len(ehbc__ncdt) + 1:
        raise BodoError(
            f"{func_name}(): 'index', 'columns', and 'values' must all refer to different columns"
            )

    def check_valid_index_typ(index_column):
        if isinstance(index_column, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType, bodo.
            IntervalArrayType)):
            raise BodoError(
                f"{func_name}(): 'index' DataFrame column must have scalar rows"
                )
        if isinstance(index_column, bodo.CategoricalArrayType):
            raise BodoError(
                f"{func_name}(): 'index' DataFrame column does not support categorical data"
                )
    if len(ehbc__ncdt) == 0:
        index = df.index
        if isinstance(index, MultiIndexType):
            raise BodoError(
                f"{func_name}(): 'index' cannot be None with a DataFrame with a multi-index"
                )
        if not isinstance(index, RangeIndexType):
            check_valid_index_typ(index.data)
        if not is_literal_type(df.index.name_typ):
            raise BodoError(
                f"{func_name}(): If 'index' is None, the name of the DataFrame's Index must be constant at compile-time"
                )
    else:
        for gsmt__risr in ehbc__ncdt:
            index_column = df.data[gsmt__risr]
            check_valid_index_typ(index_column)
    anppq__lpa = df.data[sno__dmenh]
    if isinstance(anppq__lpa, (bodo.ArrayItemArrayType, bodo.MapArrayType,
        bodo.StructArrayType, bodo.TupleArrayType, bodo.IntervalArrayType)):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column must have scalar rows")
    if isinstance(anppq__lpa, bodo.CategoricalArrayType):
        raise BodoError(
            f"{func_name}(): 'columns' DataFrame column does not support categorical data"
            )
    for jjq__kkqne in xkk__vyrl:
        cvln__uldw = df.data[jjq__kkqne]
        if isinstance(cvln__uldw, (bodo.ArrayItemArrayType, bodo.
            MapArrayType, bodo.StructArrayType, bodo.TupleArrayType)
            ) or cvln__uldw == bodo.binary_array_type:
            raise BodoError(
                f"{func_name}(): 'values' DataFrame column must have scalar rows"
                )
    return (usrc__ygewi, piu__dsf, yfzkb__uzits, ehbc__ncdt, sno__dmenh,
        xkk__vyrl)


@overload(pd.pivot, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot', inline='always', no_unliteral=True)
def overload_dataframe_pivot(data, index=None, columns=None, values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot()')
    if not isinstance(data, DataFrameType):
        raise BodoError("pandas.pivot(): 'data' argument must be a DataFrame")
    (usrc__ygewi, piu__dsf, yfzkb__uzits, gsmt__risr, sno__dmenh, sksqj__bod
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot'))
    if len(usrc__ygewi) == 0:
        if is_overload_none(data.index.name_typ):
            xmurr__gfwvz = None,
        else:
            xmurr__gfwvz = get_literal_value(data.index.name_typ),
    else:
        xmurr__gfwvz = tuple(usrc__ygewi)
    usrc__ygewi = ColNamesMetaType(xmurr__gfwvz)
    yfzkb__uzits = ColNamesMetaType(tuple(yfzkb__uzits))
    piu__dsf = ColNamesMetaType((piu__dsf,))
    dvhz__hbzun = 'def impl(data, index=None, columns=None, values=None):\n'
    dvhz__hbzun += "    ev = tracing.Event('df.pivot')\n"
    dvhz__hbzun += f'    pivot_values = data.iloc[:, {sno__dmenh}].unique()\n'
    dvhz__hbzun += '    result = bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    if len(gsmt__risr) == 0:
        dvhz__hbzun += f"""        (bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(data)),),
"""
    else:
        dvhz__hbzun += '        (\n'
        for odi__dqjw in gsmt__risr:
            dvhz__hbzun += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {odi__dqjw}),
"""
        dvhz__hbzun += '        ),\n'
    dvhz__hbzun += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {sno__dmenh}),),
"""
    dvhz__hbzun += '        (\n'
    for jjq__kkqne in sksqj__bod:
        dvhz__hbzun += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {jjq__kkqne}),
"""
    dvhz__hbzun += '        ),\n'
    dvhz__hbzun += '        pivot_values,\n'
    dvhz__hbzun += '        index_lit,\n'
    dvhz__hbzun += '        columns_lit,\n'
    dvhz__hbzun += '        values_lit,\n'
    dvhz__hbzun += '    )\n'
    dvhz__hbzun += '    ev.finalize()\n'
    dvhz__hbzun += '    return result\n'
    unozl__xox = {}
    exec(dvhz__hbzun, {'bodo': bodo, 'index_lit': usrc__ygewi,
        'columns_lit': piu__dsf, 'values_lit': yfzkb__uzits, 'tracing':
        tracing}, unozl__xox)
    impl = unozl__xox['impl']
    return impl


@overload(pd.pivot_table, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'pivot_table', inline='always',
    no_unliteral=True)
def overload_dataframe_pivot_table(data, values=None, index=None, columns=
    None, aggfunc='mean', fill_value=None, margins=False, dropna=True,
    margins_name='All', observed=False, sort=True, _pivot_values=None):
    check_runtime_cols_unsupported(data, 'DataFrame.pivot_table()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(data,
        'DataFrame.pivot_table()')
    hwzb__jnck = dict(fill_value=fill_value, margins=margins, dropna=dropna,
        margins_name=margins_name, observed=observed, sort=sort)
    szrb__ldodx = dict(fill_value=None, margins=False, dropna=True,
        margins_name='All', observed=False, sort=True)
    check_unsupported_args('DataFrame.pivot_table', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(data, DataFrameType):
        raise BodoError(
            "pandas.pivot_table(): 'data' argument must be a DataFrame")
    (usrc__ygewi, piu__dsf, yfzkb__uzits, gsmt__risr, sno__dmenh, sksqj__bod
        ) = (pivot_error_checking(data, index, columns, values,
        'DataFrame.pivot_table'))
    yeep__kssez = usrc__ygewi
    usrc__ygewi = ColNamesMetaType(tuple(usrc__ygewi))
    yfzkb__uzits = ColNamesMetaType(tuple(yfzkb__uzits))
    srv__bbpcg = piu__dsf
    piu__dsf = ColNamesMetaType((piu__dsf,))
    dvhz__hbzun = 'def impl(\n'
    dvhz__hbzun += '    data,\n'
    dvhz__hbzun += '    values=None,\n'
    dvhz__hbzun += '    index=None,\n'
    dvhz__hbzun += '    columns=None,\n'
    dvhz__hbzun += '    aggfunc="mean",\n'
    dvhz__hbzun += '    fill_value=None,\n'
    dvhz__hbzun += '    margins=False,\n'
    dvhz__hbzun += '    dropna=True,\n'
    dvhz__hbzun += '    margins_name="All",\n'
    dvhz__hbzun += '    observed=False,\n'
    dvhz__hbzun += '    sort=True,\n'
    dvhz__hbzun += '    _pivot_values=None,\n'
    dvhz__hbzun += '):\n'
    dvhz__hbzun += "    ev = tracing.Event('df.pivot_table')\n"
    joib__nxmia = gsmt__risr + [sno__dmenh] + sksqj__bod
    dvhz__hbzun += f'    data = data.iloc[:, {joib__nxmia}]\n'
    ulcza__evk = yeep__kssez + [srv__bbpcg]
    if not is_overload_none(_pivot_values):
        wicx__cys = tuple(sorted(_pivot_values.meta))
        _pivot_values = ColNamesMetaType(wicx__cys)
        dvhz__hbzun += '    pivot_values = _pivot_values_arr\n'
        dvhz__hbzun += (
            f'    data = data[data.iloc[:, {len(gsmt__risr)}].isin(pivot_values)]\n'
            )
        if all(isinstance(ibfb__ifl, str) for ibfb__ifl in wicx__cys):
            rdemv__eokzo = pd.array(wicx__cys, 'string')
        elif all(isinstance(ibfb__ifl, int) for ibfb__ifl in wicx__cys):
            rdemv__eokzo = np.array(wicx__cys, 'int64')
        else:
            raise BodoError(
                f'pivot(): pivot values selcected via pivot JIT argument must all share a common int or string type.'
                )
    else:
        rdemv__eokzo = None
    thi__qzc = is_overload_constant_str(aggfunc) and get_overload_const_str(
        aggfunc) == 'nunique'
    culu__wvzu = len(ulcza__evk) if thi__qzc else len(yeep__kssez)
    dvhz__hbzun += f"""    data = data.groupby({ulcza__evk!r}, as_index=False, _bodo_num_shuffle_keys={culu__wvzu}).agg(aggfunc)
"""
    if is_overload_none(_pivot_values):
        dvhz__hbzun += (
            f'    pivot_values = data.iloc[:, {len(gsmt__risr)}].unique()\n')
    dvhz__hbzun += '    result = bodo.hiframes.pd_dataframe_ext.pivot_impl(\n'
    dvhz__hbzun += '        (\n'
    for i in range(0, len(gsmt__risr)):
        dvhz__hbzun += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
    dvhz__hbzun += '        ),\n'
    dvhz__hbzun += f"""        (bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {len(gsmt__risr)}),),
"""
    dvhz__hbzun += '        (\n'
    for i in range(len(gsmt__risr) + 1, len(sksqj__bod) + len(gsmt__risr) + 1):
        dvhz__hbzun += f"""            bodo.hiframes.pd_dataframe_ext.get_dataframe_data(data, {i}),
"""
    dvhz__hbzun += '        ),\n'
    dvhz__hbzun += '        pivot_values,\n'
    dvhz__hbzun += '        index_lit,\n'
    dvhz__hbzun += '        columns_lit,\n'
    dvhz__hbzun += '        values_lit,\n'
    dvhz__hbzun += '        check_duplicates=False,\n'
    dvhz__hbzun += f'        is_already_shuffled={not thi__qzc},\n'
    dvhz__hbzun += '        _constant_pivot_values=_constant_pivot_values,\n'
    dvhz__hbzun += '    )\n'
    dvhz__hbzun += '    ev.finalize()\n'
    dvhz__hbzun += '    return result\n'
    unozl__xox = {}
    exec(dvhz__hbzun, {'bodo': bodo, 'numba': numba, 'index_lit':
        usrc__ygewi, 'columns_lit': piu__dsf, 'values_lit': yfzkb__uzits,
        '_pivot_values_arr': rdemv__eokzo, '_constant_pivot_values':
        _pivot_values, 'tracing': tracing}, unozl__xox)
    impl = unozl__xox['impl']
    return impl


@overload(pd.melt, inline='always', no_unliteral=True)
@overload_method(DataFrameType, 'melt', inline='always', no_unliteral=True)
def overload_dataframe_melt(frame, id_vars=None, value_vars=None, var_name=
    None, value_name='value', col_level=None, ignore_index=True):
    hwzb__jnck = dict(col_level=col_level, ignore_index=ignore_index)
    szrb__ldodx = dict(col_level=None, ignore_index=True)
    check_unsupported_args('DataFrame.melt', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    if not isinstance(frame, DataFrameType):
        raise BodoError("pandas.melt(): 'frame' argument must be a DataFrame.")
    if not is_overload_none(id_vars) and not is_literal_type(id_vars):
        raise_bodo_error(
            "DataFrame.melt(): 'id_vars', if specified, must be a literal.")
    if not is_overload_none(value_vars) and not is_literal_type(value_vars):
        raise_bodo_error(
            "DataFrame.melt(): 'value_vars', if specified, must be a literal.")
    if not is_overload_none(var_name) and not (is_literal_type(var_name) and
        (is_scalar_type(var_name) or isinstance(value_name, types.Omitted))):
        raise_bodo_error(
            "DataFrame.melt(): 'var_name', if specified, must be a literal.")
    if value_name != 'value' and not (is_literal_type(value_name) and (
        is_scalar_type(value_name) or isinstance(value_name, types.Omitted))):
        raise_bodo_error(
            "DataFrame.melt(): 'value_name', if specified, must be a literal.")
    var_name = get_literal_value(var_name) if not is_overload_none(var_name
        ) else 'variable'
    value_name = get_literal_value(value_name
        ) if value_name != 'value' else 'value'
    gss__kzjdd = get_literal_value(id_vars) if not is_overload_none(id_vars
        ) else []
    if not isinstance(gss__kzjdd, (list, tuple)):
        gss__kzjdd = [gss__kzjdd]
    for ibfb__ifl in gss__kzjdd:
        if ibfb__ifl not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'id_vars' column {ibfb__ifl} not found in {frame}."
                )
    rsx__pha = [frame.column_index[i] for i in gss__kzjdd]
    if is_overload_none(value_vars):
        bhx__aun = []
        pfxu__nldna = []
        for i, ibfb__ifl in enumerate(frame.columns):
            if i not in rsx__pha:
                bhx__aun.append(i)
                pfxu__nldna.append(ibfb__ifl)
    else:
        pfxu__nldna = get_literal_value(value_vars)
        if not isinstance(pfxu__nldna, (list, tuple)):
            pfxu__nldna = [pfxu__nldna]
        pfxu__nldna = [v for v in pfxu__nldna if v not in gss__kzjdd]
        if not pfxu__nldna:
            raise BodoError(
                "DataFrame.melt(): currently empty 'value_vars' is unsupported."
                )
        bhx__aun = []
        for val in pfxu__nldna:
            if val not in frame.column_index:
                raise BodoError(
                    f"DataFrame.melt(): 'value_vars' column {val} not found in DataFrame {frame}."
                    )
            bhx__aun.append(frame.column_index[val])
    for ibfb__ifl in pfxu__nldna:
        if ibfb__ifl not in frame.columns:
            raise BodoError(
                f"DataFrame.melt(): 'value_vars' column {ibfb__ifl} not found in {frame}."
                )
    if not (all(isinstance(ibfb__ifl, int) for ibfb__ifl in pfxu__nldna) or
        all(isinstance(ibfb__ifl, str) for ibfb__ifl in pfxu__nldna)):
        raise BodoError(
            f"DataFrame.melt(): column names selected for 'value_vars' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
            )
    ywpg__kawm = frame.data[bhx__aun[0]]
    zbkt__csf = [frame.data[i].dtype for i in bhx__aun]
    bhx__aun = np.array(bhx__aun, dtype=np.int64)
    rsx__pha = np.array(rsx__pha, dtype=np.int64)
    _, snq__blyu = bodo.utils.typing.get_common_scalar_dtype(zbkt__csf)
    if not snq__blyu:
        raise BodoError(
            "DataFrame.melt(): columns selected in 'value_vars' must have a unifiable type."
            )
    extra_globals = {'np': np, 'value_lit': pfxu__nldna, 'val_type': ywpg__kawm
        }
    header = 'def impl(\n'
    header += '  frame,\n'
    header += '  id_vars=None,\n'
    header += '  value_vars=None,\n'
    header += '  var_name=None,\n'
    header += "  value_name='value',\n"
    header += '  col_level=None,\n'
    header += '  ignore_index=True,\n'
    header += '):\n'
    header += (
        '  dummy_id = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, 0)\n'
        )
    if frame.is_table_format and all(v == ywpg__kawm.dtype for v in zbkt__csf):
        extra_globals['value_idxs'] = bodo.utils.typing.MetaType(tuple(
            bhx__aun))
        header += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(frame)\n'
            )
        header += (
            '  val_col = bodo.utils.table_utils.table_concat(table, value_idxs, val_type)\n'
            )
    elif len(pfxu__nldna) == 1:
        header += f"""  val_col = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {bhx__aun[0]})
"""
    else:
        abi__ame = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})'
             for i in bhx__aun)
        header += (
            f'  val_col = bodo.libs.array_kernels.concat(({abi__ame},))\n')
    header += """  var_col = bodo.libs.array_kernels.repeat_like(bodo.utils.conversion.coerce_to_array(value_lit), dummy_id)
"""
    for i in rsx__pha:
        header += (
            f'  id{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(frame, {i})\n'
            )
        header += (
            f'  out_id{i} = bodo.libs.array_kernels.concat([id{i}] * {len(pfxu__nldna)})\n'
            )
    ytwuo__ajl = ', '.join(f'out_id{i}' for i in rsx__pha) + (', ' if len(
        rsx__pha) > 0 else '')
    data_args = ytwuo__ajl + 'var_col, val_col'
    columns = tuple(gss__kzjdd + [var_name, value_name])
    index = (
        f'bodo.hiframes.pd_index_ext.init_range_index(0, len(frame) * {len(pfxu__nldna)}, 1, None)'
        )
    return _gen_init_df(header, columns, data_args, index, extra_globals)


@overload(pd.crosstab, inline='always', no_unliteral=True)
def crosstab_overload(index, columns, values=None, rownames=None, colnames=
    None, aggfunc=None, margins=False, margins_name='All', dropna=True,
    normalize=False, _pivot_values=None):
    raise BodoError(f'pandas.crosstab() not supported yet')
    hwzb__jnck = dict(values=values, rownames=rownames, colnames=colnames,
        aggfunc=aggfunc, margins=margins, margins_name=margins_name, dropna
        =dropna, normalize=normalize)
    szrb__ldodx = dict(values=None, rownames=None, colnames=None, aggfunc=
        None, margins=False, margins_name='All', dropna=True, normalize=False)
    check_unsupported_args('pandas.crosstab', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(index,
        'pandas.crosstab()')
    if not isinstance(index, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'index' argument only supported for Series types, found {index}"
            )
    if not isinstance(columns, SeriesType):
        raise BodoError(
            f"pandas.crosstab(): 'columns' argument only supported for Series types, found {columns}"
            )

    def _impl(index, columns, values=None, rownames=None, colnames=None,
        aggfunc=None, margins=False, margins_name='All', dropna=True,
        normalize=False, _pivot_values=None):
        return bodo.hiframes.pd_groupby_ext.crosstab_dummy(index, columns,
            _pivot_values)
    return _impl


@overload_method(DataFrameType, 'sort_values', inline='always',
    no_unliteral=True)
def overload_dataframe_sort_values(df, by, axis=0, ascending=True, inplace=
    False, kind='quicksort', na_position='last', ignore_index=False, key=
    None, _bodo_chunk_bounds=None, _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_values()')
    hwzb__jnck = dict(ignore_index=ignore_index, key=key)
    szrb__ldodx = dict(ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_values', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'sort_values')
    validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
        na_position, _bodo_chunk_bounds)

    def _impl(df, by, axis=0, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', ignore_index=False, key=None,
        _bodo_chunk_bounds=None, _bodo_transformed=False):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df, by,
            ascending, inplace, na_position, _bodo_chunk_bounds)
    return _impl


def validate_sort_values_spec(df, by, axis, ascending, inplace, kind,
    na_position, _bodo_chunk_bounds):
    if is_overload_none(by) or not is_literal_type(by
        ) and not is_overload_constant_list(by):
        raise_bodo_error(
            "sort_values(): 'by' parameter only supports a constant column label or column labels. by={}"
            .format(by))
    napoq__fgp = set(df.columns)
    if is_overload_constant_str(df.index.name_typ):
        napoq__fgp.add(get_overload_const_str(df.index.name_typ))
    if is_overload_constant_tuple(by):
        avv__whn = [get_overload_const_tuple(by)]
    else:
        avv__whn = get_overload_const_list(by)
    avv__whn = set((k, '') if (k, '') in napoq__fgp else k for k in avv__whn)
    if len(avv__whn.difference(napoq__fgp)) > 0:
        qwztx__cgw = list(set(get_overload_const_list(by)).difference(
            napoq__fgp))
        raise_bodo_error(f'sort_values(): invalid keys {qwztx__cgw} for by.')
    if not is_overload_none(_bodo_chunk_bounds) and len(avv__whn) != 1:
        raise_bodo_error(
            f'sort_values(): _bodo_chunk_bounds only supported when there is a single key.'
            )
    if not is_overload_zero(axis):
        raise_bodo_error(
            "sort_values(): 'axis' parameter only supports integer value 0.")
    if not is_overload_bool(ascending) and not is_overload_bool_list(ascending
        ):
        raise_bodo_error(
            "sort_values(): 'ascending' parameter must be of type bool or list of bool, not {}."
            .format(ascending))
    if not is_overload_bool(inplace):
        raise_bodo_error(
            "sort_values(): 'inplace' parameter must be of type bool, not {}."
            .format(inplace))
    if kind != 'quicksort' and not isinstance(kind, types.Omitted):
        warnings.warn(BodoWarning(
            'sort_values(): specifying sorting algorithm is not supported in Bodo. Bodo uses stable sort.'
            ))
    if is_overload_constant_str(na_position):
        na_position = get_overload_const_str(na_position)
        if na_position not in ('first', 'last'):
            raise BodoError(
                "sort_values(): na_position should either be 'first' or 'last'"
                )
    elif is_overload_constant_list(na_position):
        mnogt__cldg = get_overload_const_list(na_position)
        for na_position in mnogt__cldg:
            if na_position not in ('first', 'last'):
                raise BodoError(
                    "sort_values(): Every value in na_position should either be 'first' or 'last'"
                    )
    else:
        raise_bodo_error(
            f'sort_values(): na_position parameter must be a literal constant of type str or a constant list of str with 1 entry per key column, not {na_position}'
            )
    na_position = get_overload_const_str(na_position)
    if na_position not in ['first', 'last']:
        raise BodoError(
            "sort_values(): na_position should either be 'first' or 'last'")


@overload_method(DataFrameType, 'sort_index', inline='always', no_unliteral
    =True)
def overload_dataframe_sort_index(df, axis=0, level=None, ascending=True,
    inplace=False, kind='quicksort', na_position='last', sort_remaining=
    True, ignore_index=False, key=None):
    check_runtime_cols_unsupported(df, 'DataFrame.sort_index()')
    hwzb__jnck = dict(axis=axis, level=level, kind=kind, sort_remaining=
        sort_remaining, ignore_index=ignore_index, key=key)
    szrb__ldodx = dict(axis=0, level=None, kind='quicksort', sort_remaining
        =True, ignore_index=False, key=None)
    check_unsupported_args('DataFrame.sort_index', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_bool(ascending):
        raise BodoError(
            "DataFrame.sort_index(): 'ascending' parameter must be of type bool"
            )
    if not is_overload_bool(inplace):
        raise BodoError(
            "DataFrame.sort_index(): 'inplace' parameter must be of type bool")
    if not is_overload_constant_str(na_position) or get_overload_const_str(
        na_position) not in ('first', 'last'):
        raise_bodo_error(
            "DataFrame.sort_index(): 'na_position' should either be 'first' or 'last'"
            )

    def _impl(df, axis=0, level=None, ascending=True, inplace=False, kind=
        'quicksort', na_position='last', sort_remaining=True, ignore_index=
        False, key=None):
        return bodo.hiframes.pd_dataframe_ext.sort_values_dummy(df,
            '$_bodo_index_', ascending, inplace, na_position, None)
    return _impl


@overload_method(DataFrameType, 'rank', inline='always', no_unliteral=True)
def overload_dataframe_rank(df, axis=0, method='average', numeric_only=None,
    na_option='keep', ascending=True, pct=False):
    dvhz__hbzun = """def impl(df, axis=0, method='average', numeric_only=None, na_option='keep', ascending=True, pct=False):
"""
    zlzx__dvfjm = len(df.columns)
    data_args = ', '.join(
        'bodo.libs.array_kernels.rank(data_{}, method=method, na_option=na_option, ascending=ascending, pct=pct)'
        .format(i) for i in range(zlzx__dvfjm))
    for i in range(zlzx__dvfjm):
        dvhz__hbzun += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(dvhz__hbzun, df.columns, data_args, index)


@overload_method(DataFrameType, 'fillna', inline='always', no_unliteral=True)
def overload_dataframe_fillna(df, value=None, method=None, axis=None,
    inplace=False, limit=None, downcast=None):
    check_runtime_cols_unsupported(df, 'DataFrame.fillna()')
    hwzb__jnck = dict(limit=limit, downcast=downcast)
    szrb__ldodx = dict(limit=None, downcast=None)
    check_unsupported_args('DataFrame.fillna', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.fillna()')
    if not (is_overload_none(axis) or is_overload_zero(axis)):
        raise BodoError("DataFrame.fillna(): 'axis' argument not supported.")
    fxy__sqe = not is_overload_none(value)
    hxdi__zleva = not is_overload_none(method)
    if fxy__sqe and hxdi__zleva:
        raise BodoError(
            "DataFrame.fillna(): Cannot specify both 'value' and 'method'.")
    if not fxy__sqe and not hxdi__zleva:
        raise BodoError(
            "DataFrame.fillna(): Must specify one of 'value' and 'method'.")
    if fxy__sqe:
        judi__swd = 'value=value'
    else:
        judi__swd = 'method=method'
    data_args = [(f"df['{ibfb__ifl}'].fillna({judi__swd}, inplace=inplace)" if
        isinstance(ibfb__ifl, str) else
        f'df[{ibfb__ifl}].fillna({judi__swd}, inplace=inplace)') for
        ibfb__ifl in df.columns]
    dvhz__hbzun = """def impl(df, value=None, method=None, axis=None, inplace=False, limit=None, downcast=None):
"""
    if is_overload_true(inplace):
        dvhz__hbzun += '  ' + '  \n'.join(data_args) + '\n'
        unozl__xox = {}
        exec(dvhz__hbzun, {}, unozl__xox)
        impl = unozl__xox['impl']
        return impl
    else:
        return _gen_init_df(dvhz__hbzun, df.columns, ', '.join(uibz__fawu +
            '.values' for uibz__fawu in data_args))


@overload_method(DataFrameType, 'reset_index', inline='always',
    no_unliteral=True)
def overload_dataframe_reset_index(df, level=None, drop=False, inplace=
    False, col_level=0, col_fill='', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.reset_index()')
    hwzb__jnck = dict(col_level=col_level, col_fill=col_fill)
    szrb__ldodx = dict(col_level=0, col_fill='')
    check_unsupported_args('DataFrame.reset_index', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'reset_index')
    if not _is_all_levels(df, level):
        raise_bodo_error(
            'DataFrame.reset_index(): only dropping all index levels supported'
            )
    if not is_overload_constant_bool(drop):
        raise BodoError(
            "DataFrame.reset_index(): 'drop' parameter should be a constant boolean value"
            )
    if not is_overload_constant_bool(inplace):
        raise BodoError(
            "DataFrame.reset_index(): 'inplace' parameter should be a constant boolean value"
            )
    dvhz__hbzun = """def impl(df, level=None, drop=False, inplace=False, col_level=0, col_fill='', _bodo_transformed=False,):
"""
    dvhz__hbzun += (
        '  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(df), 1, None)\n'
        )
    drop = is_overload_true(drop)
    inplace = is_overload_true(inplace)
    columns = df.columns
    data_args = [
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}\n'.
        format(i, '' if inplace else '.copy()') for i in range(len(df.columns))
        ]
    if not drop:
        temk__wfk = 'index' if 'index' not in columns else 'level_0'
        index_names = get_index_names(df.index, 'DataFrame.reset_index()',
            temk__wfk)
        columns = index_names + columns
        if isinstance(df.index, MultiIndexType):
            dvhz__hbzun += """  m_index = bodo.hiframes.pd_index_ext.get_index_data(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
"""
            erubn__pltmj = ['m_index[{}]'.format(i) for i in range(df.index
                .nlevels)]
            data_args = erubn__pltmj + data_args
        else:
            vnog__wwo = (
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
                )
            data_args = [vnog__wwo] + data_args
    return _gen_init_df(dvhz__hbzun, columns, ', '.join(data_args), 'index')


def _is_all_levels(df, level):
    qwhz__fxwq = len(get_index_data_arr_types(df.index))
    return is_overload_none(level) or is_overload_constant_int(level
        ) and get_overload_const_int(level
        ) == 0 and qwhz__fxwq == 1 or is_overload_constant_list(level
        ) and list(get_overload_const_list(level)) == list(range(qwhz__fxwq))


@overload_method(DataFrameType, 'dropna', inline='always', no_unliteral=True)
def overload_dataframe_dropna(df, axis=0, how='any', thresh=None, subset=
    None, inplace=False):
    check_runtime_cols_unsupported(df, 'DataFrame.dropna()')
    if not is_overload_constant_bool(inplace) or is_overload_true(inplace):
        raise BodoError('DataFrame.dropna(): inplace=True is not supported')
    if not is_overload_zero(axis):
        raise_bodo_error(f'df.dropna(): only axis=0 supported')
    ensure_constant_values('dropna', 'how', how, ('any', 'all'))
    if is_overload_none(subset):
        fie__gpvz = list(range(len(df.columns)))
    elif not is_overload_constant_list(subset):
        raise_bodo_error(
            f'df.dropna(): subset argument should a constant list, not {subset}'
            )
    else:
        tfcke__uqzj = get_overload_const_list(subset)
        fie__gpvz = []
        for sizs__fupa in tfcke__uqzj:
            if sizs__fupa not in df.column_index:
                raise_bodo_error(
                    f"df.dropna(): column '{sizs__fupa}' not in data frame columns {df}"
                    )
            fie__gpvz.append(df.column_index[sizs__fupa])
    zlzx__dvfjm = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(zlzx__dvfjm))
    dvhz__hbzun = (
        "def impl(df, axis=0, how='any', thresh=None, subset=None, inplace=False):\n"
        )
    for i in range(zlzx__dvfjm):
        dvhz__hbzun += (
            '  data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})\n'
            .format(i))
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    dvhz__hbzun += (
        """  ({0}, index_arr) = bodo.libs.array_kernels.dropna(({0}, {1}), how, thresh, ({2},))
"""
        .format(data_args, index, ', '.join(str(a) for a in fie__gpvz)))
    dvhz__hbzun += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return _gen_init_df(dvhz__hbzun, df.columns, data_args, 'index')


@overload_method(DataFrameType, 'drop', inline='always', no_unliteral=True)
def overload_dataframe_drop(df, labels=None, axis=0, index=None, columns=
    None, level=None, inplace=False, errors='raise', _bodo_transformed=False):
    check_runtime_cols_unsupported(df, 'DataFrame.drop()')
    hwzb__jnck = dict(index=index, level=level, errors=errors)
    szrb__ldodx = dict(index=None, level=None, errors='raise')
    check_unsupported_args('DataFrame.drop', hwzb__jnck, szrb__ldodx,
        package_name='pandas', module_name='DataFrame')
    handle_inplace_df_type_change(inplace, _bodo_transformed, 'drop')
    if not is_overload_constant_bool(inplace):
        raise_bodo_error(
            "DataFrame.drop(): 'inplace' parameter should be a constant bool")
    if not is_overload_none(labels):
        if not is_overload_none(columns):
            raise BodoError(
                "Dataframe.drop(): Cannot specify both 'labels' and 'columns'")
        if not is_overload_constant_int(axis) or get_overload_const_int(axis
            ) != 1:
            raise_bodo_error('DataFrame.drop(): only axis=1 supported')
        if is_overload_constant_str(labels):
            midi__kqgwl = get_overload_const_str(labels),
        elif is_overload_constant_list(labels):
            midi__kqgwl = get_overload_const_list(labels)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    else:
        if is_overload_none(columns):
            raise BodoError(
                "DataFrame.drop(): Need to specify at least one of 'labels' or 'columns'"
                )
        if is_overload_constant_str(columns):
            midi__kqgwl = get_overload_const_str(columns),
        elif is_overload_constant_list(columns):
            midi__kqgwl = get_overload_const_list(columns)
        else:
            raise_bodo_error(
                'constant list of columns expected for labels in DataFrame.drop()'
                )
    for ibfb__ifl in midi__kqgwl:
        if ibfb__ifl not in df.columns:
            raise_bodo_error(
                'DataFrame.drop(): column {} not in DataFrame columns {}'.
                format(ibfb__ifl, df.columns))
    if len(set(midi__kqgwl)) == len(df.columns):
        raise BodoError('DataFrame.drop(): Dropping all columns not supported.'
            )
    inplace = is_overload_true(inplace)
    jixx__ebagc = tuple(ibfb__ifl for ibfb__ifl in df.columns if ibfb__ifl
         not in midi__kqgwl)
    data_args = ', '.join(
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}){}'.
        format(df.column_index[ibfb__ifl], '.copy()' if not inplace else ''
        ) for ibfb__ifl in jixx__ebagc)
    dvhz__hbzun = (
        'def impl(df, labels=None, axis=0, index=None, columns=None,\n')
    dvhz__hbzun += (
        "     level=None, inplace=False, errors='raise', _bodo_transformed=False):\n"
        )
    index = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
    return _gen_init_df(dvhz__hbzun, jixx__ebagc, data_args, index)


@overload_method(DataFrameType, 'append', inline='always', no_unliteral=True)
def overload_dataframe_append(df, other, ignore_index=False,
    verify_integrity=False, sort=None):
    check_runtime_cols_unsupported(df, 'DataFrame.append()')
    check_runtime_cols_unsupported(other, 'DataFrame.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.append()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(other,
        'DataFrame.append()')
    if isinstance(other, DataFrameType):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df, other), ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.BaseTuple):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat((df,) + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    if isinstance(other, types.List) and isinstance(other.dtype, DataFrameType
        ):
        return (lambda df, other, ignore_index=False, verify_integrity=
            False, sort=None: pd.concat([df] + other, ignore_index=
            ignore_index, verify_integrity=verify_integrity))
    raise BodoError(
        'invalid df.append() input. Only dataframe and list/tuple of dataframes supported'
        )


@overload_method(DataFrameType, 'sample', inline='always', no_unliteral=True)
def overload_dataframe_sample(df, n=None, frac=None, replace=False, weights
    =None, random_state=None, axis=None, ignore_index=False):
    check_runtime_cols_unsupported(df, 'DataFrame.sample()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df,
        'DataFrame.sample()')
    hwzb__jnck = dict(random_state=random_state, weights=weights, axis=axis,
        ignore_index=ignore_index)
    fhhmx__wtdl = dict(random_state=None, weights=None, axis=None,
        ignore_index=False)
    check_unsupported_args('DataFrame.sample', hwzb__jnck, fhhmx__wtdl,
        package_name='pandas', module_name='DataFrame')
    if not is_overload_none(n) and not is_overload_none(frac):
        raise BodoError(
            'DataFrame.sample(): only one of n and frac option can be selected'
            )
    zlzx__dvfjm = len(df.columns)
    data_args = ', '.join('data_{}'.format(i) for i in range(zlzx__dvfjm))
    dsle__rwcv = ', '.join('rhs_data_{}'.format(i) for i in range(zlzx__dvfjm))
    dvhz__hbzun = """def impl(df, n=None, frac=None, replace=False, weights=None, random_state=None, axis=None, ignore_index=False):
"""
    dvhz__hbzun += '  if (frac == 1 or n == len(df)) and not replace:\n'
    dvhz__hbzun += (
        '    return bodo.allgatherv(bodo.random_shuffle(df), False)\n')
    for i in range(zlzx__dvfjm):
        dvhz__hbzun += (
            """  rhs_data_{0} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0})
"""
            .format(i))
    dvhz__hbzun += '  if frac is None:\n'
    dvhz__hbzun += '    frac_d = -1.0\n'
    dvhz__hbzun += '  else:\n'
    dvhz__hbzun += '    frac_d = frac\n'
    dvhz__hbzun += '  if n is None:\n'
    dvhz__hbzun += '    n_i = 0\n'
    dvhz__hbzun += '  else:\n'
    dvhz__hbzun += '    n_i = n\n'
    index = (
        'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))'
        )
    dvhz__hbzun += f"""  ({data_args},), index_arr = bodo.libs.array_kernels.sample_table_operation(({dsle__rwcv},), {index}, n_i, frac_d, replace)
"""
    dvhz__hbzun += (
        '  index = bodo.utils.conversion.index_from_array(index_arr)\n')
    return bodo.hiframes.dataframe_impl._gen_init_df(dvhz__hbzun, df.
        columns, data_args, 'index')


@numba.njit
def _sizeof_fmt(num, size_qualifier=''):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f'{num:3.1f}{size_qualifier} {x}'
        num /= 1024.0
    return f'{num:3.1f}{size_qualifier} PB'


@overload_method(DataFrameType, 'info', no_unliteral=True)
def overload_dataframe_info(df, verbose=None, buf=None, max_cols=None,
    memory_usage=None, show_counts=None, null_counts=None):
    check_runtime_cols_unsupported(df, 'DataFrame.info()')
    zzfx__trn = {'verbose': verbose, 'buf': buf, 'max_cols': max_cols,
        'memory_usage': memory_usage, 'show_counts': show_counts,
        'null_counts': null_counts}
    nwf__nku = {'verbose': None, 'buf': None, 'max_cols': None,
        'memory_usage': None, 'show_counts': None, 'null_counts': None}
    check_unsupported_args('DataFrame.info', zzfx__trn, nwf__nku,
        package_name='pandas', module_name='DataFrame')
    cchyy__jsmbo = f"<class '{str(type(df)).split('.')[-1]}"
    if len(df.columns) == 0:

        def _info_impl(df, verbose=None, buf=None, max_cols=None,
            memory_usage=None, show_counts=None, null_counts=None):
            qqmyg__mvolr = cchyy__jsmbo + '\n'
            qqmyg__mvolr += 'Index: 0 entries\n'
            qqmyg__mvolr += 'Empty DataFrame'
            print(qqmyg__mvolr)
        return _info_impl
    else:
        dvhz__hbzun = """def _info_impl(df, verbose=None, buf=None, max_cols=None, memory_usage=None, show_counts=None, null_counts=None): #pragma: no cover
"""
        dvhz__hbzun += '    ncols = df.shape[1]\n'
        dvhz__hbzun += f'    lines = "{cchyy__jsmbo}\\n"\n'
        dvhz__hbzun += f'    lines += "{df.index}: "\n'
        dvhz__hbzun += (
            '    index = bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)\n'
            )
        if isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType):
            dvhz__hbzun += """    lines += f"{len(index)} entries, {index.start} to {index.stop-1}\\n\"
"""
        elif isinstance(df.index, bodo.hiframes.pd_index_ext.StringIndexType):
            dvhz__hbzun += """    lines += f"{len(index)} entries, {index[0]} to {index[len(index)-1]}\\n\"
"""
        else:
            dvhz__hbzun += (
                '    lines += f"{len(index)} entries, {index[0]} to {index[-1]}\\n"\n'
                )
        dvhz__hbzun += (
            '    lines += f"Data columns (total {ncols} columns):\\n"\n')
        dvhz__hbzun += (
            f'    space = {max(len(str(k)) for k in df.columns) + 1}\n')
        dvhz__hbzun += '    column_width = max(space, 7)\n'
        dvhz__hbzun += '    column= "Column"\n'
        dvhz__hbzun += '    underl= "------"\n'
        dvhz__hbzun += (
            '    lines += f"#   {column:<{column_width}} Non-Null Count  Dtype\\n"\n'
            )
        dvhz__hbzun += (
            '    lines += f"--- {underl:<{column_width}} --------------  -----\\n"\n'
            )
        dvhz__hbzun += '    mem_size = 0\n'
        dvhz__hbzun += (
            '    col_name = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        dvhz__hbzun += """    non_null_count = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)
"""
        dvhz__hbzun += (
            '    col_dtype = bodo.libs.str_arr_ext.pre_alloc_string_array(ncols, -1)\n'
            )
        awnb__wvlc = dict()
        for i in range(len(df.columns)):
            dvhz__hbzun += f"""    non_null_count[{i}] = str(bodo.libs.array_ops.array_op_count(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})))
"""
            ympc__bni = f'{df.data[i].dtype}'
            if isinstance(df.data[i], bodo.CategoricalArrayType):
                ympc__bni = 'category'
            elif isinstance(df.data[i], bodo.IntegerArrayType):
                soxy__pvbk = bodo.libs.int_arr_ext.IntDtype(df.data[i].dtype
                    ).name
                ympc__bni = f'{soxy__pvbk[:-7]}'
            dvhz__hbzun += f'    col_dtype[{i}] = "{ympc__bni}"\n'
            if ympc__bni in awnb__wvlc:
                awnb__wvlc[ympc__bni] += 1
            else:
                awnb__wvlc[ympc__bni] = 1
            dvhz__hbzun += f'    col_name[{i}] = "{df.columns[i]}"\n'
            dvhz__hbzun += f"""    mem_size += bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).nbytes
"""
        dvhz__hbzun += """    column_info = [f'{i:^3} {name:<{column_width}} {count} non-null      {dtype}' for i, (name, count, dtype) in enumerate(zip(col_name, non_null_count, col_dtype))]
"""
        dvhz__hbzun += '    for i in column_info:\n'
        dvhz__hbzun += "        lines += f'{i}\\n'\n"
        jgy__wtpv = ', '.join(f'{k}({awnb__wvlc[k]})' for k in sorted(
            awnb__wvlc))
        dvhz__hbzun += f"    lines += 'dtypes: {jgy__wtpv}\\n'\n"
        dvhz__hbzun += '    mem_size += df.index.nbytes\n'
        dvhz__hbzun += '    total_size = _sizeof_fmt(mem_size)\n'
        dvhz__hbzun += "    lines += f'memory usage: {total_size}'\n"
        dvhz__hbzun += '    print(lines)\n'
        unozl__xox = {}
        exec(dvhz__hbzun, {'_sizeof_fmt': _sizeof_fmt, 'pd': pd, 'bodo':
            bodo, 'np': np}, unozl__xox)
        _info_impl = unozl__xox['_info_impl']
        return _info_impl


@overload_method(DataFrameType, 'memory_usage', inline='always',
    no_unliteral=True)
def overload_dataframe_memory_usage(df, index=True, deep=False):
    check_runtime_cols_unsupported(df, 'DataFrame.memory_usage()')
    dvhz__hbzun = 'def impl(df, index=True, deep=False):\n'
    jzfbo__biv = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df).nbytes')
    fkoix__slgbt = is_overload_true(index)
    columns = df.columns
    if fkoix__slgbt:
        columns = ('Index',) + columns
    if len(columns) == 0:
        eovtm__zrish = ()
    elif all(isinstance(ibfb__ifl, int) for ibfb__ifl in columns):
        eovtm__zrish = np.array(columns, 'int64')
    elif all(isinstance(ibfb__ifl, str) for ibfb__ifl in columns):
        eovtm__zrish = pd.array(columns, 'string')
    else:
        eovtm__zrish = columns
    if df.is_table_format and len(df.columns) > 0:
        zpru__exhl = int(fkoix__slgbt)
        vcbh__wjibz = len(columns)
        dvhz__hbzun += f'  nbytes_arr = np.empty({vcbh__wjibz}, np.int64)\n'
        dvhz__hbzun += (
            '  table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)\n'
            )
        dvhz__hbzun += f"""  bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, {zpru__exhl})
"""
        if fkoix__slgbt:
            dvhz__hbzun += f'  nbytes_arr[0] = {jzfbo__biv}\n'
        dvhz__hbzun += f"""  return bodo.hiframes.pd_series_ext.init_series(nbytes_arr, pd.Index(column_vals), None)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        if fkoix__slgbt:
            data = f'{jzfbo__biv},{data}'
        else:
            mvg__sza = ',' if len(columns) == 1 else ''
            data = f'{data}{mvg__sza}'
        dvhz__hbzun += f"""  return bodo.hiframes.pd_series_ext.init_series(({data}), pd.Index(column_vals), None)
"""
    unozl__xox = {}
    exec(dvhz__hbzun, {'bodo': bodo, 'np': np, 'pd': pd, 'column_vals':
        eovtm__zrish}, unozl__xox)
    impl = unozl__xox['impl']
    return impl


@overload(pd.read_excel, no_unliteral=True)
def overload_read_excel(io, sheet_name=0, header=0, names=None, index_col=
    None, usecols=None, squeeze=False, dtype=None, engine=None, converters=
    None, true_values=None, false_values=None, skiprows=None, nrows=None,
    na_values=None, keep_default_na=True, na_filter=True, verbose=False,
    parse_dates=False, date_parser=None, thousands=None, comment=None,
    skipfooter=0, convert_float=True, mangle_dupe_cols=True, _bodo_df_type=None
    ):
    df_type = _bodo_df_type.instance_type
    vihit__bptpy = 'read_excel_df{}'.format(next_label())
    setattr(types, vihit__bptpy, df_type)
    sua__dhv = False
    if is_overload_constant_list(parse_dates):
        sua__dhv = get_overload_const_list(parse_dates)
    vnk__zoe = ', '.join(["'{}':{}".format(cname, _get_pd_dtype_str(t)) for
        cname, t in zip(df_type.columns, df_type.data)])
    dvhz__hbzun = f"""
def impl(
    io,
    sheet_name=0,
    header=0,
    names=None,
    index_col=None,
    usecols=None,
    squeeze=False,
    dtype=None,
    engine=None,
    converters=None,
    true_values=None,
    false_values=None,
    skiprows=None,
    nrows=None,
    na_values=None,
    keep_default_na=True,
    na_filter=True,
    verbose=False,
    parse_dates=False,
    date_parser=None,
    thousands=None,
    comment=None,
    skipfooter=0,
    convert_float=True,
    mangle_dupe_cols=True,
    _bodo_df_type=None,
):
    with numba.objmode(df="{vihit__bptpy}"):
        df = pd.read_excel(
            io=io,
            sheet_name=sheet_name,
            header=header,
            names={list(df_type.columns)},
            index_col=index_col,
            usecols=usecols,
            squeeze=squeeze,
            dtype={{{vnk__zoe}}},
            engine=engine,
            converters=converters,
            true_values=true_values,
            false_values=false_values,
            skiprows=skiprows,
            nrows=nrows,
            na_values=na_values,
            keep_default_na=keep_default_na,
            na_filter=na_filter,
            verbose=verbose,
            parse_dates={sua__dhv},
            date_parser=date_parser,
            thousands=thousands,
            comment=comment,
            skipfooter=skipfooter,
            convert_float=convert_float,
            mangle_dupe_cols=mangle_dupe_cols,
        )
    return df
"""
    unozl__xox = {}
    exec(dvhz__hbzun, globals(), unozl__xox)
    impl = unozl__xox['impl']
    return impl


def overload_dataframe_plot(df, x=None, y=None, kind='line', figsize=None,
    xlabel=None, ylabel=None, title=None, legend=True, fontsize=None,
    xticks=None, yticks=None, ax=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError as zbo__xhegc:
        raise BodoError('df.plot needs matplotllib which is not installed.')
    dvhz__hbzun = (
        "def impl(df, x=None, y=None, kind='line', figsize=None, xlabel=None, \n"
        )
    dvhz__hbzun += (
        '    ylabel=None, title=None, legend=True, fontsize=None, \n')
    dvhz__hbzun += '    xticks=None, yticks=None, ax=None):\n'
    if is_overload_none(ax):
        dvhz__hbzun += '   fig, ax = plt.subplots()\n'
    else:
        dvhz__hbzun += '   fig = ax.get_figure()\n'
    if not is_overload_none(figsize):
        dvhz__hbzun += '   fig.set_figwidth(figsize[0])\n'
        dvhz__hbzun += '   fig.set_figheight(figsize[1])\n'
    if is_overload_none(xlabel):
        dvhz__hbzun += '   xlabel = x\n'
    dvhz__hbzun += '   ax.set_xlabel(xlabel)\n'
    if is_overload_none(ylabel):
        dvhz__hbzun += '   ylabel = y\n'
    else:
        dvhz__hbzun += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(title):
        dvhz__hbzun += '   ax.set_title(title)\n'
    if not is_overload_none(fontsize):
        dvhz__hbzun += '   ax.tick_params(labelsize=fontsize)\n'
    kind = get_overload_const_str(kind)
    if kind == 'line':
        if is_overload_none(x) and is_overload_none(y):
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    dvhz__hbzun += (
                        f'   ax.plot(df.iloc[:, {i}], label=df.columns[{i}])\n'
                        )
        elif is_overload_none(x):
            dvhz__hbzun += '   ax.plot(df[y], label=y)\n'
        elif is_overload_none(y):
            zbfrf__zdyqe = get_overload_const_str(x)
            qluyw__rnhdl = df.columns.index(zbfrf__zdyqe)
            for i in range(len(df.columns)):
                if isinstance(df.data[i], (types.Array, IntegerArrayType)
                    ) and isinstance(df.data[i].dtype, (types.Integer,
                    types.Float)):
                    if qluyw__rnhdl != i:
                        dvhz__hbzun += f"""   ax.plot(df[x], df.iloc[:, {i}], label=df.columns[{i}])
"""
        else:
            dvhz__hbzun += '   ax.plot(df[x], df[y], label=y)\n'
    elif kind == 'scatter':
        legend = False
        dvhz__hbzun += '   ax.scatter(df[x], df[y], s=20)\n'
        dvhz__hbzun += '   ax.set_ylabel(ylabel)\n'
    if not is_overload_none(xticks):
        dvhz__hbzun += '   ax.set_xticks(xticks)\n'
    if not is_overload_none(yticks):
        dvhz__hbzun += '   ax.set_yticks(yticks)\n'
    if is_overload_true(legend):
        dvhz__hbzun += '   ax.legend()\n'
    dvhz__hbzun += '   return ax\n'
    unozl__xox = {}
    exec(dvhz__hbzun, {'bodo': bodo, 'plt': plt}, unozl__xox)
    impl = unozl__xox['impl']
    return impl


@lower_builtin('df.plot', DataFrameType, types.VarArg(types.Any))
def dataframe_plot_low(context, builder, sig, args):
    impl = overload_dataframe_plot(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def is_df_values_numpy_supported_dftyp(df_typ):
    for axafs__qkicv in df_typ.data:
        if not (isinstance(axafs__qkicv, (IntegerArrayType,
            FloatingArrayType)) or isinstance(axafs__qkicv.dtype, types.
            Number) or axafs__qkicv.dtype in (bodo.datetime64ns, bodo.
            timedelta64ns)):
            return False
    return True


def typeref_to_type(v):
    if isinstance(v, types.BaseTuple):
        return types.BaseTuple.from_types(tuple(typeref_to_type(a) for a in v))
    return v.instance_type if isinstance(v, (types.TypeRef, types.NumberClass)
        ) else v


def _install_typer_for_type(type_name, typ):

    @type_callable(typ)
    def type_call_type(context):

        def typer(*args, **kws):
            args = tuple(typeref_to_type(v) for v in args)
            kws = {name: typeref_to_type(v) for name, v in kws.items()}
            return types.TypeRef(typ(*args, **kws))
        return typer
    no_side_effect_call_tuples.add((type_name, bodo))
    no_side_effect_call_tuples.add((typ,))


def _install_type_call_typers():
    for type_name in bodo_types_with_params:
        typ = getattr(bodo, type_name)
        _install_typer_for_type(type_name, typ)


_install_type_call_typers()


def set_df_col(df, cname, arr, inplace):
    df[cname] = arr


@infer_global(set_df_col)
class SetDfColInfer(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        assert not kws
        assert len(args) == 4
        assert isinstance(args[1], types.Literal)
        pibs__shchb = args[0]
        sbuz__intc = args[1].literal_value
        val = args[2]
        assert val != types.unknown
        teuoh__vrb = pibs__shchb
        check_runtime_cols_unsupported(pibs__shchb, 'set_df_col()')
        if isinstance(pibs__shchb, DataFrameType):
            index = pibs__shchb.index
            if len(pibs__shchb.columns) == 0:
                index = bodo.hiframes.pd_index_ext.RangeIndexType(types.none)
            if isinstance(val, SeriesType):
                if len(pibs__shchb.columns) == 0:
                    index = val.index
                val = val.data
            if is_pd_index_type(val):
                val = bodo.utils.typing.get_index_data_arr_types(val)[0]
            if isinstance(val, types.List):
                val = dtype_to_array_type(val.dtype)
            if is_overload_constant_str(val) or val == types.unicode_type:
                val = bodo.dict_str_arr_type
            elif not is_array_typ(val):
                val = dtype_to_array_type(val)
            if sbuz__intc in pibs__shchb.columns:
                jixx__ebagc = pibs__shchb.columns
                cux__mqb = pibs__shchb.columns.index(sbuz__intc)
                lkolt__byv = list(pibs__shchb.data)
                lkolt__byv[cux__mqb] = val
                lkolt__byv = tuple(lkolt__byv)
            else:
                jixx__ebagc = pibs__shchb.columns + (sbuz__intc,)
                lkolt__byv = pibs__shchb.data + (val,)
            teuoh__vrb = DataFrameType(lkolt__byv, index, jixx__ebagc,
                pibs__shchb.dist, pibs__shchb.is_table_format)
        return teuoh__vrb(*args)


SetDfColInfer.prefer_literal = True


def __bodosql_replace_columns_dummy(df, col_names_to_replace,
    cols_to_replace_with):
    for i in range(len(col_names_to_replace)):
        df[col_names_to_replace[i]] = cols_to_replace_with[i]


@infer_global(__bodosql_replace_columns_dummy)
class BodoSQLReplaceColsInfer(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        assert not kws
        assert len(args) == 3
        assert is_overload_constant_tuple(args[1])
        assert isinstance(args[2], types.BaseTuple)
        uttht__xul = args[0]
        assert isinstance(uttht__xul, DataFrameType) and len(uttht__xul.columns
            ) > 0, 'Error while typechecking __bodosql_replace_columns_dummy: we should only generate a call __bodosql_replace_columns_dummy if the input dataframe'
        col_names_to_replace = get_overload_const_tuple(args[1])
        pct__tnrk = args[2]
        assert len(col_names_to_replace) == len(pct__tnrk
            ), 'Error while typechecking __bodosql_replace_columns_dummy: the tuple of column indicies to replace should be equal to the number of columns to replace them with'
        assert len(col_names_to_replace) <= len(uttht__xul.columns
            ), 'Error while typechecking __bodosql_replace_columns_dummy: The number of indicies provided should be less than or equal to the number of columns in the input dataframe'
        for col_name in col_names_to_replace:
            assert col_name in uttht__xul.columns, 'Error while typechecking __bodosql_replace_columns_dummy: All columns specified to be replaced should already be present in input dataframe'
        check_runtime_cols_unsupported(uttht__xul,
            '__bodosql_replace_columns_dummy()')
        index = uttht__xul.index
        jixx__ebagc = uttht__xul.columns
        lkolt__byv = list(uttht__xul.data)
        for i in range(len(col_names_to_replace)):
            col_name = col_names_to_replace[i]
            famrl__ldj = pct__tnrk[i]
            assert isinstance(famrl__ldj, SeriesType
                ), 'Error while typechecking __bodosql_replace_columns_dummy: the values to replace the columns with are expected to be series'
            if isinstance(famrl__ldj, SeriesType):
                famrl__ldj = famrl__ldj.data
            boqi__fvt = uttht__xul.column_index[col_name]
            lkolt__byv[boqi__fvt] = famrl__ldj
        lkolt__byv = tuple(lkolt__byv)
        teuoh__vrb = DataFrameType(lkolt__byv, index, jixx__ebagc,
            uttht__xul.dist, uttht__xul.is_table_format)
        return teuoh__vrb(*args)


BodoSQLReplaceColsInfer.prefer_literal = True


def _parse_query_expr(expr, env, columns, cleaned_columns, index_name=None,
    join_cleaned_cols=()):
    fyyjw__ajg = {}

    def _rewrite_membership_op(self, node, left, right):
        nmqq__umj = node.op
        op = self.visit(nmqq__umj)
        return op, nmqq__umj, left, right

    def _maybe_evaluate_binop(self, op, op_class, lhs, rhs, eval_in_python=
        ('in', 'not in'), maybe_eval_in_python=('==', '!=', '<', '>', '<=',
        '>=')):
        res = op(lhs, rhs)
        return res
    xit__mfegn = []


    class NewFuncNode(pd.core.computation.ops.FuncNode):

        def __init__(self, name):
            if (name not in pd.core.computation.ops.MATHOPS or pd.core.
                computation.check._NUMEXPR_INSTALLED and pd.core.
                computation.check_NUMEXPR_VERSION < pd.core.computation.ops
                .LooseVersion('2.6.9') and name in ('floor', 'ceil')):
                if name not in xit__mfegn:
                    raise BodoError('"{0}" is not a supported function'.
                        format(name))
            self.name = name
            if name in xit__mfegn:
                self.func = name
            else:
                self.func = getattr(np, name)

        def __call__(self, *args):
            return pd.core.computation.ops.MathCall(self, args)

        def __repr__(self):
            return pd.io.formats.printing.pprint_thing('(' + self.name + ')')

    def visit_Attribute(self, node, **kwargs):
        qajs__lrdt = node.attr
        value = node.value
        tjxx__rdj = pd.core.computation.ops.LOCAL_TAG
        if qajs__lrdt in ('str', 'dt'):
            try:
                lbdv__hugf = str(self.visit(value))
            except pd.core.computation.ops.UndefinedVariableError as qnmle__ygrn:
                col_name = qnmle__ygrn.args[0].split("'")[1]
                raise BodoError(
                    'df.query(): column {} is not found in dataframe columns {}'
                    .format(col_name, columns))
        else:
            lbdv__hugf = str(self.visit(value))
        onrvw__wupnr = lbdv__hugf, qajs__lrdt
        if onrvw__wupnr in join_cleaned_cols:
            qajs__lrdt = join_cleaned_cols[onrvw__wupnr]
        name = lbdv__hugf + '.' + qajs__lrdt
        if name.startswith(tjxx__rdj):
            name = name[len(tjxx__rdj):]
        if qajs__lrdt in ('str', 'dt'):
            smxuf__luwr = columns[cleaned_columns.index(lbdv__hugf)]
            fyyjw__ajg[smxuf__luwr] = lbdv__hugf
            self.env.scope[name] = 0
            return self.term_type(tjxx__rdj + name, self.env)
        xit__mfegn.append(name)
        return NewFuncNode(name)

    def __str__(self):
        if isinstance(self.value, list):
            return '{}'.format(self.value)
        if isinstance(self.value, str):
            return "'{}'".format(self.value)
        return pd.io.formats.printing.pprint_thing(self.name)

    def math__str__(self):
        if self.op in xit__mfegn:
            return pd.io.formats.printing.pprint_thing('{0}({1})'.format(
                self.op, ','.join(map(str, self.operands))))
        iuz__uqtan = map(lambda a:
            'bodo.hiframes.pd_series_ext.get_series_data({})'.format(str(a)
            ), self.operands)
        op = 'np.{}'.format(self.op)
        sbuz__intc = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len({}), 1, None)'
            .format(str(self.operands[0])))
        return pd.io.formats.printing.pprint_thing(
            'bodo.hiframes.pd_series_ext.init_series({0}({1}), {2})'.format
            (op, ','.join(iuz__uqtan), sbuz__intc))

    def op__str__(self):
        wynq__uddat = ('({0})'.format(pd.io.formats.printing.pprint_thing(
            xernz__zbchg)) for xernz__zbchg in self.operands)
        if self.op == 'in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_isin_dummy({})'.format(
                ', '.join(wynq__uddat)))
        if self.op == 'not in':
            return pd.io.formats.printing.pprint_thing(
                'bodo.hiframes.pd_dataframe_ext.val_notin_dummy({})'.format
                (', '.join(wynq__uddat)))
        return pd.io.formats.printing.pprint_thing(' {0} '.format(self.op).
            join(wynq__uddat))
    cms__nitkg = (pd.core.computation.expr.BaseExprVisitor.
        _rewrite_membership_op)
    wbsew__mrp = pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop
    yga__qhkv = pd.core.computation.expr.BaseExprVisitor.visit_Attribute
    kbb__buaqh = (pd.core.computation.expr.BaseExprVisitor.
        _maybe_downcast_constants)
    bmdy__bmfwi = pd.core.computation.ops.Term.__str__
    ufoh__vtk = pd.core.computation.ops.MathCall.__str__
    sbc__wktbw = pd.core.computation.ops.Op.__str__
    bzp__urqav = pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops
    try:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            _rewrite_membership_op)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            _maybe_evaluate_binop)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = (
            visit_Attribute)
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = lambda self, left, right: (left, right)
        pd.core.computation.ops.Term.__str__ = __str__
        pd.core.computation.ops.MathCall.__str__ = math__str__
        pd.core.computation.ops.Op.__str__ = op__str__
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (lambda
            self: None)
        nma__clkv = pd.core.computation.expr.Expr(expr, env=env)
        uvoz__oct = str(nma__clkv)
    except pd.core.computation.ops.UndefinedVariableError as qnmle__ygrn:
        if not is_overload_none(index_name) and get_overload_const_str(
            index_name) == qnmle__ygrn.args[0].split("'")[1]:
            raise BodoError(
                "df.query(): Refering to named index ('{}') by name is not supported"
                .format(get_overload_const_str(index_name)))
        else:
            raise BodoError(f'df.query(): undefined variable, {qnmle__ygrn}')
    finally:
        pd.core.computation.expr.BaseExprVisitor._rewrite_membership_op = (
            cms__nitkg)
        pd.core.computation.expr.BaseExprVisitor._maybe_evaluate_binop = (
            wbsew__mrp)
        pd.core.computation.expr.BaseExprVisitor.visit_Attribute = yga__qhkv
        (pd.core.computation.expr.BaseExprVisitor._maybe_downcast_constants
            ) = kbb__buaqh
        pd.core.computation.ops.Term.__str__ = bmdy__bmfwi
        pd.core.computation.ops.MathCall.__str__ = ufoh__vtk
        pd.core.computation.ops.Op.__str__ = sbc__wktbw
        pd.core.computation.ops.BinOp._disallow_scalar_only_bool_ops = (
            bzp__urqav)
    mtky__dci = pd.core.computation.parsing.clean_column_name
    fyyjw__ajg.update({ibfb__ifl: mtky__dci(ibfb__ifl) for ibfb__ifl in
        columns if mtky__dci(ibfb__ifl) in nma__clkv.names})
    return nma__clkv, uvoz__oct, fyyjw__ajg


class DataFrameTupleIterator(types.SimpleIteratorType):

    def __init__(self, col_names, arr_typs):
        self.array_types = arr_typs
        self.col_names = col_names
        vxdx__zen = ['{}={}'.format(col_names[i], arr_typs[i]) for i in
            range(len(col_names))]
        name = 'itertuples({})'.format(','.join(vxdx__zen))
        wiw__ehcjl = namedtuple('Pandas', col_names)
        xfzbu__mhl = types.NamedTuple([_get_series_dtype(a) for a in
            arr_typs], wiw__ehcjl)
        super(DataFrameTupleIterator, self).__init__(name, xfzbu__mhl)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


def _get_series_dtype(arr_typ):
    if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
        return pd_timestamp_tz_naive_type
    return arr_typ.dtype


def get_itertuples():
    pass


@infer_global(get_itertuples)
class TypeIterTuples(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) % 2 == 0, 'name and column pairs expected'
        col_names = [a.literal_value for a in args[:len(args) // 2]]
        oeurl__vos = [if_series_to_array_type(a) for a in args[len(args) // 2:]
            ]
        assert 'Index' not in col_names[0]
        col_names = ['Index'] + col_names
        oeurl__vos = [types.Array(types.int64, 1, 'C')] + oeurl__vos
        tfdgl__rtvr = DataFrameTupleIterator(col_names, oeurl__vos)
        return tfdgl__rtvr(*args)


TypeIterTuples.prefer_literal = True


@register_model(DataFrameTupleIterator)
class DataFrameTupleIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ylde__ytqv = [('index', types.EphemeralPointer(types.uintp))] + [(
            'array{}'.format(i), arr) for i, arr in enumerate(fe_type.
            array_types[1:])]
        super(DataFrameTupleIteratorModel, self).__init__(dmm, fe_type,
            ylde__ytqv)

    def from_return(self, builder, value):
        return value


@lower_builtin(get_itertuples, types.VarArg(types.Any))
def get_itertuples_impl(context, builder, sig, args):
    ntee__bbmyd = args[len(args) // 2:]
    rxgsi__fiig = sig.args[len(sig.args) // 2:]
    cck__lwcd = context.make_helper(builder, sig.return_type)
    xnt__hlff = context.get_constant(types.intp, 0)
    ewu__kwi = cgutils.alloca_once_value(builder, xnt__hlff)
    cck__lwcd.index = ewu__kwi
    for i, arr in enumerate(ntee__bbmyd):
        setattr(cck__lwcd, 'array{}'.format(i), arr)
    for arr, arr_typ in zip(ntee__bbmyd, rxgsi__fiig):
        context.nrt.incref(builder, arr_typ, arr)
    res = cck__lwcd._getvalue()
    return impl_ret_new_ref(context, builder, sig.return_type, res)


@lower_builtin('getiter', DataFrameTupleIterator)
def getiter_itertuples(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', DataFrameTupleIterator)
@iternext_impl(RefType.UNTRACKED)
def iternext_itertuples(context, builder, sig, args, result):
    szvib__syuv, = sig.args
    eckb__missq, = args
    cck__lwcd = context.make_helper(builder, szvib__syuv, value=eckb__missq)
    zsqd__huzdq = signature(types.intp, szvib__syuv.array_types[1])
    zdsex__ykq = context.compile_internal(builder, lambda a: len(a),
        zsqd__huzdq, [cck__lwcd.array0])
    index = builder.load(cck__lwcd.index)
    ubu__ozdf = builder.icmp_signed('<', index, zdsex__ykq)
    result.set_valid(ubu__ozdf)
    with builder.if_then(ubu__ozdf):
        values = [index]
        for i, arr_typ in enumerate(szvib__syuv.array_types[1:]):
            oxjow__pepk = getattr(cck__lwcd, 'array{}'.format(i))
            if arr_typ == types.Array(types.NPDatetime('ns'), 1, 'C'):
                qkb__zbj = signature(pd_timestamp_tz_naive_type, arr_typ,
                    types.intp)
                val = context.compile_internal(builder, lambda a, i: bodo.
                    hiframes.pd_timestamp_ext.
                    convert_datetime64_to_timestamp(np.int64(a[i])),
                    qkb__zbj, [oxjow__pepk, index])
            else:
                qkb__zbj = signature(arr_typ.dtype, arr_typ, types.intp)
                val = context.compile_internal(builder, lambda a, i: a[i],
                    qkb__zbj, [oxjow__pepk, index])
            values.append(val)
        value = context.make_tuple(builder, szvib__syuv.yield_type, values)
        result.yield_(value)
        lcxhu__qkk = cgutils.increment_index(builder, index)
        builder.store(lcxhu__qkk, cck__lwcd.index)


def _analyze_op_pair_first(self, scope, equiv_set, expr, lhs):
    typ = self.typemap[expr.value.name].first_type
    if not isinstance(typ, types.NamedTuple):
        return None
    lhs = ir.Var(scope, mk_unique_var('tuple_var'), expr.loc)
    self.typemap[lhs.name] = typ
    rhs = ir.Expr.pair_first(expr.value, expr.loc)
    mxq__buj = ir.Assign(rhs, lhs, expr.loc)
    gqn__kcvjc = lhs
    qeh__cba = []
    olziq__rnzy = []
    yqvm__rlxy = typ.count
    for i in range(yqvm__rlxy):
        ynq__iyq = ir.Var(gqn__kcvjc.scope, mk_unique_var('{}_size{}'.
            format(gqn__kcvjc.name, i)), gqn__kcvjc.loc)
        vovyx__bdd = ir.Expr.static_getitem(lhs, i, None, gqn__kcvjc.loc)
        self.calltypes[vovyx__bdd] = None
        qeh__cba.append(ir.Assign(vovyx__bdd, ynq__iyq, gqn__kcvjc.loc))
        self._define(equiv_set, ynq__iyq, types.intp, vovyx__bdd)
        olziq__rnzy.append(ynq__iyq)
    qxe__pbqn = tuple(olziq__rnzy)
    return numba.parfors.array_analysis.ArrayAnalysis.AnalyzeResult(shape=
        qxe__pbqn, pre=[mxq__buj] + qeh__cba)


numba.parfors.array_analysis.ArrayAnalysis._analyze_op_pair_first = (
    _analyze_op_pair_first)
