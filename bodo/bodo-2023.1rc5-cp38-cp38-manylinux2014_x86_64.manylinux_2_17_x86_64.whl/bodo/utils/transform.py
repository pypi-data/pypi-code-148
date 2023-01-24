"""
Helper functions for transformations.
"""
import itertools
import math
import operator
import types as pytypes
from collections import namedtuple
import numba
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, types
from numba.core.ir_utils import GuardException, build_definitions, compile_to_numba_ir, compute_cfg_from_blocks, find_callname, find_const, get_definition, guard, is_setitem, mk_unique_var, replace_arg_nodes, require
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import fold_arguments
import bodo
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoConstUpdatedError, BodoError, can_literalize_type, get_literal_value, get_overload_const_bool, get_overload_const_list, is_literal_type, is_overload_constant_bool
from bodo.utils.utils import is_array_typ, is_assign, is_call, is_expr
ReplaceFunc = namedtuple('ReplaceFunc', ['func', 'arg_types', 'args',
    'glbls', 'inline_bodo_calls', 'run_full_pipeline', 'pre_nodes'])
bodo_types_with_params = {'ArrayItemArrayType', 'CSRMatrixType',
    'CategoricalArrayType', 'CategoricalIndexType', 'DataFrameType',
    'DatetimeIndexType', 'Decimal128Type', 'DecimalArrayType',
    'IntegerArrayType', 'FloatingArrayType', 'IntervalArrayType',
    'IntervalIndexType', 'List', 'MapArrayType', 'NumericIndexType',
    'PDCategoricalDtype', 'PeriodIndexType', 'RangeIndexType', 'SeriesType',
    'StringIndexType', 'BinaryIndexType', 'StructArrayType',
    'TimedeltaIndexType', 'TupleArrayType'}
container_update_method_names = ('clear', 'pop', 'popitem', 'update', 'add',
    'difference_update', 'discard', 'intersection_update', 'remove',
    'symmetric_difference_update', 'append', 'extend', 'insert', 'reverse',
    'sort')
no_side_effect_call_tuples = {(int,), (list,), (set,), (dict,), (min,), (
    max,), (abs,), (len,), (bool,), (str,), ('ceil', math), ('Int32Dtype',
    pd), ('Int64Dtype', pd), ('Timestamp', pd), ('Week', 'offsets',
    'tseries', pd), ('init_series', 'pd_series_ext', 'hiframes', bodo), (
    'get_series_data', 'pd_series_ext', 'hiframes', bodo), (
    'get_series_index', 'pd_series_ext', 'hiframes', bodo), (
    'get_series_name', 'pd_series_ext', 'hiframes', bodo), (
    'get_index_data', 'pd_index_ext', 'hiframes', bodo), ('get_index_name',
    'pd_index_ext', 'hiframes', bodo), ('init_binary_str_index',
    'pd_index_ext', 'hiframes', bodo), ('init_numeric_index',
    'pd_index_ext', 'hiframes', bodo), ('init_categorical_index',
    'pd_index_ext', 'hiframes', bodo), ('_dti_val_finalize', 'pd_index_ext',
    'hiframes', bodo), ('init_datetime_index', 'pd_index_ext', 'hiframes',
    bodo), ('init_timedelta_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_range_index', 'pd_index_ext', 'hiframes', bodo), (
    'init_heter_index', 'pd_index_ext', 'hiframes', bodo), (
    'get_int_arr_data', 'int_arr_ext', 'libs', bodo), ('get_int_arr_bitmap',
    'int_arr_ext', 'libs', bodo), ('init_integer_array', 'int_arr_ext',
    'libs', bodo), ('alloc_int_array', 'int_arr_ext', 'libs', bodo), (
    'init_float_array', 'float_arr_ext', 'libs', bodo), (
    'alloc_float_array', 'float_arr_ext', 'libs', bodo), ('inplace_eq',
    'str_arr_ext', 'libs', bodo), ('get_bool_arr_data', 'bool_arr_ext',
    'libs', bodo), ('get_bool_arr_bitmap', 'bool_arr_ext', 'libs', bodo), (
    'init_bool_array', 'bool_arr_ext', 'libs', bodo), ('alloc_bool_array',
    'bool_arr_ext', 'libs', bodo), ('datetime_date_arr_to_dt64_arr',
    'pd_timestamp_ext', 'hiframes', bodo), ('alloc_pd_datetime_array',
    'pd_datetime_arr_ext', 'libs', bodo), (bodo.libs.bool_arr_ext.
    compute_or_body,), (bodo.libs.bool_arr_ext.compute_and_body,), (
    'alloc_datetime_date_array', 'datetime_date_ext', 'hiframes', bodo), (
    'alloc_datetime_timedelta_array', 'datetime_timedelta_ext', 'hiframes',
    bodo), ('cat_replace', 'pd_categorical_ext', 'hiframes', bodo), (
    'init_categorical_array', 'pd_categorical_ext', 'hiframes', bodo), (
    'alloc_categorical_array', 'pd_categorical_ext', 'hiframes', bodo), (
    'get_categorical_arr_codes', 'pd_categorical_ext', 'hiframes', bodo), (
    '_sum_handle_nan', 'series_kernels', 'hiframes', bodo), ('_box_cat_val',
    'series_kernels', 'hiframes', bodo), ('_mean_handle_nan',
    'series_kernels', 'hiframes', bodo), ('_var_handle_mincount',
    'series_kernels', 'hiframes', bodo), ('_compute_var_nan_count_ddof',
    'series_kernels', 'hiframes', bodo), ('_sem_handle_nan',
    'series_kernels', 'hiframes', bodo), ('dist_return', 'distributed_api',
    'libs', bodo), ('rep_return', 'distributed_api', 'libs', bodo), (
    'init_dataframe', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_data', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_all_data', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_table', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_dataframe_column_names', 'pd_dataframe_ext', 'hiframes', bodo), (
    'get_table_data', 'table', 'hiframes', bodo), ('get_dataframe_index',
    'pd_dataframe_ext', 'hiframes', bodo), ('init_rolling',
    'pd_rolling_ext', 'hiframes', bodo), ('init_groupby', 'pd_groupby_ext',
    'hiframes', bodo), ('calc_nitems', 'array_kernels', 'libs', bodo), (
    'concat', 'array_kernels', 'libs', bodo), ('unique', 'array_kernels',
    'libs', bodo), ('nunique', 'array_kernels', 'libs', bodo), ('quantile',
    'array_kernels', 'libs', bodo), ('explode', 'array_kernels', 'libs',
    bodo), ('explode_no_index', 'array_kernels', 'libs', bodo), (
    'get_arr_lens', 'array_kernels', 'libs', bodo), (
    'str_arr_from_sequence', 'str_arr_ext', 'libs', bodo), (
    'get_str_arr_str_length', 'str_arr_ext', 'libs', bodo), (
    'parse_datetime_str', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_dt64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'dt64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'timedelta64_to_integer', 'pd_timestamp_ext', 'hiframes', bodo), (
    'integer_to_timedelta64', 'pd_timestamp_ext', 'hiframes', bodo), (
    'npy_datetimestruct_to_datetime', 'pd_timestamp_ext', 'hiframes', bodo),
    ('isna', 'array_kernels', 'libs', bodo), (bodo.libs.str_arr_ext.
    num_total_chars,), ('num_total_chars', 'str_arr_ext', 'libs', bodo), (
    'copy',), ('from_iterable_impl', 'typing', 'utils', bodo), ('chain',
    itertools), ('groupby',), ('rolling',), (pd.CategoricalDtype,), (bodo.
    hiframes.pd_categorical_ext.get_code_for_value,), ('asarray', np), (
    'int32', np), ('int64', np), ('float64', np), ('float32', np), ('bool_',
    np), ('full', np), ('round', np), ('isnan', np), ('isnat', np), (
    'arange', np), ('internal_prange', 'parfor', numba), ('internal_prange',
    'parfor', 'parfors', numba), ('empty_inferred', 'ndarray', 'unsafe',
    numba), ('_slice_span', 'unicode', numba), ('_normalize_slice',
    'unicode', numba), ('init_session_builder', 'pyspark_ext', 'libs', bodo
    ), ('init_session', 'pyspark_ext', 'libs', bodo), ('init_spark_df',
    'pyspark_ext', 'libs', bodo), ('h5size', 'h5_api', 'io', bodo), (
    'pre_alloc_struct_array', 'struct_arr_ext', 'libs', bodo), (bodo.libs.
    struct_arr_ext.pre_alloc_struct_array,), ('pre_alloc_tuple_array',
    'tuple_arr_ext', 'libs', bodo), (bodo.libs.tuple_arr_ext.
    pre_alloc_tuple_array,), ('pre_alloc_array_item_array',
    'array_item_arr_ext', 'libs', bodo), (bodo.libs.array_item_arr_ext.
    pre_alloc_array_item_array,), ('dist_reduce', 'distributed_api', 'libs',
    bodo), (bodo.libs.distributed_api.dist_reduce,), (
    'pre_alloc_string_array', 'str_arr_ext', 'libs', bodo), (bodo.libs.
    str_arr_ext.pre_alloc_string_array,), ('pre_alloc_binary_array',
    'binary_arr_ext', 'libs', bodo), (bodo.libs.binary_arr_ext.
    pre_alloc_binary_array,), ('pre_alloc_map_array', 'map_arr_ext', 'libs',
    bodo), (bodo.libs.map_arr_ext.pre_alloc_map_array,), (
    'convert_dict_arr_to_int', 'dict_arr_ext', 'libs', bodo), (
    'cat_dict_str', 'dict_arr_ext', 'libs', bodo), ('str_replace',
    'dict_arr_ext', 'libs', bodo), ('dict_arr_to_numeric', 'dict_arr_ext',
    'libs', bodo), ('dict_arr_eq', 'dict_arr_ext', 'libs', bodo), (
    'dict_arr_ne', 'dict_arr_ext', 'libs', bodo), ('str_startswith',
    'dict_arr_ext', 'libs', bodo), ('str_endswith', 'dict_arr_ext', 'libs',
    bodo), ('str_contains_non_regex', 'dict_arr_ext', 'libs', bodo), (
    'str_series_contains_regex', 'dict_arr_ext', 'libs', bodo), (
    'str_capitalize', 'dict_arr_ext', 'libs', bodo), ('str_lower',
    'dict_arr_ext', 'libs', bodo), ('str_swapcase', 'dict_arr_ext', 'libs',
    bodo), ('str_title', 'dict_arr_ext', 'libs', bodo), ('str_upper',
    'dict_arr_ext', 'libs', bodo), ('str_center', 'dict_arr_ext', 'libs',
    bodo), ('str_get', 'dict_arr_ext', 'libs', bodo), ('str_repeat_int',
    'dict_arr_ext', 'libs', bodo), ('str_lstrip', 'dict_arr_ext', 'libs',
    bodo), ('str_rstrip', 'dict_arr_ext', 'libs', bodo), ('str_strip',
    'dict_arr_ext', 'libs', bodo), ('str_zfill', 'dict_arr_ext', 'libs',
    bodo), ('str_ljust', 'dict_arr_ext', 'libs', bodo), ('str_rjust',
    'dict_arr_ext', 'libs', bodo), ('str_find', 'dict_arr_ext', 'libs',
    bodo), ('str_rfind', 'dict_arr_ext', 'libs', bodo), ('str_index',
    'dict_arr_ext', 'libs', bodo), ('str_rindex', 'dict_arr_ext', 'libs',
    bodo), ('str_slice', 'dict_arr_ext', 'libs', bodo), ('str_extract',
    'dict_arr_ext', 'libs', bodo), ('str_extractall', 'dict_arr_ext',
    'libs', bodo), ('str_extractall_multi', 'dict_arr_ext', 'libs', bodo),
    ('str_len', 'dict_arr_ext', 'libs', bodo), ('str_count', 'dict_arr_ext',
    'libs', bodo), ('str_isalnum', 'dict_arr_ext', 'libs', bodo), (
    'str_isalpha', 'dict_arr_ext', 'libs', bodo), ('str_isdigit',
    'dict_arr_ext', 'libs', bodo), ('str_isspace', 'dict_arr_ext', 'libs',
    bodo), ('str_islower', 'dict_arr_ext', 'libs', bodo), ('str_isupper',
    'dict_arr_ext', 'libs', bodo), ('str_istitle', 'dict_arr_ext', 'libs',
    bodo), ('str_isnumeric', 'dict_arr_ext', 'libs', bodo), (
    'str_isdecimal', 'dict_arr_ext', 'libs', bodo), ('str_match',
    'dict_arr_ext', 'libs', bodo), ('prange', bodo), (bodo.prange,), (
    'objmode', bodo), (bodo.objmode,), ('get_label_dict_from_categories',
    'pd_categorial_ext', 'hiframes', bodo), (
    'get_label_dict_from_categories_no_duplicates', 'pd_categorial_ext',
    'hiframes', bodo), ('build_nullable_tuple', 'nullable_tuple_ext',
    'libs', bodo), ('generate_mappable_table_func', 'table_utils', 'utils',
    bodo), ('table_astype', 'table_utils', 'utils', bodo), ('table_concat',
    'table_utils', 'utils', bodo), ('table_filter', 'table', 'hiframes',
    bodo), ('table_subset', 'table', 'hiframes', bodo), (
    'logical_table_to_table', 'table', 'hiframes', bodo), ('set_table_data',
    'table', 'hiframes', bodo), ('set_table_null', 'table', 'hiframes',
    bodo), ('startswith',), ('endswith',), ('upper',), ('lower',), (
    '__bodosql_replace_columns_dummy', 'dataframe_impl', 'hiframes', bodo)}
_np_type_names = {'int8', 'int16', 'int32', 'int64', 'uint8', 'uint16',
    'uint32', 'uint64', 'float32', 'float64', 'bool_'}


def remove_hiframes(rhs, lives, call_list):
    wpukt__avpw = tuple(call_list)
    if wpukt__avpw in no_side_effect_call_tuples:
        return True
    if wpukt__avpw == (bodo.hiframes.pd_index_ext.init_range_index,):
        return True
    if len(call_list) == 4 and call_list[1:] == ['conversion', 'utils', bodo]:
        return True
    if isinstance(call_list[-1], pytypes.ModuleType) and call_list[-1
        ].__name__ == 'bodosql':
        return True
    if call_list[1:] == ['bodosql_array_kernels', 'libs', bodo]:
        return True
    if len(call_list) == 2 and call_list[0] == 'copy':
        return True
    if call_list == ['h5read', 'h5_api', 'io', bodo] and rhs.args[5
        ].name not in lives:
        return True
    if call_list == ['move_str_binary_arr_payload', 'str_arr_ext', 'libs', bodo
        ] and rhs.args[0].name not in lives:
        return True
    if call_list in (['setna', 'array_kernels', 'libs', bodo], [
        'copy_array_element', 'array_kernels', 'libs', bodo], [
        'get_str_arr_item_copy', 'str_arr_ext', 'libs', bodo]) and rhs.args[0
        ].name not in lives:
        return True
    if call_list == ['ensure_column_unboxed', 'table', 'hiframes', bodo
        ] and rhs.args[0].name not in lives and rhs.args[1].name not in lives:
        return True
    if call_list == ['generate_table_nbytes', 'table_utils', 'utils', bodo
        ] and rhs.args[1].name not in lives:
        return True
    if len(wpukt__avpw) == 1 and tuple in getattr(wpukt__avpw[0], '__mro__', ()
        ):
        return True
    return False


numba.core.ir_utils.remove_call_handlers.append(remove_hiframes)


def compile_func_single_block(func, args, ret_var, typing_info=None,
    extra_globals=None, infer_types=True, run_untyped_pass=False, flags=
    None, replace_globals=False, add_default_globals=True):
    if replace_globals:
        yza__vyum = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd,
            'math': math}
    else:
        yza__vyum = func.__globals__
    if extra_globals is not None:
        yza__vyum.update(extra_globals)
    if add_default_globals:
        yza__vyum.update({'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd,
            'math': math})
    loc = ir.Loc('', 0)
    if ret_var:
        loc = ret_var.loc
    if typing_info and infer_types:
        loc = typing_info.curr_loc
        f_ir = compile_to_numba_ir(func, yza__vyum, typingctx=typing_info.
            typingctx, targetctx=typing_info.targetctx, arg_typs=tuple(
            typing_info.typemap[lgkti__dckvr.name] for lgkti__dckvr in args
            ), typemap=typing_info.typemap, calltypes=typing_info.calltypes)
    else:
        f_ir = compile_to_numba_ir(func, yza__vyum)
    assert len(f_ir.blocks
        ) == 1, 'only single block functions supported in compile_func_single_block()'
    if run_untyped_pass:
        squej__wva = tuple(typing_info.typemap[lgkti__dckvr.name] for
            lgkti__dckvr in args)
        mwuzb__zqpk = bodo.transforms.untyped_pass.UntypedPass(f_ir,
            typing_info.typingctx, squej__wva, {}, {}, flags)
        mwuzb__zqpk.run()
    cpki__zeu = f_ir.blocks.popitem()[1]
    replace_arg_nodes(cpki__zeu, args)
    lova__ccfn = cpki__zeu.body[:-2]
    update_locs(lova__ccfn[len(args):], loc)
    for stmt in lova__ccfn[:len(args)]:
        stmt.target.loc = loc
    if ret_var is not None:
        jcjd__fsx = cpki__zeu.body[-2]
        assert is_assign(jcjd__fsx) and is_expr(jcjd__fsx.value, 'cast')
        zfjwc__joyi = jcjd__fsx.value.value
        lova__ccfn.append(ir.Assign(zfjwc__joyi, ret_var, loc))
    return lova__ccfn


def update_locs(node_list, loc):
    for stmt in node_list:
        stmt.loc = loc
        for xadll__ccx in stmt.list_vars():
            xadll__ccx.loc = loc
        if is_assign(stmt):
            stmt.value.loc = loc


def get_stmt_defs(stmt):
    if is_assign(stmt):
        return set([stmt.target.name])
    if type(stmt) in numba.core.analysis.ir_extension_usedefs:
        wiwr__qpli = numba.core.analysis.ir_extension_usedefs[type(stmt)]
        nrw__kfxu, liflr__ycnnb = wiwr__qpli(stmt)
        return liflr__ycnnb
    return set()


def get_const_value(var, func_ir, err_msg, typemap=None, arg_types=None,
    file_info=None):
    if hasattr(var, 'loc'):
        loc = var.loc
    else:
        loc = None
    try:
        vde__sxd = get_const_value_inner(func_ir, var, arg_types, typemap,
            file_info=file_info)
        if isinstance(vde__sxd, ir.UndefinedType):
            wkn__hqccm = func_ir.get_definition(var.name).name
            raise BodoError(f"name '{wkn__hqccm}' is not defined", loc=loc)
    except GuardException as jnke__xicph:
        raise BodoError(err_msg, loc=loc)
    return vde__sxd


def get_const_value_inner(func_ir, var, arg_types=None, typemap=None,
    updated_containers=None, file_info=None, pyobject_to_literal=False,
    literalize_args=True):
    require(isinstance(var, ir.Var))
    ovktn__uojp = get_definition(func_ir, var)
    xqirh__yeuun = None
    if typemap is not None:
        xqirh__yeuun = typemap.get(var.name, None)
    if isinstance(ovktn__uojp, ir.Arg) and arg_types is not None:
        xqirh__yeuun = arg_types[ovktn__uojp.index]
    if updated_containers and var.name in updated_containers:
        raise BodoConstUpdatedError(
            f"variable '{var.name}' is updated inplace using '{updated_containers[var.name]}'"
            )
    if is_literal_type(xqirh__yeuun):
        return get_literal_value(xqirh__yeuun)
    if isinstance(ovktn__uojp, (ir.Const, ir.Global, ir.FreeVar)):
        vde__sxd = ovktn__uojp.value
        return vde__sxd
    if literalize_args and isinstance(ovktn__uojp, ir.Arg
        ) and can_literalize_type(xqirh__yeuun, pyobject_to_literal):
        raise numba.core.errors.ForceLiteralArg({ovktn__uojp.index}, loc=
            var.loc, file_infos={ovktn__uojp.index: file_info} if file_info
             is not None else None)
    if is_expr(ovktn__uojp, 'binop'):
        if file_info and ovktn__uojp.fn == operator.add:
            try:
                mkxlg__nnd = get_const_value_inner(func_ir, ovktn__uojp.lhs,
                    arg_types, typemap, updated_containers, literalize_args
                    =False)
                file_info.set_concat(mkxlg__nnd, True)
                dnfr__kjlsz = get_const_value_inner(func_ir, ovktn__uojp.
                    rhs, arg_types, typemap, updated_containers, file_info)
                return ovktn__uojp.fn(mkxlg__nnd, dnfr__kjlsz)
            except (GuardException, BodoConstUpdatedError) as jnke__xicph:
                pass
            try:
                dnfr__kjlsz = get_const_value_inner(func_ir, ovktn__uojp.
                    rhs, arg_types, typemap, updated_containers,
                    literalize_args=False)
                file_info.set_concat(dnfr__kjlsz, False)
                mkxlg__nnd = get_const_value_inner(func_ir, ovktn__uojp.lhs,
                    arg_types, typemap, updated_containers, file_info)
                return ovktn__uojp.fn(mkxlg__nnd, dnfr__kjlsz)
            except (GuardException, BodoConstUpdatedError) as jnke__xicph:
                pass
        mkxlg__nnd = get_const_value_inner(func_ir, ovktn__uojp.lhs,
            arg_types, typemap, updated_containers)
        dnfr__kjlsz = get_const_value_inner(func_ir, ovktn__uojp.rhs,
            arg_types, typemap, updated_containers)
        return ovktn__uojp.fn(mkxlg__nnd, dnfr__kjlsz)
    if is_expr(ovktn__uojp, 'unary'):
        vde__sxd = get_const_value_inner(func_ir, ovktn__uojp.value,
            arg_types, typemap, updated_containers)
        return ovktn__uojp.fn(vde__sxd)
    if is_expr(ovktn__uojp, 'getattr') and typemap:
        qrsc__oky = typemap.get(ovktn__uojp.value.name, None)
        if isinstance(qrsc__oky, bodo.hiframes.pd_dataframe_ext.DataFrameType
            ) and ovktn__uojp.attr == 'columns':
            return pd.Index(qrsc__oky.columns)
        if isinstance(qrsc__oky, types.SliceType):
            dol__neqi = get_definition(func_ir, ovktn__uojp.value)
            require(is_call(dol__neqi))
            encnk__jbrm = find_callname(func_ir, dol__neqi)
            dlgb__anpd = False
            if encnk__jbrm == ('_normalize_slice', 'numba.cpython.unicode'):
                require(ovktn__uojp.attr in ('start', 'step'))
                dol__neqi = get_definition(func_ir, dol__neqi.args[0])
                dlgb__anpd = True
            require(find_callname(func_ir, dol__neqi) == ('slice', 'builtins'))
            if len(dol__neqi.args) == 1:
                if ovktn__uojp.attr == 'start':
                    return 0
                if ovktn__uojp.attr == 'step':
                    return 1
                require(ovktn__uojp.attr == 'stop')
                return get_const_value_inner(func_ir, dol__neqi.args[0],
                    arg_types, typemap, updated_containers)
            if ovktn__uojp.attr == 'start':
                vde__sxd = get_const_value_inner(func_ir, dol__neqi.args[0],
                    arg_types, typemap, updated_containers)
                if vde__sxd is None:
                    vde__sxd = 0
                if dlgb__anpd:
                    require(vde__sxd == 0)
                return vde__sxd
            if ovktn__uojp.attr == 'stop':
                assert not dlgb__anpd
                return get_const_value_inner(func_ir, dol__neqi.args[1],
                    arg_types, typemap, updated_containers)
            require(ovktn__uojp.attr == 'step')
            if len(dol__neqi.args) == 2:
                return 1
            else:
                vde__sxd = get_const_value_inner(func_ir, dol__neqi.args[2],
                    arg_types, typemap, updated_containers)
                if vde__sxd is None:
                    vde__sxd = 1
                if dlgb__anpd:
                    require(vde__sxd == 1)
                return vde__sxd
    if is_expr(ovktn__uojp, 'getattr'):
        return getattr(get_const_value_inner(func_ir, ovktn__uojp.value,
            arg_types, typemap, updated_containers), ovktn__uojp.attr)
    if is_expr(ovktn__uojp, 'getitem'):
        value = get_const_value_inner(func_ir, ovktn__uojp.value, arg_types,
            typemap, updated_containers)
        index = get_const_value_inner(func_ir, ovktn__uojp.index, arg_types,
            typemap, updated_containers)
        return value[index]
    tes__ewq = guard(find_callname, func_ir, ovktn__uojp, typemap)
    if tes__ewq is not None and len(tes__ewq) == 2 and tes__ewq[0
        ] == 'keys' and isinstance(tes__ewq[1], ir.Var):
        qavx__wkbx = ovktn__uojp.func
        ovktn__uojp = get_definition(func_ir, tes__ewq[1])
        bwem__nfim = tes__ewq[1].name
        if updated_containers and bwem__nfim in updated_containers:
            raise BodoConstUpdatedError(
                "variable '{}' is updated inplace using '{}'".format(
                bwem__nfim, updated_containers[bwem__nfim]))
        require(is_expr(ovktn__uojp, 'build_map'))
        vals = [xadll__ccx[0] for xadll__ccx in ovktn__uojp.items]
        yocjc__gan = guard(get_definition, func_ir, qavx__wkbx)
        assert isinstance(yocjc__gan, ir.Expr) and yocjc__gan.attr == 'keys'
        yocjc__gan.attr = 'copy'
        return [get_const_value_inner(func_ir, xadll__ccx, arg_types,
            typemap, updated_containers) for xadll__ccx in vals]
    if is_expr(ovktn__uojp, 'build_map'):
        return {get_const_value_inner(func_ir, xadll__ccx[0], arg_types,
            typemap, updated_containers): get_const_value_inner(func_ir,
            xadll__ccx[1], arg_types, typemap, updated_containers) for
            xadll__ccx in ovktn__uojp.items}
    if is_expr(ovktn__uojp, 'build_tuple'):
        return tuple(get_const_value_inner(func_ir, xadll__ccx, arg_types,
            typemap, updated_containers) for xadll__ccx in ovktn__uojp.items)
    if is_expr(ovktn__uojp, 'build_list'):
        return [get_const_value_inner(func_ir, xadll__ccx, arg_types,
            typemap, updated_containers) for xadll__ccx in ovktn__uojp.items]
    if is_expr(ovktn__uojp, 'build_set'):
        return {get_const_value_inner(func_ir, xadll__ccx, arg_types,
            typemap, updated_containers) for xadll__ccx in ovktn__uojp.items}
    if tes__ewq == ('list', 'builtins'):
        values = get_const_value_inner(func_ir, ovktn__uojp.args[0],
            arg_types, typemap, updated_containers)
        if isinstance(values, set):
            values = sorted(values)
        return list(values)
    if tes__ewq == ('set', 'builtins'):
        return set(get_const_value_inner(func_ir, ovktn__uojp.args[0],
            arg_types, typemap, updated_containers))
    if tes__ewq == ('range', 'builtins') and len(ovktn__uojp.args) == 1:
        return range(get_const_value_inner(func_ir, ovktn__uojp.args[0],
            arg_types, typemap, updated_containers))
    if tes__ewq == ('slice', 'builtins'):
        return slice(*tuple(get_const_value_inner(func_ir, xadll__ccx,
            arg_types, typemap, updated_containers) for xadll__ccx in
            ovktn__uojp.args))
    if tes__ewq == ('str', 'builtins'):
        return str(get_const_value_inner(func_ir, ovktn__uojp.args[0],
            arg_types, typemap, updated_containers))
    if tes__ewq == ('bool', 'builtins'):
        return bool(get_const_value_inner(func_ir, ovktn__uojp.args[0],
            arg_types, typemap, updated_containers))
    if tes__ewq == ('format', 'builtins'):
        lgkti__dckvr = get_const_value_inner(func_ir, ovktn__uojp.args[0],
            arg_types, typemap, updated_containers)
        xlph__rztiz = get_const_value_inner(func_ir, ovktn__uojp.args[1],
            arg_types, typemap, updated_containers) if len(ovktn__uojp.args
            ) > 1 else ''
        return format(lgkti__dckvr, xlph__rztiz)
    if tes__ewq in (('init_binary_str_index', 'bodo.hiframes.pd_index_ext'),
        ('init_numeric_index', 'bodo.hiframes.pd_index_ext'), (
        'init_categorical_index', 'bodo.hiframes.pd_index_ext'), (
        'init_datetime_index', 'bodo.hiframes.pd_index_ext'), (
        'init_timedelta_index', 'bodo.hiframes.pd_index_ext'), (
        'init_heter_index', 'bodo.hiframes.pd_index_ext')):
        return pd.Index(get_const_value_inner(func_ir, ovktn__uojp.args[0],
            arg_types, typemap, updated_containers))
    if tes__ewq == ('str_arr_from_sequence', 'bodo.libs.str_arr_ext'):
        return np.array(get_const_value_inner(func_ir, ovktn__uojp.args[0],
            arg_types, typemap, updated_containers))
    if tes__ewq == ('init_range_index', 'bodo.hiframes.pd_index_ext'):
        return pd.RangeIndex(get_const_value_inner(func_ir, ovktn__uojp.
            args[0], arg_types, typemap, updated_containers),
            get_const_value_inner(func_ir, ovktn__uojp.args[1], arg_types,
            typemap, updated_containers), get_const_value_inner(func_ir,
            ovktn__uojp.args[2], arg_types, typemap, updated_containers))
    if tes__ewq == ('len', 'builtins') and typemap and isinstance(typemap.
        get(ovktn__uojp.args[0].name, None), types.BaseTuple):
        return len(typemap[ovktn__uojp.args[0].name])
    if tes__ewq == ('len', 'builtins'):
        bwjbt__aqop = guard(get_definition, func_ir, ovktn__uojp.args[0])
        if isinstance(bwjbt__aqop, ir.Expr) and bwjbt__aqop.op in (
            'build_tuple', 'build_list', 'build_set', 'build_map'):
            return len(bwjbt__aqop.items)
        return len(get_const_value_inner(func_ir, ovktn__uojp.args[0],
            arg_types, typemap, updated_containers))
    if tes__ewq == ('CategoricalDtype', 'pandas'):
        kws = dict(ovktn__uojp.kws)
        vjci__ykwc = get_call_expr_arg('CategoricalDtype', ovktn__uojp.args,
            kws, 0, 'categories', '')
        eumhv__msr = get_call_expr_arg('CategoricalDtype', ovktn__uojp.args,
            kws, 1, 'ordered', False)
        if eumhv__msr is not False:
            eumhv__msr = get_const_value_inner(func_ir, eumhv__msr,
                arg_types, typemap, updated_containers)
        if vjci__ykwc == '':
            vjci__ykwc = None
        else:
            vjci__ykwc = get_const_value_inner(func_ir, vjci__ykwc,
                arg_types, typemap, updated_containers)
        return pd.CategoricalDtype(vjci__ykwc, eumhv__msr)
    if tes__ewq == ('dtype', 'numpy'):
        return np.dtype(get_const_value_inner(func_ir, ovktn__uojp.args[0],
            arg_types, typemap, updated_containers))
    if tes__ewq is not None and tes__ewq[1] == 'numpy' and tes__ewq[0
        ] in _np_type_names:
        return getattr(np, tes__ewq[0])(get_const_value_inner(func_ir,
            ovktn__uojp.args[0], arg_types, typemap, updated_containers))
    if tes__ewq is not None and len(tes__ewq) == 2 and tes__ewq[1
        ] == 'pandas' and tes__ewq[0] in ('Int8Dtype', 'Int16Dtype',
        'Int32Dtype', 'Int64Dtype', 'UInt8Dtype', 'UInt16Dtype',
        'UInt32Dtype', 'UInt64Dtype'):
        return getattr(pd, tes__ewq[0])()
    if tes__ewq is not None and len(tes__ewq) == 2 and isinstance(tes__ewq[
        1], ir.Var):
        vde__sxd = get_const_value_inner(func_ir, tes__ewq[1], arg_types,
            typemap, updated_containers)
        args = [get_const_value_inner(func_ir, xadll__ccx, arg_types,
            typemap, updated_containers) for xadll__ccx in ovktn__uojp.args]
        kws = {uwxv__lgx[0]: get_const_value_inner(func_ir, uwxv__lgx[1],
            arg_types, typemap, updated_containers) for uwxv__lgx in
            ovktn__uojp.kws}
        return getattr(vde__sxd, tes__ewq[0])(*args, **kws)
    if tes__ewq is not None and len(tes__ewq) == 2 and tes__ewq[1
        ] == 'bodo' and tes__ewq[0] in bodo_types_with_params:
        args = tuple(get_const_value_inner(func_ir, xadll__ccx, arg_types,
            typemap, updated_containers) for xadll__ccx in ovktn__uojp.args)
        kwargs = {wkn__hqccm: get_const_value_inner(func_ir, xadll__ccx,
            arg_types, typemap, updated_containers) for wkn__hqccm,
            xadll__ccx in dict(ovktn__uojp.kws).items()}
        return getattr(bodo, tes__ewq[0])(*args, **kwargs)
    if is_call(ovktn__uojp) and typemap and isinstance(typemap.get(
        ovktn__uojp.func.name, None), types.Dispatcher):
        py_func = typemap[ovktn__uojp.func.name].dispatcher.py_func
        require(ovktn__uojp.vararg is None)
        args = tuple(get_const_value_inner(func_ir, xadll__ccx, arg_types,
            typemap, updated_containers) for xadll__ccx in ovktn__uojp.args)
        kwargs = {wkn__hqccm: get_const_value_inner(func_ir, xadll__ccx,
            arg_types, typemap, updated_containers) for wkn__hqccm,
            xadll__ccx in dict(ovktn__uojp.kws).items()}
        arg_types = tuple(bodo.typeof(xadll__ccx) for xadll__ccx in args)
        kw_types = {okd__bcg: bodo.typeof(xadll__ccx) for okd__bcg,
            xadll__ccx in kwargs.items()}
        require(_func_is_pure(py_func, arg_types, kw_types))
        return py_func(*args, **kwargs)
    raise GuardException('Constant value not found')


def _func_is_pure(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.ir.csv_ext import CsvReader
    from bodo.ir.json_ext import JsonReader
    from bodo.ir.parquet_ext import ParquetReader
    from bodo.ir.sql_ext import SqlReader
    f_ir, typemap, gwbxj__txzjv, gwbxj__txzjv = (bodo.compiler.
        get_func_type_info(py_func, arg_types, kw_types))
    for block in f_ir.blocks.values():
        for stmt in block.body:
            if isinstance(stmt, ir.Print):
                return False
            if isinstance(stmt, (CsvReader, JsonReader, ParquetReader,
                SqlReader)):
                return False
            if is_setitem(stmt) and isinstance(guard(get_definition, f_ir,
                stmt.target), ir.Arg):
                return False
            if is_assign(stmt):
                rhs = stmt.value
                if isinstance(rhs, ir.Yield):
                    return False
                if is_call(rhs):
                    iinw__lva = guard(get_definition, f_ir, rhs.func)
                    if isinstance(iinw__lva, ir.Const) and isinstance(iinw__lva
                        .value, numba.core.dispatcher.ObjModeLiftedWith):
                        return False
                    qfe__oxgy = guard(find_callname, f_ir, rhs)
                    if qfe__oxgy is None:
                        return False
                    func_name, zje__zyick = qfe__oxgy
                    if zje__zyick == 'pandas' and func_name.startswith('read_'
                        ):
                        return False
                    if qfe__oxgy in (('fromfile', 'numpy'), ('file_read',
                        'bodo.io.np_io')):
                        return False
                    if qfe__oxgy == ('File', 'h5py'):
                        return False
                    if isinstance(zje__zyick, ir.Var):
                        xqirh__yeuun = typemap[zje__zyick.name]
                        if isinstance(xqirh__yeuun, (DataFrameType, SeriesType)
                            ) and func_name in ('to_csv', 'to_excel',
                            'to_json', 'to_sql', 'to_pickle', 'to_parquet',
                            'info'):
                            return False
                        if isinstance(xqirh__yeuun, types.Array
                            ) and func_name == 'tofile':
                            return False
                        if isinstance(xqirh__yeuun, bodo.LoggingLoggerType):
                            return False
                        if str(xqirh__yeuun).startswith('Mpl'):
                            return False
                        if (func_name in container_update_method_names and
                            isinstance(guard(get_definition, f_ir,
                            zje__zyick), ir.Arg)):
                            return False
                    if zje__zyick in ('numpy.random', 'time', 'logging',
                        'matplotlib.pyplot'):
                        return False
    return True


def fold_argument_types(pysig, args, kws):

    def normal_handler(index, param, value):
        return value

    def default_handler(index, param, default):
        return types.Omitted(default)

    def stararg_handler(index, param, values):
        return types.StarArgTuple(values)
    args = fold_arguments(pysig, args, kws, normal_handler, default_handler,
        stararg_handler)
    return args


def get_const_func_output_type(func, arg_types, kw_types, typing_context,
    target_context, is_udf=True):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
    py_func = None
    if isinstance(func, types.MakeFunctionLiteral):
        tfp__wwf = func.literal_value.code
        eycr__vcdj = {'np': np, 'pd': pd, 'numba': numba, 'bodo': bodo}
        if hasattr(func.literal_value, 'globals'):
            eycr__vcdj = func.literal_value.globals
        f_ir = numba.core.ir_utils.get_ir_of_code(eycr__vcdj, tfp__wwf)
        fix_struct_return(f_ir)
        typemap, vsdyd__kirz, zzz__ueeq, gwbxj__txzjv = (numba.core.
            typed_passes.type_inference_stage(typing_context,
            target_context, f_ir, arg_types, None))
    elif isinstance(func, bodo.utils.typing.FunctionLiteral):
        py_func = func.literal_value
        f_ir, typemap, zzz__ueeq, vsdyd__kirz = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    elif isinstance(func, CPUDispatcher):
        py_func = func.py_func
        f_ir, typemap, zzz__ueeq, vsdyd__kirz = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    else:
        if not isinstance(func, types.Dispatcher):
            if isinstance(func, types.Function):
                raise BodoError(
                    f'Bodo does not support built-in functions yet, {func}')
            else:
                raise BodoError(f'Function type expected, not {func}')
        py_func = func.dispatcher.py_func
        f_ir, typemap, zzz__ueeq, vsdyd__kirz = (bodo.compiler.
            get_func_type_info(py_func, arg_types, kw_types))
    if is_udf and isinstance(vsdyd__kirz, types.DictType):
        hgco__sgfml = guard(get_struct_keynames, f_ir, typemap)
        if hgco__sgfml is not None:
            vsdyd__kirz = StructType((vsdyd__kirz.value_type,) * len(
                hgco__sgfml), hgco__sgfml)
    if is_udf and isinstance(vsdyd__kirz, (SeriesType, HeterogeneousSeriesType)
        ):
        swzgl__sxa = numba.core.registry.cpu_target.typing_context
        slqct__uwzvv = numba.core.registry.cpu_target.target_context
        buqsf__giya = bodo.transforms.series_pass.SeriesPass(f_ir,
            swzgl__sxa, slqct__uwzvv, typemap, zzz__ueeq, {})
        vhxf__vlhaf = buqsf__giya.run()
        if vhxf__vlhaf:
            vhxf__vlhaf = buqsf__giya.run()
            if vhxf__vlhaf:
                buqsf__giya.run()
        aaqq__cfh = compute_cfg_from_blocks(f_ir.blocks)
        hbje__ssx = [guard(_get_const_series_info, f_ir.blocks[skg__ddbb],
            f_ir, typemap) for skg__ddbb in aaqq__cfh.exit_points() if
            isinstance(f_ir.blocks[skg__ddbb].body[-1], ir.Return)]
        if None in hbje__ssx or len(pd.Series(hbje__ssx).unique()) != 1:
            vsdyd__kirz.const_info = None
        else:
            vsdyd__kirz.const_info = hbje__ssx[0]
    return vsdyd__kirz


def _get_const_series_info(block, f_ir, typemap):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType
    assert isinstance(block.body[-1], ir.Return)
    lqog__mcffw = block.body[-1].value
    lzshe__rpu = get_definition(f_ir, lqog__mcffw)
    require(is_expr(lzshe__rpu, 'cast'))
    lzshe__rpu = get_definition(f_ir, lzshe__rpu.value)
    require(is_call(lzshe__rpu) and find_callname(f_ir, lzshe__rpu) == (
        'init_series', 'bodo.hiframes.pd_series_ext'))
    hlne__qdfli = lzshe__rpu.args[1]
    sqwkv__yldjk = tuple(get_const_value_inner(f_ir, hlne__qdfli, typemap=
        typemap))
    if isinstance(typemap[lqog__mcffw.name], HeterogeneousSeriesType):
        return len(typemap[lqog__mcffw.name].data), sqwkv__yldjk
    oef__gxruk = lzshe__rpu.args[0]
    obnn__lwhat = get_definition(f_ir, oef__gxruk)
    func_name, smmx__uut = find_callname(f_ir, obnn__lwhat)
    if is_call(obnn__lwhat) and bodo.utils.utils.is_alloc_callname(func_name,
        smmx__uut):
        iwerk__cnmr = obnn__lwhat.args[0]
        nlouz__exmu = get_const_value_inner(f_ir, iwerk__cnmr, typemap=typemap)
        return nlouz__exmu, sqwkv__yldjk
    if is_call(obnn__lwhat) and find_callname(f_ir, obnn__lwhat) in [(
        'asarray', 'numpy'), ('str_arr_from_sequence',
        'bodo.libs.str_arr_ext'), ('build_nullable_tuple',
        'bodo.libs.nullable_tuple_ext')]:
        oef__gxruk = obnn__lwhat.args[0]
        obnn__lwhat = get_definition(f_ir, oef__gxruk)
    require(is_expr(obnn__lwhat, 'build_tuple') or is_expr(obnn__lwhat,
        'build_list'))
    return len(obnn__lwhat.items), sqwkv__yldjk


def extract_keyvals_from_struct_map(f_ir, build_map, loc, scope, typemap=None):
    lheqn__jgte = []
    rdfum__mdugf = []
    values = []
    for okd__bcg, xadll__ccx in build_map.items:
        tyw__pjuld = find_const(f_ir, okd__bcg)
        require(isinstance(tyw__pjuld, str))
        rdfum__mdugf.append(tyw__pjuld)
        lheqn__jgte.append(okd__bcg)
        values.append(xadll__ccx)
    lsf__igqbb = ir.Var(scope, mk_unique_var('val_tup'), loc)
    bcepa__zqqqf = ir.Assign(ir.Expr.build_tuple(values, loc), lsf__igqbb, loc)
    f_ir._definitions[lsf__igqbb.name] = [bcepa__zqqqf.value]
    jve__jid = ir.Var(scope, mk_unique_var('key_tup'), loc)
    mdpi__wknop = ir.Assign(ir.Expr.build_tuple(lheqn__jgte, loc), jve__jid,
        loc)
    f_ir._definitions[jve__jid.name] = [mdpi__wknop.value]
    if typemap is not None:
        typemap[lsf__igqbb.name] = types.Tuple([typemap[xadll__ccx.name] for
            xadll__ccx in values])
        typemap[jve__jid.name] = types.Tuple([typemap[xadll__ccx.name] for
            xadll__ccx in lheqn__jgte])
    return rdfum__mdugf, lsf__igqbb, bcepa__zqqqf, jve__jid, mdpi__wknop


def _replace_const_map_return(f_ir, block, label):
    require(isinstance(block.body[-1], ir.Return))
    ikop__vve = block.body[-1].value
    gbyi__cfvgb = guard(get_definition, f_ir, ikop__vve)
    require(is_expr(gbyi__cfvgb, 'cast'))
    lzshe__rpu = guard(get_definition, f_ir, gbyi__cfvgb.value)
    require(is_expr(lzshe__rpu, 'build_map'))
    require(len(lzshe__rpu.items) > 0)
    loc = block.loc
    scope = block.scope
    rdfum__mdugf, lsf__igqbb, bcepa__zqqqf, jve__jid, mdpi__wknop = (
        extract_keyvals_from_struct_map(f_ir, lzshe__rpu, loc, scope))
    vqe__ifloi = ir.Var(scope, mk_unique_var('conv_call'), loc)
    ire__ilv = ir.Assign(ir.Global('struct_if_heter_dict', bodo.utils.
        conversion.struct_if_heter_dict, loc), vqe__ifloi, loc)
    f_ir._definitions[vqe__ifloi.name] = [ire__ilv.value]
    zbgd__lsg = ir.Var(scope, mk_unique_var('struct_val'), loc)
    wea__dqnr = ir.Assign(ir.Expr.call(vqe__ifloi, [lsf__igqbb, jve__jid],
        {}, loc), zbgd__lsg, loc)
    f_ir._definitions[zbgd__lsg.name] = [wea__dqnr.value]
    gbyi__cfvgb.value = zbgd__lsg
    lzshe__rpu.items = [(okd__bcg, okd__bcg) for okd__bcg, gwbxj__txzjv in
        lzshe__rpu.items]
    block.body = block.body[:-2] + [bcepa__zqqqf, mdpi__wknop, ire__ilv,
        wea__dqnr] + block.body[-2:]
    return tuple(rdfum__mdugf)


def get_struct_keynames(f_ir, typemap):
    aaqq__cfh = compute_cfg_from_blocks(f_ir.blocks)
    zdjaz__lzij = list(aaqq__cfh.exit_points())[0]
    block = f_ir.blocks[zdjaz__lzij]
    require(isinstance(block.body[-1], ir.Return))
    ikop__vve = block.body[-1].value
    gbyi__cfvgb = guard(get_definition, f_ir, ikop__vve)
    require(is_expr(gbyi__cfvgb, 'cast'))
    lzshe__rpu = guard(get_definition, f_ir, gbyi__cfvgb.value)
    require(is_call(lzshe__rpu) and find_callname(f_ir, lzshe__rpu) == (
        'struct_if_heter_dict', 'bodo.utils.conversion'))
    return get_overload_const_list(typemap[lzshe__rpu.args[1].name])


def fix_struct_return(f_ir):
    ampe__dcfid = None
    aaqq__cfh = compute_cfg_from_blocks(f_ir.blocks)
    for zdjaz__lzij in aaqq__cfh.exit_points():
        ampe__dcfid = guard(_replace_const_map_return, f_ir, f_ir.blocks[
            zdjaz__lzij], zdjaz__lzij)
    return ampe__dcfid


def update_node_list_definitions(node_list, func_ir):
    loc = ir.Loc('', 0)
    lbswf__nqb = ir.Block(ir.Scope(None, loc), loc)
    lbswf__nqb.body = node_list
    build_definitions({(0): lbswf__nqb}, func_ir._definitions)
    return


NESTED_TUP_SENTINEL = '$BODO_NESTED_TUP'


def gen_const_val_str(c):
    if isinstance(c, tuple):
        return "'{}{}', ".format(NESTED_TUP_SENTINEL, len(c)) + ', '.join(
            gen_const_val_str(xadll__ccx) for xadll__ccx in c)
    if isinstance(c, str):
        return "'{}'".format(c)
    if isinstance(c, (pd.Timestamp, pd.Timedelta, float)):
        return "'{}'".format(c)
    return str(c)


def gen_const_tup(vals):
    uioz__cppq = ', '.join(gen_const_val_str(c) for c in vals)
    return '({}{})'.format(uioz__cppq, ',' if len(vals) == 1 else '')


def get_const_tup_vals(c_typ):
    vals = get_overload_const_list(c_typ)
    return _get_original_nested_tups(vals)


def _get_original_nested_tups(vals):
    for ljpx__qttq in range(len(vals) - 1, -1, -1):
        xadll__ccx = vals[ljpx__qttq]
        if isinstance(xadll__ccx, str) and xadll__ccx.startswith(
            NESTED_TUP_SENTINEL):
            ypkh__jtjj = int(xadll__ccx[len(NESTED_TUP_SENTINEL):])
            return _get_original_nested_tups(tuple(vals[:ljpx__qttq]) + (
                tuple(vals[ljpx__qttq + 1:ljpx__qttq + ypkh__jtjj + 1]),) +
                tuple(vals[ljpx__qttq + ypkh__jtjj + 1:]))
    return tuple(vals)


def get_call_expr_arg(f_name, args, kws, arg_no, arg_name, default=None,
    err_msg=None, use_default=False):
    lgkti__dckvr = None
    if len(args) > arg_no and arg_no >= 0:
        lgkti__dckvr = args[arg_no]
        if arg_name in kws:
            err_msg = (
                f"{f_name}() got multiple values for argument '{arg_name}'")
            raise BodoError(err_msg)
    elif arg_name in kws:
        lgkti__dckvr = kws[arg_name]
    if lgkti__dckvr is None:
        if use_default or default is not None:
            return default
        if err_msg is None:
            err_msg = "{} requires '{}' argument".format(f_name, arg_name)
        raise BodoError(err_msg)
    return lgkti__dckvr


def set_call_expr_arg(var, args, kws, arg_no, arg_name, add_if_missing=False):
    if len(args) > arg_no:
        args[arg_no] = var
    elif add_if_missing or arg_name in kws:
        kws[arg_name] = var
    else:
        raise BodoError('cannot set call argument since does not exist')


def avoid_udf_inline(py_func, arg_types, kw_types):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    f_ir = numba.core.compiler.run_frontend(py_func, inline_closures=True)
    if '_bodo_inline' in kw_types and is_overload_constant_bool(kw_types[
        '_bodo_inline']):
        return not get_overload_const_bool(kw_types['_bodo_inline'])
    if any(isinstance(t, DataFrameType) for t in arg_types + tuple(kw_types
        .values())):
        return True
    for block in f_ir.blocks.values():
        if isinstance(block.body[-1], (ir.Raise, ir.StaticRaise)):
            return True
        for stmt in block.body:
            if isinstance(stmt, ir.EnterWith):
                return True
    return False


def replace_func(pass_info, func, args, const=False, pre_nodes=None,
    extra_globals=None, pysig=None, kws=None, inline_bodo_calls=False,
    run_full_pipeline=False):
    yza__vyum = {'numba': numba, 'np': np, 'bodo': bodo, 'pd': pd}
    if extra_globals is not None:
        yza__vyum.update(extra_globals)
    func.__globals__.update(yza__vyum)
    if pysig is not None:
        pre_nodes = [] if pre_nodes is None else pre_nodes
        scope = next(iter(pass_info.func_ir.blocks.values())).scope
        loc = scope.loc

        def normal_handler(index, param, default):
            return default

        def default_handler(index, param, default):
            iziau__bpkt = ir.Var(scope, mk_unique_var('defaults'), loc)
            try:
                pass_info.typemap[iziau__bpkt.name] = types.literal(default)
            except:
                pass_info.typemap[iziau__bpkt.name] = numba.typeof(default)
            unv__ryyyb = ir.Assign(ir.Const(default, loc), iziau__bpkt, loc)
            pre_nodes.append(unv__ryyyb)
            return iziau__bpkt
        args = numba.core.typing.fold_arguments(pysig, args, kws,
            normal_handler, default_handler, normal_handler)
    squej__wva = tuple(pass_info.typemap[xadll__ccx.name] for xadll__ccx in
        args)
    if const:
        nheuh__zpxr = []
        for ljpx__qttq, lgkti__dckvr in enumerate(args):
            vde__sxd = guard(find_const, pass_info.func_ir, lgkti__dckvr)
            if vde__sxd:
                nheuh__zpxr.append(types.literal(vde__sxd))
            else:
                nheuh__zpxr.append(squej__wva[ljpx__qttq])
        squej__wva = tuple(nheuh__zpxr)
    return ReplaceFunc(func, squej__wva, args, yza__vyum, inline_bodo_calls,
        run_full_pipeline, pre_nodes)


def is_var_size_item_array_type(t):
    assert is_array_typ(t, False)
    return t == string_array_type or isinstance(t, ArrayItemArrayType
        ) or isinstance(t, StructArrayType) and any(
        is_var_size_item_array_type(ljo__mvmcr) for ljo__mvmcr in t.data)


def gen_init_varsize_alloc_sizes(t):
    if t == string_array_type:
        mdug__wgcdi = 'num_chars_{}'.format(ir_utils.next_label())
        return f'  {mdug__wgcdi} = 0\n', (mdug__wgcdi,)
    if isinstance(t, ArrayItemArrayType):
        xewn__aee, styg__kcxo = gen_init_varsize_alloc_sizes(t.dtype)
        mdug__wgcdi = 'num_items_{}'.format(ir_utils.next_label())
        return f'  {mdug__wgcdi} = 0\n' + xewn__aee, (mdug__wgcdi,
            ) + styg__kcxo
    return '', ()


def gen_varsize_item_sizes(t, item, var_names):
    if t == string_array_type:
        return '    {} += bodo.libs.str_arr_ext.get_utf8_size({})\n'.format(
            var_names[0], item)
    if isinstance(t, ArrayItemArrayType):
        return '    {} += len({})\n'.format(var_names[0], item
            ) + gen_varsize_array_counts(t.dtype, item, var_names[1:])
    return ''


def gen_varsize_array_counts(t, item, var_names):
    if t == string_array_type:
        return ('    {} += bodo.libs.str_arr_ext.get_num_total_chars({})\n'
            .format(var_names[0], item))
    return ''


def get_type_alloc_counts(t):
    if isinstance(t, (StructArrayType, TupleArrayType)):
        return 1 + sum(get_type_alloc_counts(ljo__mvmcr.dtype) for
            ljo__mvmcr in t.data)
    if isinstance(t, ArrayItemArrayType) or t == string_array_type:
        return 1 + get_type_alloc_counts(t.dtype)
    if isinstance(t, MapArrayType):
        return get_type_alloc_counts(t.key_arr_type) + get_type_alloc_counts(t
            .value_arr_type)
    if bodo.utils.utils.is_array_typ(t, False) or t == bodo.string_type:
        return 1
    if isinstance(t, StructType):
        return sum(get_type_alloc_counts(ljo__mvmcr) for ljo__mvmcr in t.data)
    if isinstance(t, types.BaseTuple):
        return sum(get_type_alloc_counts(ljo__mvmcr) for ljo__mvmcr in t.types)
    return 0


def find_udf_str_name(obj_dtype, func_name, typing_context, caller_name):
    dojd__vqiy = typing_context.resolve_getattr(obj_dtype, func_name)
    if dojd__vqiy is None:
        dfx__ngnsw = types.misc.Module(np)
        try:
            dojd__vqiy = typing_context.resolve_getattr(dfx__ngnsw, func_name)
        except AttributeError as jnke__xicph:
            dojd__vqiy = None
        if dojd__vqiy is None:
            raise BodoError(
                f"{caller_name}(): No Pandas method or Numpy function found with the name '{func_name}'."
                )
    return dojd__vqiy


def get_udf_str_return_type(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    dojd__vqiy = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(dojd__vqiy, types.BoundFunction):
        if axis is not None:
            xwzn__zdnm = dojd__vqiy.get_call_type(typing_context, (), {
                'axis': axis})
        else:
            xwzn__zdnm = dojd__vqiy.get_call_type(typing_context, (), {})
        return xwzn__zdnm.return_type
    else:
        if bodo.utils.typing.is_numpy_ufunc(dojd__vqiy):
            xwzn__zdnm = dojd__vqiy.get_call_type(typing_context, (
                obj_dtype,), {})
            return xwzn__zdnm.return_type
        raise BodoError(
            f"{caller_name}(): Only Pandas methods and np.ufunc are supported as string literals. '{func_name}' not supported."
            )


def get_pandas_method_str_impl(obj_dtype, func_name, typing_context,
    caller_name, axis=None):
    dojd__vqiy = find_udf_str_name(obj_dtype, func_name, typing_context,
        caller_name)
    if isinstance(dojd__vqiy, types.BoundFunction):
        kqt__omsgd = dojd__vqiy.template
        if axis is not None:
            return kqt__omsgd._overload_func(obj_dtype, axis=axis)
        else:
            return kqt__omsgd._overload_func(obj_dtype)
    return None


def dict_to_const_keys_var_values_lists(dict_var, func_ir, arg_types,
    typemap, updated_containers, require_const_map, label):
    require(isinstance(dict_var, ir.Var))
    jvmmo__fuiq = get_definition(func_ir, dict_var)
    require(isinstance(jvmmo__fuiq, ir.Expr))
    require(jvmmo__fuiq.op == 'build_map')
    swoo__snh = jvmmo__fuiq.items
    lheqn__jgte = []
    values = []
    ivfe__obju = False
    for ljpx__qttq in range(len(swoo__snh)):
        jzte__qod, value = swoo__snh[ljpx__qttq]
        try:
            ptd__uuv = get_const_value_inner(func_ir, jzte__qod, arg_types,
                typemap, updated_containers)
            lheqn__jgte.append(ptd__uuv)
            values.append(value)
        except GuardException as jnke__xicph:
            require_const_map[jzte__qod] = label
            ivfe__obju = True
    if ivfe__obju:
        raise GuardException
    return lheqn__jgte, values


def _get_const_keys_from_dict(args, func_ir, build_map, err_msg, loc):
    try:
        lheqn__jgte = tuple(get_const_value_inner(func_ir, t[0], args) for
            t in build_map.items)
    except GuardException as jnke__xicph:
        raise BodoError(err_msg, loc)
    if not all(isinstance(c, (str, int)) for c in lheqn__jgte):
        raise BodoError(err_msg, loc)
    return lheqn__jgte


def _convert_const_key_dict(args, func_ir, build_map, err_msg, scope, loc,
    output_sentinel_tuple=False):
    lheqn__jgte = _get_const_keys_from_dict(args, func_ir, build_map,
        err_msg, loc)
    jvu__lhtyg = []
    cegi__iujdm = [bodo.transforms.typing_pass._create_const_var(okd__bcg,
        'dict_key', scope, loc, jvu__lhtyg) for okd__bcg in lheqn__jgte]
    kdm__foryh = [t[1] for t in build_map.items]
    if output_sentinel_tuple:
        bju__ihe = ir.Var(scope, mk_unique_var('sentinel'), loc)
        lqwy__lqjy = ir.Var(scope, mk_unique_var('dict_tup'), loc)
        jvu__lhtyg.append(ir.Assign(ir.Const('__bodo_tup', loc), bju__ihe, loc)
            )
        mjlwh__ssnx = [bju__ihe] + cegi__iujdm + kdm__foryh
        jvu__lhtyg.append(ir.Assign(ir.Expr.build_tuple(mjlwh__ssnx, loc),
            lqwy__lqjy, loc))
        return (lqwy__lqjy,), jvu__lhtyg
    else:
        phrun__gnq = ir.Var(scope, mk_unique_var('values_tup'), loc)
        vqrr__amzo = ir.Var(scope, mk_unique_var('idx_tup'), loc)
        jvu__lhtyg.append(ir.Assign(ir.Expr.build_tuple(kdm__foryh, loc),
            phrun__gnq, loc))
        jvu__lhtyg.append(ir.Assign(ir.Expr.build_tuple(cegi__iujdm, loc),
            vqrr__amzo, loc))
        return (phrun__gnq, vqrr__amzo), jvu__lhtyg
