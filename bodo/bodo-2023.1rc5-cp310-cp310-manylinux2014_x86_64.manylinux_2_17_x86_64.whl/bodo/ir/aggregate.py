"""IR node for the groupby"""
import ctypes
import operator
import types as pytypes
from collections import defaultdict, namedtuple
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, compiler, ir, ir_utils, types
from numba.core.analysis import compute_use_defs
from numba.core.ir_utils import build_definitions, compile_to_numba_ir, find_callname, find_const, find_topo_order, get_definition, get_ir_of_code, get_name_var_table, guard, is_getitem, mk_unique_var, next_label, remove_dels, replace_arg_nodes, replace_var_names, replace_vars_inner, visit_vars_inner
from numba.core.typing import signature
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic
from numba.parfors.parfor import Parfor, unwrap_parfor_blocks, wrap_parfor_blocks
import bodo
from bodo.hiframes.datetime_date_ext import DatetimeDateArrayType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.libs.array import arr_info_list_to_table, array_to_info, cpp_table_to_py_data, decref_table_array, delete_info_decref_array, delete_table, delete_table_decref_arrays, groupby_and_aggregate, info_from_table, info_to_array, py_data_to_cpp_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType, pre_alloc_array_item_array
from bodo.libs.binary_arr_ext import BinaryArrayType, pre_alloc_binary_array
from bodo.libs.bool_arr_ext import BooleanArrayType
from bodo.libs.decimal_arr_ext import DecimalArrayType, alloc_decimal_array
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import _compute_table_column_uses, _find_used_columns, ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.transform import get_call_expr_arg
from bodo.utils.typing import BodoError, MetaType, decode_if_dict_array, dtype_to_array_type, get_index_data_arr_types, get_literal_value, get_overload_const_func, get_overload_const_list, get_overload_const_str, get_overload_constant_dict, is_overload_constant_dict, is_overload_constant_list, is_overload_constant_str, list_cumulative, to_str_arr_if_dict_array, type_has_unknown_cats, unwrap_typeref
from bodo.utils.utils import gen_getitem, incref, is_assign, is_call_assign, is_expr, is_null_pointer, is_var_assign
gb_agg_cfunc = {}
gb_agg_cfunc_addr = {}


@intrinsic
def add_agg_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        ahetz__hugr = func.signature
        if ahetz__hugr == types.none(types.voidptr):
            aboq__xwgy = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer()])
            oafe__edhc = cgutils.get_or_insert_function(builder.module,
                aboq__xwgy, sym._literal_value)
            builder.call(oafe__edhc, [context.get_constant_null(ahetz__hugr
                .args[0])])
        elif ahetz__hugr == types.none(types.int64, types.voidptr, types.
            voidptr):
            aboq__xwgy = lir.FunctionType(lir.VoidType(), [lir.IntType(64),
                lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
            oafe__edhc = cgutils.get_or_insert_function(builder.module,
                aboq__xwgy, sym._literal_value)
            builder.call(oafe__edhc, [context.get_constant(types.int64, 0),
                context.get_constant_null(ahetz__hugr.args[1]), context.
                get_constant_null(ahetz__hugr.args[2])])
        else:
            aboq__xwgy = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
                as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64).
                as_pointer()])
            oafe__edhc = cgutils.get_or_insert_function(builder.module,
                aboq__xwgy, sym._literal_value)
            builder.call(oafe__edhc, [context.get_constant_null(ahetz__hugr
                .args[0]), context.get_constant_null(ahetz__hugr.args[1]),
                context.get_constant_null(ahetz__hugr.args[2])])
        context.add_linking_libs([gb_agg_cfunc[sym._literal_value]._library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_agg_udf_addr(name):
    with numba.objmode(addr='int64'):
        addr = gb_agg_cfunc_addr[name]
    return addr


class AggUDFStruct(object):

    def __init__(self, regular_udf_funcs=None, general_udf_funcs=None):
        assert regular_udf_funcs is not None or general_udf_funcs is not None
        self.regular_udfs = False
        self.general_udfs = False
        self.regular_udf_cfuncs = None
        self.general_udf_cfunc = None
        if regular_udf_funcs is not None:
            (self.var_typs, self.init_func, self.update_all_func, self.
                combine_all_func, self.eval_all_func) = regular_udf_funcs
            self.regular_udfs = True
        if general_udf_funcs is not None:
            self.general_udf_funcs = general_udf_funcs
            self.general_udfs = True

    def set_regular_cfuncs(self, update_cb, combine_cb, eval_cb):
        assert self.regular_udfs and self.regular_udf_cfuncs is None
        self.regular_udf_cfuncs = [update_cb, combine_cb, eval_cb]

    def set_general_cfunc(self, general_udf_cb):
        assert self.general_udfs and self.general_udf_cfunc is None
        self.general_udf_cfunc = general_udf_cb


AggFuncStruct = namedtuple('AggFuncStruct', ['func', 'ftype'])
supported_agg_funcs = ['no_op', 'ngroup', 'head', 'transform', 'size',
    'shift', 'sum', 'count', 'nunique', 'median', 'cumsum', 'cumprod',
    'cummin', 'cummax', 'mean', 'min', 'max', 'prod', 'first', 'last',
    'idxmin', 'idxmax', 'var', 'std', 'boolor_agg', 'udf', 'gen_udf']
supported_transform_funcs = ['no_op', 'sum', 'count', 'nunique', 'median',
    'mean', 'min', 'max', 'prod', 'first', 'last', 'var', 'std']


def get_agg_func(func_ir, func_name, rhs, series_type=None, typemap=None):
    if func_name == 'no_op':
        raise BodoError('Unknown aggregation function used in groupby.')
    if series_type is None:
        series_type = SeriesType(types.float64)
    if func_name in {'var', 'std'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 3
        func.ncols_post_shuffle = 4
        return func
    if func_name in {'first', 'last', 'boolor_agg'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        return func
    if func_name in {'idxmin', 'idxmax'}:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 2
        func.ncols_post_shuffle = 2
        return func
    if func_name in supported_agg_funcs[:-8]:
        func = pytypes.SimpleNamespace()
        func.ftype = func_name
        func.fname = func_name
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        qugff__uie = True
        zgvem__fkvve = 1
        caatx__kcrg = -1
        if isinstance(rhs, ir.Expr):
            for imc__wcyv in rhs.kws:
                if func_name in list_cumulative:
                    if imc__wcyv[0] == 'skipna':
                        qugff__uie = guard(find_const, func_ir, imc__wcyv[1])
                        if not isinstance(qugff__uie, bool):
                            raise BodoError(
                                'For {} argument of skipna should be a boolean'
                                .format(func_name))
                if func_name == 'nunique':
                    if imc__wcyv[0] == 'dropna':
                        qugff__uie = guard(find_const, func_ir, imc__wcyv[1])
                        if not isinstance(qugff__uie, bool):
                            raise BodoError(
                                'argument of dropna to nunique should be a boolean'
                                )
        if func_name == 'shift' and (len(rhs.args) > 0 or len(rhs.kws) > 0):
            zgvem__fkvve = get_call_expr_arg('shift', rhs.args, dict(rhs.
                kws), 0, 'periods', zgvem__fkvve)
            zgvem__fkvve = guard(find_const, func_ir, zgvem__fkvve)
        if func_name == 'head':
            caatx__kcrg = get_call_expr_arg('head', rhs.args, dict(rhs.kws),
                0, 'n', 5)
            if not isinstance(caatx__kcrg, int):
                caatx__kcrg = guard(find_const, func_ir, caatx__kcrg)
            if caatx__kcrg < 0:
                raise BodoError(
                    f'groupby.{func_name} does not work with negative values.')
        func.skipdropna = qugff__uie
        func.periods = zgvem__fkvve
        func.head_n = caatx__kcrg
        if func_name == 'transform':
            kws = dict(rhs.kws)
            zxagt__pxpw = get_call_expr_arg(func_name, rhs.args, kws, 0,
                'func', '')
            dmjxg__newaj = typemap[zxagt__pxpw.name]
            phmh__haa = None
            if isinstance(dmjxg__newaj, str):
                phmh__haa = dmjxg__newaj
            elif is_overload_constant_str(dmjxg__newaj):
                phmh__haa = get_overload_const_str(dmjxg__newaj)
            elif bodo.utils.typing.is_builtin_function(dmjxg__newaj):
                phmh__haa = bodo.utils.typing.get_builtin_function_name(
                    dmjxg__newaj)
            if phmh__haa not in bodo.ir.aggregate.supported_transform_funcs[:]:
                raise BodoError(f'unsupported transform function {phmh__haa}')
            func.transform_func = supported_agg_funcs.index(phmh__haa)
        else:
            func.transform_func = supported_agg_funcs.index('no_op')
        return func
    assert func_name in ['agg', 'aggregate']
    assert typemap is not None
    kws = dict(rhs.kws)
    zxagt__pxpw = get_call_expr_arg(func_name, rhs.args, kws, 0, 'func', '')
    if zxagt__pxpw == '':
        dmjxg__newaj = types.none
    else:
        dmjxg__newaj = typemap[zxagt__pxpw.name]
    if is_overload_constant_dict(dmjxg__newaj):
        tah__xhas = get_overload_constant_dict(dmjxg__newaj)
        ytwgc__cbn = [get_agg_func_udf(func_ir, f_val, rhs, series_type,
            typemap) for f_val in tah__xhas.values()]
        return ytwgc__cbn
    if dmjxg__newaj == types.none:
        return [get_agg_func_udf(func_ir, get_literal_value(typemap[f_val.
            name])[1], rhs, series_type, typemap) for f_val in kws.values()]
    if isinstance(dmjxg__newaj, types.BaseTuple) or is_overload_constant_list(
        dmjxg__newaj):
        ytwgc__cbn = []
        bshw__kyysg = 0
        if is_overload_constant_list(dmjxg__newaj):
            gmcqc__ija = get_overload_const_list(dmjxg__newaj)
        else:
            gmcqc__ija = dmjxg__newaj.types
        for t in gmcqc__ija:
            if is_overload_constant_str(t):
                func_name = get_overload_const_str(t)
                ytwgc__cbn.append(get_agg_func(func_ir, func_name, rhs,
                    series_type, typemap))
            else:
                assert typemap is not None, 'typemap is required for agg UDF handling'
                func = _get_const_agg_func(t, func_ir)
                func.ftype = 'udf'
                func.fname = _get_udf_name(func)
                if func.fname == '<lambda>' and len(gmcqc__ija) > 1:
                    func.fname = '<lambda_' + str(bshw__kyysg) + '>'
                    bshw__kyysg += 1
                ytwgc__cbn.append(func)
        return [ytwgc__cbn]
    if is_overload_constant_str(dmjxg__newaj):
        func_name = get_overload_const_str(dmjxg__newaj)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(dmjxg__newaj):
        func_name = bodo.utils.typing.get_builtin_function_name(dmjxg__newaj)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    assert typemap is not None, 'typemap is required for agg UDF handling'
    func = _get_const_agg_func(typemap[rhs.args[0].name], func_ir)
    func.ftype = 'udf'
    func.fname = _get_udf_name(func)
    return func


def get_agg_func_udf(func_ir, f_val, rhs, series_type, typemap):
    if isinstance(f_val, str):
        return get_agg_func(func_ir, f_val, rhs, series_type, typemap)
    if bodo.utils.typing.is_builtin_function(f_val):
        func_name = bodo.utils.typing.get_builtin_function_name(f_val)
        return get_agg_func(func_ir, func_name, rhs, series_type, typemap)
    if isinstance(f_val, (tuple, list)):
        bshw__kyysg = 0
        pbx__qyjq = []
        for jvg__fgzmj in f_val:
            func = get_agg_func_udf(func_ir, jvg__fgzmj, rhs, series_type,
                typemap)
            if func.fname == '<lambda>' and len(f_val) > 1:
                func.fname = f'<lambda_{bshw__kyysg}>'
                bshw__kyysg += 1
            pbx__qyjq.append(func)
        return pbx__qyjq
    else:
        assert is_expr(f_val, 'make_function') or isinstance(f_val, (numba.
            core.registry.CPUDispatcher, types.Dispatcher))
        assert typemap is not None, 'typemap is required for agg UDF handling'
        func = _get_const_agg_func(f_val, func_ir)
        func.ftype = 'udf'
        func.fname = _get_udf_name(func)
        return func


def _get_udf_name(func):
    code = func.code if hasattr(func, 'code') else func.__code__
    phmh__haa = code.co_name
    return phmh__haa


def _get_const_agg_func(func_typ, func_ir):
    agg_func = get_overload_const_func(func_typ, func_ir)
    if is_expr(agg_func, 'make_function'):

        def agg_func_wrapper(A):
            return A
        agg_func_wrapper.__code__ = agg_func.code
        agg_func = agg_func_wrapper
        return agg_func
    return agg_func


@infer_global(type)
class TypeDt64(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if len(args) == 1 and isinstance(args[0], (types.NPDatetime, types.
            NPTimedelta)):
            cge__xjg = types.DType(args[0])
            return signature(cge__xjg, *args)


class Aggregate(ir.Stmt):

    def __init__(self, df_out, df_in, key_names, gb_info_in, gb_info_out,
        out_vars, in_vars, in_key_inds, df_in_type, out_type,
        input_has_index, same_index, return_key, loc, func_name, dropna,
        _num_shuffle_keys):
        self.df_out = df_out
        self.df_in = df_in
        self.key_names = key_names
        self.gb_info_in = gb_info_in
        self.gb_info_out = gb_info_out
        self.out_vars = out_vars
        self.in_vars = in_vars
        self.in_key_inds = in_key_inds
        self.df_in_type = df_in_type
        self.out_type = out_type
        self.input_has_index = input_has_index
        self.same_index = same_index
        self.return_key = return_key
        self.loc = loc
        self.func_name = func_name
        self.dropna = dropna
        self._num_shuffle_keys = _num_shuffle_keys
        self.dead_in_inds = set()
        self.dead_out_inds = set()

    def get_live_in_vars(self):
        return [axdy__tdda for axdy__tdda in self.in_vars if axdy__tdda is not
            None]

    def get_live_out_vars(self):
        return [axdy__tdda for axdy__tdda in self.out_vars if axdy__tdda is not
            None]

    @property
    def is_in_table_format(self):
        return self.df_in_type.is_table_format

    @property
    def n_in_table_arrays(self):
        return len(self.df_in_type.columns
            ) if self.df_in_type.is_table_format else 1

    @property
    def n_in_cols(self):
        return self.n_in_table_arrays + len(self.in_vars) - 1

    @property
    def in_col_types(self):
        return list(self.df_in_type.data) + list(get_index_data_arr_types(
            self.df_in_type.index))

    @property
    def is_output_table(self):
        return not isinstance(self.out_type, SeriesType)

    @property
    def n_out_table_arrays(self):
        return len(self.out_type.table_type.arr_types) if not isinstance(self
            .out_type, SeriesType) else 1

    @property
    def n_out_cols(self):
        return self.n_out_table_arrays + len(self.out_vars) - 1

    @property
    def out_col_types(self):
        csthy__gtilt = [self.out_type.data] if isinstance(self.out_type,
            SeriesType) else list(self.out_type.table_type.arr_types)
        oyqs__xmjz = list(get_index_data_arr_types(self.out_type.index))
        return csthy__gtilt + oyqs__xmjz

    def update_dead_col_info(self):
        for dbvin__aciyf in self.dead_out_inds:
            self.gb_info_out.pop(dbvin__aciyf, None)
        if not self.input_has_index:
            self.dead_in_inds.add(self.n_in_cols - 1)
            self.dead_out_inds.add(self.n_out_cols - 1)
        for zdxhu__jsdbo, gyum__drp in self.gb_info_in.copy().items():
            wfar__wjfo = []
            for jvg__fgzmj, ofe__efuq in gyum__drp:
                if ofe__efuq not in self.dead_out_inds:
                    wfar__wjfo.append((jvg__fgzmj, ofe__efuq))
            if not wfar__wjfo:
                if (zdxhu__jsdbo is not None and zdxhu__jsdbo not in self.
                    in_key_inds):
                    self.dead_in_inds.add(zdxhu__jsdbo)
                self.gb_info_in.pop(zdxhu__jsdbo)
            else:
                self.gb_info_in[zdxhu__jsdbo] = wfar__wjfo
        if self.is_in_table_format:
            if not set(range(self.n_in_table_arrays)) - self.dead_in_inds:
                self.in_vars[0] = None
            for eyg__qpy in range(1, len(self.in_vars)):
                dbvin__aciyf = self.n_in_table_arrays + eyg__qpy - 1
                if dbvin__aciyf in self.dead_in_inds:
                    self.in_vars[eyg__qpy] = None
        else:
            for eyg__qpy in range(len(self.in_vars)):
                if eyg__qpy in self.dead_in_inds:
                    self.in_vars[eyg__qpy] = None

    def __repr__(self):
        lwvpx__eyuse = ', '.join(axdy__tdda.name for axdy__tdda in self.
            get_live_in_vars())
        hie__opj = f'{self.df_in}{{{lwvpx__eyuse}}}'
        vemor__bsify = ', '.join(axdy__tdda.name for axdy__tdda in self.
            get_live_out_vars())
        bwh__joj = f'{self.df_out}{{{vemor__bsify}}}'
        return (
            f'Groupby (keys: {self.key_names} {self.in_key_inds}): {hie__opj} {bwh__joj}'
            )


def aggregate_usedefs(aggregate_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({axdy__tdda.name for axdy__tdda in aggregate_node.
        get_live_in_vars()})
    def_set.update({axdy__tdda.name for axdy__tdda in aggregate_node.
        get_live_out_vars()})
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Aggregate] = aggregate_usedefs


def remove_dead_aggregate(agg_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    deozt__kteh = agg_node.out_vars[0]
    if deozt__kteh is not None and deozt__kteh.name not in lives:
        agg_node.out_vars[0] = None
        if agg_node.is_output_table:
            dxuyt__tshyv = set(range(agg_node.n_out_table_arrays))
            agg_node.dead_out_inds.update(dxuyt__tshyv)
        else:
            agg_node.dead_out_inds.add(0)
    for eyg__qpy in range(1, len(agg_node.out_vars)):
        axdy__tdda = agg_node.out_vars[eyg__qpy]
        if axdy__tdda is not None and axdy__tdda.name not in lives:
            agg_node.out_vars[eyg__qpy] = None
            dbvin__aciyf = agg_node.n_out_table_arrays + eyg__qpy - 1
            agg_node.dead_out_inds.add(dbvin__aciyf)
    if all(axdy__tdda is None for axdy__tdda in agg_node.out_vars):
        return None
    agg_node.update_dead_col_info()
    return agg_node


ir_utils.remove_dead_extensions[Aggregate] = remove_dead_aggregate


def get_copies_aggregate(aggregate_node, typemap):
    bkcv__jrk = {axdy__tdda.name for axdy__tdda in aggregate_node.
        get_live_out_vars()}
    return set(), bkcv__jrk


ir_utils.copy_propagate_extensions[Aggregate] = get_copies_aggregate


def apply_copies_aggregate(aggregate_node, var_dict, name_var_table,
    typemap, calltypes, save_copies):
    for eyg__qpy in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[eyg__qpy] is not None:
            aggregate_node.in_vars[eyg__qpy] = replace_vars_inner(
                aggregate_node.in_vars[eyg__qpy], var_dict)
    for eyg__qpy in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[eyg__qpy] is not None:
            aggregate_node.out_vars[eyg__qpy] = replace_vars_inner(
                aggregate_node.out_vars[eyg__qpy], var_dict)


ir_utils.apply_copy_propagate_extensions[Aggregate] = apply_copies_aggregate


def visit_vars_aggregate(aggregate_node, callback, cbdata):
    for eyg__qpy in range(len(aggregate_node.in_vars)):
        if aggregate_node.in_vars[eyg__qpy] is not None:
            aggregate_node.in_vars[eyg__qpy] = visit_vars_inner(aggregate_node
                .in_vars[eyg__qpy], callback, cbdata)
    for eyg__qpy in range(len(aggregate_node.out_vars)):
        if aggregate_node.out_vars[eyg__qpy] is not None:
            aggregate_node.out_vars[eyg__qpy] = visit_vars_inner(aggregate_node
                .out_vars[eyg__qpy], callback, cbdata)


ir_utils.visit_vars_extensions[Aggregate] = visit_vars_aggregate


def aggregate_array_analysis(aggregate_node, equiv_set, typemap, array_analysis
    ):
    yju__htyhi = []
    for tewo__pzm in aggregate_node.get_live_in_vars():
        ttz__extwt = equiv_set.get_shape(tewo__pzm)
        if ttz__extwt is not None:
            yju__htyhi.append(ttz__extwt[0])
    if len(yju__htyhi) > 1:
        equiv_set.insert_equiv(*yju__htyhi)
    ddl__xdz = []
    yju__htyhi = []
    for tewo__pzm in aggregate_node.get_live_out_vars():
        oyxx__bbmfu = typemap[tewo__pzm.name]
        fiel__ecsya = array_analysis._gen_shape_call(equiv_set, tewo__pzm,
            oyxx__bbmfu.ndim, None, ddl__xdz)
        equiv_set.insert_equiv(tewo__pzm, fiel__ecsya)
        yju__htyhi.append(fiel__ecsya[0])
        equiv_set.define(tewo__pzm, set())
    if len(yju__htyhi) > 1:
        equiv_set.insert_equiv(*yju__htyhi)
    return [], ddl__xdz


numba.parfors.array_analysis.array_analysis_extensions[Aggregate
    ] = aggregate_array_analysis


def aggregate_distributed_analysis(aggregate_node, array_dists):
    rlth__hyrd = aggregate_node.get_live_in_vars()
    fveqs__hfu = aggregate_node.get_live_out_vars()
    jmdj__mru = Distribution.OneD
    for tewo__pzm in rlth__hyrd:
        jmdj__mru = Distribution(min(jmdj__mru.value, array_dists[tewo__pzm
            .name].value))
    csh__moip = Distribution(min(jmdj__mru.value, Distribution.OneD_Var.value))
    for tewo__pzm in fveqs__hfu:
        if tewo__pzm.name in array_dists:
            csh__moip = Distribution(min(csh__moip.value, array_dists[
                tewo__pzm.name].value))
    if csh__moip != Distribution.OneD_Var:
        jmdj__mru = csh__moip
    for tewo__pzm in rlth__hyrd:
        array_dists[tewo__pzm.name] = jmdj__mru
    for tewo__pzm in fveqs__hfu:
        array_dists[tewo__pzm.name] = csh__moip


distributed_analysis.distributed_analysis_extensions[Aggregate
    ] = aggregate_distributed_analysis


def build_agg_definitions(agg_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for tewo__pzm in agg_node.get_live_out_vars():
        definitions[tewo__pzm.name].append(agg_node)
    return definitions


ir_utils.build_defs_extensions[Aggregate] = build_agg_definitions


def __update_redvars():
    pass


@infer_global(__update_redvars)
class UpdateDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __combine_redvars():
    pass


@infer_global(__combine_redvars)
class CombineDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(types.void, *args)


def __eval_res():
    pass


@infer_global(__eval_res)
class EvalDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(args[0].dtype, *args)


def agg_distributed_run(agg_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    xrj__bekku = agg_node.get_live_in_vars()
    begnp__nsq = agg_node.get_live_out_vars()
    if array_dists is not None:
        parallel = True
        for axdy__tdda in (xrj__bekku + begnp__nsq):
            if array_dists[axdy__tdda.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                axdy__tdda.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    out_col_typs = agg_node.out_col_types
    in_col_typs = []
    ytwgc__cbn = []
    func_out_types = []
    for ofe__efuq, (zdxhu__jsdbo, func) in agg_node.gb_info_out.items():
        if zdxhu__jsdbo is not None:
            t = agg_node.in_col_types[zdxhu__jsdbo]
            in_col_typs.append(t)
        ytwgc__cbn.append(func)
        func_out_types.append(out_col_typs[ofe__efuq])
    hvz__fwje = {'bodo': bodo, 'np': np, 'dt64_dtype': np.dtype(
        'datetime64[ns]'), 'td64_dtype': np.dtype('timedelta64[ns]')}
    for eyg__qpy, in_col_typ in enumerate(in_col_typs):
        if isinstance(in_col_typ, bodo.CategoricalArrayType):
            hvz__fwje.update({f'in_cat_dtype_{eyg__qpy}': in_col_typ})
    for eyg__qpy, qqy__umq in enumerate(out_col_typs):
        if isinstance(qqy__umq, bodo.CategoricalArrayType):
            hvz__fwje.update({f'out_cat_dtype_{eyg__qpy}': qqy__umq})
    udf_func_struct = get_udf_func_struct(ytwgc__cbn, in_col_typs,
        typingctx, targetctx)
    out_var_types = [(typemap[axdy__tdda.name] if axdy__tdda is not None else
        types.none) for axdy__tdda in agg_node.out_vars]
    rbgk__vkj, yninm__bly = gen_top_level_agg_func(agg_node, in_col_typs,
        out_col_typs, func_out_types, parallel, udf_func_struct,
        out_var_types, typemap)
    hvz__fwje.update(yninm__bly)
    hvz__fwje.update({'pd': pd, 'pre_alloc_string_array':
        pre_alloc_string_array, 'pre_alloc_binary_array':
        pre_alloc_binary_array, 'pre_alloc_array_item_array':
        pre_alloc_array_item_array, 'string_array_type': string_array_type,
        'alloc_decimal_array': alloc_decimal_array, 'array_to_info':
        array_to_info, 'arr_info_list_to_table': arr_info_list_to_table,
        'coerce_to_array': bodo.utils.conversion.coerce_to_array,
        'groupby_and_aggregate': groupby_and_aggregate, 'info_from_table':
        info_from_table, 'info_to_array': info_to_array,
        'delete_info_decref_array': delete_info_decref_array,
        'delete_table': delete_table, 'add_agg_cfunc_sym':
        add_agg_cfunc_sym, 'get_agg_udf_addr': get_agg_udf_addr,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'decref_table_array': decref_table_array, 'decode_if_dict_array':
        decode_if_dict_array, 'set_table_data': bodo.hiframes.table.
        set_table_data, 'get_table_data': bodo.hiframes.table.
        get_table_data, 'out_typs': out_col_typs})
    if udf_func_struct is not None:
        if udf_func_struct.regular_udfs:
            hvz__fwje.update({'__update_redvars': udf_func_struct.
                update_all_func, '__init_func': udf_func_struct.init_func,
                '__combine_redvars': udf_func_struct.combine_all_func,
                '__eval_res': udf_func_struct.eval_all_func,
                'cpp_cb_update': udf_func_struct.regular_udf_cfuncs[0],
                'cpp_cb_combine': udf_func_struct.regular_udf_cfuncs[1],
                'cpp_cb_eval': udf_func_struct.regular_udf_cfuncs[2]})
        if udf_func_struct.general_udfs:
            hvz__fwje.update({'cpp_cb_general': udf_func_struct.
                general_udf_cfunc})
    qud__meeg = {}
    exec(rbgk__vkj, {}, qud__meeg)
    rbu__zxlf = qud__meeg['agg_top']
    puaj__xff = compile_to_numba_ir(rbu__zxlf, hvz__fwje, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[axdy__tdda.
        name] for axdy__tdda in xrj__bekku), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(puaj__xff, xrj__bekku)
    oyhwy__nefy = puaj__xff.body[-2].value.value
    dfrpk__moy = puaj__xff.body[:-2]
    for eyg__qpy, axdy__tdda in enumerate(begnp__nsq):
        gen_getitem(axdy__tdda, oyhwy__nefy, eyg__qpy, calltypes, dfrpk__moy)
    return dfrpk__moy


distributed_pass.distributed_run_extensions[Aggregate] = agg_distributed_run


def _gen_dummy_alloc(t, colnum=0, is_input=False):
    if isinstance(t, IntegerArrayType):
        qkx__aji = IntDtype(t.dtype).name
        assert qkx__aji.endswith('Dtype()')
        qkx__aji = qkx__aji[:-7]
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1], dtype='{qkx__aji}'))"
            )
    elif isinstance(t, FloatingArrayType):
        return (
            f"bodo.hiframes.pd_series_ext.get_series_data(pd.Series([1.0], dtype='{t.dtype}'))"
            )
    elif isinstance(t, BooleanArrayType):
        return (
            'bodo.libs.bool_arr_ext.init_bool_array(np.empty(0, np.bool_), np.empty(0, np.uint8))'
            )
    elif isinstance(t, StringArrayType):
        return 'pre_alloc_string_array(1, 1)'
    elif t == bodo.dict_str_arr_type:
        return (
            'bodo.libs.dict_arr_ext.init_dict_arr(pre_alloc_string_array(1, 1), bodo.libs.int_arr_ext.alloc_int_array(1, np.int32), False, False)'
            )
    elif isinstance(t, BinaryArrayType):
        return 'pre_alloc_binary_array(1, 1)'
    elif t == ArrayItemArrayType(string_array_type):
        return 'pre_alloc_array_item_array(1, (1, 1), string_array_type)'
    elif isinstance(t, DecimalArrayType):
        return 'alloc_decimal_array(1, {}, {})'.format(t.precision, t.scale)
    elif isinstance(t, DatetimeDateArrayType):
        return (
            'bodo.hiframes.datetime_date_ext.init_datetime_date_array(np.empty(1, np.int64), np.empty(1, np.uint8))'
            )
    elif isinstance(t, bodo.CategoricalArrayType):
        if t.dtype.categories is None:
            raise BodoError(
                'Groupby agg operations on Categorical types require constant categories'
                )
        rpejf__sijtb = 'in' if is_input else 'out'
        return (
            f'bodo.utils.utils.alloc_type(1, {rpejf__sijtb}_cat_dtype_{colnum})'
            )
    else:
        return 'np.empty(1, {})'.format(_get_np_dtype(t.dtype))


def _get_np_dtype(t):
    if t == types.bool_:
        return 'np.bool_'
    if t == types.NPDatetime('ns'):
        return 'dt64_dtype'
    if t == types.NPTimedelta('ns'):
        return 'td64_dtype'
    return 'np.{}'.format(t)


def gen_update_cb(udf_func_struct, allfuncs, n_keys, data_in_typs_,
    do_combine, func_idx_to_in_col, label_suffix):
    mtc__vuoua = udf_func_struct.var_typs
    hhf__duqqn = len(mtc__vuoua)
    rbgk__vkj = (
        'def bodo_gb_udf_update_local{}(in_table, out_table, row_to_group):\n'
        .format(label_suffix))
    rbgk__vkj += '    if is_null_pointer(in_table):\n'
    rbgk__vkj += '        return\n'
    rbgk__vkj += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in mtc__vuoua]), 
        ',' if len(mtc__vuoua) == 1 else '')
    sezc__wgn = n_keys
    eek__ovcu = []
    redvar_offsets = []
    klem__wcek = []
    if do_combine:
        for eyg__qpy, jvg__fgzmj in enumerate(allfuncs):
            if jvg__fgzmj.ftype != 'udf':
                sezc__wgn += jvg__fgzmj.ncols_pre_shuffle
            else:
                redvar_offsets += list(range(sezc__wgn, sezc__wgn +
                    jvg__fgzmj.n_redvars))
                sezc__wgn += jvg__fgzmj.n_redvars
                klem__wcek.append(data_in_typs_[func_idx_to_in_col[eyg__qpy]])
                eek__ovcu.append(func_idx_to_in_col[eyg__qpy] + n_keys)
    else:
        for eyg__qpy, jvg__fgzmj in enumerate(allfuncs):
            if jvg__fgzmj.ftype != 'udf':
                sezc__wgn += jvg__fgzmj.ncols_post_shuffle
            else:
                redvar_offsets += list(range(sezc__wgn + 1, sezc__wgn + 1 +
                    jvg__fgzmj.n_redvars))
                sezc__wgn += jvg__fgzmj.n_redvars + 1
                klem__wcek.append(data_in_typs_[func_idx_to_in_col[eyg__qpy]])
                eek__ovcu.append(func_idx_to_in_col[eyg__qpy] + n_keys)
    assert len(redvar_offsets) == hhf__duqqn
    rbypp__ojper = len(klem__wcek)
    ylq__wjmps = []
    for eyg__qpy, t in enumerate(klem__wcek):
        ylq__wjmps.append(_gen_dummy_alloc(t, eyg__qpy, True))
    rbgk__vkj += '    data_in_dummy = ({}{})\n'.format(','.join(ylq__wjmps),
        ',' if len(klem__wcek) == 1 else '')
    rbgk__vkj += """
    # initialize redvar cols
"""
    rbgk__vkj += '    init_vals = __init_func()\n'
    for eyg__qpy in range(hhf__duqqn):
        rbgk__vkj += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(eyg__qpy, redvar_offsets[eyg__qpy], eyg__qpy))
        rbgk__vkj += '    incref(redvar_arr_{})\n'.format(eyg__qpy)
        rbgk__vkj += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(eyg__qpy,
            eyg__qpy)
    rbgk__vkj += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(eyg__qpy) for eyg__qpy in range(hhf__duqqn)]), ',' if 
        hhf__duqqn == 1 else '')
    rbgk__vkj += '\n'
    for eyg__qpy in range(rbypp__ojper):
        rbgk__vkj += (
            """    data_in_{} = info_to_array(info_from_table(in_table, {}), data_in_dummy[{}])
"""
            .format(eyg__qpy, eek__ovcu[eyg__qpy], eyg__qpy))
        rbgk__vkj += '    incref(data_in_{})\n'.format(eyg__qpy)
    rbgk__vkj += '    data_in = ({}{})\n'.format(','.join(['data_in_{}'.
        format(eyg__qpy) for eyg__qpy in range(rbypp__ojper)]), ',' if 
        rbypp__ojper == 1 else '')
    rbgk__vkj += '\n'
    rbgk__vkj += '    for i in range(len(data_in_0)):\n'
    rbgk__vkj += '        w_ind = row_to_group[i]\n'
    rbgk__vkj += '        if w_ind != -1:\n'
    rbgk__vkj += '            __update_redvars(redvars, data_in, w_ind, i)\n'
    qud__meeg = {}
    exec(rbgk__vkj, {'bodo': bodo, 'np': np, 'pd': pd, 'info_to_array':
        info_to_array, 'info_from_table': info_from_table, 'incref': incref,
        'pre_alloc_string_array': pre_alloc_string_array, '__init_func':
        udf_func_struct.init_func, '__update_redvars': udf_func_struct.
        update_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, qud__meeg)
    return qud__meeg['bodo_gb_udf_update_local{}'.format(label_suffix)]


def gen_combine_cb(udf_func_struct, allfuncs, n_keys, label_suffix):
    mtc__vuoua = udf_func_struct.var_typs
    hhf__duqqn = len(mtc__vuoua)
    rbgk__vkj = (
        'def bodo_gb_udf_combine{}(in_table, out_table, row_to_group):\n'.
        format(label_suffix))
    rbgk__vkj += '    if is_null_pointer(in_table):\n'
    rbgk__vkj += '        return\n'
    rbgk__vkj += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in mtc__vuoua]), 
        ',' if len(mtc__vuoua) == 1 else '')
    inuqp__mgnd = n_keys
    sgo__fzfm = n_keys
    dhymd__iiuo = []
    qlak__hene = []
    for jvg__fgzmj in allfuncs:
        if jvg__fgzmj.ftype != 'udf':
            inuqp__mgnd += jvg__fgzmj.ncols_pre_shuffle
            sgo__fzfm += jvg__fgzmj.ncols_post_shuffle
        else:
            dhymd__iiuo += list(range(inuqp__mgnd, inuqp__mgnd + jvg__fgzmj
                .n_redvars))
            qlak__hene += list(range(sgo__fzfm + 1, sgo__fzfm + 1 +
                jvg__fgzmj.n_redvars))
            inuqp__mgnd += jvg__fgzmj.n_redvars
            sgo__fzfm += 1 + jvg__fgzmj.n_redvars
    assert len(dhymd__iiuo) == hhf__duqqn
    rbgk__vkj += """
    # initialize redvar cols
"""
    rbgk__vkj += '    init_vals = __init_func()\n'
    for eyg__qpy in range(hhf__duqqn):
        rbgk__vkj += (
            """    redvar_arr_{} = info_to_array(info_from_table(out_table, {}), data_redvar_dummy[{}])
"""
            .format(eyg__qpy, qlak__hene[eyg__qpy], eyg__qpy))
        rbgk__vkj += '    incref(redvar_arr_{})\n'.format(eyg__qpy)
        rbgk__vkj += '    redvar_arr_{}.fill(init_vals[{}])\n'.format(eyg__qpy,
            eyg__qpy)
    rbgk__vkj += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(eyg__qpy) for eyg__qpy in range(hhf__duqqn)]), ',' if 
        hhf__duqqn == 1 else '')
    rbgk__vkj += '\n'
    for eyg__qpy in range(hhf__duqqn):
        rbgk__vkj += (
            """    recv_redvar_arr_{} = info_to_array(info_from_table(in_table, {}), data_redvar_dummy[{}])
"""
            .format(eyg__qpy, dhymd__iiuo[eyg__qpy], eyg__qpy))
        rbgk__vkj += '    incref(recv_redvar_arr_{})\n'.format(eyg__qpy)
    rbgk__vkj += '    recv_redvars = ({}{})\n'.format(','.join([
        'recv_redvar_arr_{}'.format(eyg__qpy) for eyg__qpy in range(
        hhf__duqqn)]), ',' if hhf__duqqn == 1 else '')
    rbgk__vkj += '\n'
    if hhf__duqqn:
        rbgk__vkj += '    for i in range(len(recv_redvar_arr_0)):\n'
        rbgk__vkj += '        w_ind = row_to_group[i]\n'
        rbgk__vkj += (
            '        __combine_redvars(redvars, recv_redvars, w_ind, i)\n')
    qud__meeg = {}
    exec(rbgk__vkj, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__init_func':
        udf_func_struct.init_func, '__combine_redvars': udf_func_struct.
        combine_all_func, 'is_null_pointer': is_null_pointer, 'dt64_dtype':
        np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, qud__meeg)
    return qud__meeg['bodo_gb_udf_combine{}'.format(label_suffix)]


def gen_eval_cb(udf_func_struct, allfuncs, n_keys, out_data_typs_, label_suffix
    ):
    mtc__vuoua = udf_func_struct.var_typs
    hhf__duqqn = len(mtc__vuoua)
    sezc__wgn = n_keys
    redvar_offsets = []
    lnt__qda = []
    osa__pgyiz = []
    for eyg__qpy, jvg__fgzmj in enumerate(allfuncs):
        if jvg__fgzmj.ftype != 'udf':
            sezc__wgn += jvg__fgzmj.ncols_post_shuffle
        else:
            lnt__qda.append(sezc__wgn)
            redvar_offsets += list(range(sezc__wgn + 1, sezc__wgn + 1 +
                jvg__fgzmj.n_redvars))
            sezc__wgn += 1 + jvg__fgzmj.n_redvars
            osa__pgyiz.append(out_data_typs_[eyg__qpy])
    assert len(redvar_offsets) == hhf__duqqn
    rbypp__ojper = len(osa__pgyiz)
    rbgk__vkj = 'def bodo_gb_udf_eval{}(table):\n'.format(label_suffix)
    rbgk__vkj += '    if is_null_pointer(table):\n'
    rbgk__vkj += '        return\n'
    rbgk__vkj += '    data_redvar_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t)) for t in mtc__vuoua]), 
        ',' if len(mtc__vuoua) == 1 else '')
    rbgk__vkj += '    out_data_dummy = ({}{})\n'.format(','.join([
        'np.empty(1, {})'.format(_get_np_dtype(t.dtype)) for t in
        osa__pgyiz]), ',' if len(osa__pgyiz) == 1 else '')
    for eyg__qpy in range(hhf__duqqn):
        rbgk__vkj += (
            """    redvar_arr_{} = info_to_array(info_from_table(table, {}), data_redvar_dummy[{}])
"""
            .format(eyg__qpy, redvar_offsets[eyg__qpy], eyg__qpy))
        rbgk__vkj += '    incref(redvar_arr_{})\n'.format(eyg__qpy)
    rbgk__vkj += '    redvars = ({}{})\n'.format(','.join(['redvar_arr_{}'.
        format(eyg__qpy) for eyg__qpy in range(hhf__duqqn)]), ',' if 
        hhf__duqqn == 1 else '')
    rbgk__vkj += '\n'
    for eyg__qpy in range(rbypp__ojper):
        rbgk__vkj += (
            """    data_out_{} = info_to_array(info_from_table(table, {}), out_data_dummy[{}])
"""
            .format(eyg__qpy, lnt__qda[eyg__qpy], eyg__qpy))
        rbgk__vkj += '    incref(data_out_{})\n'.format(eyg__qpy)
    rbgk__vkj += '    data_out = ({}{})\n'.format(','.join(['data_out_{}'.
        format(eyg__qpy) for eyg__qpy in range(rbypp__ojper)]), ',' if 
        rbypp__ojper == 1 else '')
    rbgk__vkj += '\n'
    rbgk__vkj += '    for i in range(len(data_out_0)):\n'
    rbgk__vkj += '        __eval_res(redvars, data_out, i)\n'
    qud__meeg = {}
    exec(rbgk__vkj, {'np': np, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref, '__eval_res':
        udf_func_struct.eval_all_func, 'is_null_pointer': is_null_pointer,
        'dt64_dtype': np.dtype('datetime64[ns]'), 'td64_dtype': np.dtype(
        'timedelta64[ns]')}, qud__meeg)
    return qud__meeg['bodo_gb_udf_eval{}'.format(label_suffix)]


def gen_general_udf_cb(udf_func_struct, allfuncs, n_keys, in_col_typs,
    out_col_typs, func_idx_to_in_col, label_suffix):
    sezc__wgn = n_keys
    cjleb__euwjw = []
    for eyg__qpy, jvg__fgzmj in enumerate(allfuncs):
        if jvg__fgzmj.ftype == 'gen_udf':
            cjleb__euwjw.append(sezc__wgn)
            sezc__wgn += 1
        elif jvg__fgzmj.ftype != 'udf':
            sezc__wgn += jvg__fgzmj.ncols_post_shuffle
        else:
            sezc__wgn += jvg__fgzmj.n_redvars + 1
    rbgk__vkj = (
        'def bodo_gb_apply_general_udfs{}(num_groups, in_table, out_table):\n'
        .format(label_suffix))
    rbgk__vkj += '    if num_groups == 0:\n'
    rbgk__vkj += '        return\n'
    for eyg__qpy, func in enumerate(udf_func_struct.general_udf_funcs):
        rbgk__vkj += '    # col {}\n'.format(eyg__qpy)
        rbgk__vkj += (
            """    out_col = info_to_array(info_from_table(out_table, {}), out_col_{}_typ)
"""
            .format(cjleb__euwjw[eyg__qpy], eyg__qpy))
        rbgk__vkj += '    incref(out_col)\n'
        rbgk__vkj += '    for j in range(num_groups):\n'
        rbgk__vkj += (
            """        in_col = info_to_array(info_from_table(in_table, {}*num_groups + j), in_col_{}_typ)
"""
            .format(eyg__qpy, eyg__qpy))
        rbgk__vkj += '        incref(in_col)\n'
        rbgk__vkj += (
            '        out_col[j] = func_{}(pd.Series(in_col))  # func returns scalar\n'
            .format(eyg__qpy))
    hvz__fwje = {'pd': pd, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'incref': incref}
    qdns__hcfe = 0
    for eyg__qpy, func in enumerate(allfuncs):
        if func.ftype != 'gen_udf':
            continue
        func = udf_func_struct.general_udf_funcs[qdns__hcfe]
        hvz__fwje['func_{}'.format(qdns__hcfe)] = func
        hvz__fwje['in_col_{}_typ'.format(qdns__hcfe)] = in_col_typs[
            func_idx_to_in_col[eyg__qpy]]
        hvz__fwje['out_col_{}_typ'.format(qdns__hcfe)] = out_col_typs[eyg__qpy]
        qdns__hcfe += 1
    qud__meeg = {}
    exec(rbgk__vkj, hvz__fwje, qud__meeg)
    jvg__fgzmj = qud__meeg['bodo_gb_apply_general_udfs{}'.format(label_suffix)]
    goaa__fbgi = types.void(types.int64, types.voidptr, types.voidptr)
    return numba.cfunc(goaa__fbgi, nopython=True)(jvg__fgzmj)


def gen_top_level_agg_func(agg_node, in_col_typs, out_col_typs,
    func_out_types, parallel, udf_func_struct, out_var_types, typemap):
    n_keys = len(agg_node.in_key_inds)
    uen__vqo = len(agg_node.out_vars)
    if agg_node.same_index:
        assert agg_node.input_has_index, 'agg codegen: input_has_index=True required for same_index=True'
    if agg_node.is_in_table_format:
        chzxr__icoa = []
        if agg_node.in_vars[0] is not None:
            chzxr__icoa.append('arg0')
        for eyg__qpy in range(agg_node.n_in_table_arrays, agg_node.n_in_cols):
            if eyg__qpy not in agg_node.dead_in_inds:
                chzxr__icoa.append(f'arg{eyg__qpy}')
    else:
        chzxr__icoa = [f'arg{eyg__qpy}' for eyg__qpy, axdy__tdda in
            enumerate(agg_node.in_vars) if axdy__tdda is not None]
    rbgk__vkj = f"def agg_top({', '.join(chzxr__icoa)}):\n"
    sza__afbq = []
    if agg_node.is_in_table_format:
        sza__afbq = agg_node.in_key_inds + [zdxhu__jsdbo for zdxhu__jsdbo,
            qvi__ouqa in agg_node.gb_info_out.values() if zdxhu__jsdbo is not
            None]
        if agg_node.input_has_index:
            sza__afbq.append(agg_node.n_in_cols - 1)
        ikil__xda = ',' if len(agg_node.in_vars) - 1 == 1 else ''
        qmlwt__ulmf = []
        for eyg__qpy in range(agg_node.n_in_table_arrays, agg_node.n_in_cols):
            if eyg__qpy in agg_node.dead_in_inds:
                qmlwt__ulmf.append('None')
            else:
                qmlwt__ulmf.append(f'arg{eyg__qpy}')
        szm__rmnnp = 'arg0' if agg_node.in_vars[0] is not None else 'None'
        rbgk__vkj += f"""    table = py_data_to_cpp_table({szm__rmnnp}, ({', '.join(qmlwt__ulmf)}{ikil__xda}), in_col_inds, {agg_node.n_in_table_arrays})
"""
    else:
        jzzf__mwf = [f'arg{eyg__qpy}' for eyg__qpy in agg_node.in_key_inds]
        oxqs__zxuz = [f'arg{zdxhu__jsdbo}' for zdxhu__jsdbo, qvi__ouqa in
            agg_node.gb_info_out.values() if zdxhu__jsdbo is not None]
        xwl__xstt = jzzf__mwf + oxqs__zxuz
        if agg_node.input_has_index:
            xwl__xstt.append(f'arg{len(agg_node.in_vars) - 1}')
        rbgk__vkj += '    info_list = [{}]\n'.format(', '.join(
            f'array_to_info({ddw__yhnl})' for ddw__yhnl in xwl__xstt))
        rbgk__vkj += '    table = arr_info_list_to_table(info_list)\n'
    do_combine = parallel
    allfuncs = []
    lua__niwsk = []
    func_idx_to_in_col = []
    rndh__zjmth = []
    qugff__uie = False
    ore__fhxd = 1
    caatx__kcrg = -1
    wfzry__oiryr = 0
    ntr__cim = 0
    ytwgc__cbn = [func for qvi__ouqa, func in agg_node.gb_info_out.values()]
    for mkyx__zqywt, func in enumerate(ytwgc__cbn):
        lua__niwsk.append(len(allfuncs))
        if func.ftype in {'median', 'nunique', 'ngroup'}:
            do_combine = False
        if func.ftype in list_cumulative:
            wfzry__oiryr += 1
        if hasattr(func, 'skipdropna'):
            qugff__uie = func.skipdropna
        if func.ftype == 'shift':
            ore__fhxd = func.periods
            do_combine = False
        if func.ftype in {'transform'}:
            ntr__cim = func.transform_func
            do_combine = False
        if func.ftype == 'head':
            caatx__kcrg = func.head_n
            do_combine = False
        allfuncs.append(func)
        func_idx_to_in_col.append(mkyx__zqywt)
        if func.ftype == 'udf':
            rndh__zjmth.append(func.n_redvars)
        elif func.ftype == 'gen_udf':
            rndh__zjmth.append(0)
            do_combine = False
    lua__niwsk.append(len(allfuncs))
    assert len(agg_node.gb_info_out) == len(allfuncs
        ), 'invalid number of groupby outputs'
    if wfzry__oiryr > 0:
        if wfzry__oiryr != len(allfuncs):
            raise BodoError(
                f'{agg_node.func_name}(): Cannot mix cumulative operations with other aggregation functions'
                , loc=agg_node.loc)
        do_combine = False
    xlk__hpj = []
    if udf_func_struct is not None:
        xyaac__jtoc = next_label()
        if udf_func_struct.regular_udfs:
            goaa__fbgi = types.void(types.voidptr, types.voidptr, types.
                CPointer(types.int64))
            wji__ajjt = numba.cfunc(goaa__fbgi, nopython=True)(gen_update_cb
                (udf_func_struct, allfuncs, n_keys, in_col_typs, do_combine,
                func_idx_to_in_col, xyaac__jtoc))
            djwz__ltxu = numba.cfunc(goaa__fbgi, nopython=True)(gen_combine_cb
                (udf_func_struct, allfuncs, n_keys, xyaac__jtoc))
            emqeo__dtt = numba.cfunc('void(voidptr)', nopython=True)(
                gen_eval_cb(udf_func_struct, allfuncs, n_keys,
                func_out_types, xyaac__jtoc))
            udf_func_struct.set_regular_cfuncs(wji__ajjt, djwz__ltxu,
                emqeo__dtt)
            for bgx__mrw in udf_func_struct.regular_udf_cfuncs:
                gb_agg_cfunc[bgx__mrw.native_name] = bgx__mrw
                gb_agg_cfunc_addr[bgx__mrw.native_name] = bgx__mrw.address
        if udf_func_struct.general_udfs:
            juck__muq = gen_general_udf_cb(udf_func_struct, allfuncs,
                n_keys, in_col_typs, func_out_types, func_idx_to_in_col,
                xyaac__jtoc)
            udf_func_struct.set_general_cfunc(juck__muq)
        mtc__vuoua = (udf_func_struct.var_typs if udf_func_struct.
            regular_udfs else None)
        zwz__sjkol = 0
        eyg__qpy = 0
        for dru__zcxcr, jvg__fgzmj in zip(agg_node.gb_info_out.keys(), allfuncs
            ):
            if jvg__fgzmj.ftype in ('udf', 'gen_udf'):
                xlk__hpj.append(out_col_typs[dru__zcxcr])
                for ptzjy__uhc in range(zwz__sjkol, zwz__sjkol +
                    rndh__zjmth[eyg__qpy]):
                    xlk__hpj.append(dtype_to_array_type(mtc__vuoua[ptzjy__uhc])
                        )
                zwz__sjkol += rndh__zjmth[eyg__qpy]
                eyg__qpy += 1
        rbgk__vkj += f"""    dummy_table = create_dummy_table(({', '.join(f'udf_type{eyg__qpy}' for eyg__qpy in range(len(xlk__hpj)))}{',' if len(xlk__hpj) == 1 else ''}))
"""
        rbgk__vkj += f"""    udf_table_dummy = py_data_to_cpp_table(dummy_table, (), udf_dummy_col_inds, {len(xlk__hpj)})
"""
        if udf_func_struct.regular_udfs:
            rbgk__vkj += (
                f"    add_agg_cfunc_sym(cpp_cb_update, '{wji__ajjt.native_name}')\n"
                )
            rbgk__vkj += (
                f"    add_agg_cfunc_sym(cpp_cb_combine, '{djwz__ltxu.native_name}')\n"
                )
            rbgk__vkj += (
                f"    add_agg_cfunc_sym(cpp_cb_eval, '{emqeo__dtt.native_name}')\n"
                )
            rbgk__vkj += (
                f"    cpp_cb_update_addr = get_agg_udf_addr('{wji__ajjt.native_name}')\n"
                )
            rbgk__vkj += (
                f"    cpp_cb_combine_addr = get_agg_udf_addr('{djwz__ltxu.native_name}')\n"
                )
            rbgk__vkj += (
                f"    cpp_cb_eval_addr = get_agg_udf_addr('{emqeo__dtt.native_name}')\n"
                )
        else:
            rbgk__vkj += '    cpp_cb_update_addr = 0\n'
            rbgk__vkj += '    cpp_cb_combine_addr = 0\n'
            rbgk__vkj += '    cpp_cb_eval_addr = 0\n'
        if udf_func_struct.general_udfs:
            bgx__mrw = udf_func_struct.general_udf_cfunc
            gb_agg_cfunc[bgx__mrw.native_name] = bgx__mrw
            gb_agg_cfunc_addr[bgx__mrw.native_name] = bgx__mrw.address
            rbgk__vkj += (
                f"    add_agg_cfunc_sym(cpp_cb_general, '{bgx__mrw.native_name}')\n"
                )
            rbgk__vkj += (
                f"    cpp_cb_general_addr = get_agg_udf_addr('{bgx__mrw.native_name}')\n"
                )
        else:
            rbgk__vkj += '    cpp_cb_general_addr = 0\n'
    else:
        rbgk__vkj += (
            '    udf_table_dummy = arr_info_list_to_table([array_to_info(np.empty(1))])\n'
            )
        rbgk__vkj += '    cpp_cb_update_addr = 0\n'
        rbgk__vkj += '    cpp_cb_combine_addr = 0\n'
        rbgk__vkj += '    cpp_cb_eval_addr = 0\n'
        rbgk__vkj += '    cpp_cb_general_addr = 0\n'
    rbgk__vkj += '    ftypes = np.array([{}, 0], dtype=np.int32)\n'.format(', '
        .join([str(supported_agg_funcs.index(jvg__fgzmj.ftype)) for
        jvg__fgzmj in allfuncs] + ['0']))
    rbgk__vkj += (
        f'    func_offsets = np.array({str(lua__niwsk)}, dtype=np.int32)\n')
    if len(rndh__zjmth) > 0:
        rbgk__vkj += (
            f'    udf_ncols = np.array({str(rndh__zjmth)}, dtype=np.int32)\n')
    else:
        rbgk__vkj += '    udf_ncols = np.array([0], np.int32)\n'
    rbgk__vkj += '    total_rows_np = np.array([0], dtype=np.int64)\n'
    nng__ynst = (agg_node._num_shuffle_keys if agg_node._num_shuffle_keys !=
        -1 else n_keys)
    rbgk__vkj += f"""    out_table = groupby_and_aggregate(table, {n_keys}, {agg_node.input_has_index}, ftypes.ctypes, func_offsets.ctypes, udf_ncols.ctypes, {parallel}, {qugff__uie}, {ore__fhxd}, {ntr__cim}, {caatx__kcrg}, {agg_node.return_key}, {agg_node.same_index}, {agg_node.dropna}, cpp_cb_update_addr, cpp_cb_combine_addr, cpp_cb_eval_addr, cpp_cb_general_addr, udf_table_dummy, total_rows_np.ctypes, {nng__ynst})
"""
    lof__dym = []
    xocm__utqb = 0
    if agg_node.return_key:
        siv__rxdf = 0 if isinstance(agg_node.out_type.index, bodo.
            RangeIndexType) else agg_node.n_out_cols - len(agg_node.in_key_inds
            ) - 1
        for eyg__qpy in range(n_keys):
            dbvin__aciyf = siv__rxdf + eyg__qpy
            lof__dym.append(dbvin__aciyf if dbvin__aciyf not in agg_node.
                dead_out_inds else -1)
            xocm__utqb += 1
    for dru__zcxcr in agg_node.gb_info_out.keys():
        lof__dym.append(dru__zcxcr)
        xocm__utqb += 1
    vhhle__xjzgw = False
    if agg_node.same_index:
        if agg_node.out_vars[-1] is not None:
            lof__dym.append(agg_node.n_out_cols - 1)
        else:
            vhhle__xjzgw = True
    ikil__xda = ',' if uen__vqo == 1 else ''
    exhkg__qjvi = (
        f"({', '.join(f'out_type{eyg__qpy}' for eyg__qpy in range(uen__vqo))}{ikil__xda})"
        )
    gqol__cyoz = []
    zhufv__ktwvu = []
    for eyg__qpy, t in enumerate(out_col_typs):
        if eyg__qpy not in agg_node.dead_out_inds and type_has_unknown_cats(t):
            if eyg__qpy in agg_node.gb_info_out:
                zdxhu__jsdbo = agg_node.gb_info_out[eyg__qpy][0]
            else:
                assert agg_node.return_key, 'Internal error: groupby key output with unknown categoricals detected, but return_key is False'
                vwrw__vcev = eyg__qpy - siv__rxdf
                zdxhu__jsdbo = agg_node.in_key_inds[vwrw__vcev]
            zhufv__ktwvu.append(eyg__qpy)
            if (agg_node.is_in_table_format and zdxhu__jsdbo < agg_node.
                n_in_table_arrays):
                gqol__cyoz.append(f'get_table_data(arg0, {zdxhu__jsdbo})')
            else:
                gqol__cyoz.append(f'arg{zdxhu__jsdbo}')
    ikil__xda = ',' if len(gqol__cyoz) == 1 else ''
    rbgk__vkj += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {exhkg__qjvi}, total_rows_np[0], {agg_node.n_out_table_arrays}, ({', '.join(gqol__cyoz)}{ikil__xda}), unknown_cat_out_inds)
"""
    rbgk__vkj += (
        f"    ev_clean = bodo.utils.tracing.Event('tables_clean_up', {parallel})\n"
        )
    rbgk__vkj += '    delete_table_decref_arrays(table)\n'
    rbgk__vkj += '    delete_table_decref_arrays(udf_table_dummy)\n'
    if agg_node.return_key:
        for eyg__qpy in range(n_keys):
            if lof__dym[eyg__qpy] == -1:
                rbgk__vkj += f'    decref_table_array(out_table, {eyg__qpy})\n'
    if vhhle__xjzgw:
        shqk__ayoqm = len(agg_node.gb_info_out) + (n_keys if agg_node.
            return_key else 0)
        rbgk__vkj += f'    decref_table_array(out_table, {shqk__ayoqm})\n'
    rbgk__vkj += '    delete_table(out_table)\n'
    rbgk__vkj += '    ev_clean.finalize()\n'
    rbgk__vkj += '    return out_data\n'
    itm__ysuvq = {f'out_type{eyg__qpy}': out_var_types[eyg__qpy] for
        eyg__qpy in range(uen__vqo)}
    itm__ysuvq['out_col_inds'] = MetaType(tuple(lof__dym))
    itm__ysuvq['in_col_inds'] = MetaType(tuple(sza__afbq))
    itm__ysuvq['cpp_table_to_py_data'] = cpp_table_to_py_data
    itm__ysuvq['py_data_to_cpp_table'] = py_data_to_cpp_table
    itm__ysuvq.update({f'udf_type{eyg__qpy}': t for eyg__qpy, t in
        enumerate(xlk__hpj)})
    itm__ysuvq['udf_dummy_col_inds'] = MetaType(tuple(range(len(xlk__hpj))))
    itm__ysuvq['create_dummy_table'] = create_dummy_table
    itm__ysuvq['unknown_cat_out_inds'] = MetaType(tuple(zhufv__ktwvu))
    itm__ysuvq['get_table_data'] = bodo.hiframes.table.get_table_data
    return rbgk__vkj, itm__ysuvq


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def create_dummy_table(data_types):
    lpdx__mvdce = tuple(unwrap_typeref(data_types.types[eyg__qpy]) for
        eyg__qpy in range(len(data_types.types)))
    ghero__fwf = bodo.TableType(lpdx__mvdce)
    itm__ysuvq = {'table_type': ghero__fwf}
    rbgk__vkj = 'def impl(data_types):\n'
    rbgk__vkj += '  py_table = init_table(table_type, False)\n'
    rbgk__vkj += '  py_table = set_table_len(py_table, 1)\n'
    for oyxx__bbmfu, mmp__gbii in ghero__fwf.type_to_blk.items():
        itm__ysuvq[f'typ_list_{mmp__gbii}'] = types.List(oyxx__bbmfu)
        itm__ysuvq[f'typ_{mmp__gbii}'] = oyxx__bbmfu
        vmxly__qrzko = len(ghero__fwf.block_to_arr_ind[mmp__gbii])
        rbgk__vkj += f"""  arr_list_{mmp__gbii} = alloc_list_like(typ_list_{mmp__gbii}, {vmxly__qrzko}, False)
"""
        rbgk__vkj += f'  for i in range(len(arr_list_{mmp__gbii})):\n'
        rbgk__vkj += (
            f'    arr_list_{mmp__gbii}[i] = alloc_type(1, typ_{mmp__gbii}, (-1,))\n'
            )
        rbgk__vkj += (
            f'  py_table = set_table_block(py_table, arr_list_{mmp__gbii}, {mmp__gbii})\n'
            )
    rbgk__vkj += '  return py_table\n'
    itm__ysuvq.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len, 'alloc_type':
        bodo.utils.utils.alloc_type})
    qud__meeg = {}
    exec(rbgk__vkj, itm__ysuvq, qud__meeg)
    return qud__meeg['impl']


def agg_table_column_use(agg_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not agg_node.is_in_table_format or agg_node.in_vars[0] is None:
        return
    wduyt__wekqz = agg_node.in_vars[0].name
    jqtl__cidv, kav__kqqh, zjxgo__kvr = block_use_map[wduyt__wekqz]
    if kav__kqqh or zjxgo__kvr:
        return
    if agg_node.is_output_table and agg_node.out_vars[0] is not None:
        mwmu__vzwn, fza__kazxc, dcf__jvf = _compute_table_column_uses(agg_node
            .out_vars[0].name, table_col_use_map, equiv_vars)
        if fza__kazxc or dcf__jvf:
            mwmu__vzwn = set(range(agg_node.n_out_table_arrays))
    else:
        mwmu__vzwn = {}
        if agg_node.out_vars[0
            ] is not None and 0 not in agg_node.dead_out_inds:
            mwmu__vzwn = {0}
    gyk__nqm = set(eyg__qpy for eyg__qpy in agg_node.in_key_inds if 
        eyg__qpy < agg_node.n_in_table_arrays)
    hrxv__yvww = set(agg_node.gb_info_out[eyg__qpy][0] for eyg__qpy in
        mwmu__vzwn if eyg__qpy in agg_node.gb_info_out and agg_node.
        gb_info_out[eyg__qpy][0] is not None)
    hrxv__yvww |= gyk__nqm | jqtl__cidv
    irlm__buofx = len(set(range(agg_node.n_in_table_arrays)) - hrxv__yvww) == 0
    block_use_map[wduyt__wekqz] = hrxv__yvww, irlm__buofx, False


ir_extension_table_column_use[Aggregate] = agg_table_column_use


def agg_remove_dead_column(agg_node, column_live_map, equiv_vars, typemap):
    if not agg_node.is_output_table or agg_node.out_vars[0] is None:
        return False
    bla__hrjv = agg_node.n_out_table_arrays
    qjq__utqw = agg_node.out_vars[0].name
    kyfd__ght = _find_used_columns(qjq__utqw, bla__hrjv, column_live_map,
        equiv_vars)
    if kyfd__ght is None:
        return False
    cseq__gcirf = set(range(bla__hrjv)) - kyfd__ght
    tut__jtj = len(cseq__gcirf - agg_node.dead_out_inds) != 0
    if tut__jtj:
        agg_node.dead_out_inds.update(cseq__gcirf)
        agg_node.update_dead_col_info()
    return tut__jtj


remove_dead_column_extensions[Aggregate] = agg_remove_dead_column


def compile_to_optimized_ir(func, arg_typs, typingctx, targetctx):
    code = func.code if hasattr(func, 'code') else func.__code__
    closure = func.closure if hasattr(func, 'closure') else func.__closure__
    f_ir = get_ir_of_code(func.__globals__, code)
    replace_closures(f_ir, closure, code)
    for block in f_ir.blocks.values():
        for gwus__idms in block.body:
            if is_call_assign(gwus__idms) and find_callname(f_ir,
                gwus__idms.value) == ('len', 'builtins'
                ) and gwus__idms.value.args[0].name == f_ir.arg_names[0]:
                myg__staju = get_definition(f_ir, gwus__idms.value.func)
                myg__staju.name = 'dummy_agg_count'
                myg__staju.value = dummy_agg_count
    uycym__mjq = get_name_var_table(f_ir.blocks)
    lgi__cegm = {}
    for name, qvi__ouqa in uycym__mjq.items():
        lgi__cegm[name] = mk_unique_var(name)
    replace_var_names(f_ir.blocks, lgi__cegm)
    f_ir._definitions = build_definitions(f_ir.blocks)
    assert f_ir.arg_count == 1, 'agg function should have one input'
    uqhho__ahi = numba.core.compiler.Flags()
    uqhho__ahi.nrt = True
    rxmpb__cxeb = bodo.transforms.untyped_pass.UntypedPass(f_ir, typingctx,
        arg_typs, {}, {}, uqhho__ahi)
    rxmpb__cxeb.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    typemap, tcfp__tglf, calltypes, qvi__ouqa = (numba.core.typed_passes.
        type_inference_stage(typingctx, targetctx, f_ir, arg_typs, None))
    qoqef__umuvd = numba.core.cpu.ParallelOptions(True)
    targetctx = numba.core.cpu.CPUContext(typingctx)
    gjk__cmepy = namedtuple('DummyPipeline', ['typingctx', 'targetctx',
        'args', 'func_ir', 'typemap', 'return_type', 'calltypes',
        'type_annotation', 'locals', 'flags', 'pipeline'])
    vkde__lpyaw = namedtuple('TypeAnnotation', ['typemap', 'calltypes'])
    qbnc__uey = vkde__lpyaw(typemap, calltypes)
    pm = gjk__cmepy(typingctx, targetctx, None, f_ir, typemap, tcfp__tglf,
        calltypes, qbnc__uey, {}, uqhho__ahi, None)
    gjcji__nhd = (numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline(pm))
    pm = gjk__cmepy(typingctx, targetctx, None, f_ir, typemap, tcfp__tglf,
        calltypes, qbnc__uey, {}, uqhho__ahi, gjcji__nhd)
    qpt__cpmcc = numba.core.typed_passes.InlineOverloads()
    qpt__cpmcc.run_pass(pm)
    lko__yyxto = bodo.transforms.series_pass.SeriesPass(f_ir, typingctx,
        targetctx, typemap, calltypes, {}, False)
    lko__yyxto.run()
    for block in f_ir.blocks.values():
        for gwus__idms in block.body:
            if is_assign(gwus__idms) and isinstance(gwus__idms.value, (ir.
                Arg, ir.Var)) and isinstance(typemap[gwus__idms.target.name
                ], SeriesType):
                oyxx__bbmfu = typemap.pop(gwus__idms.target.name)
                typemap[gwus__idms.target.name] = oyxx__bbmfu.data
            if is_call_assign(gwus__idms) and find_callname(f_ir,
                gwus__idms.value) == ('get_series_data',
                'bodo.hiframes.pd_series_ext'):
                f_ir._definitions[gwus__idms.target.name].remove(gwus__idms
                    .value)
                gwus__idms.value = gwus__idms.value.args[0]
                f_ir._definitions[gwus__idms.target.name].append(gwus__idms
                    .value)
            if is_call_assign(gwus__idms) and find_callname(f_ir,
                gwus__idms.value) == ('isna', 'bodo.libs.array_kernels'):
                f_ir._definitions[gwus__idms.target.name].remove(gwus__idms
                    .value)
                gwus__idms.value = ir.Const(False, gwus__idms.loc)
                f_ir._definitions[gwus__idms.target.name].append(gwus__idms
                    .value)
            if is_call_assign(gwus__idms) and find_callname(f_ir,
                gwus__idms.value) == ('setna', 'bodo.libs.array_kernels'):
                f_ir._definitions[gwus__idms.target.name].remove(gwus__idms
                    .value)
                gwus__idms.value = ir.Const(False, gwus__idms.loc)
                f_ir._definitions[gwus__idms.target.name].append(gwus__idms
                    .value)
    bodo.transforms.untyped_pass.remove_dead_branches(f_ir)
    djant__ftot = numba.parfors.parfor.PreParforPass(f_ir, typemap,
        calltypes, typingctx, targetctx, qoqef__umuvd)
    djant__ftot.run()
    f_ir._definitions = build_definitions(f_ir.blocks)
    hlwhz__dlfy = numba.core.compiler.StateDict()
    hlwhz__dlfy.func_ir = f_ir
    hlwhz__dlfy.typemap = typemap
    hlwhz__dlfy.calltypes = calltypes
    hlwhz__dlfy.typingctx = typingctx
    hlwhz__dlfy.targetctx = targetctx
    hlwhz__dlfy.return_type = tcfp__tglf
    numba.core.rewrites.rewrite_registry.apply('after-inference', hlwhz__dlfy)
    nrb__gdq = numba.parfors.parfor.ParforPass(f_ir, typemap, calltypes,
        tcfp__tglf, typingctx, targetctx, qoqef__umuvd, uqhho__ahi, {})
    nrb__gdq.run()
    remove_dels(f_ir.blocks)
    numba.parfors.parfor.maximize_fusion(f_ir, f_ir.blocks, typemap, False)
    return f_ir, pm


def replace_closures(f_ir, closure, code):
    if closure:
        closure = f_ir.get_definition(closure)
        if isinstance(closure, tuple):
            vtcf__qmo = ctypes.pythonapi.PyCell_Get
            vtcf__qmo.restype = ctypes.py_object
            vtcf__qmo.argtypes = ctypes.py_object,
            tah__xhas = tuple(vtcf__qmo(bngi__rfs) for bngi__rfs in closure)
        else:
            assert isinstance(closure, ir.Expr) and closure.op == 'build_tuple'
            tah__xhas = closure.items
        assert len(code.co_freevars) == len(tah__xhas)
        numba.core.inline_closurecall._replace_freevars(f_ir.blocks, tah__xhas)


class RegularUDFGenerator:

    def __init__(self, in_col_types, typingctx, targetctx):
        self.in_col_types = in_col_types
        self.typingctx = typingctx
        self.targetctx = targetctx
        self.all_reduce_vars = []
        self.all_vartypes = []
        self.all_init_nodes = []
        self.all_eval_funcs = []
        self.all_update_funcs = []
        self.all_combine_funcs = []
        self.curr_offset = 0
        self.redvar_offsets = [0]

    def add_udf(self, in_col_typ, func):
        geib__qmyt = SeriesType(in_col_typ.dtype, to_str_arr_if_dict_array(
            in_col_typ), None, string_type)
        f_ir, pm = compile_to_optimized_ir(func, (geib__qmyt,), self.
            typingctx, self.targetctx)
        f_ir._definitions = build_definitions(f_ir.blocks)
        assert len(f_ir.blocks
            ) == 1 and 0 in f_ir.blocks, 'only simple functions with one block supported for aggregation'
        block = f_ir.blocks[0]
        gmmv__tam, arr_var = _rm_arg_agg_block(block, pm.typemap)
        pjpqt__dosmf = -1
        for eyg__qpy, gwus__idms in enumerate(gmmv__tam):
            if isinstance(gwus__idms, numba.parfors.parfor.Parfor):
                assert pjpqt__dosmf == -1, 'only one parfor for aggregation function'
                pjpqt__dosmf = eyg__qpy
        parfor = None
        if pjpqt__dosmf != -1:
            parfor = gmmv__tam[pjpqt__dosmf]
            remove_dels(parfor.loop_body)
            remove_dels({(0): parfor.init_block})
        init_nodes = []
        if parfor:
            init_nodes = gmmv__tam[:pjpqt__dosmf] + parfor.init_block.body
        eval_nodes = gmmv__tam[pjpqt__dosmf + 1:]
        redvars = []
        var_to_redvar = {}
        if parfor:
            redvars, var_to_redvar = get_parfor_reductions(parfor, parfor.
                params, pm.calltypes)
        func.ncols_pre_shuffle = len(redvars)
        func.ncols_post_shuffle = len(redvars) + 1
        func.n_redvars = len(redvars)
        reduce_vars = [0] * len(redvars)
        for gwus__idms in init_nodes:
            if is_assign(gwus__idms) and gwus__idms.target.name in redvars:
                ind = redvars.index(gwus__idms.target.name)
                reduce_vars[ind] = gwus__idms.target
        var_types = [pm.typemap[axdy__tdda] for axdy__tdda in redvars]
        fiu__pxhn = gen_combine_func(f_ir, parfor, redvars, var_to_redvar,
            var_types, arr_var, pm, self.typingctx, self.targetctx)
        init_nodes = _mv_read_only_init_vars(init_nodes, parfor, eval_nodes)
        sid__wen = gen_update_func(parfor, redvars, var_to_redvar,
            var_types, arr_var, in_col_typ, pm, self.typingctx, self.targetctx)
        uektb__rfykt = gen_eval_func(f_ir, eval_nodes, reduce_vars,
            var_types, pm, self.typingctx, self.targetctx)
        self.all_reduce_vars += reduce_vars
        self.all_vartypes += var_types
        self.all_init_nodes += init_nodes
        self.all_eval_funcs.append(uektb__rfykt)
        self.all_update_funcs.append(sid__wen)
        self.all_combine_funcs.append(fiu__pxhn)
        self.curr_offset += len(redvars)
        self.redvar_offsets.append(self.curr_offset)

    def gen_all_func(self):
        if len(self.all_update_funcs) == 0:
            return None
        wrxk__maula = gen_init_func(self.all_init_nodes, self.
            all_reduce_vars, self.all_vartypes, self.typingctx, self.targetctx)
        gxf__avs = gen_all_update_func(self.all_update_funcs, self.
            in_col_types, self.redvar_offsets)
        zzwzd__cnyn = gen_all_combine_func(self.all_combine_funcs, self.
            all_vartypes, self.redvar_offsets, self.typingctx, self.targetctx)
        nug__rprvn = gen_all_eval_func(self.all_eval_funcs, self.redvar_offsets
            )
        return (self.all_vartypes, wrxk__maula, gxf__avs, zzwzd__cnyn,
            nug__rprvn)


class GeneralUDFGenerator(object):

    def __init__(self):
        self.funcs = []

    def add_udf(self, func):
        self.funcs.append(bodo.jit(distributed=False)(func))
        func.ncols_pre_shuffle = 1
        func.ncols_post_shuffle = 1
        func.n_redvars = 0

    def gen_all_func(self):
        if len(self.funcs) > 0:
            return self.funcs
        else:
            return None


def get_udf_func_struct(agg_func, in_col_types, typingctx, targetctx):
    toklm__jwb = []
    for t, jvg__fgzmj in zip(in_col_types, agg_func):
        toklm__jwb.append((t, jvg__fgzmj))
    jftn__doiv = RegularUDFGenerator(in_col_types, typingctx, targetctx)
    kqz__vfirl = GeneralUDFGenerator()
    for in_col_typ, func in toklm__jwb:
        if func.ftype not in ('udf', 'gen_udf'):
            continue
        try:
            jftn__doiv.add_udf(in_col_typ, func)
        except:
            kqz__vfirl.add_udf(func)
            func.ftype = 'gen_udf'
    regular_udf_funcs = jftn__doiv.gen_all_func()
    general_udf_funcs = kqz__vfirl.gen_all_func()
    if regular_udf_funcs is not None or general_udf_funcs is not None:
        return AggUDFStruct(regular_udf_funcs, general_udf_funcs)
    else:
        return None


def _mv_read_only_init_vars(init_nodes, parfor, eval_nodes):
    if not parfor:
        return init_nodes
    iphgb__wspll = compute_use_defs(parfor.loop_body)
    xxwjk__hkab = set()
    for nwlc__ozf in iphgb__wspll.usemap.values():
        xxwjk__hkab |= nwlc__ozf
    tbh__npcp = set()
    for nwlc__ozf in iphgb__wspll.defmap.values():
        tbh__npcp |= nwlc__ozf
    oywoz__brr = ir.Block(ir.Scope(None, parfor.loc), parfor.loc)
    oywoz__brr.body = eval_nodes
    yiu__iuc = compute_use_defs({(0): oywoz__brr})
    rfs__fhsm = yiu__iuc.usemap[0]
    nfxs__xzr = set()
    awq__alo = []
    ykuxd__gok = []
    for gwus__idms in reversed(init_nodes):
        wnoim__yfw = {axdy__tdda.name for axdy__tdda in gwus__idms.list_vars()}
        if is_assign(gwus__idms):
            axdy__tdda = gwus__idms.target.name
            wnoim__yfw.remove(axdy__tdda)
            if (axdy__tdda in xxwjk__hkab and axdy__tdda not in nfxs__xzr and
                axdy__tdda not in rfs__fhsm and axdy__tdda not in tbh__npcp):
                ykuxd__gok.append(gwus__idms)
                xxwjk__hkab |= wnoim__yfw
                tbh__npcp.add(axdy__tdda)
                continue
        nfxs__xzr |= wnoim__yfw
        awq__alo.append(gwus__idms)
    ykuxd__gok.reverse()
    awq__alo.reverse()
    ajwd__iqnle = min(parfor.loop_body.keys())
    cwx__mhsni = parfor.loop_body[ajwd__iqnle]
    cwx__mhsni.body = ykuxd__gok + cwx__mhsni.body
    return awq__alo


def gen_init_func(init_nodes, reduce_vars, var_types, typingctx, targetctx):
    shzzi__bup = (numba.parfors.parfor.max_checker, numba.parfors.parfor.
        min_checker, numba.parfors.parfor.argmax_checker, numba.parfors.
        parfor.argmin_checker)
    ptpf__flp = set()
    sbdp__qohcr = []
    for gwus__idms in init_nodes:
        if is_assign(gwus__idms) and isinstance(gwus__idms.value, ir.Global
            ) and isinstance(gwus__idms.value.value, pytypes.FunctionType
            ) and gwus__idms.value.value in shzzi__bup:
            ptpf__flp.add(gwus__idms.target.name)
        elif is_call_assign(gwus__idms
            ) and gwus__idms.value.func.name in ptpf__flp:
            pass
        else:
            sbdp__qohcr.append(gwus__idms)
    init_nodes = sbdp__qohcr
    kap__kgopl = types.Tuple(var_types)
    unvgv__cavj = lambda : None
    f_ir = compile_to_numba_ir(unvgv__cavj, {})
    block = list(f_ir.blocks.values())[0]
    loc = block.loc
    bije__iao = ir.Var(block.scope, mk_unique_var('init_tup'), loc)
    vsgsl__hsyof = ir.Assign(ir.Expr.build_tuple(reduce_vars, loc),
        bije__iao, loc)
    block.body = block.body[-2:]
    block.body = init_nodes + [vsgsl__hsyof] + block.body
    block.body[-2].value.value = bije__iao
    vcubs__dnppd = compiler.compile_ir(typingctx, targetctx, f_ir, (),
        kap__kgopl, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    qrzh__ejkhh = numba.core.target_extension.dispatcher_registry[cpu_target](
        unvgv__cavj)
    qrzh__ejkhh.add_overload(vcubs__dnppd)
    return qrzh__ejkhh


def gen_all_update_func(update_funcs, in_col_types, redvar_offsets):
    mgr__pfm = len(update_funcs)
    tvtf__ehzab = len(in_col_types)
    rbgk__vkj = 'def update_all_f(redvar_arrs, data_in, w_ind, i):\n'
    for ptzjy__uhc in range(mgr__pfm):
        evdhe__ljju = ', '.join(['redvar_arrs[{}][w_ind]'.format(eyg__qpy) for
            eyg__qpy in range(redvar_offsets[ptzjy__uhc], redvar_offsets[
            ptzjy__uhc + 1])])
        if evdhe__ljju:
            rbgk__vkj += '  {} = update_vars_{}({},  data_in[{}][i])\n'.format(
                evdhe__ljju, ptzjy__uhc, evdhe__ljju, 0 if tvtf__ehzab == 1
                 else ptzjy__uhc)
    rbgk__vkj += '  return\n'
    hvz__fwje = {}
    for eyg__qpy, jvg__fgzmj in enumerate(update_funcs):
        hvz__fwje['update_vars_{}'.format(eyg__qpy)] = jvg__fgzmj
    qud__meeg = {}
    exec(rbgk__vkj, hvz__fwje, qud__meeg)
    xgpq__ceoam = qud__meeg['update_all_f']
    return numba.njit(no_cpython_wrapper=True)(xgpq__ceoam)


def gen_all_combine_func(combine_funcs, reduce_var_types, redvar_offsets,
    typingctx, targetctx):
    dfomb__ktjx = types.Tuple([types.Array(t, 1, 'C') for t in
        reduce_var_types])
    arg_typs = dfomb__ktjx, dfomb__ktjx, types.intp, types.intp
    xfp__tyrd = len(redvar_offsets) - 1
    rbgk__vkj = 'def combine_all_f(redvar_arrs, recv_arrs, w_ind, i):\n'
    for ptzjy__uhc in range(xfp__tyrd):
        evdhe__ljju = ', '.join(['redvar_arrs[{}][w_ind]'.format(eyg__qpy) for
            eyg__qpy in range(redvar_offsets[ptzjy__uhc], redvar_offsets[
            ptzjy__uhc + 1])])
        rwhi__bfuc = ', '.join(['recv_arrs[{}][i]'.format(eyg__qpy) for
            eyg__qpy in range(redvar_offsets[ptzjy__uhc], redvar_offsets[
            ptzjy__uhc + 1])])
        if rwhi__bfuc:
            rbgk__vkj += '  {} = combine_vars_{}({}, {})\n'.format(evdhe__ljju,
                ptzjy__uhc, evdhe__ljju, rwhi__bfuc)
    rbgk__vkj += '  return\n'
    hvz__fwje = {}
    for eyg__qpy, jvg__fgzmj in enumerate(combine_funcs):
        hvz__fwje['combine_vars_{}'.format(eyg__qpy)] = jvg__fgzmj
    qud__meeg = {}
    exec(rbgk__vkj, hvz__fwje, qud__meeg)
    nvsjc__wsvz = qud__meeg['combine_all_f']
    f_ir = compile_to_numba_ir(nvsjc__wsvz, hvz__fwje)
    zzwzd__cnyn = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        types.none, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    qrzh__ejkhh = numba.core.target_extension.dispatcher_registry[cpu_target](
        nvsjc__wsvz)
    qrzh__ejkhh.add_overload(zzwzd__cnyn)
    return qrzh__ejkhh


def gen_all_eval_func(eval_funcs, redvar_offsets):
    xfp__tyrd = len(redvar_offsets) - 1
    rbgk__vkj = 'def eval_all_f(redvar_arrs, out_arrs, j):\n'
    for ptzjy__uhc in range(xfp__tyrd):
        evdhe__ljju = ', '.join(['redvar_arrs[{}][j]'.format(eyg__qpy) for
            eyg__qpy in range(redvar_offsets[ptzjy__uhc], redvar_offsets[
            ptzjy__uhc + 1])])
        rbgk__vkj += '  out_arrs[{}][j] = eval_vars_{}({})\n'.format(ptzjy__uhc
            , ptzjy__uhc, evdhe__ljju)
    rbgk__vkj += '  return\n'
    hvz__fwje = {}
    for eyg__qpy, jvg__fgzmj in enumerate(eval_funcs):
        hvz__fwje['eval_vars_{}'.format(eyg__qpy)] = jvg__fgzmj
    qud__meeg = {}
    exec(rbgk__vkj, hvz__fwje, qud__meeg)
    ftdb__lnbcy = qud__meeg['eval_all_f']
    return numba.njit(no_cpython_wrapper=True)(ftdb__lnbcy)


def gen_eval_func(f_ir, eval_nodes, reduce_vars, var_types, pm, typingctx,
    targetctx):
    hfsvl__mrok = len(var_types)
    pnfk__gxlk = [f'in{eyg__qpy}' for eyg__qpy in range(hfsvl__mrok)]
    kap__kgopl = types.unliteral(pm.typemap[eval_nodes[-1].value.name])
    adnu__ckln = kap__kgopl(0)
    rbgk__vkj = 'def agg_eval({}):\n return _zero\n'.format(', '.join(
        pnfk__gxlk))
    qud__meeg = {}
    exec(rbgk__vkj, {'_zero': adnu__ckln}, qud__meeg)
    whvvj__caai = qud__meeg['agg_eval']
    arg_typs = tuple(var_types)
    f_ir = compile_to_numba_ir(whvvj__caai, {'numba': numba, 'bodo': bodo,
        'np': np, '_zero': adnu__ckln}, typingctx=typingctx, targetctx=
        targetctx, arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.
        calltypes)
    block = list(f_ir.blocks.values())[0]
    yygv__wegim = []
    for eyg__qpy, axdy__tdda in enumerate(reduce_vars):
        yygv__wegim.append(ir.Assign(block.body[eyg__qpy].target,
            axdy__tdda, axdy__tdda.loc))
        for wnjw__vjztg in axdy__tdda.versioned_names:
            yygv__wegim.append(ir.Assign(axdy__tdda, ir.Var(axdy__tdda.
                scope, wnjw__vjztg, axdy__tdda.loc), axdy__tdda.loc))
    block.body = block.body[:hfsvl__mrok] + yygv__wegim + eval_nodes
    uektb__rfykt = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        kap__kgopl, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    qrzh__ejkhh = numba.core.target_extension.dispatcher_registry[cpu_target](
        whvvj__caai)
    qrzh__ejkhh.add_overload(uektb__rfykt)
    return qrzh__ejkhh


def gen_combine_func(f_ir, parfor, redvars, var_to_redvar, var_types,
    arr_var, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda : ())
    hfsvl__mrok = len(redvars)
    myju__mswxx = [f'v{eyg__qpy}' for eyg__qpy in range(hfsvl__mrok)]
    pnfk__gxlk = [f'in{eyg__qpy}' for eyg__qpy in range(hfsvl__mrok)]
    rbgk__vkj = 'def agg_combine({}):\n'.format(', '.join(myju__mswxx +
        pnfk__gxlk))
    wjakq__qvvtn = wrap_parfor_blocks(parfor)
    iikb__ckxam = find_topo_order(wjakq__qvvtn)
    iikb__ckxam = iikb__ckxam[1:]
    unwrap_parfor_blocks(parfor)
    rkb__ldbj = {}
    mqagr__srfwk = []
    for sboed__amxdj in iikb__ckxam:
        xccke__ykuoj = parfor.loop_body[sboed__amxdj]
        for gwus__idms in xccke__ykuoj.body:
            if is_assign(gwus__idms) and gwus__idms.target.name in redvars:
                jmqiy__qajq = gwus__idms.target.name
                ind = redvars.index(jmqiy__qajq)
                if ind in mqagr__srfwk:
                    continue
                if len(f_ir._definitions[jmqiy__qajq]) == 2:
                    var_def = f_ir._definitions[jmqiy__qajq][0]
                    rbgk__vkj += _match_reduce_def(var_def, f_ir, ind)
                    var_def = f_ir._definitions[jmqiy__qajq][1]
                    rbgk__vkj += _match_reduce_def(var_def, f_ir, ind)
    rbgk__vkj += '    return {}'.format(', '.join(['v{}'.format(eyg__qpy) for
        eyg__qpy in range(hfsvl__mrok)]))
    qud__meeg = {}
    exec(rbgk__vkj, {}, qud__meeg)
    trf__kic = qud__meeg['agg_combine']
    arg_typs = tuple(2 * var_types)
    hvz__fwje = {'numba': numba, 'bodo': bodo, 'np': np}
    hvz__fwje.update(rkb__ldbj)
    f_ir = compile_to_numba_ir(trf__kic, hvz__fwje, typingctx=typingctx,
        targetctx=targetctx, arg_typs=arg_typs, typemap=pm.typemap,
        calltypes=pm.calltypes)
    block = list(f_ir.blocks.values())[0]
    kap__kgopl = pm.typemap[block.body[-1].value.name]
    fiu__pxhn = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        kap__kgopl, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    qrzh__ejkhh = numba.core.target_extension.dispatcher_registry[cpu_target](
        trf__kic)
    qrzh__ejkhh.add_overload(fiu__pxhn)
    return qrzh__ejkhh


def _match_reduce_def(var_def, f_ir, ind):
    rbgk__vkj = ''
    while isinstance(var_def, ir.Var):
        var_def = guard(get_definition, f_ir, var_def)
    if isinstance(var_def, ir.Expr
        ) and var_def.op == 'inplace_binop' and var_def.fn in ('+=',
        operator.iadd):
        rbgk__vkj = '    v{} += in{}\n'.format(ind, ind)
    if isinstance(var_def, ir.Expr) and var_def.op == 'call':
        klwhh__vjnpe = guard(find_callname, f_ir, var_def)
        if klwhh__vjnpe == ('min', 'builtins'):
            rbgk__vkj = '    v{} = min(v{}, in{})\n'.format(ind, ind, ind)
        if klwhh__vjnpe == ('max', 'builtins'):
            rbgk__vkj = '    v{} = max(v{}, in{})\n'.format(ind, ind, ind)
    return rbgk__vkj


def gen_update_func(parfor, redvars, var_to_redvar, var_types, arr_var,
    in_col_typ, pm, typingctx, targetctx):
    if not parfor:
        return numba.njit(lambda A: ())
    hfsvl__mrok = len(redvars)
    likh__niv = 1
    in_vars = []
    for eyg__qpy in range(likh__niv):
        lkep__dsazw = ir.Var(arr_var.scope, f'$input{eyg__qpy}', arr_var.loc)
        in_vars.append(lkep__dsazw)
    kohr__wcb = parfor.loop_nests[0].index_variable
    man__ovy = [0] * hfsvl__mrok
    for xccke__ykuoj in parfor.loop_body.values():
        hfuos__leq = []
        for gwus__idms in xccke__ykuoj.body:
            if is_var_assign(gwus__idms
                ) and gwus__idms.value.name == kohr__wcb.name:
                continue
            if is_getitem(gwus__idms
                ) and gwus__idms.value.value.name == arr_var.name:
                gwus__idms.value = in_vars[0]
            if is_call_assign(gwus__idms) and guard(find_callname, pm.
                func_ir, gwus__idms.value) == ('isna',
                'bodo.libs.array_kernels') and gwus__idms.value.args[0
                ].name == arr_var.name:
                gwus__idms.value = ir.Const(False, gwus__idms.target.loc)
            if is_assign(gwus__idms) and gwus__idms.target.name in redvars:
                ind = redvars.index(gwus__idms.target.name)
                man__ovy[ind] = gwus__idms.target
            hfuos__leq.append(gwus__idms)
        xccke__ykuoj.body = hfuos__leq
    myju__mswxx = ['v{}'.format(eyg__qpy) for eyg__qpy in range(hfsvl__mrok)]
    pnfk__gxlk = ['in{}'.format(eyg__qpy) for eyg__qpy in range(likh__niv)]
    rbgk__vkj = 'def agg_update({}):\n'.format(', '.join(myju__mswxx +
        pnfk__gxlk))
    rbgk__vkj += '    __update_redvars()\n'
    rbgk__vkj += '    return {}'.format(', '.join(['v{}'.format(eyg__qpy) for
        eyg__qpy in range(hfsvl__mrok)]))
    qud__meeg = {}
    exec(rbgk__vkj, {}, qud__meeg)
    kpveq__wjrge = qud__meeg['agg_update']
    arg_typs = tuple(var_types + [in_col_typ.dtype] * likh__niv)
    f_ir = compile_to_numba_ir(kpveq__wjrge, {'__update_redvars':
        __update_redvars}, typingctx=typingctx, targetctx=targetctx,
        arg_typs=arg_typs, typemap=pm.typemap, calltypes=pm.calltypes)
    f_ir._definitions = build_definitions(f_ir.blocks)
    ihlla__xqe = f_ir.blocks.popitem()[1].body
    kap__kgopl = pm.typemap[ihlla__xqe[-1].value.name]
    wjakq__qvvtn = wrap_parfor_blocks(parfor)
    iikb__ckxam = find_topo_order(wjakq__qvvtn)
    iikb__ckxam = iikb__ckxam[1:]
    unwrap_parfor_blocks(parfor)
    f_ir.blocks = parfor.loop_body
    cwx__mhsni = f_ir.blocks[iikb__ckxam[0]]
    vuuia__rkp = f_ir.blocks[iikb__ckxam[-1]]
    xcljs__mbv = ihlla__xqe[:hfsvl__mrok + likh__niv]
    if hfsvl__mrok > 1:
        pyq__zkx = ihlla__xqe[-3:]
        assert is_assign(pyq__zkx[0]) and isinstance(pyq__zkx[0].value, ir.Expr
            ) and pyq__zkx[0].value.op == 'build_tuple'
    else:
        pyq__zkx = ihlla__xqe[-2:]
    for eyg__qpy in range(hfsvl__mrok):
        ggypc__xty = ihlla__xqe[eyg__qpy].target
        mfzzo__tfce = ir.Assign(ggypc__xty, man__ovy[eyg__qpy], ggypc__xty.loc)
        xcljs__mbv.append(mfzzo__tfce)
    for eyg__qpy in range(hfsvl__mrok, hfsvl__mrok + likh__niv):
        ggypc__xty = ihlla__xqe[eyg__qpy].target
        mfzzo__tfce = ir.Assign(ggypc__xty, in_vars[eyg__qpy - hfsvl__mrok],
            ggypc__xty.loc)
        xcljs__mbv.append(mfzzo__tfce)
    cwx__mhsni.body = xcljs__mbv + cwx__mhsni.body
    kcu__heok = []
    for eyg__qpy in range(hfsvl__mrok):
        ggypc__xty = ihlla__xqe[eyg__qpy].target
        mfzzo__tfce = ir.Assign(man__ovy[eyg__qpy], ggypc__xty, ggypc__xty.loc)
        kcu__heok.append(mfzzo__tfce)
    vuuia__rkp.body += kcu__heok + pyq__zkx
    hrktj__jfxb = compiler.compile_ir(typingctx, targetctx, f_ir, arg_typs,
        kap__kgopl, compiler.DEFAULT_FLAGS, {})
    from numba.core.target_extension import cpu_target
    qrzh__ejkhh = numba.core.target_extension.dispatcher_registry[cpu_target](
        kpveq__wjrge)
    qrzh__ejkhh.add_overload(hrktj__jfxb)
    return qrzh__ejkhh


def _rm_arg_agg_block(block, typemap):
    gmmv__tam = []
    arr_var = None
    for eyg__qpy, gwus__idms in enumerate(block.body):
        if is_assign(gwus__idms) and isinstance(gwus__idms.value, ir.Arg):
            arr_var = gwus__idms.target
            pvvfo__eeakf = typemap[arr_var.name]
            if not isinstance(pvvfo__eeakf, types.ArrayCompatible):
                gmmv__tam += block.body[eyg__qpy + 1:]
                break
            erugr__knk = block.body[eyg__qpy + 1]
            assert is_assign(erugr__knk) and isinstance(erugr__knk.value,
                ir.Expr
                ) and erugr__knk.value.op == 'getattr' and erugr__knk.value.attr == 'shape' and erugr__knk.value.value.name == arr_var.name
            uxo__zso = erugr__knk.target
            ljljz__syulb = block.body[eyg__qpy + 2]
            assert is_assign(ljljz__syulb) and isinstance(ljljz__syulb.
                value, ir.Expr
                ) and ljljz__syulb.value.op == 'static_getitem' and ljljz__syulb.value.value.name == uxo__zso.name
            gmmv__tam += block.body[eyg__qpy + 3:]
            break
        gmmv__tam.append(gwus__idms)
    return gmmv__tam, arr_var


def get_parfor_reductions(parfor, parfor_params, calltypes, reduce_varnames
    =None, param_uses=None, var_to_param=None):
    if reduce_varnames is None:
        reduce_varnames = []
    if param_uses is None:
        param_uses = defaultdict(list)
    if var_to_param is None:
        var_to_param = {}
    wjakq__qvvtn = wrap_parfor_blocks(parfor)
    iikb__ckxam = find_topo_order(wjakq__qvvtn)
    iikb__ckxam = iikb__ckxam[1:]
    unwrap_parfor_blocks(parfor)
    for sboed__amxdj in reversed(iikb__ckxam):
        for gwus__idms in reversed(parfor.loop_body[sboed__amxdj].body):
            if isinstance(gwus__idms, ir.Assign) and (gwus__idms.target.
                name in parfor_params or gwus__idms.target.name in var_to_param
                ):
                ghn__zwd = gwus__idms.target.name
                rhs = gwus__idms.value
                glhyi__awemo = (ghn__zwd if ghn__zwd in parfor_params else
                    var_to_param[ghn__zwd])
                uglbg__zdlx = []
                if isinstance(rhs, ir.Var):
                    uglbg__zdlx = [rhs.name]
                elif isinstance(rhs, ir.Expr):
                    uglbg__zdlx = [axdy__tdda.name for axdy__tdda in
                        gwus__idms.value.list_vars()]
                param_uses[glhyi__awemo].extend(uglbg__zdlx)
                for axdy__tdda in uglbg__zdlx:
                    var_to_param[axdy__tdda] = glhyi__awemo
            if isinstance(gwus__idms, Parfor):
                get_parfor_reductions(gwus__idms, parfor_params, calltypes,
                    reduce_varnames, param_uses, var_to_param)
    for dadu__syvk, uglbg__zdlx in param_uses.items():
        if dadu__syvk in uglbg__zdlx and dadu__syvk not in reduce_varnames:
            reduce_varnames.append(dadu__syvk)
    return reduce_varnames, var_to_param


@numba.extending.register_jitable
def dummy_agg_count(A):
    return len(A)
