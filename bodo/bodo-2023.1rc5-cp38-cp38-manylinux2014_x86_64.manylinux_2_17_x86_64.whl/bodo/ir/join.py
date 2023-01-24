"""IR node for the join and merge"""
from collections import defaultdict
from typing import Dict, List, Literal, Optional, Set, Tuple, Union
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes, replace_vars_inner, visit_vars_inner
from numba.extending import intrinsic
import bodo
from bodo.hiframes.table import TableType
from bodo.ir.connector import trim_extra_used_columns
from bodo.libs.array import arr_info_list_to_table, array_to_info, cpp_table_to_py_data, cross_join_table, delete_table, hash_join_table, py_data_to_cpp_table
from bodo.libs.timsort import getitem_arr_tup, setitem_arr_tup
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import _compute_table_column_uses, get_live_column_nums_block, ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import INDEX_SENTINEL, BodoError, MetaType, dtype_to_array_type, find_common_np_dtype, is_dtype_nullable, is_nullable_type, is_str_arr_type, to_nullable_type
from bodo.utils.utils import alloc_arr_tup, is_null_pointer
join_gen_cond_cfunc = {}
join_gen_cond_cfunc_addr = {}


@intrinsic
def add_join_gen_cond_cfunc_sym(typingctx, func, sym):

    def codegen(context, builder, signature, args):
        oexi__awaa = func.signature
        wbjz__ofn = lir.FunctionType(lir.IntType(1), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64), lir
            .IntType(64)])
        xbf__xzwz = cgutils.get_or_insert_function(builder.module,
            wbjz__ofn, sym._literal_value)
        builder.call(xbf__xzwz, [context.get_constant_null(oexi__awaa.args[
            0]), context.get_constant_null(oexi__awaa.args[1]), context.
            get_constant_null(oexi__awaa.args[2]), context.
            get_constant_null(oexi__awaa.args[3]), context.
            get_constant_null(oexi__awaa.args[4]), context.
            get_constant_null(oexi__awaa.args[5]), context.get_constant(
            types.int64, 0), context.get_constant(types.int64, 0)])
        context.add_linking_libs([join_gen_cond_cfunc[sym._literal_value].
            _library])
        return
    return types.none(func, sym), codegen


@numba.jit
def get_join_cond_addr(name):
    with numba.objmode(addr='int64'):
        addr = join_gen_cond_cfunc_addr[name]
    return addr


HOW_OPTIONS = Literal['inner', 'left', 'right', 'outer', 'asof', 'cross']


class Join(ir.Stmt):

    def __init__(self, left_keys: Union[List[str], str], right_keys: Union[
        List[str], str], out_data_vars: List[ir.Var], out_df_type: bodo.
        DataFrameType, left_vars: List[ir.Var], left_df_type: bodo.
        DataFrameType, right_vars: List[ir.Var], right_df_type: bodo.
        DataFrameType, how: HOW_OPTIONS, suffix_left: str, suffix_right:
        str, loc: ir.Loc, is_left: bool, is_right: bool, is_join: bool,
        left_index: bool, right_index: bool, indicator_col_num: int,
        is_na_equal: bool, gen_cond_expr: str, left_len_var: ir.Var,
        right_len_var: ir.Var):
        self.left_keys = left_keys
        self.right_keys = right_keys
        self.out_data_vars = out_data_vars
        self.out_col_names = out_df_type.columns
        self.left_vars = left_vars
        self.right_vars = right_vars
        self.how = how
        self.loc = loc
        self.is_left = is_left
        self.is_right = is_right
        self.is_join = is_join
        self.left_index = left_index
        self.right_index = right_index
        self.indicator_col_num = indicator_col_num
        self.is_na_equal = is_na_equal
        self.gen_cond_expr = gen_cond_expr
        self.left_len_var = left_len_var
        self.right_len_var = right_len_var
        self.n_out_table_cols = len(self.out_col_names)
        self.out_used_cols = set(range(self.n_out_table_cols))
        if self.out_data_vars[1] is not None:
            self.out_used_cols.add(self.n_out_table_cols)
        xven__tjsuk = left_df_type.columns
        ibl__tan = right_df_type.columns
        self.left_col_names = xven__tjsuk
        self.right_col_names = ibl__tan
        self.is_left_table = left_df_type.is_table_format
        self.is_right_table = right_df_type.is_table_format
        self.n_left_table_cols = len(xven__tjsuk) if self.is_left_table else 0
        self.n_right_table_cols = len(ibl__tan) if self.is_right_table else 0
        mxabr__lng = self.n_left_table_cols if self.is_left_table else len(
            left_vars) - 1
        vdpmf__hcnvd = self.n_right_table_cols if self.is_right_table else len(
            right_vars) - 1
        self.left_dead_var_inds = set()
        self.right_dead_var_inds = set()
        if self.left_vars[-1] is None:
            self.left_dead_var_inds.add(mxabr__lng)
        if self.right_vars[-1] is None:
            self.right_dead_var_inds.add(vdpmf__hcnvd)
        self.left_var_map = {ecija__vrw: gjiam__ljyt for gjiam__ljyt,
            ecija__vrw in enumerate(xven__tjsuk)}
        self.right_var_map = {ecija__vrw: gjiam__ljyt for gjiam__ljyt,
            ecija__vrw in enumerate(ibl__tan)}
        if self.left_vars[-1] is not None:
            self.left_var_map[INDEX_SENTINEL] = mxabr__lng
        if self.right_vars[-1] is not None:
            self.right_var_map[INDEX_SENTINEL] = vdpmf__hcnvd
        self.left_key_set = set(self.left_var_map[ecija__vrw] for
            ecija__vrw in left_keys)
        self.right_key_set = set(self.right_var_map[ecija__vrw] for
            ecija__vrw in right_keys)
        if gen_cond_expr:
            self.left_cond_cols = set(self.left_var_map[ecija__vrw] for
                ecija__vrw in xven__tjsuk if f'(left.{ecija__vrw})' in
                gen_cond_expr)
            self.right_cond_cols = set(self.right_var_map[ecija__vrw] for
                ecija__vrw in ibl__tan if f'(right.{ecija__vrw})' in
                gen_cond_expr)
        else:
            self.left_cond_cols = set()
            self.right_cond_cols = set()
        uoox__dvso: int = -1
        van__rtt = set(left_keys) & set(right_keys)
        jqdz__typw = set(xven__tjsuk) & set(ibl__tan)
        nmqd__euf = jqdz__typw - van__rtt
        veb__hpkfq: Dict[int, (Literal['left', 'right'], int)] = {}
        kkvm__tsdb: Dict[int, int] = {}
        mbscl__mnj: Dict[int, int] = {}
        for gjiam__ljyt, ecija__vrw in enumerate(xven__tjsuk):
            if ecija__vrw in nmqd__euf:
                stc__miikq = str(ecija__vrw) + suffix_left
                dbshd__ckt = out_df_type.column_index[stc__miikq]
                if (right_index and not left_index and gjiam__ljyt in self.
                    left_key_set):
                    uoox__dvso = out_df_type.column_index[ecija__vrw]
                    veb__hpkfq[uoox__dvso] = 'left', gjiam__ljyt
            else:
                dbshd__ckt = out_df_type.column_index[ecija__vrw]
            veb__hpkfq[dbshd__ckt] = 'left', gjiam__ljyt
            kkvm__tsdb[gjiam__ljyt] = dbshd__ckt
        for gjiam__ljyt, ecija__vrw in enumerate(ibl__tan):
            if ecija__vrw not in van__rtt:
                if ecija__vrw in nmqd__euf:
                    zetf__wkj = str(ecija__vrw) + suffix_right
                    dbshd__ckt = out_df_type.column_index[zetf__wkj]
                    if (left_index and not right_index and gjiam__ljyt in
                        self.right_key_set):
                        uoox__dvso = out_df_type.column_index[ecija__vrw]
                        veb__hpkfq[uoox__dvso] = 'right', gjiam__ljyt
                else:
                    dbshd__ckt = out_df_type.column_index[ecija__vrw]
                veb__hpkfq[dbshd__ckt] = 'right', gjiam__ljyt
                mbscl__mnj[gjiam__ljyt] = dbshd__ckt
        if self.left_vars[-1] is not None:
            kkvm__tsdb[mxabr__lng] = self.n_out_table_cols
        if self.right_vars[-1] is not None:
            mbscl__mnj[vdpmf__hcnvd] = self.n_out_table_cols
        self.out_to_input_col_map = veb__hpkfq
        self.left_to_output_map = kkvm__tsdb
        self.right_to_output_map = mbscl__mnj
        self.extra_data_col_num = uoox__dvso
        if self.out_data_vars[1] is not None:
            lomhe__bwhwq = 'left' if right_index else 'right'
            if lomhe__bwhwq == 'left':
                byrs__dxz = mxabr__lng
            elif lomhe__bwhwq == 'right':
                byrs__dxz = vdpmf__hcnvd
        else:
            lomhe__bwhwq = None
            byrs__dxz = -1
        self.index_source = lomhe__bwhwq
        self.index_col_num = byrs__dxz
        hjd__xcth = []
        tren__qnj = len(left_keys)
        for deft__bge in range(tren__qnj):
            fzgg__eky = left_keys[deft__bge]
            fvfp__tnwy = right_keys[deft__bge]
            hjd__xcth.append(fzgg__eky == fvfp__tnwy)
        self.vect_same_key = hjd__xcth

    @property
    def has_live_left_table_var(self):
        return self.is_left_table and self.left_vars[0] is not None

    @property
    def has_live_right_table_var(self):
        return self.is_right_table and self.right_vars[0] is not None

    @property
    def has_live_out_table_var(self):
        return self.out_data_vars[0] is not None

    @property
    def has_live_out_index_var(self):
        return self.out_data_vars[1] is not None

    def get_out_table_var(self):
        return self.out_data_vars[0]

    def get_out_index_var(self):
        return self.out_data_vars[1]

    def get_live_left_vars(self):
        vars = []
        for nina__gtixp in self.left_vars:
            if nina__gtixp is not None:
                vars.append(nina__gtixp)
        return vars

    def get_live_right_vars(self):
        vars = []
        for nina__gtixp in self.right_vars:
            if nina__gtixp is not None:
                vars.append(nina__gtixp)
        return vars

    def get_live_out_vars(self):
        vars = []
        for nina__gtixp in self.out_data_vars:
            if nina__gtixp is not None:
                vars.append(nina__gtixp)
        return vars

    def set_live_left_vars(self, live_data_vars):
        left_vars = []
        zehvl__qua = 0
        start = 0
        if self.is_left_table:
            if self.has_live_left_table_var:
                left_vars.append(live_data_vars[zehvl__qua])
                zehvl__qua += 1
            else:
                left_vars.append(None)
            start = 1
        lbchy__taxaj = max(self.n_left_table_cols - 1, 0)
        for gjiam__ljyt in range(start, len(self.left_vars)):
            if gjiam__ljyt + lbchy__taxaj in self.left_dead_var_inds:
                left_vars.append(None)
            else:
                left_vars.append(live_data_vars[zehvl__qua])
                zehvl__qua += 1
        self.left_vars = left_vars

    def set_live_right_vars(self, live_data_vars):
        right_vars = []
        zehvl__qua = 0
        start = 0
        if self.is_right_table:
            if self.has_live_right_table_var:
                right_vars.append(live_data_vars[zehvl__qua])
                zehvl__qua += 1
            else:
                right_vars.append(None)
            start = 1
        lbchy__taxaj = max(self.n_right_table_cols - 1, 0)
        for gjiam__ljyt in range(start, len(self.right_vars)):
            if gjiam__ljyt + lbchy__taxaj in self.right_dead_var_inds:
                right_vars.append(None)
            else:
                right_vars.append(live_data_vars[zehvl__qua])
                zehvl__qua += 1
        self.right_vars = right_vars

    def set_live_out_data_vars(self, live_data_vars):
        out_data_vars = []
        gwj__vdtql = [self.has_live_out_table_var, self.has_live_out_index_var]
        zehvl__qua = 0
        for gjiam__ljyt in range(len(self.out_data_vars)):
            if not gwj__vdtql[gjiam__ljyt]:
                out_data_vars.append(None)
            else:
                out_data_vars.append(live_data_vars[zehvl__qua])
                zehvl__qua += 1
        self.out_data_vars = out_data_vars

    def get_out_table_used_cols(self):
        return {gjiam__ljyt for gjiam__ljyt in self.out_used_cols if 
            gjiam__ljyt < self.n_out_table_cols}

    def __repr__(self):
        qsuux__lsmwf = ', '.join([f'{ecija__vrw}' for ecija__vrw in self.
            left_col_names])
        gqdy__adq = f'left={{{qsuux__lsmwf}}}'
        qsuux__lsmwf = ', '.join([f'{ecija__vrw}' for ecija__vrw in self.
            right_col_names])
        gbrig__uaty = f'right={{{qsuux__lsmwf}}}'
        return 'join [{}={}]: {}, {}'.format(self.left_keys, self.
            right_keys, gqdy__adq, gbrig__uaty)


def join_array_analysis(join_node, equiv_set, typemap, array_analysis):
    gslth__yyi = []
    assert len(join_node.get_live_out_vars()
        ) > 0, 'empty join in array analysis'
    rlgdc__ontwg = []
    mwuz__ufy = join_node.get_live_left_vars()
    for xqyq__nkr in mwuz__ufy:
        tbtn__yeg = typemap[xqyq__nkr.name]
        gjox__kwds = equiv_set.get_shape(xqyq__nkr)
        if gjox__kwds:
            rlgdc__ontwg.append(gjox__kwds[0])
    if len(rlgdc__ontwg) > 1:
        equiv_set.insert_equiv(*rlgdc__ontwg)
    rlgdc__ontwg = []
    mwuz__ufy = list(join_node.get_live_right_vars())
    for xqyq__nkr in mwuz__ufy:
        tbtn__yeg = typemap[xqyq__nkr.name]
        gjox__kwds = equiv_set.get_shape(xqyq__nkr)
        if gjox__kwds:
            rlgdc__ontwg.append(gjox__kwds[0])
    if len(rlgdc__ontwg) > 1:
        equiv_set.insert_equiv(*rlgdc__ontwg)
    rlgdc__ontwg = []
    for onse__qql in join_node.get_live_out_vars():
        tbtn__yeg = typemap[onse__qql.name]
        vhwt__yty = array_analysis._gen_shape_call(equiv_set, onse__qql,
            tbtn__yeg.ndim, None, gslth__yyi)
        equiv_set.insert_equiv(onse__qql, vhwt__yty)
        rlgdc__ontwg.append(vhwt__yty[0])
        equiv_set.define(onse__qql, set())
    if len(rlgdc__ontwg) > 1:
        equiv_set.insert_equiv(*rlgdc__ontwg)
    return [], gslth__yyi


numba.parfors.array_analysis.array_analysis_extensions[Join
    ] = join_array_analysis


def join_distributed_analysis(join_node, array_dists):
    cxqyp__duzu = Distribution.OneD
    eapu__awqbg = Distribution.OneD
    for xqyq__nkr in join_node.get_live_left_vars():
        cxqyp__duzu = Distribution(min(cxqyp__duzu.value, array_dists[
            xqyq__nkr.name].value))
    for xqyq__nkr in join_node.get_live_right_vars():
        eapu__awqbg = Distribution(min(eapu__awqbg.value, array_dists[
            xqyq__nkr.name].value))
    zoy__xcmdc = Distribution.OneD_Var
    for onse__qql in join_node.get_live_out_vars():
        if onse__qql.name in array_dists:
            zoy__xcmdc = Distribution(min(zoy__xcmdc.value, array_dists[
                onse__qql.name].value))
    vsw__srbj = Distribution(min(zoy__xcmdc.value, cxqyp__duzu.value))
    vjojn__raub = Distribution(min(zoy__xcmdc.value, eapu__awqbg.value))
    zoy__xcmdc = Distribution(max(vsw__srbj.value, vjojn__raub.value))
    for onse__qql in join_node.get_live_out_vars():
        array_dists[onse__qql.name] = zoy__xcmdc
    if zoy__xcmdc != Distribution.OneD_Var:
        cxqyp__duzu = zoy__xcmdc
        eapu__awqbg = zoy__xcmdc
    for xqyq__nkr in join_node.get_live_left_vars():
        array_dists[xqyq__nkr.name] = cxqyp__duzu
    for xqyq__nkr in join_node.get_live_right_vars():
        array_dists[xqyq__nkr.name] = eapu__awqbg
    join_node.left_dist = cxqyp__duzu
    join_node.right_dist = eapu__awqbg


distributed_analysis.distributed_analysis_extensions[Join
    ] = join_distributed_analysis


def visit_vars_join(join_node, callback, cbdata):
    join_node.set_live_left_vars([visit_vars_inner(nina__gtixp, callback,
        cbdata) for nina__gtixp in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([visit_vars_inner(nina__gtixp, callback,
        cbdata) for nina__gtixp in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([visit_vars_inner(nina__gtixp,
        callback, cbdata) for nina__gtixp in join_node.get_live_out_vars()])
    if join_node.how == 'cross':
        join_node.left_len_var = visit_vars_inner(join_node.left_len_var,
            callback, cbdata)
        join_node.right_len_var = visit_vars_inner(join_node.right_len_var,
            callback, cbdata)


ir_utils.visit_vars_extensions[Join] = visit_vars_join


def _is_cross_join_len(join_node):
    return (join_node.how == 'cross' and not join_node.out_used_cols and
        join_node.has_live_out_table_var and not join_node.
        has_live_out_index_var)


def remove_dead_join(join_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if join_node.has_live_out_table_var:
        iseu__yxqt = []
        ihvjp__oml = join_node.get_out_table_var()
        if ihvjp__oml.name not in lives:
            join_node.out_data_vars[0] = None
            join_node.out_used_cols.difference_update(join_node.
                get_out_table_used_cols())
        for giana__cgqk in join_node.out_to_input_col_map.keys():
            if giana__cgqk in join_node.out_used_cols:
                continue
            iseu__yxqt.append(giana__cgqk)
            if join_node.indicator_col_num == giana__cgqk:
                join_node.indicator_col_num = -1
                continue
            if giana__cgqk == join_node.extra_data_col_num:
                join_node.extra_data_col_num = -1
                continue
            xqge__qxj, giana__cgqk = join_node.out_to_input_col_map[giana__cgqk
                ]
            if xqge__qxj == 'left':
                if (giana__cgqk not in join_node.left_key_set and 
                    giana__cgqk not in join_node.left_cond_cols):
                    join_node.left_dead_var_inds.add(giana__cgqk)
                    if not join_node.is_left_table:
                        join_node.left_vars[giana__cgqk] = None
            elif xqge__qxj == 'right':
                if (giana__cgqk not in join_node.right_key_set and 
                    giana__cgqk not in join_node.right_cond_cols):
                    join_node.right_dead_var_inds.add(giana__cgqk)
                    if not join_node.is_right_table:
                        join_node.right_vars[giana__cgqk] = None
        for gjiam__ljyt in iseu__yxqt:
            del join_node.out_to_input_col_map[gjiam__ljyt]
        if join_node.is_left_table:
            ewqid__pzvqb = set(range(join_node.n_left_table_cols))
            jbheg__tlz = not bool(ewqid__pzvqb - join_node.left_dead_var_inds)
            if jbheg__tlz:
                join_node.left_vars[0] = None
        if join_node.is_right_table:
            ewqid__pzvqb = set(range(join_node.n_right_table_cols))
            jbheg__tlz = not bool(ewqid__pzvqb - join_node.right_dead_var_inds)
            if jbheg__tlz:
                join_node.right_vars[0] = None
    if join_node.has_live_out_index_var:
        zam__dddbp = join_node.get_out_index_var()
        if zam__dddbp.name not in lives:
            join_node.out_data_vars[1] = None
            join_node.out_used_cols.remove(join_node.n_out_table_cols)
            if join_node.index_source == 'left':
                if (join_node.index_col_num not in join_node.left_key_set and
                    join_node.index_col_num not in join_node.left_cond_cols):
                    join_node.left_dead_var_inds.add(join_node.index_col_num)
                    join_node.left_vars[-1] = None
            elif join_node.index_col_num not in join_node.right_key_set and join_node.index_col_num not in join_node.right_cond_cols:
                join_node.right_dead_var_inds.add(join_node.index_col_num)
                join_node.right_vars[-1] = None
    if not (join_node.has_live_out_table_var or join_node.
        has_live_out_index_var):
        return None
    return join_node


ir_utils.remove_dead_extensions[Join] = remove_dead_join


def join_remove_dead_column(join_node, column_live_map, equiv_vars, typemap):
    ehxld__ndfl = False
    if join_node.has_live_out_table_var:
        xns__qpyvg = join_node.get_out_table_var().name
        pemnb__rsib, mhy__phi, csmm__zdfl = get_live_column_nums_block(
            column_live_map, equiv_vars, xns__qpyvg)
        if not (mhy__phi or csmm__zdfl):
            pemnb__rsib = trim_extra_used_columns(pemnb__rsib, join_node.
                n_out_table_cols)
            pqtz__jsf = join_node.get_out_table_used_cols()
            if len(pemnb__rsib) != len(pqtz__jsf):
                ehxld__ndfl = not (join_node.is_left_table and join_node.
                    is_right_table)
                fzdx__avdf = pqtz__jsf - pemnb__rsib
                join_node.out_used_cols = join_node.out_used_cols - fzdx__avdf
    return ehxld__ndfl


remove_dead_column_extensions[Join] = join_remove_dead_column


def join_table_column_use(join_node: Join, block_use_map: Dict[str, Tuple[
    Set[int], bool, bool]], equiv_vars: Dict[str, Set[str]], typemap: Dict[
    str, types.Type], table_col_use_map: Dict[int, Dict[str, Tuple[Set[int],
    bool, bool]]]):
    if not (join_node.is_left_table or join_node.is_right_table):
        return
    if join_node.has_live_out_table_var:
        xtf__qtoxr = join_node.get_out_table_var()
        fnavo__zoyt, mhy__phi, csmm__zdfl = _compute_table_column_uses(
            xtf__qtoxr.name, table_col_use_map, equiv_vars)
    else:
        fnavo__zoyt, mhy__phi, csmm__zdfl = set(), False, False
    if join_node.has_live_left_table_var:
        lal__txvwa = join_node.left_vars[0].name
        ovnfo__lxyoe, mlk__fhw, byvnd__adikj = block_use_map[lal__txvwa]
        if not (mlk__fhw or byvnd__adikj):
            rcy__tmxb = set([join_node.out_to_input_col_map[gjiam__ljyt][1] for
                gjiam__ljyt in fnavo__zoyt if join_node.
                out_to_input_col_map[gjiam__ljyt][0] == 'left'])
            mmtmm__cgq = set(gjiam__ljyt for gjiam__ljyt in join_node.
                left_key_set | join_node.left_cond_cols if gjiam__ljyt <
                join_node.n_left_table_cols)
            if not (mhy__phi or csmm__zdfl):
                join_node.left_dead_var_inds |= set(range(join_node.
                    n_left_table_cols)) - (rcy__tmxb | mmtmm__cgq)
            block_use_map[lal__txvwa] = (ovnfo__lxyoe | rcy__tmxb |
                mmtmm__cgq, mhy__phi or csmm__zdfl, False)
    if join_node.has_live_right_table_var:
        kwx__bfwg = join_node.right_vars[0].name
        ovnfo__lxyoe, mlk__fhw, byvnd__adikj = block_use_map[kwx__bfwg]
        if not (mlk__fhw or byvnd__adikj):
            hvm__eigxm = set([join_node.out_to_input_col_map[gjiam__ljyt][1
                ] for gjiam__ljyt in fnavo__zoyt if join_node.
                out_to_input_col_map[gjiam__ljyt][0] == 'right'])
            mmydz__kbs = set(gjiam__ljyt for gjiam__ljyt in join_node.
                right_key_set | join_node.right_cond_cols if gjiam__ljyt <
                join_node.n_right_table_cols)
            if not (mhy__phi or csmm__zdfl):
                join_node.right_dead_var_inds |= set(range(join_node.
                    n_right_table_cols)) - (hvm__eigxm | mmydz__kbs)
            block_use_map[kwx__bfwg] = (ovnfo__lxyoe | hvm__eigxm |
                mmydz__kbs, mhy__phi or csmm__zdfl, False)


ir_extension_table_column_use[Join] = join_table_column_use


def join_usedefs(join_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({zzjs__arcaj.name for zzjs__arcaj in join_node.
        get_live_left_vars()})
    use_set.update({zzjs__arcaj.name for zzjs__arcaj in join_node.
        get_live_right_vars()})
    def_set.update({zzjs__arcaj.name for zzjs__arcaj in join_node.
        get_live_out_vars()})
    if join_node.how == 'cross':
        use_set.add(join_node.left_len_var.name)
        use_set.add(join_node.right_len_var.name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Join] = join_usedefs


def get_copies_join(join_node, typemap):
    vxrci__tpft = set(zzjs__arcaj.name for zzjs__arcaj in join_node.
        get_live_out_vars())
    return set(), vxrci__tpft


ir_utils.copy_propagate_extensions[Join] = get_copies_join


def apply_copies_join(join_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    join_node.set_live_left_vars([replace_vars_inner(nina__gtixp, var_dict) for
        nina__gtixp in join_node.get_live_left_vars()])
    join_node.set_live_right_vars([replace_vars_inner(nina__gtixp, var_dict
        ) for nina__gtixp in join_node.get_live_right_vars()])
    join_node.set_live_out_data_vars([replace_vars_inner(nina__gtixp,
        var_dict) for nina__gtixp in join_node.get_live_out_vars()])
    if join_node.how == 'cross':
        join_node.left_len_var = replace_vars_inner(join_node.left_len_var,
            var_dict)
        join_node.right_len_var = replace_vars_inner(join_node.
            right_len_var, var_dict)


ir_utils.apply_copy_propagate_extensions[Join] = apply_copies_join


def build_join_definitions(join_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for xqyq__nkr in join_node.get_live_out_vars():
        definitions[xqyq__nkr.name].append(join_node)
    return definitions


ir_utils.build_defs_extensions[Join] = build_join_definitions


def _gen_cross_join_len(join_node, out_table_type, typemap, calltypes,
    typingctx, targetctx, left_parallel, right_parallel):
    func_text = 'def f(left_len, right_len):\n'
    atcns__fidp = 'bodo.libs.distributed_api.get_size()'
    qbi__ief = 'bodo.libs.distributed_api.get_rank()'
    if left_parallel:
        func_text += f"""  left_len = bodo.libs.distributed_api.get_node_portion(left_len, {atcns__fidp}, {qbi__ief})
"""
    if right_parallel and not left_parallel:
        func_text += f"""  right_len = bodo.libs.distributed_api.get_node_portion(right_len, {atcns__fidp}, {qbi__ief})
"""
    func_text += '  n_rows = left_len * right_len\n'
    func_text += '  py_table = init_table(py_table_type, False)\n'
    func_text += '  py_table = set_table_len(py_table, n_rows)\n'
    vqgv__miekw = {}
    exec(func_text, {}, vqgv__miekw)
    rnmj__yfrz = vqgv__miekw['f']
    glbs = {'py_table_type': out_table_type, 'init_table': bodo.hiframes.
        table.init_table, 'set_table_len': bodo.hiframes.table.
        set_table_len, 'sum_op': np.int32(bodo.libs.distributed_api.
        Reduce_Type.Sum.value), 'bodo': bodo}
    klzup__leuir = [join_node.left_len_var, join_node.right_len_var]
    vpog__xqtr = tuple(typemap[zzjs__arcaj.name] for zzjs__arcaj in
        klzup__leuir)
    bkrt__omly = compile_to_numba_ir(rnmj__yfrz, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=vpog__xqtr, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(bkrt__omly, klzup__leuir)
    dwsaw__cgaz = bkrt__omly.body[:-3]
    dwsaw__cgaz[-1].target = join_node.out_data_vars[0]
    return dwsaw__cgaz


def _gen_cross_join_repeat(join_node, out_table_type, typemap, calltypes,
    typingctx, targetctx, left_parallel, right_parallel, left_is_dead):
    mwuz__ufy = join_node.right_vars if left_is_dead else join_node.left_vars
    buh__ijbe = ', '.join(f't{gjiam__ljyt}' for gjiam__ljyt in range(len(
        mwuz__ufy)) if mwuz__ufy[gjiam__ljyt] is not None)
    pug__bqb = len(join_node.right_col_names) if left_is_dead else len(
        join_node.left_col_names)
    nkbqk__vhleb = (join_node.is_right_table if left_is_dead else join_node
        .is_left_table)
    ihyqy__ifk = (join_node.right_dead_var_inds if left_is_dead else
        join_node.left_dead_var_inds)
    hzwjv__xlq = [(f'get_table_data(t0, {gjiam__ljyt})' if nkbqk__vhleb else
        f't{gjiam__ljyt}') for gjiam__ljyt in range(pug__bqb)]
    xlfmv__vvu = ', '.join(
        f'bodo.libs.array_kernels.repeat_kernel({hzwjv__xlq[gjiam__ljyt]}, repeats)'
         if gjiam__ljyt not in ihyqy__ifk else 'None' for gjiam__ljyt in
        range(pug__bqb))
    fhx__nlfhr = len(out_table_type.arr_types)
    hhpku__scd = [join_node.out_to_input_col_map.get(gjiam__ljyt, (-1, -1))
        [1] for gjiam__ljyt in range(fhx__nlfhr)]
    atcns__fidp = 'bodo.libs.distributed_api.get_size()'
    qbi__ief = 'bodo.libs.distributed_api.get_rank()'
    dvr__ycto = 'left_len' if left_is_dead else 'right_len'
    lvsds__anhw = right_parallel if left_is_dead else left_parallel
    olhi__cnnt = left_parallel if left_is_dead else right_parallel
    btn__aonva = not lvsds__anhw and olhi__cnnt
    ilixi__ezedb = (
        f'bodo.libs.distributed_api.get_node_portion({dvr__ycto}, {atcns__fidp}, {qbi__ief})'
         if btn__aonva else dvr__ycto)
    func_text = f'def f({buh__ijbe}, left_len, right_len):\n'
    func_text += f'  repeats = {ilixi__ezedb}\n'
    func_text += f'  out_data = ({xlfmv__vvu},)\n'
    func_text += f"""  py_table = logical_table_to_table(out_data, (), col_inds, {pug__bqb}, out_table_type, used_cols)
"""
    vqgv__miekw = {}
    exec(func_text, {}, vqgv__miekw)
    rnmj__yfrz = vqgv__miekw['f']
    glbs = {'out_table_type': out_table_type, 'sum_op': np.int32(bodo.libs.
        distributed_api.Reduce_Type.Sum.value), 'bodo': bodo, 'used_cols':
        bodo.utils.typing.MetaType(tuple(join_node.out_used_cols)),
        'col_inds': bodo.utils.typing.MetaType(tuple(hhpku__scd)),
        'logical_table_to_table': bodo.hiframes.table.
        logical_table_to_table, 'get_table_data': bodo.hiframes.table.
        get_table_data}
    klzup__leuir = [zzjs__arcaj for zzjs__arcaj in mwuz__ufy if zzjs__arcaj
         is not None] + [join_node.left_len_var, join_node.right_len_var]
    vpog__xqtr = tuple(typemap[zzjs__arcaj.name] for zzjs__arcaj in
        klzup__leuir)
    bkrt__omly = compile_to_numba_ir(rnmj__yfrz, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=vpog__xqtr, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(bkrt__omly, klzup__leuir)
    dwsaw__cgaz = bkrt__omly.body[:-3]
    dwsaw__cgaz[-1].target = join_node.out_data_vars[0]
    return dwsaw__cgaz


def join_distributed_run(join_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 2:
        uouy__eow = join_node.loc.strformat()
        otkz__jzigr = [join_node.left_col_names[gjiam__ljyt] for
            gjiam__ljyt in sorted(set(range(len(join_node.left_col_names))) -
            join_node.left_dead_var_inds)]
        ssdto__tqzht = """Finished column elimination on join's left input:
%s
Left input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', ssdto__tqzht,
            uouy__eow, otkz__jzigr)
        fqk__xxxv = [join_node.right_col_names[gjiam__ljyt] for gjiam__ljyt in
            sorted(set(range(len(join_node.right_col_names))) - join_node.
            right_dead_var_inds)]
        ssdto__tqzht = """Finished column elimination on join's right input:
%s
Right input columns: %s
"""
        bodo.user_logging.log_message('Column Pruning', ssdto__tqzht,
            uouy__eow, fqk__xxxv)
        lcvy__bseul = [join_node.out_col_names[gjiam__ljyt] for gjiam__ljyt in
            sorted(join_node.get_out_table_used_cols())]
        ssdto__tqzht = (
            'Finished column pruning on join node:\n%s\nOutput columns: %s\n')
        bodo.user_logging.log_message('Column Pruning', ssdto__tqzht,
            uouy__eow, lcvy__bseul)
    left_parallel, right_parallel = False, False
    if array_dists is not None:
        left_parallel, right_parallel = _get_table_parallel_flags(join_node,
            array_dists)
    tren__qnj = len(join_node.left_keys)
    out_physical_to_logical_list = []
    if join_node.has_live_out_table_var:
        out_table_type = typemap[join_node.get_out_table_var().name]
    else:
        out_table_type = types.none
    if join_node.has_live_out_index_var:
        index_col_type = typemap[join_node.get_out_index_var().name]
    else:
        index_col_type = types.none
    if _is_cross_join_len(join_node):
        return _gen_cross_join_len(join_node, out_table_type, typemap,
            calltypes, typingctx, targetctx, left_parallel, right_parallel)
    elif join_node.how == 'cross' and all(gjiam__ljyt in join_node.
        left_dead_var_inds for gjiam__ljyt in range(len(join_node.
        left_col_names))):
        return _gen_cross_join_repeat(join_node, out_table_type, typemap,
            calltypes, typingctx, targetctx, left_parallel, right_parallel,
            True)
    elif join_node.how == 'cross' and all(gjiam__ljyt in join_node.
        right_dead_var_inds for gjiam__ljyt in range(len(join_node.
        right_col_names))):
        return _gen_cross_join_repeat(join_node, out_table_type, typemap,
            calltypes, typingctx, targetctx, left_parallel, right_parallel,
            False)
    if join_node.extra_data_col_num != -1:
        out_physical_to_logical_list.append(join_node.extra_data_col_num)
    left_key_in_output = []
    right_key_in_output = []
    left_used_key_nums = set()
    right_used_key_nums = set()
    zqqcl__gzhh = set()
    hbj__enhkx = set()
    left_logical_physical_map = {}
    right_logical_physical_map = {}
    left_physical_to_logical_list = []
    right_physical_to_logical_list = []
    wdzit__gqv = 0
    qsqw__xurv = 0
    itcik__vifn = []
    for orozv__yoc, ecija__vrw in enumerate(join_node.left_keys):
        idfw__yobr = join_node.left_var_map[ecija__vrw]
        if not join_node.is_left_table:
            itcik__vifn.append(join_node.left_vars[idfw__yobr])
        gwj__vdtql = 1
        dbshd__ckt = join_node.left_to_output_map[idfw__yobr]
        if ecija__vrw == INDEX_SENTINEL:
            if (join_node.has_live_out_index_var and join_node.index_source ==
                'left' and join_node.index_col_num == idfw__yobr):
                out_physical_to_logical_list.append(dbshd__ckt)
                left_used_key_nums.add(orozv__yoc)
                zqqcl__gzhh.add(idfw__yobr)
            else:
                gwj__vdtql = 0
        elif dbshd__ckt not in join_node.out_used_cols:
            gwj__vdtql = 0
        elif idfw__yobr in zqqcl__gzhh:
            gwj__vdtql = 0
        else:
            left_used_key_nums.add(orozv__yoc)
            zqqcl__gzhh.add(idfw__yobr)
            out_physical_to_logical_list.append(dbshd__ckt)
        left_physical_to_logical_list.append(idfw__yobr)
        left_logical_physical_map[idfw__yobr] = wdzit__gqv
        wdzit__gqv += 1
        left_key_in_output.append(gwj__vdtql)
    itcik__vifn = tuple(itcik__vifn)
    txd__boff = []
    for gjiam__ljyt in range(len(join_node.left_col_names)):
        if (gjiam__ljyt not in join_node.left_dead_var_inds and gjiam__ljyt
             not in join_node.left_key_set):
            if not join_node.is_left_table:
                zzjs__arcaj = join_node.left_vars[gjiam__ljyt]
                txd__boff.append(zzjs__arcaj)
            cpkt__nht = 1
            ekxbh__tuqj = 1
            dbshd__ckt = join_node.left_to_output_map[gjiam__ljyt]
            if gjiam__ljyt in join_node.left_cond_cols:
                if dbshd__ckt not in join_node.out_used_cols:
                    cpkt__nht = 0
                left_key_in_output.append(cpkt__nht)
            elif gjiam__ljyt in join_node.left_dead_var_inds:
                cpkt__nht = 0
                ekxbh__tuqj = 0
            if cpkt__nht:
                out_physical_to_logical_list.append(dbshd__ckt)
            if ekxbh__tuqj:
                left_physical_to_logical_list.append(gjiam__ljyt)
                left_logical_physical_map[gjiam__ljyt] = wdzit__gqv
                wdzit__gqv += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'left' and join_node.index_col_num not in join_node.left_key_set):
        if not join_node.is_left_table:
            txd__boff.append(join_node.left_vars[join_node.index_col_num])
        dbshd__ckt = join_node.left_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(dbshd__ckt)
        left_physical_to_logical_list.append(join_node.index_col_num)
    txd__boff = tuple(txd__boff)
    if join_node.is_left_table:
        txd__boff = tuple(join_node.get_live_left_vars())
    qzqh__mupgs = []
    for orozv__yoc, ecija__vrw in enumerate(join_node.right_keys):
        idfw__yobr = join_node.right_var_map[ecija__vrw]
        if not join_node.is_right_table:
            qzqh__mupgs.append(join_node.right_vars[idfw__yobr])
        if not join_node.vect_same_key[orozv__yoc] and not join_node.is_join:
            gwj__vdtql = 1
            if idfw__yobr not in join_node.right_to_output_map:
                gwj__vdtql = 0
            else:
                dbshd__ckt = join_node.right_to_output_map[idfw__yobr]
                if ecija__vrw == INDEX_SENTINEL:
                    if (join_node.has_live_out_index_var and join_node.
                        index_source == 'right' and join_node.index_col_num ==
                        idfw__yobr):
                        out_physical_to_logical_list.append(dbshd__ckt)
                        right_used_key_nums.add(orozv__yoc)
                        hbj__enhkx.add(idfw__yobr)
                    else:
                        gwj__vdtql = 0
                elif dbshd__ckt not in join_node.out_used_cols:
                    gwj__vdtql = 0
                elif idfw__yobr in hbj__enhkx:
                    gwj__vdtql = 0
                else:
                    right_used_key_nums.add(orozv__yoc)
                    hbj__enhkx.add(idfw__yobr)
                    out_physical_to_logical_list.append(dbshd__ckt)
            right_key_in_output.append(gwj__vdtql)
        right_physical_to_logical_list.append(idfw__yobr)
        right_logical_physical_map[idfw__yobr] = qsqw__xurv
        qsqw__xurv += 1
    qzqh__mupgs = tuple(qzqh__mupgs)
    hak__flwuj = []
    for gjiam__ljyt in range(len(join_node.right_col_names)):
        if (gjiam__ljyt not in join_node.right_dead_var_inds and 
            gjiam__ljyt not in join_node.right_key_set):
            if not join_node.is_right_table:
                hak__flwuj.append(join_node.right_vars[gjiam__ljyt])
            cpkt__nht = 1
            ekxbh__tuqj = 1
            dbshd__ckt = join_node.right_to_output_map[gjiam__ljyt]
            if gjiam__ljyt in join_node.right_cond_cols:
                if dbshd__ckt not in join_node.out_used_cols:
                    cpkt__nht = 0
                right_key_in_output.append(cpkt__nht)
            elif gjiam__ljyt in join_node.right_dead_var_inds:
                cpkt__nht = 0
                ekxbh__tuqj = 0
            if cpkt__nht:
                out_physical_to_logical_list.append(dbshd__ckt)
            if ekxbh__tuqj:
                right_physical_to_logical_list.append(gjiam__ljyt)
                right_logical_physical_map[gjiam__ljyt] = qsqw__xurv
                qsqw__xurv += 1
    if (join_node.has_live_out_index_var and join_node.index_source ==
        'right' and join_node.index_col_num not in join_node.right_key_set):
        if not join_node.is_right_table:
            hak__flwuj.append(join_node.right_vars[join_node.index_col_num])
        dbshd__ckt = join_node.right_to_output_map[join_node.index_col_num]
        out_physical_to_logical_list.append(dbshd__ckt)
        right_physical_to_logical_list.append(join_node.index_col_num)
    hak__flwuj = tuple(hak__flwuj)
    if join_node.is_right_table:
        hak__flwuj = tuple(join_node.get_live_right_vars())
    if join_node.indicator_col_num != -1:
        out_physical_to_logical_list.append(join_node.indicator_col_num)
    klzup__leuir = itcik__vifn + qzqh__mupgs + txd__boff + hak__flwuj
    vpog__xqtr = tuple(typemap[zzjs__arcaj.name] for zzjs__arcaj in
        klzup__leuir)
    left_other_names = tuple('t1_c' + str(gjiam__ljyt) for gjiam__ljyt in
        range(len(txd__boff)))
    right_other_names = tuple('t2_c' + str(gjiam__ljyt) for gjiam__ljyt in
        range(len(hak__flwuj)))
    if join_node.is_left_table:
        ocfq__wdwdm = ()
    else:
        ocfq__wdwdm = tuple('t1_key' + str(gjiam__ljyt) for gjiam__ljyt in
            range(tren__qnj))
    if join_node.is_right_table:
        rudqr__lfuw = ()
    else:
        rudqr__lfuw = tuple('t2_key' + str(gjiam__ljyt) for gjiam__ljyt in
            range(tren__qnj))
    glbs = {}
    loc = join_node.loc
    func_text = 'def f({}):\n'.format(','.join(ocfq__wdwdm + rudqr__lfuw +
        left_other_names + right_other_names))
    if join_node.is_left_table:
        left_key_types = []
        left_other_types = []
        if join_node.has_live_left_table_var:
            twprf__nketm = typemap[join_node.left_vars[0].name]
        else:
            twprf__nketm = types.none
        for xzu__lmu in left_physical_to_logical_list:
            if xzu__lmu < join_node.n_left_table_cols:
                assert join_node.has_live_left_table_var, 'No logical columns should refer to a dead table'
                tbtn__yeg = twprf__nketm.arr_types[xzu__lmu]
            else:
                tbtn__yeg = typemap[join_node.left_vars[-1].name]
            if xzu__lmu in join_node.left_key_set:
                left_key_types.append(tbtn__yeg)
            else:
                left_other_types.append(tbtn__yeg)
        left_key_types = tuple(left_key_types)
        left_other_types = tuple(left_other_types)
    else:
        left_key_types = tuple(typemap[zzjs__arcaj.name] for zzjs__arcaj in
            itcik__vifn)
        left_other_types = tuple([typemap[ecija__vrw.name] for ecija__vrw in
            txd__boff])
    if join_node.is_right_table:
        right_key_types = []
        right_other_types = []
        if join_node.has_live_right_table_var:
            twprf__nketm = typemap[join_node.right_vars[0].name]
        else:
            twprf__nketm = types.none
        for xzu__lmu in right_physical_to_logical_list:
            if xzu__lmu < join_node.n_right_table_cols:
                assert join_node.has_live_right_table_var, 'No logical columns should refer to a dead table'
                tbtn__yeg = twprf__nketm.arr_types[xzu__lmu]
            else:
                tbtn__yeg = typemap[join_node.right_vars[-1].name]
            if xzu__lmu in join_node.right_key_set:
                right_key_types.append(tbtn__yeg)
            else:
                right_other_types.append(tbtn__yeg)
        right_key_types = tuple(right_key_types)
        right_other_types = tuple(right_other_types)
    else:
        right_key_types = tuple(typemap[zzjs__arcaj.name] for zzjs__arcaj in
            qzqh__mupgs)
        right_other_types = tuple([typemap[ecija__vrw.name] for ecija__vrw in
            hak__flwuj])
    matched_key_types = []
    for gjiam__ljyt in range(tren__qnj):
        vtyq__rkzv = _match_join_key_types(left_key_types[gjiam__ljyt],
            right_key_types[gjiam__ljyt], loc)
        glbs[f'key_type_{gjiam__ljyt}'] = vtyq__rkzv
        matched_key_types.append(vtyq__rkzv)
    if join_node.is_left_table:
        jie__ybv = determine_table_cast_map(matched_key_types,
            left_key_types, None, {gjiam__ljyt: join_node.left_var_map[
            qcgh__oorlo] for gjiam__ljyt, qcgh__oorlo in enumerate(
            join_node.left_keys)}, True)
        if jie__ybv:
            mra__wsr = False
            cntw__ccav = False
            lkmc__rdmta = None
            if join_node.has_live_left_table_var:
                ojdvx__bquw = list(typemap[join_node.left_vars[0].name].
                    arr_types)
            else:
                ojdvx__bquw = None
            for giana__cgqk, tbtn__yeg in jie__ybv.items():
                if giana__cgqk < join_node.n_left_table_cols:
                    assert join_node.has_live_left_table_var, 'Casting columns for a dead table should not occur'
                    ojdvx__bquw[giana__cgqk] = tbtn__yeg
                    mra__wsr = True
                else:
                    lkmc__rdmta = tbtn__yeg
                    cntw__ccav = True
            if mra__wsr:
                func_text += f"""    {left_other_names[0]} = bodo.utils.table_utils.table_astype({left_other_names[0]}, left_cast_table_type, False, _bodo_nan_to_str=False, used_cols=left_used_cols)
"""
                glbs['left_cast_table_type'] = TableType(tuple(ojdvx__bquw))
                glbs['left_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_left_table_cols)) - join_node.
                    left_dead_var_inds)))
            if cntw__ccav:
                func_text += f"""    {left_other_names[1]} = bodo.utils.utils.astype({left_other_names[1]}, left_cast_index_type)
"""
                glbs['left_cast_index_type'] = lkmc__rdmta
    else:
        func_text += '    t1_keys = ({}{})\n'.format(', '.join(
            f'bodo.utils.utils.astype({ocfq__wdwdm[gjiam__ljyt]}, key_type_{gjiam__ljyt})'
             if left_key_types[gjiam__ljyt] != matched_key_types[
            gjiam__ljyt] else f'{ocfq__wdwdm[gjiam__ljyt]}' for gjiam__ljyt in
            range(tren__qnj)), ',' if tren__qnj != 0 else '')
        func_text += '    data_left = ({}{})\n'.format(','.join(
            left_other_names), ',' if len(left_other_names) != 0 else '')
    if join_node.is_right_table:
        jie__ybv = determine_table_cast_map(matched_key_types,
            right_key_types, None, {gjiam__ljyt: join_node.right_var_map[
            qcgh__oorlo] for gjiam__ljyt, qcgh__oorlo in enumerate(
            join_node.right_keys)}, True)
        if jie__ybv:
            mra__wsr = False
            cntw__ccav = False
            lkmc__rdmta = None
            if join_node.has_live_right_table_var:
                ojdvx__bquw = list(typemap[join_node.right_vars[0].name].
                    arr_types)
            else:
                ojdvx__bquw = None
            for giana__cgqk, tbtn__yeg in jie__ybv.items():
                if giana__cgqk < join_node.n_right_table_cols:
                    assert join_node.has_live_right_table_var, 'Casting columns for a dead table should not occur'
                    ojdvx__bquw[giana__cgqk] = tbtn__yeg
                    mra__wsr = True
                else:
                    lkmc__rdmta = tbtn__yeg
                    cntw__ccav = True
            if mra__wsr:
                func_text += f"""    {right_other_names[0]} = bodo.utils.table_utils.table_astype({right_other_names[0]}, right_cast_table_type, False, _bodo_nan_to_str=False, used_cols=right_used_cols)
"""
                glbs['right_cast_table_type'] = TableType(tuple(ojdvx__bquw))
                glbs['right_used_cols'] = MetaType(tuple(sorted(set(range(
                    join_node.n_right_table_cols)) - join_node.
                    right_dead_var_inds)))
            if cntw__ccav:
                func_text += f"""    {right_other_names[1]} = bodo.utils.utils.astype({right_other_names[1]}, left_cast_index_type)
"""
                glbs['right_cast_index_type'] = lkmc__rdmta
    else:
        func_text += '    t2_keys = ({}{})\n'.format(', '.join(
            f'bodo.utils.utils.astype({rudqr__lfuw[gjiam__ljyt]}, key_type_{gjiam__ljyt})'
             if right_key_types[gjiam__ljyt] != matched_key_types[
            gjiam__ljyt] else f'{rudqr__lfuw[gjiam__ljyt]}' for gjiam__ljyt in
            range(tren__qnj)), ',' if tren__qnj != 0 else '')
        func_text += '    data_right = ({}{})\n'.format(','.join(
            right_other_names), ',' if len(right_other_names) != 0 else '')
    general_cond_cfunc, left_col_nums, right_col_nums = (
        _gen_general_cond_cfunc(join_node, typemap,
        left_logical_physical_map, right_logical_physical_map))
    if join_node.how == 'asof':
        if left_parallel or right_parallel:
            assert left_parallel and right_parallel, 'pd.merge_asof requires both left and right to be replicated or distributed'
            func_text += """    t2_keys, data_right = parallel_asof_comm(t1_keys, t2_keys, data_right)
"""
        func_text += """    out_t1_keys, out_t2_keys, out_data_left, out_data_right = bodo.ir.join.local_merge_asof(t1_keys, t2_keys, data_left, data_right)
"""
    else:
        func_text += _gen_join_cpp_call(join_node, left_key_types,
            right_key_types, matched_key_types, left_other_names,
            right_other_names, left_other_types, right_other_types,
            left_key_in_output, right_key_in_output, left_parallel,
            right_parallel, glbs, out_physical_to_logical_list,
            out_table_type, index_col_type, join_node.
            get_out_table_used_cols(), left_used_key_nums,
            right_used_key_nums, general_cond_cfunc, left_col_nums,
            right_col_nums, left_physical_to_logical_list,
            right_physical_to_logical_list)
    if join_node.how == 'asof':
        for gjiam__ljyt in range(len(left_other_names)):
            func_text += '    left_{} = out_data_left[{}]\n'.format(gjiam__ljyt
                , gjiam__ljyt)
        for gjiam__ljyt in range(len(right_other_names)):
            func_text += '    right_{} = out_data_right[{}]\n'.format(
                gjiam__ljyt, gjiam__ljyt)
        for gjiam__ljyt in range(tren__qnj):
            func_text += (
                f'    t1_keys_{gjiam__ljyt} = out_t1_keys[{gjiam__ljyt}]\n')
        for gjiam__ljyt in range(tren__qnj):
            func_text += (
                f'    t2_keys_{gjiam__ljyt} = out_t2_keys[{gjiam__ljyt}]\n')
    vqgv__miekw = {}
    exec(func_text, {}, vqgv__miekw)
    rnmj__yfrz = vqgv__miekw['f']
    glbs.update({'bodo': bodo, 'np': np, 'pd': pd, 'parallel_asof_comm':
        parallel_asof_comm, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'cross_join_table': cross_join_table, 'hash_join_table':
        hash_join_table, 'delete_table': delete_table,
        'add_join_gen_cond_cfunc_sym': add_join_gen_cond_cfunc_sym,
        'get_join_cond_addr': get_join_cond_addr, 'key_in_output': np.array
        (left_key_in_output + right_key_in_output, dtype=np.bool_),
        'py_data_to_cpp_table': py_data_to_cpp_table,
        'cpp_table_to_py_data': cpp_table_to_py_data})
    if general_cond_cfunc:
        glbs.update({'general_cond_cfunc': general_cond_cfunc})
    bkrt__omly = compile_to_numba_ir(rnmj__yfrz, glbs, typingctx=typingctx,
        targetctx=targetctx, arg_typs=vpog__xqtr, typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(bkrt__omly, klzup__leuir)
    dwsaw__cgaz = bkrt__omly.body[:-3]
    if join_node.has_live_out_index_var:
        dwsaw__cgaz[-1].target = join_node.out_data_vars[1]
    if join_node.has_live_out_table_var:
        dwsaw__cgaz[-2].target = join_node.out_data_vars[0]
    assert join_node.has_live_out_index_var or join_node.has_live_out_table_var, 'At most one of table and index should be dead if the Join IR node is live'
    if not join_node.has_live_out_index_var:
        dwsaw__cgaz.pop(-1)
    elif not join_node.has_live_out_table_var:
        dwsaw__cgaz.pop(-2)
    return dwsaw__cgaz


distributed_pass.distributed_run_extensions[Join] = join_distributed_run


def _gen_general_cond_cfunc(join_node, typemap, left_logical_physical_map,
    right_logical_physical_map):
    expr = join_node.gen_cond_expr
    if not expr:
        return None, [], []
    ksebb__odgkx = next_label()
    table_getitem_funcs = {'bodo': bodo, 'numba': numba, 'is_null_pointer':
        is_null_pointer}
    na_check_name = 'NOT_NA'
    func_text = f"""def bodo_join_gen_cond{ksebb__odgkx}(left_table, right_table, left_data1, right_data1, left_null_bitmap, right_null_bitmap, left_ind, right_ind):
"""
    func_text += '  if is_null_pointer(left_table):\n'
    func_text += '    return False\n'
    expr, func_text, left_col_nums = _replace_column_accesses(expr,
        left_logical_physical_map, join_node.left_var_map, typemap,
        join_node.left_vars, table_getitem_funcs, func_text, 'left',
        join_node.left_key_set, na_check_name, join_node.is_left_table)
    expr, func_text, right_col_nums = _replace_column_accesses(expr,
        right_logical_physical_map, join_node.right_var_map, typemap,
        join_node.right_vars, table_getitem_funcs, func_text, 'right',
        join_node.right_key_set, na_check_name, join_node.is_right_table)
    expr = expr.replace(' & ', ' and ').replace(' | ', ' or ')
    func_text += f'  return {expr}'
    vqgv__miekw = {}
    exec(func_text, table_getitem_funcs, vqgv__miekw)
    padml__hqcev = vqgv__miekw[f'bodo_join_gen_cond{ksebb__odgkx}']
    wwd__ilvo = types.bool_(types.voidptr, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.int64, types.int64)
    nmcna__invek = numba.cfunc(wwd__ilvo, nopython=True)(padml__hqcev)
    join_gen_cond_cfunc[nmcna__invek.native_name] = nmcna__invek
    join_gen_cond_cfunc_addr[nmcna__invek.native_name] = nmcna__invek.address
    return nmcna__invek, left_col_nums, right_col_nums


def _replace_column_accesses(expr, logical_to_physical_ind, name_to_var_map,
    typemap, col_vars, table_getitem_funcs, func_text, table_name, key_set,
    na_check_name, is_table_var):
    tdgbn__dzlvx = []
    for ecija__vrw, ebcj__dpute in name_to_var_map.items():
        tsxvs__whm = f'({table_name}.{ecija__vrw})'
        if tsxvs__whm not in expr:
            continue
        keeu__gjpee = f'getitem_{table_name}_val_{ebcj__dpute}'
        if is_table_var:
            ojpj__iryd = typemap[col_vars[0].name].arr_types[ebcj__dpute]
        else:
            ojpj__iryd = typemap[col_vars[ebcj__dpute].name]
        if is_str_arr_type(ojpj__iryd) or ojpj__iryd == bodo.binary_array_type:
            adk__cqf = f'{keeu__gjpee}({table_name}_table, {table_name}_ind)\n'
        else:
            adk__cqf = f'{keeu__gjpee}({table_name}_data1, {table_name}_ind)\n'
        bisi__rkvq = logical_to_physical_ind[ebcj__dpute]
        table_getitem_funcs[keeu__gjpee
            ] = bodo.libs.array._gen_row_access_intrinsic(ojpj__iryd,
            bisi__rkvq)
        expr = expr.replace(tsxvs__whm, adk__cqf)
        jok__xal = f'({na_check_name}.{table_name}.{ecija__vrw})'
        if jok__xal in expr:
            nxwz__trwt = f'nacheck_{table_name}_val_{ebcj__dpute}'
            trwvk__opz = f'_bodo_isna_{table_name}_val_{ebcj__dpute}'
            if isinstance(ojpj__iryd, (bodo.libs.int_arr_ext.
                IntegerArrayType, bodo.FloatingArrayType, bodo.TimeArrayType)
                ) or ojpj__iryd in (bodo.libs.bool_arr_ext.boolean_array,
                bodo.binary_array_type, bodo.datetime_date_array_type
                ) or is_str_arr_type(ojpj__iryd):
                func_text += f"""  {trwvk__opz} = {nxwz__trwt}({table_name}_null_bitmap, {table_name}_ind)
"""
            else:
                func_text += f"""  {trwvk__opz} = {nxwz__trwt}({table_name}_data1, {table_name}_ind)
"""
            table_getitem_funcs[nxwz__trwt
                ] = bodo.libs.array._gen_row_na_check_intrinsic(ojpj__iryd,
                bisi__rkvq)
            expr = expr.replace(jok__xal, trwvk__opz)
        if ebcj__dpute not in key_set:
            tdgbn__dzlvx.append(bisi__rkvq)
    return expr, func_text, tdgbn__dzlvx


def _match_join_key_types(t1, t2, loc):
    if t1 == t2:
        return t1
    if is_str_arr_type(t1) and is_str_arr_type(t2):
        return bodo.string_array_type
    try:
        arr = dtype_to_array_type(find_common_np_dtype([t1, t2]))
        return to_nullable_type(arr) if is_nullable_type(t1
            ) or is_nullable_type(t2) else arr
    except Exception as cnpdt__dcnd:
        raise BodoError(f'Join key types {t1} and {t2} do not match', loc=loc)


def _get_table_parallel_flags(join_node, array_dists):
    vrm__ovumq = (distributed_pass.Distribution.OneD, distributed_pass.
        Distribution.OneD_Var)
    left_parallel = all(array_dists[zzjs__arcaj.name] in vrm__ovumq for
        zzjs__arcaj in join_node.get_live_left_vars())
    if not join_node.get_live_left_vars():
        assert join_node.how == 'cross', 'cross join expected if left data is dead'
        left_parallel = join_node.left_dist in vrm__ovumq
    right_parallel = all(array_dists[zzjs__arcaj.name] in vrm__ovumq for
        zzjs__arcaj in join_node.get_live_right_vars())
    if not join_node.get_live_right_vars():
        assert join_node.how == 'cross', 'cross join expected if right data is dead'
        right_parallel = join_node.right_dist in vrm__ovumq
    if not left_parallel:
        assert not any(array_dists[zzjs__arcaj.name] in vrm__ovumq for
            zzjs__arcaj in join_node.get_live_left_vars())
    if not right_parallel:
        assert not any(array_dists[zzjs__arcaj.name] in vrm__ovumq for
            zzjs__arcaj in join_node.get_live_right_vars())
    if left_parallel or right_parallel:
        assert all(array_dists[zzjs__arcaj.name] in vrm__ovumq for
            zzjs__arcaj in join_node.get_live_out_vars())
    return left_parallel, right_parallel


def _gen_join_cpp_call(join_node, left_key_types, right_key_types,
    matched_key_types, left_other_names, right_other_names,
    left_other_types, right_other_types, left_key_in_output,
    right_key_in_output, left_parallel, right_parallel, glbs,
    out_physical_to_logical_list, out_table_type, index_col_type,
    out_table_used_cols, left_used_key_nums, right_used_key_nums,
    general_cond_cfunc, left_col_nums, right_col_nums,
    left_physical_to_logical_list, right_physical_to_logical_list):

    def needs_typechange(in_type, need_nullable, is_same_key):
        return isinstance(in_type, types.Array) and not is_dtype_nullable(
            in_type.dtype) and need_nullable and not is_same_key
    ospv__tnqg = set(left_col_nums)
    aohj__iqo = set(right_col_nums)
    hjd__xcth = join_node.vect_same_key
    nhey__jufi = []
    for gjiam__ljyt in range(len(left_key_types)):
        if left_key_in_output[gjiam__ljyt]:
            nhey__jufi.append(needs_typechange(matched_key_types[
                gjiam__ljyt], join_node.is_right, hjd__xcth[gjiam__ljyt]))
    ypf__hzw = len(left_key_types)
    att__kcdbn = 0
    umka__wfzy = left_physical_to_logical_list[len(left_key_types):]
    for gjiam__ljyt, xzu__lmu in enumerate(umka__wfzy):
        qzzl__ohcyg = True
        if xzu__lmu in ospv__tnqg:
            qzzl__ohcyg = left_key_in_output[ypf__hzw]
            ypf__hzw += 1
        if qzzl__ohcyg:
            nhey__jufi.append(needs_typechange(left_other_types[gjiam__ljyt
                ], join_node.is_right, False))
    for gjiam__ljyt in range(len(right_key_types)):
        if not hjd__xcth[gjiam__ljyt] and not join_node.is_join:
            if right_key_in_output[att__kcdbn]:
                nhey__jufi.append(needs_typechange(matched_key_types[
                    gjiam__ljyt], join_node.is_left, False))
            att__kcdbn += 1
    scnf__qyc = right_physical_to_logical_list[len(right_key_types):]
    for gjiam__ljyt, xzu__lmu in enumerate(scnf__qyc):
        qzzl__ohcyg = True
        if xzu__lmu in aohj__iqo:
            qzzl__ohcyg = right_key_in_output[att__kcdbn]
            att__kcdbn += 1
        if qzzl__ohcyg:
            nhey__jufi.append(needs_typechange(right_other_types[
                gjiam__ljyt], join_node.is_left, False))
    tren__qnj = len(left_key_types)
    func_text = '    # beginning of _gen_join_cpp_call\n'
    if join_node.is_left_table:
        if join_node.has_live_left_table_var:
            fdt__pthxe = left_other_names[1:]
            ihvjp__oml = left_other_names[0]
        else:
            fdt__pthxe = left_other_names
            ihvjp__oml = None
        qub__mahpe = '()' if len(fdt__pthxe) == 0 else f'({fdt__pthxe[0]},)'
        func_text += f"""    table_left = py_data_to_cpp_table({ihvjp__oml}, {qub__mahpe}, left_in_cols, {join_node.n_left_table_cols})
"""
        glbs['left_in_cols'] = MetaType(tuple(left_physical_to_logical_list))
    else:
        sdzqk__ebzf = []
        for gjiam__ljyt in range(tren__qnj):
            sdzqk__ebzf.append('t1_keys[{}]'.format(gjiam__ljyt))
        for gjiam__ljyt in range(len(left_other_names)):
            sdzqk__ebzf.append('data_left[{}]'.format(gjiam__ljyt))
        func_text += '    info_list_total_l = [{}]\n'.format(','.join(
            'array_to_info({})'.format(smcd__kuxaq) for smcd__kuxaq in
            sdzqk__ebzf))
        func_text += (
            '    table_left = arr_info_list_to_table(info_list_total_l)\n')
    if join_node.is_right_table:
        if join_node.has_live_right_table_var:
            scs__zqgll = right_other_names[1:]
            ihvjp__oml = right_other_names[0]
        else:
            scs__zqgll = right_other_names
            ihvjp__oml = None
        qub__mahpe = '()' if len(scs__zqgll) == 0 else f'({scs__zqgll[0]},)'
        func_text += f"""    table_right = py_data_to_cpp_table({ihvjp__oml}, {qub__mahpe}, right_in_cols, {join_node.n_right_table_cols})
"""
        glbs['right_in_cols'] = MetaType(tuple(right_physical_to_logical_list))
    else:
        orpvc__exlzt = []
        for gjiam__ljyt in range(tren__qnj):
            orpvc__exlzt.append('t2_keys[{}]'.format(gjiam__ljyt))
        for gjiam__ljyt in range(len(right_other_names)):
            orpvc__exlzt.append('data_right[{}]'.format(gjiam__ljyt))
        func_text += '    info_list_total_r = [{}]\n'.format(','.join(
            'array_to_info({})'.format(smcd__kuxaq) for smcd__kuxaq in
            orpvc__exlzt))
        func_text += (
            '    table_right = arr_info_list_to_table(info_list_total_r)\n')
    glbs['vect_same_key'] = np.array(hjd__xcth, dtype=np.int64)
    glbs['use_nullable_arr_type'] = np.array(nhey__jufi, dtype=np.int64)
    glbs['left_table_cond_columns'] = np.array(left_col_nums if len(
        left_col_nums) > 0 else [-1], dtype=np.int64)
    glbs['right_table_cond_columns'] = np.array(right_col_nums if len(
        right_col_nums) > 0 else [-1], dtype=np.int64)
    if general_cond_cfunc:
        func_text += f"""    cfunc_cond = add_join_gen_cond_cfunc_sym(general_cond_cfunc, '{general_cond_cfunc.native_name}')
"""
        func_text += (
            f"    cfunc_cond = get_join_cond_addr('{general_cond_cfunc.native_name}')\n"
            )
    else:
        func_text += '    cfunc_cond = 0\n'
    func_text += f'    total_rows_np = np.array([0], dtype=np.int64)\n'
    if join_node.how == 'cross' or not join_node.left_keys:
        func_text += f"""    out_table = cross_join_table(table_left, table_right, {left_parallel}, {right_parallel}, {join_node.is_left}, {join_node.is_right}, key_in_output.ctypes, use_nullable_arr_type.ctypes, cfunc_cond, left_table_cond_columns.ctypes, {len(left_col_nums)}, right_table_cond_columns.ctypes, {len(right_col_nums)}, total_rows_np.ctypes)
"""
    else:
        func_text += f"""    out_table = hash_join_table(table_left, table_right, {left_parallel}, {right_parallel}, {tren__qnj}, {len(umka__wfzy)}, {len(scnf__qyc)}, vect_same_key.ctypes, key_in_output.ctypes, use_nullable_arr_type.ctypes, {join_node.is_left}, {join_node.is_right}, {join_node.is_join}, {join_node.extra_data_col_num != -1}, {join_node.indicator_col_num != -1}, {join_node.is_na_equal}, cfunc_cond, left_table_cond_columns.ctypes, {len(left_col_nums)}, right_table_cond_columns.ctypes, {len(right_col_nums)}, total_rows_np.ctypes)
"""
    func_text += '    delete_table(table_left)\n'
    func_text += '    delete_table(table_right)\n'
    okwdn__djq = '(py_table_type, index_col_type)'
    func_text += f"""    out_data = cpp_table_to_py_data(out_table, out_col_inds, {okwdn__djq}, total_rows_np[0], {join_node.n_out_table_cols})
"""
    if join_node.has_live_out_table_var:
        func_text += f'    T = out_data[0]\n'
    else:
        func_text += f'    T = None\n'
    if join_node.has_live_out_index_var:
        zehvl__qua = 1 if join_node.has_live_out_table_var else 0
        func_text += f'    index_var = out_data[{zehvl__qua}]\n'
    else:
        func_text += f'    index_var = None\n'
    glbs['py_table_type'] = out_table_type
    glbs['index_col_type'] = index_col_type
    glbs['out_col_inds'] = MetaType(tuple(out_physical_to_logical_list))
    if bool(join_node.out_used_cols) or index_col_type != types.none:
        func_text += '    delete_table(out_table)\n'
    if out_table_type != types.none:
        cinym__aqp = {}
        for gjiam__ljyt, qcgh__oorlo in enumerate(join_node.left_keys):
            if gjiam__ljyt in left_used_key_nums:
                fup__ohais = join_node.left_var_map[qcgh__oorlo]
                cinym__aqp[gjiam__ljyt] = join_node.left_to_output_map[
                    fup__ohais]
        jie__ybv = determine_table_cast_map(matched_key_types,
            left_key_types, left_used_key_nums, cinym__aqp, False)
        xskoz__gmm = {}
        for gjiam__ljyt, qcgh__oorlo in enumerate(join_node.right_keys):
            if gjiam__ljyt in right_used_key_nums:
                fup__ohais = join_node.right_var_map[qcgh__oorlo]
                xskoz__gmm[gjiam__ljyt] = join_node.right_to_output_map[
                    fup__ohais]
        jie__ybv.update(determine_table_cast_map(matched_key_types,
            right_key_types, right_used_key_nums, xskoz__gmm, False))
        mra__wsr = False
        cntw__ccav = False
        if join_node.has_live_out_table_var:
            ojdvx__bquw = list(out_table_type.arr_types)
        else:
            ojdvx__bquw = None
        for giana__cgqk, tbtn__yeg in jie__ybv.items():
            if giana__cgqk < join_node.n_out_table_cols:
                assert join_node.has_live_out_table_var, 'Casting columns for a dead table should not occur'
                ojdvx__bquw[giana__cgqk] = tbtn__yeg
                mra__wsr = True
            else:
                lkmc__rdmta = tbtn__yeg
                cntw__ccav = True
        if mra__wsr:
            func_text += f"""    T = bodo.utils.table_utils.table_astype(T, cast_table_type, False, _bodo_nan_to_str=False, used_cols=used_cols)
"""
            jnr__kww = bodo.TableType(tuple(ojdvx__bquw))
            glbs['py_table_type'] = jnr__kww
            glbs['cast_table_type'] = out_table_type
            glbs['used_cols'] = MetaType(tuple(out_table_used_cols))
        if cntw__ccav:
            glbs['index_col_type'] = lkmc__rdmta
            glbs['index_cast_type'] = index_col_type
            func_text += (
                f'    index_var = bodo.utils.utils.astype(index_var, index_cast_type)\n'
                )
    func_text += f'    out_table = T\n'
    func_text += f'    out_index = index_var\n'
    return func_text


def determine_table_cast_map(matched_key_types: List[types.Type], key_types:
    List[types.Type], used_key_nums: Optional[Set[int]], output_map: Dict[
    int, int], convert_dict_col: bool):
    jie__ybv: Dict[int, types.Type] = {}
    tren__qnj = len(matched_key_types)
    for gjiam__ljyt in range(tren__qnj):
        if used_key_nums is None or gjiam__ljyt in used_key_nums:
            if matched_key_types[gjiam__ljyt] != key_types[gjiam__ljyt] and (
                convert_dict_col or key_types[gjiam__ljyt] != bodo.
                dict_str_arr_type):
                zehvl__qua = output_map[gjiam__ljyt]
                jie__ybv[zehvl__qua] = matched_key_types[gjiam__ljyt]
    return jie__ybv


@numba.njit
def parallel_asof_comm(left_key_arrs, right_key_arrs, right_data):
    atcns__fidp = bodo.libs.distributed_api.get_size()
    efrgp__mimai = np.empty(atcns__fidp, left_key_arrs[0].dtype)
    dwjcv__ira = np.empty(atcns__fidp, left_key_arrs[0].dtype)
    bodo.libs.distributed_api.allgather(efrgp__mimai, left_key_arrs[0][0])
    bodo.libs.distributed_api.allgather(dwjcv__ira, left_key_arrs[0][-1])
    bujq__kaev = np.zeros(atcns__fidp, np.int32)
    bnyag__bia = np.zeros(atcns__fidp, np.int32)
    ctpdd__oqrui = np.zeros(atcns__fidp, np.int32)
    ahkie__jkp = right_key_arrs[0][0]
    csxq__qlld = right_key_arrs[0][-1]
    lbchy__taxaj = -1
    gjiam__ljyt = 0
    while gjiam__ljyt < atcns__fidp - 1 and dwjcv__ira[gjiam__ljyt
        ] < ahkie__jkp:
        gjiam__ljyt += 1
    while gjiam__ljyt < atcns__fidp and efrgp__mimai[gjiam__ljyt
        ] <= csxq__qlld:
        lbchy__taxaj, smdud__wprjz = _count_overlap(right_key_arrs[0],
            efrgp__mimai[gjiam__ljyt], dwjcv__ira[gjiam__ljyt])
        if lbchy__taxaj != 0:
            lbchy__taxaj -= 1
            smdud__wprjz += 1
        bujq__kaev[gjiam__ljyt] = smdud__wprjz
        bnyag__bia[gjiam__ljyt] = lbchy__taxaj
        gjiam__ljyt += 1
    while gjiam__ljyt < atcns__fidp:
        bujq__kaev[gjiam__ljyt] = 1
        bnyag__bia[gjiam__ljyt] = len(right_key_arrs[0]) - 1
        gjiam__ljyt += 1
    bodo.libs.distributed_api.alltoall(bujq__kaev, ctpdd__oqrui, 1)
    jyh__thd = ctpdd__oqrui.sum()
    tou__zcir = np.empty(jyh__thd, right_key_arrs[0].dtype)
    swt__tisjb = alloc_arr_tup(jyh__thd, right_data)
    ass__eeath = bodo.ir.join.calc_disp(ctpdd__oqrui)
    bodo.libs.distributed_api.alltoallv(right_key_arrs[0], tou__zcir,
        bujq__kaev, ctpdd__oqrui, bnyag__bia, ass__eeath)
    bodo.libs.distributed_api.alltoallv_tup(right_data, swt__tisjb,
        bujq__kaev, ctpdd__oqrui, bnyag__bia, ass__eeath)
    return (tou__zcir,), swt__tisjb


@numba.njit
def _count_overlap(r_key_arr, start, end):
    smdud__wprjz = 0
    lbchy__taxaj = 0
    fpw__dmv = 0
    while fpw__dmv < len(r_key_arr) and r_key_arr[fpw__dmv] < start:
        lbchy__taxaj += 1
        fpw__dmv += 1
    while fpw__dmv < len(r_key_arr) and start <= r_key_arr[fpw__dmv] <= end:
        fpw__dmv += 1
        smdud__wprjz += 1
    return lbchy__taxaj, smdud__wprjz


import llvmlite.binding as ll
from bodo.libs import hdist
ll.add_symbol('c_alltoallv', hdist.c_alltoallv)


@numba.njit
def calc_disp(arr):
    enkdb__awx = np.empty_like(arr)
    enkdb__awx[0] = 0
    for gjiam__ljyt in range(1, len(arr)):
        enkdb__awx[gjiam__ljyt] = enkdb__awx[gjiam__ljyt - 1] + arr[
            gjiam__ljyt - 1]
    return enkdb__awx


@numba.njit
def local_merge_asof(left_keys, right_keys, data_left, data_right):
    dptgn__aqv = len(left_keys[0])
    hxcv__ihlu = len(right_keys[0])
    tno__plr = alloc_arr_tup(dptgn__aqv, left_keys)
    pefrn__alg = alloc_arr_tup(dptgn__aqv, right_keys)
    pkg__lbq = alloc_arr_tup(dptgn__aqv, data_left)
    ict__vdmv = alloc_arr_tup(dptgn__aqv, data_right)
    bmt__yzc = 0
    nov__mcwnn = 0
    for bmt__yzc in range(dptgn__aqv):
        if nov__mcwnn < 0:
            nov__mcwnn = 0
        while nov__mcwnn < hxcv__ihlu and getitem_arr_tup(right_keys,
            nov__mcwnn) <= getitem_arr_tup(left_keys, bmt__yzc):
            nov__mcwnn += 1
        nov__mcwnn -= 1
        setitem_arr_tup(tno__plr, bmt__yzc, getitem_arr_tup(left_keys,
            bmt__yzc))
        setitem_arr_tup(pkg__lbq, bmt__yzc, getitem_arr_tup(data_left,
            bmt__yzc))
        if nov__mcwnn >= 0:
            setitem_arr_tup(pefrn__alg, bmt__yzc, getitem_arr_tup(
                right_keys, nov__mcwnn))
            setitem_arr_tup(ict__vdmv, bmt__yzc, getitem_arr_tup(data_right,
                nov__mcwnn))
        else:
            bodo.libs.array_kernels.setna_tup(pefrn__alg, bmt__yzc)
            bodo.libs.array_kernels.setna_tup(ict__vdmv, bmt__yzc)
    return tno__plr, pefrn__alg, pkg__lbq, ict__vdmv
