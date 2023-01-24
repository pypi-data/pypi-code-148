import os
import sys
import traceback
import warnings
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Callable, Dict, List, Literal, Optional, Tuple
from urllib.parse import parse_qsl, urlparse
from uuid import uuid4
import pyarrow as pa
from mpi4py import MPI
from numba.core import types
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.io.helpers import ExceptionPropagatingThread, _get_numba_typ_from_pa_typ, update_env_vars, update_file_contents
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.py_objs import install_py_obj_class
from bodo.utils.typing import BodoError, BodoWarning, is_str_arr_type
if TYPE_CHECKING:
    from snowflake.connector import SnowflakeConnection
    from snowflake.connector.cursor import ResultMetadata, SnowflakeCursor
    from snowflake.connector.result_batch import JSONResultBatch, ResultBatch
SF_READ_SCHEMA_PROBE_TIMEOUT = 5
SF_READ_AUTO_DICT_ENCODE_ENABLED = True
SF_READ_DICT_ENCODE_CRITERION = 0.5
SF_READ_DICT_ENCODING_PROBE_TIMEOUT = 5
SF_READ_DICT_ENCODING_IF_TIMEOUT = False
SF_READ_DICT_ENCODING_PROBE_ROW_LIMIT = 100000000
SCALE_TO_UNIT_PRECISION: Dict[int, Literal['s', 'ms', 'us', 'ns']] = {(0):
    's', (3): 'ms', (6): 'us', (9): 'ns'}
TYPE_CODE_TO_ARROW_TYPE: List[Callable[['ResultMetadata', str], pa.DataType]
    ] = [lambda m, _: pa.int64() if m.scale == 0 else pa.float64() if m.
    scale < 18 else pa.decimal128(m.precision, m.scale), lambda _, __: pa.
    float64(), lambda _, __: pa.string(), lambda _, __: pa.date32(), lambda
    _, __: pa.time64('ns'), lambda _, __: pa.string(), lambda m, tz: pa.
    timestamp(SCALE_TO_UNIT_PRECISION[m.scale], tz=tz), lambda m, tz: pa.
    timestamp(SCALE_TO_UNIT_PRECISION[m.scale], tz=tz), lambda m, _: pa.
    timestamp(SCALE_TO_UNIT_PRECISION[m.scale]), lambda _, __: pa.string(),
    lambda _, __: pa.string(), lambda _, __: pa.binary(), lambda m, _: {(0):
    pa.time32('s'), (3): pa.time32('ms'), (6): pa.time64('us'), (9): pa.
    time64('ns')}[m.scale], lambda _, __: pa.bool_(), lambda _, __: pa.string()
    ]
INT_BITSIZE_TO_ARROW_DATATYPE = {(1): pa.int8(), (2): pa.int16(), (4): pa.
    int32(), (8): pa.int64()}


def gen_snowflake_schema(column_names, column_datatypes):
    sf_schema = {}
    for col_name, hfg__ctf in zip(column_names, column_datatypes):
        if isinstance(hfg__ctf, bodo.DatetimeArrayType
            ) or hfg__ctf == bodo.datetime_datetime_type:
            sf_schema[col_name] = 'TIMESTAMP_NTZ'
        elif hfg__ctf == bodo.datetime_date_array_type:
            sf_schema[col_name] = 'DATE'
        elif isinstance(hfg__ctf, bodo.TimeArrayType):
            if hfg__ctf.precision in [0, 3, 6]:
                vhilk__qnpf = hfg__ctf.precision
            elif hfg__ctf.precision == 9:
                if bodo.get_rank() == 0:
                    warnings.warn(BodoWarning(
                        f"""to_sql(): {col_name} time precision will be lost.
Snowflake loses nano second precision when exporting parquet file using COPY INTO.
 This is due to a limitation on Parquet V1 that is currently being used in Snowflake"""
                        ))
                vhilk__qnpf = 6
            else:
                raise ValueError(
                    'Unsupported Precision Found in Bodo Time Array')
            sf_schema[col_name] = f'TIME({vhilk__qnpf})'
        elif isinstance(hfg__ctf, types.Array):
            pzzab__jdvs = hfg__ctf.dtype.name
            if pzzab__jdvs.startswith('datetime'):
                sf_schema[col_name] = 'DATETIME'
            if pzzab__jdvs.startswith('timedelta'):
                sf_schema[col_name] = 'NUMBER(38, 0)'
                if bodo.get_rank() == 0:
                    warnings.warn(BodoWarning(
                        f"to_sql(): {col_name} with type 'timedelta' will be written as integer values (ns frequency) to the database."
                        ))
            elif pzzab__jdvs.startswith(('int', 'uint')):
                sf_schema[col_name] = 'NUMBER(38, 0)'
            elif pzzab__jdvs.startswith('float'):
                sf_schema[col_name] = 'REAL'
        elif is_str_arr_type(hfg__ctf):
            sf_schema[col_name] = 'TEXT'
        elif hfg__ctf == bodo.binary_array_type:
            sf_schema[col_name] = 'BINARY'
        elif hfg__ctf == bodo.boolean_array:
            sf_schema[col_name] = 'BOOLEAN'
        elif isinstance(hfg__ctf, bodo.IntegerArrayType):
            sf_schema[col_name] = 'NUMBER(38, 0)'
        elif isinstance(hfg__ctf, bodo.FloatingArrayType):
            sf_schema[col_name] = 'REAL'
        elif isinstance(hfg__ctf, bodo.DecimalArrayType):
            sf_schema[col_name] = 'NUMBER(38, 18)'
        elif isinstance(hfg__ctf, (ArrayItemArrayType, StructArrayType)):
            sf_schema[col_name] = 'VARIANT'
        else:
            raise BodoError(
                f'Conversion from Bodo array type {hfg__ctf} to snowflake type for {col_name} not supported yet.'
                )
    return sf_schema


SF_WRITE_COPY_INTO_ON_ERROR = 'abort_statement'
SF_WRITE_OVERLAP_UPLOAD = True
SF_WRITE_PARQUET_CHUNK_SIZE = int(256000000.0)
SF_WRITE_PARQUET_COMPRESSION = 'snappy'
SF_WRITE_UPLOAD_USING_PUT = False
SF_AZURE_WRITE_HDFS_CORE_SITE = """<configuration>
  <property>
    <name>fs.azure.account.auth.type</name>
    <value>SAS</value>
  </property>
  <property>
    <name>fs.azure.sas.token.provider.type</name>
    <value>org.bodo.azurefs.sas.BodoSASTokenProvider</value>
  </property>
  <property>
    <name>fs.abfs.impl</name>
    <value>org.apache.hadoop.fs.azurebfs.AzureBlobFileSystem</value>
  </property>
</configuration>
"""
SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION = os.path.join(bodo.
    HDFS_CORE_SITE_LOC_DIR.name, 'sas_token.txt')


def execute_query(cursor: 'SnowflakeCursor', query: str, timeout: Optional[int]
    ) ->Optional['SnowflakeCursor']:
    try:
        return cursor.execute(query, timeout=timeout)
    except snowflake.connector.errors.ProgrammingError as npq__hmkhl:
        if 'SQL execution canceled' in str(npq__hmkhl):
            return None
        else:
            raise


def escape_col_name(col_name: str) ->str:
    return '"{}"'.format(col_name.replace('"', '""'))


def snowflake_connect(conn_str: str, is_parallel: bool=False
    ) ->'SnowflakeConnection':
    qpn__bvyp = tracing.Event('snowflake_connect', is_parallel=is_parallel)
    iooq__mlk = urlparse(conn_str)
    apvww__qgea = {}
    if iooq__mlk.username:
        apvww__qgea['user'] = iooq__mlk.username
    if iooq__mlk.password:
        apvww__qgea['password'] = iooq__mlk.password
    if iooq__mlk.hostname:
        apvww__qgea['account'] = iooq__mlk.hostname
    if iooq__mlk.port:
        apvww__qgea['port'] = iooq__mlk.port
    if iooq__mlk.path:
        jlp__hblk = iooq__mlk.path
        if jlp__hblk.startswith('/'):
            jlp__hblk = jlp__hblk[1:]
        nnbg__pmap = jlp__hblk.split('/')
        if len(nnbg__pmap) == 2:
            usxsm__ohw, schema = nnbg__pmap
        elif len(nnbg__pmap) == 1:
            usxsm__ohw = nnbg__pmap[0]
            schema = None
        else:
            raise BodoError(
                f'Unexpected Snowflake connection string {conn_str}. Path is expected to contain database name and possibly schema'
                )
        apvww__qgea['database'] = usxsm__ohw
        if schema:
            apvww__qgea['schema'] = schema
    if iooq__mlk.query:
        for ffvi__itug, nxh__txr in parse_qsl(iooq__mlk.query):
            apvww__qgea[ffvi__itug] = nxh__txr
            if ffvi__itug == 'session_parameters':
                import json
                apvww__qgea[ffvi__itug] = json.loads(nxh__txr)
    apvww__qgea['application'] = 'bodo'
    apvww__qgea['login_timeout'] = 5
    try:
        import snowflake.connector
    except ImportError as cjb__uru:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    conn = snowflake.connector.connect(**apvww__qgea)
    tywsc__hbb = os.environ.get('BODO_PLATFORM_WORKSPACE_REGION', None)
    if tywsc__hbb and bodo.get_rank() == 0:
        tywsc__hbb = tywsc__hbb.lower()
        sjux__batip = os.environ.get('BODO_PLATFORM_CLOUD_PROVIDER', None)
        if sjux__batip is not None:
            sjux__batip = sjux__batip.lower()
        lwf__syfxk = conn.cursor()
        lwf__syfxk.execute('select current_region()')
        tdcr__aam: pa.Table = lwf__syfxk.fetch_arrow_all()
        fgs__kzg = tdcr__aam[0][0].as_py()
        lwf__syfxk.close()
        pvke__cnmv = fgs__kzg.split('_')
        yve__jooit = pvke__cnmv[0].lower()
        olddw__jfdky = '-'.join(pvke__cnmv[1:]).lower()
        if sjux__batip and sjux__batip != yve__jooit:
            uzjt__ykxzk = BodoWarning(
                f'Performance Warning: The Snowflake warehouse and Bodo platform are on different cloud providers. '
                 +
                f'The Snowflake warehouse is located on {yve__jooit}, but the Bodo cluster is located on {sjux__batip}. '
                 +
                'For best performance we recommend using your cluster and Snowflake account in the same region with the same cloud provider.'
                )
            warnings.warn(uzjt__ykxzk)
        elif tywsc__hbb != olddw__jfdky:
            uzjt__ykxzk = BodoWarning(
                f'Performance Warning: The Snowflake warehouse and Bodo platform are in different cloud regions. '
                 +
                f'The Snowflake warehouse is located in {olddw__jfdky}, but the Bodo cluster is located in {tywsc__hbb}. '
                 +
                'For best performance we recommend using your cluster and Snowflake account in the same region with the same cloud provider.'
                )
            warnings.warn(uzjt__ykxzk)
    qpn__bvyp.finalize()
    return conn


def get_schema_from_metadata(cursor: 'SnowflakeCursor', sql_query: str,
    is_select_query: bool) ->Tuple[List[pa.Field], List, List[int], List[pa
    .DataType]]:
    ppd__quftu = cursor.describe(sql_query)
    tz: str = cursor._timezone
    ldh__tdhd: List[pa.Field] = []
    kvres__lna: List[str] = []
    zpdt__jkwn: List[int] = []
    for tmw__kzpe, tsko__pae in enumerate(ppd__quftu):
        bfx__atck = TYPE_CODE_TO_ARROW_TYPE[tsko__pae.type_code](tsko__pae, tz)
        ldh__tdhd.append(pa.field(tsko__pae.name, bfx__atck, tsko__pae.
            is_nullable))
        if pa.types.is_int64(bfx__atck):
            kvres__lna.append(tsko__pae.name)
            zpdt__jkwn.append(tmw__kzpe)
    if is_select_query and len(kvres__lna) != 0:
        cbd__nfv = 'SELECT ' + ', '.join(
            f'SYSTEM$TYPEOF({escape_col_name(x)})' for x in kvres__lna
            ) + f' FROM ({sql_query}) LIMIT 1'
        jao__rbtrk = execute_query(cursor, cbd__nfv, timeout=
            SF_READ_SCHEMA_PROBE_TIMEOUT)
        if jao__rbtrk is not None and (grdq__yqvq := jao__rbtrk.
            fetch_arrow_all()) is not None:
            for tmw__kzpe, (iji__idg, kcbb__bguix) in enumerate(grdq__yqvq.
                to_pylist()[0].items()):
                uor__lwsbu = kvres__lna[tmw__kzpe]
                avz__vbft = (
                    f'SYSTEM$TYPEOF({escape_col_name(uor__lwsbu)})',
                    f'SYSTEM$TYPEOF({escape_col_name(uor__lwsbu.upper())})')
                assert iji__idg in avz__vbft, 'Output of Snowflake Schema Probe Query Uses Unexpected Column Names'
                lnuri__erjw = zpdt__jkwn[tmw__kzpe]
                yxizc__obuf = int(kcbb__bguix[-2])
                aine__gxzye = INT_BITSIZE_TO_ARROW_DATATYPE[yxizc__obuf]
                ldh__tdhd[lnuri__erjw] = ldh__tdhd[lnuri__erjw].with_type(
                    aine__gxzye)
    ditq__zlt = []
    kpkv__vpu = []
    lobhm__pnvs = []
    for tmw__kzpe, tvsu__xgfl in enumerate(ldh__tdhd):
        bfx__atck, lauj__ocrdj = _get_numba_typ_from_pa_typ(tvsu__xgfl, 
            False, tvsu__xgfl.nullable, None)
        ditq__zlt.append(bfx__atck)
        if not lauj__ocrdj:
            kpkv__vpu.append(tmw__kzpe)
            lobhm__pnvs.append(tvsu__xgfl.type)
    return ldh__tdhd, ditq__zlt, kpkv__vpu, lobhm__pnvs


def get_schema(conn_str: str, sql_query: str, is_select_query: bool,
    _bodo_read_as_dict: Optional[List[str]]):
    conn = snowflake_connect(conn_str)
    cursor = conn.cursor()
    mrx__vjwi, ditq__zlt, kpkv__vpu, lobhm__pnvs = get_schema_from_metadata(
        cursor, sql_query, is_select_query)
    ymwmq__sxd = _bodo_read_as_dict if _bodo_read_as_dict else []
    cfo__yop = {}
    for tmw__kzpe, rzk__afxrk in enumerate(ditq__zlt):
        if rzk__afxrk == string_array_type:
            cfo__yop[mrx__vjwi[tmw__kzpe].name] = tmw__kzpe
    vdkib__wlag = {(cqv__jpwja.lower() if cqv__jpwja.isupper() else
        cqv__jpwja): cqv__jpwja for cqv__jpwja in cfo__yop.keys()}
    gvt__nizo = ymwmq__sxd - vdkib__wlag.keys()
    if len(gvt__nizo) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(BodoWarning(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {gvt__nizo}'
                ))
    fig__jymvw = vdkib__wlag.keys() & ymwmq__sxd
    for cqv__jpwja in fig__jymvw:
        ditq__zlt[cfo__yop[vdkib__wlag[cqv__jpwja]]] = dict_str_arr_type
    hsiwl__nauj, cnkf__mvi = [], []
    anr__txkp = vdkib__wlag.keys() - ymwmq__sxd
    for cqv__jpwja in anr__txkp:
        hsiwl__nauj.append(f'count (distinct "{vdkib__wlag[cqv__jpwja]}")')
        cnkf__mvi.append(cfo__yop[vdkib__wlag[cqv__jpwja]])
    guktp__qsu: Optional[Tuple[int, List[str]]] = None
    if len(hsiwl__nauj) != 0 and SF_READ_AUTO_DICT_ENCODE_ENABLED:
        vghep__ojks = max(SF_READ_DICT_ENCODING_PROBE_ROW_LIMIT // len(
            hsiwl__nauj), 1)
        gfk__kehr = (
            f"select count(*),{', '.join(hsiwl__nauj)}from ( select * from ({sql_query}) limit {vghep__ojks} ) SAMPLE (1)"
            )
        pnn__jgmc = execute_query(cursor, gfk__kehr, timeout=
            SF_READ_DICT_ENCODING_PROBE_TIMEOUT)
        if pnn__jgmc is None:
            guktp__qsu = vghep__ojks, hsiwl__nauj
            if SF_READ_DICT_ENCODING_IF_TIMEOUT:
                for tmw__kzpe in cnkf__mvi:
                    ditq__zlt[tmw__kzpe] = dict_str_arr_type
        else:
            ivl__gmad: pa.Table = pnn__jgmc.fetch_arrow_all()
            wcn__ywt = ivl__gmad[0][0].as_py()
            dzajc__itnt = [(ivl__gmad[tmw__kzpe][0].as_py() / max(wcn__ywt,
                1)) for tmw__kzpe in range(1, len(hsiwl__nauj) + 1)]
            porvw__dan = filter(lambda x: x[0] <=
                SF_READ_DICT_ENCODE_CRITERION, zip(dzajc__itnt, cnkf__mvi))
            for _, ejxuv__ngktu in porvw__dan:
                ditq__zlt[ejxuv__ngktu] = dict_str_arr_type
    lcavc__kkg: List[str] = []
    jwoyt__cqg = set()
    for x in mrx__vjwi:
        if x.name.isupper():
            jwoyt__cqg.add(x.name.lower())
            lcavc__kkg.append(x.name.lower())
        else:
            lcavc__kkg.append(x.name)
    uwq__evn = DataFrameType(data=tuple(ditq__zlt), columns=tuple(lcavc__kkg))
    return uwq__evn, jwoyt__cqg, kpkv__vpu, lobhm__pnvs, pa.schema(mrx__vjwi
        ), guktp__qsu


class SnowflakeDataset(object):

    def __init__(self, batches: List['ResultBatch'], schema, conn:
        'SnowflakeConnection'):
        self.pieces = batches
        self._bodo_total_rows = 0
        for yvm__vgs in batches:
            yvm__vgs._bodo_num_rows = yvm__vgs.rowcount
            self._bodo_total_rows += yvm__vgs._bodo_num_rows
        self.schema = schema
        self.conn = conn


class FakeArrowJSONResultBatch:

    def __init__(self, json_batch: 'JSONResultBatch', schema: pa.Schema
        ) ->None:
        self._json_batch = json_batch
        self._schema = schema

    @property
    def rowcount(self):
        return self._json_batch.rowcount

    def to_arrow(self, _: Optional['SnowflakeConnection']=None) ->pa.Table:
        msm__eywei = []
        for aqhs__kqdit in self._json_batch.create_iter():
            msm__eywei.append({self._schema.names[tmw__kzpe]: rdzr__fhk for
                tmw__kzpe, rdzr__fhk in enumerate(aqhs__kqdit)})
        dtt__ymw = pa.Table.from_pylist(msm__eywei, schema=self._schema)
        return dtt__ymw


def get_dataset(query: str, conn_str: str, schema: pa.Schema,
    only_fetch_length: bool=False, is_select_query: bool=True, is_parallel:
    bool=True, is_independent: bool=False) ->Tuple[SnowflakeDataset, int]:
    assert not (only_fetch_length and not is_select_query
        ), 'The only length optimization can only be run with select queries'
    assert not (is_parallel and is_independent
        ), 'Snowflake get_dataset: is_parallel and is_independent cannot be True at the same time'
    try:
        import snowflake.connector
        from snowflake.connector.result_batch import ArrowResultBatch, JSONResultBatch
    except ImportError as cjb__uru:
        raise BodoError(
            "Snowflake Python connector packages not found. Fetching data from Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    qpn__bvyp = tracing.Event('get_snowflake_dataset', is_parallel=is_parallel)
    sith__befb = MPI.COMM_WORLD
    conn = snowflake_connect(conn_str)
    qty__bhe = -1
    batches = []
    if only_fetch_length and is_select_query:
        if bodo.get_rank() == 0 or is_independent:
            lwf__syfxk = conn.cursor()
            qpk__klk = tracing.Event('execute_length_query', is_parallel=False)
            lwf__syfxk.execute(query)
            tdcr__aam = lwf__syfxk.fetch_arrow_all()
            qty__bhe = tdcr__aam[0][0].as_py()
            lwf__syfxk.close()
            qpk__klk.finalize()
        if not is_independent:
            qty__bhe = sith__befb.bcast(qty__bhe)
    else:
        if bodo.get_rank() == 0 or is_independent:
            lwf__syfxk = conn.cursor()
            qpk__klk = tracing.Event('execute_query', is_parallel=False)
            lwf__syfxk = conn.cursor()
            lwf__syfxk.execute(query)
            qpk__klk.finalize()
            qty__bhe: int = lwf__syfxk.rowcount
            batches: 'List[ResultBatch]' = lwf__syfxk.get_result_batches()
            if len(batches) > 0 and not isinstance(batches[0], ArrowResultBatch
                ):
                if not is_select_query and len(batches) == 1 and isinstance(
                    batches[0], JSONResultBatch):
                    batches = [FakeArrowJSONResultBatch(x, schema) for x in
                        batches]
                else:
                    raise BodoError(
                        f"Batches returns from Snowflake don't match the expected format. Expected Arrow batches but got {type(batches[0])}"
                        )
            lwf__syfxk.close()
        if not is_independent:
            qty__bhe, batches, schema = sith__befb.bcast((qty__bhe, batches,
                schema))
    owtvy__dcr = SnowflakeDataset(batches, schema, conn)
    qpn__bvyp.finalize()
    return owtvy__dcr, qty__bhe


def create_internal_stage(cursor: 'SnowflakeCursor', is_temporary: bool=False
    ) ->str:
    qpn__bvyp = tracing.Event('create_internal_stage', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as cjb__uru:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    stage_name = ''
    cro__vnvlp = None
    while True:
        try:
            stage_name = f'bodo_io_snowflake_{uuid4()}'
            if is_temporary:
                yomr__hvjt = 'CREATE TEMPORARY STAGE'
            else:
                yomr__hvjt = 'CREATE STAGE'
            cmv__snkmu = (
                f'{yomr__hvjt} "{stage_name}" /* Python:bodo.io.snowflake.create_internal_stage() */ '
                )
            cursor.execute(cmv__snkmu, _is_internal=True).fetchall()
            break
        except snowflake.connector.ProgrammingError as hkr__svq:
            if hkr__svq.msg is not None and hkr__svq.msg.endswith(
                'already exists.'):
                continue
            cro__vnvlp = hkr__svq.msg
            break
    qpn__bvyp.finalize()
    if cro__vnvlp is not None:
        raise snowflake.connector.ProgrammingError(cro__vnvlp)
    return stage_name


def drop_internal_stage(cursor: 'SnowflakeCursor', stage_name: str):
    qpn__bvyp = tracing.Event('drop_internal_stage', is_parallel=False)
    nfpaj__tuf = (
        f'DROP STAGE "{stage_name}" /* Python:bodo.io.snowflake.drop_internal_stage() */ '
        )
    cursor.execute(nfpaj__tuf, _is_internal=True)
    qpn__bvyp.finalize()


def do_upload_and_cleanup(cursor: 'SnowflakeCursor', chunk_idx: int,
    chunk_path: str, stage_name: str):

    def upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name):
        vginy__yrw = tracing.Event(f'upload_parquet_file{chunk_idx}',
            is_parallel=False)
        txsa__thm = (
            f'PUT \'file://{chunk_path}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.do_upload_and_cleanup() */'
            )
        cursor.execute(txsa__thm, _is_internal=True).fetchall()
        vginy__yrw.finalize()
        os.remove(chunk_path)
    if SF_WRITE_OVERLAP_UPLOAD:
        ftt__docws = ExceptionPropagatingThread(target=
            upload_cleanup_thread_func, args=(chunk_idx, chunk_path,
            stage_name))
        ftt__docws.start()
    else:
        upload_cleanup_thread_func(chunk_idx, chunk_path, stage_name)
        ftt__docws = None
    return ftt__docws


def create_table_handle_exists(cursor: 'SnowflakeCursor', stage_name: str,
    location: str, sf_schema, if_exists: str):
    qpn__bvyp = tracing.Event('create_table_if_not_exists', is_parallel=False)
    try:
        import snowflake.connector
    except ImportError as cjb__uru:
        raise BodoError(
            "Snowflake Python connector packages not found. Using 'to_sql' with Snowflake requires snowflake-connector-python. This can be installed by calling 'conda install -c conda-forge snowflake-connector-python' or 'pip install snowflake-connector-python'."
            )
    if if_exists == 'fail':
        fsbcu__vsbfo = 'CREATE TABLE'
    elif if_exists == 'replace':
        fsbcu__vsbfo = 'CREATE OR REPLACE TABLE'
    elif if_exists == 'append':
        fsbcu__vsbfo = 'CREATE TABLE IF NOT EXISTS'
    else:
        raise ValueError(f"'{if_exists}' is not valid for if_exists")
    oset__qxjhi = tracing.Event('create_table', is_parallel=False)
    fbqqz__udk = ', '.join([f'"{vmie__jip}" {sf_schema[vmie__jip]}' for
        vmie__jip in sf_schema.keys()])
    ilq__pppa = (
        f'{fsbcu__vsbfo} {location} ({fbqqz__udk}) /* Python:bodo.io.snowflake.create_table_if_not_exists() */'
        )
    cursor.execute(ilq__pppa, _is_internal=True)
    oset__qxjhi.finalize()
    qpn__bvyp.finalize()


def execute_copy_into(cursor: 'SnowflakeCursor', stage_name: str, location:
    str, sf_schema):
    qpn__bvyp = tracing.Event('execute_copy_into', is_parallel=False)
    nlinl__zbxe = ','.join([f'"{vmie__jip}"' for vmie__jip in sf_schema.keys()]
        )
    yrc__tmo = {vmie__jip: ('::binary' if sf_schema[vmie__jip] == 'BINARY' else
        '::string' if sf_schema[vmie__jip].startswith('TIME') else '') for
        vmie__jip in sf_schema.keys()}
    bch__rxj = ','.join([f'$1:"{vmie__jip}"{yrc__tmo[vmie__jip]}' for
        vmie__jip in sf_schema.keys()])
    ahhyg__ebj = (
        f'COPY INTO {location} ({nlinl__zbxe}) FROM (SELECT {bch__rxj} FROM @"{stage_name}") FILE_FORMAT=(TYPE=PARQUET COMPRESSION=AUTO BINARY_AS_TEXT=False) PURGE=TRUE ON_ERROR={SF_WRITE_COPY_INTO_ON_ERROR} /* Python:bodo.io.snowflake.execute_copy_into() */'
        )
    aam__upv = cursor.execute(ahhyg__ebj, _is_internal=True).fetchall()
    hzfk__jeau = sum(1 if npq__hmkhl[1] == 'LOADED' else 0 for npq__hmkhl in
        aam__upv)
    jmkq__ozmx = len(aam__upv)
    skjsm__hdq = sum(int(npq__hmkhl[3]) for npq__hmkhl in aam__upv)
    wnj__auin = hzfk__jeau, jmkq__ozmx, skjsm__hdq, aam__upv
    qpn__bvyp.add_attribute('copy_into_nsuccess', hzfk__jeau)
    qpn__bvyp.add_attribute('copy_into_nchunks', jmkq__ozmx)
    qpn__bvyp.add_attribute('copy_into_nrows', skjsm__hdq)
    if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
        print(f'[Snowflake Write] copy_into results: {repr(aam__upv)}')
    qpn__bvyp.finalize()
    return wnj__auin


try:
    import snowflake.connector
    snowflake_connector_cursor_python_type = (snowflake.connector.cursor.
        SnowflakeCursor)
except (ImportError, AttributeError) as cjb__uru:
    snowflake_connector_cursor_python_type = None
SnowflakeConnectorCursorType = install_py_obj_class(types_name=
    'snowflake_connector_cursor_type', python_type=
    snowflake_connector_cursor_python_type, module=sys.modules[__name__],
    class_name='SnowflakeConnectorCursorType', model_name=
    'SnowflakeConnectorCursorModel')
TemporaryDirectoryType = install_py_obj_class(types_name=
    'temporary_directory_type', python_type=TemporaryDirectory, module=sys.
    modules[__name__], class_name='TemporaryDirectoryType', model_name=
    'TemporaryDirectoryModel')


def get_snowflake_stage_info(cursor: 'SnowflakeCursor', stage_name: str,
    tmp_folder: TemporaryDirectory) ->Dict:
    qpn__bvyp = tracing.Event('get_snowflake_stage_info', is_parallel=False)
    ytwgr__col = os.path.join(tmp_folder.name,
        f'get_credentials_{uuid4()}.parquet')
    ytwgr__col = ytwgr__col.replace('\\', '\\\\').replace("'", "\\'")
    txsa__thm = (
        f'PUT \'file://{ytwgr__col}\' @"{stage_name}" AUTO_COMPRESS=FALSE /* Python:bodo.io.snowflake.get_snowflake_stage_info() */'
        )
    hlwb__domvm = cursor._execute_helper(txsa__thm, is_internal=True)
    qpn__bvyp.finalize()
    return hlwb__domvm


def connect_and_get_upload_info(conn_str: str):
    qpn__bvyp = tracing.Event('connect_and_get_upload_info')
    sith__befb = MPI.COMM_WORLD
    tgc__qxtd = sith__befb.Get_rank()
    tmp_folder = TemporaryDirectory()
    cursor = None
    stage_name = ''
    mqmy__hitrp = ''
    zpq__cwgnh = {}
    old_creds = {}
    old_core_site = ''
    tmaze__jjq = ''
    old_sas_token = ''
    dyev__kvbsi = None
    if tgc__qxtd == 0:
        try:
            conn = snowflake_connect(conn_str)
            cursor = conn.cursor()
            is_temporary = not SF_WRITE_UPLOAD_USING_PUT
            stage_name = create_internal_stage(cursor, is_temporary=
                is_temporary)
            if SF_WRITE_UPLOAD_USING_PUT:
                mqmy__hitrp = ''
            else:
                hlwb__domvm = get_snowflake_stage_info(cursor, stage_name,
                    tmp_folder)
                zhscq__rss = hlwb__domvm['data']['uploadInfo']
                usd__yie = zhscq__rss.get('locationType', 'UNKNOWN')
                ayd__apn = False
                if usd__yie == 'S3':
                    sizx__bkbkp, _, jlp__hblk = zhscq__rss['location'
                        ].partition('/')
                    jlp__hblk = jlp__hblk.rstrip('/')
                    mqmy__hitrp = f's3://{sizx__bkbkp}/{jlp__hblk}/'
                    zpq__cwgnh = {'AWS_ACCESS_KEY_ID': zhscq__rss['creds'][
                        'AWS_KEY_ID'], 'AWS_SECRET_ACCESS_KEY': zhscq__rss[
                        'creds']['AWS_SECRET_KEY'], 'AWS_SESSION_TOKEN':
                        zhscq__rss['creds']['AWS_TOKEN'],
                        'AWS_DEFAULT_REGION': zhscq__rss['region']}
                elif usd__yie == 'AZURE':
                    dalvl__hcugy = False
                    try:
                        import bodo_azurefs_sas_token_provider
                        dalvl__hcugy = True
                    except ImportError as cjb__uru:
                        pass
                    rjuo__igsou = len(os.environ.get('HADOOP_HOME', '')
                        ) > 0 and len(os.environ.get('ARROW_LIBHDFS_DIR', '')
                        ) > 0 and len(os.environ.get('CLASSPATH', '')) > 0
                    if dalvl__hcugy and rjuo__igsou:
                        bvt__wpee, _, jlp__hblk = zhscq__rss['location'
                            ].partition('/')
                        jlp__hblk = jlp__hblk.rstrip('/')
                        shu__bqp = zhscq__rss['storageAccount']
                        tmaze__jjq = zhscq__rss['creds']['AZURE_SAS_TOKEN'
                            ].lstrip('?')
                        if len(jlp__hblk) == 0:
                            mqmy__hitrp = (
                                f'abfs://{bvt__wpee}@{shu__bqp}.dfs.core.windows.net/'
                                )
                        else:
                            mqmy__hitrp = (
                                f'abfs://{bvt__wpee}@{shu__bqp}.dfs.core.windows.net/{jlp__hblk}/'
                                )
                        if not 'BODO_PLATFORM_WORKSPACE_UUID' in os.environ:
                            warnings.warn(BodoWarning(
                                """Detected Azure Stage. Bodo will try to upload to the stage directly. If this fails, there might be issues with your Hadoop configuration and you may need to use the PUT method instead by setting
import bodo
bodo.io.snowflake.SF_WRITE_UPLOAD_USING_PUT = True
before calling this function."""
                                ))
                    else:
                        ayd__apn = True
                        xlaaq__niuw = 'Detected Azure Stage. '
                        if not dalvl__hcugy:
                            xlaaq__niuw += """Required package bodo_azurefs_sas_token_provider is not installed. To use direct upload to stage in the future, install the package using: 'conda install bodo-azurefs-sas-token-provider -c bodo.ai -c conda-forge'.
"""
                        if not rjuo__igsou:
                            xlaaq__niuw += """You need to download and set up Hadoop. For more information, refer to our documentation: https://docs.bodo.ai/latest/file_io/?h=hdfs#HDFS.
"""
                        xlaaq__niuw += (
                            'Falling back to PUT command for upload for now.')
                        warnings.warn(BodoWarning(xlaaq__niuw))
                else:
                    ayd__apn = True
                    warnings.warn(BodoWarning(
                        f"Direct upload to stage is not supported for internal stage type '{usd__yie}'. Falling back to PUT command for upload."
                        ))
                if ayd__apn:
                    drop_internal_stage(cursor, stage_name)
                    stage_name = create_internal_stage(cursor, is_temporary
                        =False)
        except Exception as npq__hmkhl:
            dyev__kvbsi = RuntimeError(str(npq__hmkhl))
            if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
                print(''.join(traceback.format_exception(None, npq__hmkhl,
                    npq__hmkhl.__traceback__)))
    dyev__kvbsi = sith__befb.bcast(dyev__kvbsi)
    if isinstance(dyev__kvbsi, Exception):
        raise dyev__kvbsi
    mqmy__hitrp = sith__befb.bcast(mqmy__hitrp)
    azure_stage_direct_upload = mqmy__hitrp.startswith('abfs://')
    if mqmy__hitrp == '':
        sazw__tdr = True
        mqmy__hitrp = tmp_folder.name + '/'
        if tgc__qxtd != 0:
            conn = snowflake_connect(conn_str)
            cursor = conn.cursor()
    else:
        sazw__tdr = False
        zpq__cwgnh = sith__befb.bcast(zpq__cwgnh)
        old_creds = update_env_vars(zpq__cwgnh)
        if azure_stage_direct_upload:
            import bodo_azurefs_sas_token_provider
            bodo.HDFS_CORE_SITE_LOC_DIR.initialize()
            old_core_site = update_file_contents(bodo.HDFS_CORE_SITE_LOC,
                SF_AZURE_WRITE_HDFS_CORE_SITE)
            tmaze__jjq = sith__befb.bcast(tmaze__jjq)
            old_sas_token = update_file_contents(
                SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION, tmaze__jjq)
    stage_name = sith__befb.bcast(stage_name)
    qpn__bvyp.finalize()
    return (cursor, tmp_folder, stage_name, mqmy__hitrp, sazw__tdr,
        old_creds, azure_stage_direct_upload, old_core_site, old_sas_token)


def create_table_copy_into(cursor: 'SnowflakeCursor', stage_name: str,
    location: str, sf_schema, if_exists: str, old_creds, tmp_folder:
    TemporaryDirectory, azure_stage_direct_upload: bool, old_core_site: str,
    old_sas_token: str):
    qpn__bvyp = tracing.Event('create_table_copy_into', is_parallel=False)
    sith__befb = MPI.COMM_WORLD
    tgc__qxtd = sith__befb.Get_rank()
    dyev__kvbsi = None
    if tgc__qxtd == 0:
        try:
            cbg__izsjn = (
                'BEGIN /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(cbg__izsjn)
            create_table_handle_exists(cursor, stage_name, location,
                sf_schema, if_exists)
            hzfk__jeau, jmkq__ozmx, skjsm__hdq, mjboh__nyo = execute_copy_into(
                cursor, stage_name, location, sf_schema)
            if hzfk__jeau != jmkq__ozmx:
                raise BodoError(
                    f'Snowflake write copy_into failed: {mjboh__nyo}')
            jddr__cbq = (
                'COMMIT /* Python:bodo.io.snowflake.create_table_copy_into() */'
                )
            cursor.execute(jddr__cbq)
            drop_internal_stage(cursor, stage_name)
            cursor.close()
        except Exception as npq__hmkhl:
            dyev__kvbsi = RuntimeError(str(npq__hmkhl))
            if os.environ.get('BODO_SF_WRITE_DEBUG') is not None:
                print(''.join(traceback.format_exception(None, npq__hmkhl,
                    npq__hmkhl.__traceback__)))
    dyev__kvbsi = sith__befb.bcast(dyev__kvbsi)
    if isinstance(dyev__kvbsi, Exception):
        raise dyev__kvbsi
    update_env_vars(old_creds)
    tmp_folder.cleanup()
    if azure_stage_direct_upload:
        update_file_contents(bodo.HDFS_CORE_SITE_LOC, old_core_site)
        update_file_contents(SF_AZURE_WRITE_SAS_TOKEN_FILE_LOCATION,
            old_sas_token)
    qpn__bvyp.finalize()
