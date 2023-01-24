"""
Implementation of pd.read_sql in Bodo.
We piggyback on the pandas implementation. Future plan is to have a faster
version for this task.
"""
from typing import Any, List, Optional
from urllib.parse import urlparse
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, next_label, replace_arg_nodes
from numba.extending import intrinsic
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.hiframes.table import Table, TableType
from bodo.io.helpers import PyArrowTableSchemaType, is_nullable
from bodo.io.parquet_pio import ParquetPredicateType
from bodo.libs.array import cpp_table_to_py_table, delete_table, info_from_table, info_to_array, table_type
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.distributed_api import bcast, bcast_scalar
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_and_propagate_cpp_exception
if bodo.utils.utils.has_pyarrow():
    import llvmlite.binding as ll
    from bodo.io import arrow_cpp
    ll.add_symbol('snowflake_read', arrow_cpp.snowflake_read)
    ll.add_symbol('iceberg_pq_read', arrow_cpp.iceberg_pq_read)
MPI_ROOT = 0


class SqlReader(ir.Stmt):

    def __init__(self, sql_request: str, connection: str, df_out,
        df_colnames, out_vars, out_types, converted_colnames: List[str],
        db_type: str, loc, unsupported_columns: List[str],
        unsupported_arrow_types: List[pa.DataType], is_select_query: bool,
        has_side_effects: bool, index_column_name: str, index_column_type,
        database_schema: Optional[str], pyarrow_schema: Optional[pa.Schema],
        is_merge_into: bool, file_list_type, snapshot_id_type):
        self.connector_typ = 'sql'
        self.sql_request = sql_request
        self.connection = connection
        self.df_out = df_out
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.converted_colnames = converted_colnames
        self.loc = loc
        self.limit = req_limit(sql_request)
        self.db_type = db_type
        self.filters = None
        self.unsupported_columns = unsupported_columns
        self.unsupported_arrow_types = unsupported_arrow_types
        self.is_select_query = is_select_query
        self.has_side_effects = has_side_effects
        self.index_column_name = index_column_name
        self.index_column_type = index_column_type
        self.out_used_cols = list(range(len(df_colnames)))
        self.database_schema = database_schema
        self.pyarrow_schema = pyarrow_schema
        self.is_merge_into = is_merge_into
        self.is_live_table = True
        self.file_list_live = is_merge_into
        self.snapshot_id_live = is_merge_into
        if is_merge_into:
            self.file_list_type = file_list_type
            self.snapshot_id_type = snapshot_id_type
        else:
            self.file_list_type = types.none
            self.snapshot_id_type = types.none

    def __repr__(self):
        vaen__qotv = tuple(azifi__oopdr.name for azifi__oopdr in self.out_vars)
        return (
            f'{vaen__qotv} = SQLReader(sql_request={self.sql_request}, connection={self.connection}, col_names={self.df_colnames}, types={self.out_types}, df_out={self.df_out}, limit={self.limit}, unsupported_columns={self.unsupported_columns}, unsupported_arrow_types={self.unsupported_arrow_types}, is_select_query={self.is_select_query}, index_column_name={self.index_column_name}, index_column_type={self.index_column_type}, out_used_cols={self.out_used_cols}, database_schema={self.database_schema}, pyarrow_schema={self.pyarrow_schema}, is_merge_into={self.is_merge_into})'
            )


def parse_dbtype(con_str):
    oudwi__rdlc = urlparse(con_str)
    db_type = oudwi__rdlc.scheme
    ihsd__eote = oudwi__rdlc.password
    if con_str.startswith('oracle+cx_oracle://'):
        return 'oracle', ihsd__eote
    if db_type == 'mysql+pymysql':
        return 'mysql', ihsd__eote
    if con_str.startswith('iceberg+glue') or oudwi__rdlc.scheme in ('iceberg',
        'iceberg+file', 'iceberg+s3', 'iceberg+thrift', 'iceberg+http',
        'iceberg+https'):
        return 'iceberg', ihsd__eote
    return db_type, ihsd__eote


def remove_iceberg_prefix(con):
    import sys
    if sys.version_info.minor < 9:
        if con.startswith('iceberg+'):
            con = con[len('iceberg+'):]
        if con.startswith('iceberg://'):
            con = con[len('iceberg://'):]
    else:
        con = con.removeprefix('iceberg+').removeprefix('iceberg://')
    return con


def remove_dead_sql(sql_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    egl__vtfi = sql_node.out_vars[0].name
    uscbu__stdwg = sql_node.out_vars[1].name
    xinq__ozety = sql_node.out_vars[2].name if len(sql_node.out_vars
        ) > 2 else None
    bfmtf__tzw = sql_node.out_vars[3].name if len(sql_node.out_vars
        ) > 3 else None
    if (not sql_node.has_side_effects and egl__vtfi not in lives and 
        uscbu__stdwg not in lives and xinq__ozety not in lives and 
        bfmtf__tzw not in lives):
        return None
    if egl__vtfi not in lives:
        sql_node.out_types = []
        sql_node.df_colnames = []
        sql_node.out_used_cols = []
        sql_node.is_live_table = False
    if uscbu__stdwg not in lives:
        sql_node.index_column_name = None
        sql_node.index_arr_typ = types.none
    if xinq__ozety not in lives:
        sql_node.file_list_live = False
        sql_node.file_list_type = types.none
    if bfmtf__tzw not in lives:
        sql_node.snapshot_id_live = False
        sql_node.snapshot_id_type = types.none
    return sql_node


def sql_distributed_run(sql_node: SqlReader, array_dists, typemap,
    calltypes, typingctx, targetctx, is_independent=False,
    meta_head_only_info=None):
    if bodo.user_logging.get_verbose_level() >= 1:
        awshd__ggbxc = (
            'Finish column pruning on read_sql node:\n%s\nColumns loaded %s\n')
        kifuu__aca = []
        dict_encoded_cols = []
        for hcu__ipd in sql_node.out_used_cols:
            ila__krmj = sql_node.df_colnames[hcu__ipd]
            kifuu__aca.append(ila__krmj)
            if isinstance(sql_node.out_types[hcu__ipd], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                dict_encoded_cols.append(ila__krmj)
        if sql_node.index_column_name:
            kifuu__aca.append(sql_node.index_column_name)
            if isinstance(sql_node.index_column_type, bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                dict_encoded_cols.append(sql_node.index_column_name)
        vtxt__ckxzw = sql_node.loc.strformat()
        bodo.user_logging.log_message('Column Pruning', awshd__ggbxc,
            vtxt__ckxzw, kifuu__aca)
        if dict_encoded_cols:
            yij__dzt = """Finished optimized encoding on read_sql node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', yij__dzt,
                vtxt__ckxzw, dict_encoded_cols)
    parallel = bodo.ir.connector.is_connector_table_parallel(sql_node,
        array_dists, typemap, 'SQLReader')
    if sql_node.unsupported_columns:
        ytce__tijhg = set(sql_node.unsupported_columns)
        igia__rdat = set(sql_node.out_used_cols)
        eiuqx__apls = igia__rdat & ytce__tijhg
        if eiuqx__apls:
            swoxx__rowvj = sorted(eiuqx__apls)
            ykjy__yplfv = [
                f'pandas.read_sql(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                'Please manually remove these columns from your sql query by specifying the columns you need in your SELECT statement. If these '
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            ivc__apg = 0
            for incv__cbx in swoxx__rowvj:
                while sql_node.unsupported_columns[ivc__apg] != incv__cbx:
                    ivc__apg += 1
                ykjy__yplfv.append(
                    f"Column '{sql_node.original_df_colnames[incv__cbx]}' with unsupported arrow type {sql_node.unsupported_arrow_types[ivc__apg]}"
                    )
                ivc__apg += 1
            ckor__yul = '\n'.join(ykjy__yplfv)
            raise BodoError(ckor__yul, loc=sql_node.loc)
    if sql_node.limit is None and (not meta_head_only_info or 
        meta_head_only_info[0] is None):
        limit = None
    elif sql_node.limit is None:
        limit = meta_head_only_info[0]
    elif not meta_head_only_info or meta_head_only_info[0] is None:
        limit = sql_node.limit
    else:
        limit = min(limit, meta_head_only_info[0])
    iktg__gmgcw, jzd__ojbr = bodo.ir.connector.generate_filter_map(sql_node
        .filters)
    hlmp__zpr = ', '.join(iktg__gmgcw.values())
    vxxrk__zrarq = (
        f'def sql_impl(sql_request, conn, database_schema, {hlmp__zpr}):\n')
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        if sql_node.filters:
            gbk__uuuls = []
            for eeg__mlr in sql_node.filters:
                mdlci__cqp = []
                for hsoar__xxtc in eeg__mlr:
                    towvr__jaxt, fcp__hwbdw = hsoar__xxtc[0], hsoar__xxtc[2]
                    towvr__jaxt = convert_col_name(towvr__jaxt, sql_node.
                        converted_colnames)
                    towvr__jaxt = '\\"' + towvr__jaxt + '\\"'
                    fim__jeqnk = '{' + iktg__gmgcw[hsoar__xxtc[2].name
                        ] + '}' if isinstance(hsoar__xxtc[2], ir.Var
                        ) else fcp__hwbdw
                    if hsoar__xxtc[1] in ('startswith', 'endswith'):
                        dyigq__nbwi = ['(', hsoar__xxtc[1], '(',
                            towvr__jaxt, ',', fim__jeqnk, ')', ')']
                    else:
                        dyigq__nbwi = ['(', towvr__jaxt, hsoar__xxtc[1],
                            fim__jeqnk, ')']
                    mdlci__cqp.append(' '.join(dyigq__nbwi))
                gbk__uuuls.append(' ( ' + ' AND '.join(mdlci__cqp) + ' ) ')
            anil__lbe = ' WHERE ' + ' OR '.join(gbk__uuuls)
            for hcu__ipd, ujckm__atg in enumerate(iktg__gmgcw.values()):
                vxxrk__zrarq += (
                    f'    {ujckm__atg} = get_sql_literal({ujckm__atg})\n')
            vxxrk__zrarq += (
                f'    sql_request = f"{{sql_request}} {anil__lbe}"\n')
        if sql_node.limit != limit:
            vxxrk__zrarq += (
                f'    sql_request = f"{{sql_request}} LIMIT {limit}"\n')
    yekv__qpy = ''
    if sql_node.db_type == 'iceberg':
        yekv__qpy = hlmp__zpr
    vxxrk__zrarq += f"""    (total_rows, table_var, index_var, file_list, snapshot_id) = _sql_reader_py(sql_request, conn, database_schema, {yekv__qpy})
"""
    krmk__gzuec = {}
    exec(vxxrk__zrarq, {}, krmk__gzuec)
    cedqe__cavmi = krmk__gzuec['sql_impl']
    yftj__qmfbf = _gen_sql_reader_py(sql_node.df_colnames, sql_node.
        out_types, sql_node.index_column_name, sql_node.index_column_type,
        sql_node.out_used_cols, sql_node.converted_colnames, typingctx,
        targetctx, sql_node.db_type, limit, parallel, typemap, sql_node.
        filters, sql_node.pyarrow_schema, not sql_node.is_live_table,
        sql_node.is_select_query, sql_node.is_merge_into, is_independent)
    izc__thg = types.none if sql_node.database_schema is None else string_type
    gej__pleia = compile_to_numba_ir(cedqe__cavmi, {'_sql_reader_py':
        yftj__qmfbf, 'bcast_scalar': bcast_scalar, 'bcast': bcast,
        'get_sql_literal': _get_snowflake_sql_literal}, typingctx=typingctx,
        targetctx=targetctx, arg_typs=(string_type, string_type, izc__thg) +
        tuple(typemap[azifi__oopdr.name] for azifi__oopdr in jzd__ojbr),
        typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    if sql_node.is_select_query and sql_node.db_type != 'iceberg':
        loyd__uwwf = [sql_node.df_colnames[hcu__ipd] for hcu__ipd in
            sql_node.out_used_cols]
        if sql_node.index_column_name:
            loyd__uwwf.append(sql_node.index_column_name)
        if len(loyd__uwwf) == 0:
            ejab__njzc = 'COUNT(*)'
        else:
            ejab__njzc = escape_column_names(loyd__uwwf, sql_node.db_type,
                sql_node.converted_colnames)
        if sql_node.db_type == 'oracle':
            rvtc__pht = ('SELECT ' + ejab__njzc + ' FROM (' + sql_node.
                sql_request + ') TEMP')
        else:
            rvtc__pht = ('SELECT ' + ejab__njzc + ' FROM (' + sql_node.
                sql_request + ') as TEMP')
    else:
        rvtc__pht = sql_node.sql_request
    replace_arg_nodes(gej__pleia, [ir.Const(rvtc__pht, sql_node.loc), ir.
        Const(sql_node.connection, sql_node.loc), ir.Const(sql_node.
        database_schema, sql_node.loc)] + jzd__ojbr)
    wyma__exqzn = gej__pleia.body[:-3]
    if meta_head_only_info:
        wyma__exqzn[-5].target = meta_head_only_info[1]
    wyma__exqzn[-4].target = sql_node.out_vars[0]
    wyma__exqzn[-3].target = sql_node.out_vars[1]
    assert sql_node.has_side_effects or not (sql_node.index_column_name is
        None and not sql_node.is_live_table
        ), 'At most one of table and index should be dead if the SQL IR node is live and has no side effects'
    if sql_node.index_column_name is None:
        wyma__exqzn.pop(-3)
    elif not sql_node.is_live_table:
        wyma__exqzn.pop(-4)
    if sql_node.file_list_live:
        wyma__exqzn[-2].target = sql_node.out_vars[2]
    else:
        wyma__exqzn.pop(-2)
    if sql_node.snapshot_id_live:
        wyma__exqzn[-1].target = sql_node.out_vars[3]
    else:
        wyma__exqzn.pop(-1)
    return wyma__exqzn


def convert_col_name(col_name: str, converted_colnames: List[str]) ->str:
    if col_name in converted_colnames:
        return col_name.upper()
    return col_name


def escape_column_names(col_names, db_type, converted_colnames):
    if db_type == 'snowflake':
        from bodo.io.snowflake import escape_col_name
        ejab__njzc = ', '.join(escape_col_name(convert_col_name(toi__gfirl,
            converted_colnames)) for toi__gfirl in col_names)
    elif db_type == 'oracle':
        loyd__uwwf = []
        for toi__gfirl in col_names:
            loyd__uwwf.append(convert_col_name(toi__gfirl, converted_colnames))
        ejab__njzc = ', '.join([f'"{toi__gfirl}"' for toi__gfirl in loyd__uwwf]
            )
    elif db_type == 'mysql':
        ejab__njzc = ', '.join([f'`{toi__gfirl}`' for toi__gfirl in col_names])
    else:
        ejab__njzc = ', '.join([f'"{toi__gfirl}"' for toi__gfirl in col_names])
    return ejab__njzc


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal_scalar(filter_value):
    cpcme__zkcff = types.unliteral(filter_value)
    if cpcme__zkcff == types.unicode_type:
        return lambda filter_value: f'$${filter_value}$$'
    elif isinstance(cpcme__zkcff, (types.Integer, types.Float)
        ) or filter_value == types.bool_:
        return lambda filter_value: str(filter_value)
    elif isinstance(cpcme__zkcff, bodo.PandasTimestampType):
        if cpcme__zkcff.tz is None:
            rlvmz__qpjlv = 'TIMESTAMP_NTZ'
        else:
            rlvmz__qpjlv = 'TIMESTAMP_TZ'

        def impl(filter_value):
            uoo__jwmzg = filter_value.nanosecond
            qwab__oocio = ''
            if uoo__jwmzg < 10:
                qwab__oocio = '00'
            elif uoo__jwmzg < 100:
                qwab__oocio = '0'
            return (
                f"timestamp '{filter_value.strftime('%Y-%m-%d %H:%M:%S.%f')}{qwab__oocio}{uoo__jwmzg}'::{rlvmz__qpjlv}"
                )
        return impl
    elif cpcme__zkcff == bodo.datetime_date_type:
        return (lambda filter_value:
            f"date '{filter_value.strftime('%Y-%m-%d')}'")
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported scalar type {cpcme__zkcff} used in filter pushdown.'
            )


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def _get_snowflake_sql_literal(filter_value):
    scalar_isinstance = types.Integer, types.Float, bodo.PandasTimestampType
    ruwr__muv = bodo.datetime_date_type, types.unicode_type, types.bool_
    cpcme__zkcff = types.unliteral(filter_value)
    if (isinstance(cpcme__zkcff, (types.List, types.Array, bodo.
        IntegerArrayType, bodo.FloatingArrayType, bodo.DatetimeArrayType)) or
        cpcme__zkcff in (bodo.string_array_type, bodo.dict_str_arr_type,
        bodo.boolean_array, bodo.datetime_date_array_type)) and (isinstance
        (cpcme__zkcff.dtype, scalar_isinstance) or cpcme__zkcff.dtype in
        ruwr__muv):

        def impl(filter_value):
            yhept__edn = ', '.join([_get_snowflake_sql_literal_scalar(
                toi__gfirl) for toi__gfirl in filter_value])
            return f'({yhept__edn})'
        return impl
    elif isinstance(cpcme__zkcff, scalar_isinstance
        ) or cpcme__zkcff in ruwr__muv:
        return lambda filter_value: _get_snowflake_sql_literal_scalar(
            filter_value)
    else:
        raise BodoError(
            f'pd.read_sql(): Internal error, unsupported type {cpcme__zkcff} used in filter pushdown.'
            )


def sql_remove_dead_column(sql_node, column_live_map, equiv_vars, typemap):
    return bodo.ir.connector.base_connector_remove_dead_columns(sql_node,
        column_live_map, equiv_vars, typemap, 'SQLReader', sql_node.
        df_colnames, require_one_column=sql_node.db_type not in ('iceberg',
        'snowflake'))


numba.parfors.array_analysis.array_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[SqlReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[SqlReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[SqlReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[SqlReader] = remove_dead_sql
numba.core.analysis.ir_extension_usedefs[SqlReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[SqlReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[SqlReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[SqlReader] = sql_distributed_run
remove_dead_column_extensions[SqlReader] = sql_remove_dead_column
ir_extension_table_column_use[SqlReader
    ] = bodo.ir.connector.connector_table_column_use
compiled_funcs = []


@numba.njit
def sqlalchemy_check():
    with numba.objmode():
        sqlalchemy_check_()


def sqlalchemy_check_():
    try:
        import sqlalchemy
    except ImportError as atnn__yicc:
        crm__xncf = (
            "Using URI string without sqlalchemy installed. sqlalchemy can be installed by calling 'conda install -c conda-forge sqlalchemy'."
            )
        raise BodoError(crm__xncf)


@numba.njit
def pymysql_check():
    with numba.objmode():
        pymysql_check_()


def pymysql_check_():
    try:
        import pymysql
    except ImportError as atnn__yicc:
        crm__xncf = (
            "Using MySQL URI string requires pymsql to be installed. It can be installed by calling 'conda install -c conda-forge pymysql' or 'pip install PyMySQL'."
            )
        raise BodoError(crm__xncf)


@numba.njit
def cx_oracle_check():
    with numba.objmode():
        cx_oracle_check_()


def cx_oracle_check_():
    try:
        import cx_Oracle
    except ImportError as atnn__yicc:
        crm__xncf = (
            "Using Oracle URI string requires cx_oracle to be installed. It can be installed by calling 'conda install -c conda-forge cx_oracle' or 'pip install cx-Oracle'."
            )
        raise BodoError(crm__xncf)


@numba.njit
def psycopg2_check():
    with numba.objmode():
        psycopg2_check_()


def psycopg2_check_():
    try:
        import psycopg2
    except ImportError as atnn__yicc:
        crm__xncf = (
            "Using PostgreSQL URI string requires psycopg2 to be installed. It can be installed by calling 'conda install -c conda-forge psycopg2' or 'pip install psycopg2'."
            )
        raise BodoError(crm__xncf)


def req_limit(sql_request):
    import re
    jzh__hbm = re.compile('LIMIT\\s+(\\d+)\\s*$', re.IGNORECASE)
    yik__awiqw = jzh__hbm.search(sql_request)
    if yik__awiqw:
        return int(yik__awiqw.group(1))
    else:
        return None


def _gen_sql_reader_py(col_names: List[str], col_typs: List[Any],
    index_column_name: Optional[str], index_column_type, out_used_cols:
    List[int], converted_colnames: List[str], typingctx, targetctx, db_type:
    str, limit: Optional[int], parallel: bool, typemap, filters: Optional[
    Any], pyarrow_schema: Optional[pa.Schema], is_dead_table: bool,
    is_select_query: bool, is_merge_into: bool, is_independent: bool):
    woxzj__fvhu = next_label()
    loyd__uwwf = [col_names[hcu__ipd] for hcu__ipd in out_used_cols]
    wcv__zkxiq = [col_typs[hcu__ipd] for hcu__ipd in out_used_cols]
    if index_column_name:
        loyd__uwwf.append(index_column_name)
        wcv__zkxiq.append(index_column_type)
    hut__einh = None
    kitzs__gyr = None
    wcv__wbz = types.none if is_dead_table else TableType(tuple(col_typs))
    yekv__qpy = ''
    iktg__gmgcw = {}
    jzd__ojbr = []
    if filters and db_type == 'iceberg':
        iktg__gmgcw, jzd__ojbr = bodo.ir.connector.generate_filter_map(filters)
        yekv__qpy = ', '.join(iktg__gmgcw.values())
    vxxrk__zrarq = (
        f'def sql_reader_py(sql_request, conn, database_schema, {yekv__qpy}):\n'
        )
    if db_type == 'iceberg':
        assert pyarrow_schema is not None, 'SQLNode must contain a pyarrow_schema if reading from an Iceberg database'
        wtu__yrr, zdxs__jac = bodo.ir.connector.generate_arrow_filters(filters,
            iktg__gmgcw, jzd__ojbr, col_names, col_names, col_typs, typemap,
            'iceberg')
        kpj__diun = -1
        if is_merge_into and col_names.index('_bodo_row_id') in out_used_cols:
            kpj__diun = col_names.index('_bodo_row_id')
        selected_cols: List[int] = [pyarrow_schema.get_field_index(
            col_names[hcu__ipd]) for hcu__ipd in out_used_cols if hcu__ipd !=
            kpj__diun]
        nccw__xipym = {mpz__dati: hcu__ipd for hcu__ipd, mpz__dati in
            enumerate(selected_cols)}
        nullable_cols = [int(is_nullable(col_typs[hcu__ipd])) for hcu__ipd in
            selected_cols]
        nfzmj__cbme = [hcu__ipd for hcu__ipd in selected_cols if col_typs[
            hcu__ipd] == bodo.dict_str_arr_type]
        amn__njetx = (
            f'dict_str_cols_arr_{woxzj__fvhu}.ctypes, np.int32({len(nfzmj__cbme)})'
             if nfzmj__cbme else '0, 0')
        dhwvl__cbecu = ',' if yekv__qpy else ''
        vxxrk__zrarq += f"""  ev = bodo.utils.tracing.Event('read_iceberg', {parallel})
  dnf_filters, expr_filters = get_filters_pyobject("{wtu__yrr}", "{zdxs__jac}", ({yekv__qpy}{dhwvl__cbecu}))
  out_table, total_rows, file_list, snapshot_id = iceberg_read(
    unicode_to_utf8(conn),
    unicode_to_utf8(database_schema),
    unicode_to_utf8(sql_request),
    {parallel},
    {-1 if limit is None else limit},
    dnf_filters,
    expr_filters,
    selected_cols_arr_{woxzj__fvhu}.ctypes,
    {len(selected_cols)},
    nullable_cols_arr_{woxzj__fvhu}.ctypes,
    pyarrow_schema_{woxzj__fvhu},
    {amn__njetx},
    {is_merge_into},
  )
"""
        if parallel:
            vxxrk__zrarq += f"""  local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
        else:
            vxxrk__zrarq += f'  local_rows = total_rows\n'
        hut__einh = None
        if not is_dead_table:
            hut__einh = []
            atm__drakv = 0
            for hcu__ipd in range(len(col_names)):
                if atm__drakv < len(out_used_cols
                    ) and hcu__ipd == out_used_cols[atm__drakv]:
                    if hcu__ipd == kpj__diun:
                        hut__einh.append(len(selected_cols))
                    else:
                        hut__einh.append(nccw__xipym[hcu__ipd])
                    atm__drakv += 1
                else:
                    hut__einh.append(-1)
            hut__einh = np.array(hut__einh, dtype=np.int64)
        if is_dead_table:
            vxxrk__zrarq += '  table_var = None\n'
        else:
            vxxrk__zrarq += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{woxzj__fvhu}, py_table_type_{woxzj__fvhu})
"""
            if len(out_used_cols) == 0:
                vxxrk__zrarq += (
                    f'  table_var = set_table_len(table_var, local_rows)\n')
        uscbu__stdwg = 'None'
        if index_column_name is not None:
            axnv__mhj = len(out_used_cols) + 1 if not is_dead_table else 0
            uscbu__stdwg = (
                f'info_to_array(info_from_table(out_table, {axnv__mhj}), index_col_typ)'
                )
        vxxrk__zrarq += f'  index_var = {uscbu__stdwg}\n'
        vxxrk__zrarq += f'  delete_table(out_table)\n'
        vxxrk__zrarq += f'  ev.finalize()\n'
        vxxrk__zrarq += (
            '  return (total_rows, table_var, index_var, file_list, snapshot_id)\n'
            )
    elif db_type == 'snowflake':
        assert pyarrow_schema is not None, 'SQLNode must contain a pyarrow_schema if reading from Snowflake'
        if is_select_query:
            fkbbe__ckue = []
            for col_name in loyd__uwwf:
                bgiyk__cpav = convert_col_name(col_name, converted_colnames)
                ivc__apg = pyarrow_schema.get_field_index(bgiyk__cpav)
                if ivc__apg < 0:
                    raise BodoError(
                        f'SQLReader Snowflake: Column {bgiyk__cpav} is not in source schema'
                        )
                fkbbe__ckue.append(pyarrow_schema.field(ivc__apg))
            pyarrow_schema = pa.schema(fkbbe__ckue)
        jpfm__xekgd = {mpz__dati: hcu__ipd for hcu__ipd, mpz__dati in
            enumerate(out_used_cols)}
        juzdu__fmgzq = [jpfm__xekgd[hcu__ipd] for hcu__ipd in out_used_cols if
            col_typs[hcu__ipd] == dict_str_arr_type]
        nullable_cols = [int(is_nullable(col_typs[hcu__ipd])) for hcu__ipd in
            out_used_cols]
        if index_column_name:
            nullable_cols.append(int(is_nullable(index_column_type)))
        mrjf__evcg = np.array(juzdu__fmgzq, dtype=np.int32)
        cdctk__yqt = np.array(nullable_cols, dtype=np.int32)
        vxxrk__zrarq += f"""  ev = bodo.utils.tracing.Event('read_snowflake', {parallel})
  total_rows_np = np.array([0], dtype=np.int64)
  out_table = snowflake_read(
    unicode_to_utf8(sql_request),
    unicode_to_utf8(conn),
    {parallel},
    {is_independent},
    pyarrow_schema_{woxzj__fvhu},
    {len(cdctk__yqt)},
    nullable_cols_array.ctypes,
    snowflake_dict_cols_array.ctypes,
    {len(mrjf__evcg)},
    total_rows_np.ctypes,
    {is_select_query and len(loyd__uwwf) == 0},
    {is_select_query},
  )
  check_and_propagate_cpp_exception()
"""
        vxxrk__zrarq += f'  total_rows = total_rows_np[0]\n'
        if parallel:
            vxxrk__zrarq += f"""  local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
        else:
            vxxrk__zrarq += f'  local_rows = total_rows\n'
        if index_column_name:
            vxxrk__zrarq += f"""  index_var = info_to_array(info_from_table(out_table, {len(out_used_cols)}), index_col_typ)
"""
        else:
            vxxrk__zrarq += '  index_var = None\n'
        if not is_dead_table:
            ivc__apg = []
            atm__drakv = 0
            for hcu__ipd in range(len(col_names)):
                if atm__drakv < len(out_used_cols
                    ) and hcu__ipd == out_used_cols[atm__drakv]:
                    ivc__apg.append(atm__drakv)
                    atm__drakv += 1
                else:
                    ivc__apg.append(-1)
            hut__einh = np.array(ivc__apg, dtype=np.int64)
            vxxrk__zrarq += f"""  table_var = cpp_table_to_py_table(out_table, table_idx_{woxzj__fvhu}, py_table_type_{woxzj__fvhu})
"""
            if len(out_used_cols) == 0:
                if index_column_name:
                    vxxrk__zrarq += (
                        f'  table_var = set_table_len(table_var, len(index_var))\n'
                        )
                else:
                    vxxrk__zrarq += (
                        f'  table_var = set_table_len(table_var, local_rows)\n'
                        )
        else:
            vxxrk__zrarq += '  table_var = None\n'
        vxxrk__zrarq += '  delete_table(out_table)\n'
        vxxrk__zrarq += '  ev.finalize()\n'
        vxxrk__zrarq += (
            '  return (total_rows, table_var, index_var, None, None)\n')
    else:
        if not is_dead_table:
            vxxrk__zrarq += f"""  type_usecols_offsets_arr_{woxzj__fvhu}_2 = type_usecols_offsets_arr_{woxzj__fvhu}
"""
            kitzs__gyr = np.array(out_used_cols, dtype=np.int64)
        vxxrk__zrarq += '  df_typeref_2 = df_typeref\n'
        vxxrk__zrarq += '  sqlalchemy_check()\n'
        if db_type == 'mysql':
            vxxrk__zrarq += '  pymysql_check()\n'
        elif db_type == 'oracle':
            vxxrk__zrarq += '  cx_oracle_check()\n'
        elif db_type == 'postgresql' or db_type == 'postgresql+psycopg2':
            vxxrk__zrarq += '  psycopg2_check()\n'
        if parallel:
            vxxrk__zrarq += '  rank = bodo.libs.distributed_api.get_rank()\n'
            if limit is not None:
                vxxrk__zrarq += f'  nb_row = {limit}\n'
            else:
                vxxrk__zrarq += '  with objmode(nb_row="int64"):\n'
                vxxrk__zrarq += f'     if rank == {MPI_ROOT}:\n'
                vxxrk__zrarq += """         sql_cons = 'select count(*) from (' + sql_request + ') x'
"""
                vxxrk__zrarq += (
                    '         frame = pd.read_sql(sql_cons, conn)\n')
                vxxrk__zrarq += '         nb_row = frame.iat[0,0]\n'
                vxxrk__zrarq += '     else:\n'
                vxxrk__zrarq += '         nb_row = 0\n'
                vxxrk__zrarq += '  nb_row = bcast_scalar(nb_row)\n'
            vxxrk__zrarq += f"""  with objmode(table_var=py_table_type_{woxzj__fvhu}, index_var=index_col_typ):
"""
            vxxrk__zrarq += """    offset, limit = bodo.libs.distributed_api.get_start_count(nb_row)
"""
            if db_type == 'oracle':
                vxxrk__zrarq += f"""    sql_cons = 'select * from (' + sql_request + ') OFFSET ' + str(offset) + ' ROWS FETCH NEXT ' + str(limit) + ' ROWS ONLY'
"""
            else:
                vxxrk__zrarq += f"""    sql_cons = 'select * from (' + sql_request + ') x LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
"""
            vxxrk__zrarq += '    df_ret = pd.read_sql(sql_cons, conn)\n'
            vxxrk__zrarq += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        else:
            vxxrk__zrarq += f"""  with objmode(table_var=py_table_type_{woxzj__fvhu}, index_var=index_col_typ):
"""
            vxxrk__zrarq += '    df_ret = pd.read_sql(sql_request, conn)\n'
            vxxrk__zrarq += (
                '    bodo.ir.connector.cast_float_to_nullable(df_ret, df_typeref_2)\n'
                )
        if index_column_name:
            vxxrk__zrarq += (
                f'    index_var = df_ret.iloc[:, {len(out_used_cols)}].values\n'
                )
            vxxrk__zrarq += f"""    df_ret.drop(columns=df_ret.columns[{len(out_used_cols)}], inplace=True)
"""
        else:
            vxxrk__zrarq += '    index_var = None\n'
        if not is_dead_table:
            vxxrk__zrarq += f'    arrs = []\n'
            vxxrk__zrarq += f'    for i in range(df_ret.shape[1]):\n'
            vxxrk__zrarq += f'      arrs.append(df_ret.iloc[:, i].values)\n'
            vxxrk__zrarq += f"""    table_var = Table(arrs, type_usecols_offsets_arr_{woxzj__fvhu}_2, {len(col_names)})
"""
        else:
            vxxrk__zrarq += '    table_var = None\n'
        vxxrk__zrarq += '  return (-1, table_var, index_var, None, None)\n'
    emxb__hwmzz = globals()
    emxb__hwmzz.update({'bodo': bodo, f'py_table_type_{woxzj__fvhu}':
        wcv__wbz, 'index_col_typ': index_column_type})
    if db_type in ('iceberg', 'snowflake'):
        emxb__hwmzz.update({f'table_idx_{woxzj__fvhu}': hut__einh,
            f'pyarrow_schema_{woxzj__fvhu}': pyarrow_schema,
            'unicode_to_utf8': unicode_to_utf8,
            'check_and_propagate_cpp_exception':
            check_and_propagate_cpp_exception, 'info_to_array':
            info_to_array, 'info_from_table': info_from_table,
            'delete_table': delete_table, 'cpp_table_to_py_table':
            cpp_table_to_py_table, 'set_table_len': bodo.hiframes.table.
            set_table_len, 'get_node_portion': bodo.libs.distributed_api.
            get_node_portion})
    if db_type == 'iceberg':
        emxb__hwmzz.update({f'selected_cols_arr_{woxzj__fvhu}': np.array(
            selected_cols, np.int32), f'nullable_cols_arr_{woxzj__fvhu}':
            np.array(nullable_cols, np.int32),
            f'dict_str_cols_arr_{woxzj__fvhu}': np.array(nfzmj__cbme, np.
            int32), f'py_table_type_{woxzj__fvhu}': wcv__wbz,
            'get_filters_pyobject': bodo.io.parquet_pio.
            get_filters_pyobject, 'iceberg_read': _iceberg_pq_read})
    elif db_type == 'snowflake':
        emxb__hwmzz.update({'np': np, 'snowflake_read': _snowflake_read,
            'nullable_cols_array': cdctk__yqt, 'snowflake_dict_cols_array':
            mrjf__evcg})
    else:
        emxb__hwmzz.update({'sqlalchemy_check': sqlalchemy_check, 'pd': pd,
            'objmode': objmode, 'bcast_scalar': bcast_scalar,
            'pymysql_check': pymysql_check, 'cx_oracle_check':
            cx_oracle_check, 'psycopg2_check': psycopg2_check, 'df_typeref':
            bodo.DataFrameType(tuple(wcv__zkxiq), bodo.RangeIndexType(None),
            tuple(loyd__uwwf)), 'Table': Table,
            f'type_usecols_offsets_arr_{woxzj__fvhu}': kitzs__gyr})
    krmk__gzuec = {}
    exec(vxxrk__zrarq, emxb__hwmzz, krmk__gzuec)
    yftj__qmfbf = krmk__gzuec['sql_reader_py']
    viyx__umww = numba.njit(yftj__qmfbf)
    compiled_funcs.append(viyx__umww)
    return viyx__umww


parquet_predicate_type = ParquetPredicateType()
pyarrow_schema_type = PyArrowTableSchemaType()


@intrinsic
def _iceberg_pq_read(typingctx, conn_str, db_schema, sql_request_str,
    parallel, limit, dnf_filters, expr_filters, selected_cols,
    num_selected_cols, nullable_cols, pyarrow_schema, dict_encoded_cols,
    num_dict_encoded_cols, is_merge_into_cow):

    def codegen(context, builder, signature, args):
        vein__taze = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(1), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(64).as_pointer()])
        gemrb__mucb = cgutils.get_or_insert_function(builder.module,
            vein__taze, name='iceberg_pq_read')
        pgi__glm = cgutils.alloca_once(builder, lir.IntType(64))
        tbzkr__dvmst = cgutils.alloca_once(builder, lir.IntType(8).as_pointer()
            )
        iac__kiv = cgutils.alloca_once(builder, lir.IntType(64))
        rfo__nmesa = args + (pgi__glm, tbzkr__dvmst, iac__kiv)
        usij__wmnwo = builder.call(gemrb__mucb, rfo__nmesa)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        imfgz__rtk = builder.load(tbzkr__dvmst)
        rjgtz__adser = cgutils.create_struct_proxy(types.pyobject_of_list_type
            )(context, builder)
        jtru__xdh = context.get_python_api(builder)
        rjgtz__adser.meminfo = jtru__xdh.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), imfgz__rtk)
        rjgtz__adser.pyobj = imfgz__rtk
        jtru__xdh.decref(imfgz__rtk)
        iyiq__vhobx = [usij__wmnwo, builder.load(pgi__glm), rjgtz__adser.
            _getvalue(), builder.load(iac__kiv)]
        return context.make_tuple(builder, fiha__tnrxq, iyiq__vhobx)
    fiha__tnrxq = types.Tuple([table_type, types.int64, types.
        pyobject_of_list_type, types.int64])
    lubj__juhuw = fiha__tnrxq(types.voidptr, types.voidptr, types.voidptr,
        types.boolean, types.int64, parquet_predicate_type,
        parquet_predicate_type, types.voidptr, types.int32, types.voidptr,
        pyarrow_schema_type, types.voidptr, types.int32, types.boolean)
    return lubj__juhuw, codegen


_snowflake_read = types.ExternalFunction('snowflake_read', table_type(types
    .voidptr, types.voidptr, types.boolean, types.boolean,
    pyarrow_schema_type, types.int64, types.voidptr, types.voidptr, types.
    int32, types.voidptr, types.boolean, types.boolean))
