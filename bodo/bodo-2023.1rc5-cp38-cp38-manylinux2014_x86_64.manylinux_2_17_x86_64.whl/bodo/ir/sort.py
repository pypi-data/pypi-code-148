"""IR node for the data sorting"""
from collections import defaultdict
from typing import List, Set, Tuple, Union
import numba
import numpy as np
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, mk_unique_var, replace_arg_nodes, replace_vars_inner, visit_vars_inner
import bodo
from bodo.libs.array import arr_info_list_to_table, array_to_info, cpp_table_to_py_data, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, py_data_to_cpp_table, sort_values_table
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import _compute_table_column_uses, _find_used_columns, ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import MetaType, is_overload_none, type_has_unknown_cats
from bodo.utils.utils import gen_getitem


class Sort(ir.Stmt):

    def __init__(self, df_in: str, df_out: str, in_vars: List[ir.Var],
        out_vars: List[ir.Var], key_inds: Tuple[int], inplace: bool, loc:
        ir.Loc, ascending_list: Union[List[bool], bool]=True, na_position:
        Union[List[str], str]='last', _bodo_chunk_bounds: Union[ir.Var,
        None]=None, is_table_format: bool=False, num_table_arrays: int=0):
        self.df_in = df_in
        self.df_out = df_out
        self.in_vars = in_vars
        self.out_vars = out_vars
        self.key_inds = key_inds
        self.inplace = inplace
        self._bodo_chunk_bounds = _bodo_chunk_bounds
        self.is_table_format = is_table_format
        self.num_table_arrays = num_table_arrays
        self.dead_var_inds: Set[int] = set()
        self.dead_key_var_inds: Set[int] = set()
        if isinstance(na_position, str):
            if na_position == 'last':
                self.na_position_b = (True,) * len(key_inds)
            else:
                self.na_position_b = (False,) * len(key_inds)
        else:
            self.na_position_b = tuple([(True if ssnp__cggj == 'last' else 
                False) for ssnp__cggj in na_position])
        if isinstance(ascending_list, bool):
            ascending_list = (ascending_list,) * len(key_inds)
        self.ascending_list = ascending_list
        self.loc = loc

    def get_live_in_vars(self):
        return [wpvi__htpw for wpvi__htpw in self.in_vars if wpvi__htpw is not
            None]

    def get_live_out_vars(self):
        return [wpvi__htpw for wpvi__htpw in self.out_vars if wpvi__htpw is not
            None]

    def __repr__(self):
        mnpz__sszb = ', '.join(wpvi__htpw.name for wpvi__htpw in self.
            get_live_in_vars())
        fzmeb__osrw = f'{self.df_in}{{{mnpz__sszb}}}'
        fai__eum = ', '.join(wpvi__htpw.name for wpvi__htpw in self.
            get_live_out_vars())
        tpy__lrdt = f'{self.df_out}{{{fai__eum}}}'
        return f'Sort (keys: {self.key_inds}): {fzmeb__osrw} {tpy__lrdt}'


def sort_array_analysis(sort_node, equiv_set, typemap, array_analysis):
    vlph__rdc = []
    for gaw__ddli in sort_node.get_live_in_vars():
        zzhxk__elchm = equiv_set.get_shape(gaw__ddli)
        if zzhxk__elchm is not None:
            vlph__rdc.append(zzhxk__elchm[0])
    if len(vlph__rdc) > 1:
        equiv_set.insert_equiv(*vlph__rdc)
    usiq__clsy = []
    vlph__rdc = []
    for gaw__ddli in sort_node.get_live_out_vars():
        ymtjc__ggn = typemap[gaw__ddli.name]
        tpyq__xtxat = array_analysis._gen_shape_call(equiv_set, gaw__ddli,
            ymtjc__ggn.ndim, None, usiq__clsy)
        equiv_set.insert_equiv(gaw__ddli, tpyq__xtxat)
        vlph__rdc.append(tpyq__xtxat[0])
        equiv_set.define(gaw__ddli, set())
    if len(vlph__rdc) > 1:
        equiv_set.insert_equiv(*vlph__rdc)
    return [], usiq__clsy


numba.parfors.array_analysis.array_analysis_extensions[Sort
    ] = sort_array_analysis


def sort_distributed_analysis(sort_node, array_dists):
    ajnog__elrrz = sort_node.get_live_in_vars()
    ougbu__oix = sort_node.get_live_out_vars()
    rlp__adyfb = Distribution.OneD
    for gaw__ddli in ajnog__elrrz:
        rlp__adyfb = Distribution(min(rlp__adyfb.value, array_dists[
            gaw__ddli.name].value))
    bfkq__hdk = Distribution(min(rlp__adyfb.value, Distribution.OneD_Var.value)
        )
    for gaw__ddli in ougbu__oix:
        if gaw__ddli.name in array_dists:
            bfkq__hdk = Distribution(min(bfkq__hdk.value, array_dists[
                gaw__ddli.name].value))
    if bfkq__hdk != Distribution.OneD_Var:
        rlp__adyfb = bfkq__hdk
    for gaw__ddli in ajnog__elrrz:
        array_dists[gaw__ddli.name] = rlp__adyfb
    for gaw__ddli in ougbu__oix:
        array_dists[gaw__ddli.name] = bfkq__hdk


distributed_analysis.distributed_analysis_extensions[Sort
    ] = sort_distributed_analysis


def sort_typeinfer(sort_node, typeinferer):
    for nav__kswu, blcmx__pkwe in enumerate(sort_node.out_vars):
        osg__dvo = sort_node.in_vars[nav__kswu]
        if osg__dvo is not None and blcmx__pkwe is not None:
            typeinferer.constraints.append(typeinfer.Propagate(dst=
                blcmx__pkwe.name, src=osg__dvo.name, loc=sort_node.loc))


typeinfer.typeinfer_extensions[Sort] = sort_typeinfer


def build_sort_definitions(sort_node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    if not sort_node.inplace:
        for gaw__ddli in sort_node.get_live_out_vars():
            definitions[gaw__ddli.name].append(sort_node)
    return definitions


ir_utils.build_defs_extensions[Sort] = build_sort_definitions


def visit_vars_sort(sort_node, callback, cbdata):
    for nav__kswu in range(len(sort_node.in_vars)):
        if sort_node.in_vars[nav__kswu] is not None:
            sort_node.in_vars[nav__kswu] = visit_vars_inner(sort_node.
                in_vars[nav__kswu], callback, cbdata)
        if sort_node.out_vars[nav__kswu] is not None:
            sort_node.out_vars[nav__kswu] = visit_vars_inner(sort_node.
                out_vars[nav__kswu], callback, cbdata)
    if sort_node._bodo_chunk_bounds is not None:
        sort_node._bodo_chunk_bounds = visit_vars_inner(sort_node.
            _bodo_chunk_bounds, callback, cbdata)


ir_utils.visit_vars_extensions[Sort] = visit_vars_sort


def remove_dead_sort(sort_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if sort_node.is_table_format:
        rvyc__wosaq = sort_node.out_vars[0]
        if rvyc__wosaq is not None and rvyc__wosaq.name not in lives:
            sort_node.out_vars[0] = None
            dead_cols = set(range(sort_node.num_table_arrays))
            hcpxm__owyg = set(sort_node.key_inds)
            sort_node.dead_key_var_inds.update(dead_cols & hcpxm__owyg)
            sort_node.dead_var_inds.update(dead_cols - hcpxm__owyg)
            if len(hcpxm__owyg & dead_cols) == 0:
                sort_node.in_vars[0] = None
        for nav__kswu in range(1, len(sort_node.out_vars)):
            wpvi__htpw = sort_node.out_vars[nav__kswu]
            if wpvi__htpw is not None and wpvi__htpw.name not in lives:
                sort_node.out_vars[nav__kswu] = None
                ehvmi__stzpm = sort_node.num_table_arrays + nav__kswu - 1
                if ehvmi__stzpm in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(ehvmi__stzpm)
                else:
                    sort_node.dead_var_inds.add(ehvmi__stzpm)
                    sort_node.in_vars[nav__kswu] = None
    else:
        for nav__kswu in range(len(sort_node.out_vars)):
            wpvi__htpw = sort_node.out_vars[nav__kswu]
            if wpvi__htpw is not None and wpvi__htpw.name not in lives:
                sort_node.out_vars[nav__kswu] = None
                if nav__kswu in sort_node.key_inds:
                    sort_node.dead_key_var_inds.add(nav__kswu)
                else:
                    sort_node.dead_var_inds.add(nav__kswu)
                    sort_node.in_vars[nav__kswu] = None
    if all(wpvi__htpw is None for wpvi__htpw in sort_node.out_vars):
        return None
    return sort_node


ir_utils.remove_dead_extensions[Sort] = remove_dead_sort


def sort_usedefs(sort_node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    use_set.update({wpvi__htpw.name for wpvi__htpw in sort_node.
        get_live_in_vars()})
    if not sort_node.inplace:
        def_set.update({wpvi__htpw.name for wpvi__htpw in sort_node.
            get_live_out_vars()})
    if sort_node._bodo_chunk_bounds is not None:
        use_set.add(sort_node._bodo_chunk_bounds.name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


numba.core.analysis.ir_extension_usedefs[Sort] = sort_usedefs


def get_copies_sort(sort_node, typemap):
    lpe__lgjlq = set()
    if not sort_node.inplace:
        lpe__lgjlq.update({wpvi__htpw.name for wpvi__htpw in sort_node.
            get_live_out_vars()})
    return set(), lpe__lgjlq


ir_utils.copy_propagate_extensions[Sort] = get_copies_sort


def apply_copies_sort(sort_node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    for nav__kswu in range(len(sort_node.in_vars)):
        if sort_node.in_vars[nav__kswu] is not None:
            sort_node.in_vars[nav__kswu] = replace_vars_inner(sort_node.
                in_vars[nav__kswu], var_dict)
        if sort_node.out_vars[nav__kswu] is not None:
            sort_node.out_vars[nav__kswu] = replace_vars_inner(sort_node.
                out_vars[nav__kswu], var_dict)
    if sort_node._bodo_chunk_bounds is not None:
        sort_node._bodo_chunk_bounds = replace_vars_inner(sort_node.
            _bodo_chunk_bounds, var_dict)


ir_utils.apply_copy_propagate_extensions[Sort] = apply_copies_sort


def sort_distributed_run(sort_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    parallel = False
    in_vars = sort_node.get_live_in_vars()
    out_vars = sort_node.get_live_out_vars()
    if array_dists is not None:
        parallel = True
        for wpvi__htpw in (in_vars + out_vars):
            if array_dists[wpvi__htpw.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                wpvi__htpw.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    nodes = []
    if not sort_node.inplace:
        wypb__lgbr = []
        for wpvi__htpw in in_vars:
            twd__mkcay = _copy_array_nodes(wpvi__htpw, nodes, typingctx,
                targetctx, typemap, calltypes, sort_node.dead_var_inds)
            wypb__lgbr.append(twd__mkcay)
        in_vars = wypb__lgbr
    out_types = [(typemap[wpvi__htpw.name] if wpvi__htpw is not None else
        types.none) for wpvi__htpw in sort_node.out_vars]
    fvkhm__lqcfb, cvema__aav = get_sort_cpp_section(sort_node, out_types,
        typemap, parallel)
    pyb__ohn = {}
    exec(fvkhm__lqcfb, {}, pyb__ohn)
    gwuxh__fju = pyb__ohn['f']
    cvema__aav.update({'bodo': bodo, 'np': np, 'delete_table': delete_table,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'info_to_array': info_to_array, 'info_from_table': info_from_table,
        'sort_values_table': sort_values_table, 'arr_info_list_to_table':
        arr_info_list_to_table, 'array_to_info': array_to_info,
        'py_data_to_cpp_table': py_data_to_cpp_table,
        'cpp_table_to_py_data': cpp_table_to_py_data})
    cvema__aav.update({f'out_type{nav__kswu}': out_types[nav__kswu] for
        nav__kswu in range(len(out_types))})
    bwo__wgm = sort_node._bodo_chunk_bounds
    blu__frf = bwo__wgm
    if bwo__wgm is None:
        loc = sort_node.loc
        blu__frf = ir.Var(ir.Scope(None, loc), mk_unique_var('$bounds_none'
            ), loc)
        typemap[blu__frf.name] = types.none
        nodes.append(ir.Assign(ir.Const(None, loc), blu__frf, loc))
    llgap__irrl = compile_to_numba_ir(gwuxh__fju, cvema__aav, typingctx=
        typingctx, targetctx=targetctx, arg_typs=tuple(typemap[wpvi__htpw.
        name] for wpvi__htpw in in_vars) + (typemap[blu__frf.name],),
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(llgap__irrl, in_vars + [blu__frf])
    sarys__mtpz = llgap__irrl.body[-2].value.value
    nodes += llgap__irrl.body[:-2]
    for nav__kswu, wpvi__htpw in enumerate(out_vars):
        gen_getitem(wpvi__htpw, sarys__mtpz, nav__kswu, calltypes, nodes)
    return nodes


distributed_pass.distributed_run_extensions[Sort] = sort_distributed_run


def _copy_array_nodes(var, nodes, typingctx, targetctx, typemap, calltypes,
    dead_cols):
    from bodo.hiframes.table import TableType
    gjk__vjcri = lambda arr: arr.copy()
    nsitn__bgv = None
    if isinstance(typemap[var.name], TableType):
        atp__tqgul = len(typemap[var.name].arr_types)
        nsitn__bgv = set(range(atp__tqgul)) - dead_cols
        nsitn__bgv = MetaType(tuple(sorted(nsitn__bgv)))
        gjk__vjcri = (lambda T: bodo.utils.table_utils.
            generate_mappable_table_func(T, 'copy', types.none, True,
            used_cols=_used_columns))
    llgap__irrl = compile_to_numba_ir(gjk__vjcri, {'bodo': bodo, 'types':
        types, '_used_columns': nsitn__bgv}, typingctx=typingctx, targetctx
        =targetctx, arg_typs=(typemap[var.name],), typemap=typemap,
        calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(llgap__irrl, [var])
    nodes += llgap__irrl.body[:-2]
    return nodes[-1].target


def get_sort_cpp_section(sort_node, out_types, typemap, parallel):
    syakh__hqv = len(sort_node.key_inds)
    jpn__qkpd = len(sort_node.in_vars)
    mven__eqtl = len(sort_node.out_vars)
    n_cols = (sort_node.num_table_arrays + jpn__qkpd - 1 if sort_node.
        is_table_format else jpn__qkpd)
    kao__kjzyu, kwts__rsu, ncc__kqi = _get_cpp_col_ind_mappings(sort_node.
        key_inds, sort_node.dead_var_inds, sort_node.dead_key_var_inds, n_cols)
    qes__ndvr = []
    if sort_node.is_table_format:
        qes__ndvr.append('arg0')
        for nav__kswu in range(1, jpn__qkpd):
            ehvmi__stzpm = sort_node.num_table_arrays + nav__kswu - 1
            if ehvmi__stzpm not in sort_node.dead_var_inds:
                qes__ndvr.append(f'arg{ehvmi__stzpm}')
    else:
        for nav__kswu in range(n_cols):
            if nav__kswu not in sort_node.dead_var_inds:
                qes__ndvr.append(f'arg{nav__kswu}')
    fvkhm__lqcfb = f"def f({', '.join(qes__ndvr)}, bounds_in):\n"
    if sort_node.is_table_format:
        sxsua__cszp = ',' if jpn__qkpd - 1 == 1 else ''
        jcju__yezb = []
        for nav__kswu in range(sort_node.num_table_arrays, n_cols):
            if nav__kswu in sort_node.dead_var_inds:
                jcju__yezb.append('None')
            else:
                jcju__yezb.append(f'arg{nav__kswu}')
        fvkhm__lqcfb += f"""  in_cpp_table = py_data_to_cpp_table(arg0, ({', '.join(jcju__yezb)}{sxsua__cszp}), in_col_inds, {sort_node.num_table_arrays})
"""
    else:
        zcp__wzbif = {sflb__eezx: nav__kswu for nav__kswu, sflb__eezx in
            enumerate(kao__kjzyu)}
        onl__uhw = [None] * len(kao__kjzyu)
        for nav__kswu in range(n_cols):
            osaf__zfur = zcp__wzbif.get(nav__kswu, -1)
            if osaf__zfur != -1:
                onl__uhw[osaf__zfur] = f'array_to_info(arg{nav__kswu})'
        fvkhm__lqcfb += '  info_list_total = [{}]\n'.format(','.join(onl__uhw))
        fvkhm__lqcfb += (
            '  in_cpp_table = arr_info_list_to_table(info_list_total)\n')
    fvkhm__lqcfb += '  vect_ascending = np.array([{}], np.int64)\n'.format(','
        .join('1' if tgdgf__yvpe else '0' for tgdgf__yvpe in sort_node.
        ascending_list))
    fvkhm__lqcfb += '  na_position = np.array([{}], np.int64)\n'.format(','
        .join('1' if tgdgf__yvpe else '0' for tgdgf__yvpe in sort_node.
        na_position_b))
    fvkhm__lqcfb += '  dead_keys = np.array([{}], np.int64)\n'.format(','.
        join('1' if nav__kswu in ncc__kqi else '0' for nav__kswu in range(
        syakh__hqv)))
    fvkhm__lqcfb += f'  total_rows_np = np.array([0], dtype=np.int64)\n'
    rkr__djcro = sort_node._bodo_chunk_bounds
    hgbvp__sdy = '0' if rkr__djcro is None or is_overload_none(typemap[
        rkr__djcro.name]
        ) else 'arr_info_list_to_table([array_to_info(bounds_in)])'
    fvkhm__lqcfb += f"""  out_cpp_table = sort_values_table(in_cpp_table, {syakh__hqv}, vect_ascending.ctypes, na_position.ctypes, dead_keys.ctypes, total_rows_np.ctypes, {hgbvp__sdy}, {parallel})
"""
    if sort_node.is_table_format:
        sxsua__cszp = ',' if mven__eqtl == 1 else ''
        ydgc__yycd = (
            f"({', '.join(f'out_type{nav__kswu}' if not type_has_unknown_cats(out_types[nav__kswu]) else f'arg{nav__kswu}' for nav__kswu in range(mven__eqtl))}{sxsua__cszp})"
            )
        fvkhm__lqcfb += f"""  out_data = cpp_table_to_py_data(out_cpp_table, out_col_inds, {ydgc__yycd}, total_rows_np[0], {sort_node.num_table_arrays})
"""
    else:
        zcp__wzbif = {sflb__eezx: nav__kswu for nav__kswu, sflb__eezx in
            enumerate(kwts__rsu)}
        onl__uhw = []
        for nav__kswu in range(n_cols):
            osaf__zfur = zcp__wzbif.get(nav__kswu, -1)
            if osaf__zfur != -1:
                gitsv__xip = (f'out_type{nav__kswu}' if not
                    type_has_unknown_cats(out_types[nav__kswu]) else
                    f'arg{nav__kswu}')
                fvkhm__lqcfb += f"""  out{nav__kswu} = info_to_array(info_from_table(out_cpp_table, {osaf__zfur}), {gitsv__xip})
"""
                onl__uhw.append(f'out{nav__kswu}')
        sxsua__cszp = ',' if len(onl__uhw) == 1 else ''
        ahbfq__ndxd = f"({', '.join(onl__uhw)}{sxsua__cszp})"
        fvkhm__lqcfb += f'  out_data = {ahbfq__ndxd}\n'
    fvkhm__lqcfb += '  delete_table(out_cpp_table)\n'
    fvkhm__lqcfb += '  delete_table(in_cpp_table)\n'
    fvkhm__lqcfb += f'  return out_data\n'
    return fvkhm__lqcfb, {'in_col_inds': MetaType(tuple(kao__kjzyu)),
        'out_col_inds': MetaType(tuple(kwts__rsu))}


def _get_cpp_col_ind_mappings(key_inds, dead_var_inds, dead_key_var_inds,
    n_cols):
    kao__kjzyu = []
    kwts__rsu = []
    ncc__kqi = []
    for sflb__eezx, nav__kswu in enumerate(key_inds):
        kao__kjzyu.append(nav__kswu)
        if nav__kswu in dead_key_var_inds:
            ncc__kqi.append(sflb__eezx)
        else:
            kwts__rsu.append(nav__kswu)
    for nav__kswu in range(n_cols):
        if nav__kswu in dead_var_inds or nav__kswu in key_inds:
            continue
        kao__kjzyu.append(nav__kswu)
        kwts__rsu.append(nav__kswu)
    return kao__kjzyu, kwts__rsu, ncc__kqi


def sort_table_column_use(sort_node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    if not sort_node.is_table_format or sort_node.in_vars[0
        ] is None or sort_node.out_vars[0] is None:
        return
    abjp__dkmk = sort_node.in_vars[0].name
    zvktj__cyec = sort_node.out_vars[0].name
    brm__vmyp, zqmr__yok, famt__qsvo = block_use_map[abjp__dkmk]
    if zqmr__yok or famt__qsvo:
        return
    uscz__yli, chfu__poa, clnba__pklhw = _compute_table_column_uses(zvktj__cyec
        , table_col_use_map, equiv_vars)
    qxtyx__kux = set(nav__kswu for nav__kswu in sort_node.key_inds if 
        nav__kswu < sort_node.num_table_arrays)
    block_use_map[abjp__dkmk
        ] = brm__vmyp | uscz__yli | qxtyx__kux, chfu__poa or clnba__pklhw, False


ir_extension_table_column_use[Sort] = sort_table_column_use


def sort_remove_dead_column(sort_node, column_live_map, equiv_vars, typemap):
    if not sort_node.is_table_format or sort_node.out_vars[0] is None:
        return False
    atp__tqgul = sort_node.num_table_arrays
    zvktj__cyec = sort_node.out_vars[0].name
    nsitn__bgv = _find_used_columns(zvktj__cyec, atp__tqgul,
        column_live_map, equiv_vars)
    if nsitn__bgv is None:
        return False
    cutz__bounh = set(range(atp__tqgul)) - nsitn__bgv
    qxtyx__kux = set(nav__kswu for nav__kswu in sort_node.key_inds if 
        nav__kswu < atp__tqgul)
    vab__mozss = sort_node.dead_key_var_inds | cutz__bounh & qxtyx__kux
    ygrkv__tnn = sort_node.dead_var_inds | cutz__bounh - qxtyx__kux
    nawt__ken = (vab__mozss != sort_node.dead_key_var_inds) | (ygrkv__tnn !=
        sort_node.dead_var_inds)
    sort_node.dead_key_var_inds = vab__mozss
    sort_node.dead_var_inds = ygrkv__tnn
    return nawt__ken


remove_dead_column_extensions[Sort] = sort_remove_dead_column
