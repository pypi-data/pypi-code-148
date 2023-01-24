"""
File that contains the main functionality for the Iceberg
integration within the Bodo repo. This does not contain the
main IR transformation.
"""
import os
import re
import sys
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from mpi4py import MPI
from numba.core import types
from numba.extending import intrinsic
import bodo
from bodo.io.fs_io import get_s3_bucket_region_njit
from bodo.io.helpers import _get_numba_typ_from_pa_typ, pyarrow_table_schema_type
from bodo.libs.array import arr_info_list_to_table, array_to_info, py_table_to_cpp_table
from bodo.libs.str_ext import unicode_to_utf8
from bodo.utils import tracing
from bodo.utils.py_objs import install_py_obj_class
from bodo.utils.typing import BodoError


def format_iceberg_conn(conn_str: str) ->str:
    ewcr__emha = urlparse(conn_str)
    if not conn_str.startswith('iceberg+glue') and ewcr__emha.scheme not in (
        'iceberg', 'iceberg+file', 'iceberg+s3', 'iceberg+thrift',
        'iceberg+http', 'iceberg+https'):
        raise BodoError(
            "'con' must start with one of the following: 'iceberg://', 'iceberg+file://', 'iceberg+s3://', 'iceberg+thrift://', 'iceberg+http://', 'iceberg+https://', 'iceberg+glue'"
            )
    if sys.version_info.minor < 9:
        if conn_str.startswith('iceberg+'):
            conn_str = conn_str[len('iceberg+'):]
        if conn_str.startswith('iceberg://'):
            conn_str = conn_str[len('iceberg://'):]
    else:
        conn_str = conn_str.removeprefix('iceberg+').removeprefix('iceberg://')
    return conn_str


@numba.njit
def format_iceberg_conn_njit(conn_str):
    with numba.objmode(conn_str='unicode_type'):
        conn_str = format_iceberg_conn(conn_str)
    return conn_str


def get_iceberg_type_info(table_name: str, con: str, database_schema: str,
    is_merge_into_cow: bool=False):
    import bodo_iceberg_connector
    import numba.core
    aep__atj = None
    lvfw__ltlve = None
    xfqhe__bgj = None
    if bodo.get_rank() == 0:
        try:
            aep__atj, lvfw__ltlve, xfqhe__bgj = (bodo_iceberg_connector.
                get_iceberg_typing_schema(con, database_schema, table_name))
            if xfqhe__bgj is None:
                raise BodoError('No such Iceberg table found')
        except bodo_iceberg_connector.IcebergError as jvgb__xed:
            if isinstance(jvgb__xed, bodo_iceberg_connector.IcebergJavaError
                ) and numba.core.config.DEVELOPER_MODE:
                aep__atj = BodoError(
                    f'{jvgb__xed.message}: {jvgb__xed.java_error}')
            else:
                aep__atj = BodoError(jvgb__xed.message)
    oqi__gmik = MPI.COMM_WORLD
    aep__atj = oqi__gmik.bcast(aep__atj)
    if isinstance(aep__atj, Exception):
        raise aep__atj
    col_names = aep__atj
    lvfw__ltlve = oqi__gmik.bcast(lvfw__ltlve)
    xfqhe__bgj = oqi__gmik.bcast(xfqhe__bgj)
    vsxc__lfw = [_get_numba_typ_from_pa_typ(typ, False, True, None)[0] for
        typ in lvfw__ltlve]
    if is_merge_into_cow:
        col_names.append('_bodo_row_id')
        vsxc__lfw.append(types.Array(types.int64, 1, 'C'))
    return col_names, vsxc__lfw, xfqhe__bgj


def get_iceberg_file_list(table_name: str, conn: str, database_schema: str,
    filters) ->Tuple[List[str], List[str]]:
    import bodo_iceberg_connector
    import numba.core
    assert bodo.get_rank(
        ) == 0, 'get_iceberg_file_list should only ever be called on rank 0, as the operation requires access to the py4j server, which is only available on rank 0'
    try:
        hjykv__umt = (bodo_iceberg_connector.
            bodo_connector_get_parquet_file_list(conn, database_schema,
            table_name, filters))
    except bodo_iceberg_connector.IcebergError as jvgb__xed:
        if isinstance(jvgb__xed, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(f'{jvgb__xed.message}:\n{jvgb__xed.java_error}')
        else:
            raise BodoError(jvgb__xed.message)
    return hjykv__umt


def get_iceberg_snapshot_id(table_name: str, conn: str, database_schema: str):
    import bodo_iceberg_connector
    import numba.core
    assert bodo.get_rank(
        ) == 0, 'get_iceberg_snapshot_id should only ever be called on rank 0, as the operation requires access to the py4j server, which is only available on rank 0'
    try:
        snapshot_id = (bodo_iceberg_connector.
            bodo_connector_get_current_snapshot_id(conn, database_schema,
            table_name))
    except bodo_iceberg_connector.IcebergError as jvgb__xed:
        if isinstance(jvgb__xed, bodo_iceberg_connector.IcebergJavaError
            ) and numba.core.config.DEVELOPER_MODE:
            raise BodoError(f'{jvgb__xed.message}:\n{jvgb__xed.java_error}')
        else:
            raise BodoError(jvgb__xed.message)
    return snapshot_id


class IcebergParquetDataset:

    def __init__(self, conn, database_schema, table_name, pa_table_schema,
        pq_file_list, snapshot_id, pq_dataset=None):
        self.pq_dataset = pq_dataset
        self.conn = conn
        self.database_schema = database_schema
        self.table_name = table_name
        self.schema = pa_table_schema
        self.file_list = pq_file_list
        self.snapshot_id = snapshot_id
        self.pieces = []
        self._bodo_total_rows = 0
        self._prefix = ''
        self.filesystem = None
        if pq_dataset is not None:
            self.pieces = pq_dataset.pieces
            self._bodo_total_rows = pq_dataset._bodo_total_rows
            self._prefix = pq_dataset._prefix
            self.filesystem = pq_dataset.filesystem


def get_iceberg_pq_dataset(conn: str, database_schema: str, table_name: str,
    typing_pa_table_schema: pa.Schema, dnf_filters=None, expr_filters=None,
    tot_rows_to_read=None, is_parallel=False, get_row_counts=True):
    fxcm__gzor = get_row_counts and tracing.is_tracing()
    if fxcm__gzor:
        cgers__pzb = tracing.Event('get_iceberg_pq_dataset')
    oqi__gmik = MPI.COMM_WORLD
    svc__hphsc = None
    tme__ept = None
    hgw__kddpa = None
    if bodo.get_rank() == 0:
        if fxcm__gzor:
            zmto__dknwy = tracing.Event('get_iceberg_file_list',
                is_parallel=False)
            zmto__dknwy.add_attribute('g_dnf_filter', str(dnf_filters))
        try:
            svc__hphsc, hgw__kddpa = get_iceberg_file_list(table_name, conn,
                database_schema, dnf_filters)
            if fxcm__gzor:
                yikfx__vawkc = int(os.environ.get(
                    'BODO_ICEBERG_TRACING_NUM_FILES_TO_LOG', '50'))
                zmto__dknwy.add_attribute('num_files', len(svc__hphsc))
                zmto__dknwy.add_attribute(f'first_{yikfx__vawkc}_files',
                    ', '.join(svc__hphsc[:yikfx__vawkc]))
        except Exception as jvgb__xed:
            svc__hphsc = jvgb__xed
        if fxcm__gzor:
            zmto__dknwy.finalize()
            pkmon__iuhex = tracing.Event('get_snapshot_id', is_parallel=False)
        try:
            tme__ept = get_iceberg_snapshot_id(table_name, conn,
                database_schema)
        except Exception as jvgb__xed:
            tme__ept = jvgb__xed
        if fxcm__gzor:
            pkmon__iuhex.finalize()
    svc__hphsc, tme__ept, hgw__kddpa = oqi__gmik.bcast((svc__hphsc,
        tme__ept, hgw__kddpa))
    if isinstance(svc__hphsc, Exception):
        rikon__hye = svc__hphsc
        raise BodoError(
            f"""Error reading Iceberg Table: {type(rikon__hye).__name__}: {str(rikon__hye)}
"""
            )
    if isinstance(tme__ept, Exception):
        rikon__hye = tme__ept
        raise BodoError(
            f"""Error reading Iceberg Table: {type(rikon__hye).__name__}: {str(rikon__hye)}
"""
            )
    pne__odbjy: List[str] = svc__hphsc
    snapshot_id: int = tme__ept
    if len(pne__odbjy) == 0:
        pq_dataset = None
    else:
        try:
            pq_dataset = bodo.io.parquet_pio.get_parquet_dataset(pne__odbjy,
                get_row_counts=get_row_counts, expr_filters=expr_filters,
                is_parallel=is_parallel, typing_pa_schema=
                typing_pa_table_schema, partitioning=None, tot_rows_to_read
                =tot_rows_to_read)
        except BodoError as jvgb__xed:
            if re.search('Schema .* was different', str(jvgb__xed), re.
                IGNORECASE):
                raise BodoError(
                    f"""Bodo currently doesn't support reading Iceberg tables with schema evolution.
{jvgb__xed}"""
                    )
            else:
                raise
    nbto__tojly = IcebergParquetDataset(conn, database_schema, table_name,
        typing_pa_table_schema, hgw__kddpa, snapshot_id, pq_dataset)
    if fxcm__gzor:
        cgers__pzb.finalize()
    return nbto__tojly


def are_schemas_compatible(pa_schema: pa.Schema, df_schema: pa.Schema,
    allow_downcasting: bool=False) ->bool:
    if pa_schema.equals(df_schema):
        return True
    if len(df_schema) < len(pa_schema):
        qgxe__mopwf = []
        for scz__yejes in pa_schema:
            dmq__cao = df_schema.field_by_name(scz__yejes.name)
            if not (dmq__cao is None and scz__yejes.nullable):
                qgxe__mopwf.append(scz__yejes)
        pa_schema = pa.schema(qgxe__mopwf)
    if len(pa_schema) != len(df_schema):
        return False
    for pepa__hpdwd in range(len(df_schema)):
        dmq__cao = df_schema.field(pepa__hpdwd)
        scz__yejes = pa_schema.field(pepa__hpdwd)
        if dmq__cao.equals(scz__yejes):
            continue
        ieq__exp = dmq__cao.type
        via__gys = scz__yejes.type
        if not ieq__exp.equals(via__gys) and allow_downcasting and (pa.
            types.is_signed_integer(ieq__exp) and pa.types.
            is_signed_integer(via__gys) or pa.types.is_floating(ieq__exp) and
            pa.types.is_floating(via__gys)
            ) and ieq__exp.bit_width > via__gys.bit_width:
            dmq__cao = dmq__cao.with_type(via__gys)
        if not dmq__cao.nullable and scz__yejes.nullable:
            dmq__cao = dmq__cao.with_nullable(True)
        elif allow_downcasting and dmq__cao.nullable and not scz__yejes.nullable:
            dmq__cao = dmq__cao.with_nullable(False)
        df_schema = df_schema.set(pepa__hpdwd, dmq__cao)
    return df_schema.equals(pa_schema)


def get_table_details_before_write(table_name: str, conn: str,
    database_schema: str, df_schema: pa.Schema, if_exists: str,
    allow_downcasting: bool=False):
    cgers__pzb = tracing.Event('iceberg_get_table_details_before_write')
    import bodo_iceberg_connector as connector
    oqi__gmik = MPI.COMM_WORLD
    vsk__xchny = None
    iceberg_schema_id = None
    table_loc = ''
    partition_spec = []
    sort_order = []
    iceberg_schema_str = ''
    pa_schema = None
    bsrz__ihql = {zdxa__mha: basj__mfv for basj__mfv, zdxa__mha in
        enumerate(df_schema.names)}
    if oqi__gmik.Get_rank() == 0:
        try:
            (table_loc, iceberg_schema_id, pa_schema, iceberg_schema_str,
                partition_spec, sort_order) = (connector.get_typing_info(
                conn, database_schema, table_name))
            for zaux__uwgl, *kgs__pdc in partition_spec:
                assert zaux__uwgl in bsrz__ihql, f'Iceberg Partition column {zaux__uwgl} not found in dataframe'
            for zaux__uwgl, *kgs__pdc in sort_order:
                assert zaux__uwgl in bsrz__ihql, f'Iceberg Sort column {zaux__uwgl} not found in dataframe'
            partition_spec = [(bsrz__ihql[zaux__uwgl], *axvpa__bnm) for 
                zaux__uwgl, *axvpa__bnm in partition_spec]
            sort_order = [(bsrz__ihql[zaux__uwgl], *axvpa__bnm) for 
                zaux__uwgl, *axvpa__bnm in sort_order]
            if if_exists == 'append' and pa_schema is not None:
                if not are_schemas_compatible(pa_schema, df_schema,
                    allow_downcasting):
                    if numba.core.config.DEVELOPER_MODE:
                        raise BodoError(
                            f"""DataFrame schema needs to be an ordered subset of Iceberg table for append

Iceberg:
{pa_schema}

DataFrame:
{df_schema}
"""
                            )
                    else:
                        raise BodoError(
                            'DataFrame schema needs to be an ordered subset of Iceberg table for append'
                            )
            if iceberg_schema_id is None:
                iceberg_schema_str = connector.pyarrow_to_iceberg_schema_str(
                    df_schema)
        except connector.IcebergError as jvgb__xed:
            if isinstance(jvgb__xed, connector.IcebergJavaError
                ) and numba.core.config.DEVELOPER_MODE:
                vsk__xchny = BodoError(
                    f'{jvgb__xed.message}: {jvgb__xed.java_error}')
            else:
                vsk__xchny = BodoError(jvgb__xed.message)
        except Exception as jvgb__xed:
            vsk__xchny = jvgb__xed
    vsk__xchny = oqi__gmik.bcast(vsk__xchny)
    if isinstance(vsk__xchny, Exception):
        raise vsk__xchny
    table_loc = oqi__gmik.bcast(table_loc)
    iceberg_schema_id = oqi__gmik.bcast(iceberg_schema_id)
    partition_spec = oqi__gmik.bcast(partition_spec)
    sort_order = oqi__gmik.bcast(sort_order)
    iceberg_schema_str = oqi__gmik.bcast(iceberg_schema_str)
    pa_schema = oqi__gmik.bcast(pa_schema)
    if iceberg_schema_id is None:
        already_exists = False
        iceberg_schema_id = -1
    else:
        already_exists = True
    cgers__pzb.finalize()
    return (already_exists, table_loc, iceberg_schema_id, partition_spec,
        sort_order, iceberg_schema_str, pa_schema if if_exists == 'append' and
        pa_schema is not None else df_schema)


def collect_file_info(iceberg_files_info) ->Tuple[List[str], List[int],
    List[int]]:
    from mpi4py import MPI
    oqi__gmik = MPI.COMM_WORLD
    uggum__pscw = [ztpl__ykhe[0] for ztpl__ykhe in iceberg_files_info]
    kcb__jgxq = oqi__gmik.gather(uggum__pscw)
    fnames = [bcnx__njhyd for mmxlc__ycu in kcb__jgxq for bcnx__njhyd in
        mmxlc__ycu] if oqi__gmik.Get_rank() == 0 else None
    dww__teuww = np.array([ztpl__ykhe[1] for ztpl__ykhe in
        iceberg_files_info], dtype=np.int64)
    sivo__sjomf = np.array([ztpl__ykhe[2] for ztpl__ykhe in
        iceberg_files_info], dtype=np.int64)
    qrltj__rzo = bodo.gatherv(dww__teuww).tolist()
    beqow__mhjsn = bodo.gatherv(sivo__sjomf).tolist()
    return fnames, qrltj__rzo, beqow__mhjsn


def register_table_write(conn_str: str, db_name: str, table_name: str,
    table_loc: str, fnames: List[str], all_metrics: Dict[str, List[Any]],
    iceberg_schema_id: int, pa_schema, partition_spec, sort_order, mode: str):
    cgers__pzb = tracing.Event('iceberg_register_table_write')
    import bodo_iceberg_connector
    oqi__gmik = MPI.COMM_WORLD
    success = False
    if oqi__gmik.Get_rank() == 0:
        utfy__zgwg = None if iceberg_schema_id < 0 else iceberg_schema_id
        success = bodo_iceberg_connector.commit_write(conn_str, db_name,
            table_name, table_loc, fnames, all_metrics, utfy__zgwg,
            pa_schema, partition_spec, sort_order, mode)
    success = oqi__gmik.bcast(success)
    cgers__pzb.finalize()
    return success


def register_table_merge_cow(conn_str: str, db_name: str, table_name: str,
    table_loc: str, old_fnames: List[str], new_fnames: List[str],
    all_metrics: Dict[str, List[Any]], snapshot_id: int):
    cgers__pzb = tracing.Event('iceberg_register_table_merge_cow')
    import bodo_iceberg_connector
    oqi__gmik = MPI.COMM_WORLD
    success = False
    if oqi__gmik.Get_rank() == 0:
        success = bodo_iceberg_connector.commit_merge_cow(conn_str, db_name,
            table_name, table_loc, old_fnames, new_fnames, all_metrics,
            snapshot_id)
    success: bool = oqi__gmik.bcast(success)
    cgers__pzb.finalize()
    return success


from numba.extending import NativeValue, box, models, register_model, unbox


class PythonListOfHeterogeneousTuples(types.Opaque):

    def __init__(self):
        super(PythonListOfHeterogeneousTuples, self).__init__(name=
            'PythonListOfHeterogeneousTuples')


python_list_of_heterogeneous_tuples_type = PythonListOfHeterogeneousTuples()
types.python_list_of_heterogeneous_tuples_type = (
    python_list_of_heterogeneous_tuples_type)
register_model(PythonListOfHeterogeneousTuples)(models.OpaqueModel)


@unbox(PythonListOfHeterogeneousTuples)
def unbox_python_list_of_heterogeneous_tuples_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(PythonListOfHeterogeneousTuples)
def box_python_list_of_heterogeneous_tuples_type(typ, val, c):
    c.pyapi.incref(val)
    return val


this_module = sys.modules[__name__]
PyObjectOfList = install_py_obj_class(types_name='pyobject_of_list_type',
    python_type=None, module=this_module, class_name='PyObjectOfListType',
    model_name='PyObjectOfListModel')


@numba.njit()
def iceberg_pq_write(table_loc, bodo_table, col_names, partition_spec,
    sort_order, iceberg_schema_str, is_parallel, expected_schema):
    bucket_region = get_s3_bucket_region_njit(table_loc, is_parallel)
    okkk__xeae = 'snappy'
    flwke__pxj = -1
    iceberg_files_info = iceberg_pq_write_table_cpp(unicode_to_utf8(
        table_loc), bodo_table, col_names, partition_spec, sort_order,
        unicode_to_utf8(okkk__xeae), is_parallel, unicode_to_utf8(
        bucket_region), flwke__pxj, unicode_to_utf8(iceberg_schema_str),
        expected_schema)
    return iceberg_files_info


@numba.njit()
def iceberg_write(table_name, conn, database_schema, bodo_table, col_names,
    if_exists, is_parallel, df_pyarrow_schema, allow_downcasting=False):
    cgers__pzb = tracing.Event('iceberg_write_py', is_parallel)
    assert is_parallel, 'Iceberg Write only supported for distributed dataframes'
    with numba.objmode(already_exists='bool_', table_loc='unicode_type',
        iceberg_schema_id='i8', partition_spec=
        'python_list_of_heterogeneous_tuples_type', sort_order=
        'python_list_of_heterogeneous_tuples_type', iceberg_schema_str=
        'unicode_type', expected_schema='pyarrow_table_schema_type'):
        (already_exists, table_loc, iceberg_schema_id, partition_spec,
            sort_order, iceberg_schema_str, expected_schema) = (
            get_table_details_before_write(table_name, conn,
            database_schema, df_pyarrow_schema, if_exists, allow_downcasting))
    if already_exists and if_exists == 'fail':
        raise ValueError(f'Table already exists.')
    if already_exists:
        mode = if_exists
    else:
        mode = 'create'
    iceberg_files_info = iceberg_pq_write(table_loc, bodo_table, col_names,
        partition_spec, sort_order, iceberg_schema_str, is_parallel,
        expected_schema)
    with numba.objmode(success='bool_'):
        fnames, qrltj__rzo, beqow__mhjsn = collect_file_info(iceberg_files_info
            )
        success = register_table_write(conn, database_schema, table_name,
            table_loc, fnames, {'size': beqow__mhjsn, 'record_count':
            qrltj__rzo}, iceberg_schema_id, df_pyarrow_schema,
            partition_spec, sort_order, mode)
    if not success:
        raise BodoError('Iceberg write failed.')
    cgers__pzb.finalize()


@numba.generated_jit(nopython=True)
def iceberg_merge_cow_py(table_name, conn, database_schema, bodo_df,
    snapshot_id, old_fnames, is_parallel=False):
    if not is_parallel:
        raise BodoError(
            'Merge Into with Iceberg Tables are only supported on distributed DataFrames'
            )
    df_pyarrow_schema = bodo.io.helpers.numba_to_pyarrow_schema(bodo_df,
        is_iceberg=True)
    jwrg__nfv = pd.array(bodo_df.columns)
    if bodo_df.is_table_format:
        gvpx__rdgs = bodo_df.table_type

        def impl(table_name, conn, database_schema, bodo_df, snapshot_id,
            old_fnames, is_parallel=False):
            iceberg_merge_cow(table_name, format_iceberg_conn_njit(conn),
                database_schema, py_table_to_cpp_table(bodo.hiframes.
                pd_dataframe_ext.get_dataframe_table(bodo_df), gvpx__rdgs),
                snapshot_id, old_fnames, array_to_info(jwrg__nfv),
                df_pyarrow_schema, is_parallel)
    else:
        jgw__xtzon = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(bodo_df, {}))'
            .format(basj__mfv) for basj__mfv in range(len(bodo_df.columns)))
        vab__hler = 'def impl(\n'
        vab__hler += '    table_name,\n'
        vab__hler += '    conn,\n'
        vab__hler += '    database_schema,\n'
        vab__hler += '    bodo_df,\n'
        vab__hler += '    snapshot_id,\n'
        vab__hler += '    old_fnames,\n'
        vab__hler += '    is_parallel=False,\n'
        vab__hler += '):\n'
        vab__hler += '    info_list = [{}]\n'.format(jgw__xtzon)
        vab__hler += '    table = arr_info_list_to_table(info_list)\n'
        vab__hler += '    iceberg_merge_cow(\n'
        vab__hler += '        table_name,\n'
        vab__hler += '        format_iceberg_conn_njit(conn),\n'
        vab__hler += '        database_schema,\n'
        vab__hler += '        table,\n'
        vab__hler += '        snapshot_id,\n'
        vab__hler += '        old_fnames,\n'
        vab__hler += '        array_to_info(col_names_py),\n'
        vab__hler += '        df_pyarrow_schema,\n'
        vab__hler += '        is_parallel,\n'
        vab__hler += '    )\n'
        locals = dict()
        globals = {'bodo': bodo, 'array_to_info': array_to_info,
            'arr_info_list_to_table': arr_info_list_to_table,
            'iceberg_merge_cow': iceberg_merge_cow,
            'format_iceberg_conn_njit': format_iceberg_conn_njit,
            'col_names_py': jwrg__nfv, 'df_pyarrow_schema': df_pyarrow_schema}
        exec(vab__hler, globals, locals)
        impl = locals['impl']
    return impl


@numba.njit()
def iceberg_merge_cow(table_name, conn, database_schema, bodo_table,
    snapshot_id, old_fnames, col_names, df_pyarrow_schema, is_parallel):
    cgers__pzb = tracing.Event('iceberg_merge_cow_py', is_parallel)
    assert is_parallel, 'Iceberg Write only supported for distributed dataframes'
    with numba.objmode(already_exists='bool_', table_loc='unicode_type',
        partition_spec='python_list_of_heterogeneous_tuples_type',
        sort_order='python_list_of_heterogeneous_tuples_type',
        iceberg_schema_str='unicode_type', expected_schema=
        'pyarrow_table_schema_type'):
        (already_exists, table_loc, kgs__pdc, partition_spec, sort_order,
            iceberg_schema_str, expected_schema) = (
            get_table_details_before_write(table_name, conn,
            database_schema, df_pyarrow_schema, 'append', allow_downcasting
            =True))
    if not already_exists:
        raise ValueError(f'Iceberg MERGE INTO: Table does not exist at write')
    iceberg_files_info = iceberg_pq_write(table_loc, bodo_table, col_names,
        partition_spec, sort_order, iceberg_schema_str, is_parallel,
        expected_schema)
    with numba.objmode(success='bool_'):
        fnames, qrltj__rzo, beqow__mhjsn = collect_file_info(iceberg_files_info
            )
        success = register_table_merge_cow(conn, database_schema,
            table_name, table_loc, old_fnames, fnames, {'size':
            beqow__mhjsn, 'record_count': qrltj__rzo}, snapshot_id)
    if not success:
        raise BodoError('Iceberg MERGE INTO: write failed')
    cgers__pzb.finalize()


import llvmlite.binding as ll
from llvmlite import ir as lir
from numba.core import cgutils, types
if bodo.utils.utils.has_pyarrow():
    from bodo.io import arrow_cpp
    ll.add_symbol('iceberg_pq_write', arrow_cpp.iceberg_pq_write)


@intrinsic
def iceberg_pq_write_table_cpp(typingctx, table_data_loc_t, table_t,
    col_names_t, partition_spec_t, sort_order_t, compression_t,
    is_parallel_t, bucket_region, row_group_size, iceberg_metadata_t,
    iceberg_schema_t):

    def codegen(context, builder, sig, args):
        guhrx__copy = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(8).as_pointer(), lir.IntType(64), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        gyje__vps = cgutils.get_or_insert_function(builder.module,
            guhrx__copy, name='iceberg_pq_write')
        mckd__bge = builder.call(gyje__vps, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return mckd__bge
    return types.python_list_of_heterogeneous_tuples_type(types.voidptr,
        table_t, col_names_t, python_list_of_heterogeneous_tuples_type,
        python_list_of_heterogeneous_tuples_type, types.voidptr, types.
        boolean, types.voidptr, types.int64, types.voidptr,
        pyarrow_table_schema_type), codegen
