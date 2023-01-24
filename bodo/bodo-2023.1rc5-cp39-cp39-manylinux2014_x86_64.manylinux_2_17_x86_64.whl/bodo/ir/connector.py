"""
Common IR extension functions for connectors such as CSV, Parquet and JSON readers.
"""
import sys
from collections import defaultdict
from typing import Literal, Set, Tuple
import numba
from numba.core import ir, types
from numba.core.ir_utils import replace_vars_inner, visit_vars_inner
from bodo.hiframes.table import TableType
from bodo.transforms.distributed_analysis import Distribution
from bodo.transforms.table_column_del_pass import get_live_column_nums_block
from bodo.utils.py_objs import install_py_obj_class
from bodo.utils.typing import BodoError
from bodo.utils.utils import debug_prints, is_array_typ


def connector_array_analysis(node, equiv_set, typemap, array_analysis):
    btad__sbe = []
    assert len(node.out_vars) > 0, 'empty {} in array analysis'.format(node
        .connector_typ)
    if node.connector_typ == 'csv' and node.chunksize is not None:
        return [], []
    zhqm__meda = []
    for hfzz__iuhr, ltx__nms in enumerate(node.out_vars):
        ijkw__ubn = typemap[ltx__nms.name]
        if ijkw__ubn == types.none:
            continue
        djkq__rif = hfzz__iuhr == 0 and node.connector_typ in ('parquet', 'sql'
            ) and not node.is_live_table
        kiaj__cktuq = node.connector_typ == 'sql' and hfzz__iuhr > 1
        if not (djkq__rif or kiaj__cktuq):
            jylb__ezh = array_analysis._gen_shape_call(equiv_set, ltx__nms,
                ijkw__ubn.ndim, None, btad__sbe)
            equiv_set.insert_equiv(ltx__nms, jylb__ezh)
            zhqm__meda.append(jylb__ezh[0])
            equiv_set.define(ltx__nms, set())
    if len(zhqm__meda) > 1:
        equiv_set.insert_equiv(*zhqm__meda)
    return [], btad__sbe


def connector_distributed_analysis(node, array_dists):
    from bodo.ir.sql_ext import SqlReader
    if isinstance(node, SqlReader) and not node.is_select_query:
        kiaww__him = Distribution.REP
    elif isinstance(node, SqlReader) and node.limit is not None:
        kiaww__him = Distribution.OneD_Var
    else:
        kiaww__him = Distribution.OneD
    for vmbez__ewfk in node.out_vars:
        if vmbez__ewfk.name in array_dists:
            kiaww__him = Distribution(min(kiaww__him.value, array_dists[
                vmbez__ewfk.name].value))
    for vmbez__ewfk in node.out_vars:
        array_dists[vmbez__ewfk.name] = kiaww__him


def connector_typeinfer(node, typeinferer):
    if node.connector_typ == 'csv':
        if node.chunksize is not None:
            typeinferer.lock_type(node.out_vars[0].name, node.out_types[0],
                loc=node.loc)
        else:
            typeinferer.lock_type(node.out_vars[0].name, TableType(tuple(
                node.out_types)), loc=node.loc)
            typeinferer.lock_type(node.out_vars[1].name, node.
                index_column_typ, loc=node.loc)
        return
    if node.connector_typ in ('parquet', 'sql'):
        typeinferer.lock_type(node.out_vars[0].name, TableType(tuple(node.
            out_types)), loc=node.loc)
        typeinferer.lock_type(node.out_vars[1].name, node.index_column_type,
            loc=node.loc)
        if node.connector_typ == 'sql':
            if len(node.out_vars) > 2:
                typeinferer.lock_type(node.out_vars[2].name, node.
                    file_list_type, loc=node.loc)
            if len(node.out_vars) > 3:
                typeinferer.lock_type(node.out_vars[3].name, node.
                    snapshot_id_type, loc=node.loc)
        return
    for ltx__nms, ijkw__ubn in zip(node.out_vars, node.out_types):
        typeinferer.lock_type(ltx__nms.name, ijkw__ubn, loc=node.loc)


def visit_vars_connector(node, callback, cbdata):
    if debug_prints():
        print('visiting {} vars for:'.format(node.connector_typ), node)
        print('cbdata: ', sorted(cbdata.items()))
    keo__kqz = []
    for ltx__nms in node.out_vars:
        sqjwx__wxcsf = visit_vars_inner(ltx__nms, callback, cbdata)
        keo__kqz.append(sqjwx__wxcsf)
    node.out_vars = keo__kqz
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = visit_vars_inner(node.file_name, callback, cbdata)
    if node.connector_typ == 'csv':
        node.nrows = visit_vars_inner(node.nrows, callback, cbdata)
        node.skiprows = visit_vars_inner(node.skiprows, callback, cbdata)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for ggiz__lcd in node.filters:
            for hfzz__iuhr in range(len(ggiz__lcd)):
                bvnzv__ouvt = ggiz__lcd[hfzz__iuhr]
                ggiz__lcd[hfzz__iuhr] = bvnzv__ouvt[0], bvnzv__ouvt[1
                    ], visit_vars_inner(bvnzv__ouvt[2], callback, cbdata)


def connector_usedefs(node, use_set=None, def_set=None):
    if use_set is None:
        use_set = set()
    if def_set is None:
        def_set = set()
    def_set.update({vmbez__ewfk.name for vmbez__ewfk in node.out_vars})
    if node.connector_typ in ('csv', 'parquet', 'json'):
        use_set.add(node.file_name.name)
    if node.connector_typ == 'csv':
        if isinstance(node.nrows, numba.core.ir.Var):
            use_set.add(node.nrows.name)
        if isinstance(node.skiprows, numba.core.ir.Var):
            use_set.add(node.skiprows.name)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for isuz__oeqa in node.filters:
            for vmbez__ewfk in isuz__oeqa:
                if isinstance(vmbez__ewfk[2], ir.Var):
                    use_set.add(vmbez__ewfk[2].name)
    return numba.core.analysis._use_defs_result(usemap=use_set, defmap=def_set)


def get_copies_connector(node, typemap):
    gdjd__xygl = set(vmbez__ewfk.name for vmbez__ewfk in node.out_vars)
    return set(), gdjd__xygl


def apply_copies_connector(node, var_dict, name_var_table, typemap,
    calltypes, save_copies):
    keo__kqz = []
    for ltx__nms in node.out_vars:
        sqjwx__wxcsf = replace_vars_inner(ltx__nms, var_dict)
        keo__kqz.append(sqjwx__wxcsf)
    node.out_vars = keo__kqz
    if node.connector_typ in ('csv', 'parquet', 'json'):
        node.file_name = replace_vars_inner(node.file_name, var_dict)
    if node.connector_typ in ('parquet', 'sql') and node.filters:
        for ggiz__lcd in node.filters:
            for hfzz__iuhr in range(len(ggiz__lcd)):
                bvnzv__ouvt = ggiz__lcd[hfzz__iuhr]
                ggiz__lcd[hfzz__iuhr] = bvnzv__ouvt[0], bvnzv__ouvt[1
                    ], replace_vars_inner(bvnzv__ouvt[2], var_dict)
    if node.connector_typ == 'csv':
        node.nrows = replace_vars_inner(node.nrows, var_dict)
        node.skiprows = replace_vars_inner(node.skiprows, var_dict)


def build_connector_definitions(node, definitions=None):
    if definitions is None:
        definitions = defaultdict(list)
    for ltx__nms in node.out_vars:
        hkjts__relnj = definitions[ltx__nms.name]
        if node not in hkjts__relnj:
            hkjts__relnj.append(node)
    return definitions


def generate_filter_map(filters):
    if filters:
        filter_vars = []
        mth__tcwr = [vmbez__ewfk[2] for isuz__oeqa in filters for
            vmbez__ewfk in isuz__oeqa]
        jdc__mroo = set()
        for xbg__vbpu in mth__tcwr:
            if isinstance(xbg__vbpu, ir.Var):
                if xbg__vbpu.name not in jdc__mroo:
                    filter_vars.append(xbg__vbpu)
                jdc__mroo.add(xbg__vbpu.name)
        return {vmbez__ewfk.name: f'f{hfzz__iuhr}' for hfzz__iuhr,
            vmbez__ewfk in enumerate(filter_vars)}, filter_vars
    else:
        return {}, []


this_module = sys.modules[__name__]
StreamReaderType = install_py_obj_class(types_name='stream_reader_type',
    module=this_module, class_name='StreamReaderType', model_name=
    'StreamReaderModel')


def trim_extra_used_columns(used_columns: Set, num_columns: int):
    return {hfzz__iuhr for hfzz__iuhr in used_columns if hfzz__iuhr <
        num_columns}


def cast_float_to_nullable(df, df_type):
    import bodo
    axxgg__hlru = {}
    for hfzz__iuhr, waawo__hve in enumerate(df_type.data):
        if isinstance(waawo__hve, bodo.IntegerArrayType):
            fhy__qgw = waawo__hve.get_pandas_scalar_type_instance
            if fhy__qgw not in axxgg__hlru:
                axxgg__hlru[fhy__qgw] = []
            axxgg__hlru[fhy__qgw].append(df.columns[hfzz__iuhr])
    for ijkw__ubn, hunq__omubg in axxgg__hlru.items():
        df[hunq__omubg] = df[hunq__omubg].astype(ijkw__ubn)


def connector_table_column_use(node, block_use_map, equiv_vars, typemap,
    table_col_use_map):
    return


def base_connector_remove_dead_columns(node, column_live_map, equiv_vars,
    typemap, nodename, possible_cols, require_one_column=True):
    snr__yeg = node.out_vars[0].name
    assert isinstance(typemap[snr__yeg], TableType
        ), f'{nodename} Node Table must be a TableType'
    if possible_cols:
        used_columns, fnlaz__qjze, tdt__nge = get_live_column_nums_block(
            column_live_map, equiv_vars, snr__yeg)
        if not (fnlaz__qjze or tdt__nge):
            used_columns = trim_extra_used_columns(used_columns, len(
                possible_cols))
            if not used_columns and require_one_column:
                used_columns = {0}
            if len(used_columns) != len(node.out_used_cols):
                node.out_used_cols = list(sorted(used_columns))
    """We return flase in all cases, as no changes performed in the file will allow for dead code elimination to do work."""
    return False


def is_connector_table_parallel(node, array_dists, typemap, node_name):
    ata__svg = False
    if array_dists is not None:
        cvskm__gilbt = node.out_vars[0].name
        ata__svg = array_dists[cvskm__gilbt] in (Distribution.OneD,
            Distribution.OneD_Var)
        htvk__ymhyo = node.out_vars[1].name
        assert typemap[htvk__ymhyo
            ] == types.none or not ata__svg or array_dists[htvk__ymhyo] in (
            Distribution.OneD, Distribution.OneD_Var
            ), f'{node_name} data/index parallelization does not match'
    return ata__svg


def generate_arrow_filters(filters, filter_map, filter_vars, col_names,
    partition_names, original_out_types, typemap, source: Literal['parquet',
    'iceberg'], output_dnf=True) ->Tuple[str, str]:
    pou__tcmps = 'None'
    zsdus__byb = 'None'
    if filters:
        hroog__ubbe = []
        hzdhf__rxrq = []
        rhoyc__sevuy = False
        orig_colname_map = {vjzt__fxy: hfzz__iuhr for hfzz__iuhr, vjzt__fxy in
            enumerate(col_names)}
        for ggiz__lcd in filters:
            qbpnw__olf = []
            smzp__duehu = []
            for vmbez__ewfk in ggiz__lcd:
                if isinstance(vmbez__ewfk[2], ir.Var):
                    gsl__qnj, otyi__rlzpc = determine_filter_cast(
                        original_out_types, typemap, vmbez__ewfk,
                        orig_colname_map, partition_names, source)
                    if vmbez__ewfk[1] == 'in':
                        omm__mee = (
                            f"(ds.field('{vmbez__ewfk[0]}').isin({filter_map[vmbez__ewfk[2].name]}))"
                            )
                    else:
                        omm__mee = (
                            f"(ds.field('{vmbez__ewfk[0]}'){gsl__qnj} {vmbez__ewfk[1]} ds.scalar({filter_map[vmbez__ewfk[2].name]}){otyi__rlzpc})"
                            )
                else:
                    assert vmbez__ewfk[2
                        ] == 'NULL', 'unsupport constant used in filter pushdown'
                    if vmbez__ewfk[1] == 'is not':
                        kbpl__eeaao = '~'
                    else:
                        kbpl__eeaao = ''
                    omm__mee = (
                        f"({kbpl__eeaao}ds.field('{vmbez__ewfk[0]}').is_null())"
                        )
                smzp__duehu.append(omm__mee)
                if not rhoyc__sevuy:
                    if vmbez__ewfk[0] in partition_names and isinstance(
                        vmbez__ewfk[2], ir.Var):
                        if output_dnf:
                            fryg__qcj = (
                                f"('{vmbez__ewfk[0]}', '{vmbez__ewfk[1]}', {filter_map[vmbez__ewfk[2].name]})"
                                )
                        else:
                            fryg__qcj = omm__mee
                        qbpnw__olf.append(fryg__qcj)
                    elif vmbez__ewfk[0] in partition_names and not isinstance(
                        vmbez__ewfk[2], ir.Var) and source == 'iceberg':
                        if output_dnf:
                            fryg__qcj = (
                                f"('{vmbez__ewfk[0]}', '{vmbez__ewfk[1]}', '{vmbez__ewfk[2]}')"
                                )
                        else:
                            fryg__qcj = omm__mee
                        qbpnw__olf.append(fryg__qcj)
            yab__dvjpa = ''
            if qbpnw__olf:
                if output_dnf:
                    yab__dvjpa = ', '.join(qbpnw__olf)
                else:
                    yab__dvjpa = ' & '.join(qbpnw__olf)
            else:
                rhoyc__sevuy = True
            fsxb__rgrs = ' & '.join(smzp__duehu)
            if yab__dvjpa:
                if output_dnf:
                    hroog__ubbe.append(f'[{yab__dvjpa}]')
                else:
                    hroog__ubbe.append(f'({yab__dvjpa})')
            hzdhf__rxrq.append(f'({fsxb__rgrs})')
        if output_dnf:
            raak__mri = ', '.join(hroog__ubbe)
        else:
            raak__mri = ' | '.join(hroog__ubbe)
        htd__dofwe = ' | '.join(hzdhf__rxrq)
        if raak__mri and not rhoyc__sevuy:
            if output_dnf:
                pou__tcmps = f'[{raak__mri}]'
            else:
                pou__tcmps = f'({raak__mri})'
        zsdus__byb = f'({htd__dofwe})'
    return pou__tcmps, zsdus__byb


def determine_filter_cast(col_types, typemap, filter_val, orig_colname_map,
    partition_names, source):
    import bodo
    wkjy__fxsap = filter_val[0]
    pogww__hsjx = col_types[orig_colname_map[wkjy__fxsap]]
    hqg__segdj = bodo.utils.typing.element_type(pogww__hsjx)
    if source == 'parquet' and wkjy__fxsap in partition_names:
        if hqg__segdj == types.unicode_type:
            cajo__dvm = '.cast(pyarrow.string(), safe=False)'
        elif isinstance(hqg__segdj, types.Integer):
            cajo__dvm = f'.cast(pyarrow.{hqg__segdj.name}(), safe=False)'
        else:
            cajo__dvm = ''
    else:
        cajo__dvm = ''
    hjh__wcm = typemap[filter_val[2].name]
    if isinstance(hjh__wcm, (types.List, types.Set)):
        cqxe__whl = hjh__wcm.dtype
    elif is_array_typ(hjh__wcm):
        cqxe__whl = hjh__wcm.dtype
    else:
        cqxe__whl = hjh__wcm
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(hqg__segdj,
        'Filter pushdown')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(cqxe__whl,
        'Filter pushdown')
    if not bodo.utils.typing.is_common_scalar_dtype([hqg__segdj, cqxe__whl]):
        if not bodo.utils.typing.is_safe_arrow_cast(hqg__segdj, cqxe__whl):
            raise BodoError(
                f'Unsupported Arrow cast from {hqg__segdj} to {cqxe__whl} in filter pushdown. Please try a comparison that avoids casting the column.'
                )
        if hqg__segdj == types.unicode_type and cqxe__whl in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif cqxe__whl == types.unicode_type and hqg__segdj in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            if isinstance(hjh__wcm, (types.List, types.Set)):
                guh__svi = 'list' if isinstance(hjh__wcm, types.List
                    ) else 'tuple'
                raise BodoError(
                    f'Cannot cast {guh__svi} values with isin filter pushdown.'
                    )
            return cajo__dvm, ".cast(pyarrow.timestamp('ns'), safe=False)"
        elif hqg__segdj == bodo.datetime_date_type and cqxe__whl in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return ".cast(pyarrow.timestamp('ns'), safe=False)", ''
        elif cqxe__whl == bodo.datetime_date_type and hqg__segdj in (bodo.
            datetime64ns, bodo.pd_timestamp_tz_naive_type):
            return cajo__dvm, ".cast(pyarrow.timestamp('ns'), safe=False)"
    return cajo__dvm, ''
