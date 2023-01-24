import os
import warnings
from collections import defaultdict
from glob import has_magic
from typing import Optional
from urllib.parse import urlparse
import llvmlite.binding as ll
import numba
import numpy as np
import pyarrow
import pyarrow as pa
import pyarrow.dataset as ds
from numba.core import types
from numba.extending import NativeValue, box, intrinsic, models, overload, register_model, unbox
from pyarrow._fs import PyFileSystem
from pyarrow.fs import FSSpecHandler
import bodo
import bodo.utils.tracing as tracing
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.io.fs_io import get_hdfs_fs, get_s3_fs_from_path
from bodo.io.helpers import _get_numba_typ_from_pa_typ
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.distributed_api import get_end, get_start
from bodo.utils.typing import BodoError, BodoWarning, FileInfo, FileSchema, get_overload_const_str
REMOTE_FILESYSTEMS = {'s3', 'gcs', 'gs', 'http', 'hdfs', 'abfs', 'abfss'}
READ_STR_AS_DICT_THRESHOLD = 1.0
list_of_files_error_msg = (
    '. Make sure the list/glob passed to read_parquet() only contains paths to files (no directories)'
    )


class ParquetPredicateType(types.Type):

    def __init__(self):
        super(ParquetPredicateType, self).__init__(name=
            'ParquetPredicateType()')


parquet_predicate_type = ParquetPredicateType()
types.parquet_predicate_type = parquet_predicate_type
register_model(ParquetPredicateType)(models.OpaqueModel)


@unbox(ParquetPredicateType)
def unbox_parquet_predicate_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(ParquetPredicateType)
def box_parquet_predicate_type(typ, val, c):
    c.pyapi.incref(val)
    return val


class ParquetFileInfo(FileInfo):

    def __init__(self, columns, storage_options=None, input_file_name_col=
        None, read_as_dict_cols=None, use_hive=True):
        self.columns = columns
        self.storage_options = storage_options
        self.input_file_name_col = input_file_name_col
        self.read_as_dict_cols = read_as_dict_cols
        self.use_hive = use_hive
        super().__init__()

    def _get_schema(self, fname):
        try:
            return parquet_file_schema(fname, selected_columns=self.columns,
                storage_options=self.storage_options, input_file_name_col=
                self.input_file_name_col, read_as_dict_cols=self.
                read_as_dict_cols, use_hive=self.use_hive)
        except OSError as ogkvy__uhu:
            if 'non-file path' in str(ogkvy__uhu):
                raise FileNotFoundError(str(ogkvy__uhu))
            raise


def get_filters_pyobject(dnf_filter_str, expr_filter_str, vars):
    pass


@overload(get_filters_pyobject, no_unliteral=True)
def overload_get_filters_pyobject(dnf_filter_str, expr_filter_str, var_tup):
    fvg__xiop = get_overload_const_str(dnf_filter_str)
    yya__oyd = get_overload_const_str(expr_filter_str)
    knr__bhjf = ', '.join(f'f{iiyev__zuj}' for iiyev__zuj in range(len(
        var_tup)))
    bkhj__urpnf = 'def impl(dnf_filter_str, expr_filter_str, var_tup):\n'
    if len(var_tup):
        bkhj__urpnf += f'  {knr__bhjf}, = var_tup\n'
    bkhj__urpnf += """  with numba.objmode(dnf_filters_py='parquet_predicate_type', expr_filters_py='parquet_predicate_type'):
"""
    bkhj__urpnf += f'    dnf_filters_py = {fvg__xiop}\n'
    bkhj__urpnf += f'    expr_filters_py = {yya__oyd}\n'
    bkhj__urpnf += '  return (dnf_filters_py, expr_filters_py)\n'
    zfzd__bqbrv = {}
    ukvn__nmpkb = globals()
    ukvn__nmpkb['numba'] = numba
    exec(bkhj__urpnf, ukvn__nmpkb, zfzd__bqbrv)
    return zfzd__bqbrv['impl']


def unify_schemas(schemas):
    iosk__yiqwl = []
    for schema in schemas:
        for iiyev__zuj in range(len(schema)):
            tmkm__tinhg = schema.field(iiyev__zuj)
            if tmkm__tinhg.type == pa.large_string():
                schema = schema.set(iiyev__zuj, tmkm__tinhg.with_type(pa.
                    string()))
            elif tmkm__tinhg.type == pa.large_binary():
                schema = schema.set(iiyev__zuj, tmkm__tinhg.with_type(pa.
                    binary()))
            elif isinstance(tmkm__tinhg.type, (pa.ListType, pa.LargeListType)
                ) and tmkm__tinhg.type.value_type in (pa.string(), pa.
                large_string()):
                schema = schema.set(iiyev__zuj, tmkm__tinhg.with_type(pa.
                    list_(pa.field(tmkm__tinhg.type.value_field.name, pa.
                    string()))))
            elif isinstance(tmkm__tinhg.type, pa.LargeListType):
                schema = schema.set(iiyev__zuj, tmkm__tinhg.with_type(pa.
                    list_(pa.field(tmkm__tinhg.type.value_field.name,
                    tmkm__tinhg.type.value_type))))
        iosk__yiqwl.append(schema)
    return pa.unify_schemas(iosk__yiqwl)


class ParquetDataset:

    def __init__(self, pa_pq_dataset, prefix=''):
        self.schema: pa.Schema = pa_pq_dataset.schema
        self.filesystem = None
        self._bodo_total_rows = 0
        self._prefix = prefix
        self.partitioning = None
        partitioning = pa_pq_dataset.partitioning
        self.partition_names = ([] if partitioning is None or partitioning.
            schema == pa_pq_dataset.schema else list(partitioning.schema.names)
            )
        if self.partition_names:
            self.partitioning_dictionaries = partitioning.dictionaries
            self.partitioning_cls = partitioning.__class__
            self.partitioning_schema = partitioning.schema
        else:
            self.partitioning_dictionaries = {}
        for iiyev__zuj in range(len(self.schema)):
            tmkm__tinhg = self.schema.field(iiyev__zuj)
            if tmkm__tinhg.type == pa.large_string():
                self.schema = self.schema.set(iiyev__zuj, tmkm__tinhg.
                    with_type(pa.string()))
        self.pieces = [ParquetPiece(frag, partitioning, self.
            partition_names) for frag in pa_pq_dataset._dataset.
            get_fragments(filter=pa_pq_dataset._filter_expression)]

    def set_fs(self, fs):
        self.filesystem = fs
        for uox__fpyvo in self.pieces:
            uox__fpyvo.filesystem = fs

    def __setstate__(self, state):
        self.__dict__ = state
        if self.partition_names:
            byucd__yohw = {uox__fpyvo: self.partitioning_dictionaries[
                iiyev__zuj] for iiyev__zuj, uox__fpyvo in enumerate(self.
                partition_names)}
            self.partitioning = self.partitioning_cls(self.
                partitioning_schema, byucd__yohw)


class ParquetPiece(object):

    def __init__(self, frag, partitioning, partition_names):
        self._frag = None
        self.format = frag.format
        self.path = frag.path
        self._bodo_num_rows = 0
        self.partition_keys = []
        if partitioning is not None:
            self.partition_keys = ds._get_partition_keys(frag.
                partition_expression)
            self.partition_keys = [(duy__kgph, partitioning.dictionaries[
                iiyev__zuj].index(self.partition_keys[duy__kgph]).as_py()) for
                iiyev__zuj, duy__kgph in enumerate(partition_names)]

    @property
    def frag(self):
        if self._frag is None:
            self._frag = self.format.make_fragment(self.path, self.filesystem)
            del self.format
        return self._frag

    @property
    def metadata(self):
        return self.frag.metadata

    @property
    def num_row_groups(self):
        return self.frag.num_row_groups


def get_parquet_dataset(fpath, get_row_counts: bool=True, dnf_filters=None,
    expr_filters=None, storage_options=None, read_categories: bool=False,
    is_parallel=False, tot_rows_to_read: Optional[int]=None,
    typing_pa_schema: Optional[pa.Schema]=None, use_hive: bool=True,
    partitioning='hive') ->ParquetDataset:
    if not use_hive:
        partitioning = None
    if get_row_counts:
        cvw__sfa = tracing.Event('get_parquet_dataset')
    import time
    import pyarrow as pa
    import pyarrow.parquet as pq
    from mpi4py import MPI
    glcbj__wxhr = MPI.COMM_WORLD
    if isinstance(fpath, list):
        kos__ejq = urlparse(fpath[0])
        protocol = kos__ejq.scheme
        dhoa__mxoq = kos__ejq.netloc
        for iiyev__zuj in range(len(fpath)):
            tmkm__tinhg = fpath[iiyev__zuj]
            vwfhw__fuh = urlparse(tmkm__tinhg)
            if vwfhw__fuh.scheme != protocol:
                raise BodoError(
                    'All parquet files must use the same filesystem protocol')
            if vwfhw__fuh.netloc != dhoa__mxoq:
                raise BodoError(
                    'All parquet files must be in the same S3 bucket')
            fpath[iiyev__zuj] = tmkm__tinhg.rstrip('/')
    else:
        kos__ejq = urlparse(fpath)
        protocol = kos__ejq.scheme
        fpath = fpath.rstrip('/')
    if protocol in {'gcs', 'gs'}:
        try:
            import gcsfs
        except ImportError as xpzk__adf:
            rnqv__xqvuo = """Couldn't import gcsfs, which is required for Google cloud access. gcsfs can be installed by calling 'conda install -c conda-forge gcsfs'.
"""
            raise BodoError(rnqv__xqvuo)
    if protocol == 'http':
        try:
            import fsspec
        except ImportError as xpzk__adf:
            rnqv__xqvuo = """Couldn't import fsspec, which is required for http access. fsspec can be installed by calling 'conda install -c conda-forge fsspec'.
"""
    fs = []

    def getfs(parallel=False):
        if len(fs) == 1:
            return fs[0]
        if protocol == 's3':
            fs.append(get_s3_fs_from_path(fpath, parallel=parallel,
                storage_options=storage_options) if not isinstance(fpath,
                list) else get_s3_fs_from_path(fpath[0], parallel=parallel,
                storage_options=storage_options))
        elif protocol in {'gcs', 'gs'}:
            pqd__tzzev = gcsfs.GCSFileSystem(token=None)
            fs.append(PyFileSystem(FSSpecHandler(pqd__tzzev)))
        elif protocol == 'http':
            fs.append(PyFileSystem(FSSpecHandler(fsspec.filesystem('http'))))
        elif protocol in {'hdfs', 'abfs', 'abfss'}:
            fs.append(get_hdfs_fs(fpath) if not isinstance(fpath, list) else
                get_hdfs_fs(fpath[0]))
        else:
            fs.append(pa.fs.LocalFileSystem())
        return fs[0]

    def glob(protocol, fs, path):
        if not protocol and fs is None:
            from fsspec.implementations.local import LocalFileSystem
            fs = LocalFileSystem()
        if isinstance(fs, pa.fs.FileSystem):
            from fsspec.implementations.arrow import ArrowFSWrapper
            fs = ArrowFSWrapper(fs)
        try:
            fmuom__pbzlr = fs.glob(path)
        except:
            raise BodoError(
                f'glob pattern expansion not supported for {protocol}')
        if len(fmuom__pbzlr) == 0:
            raise BodoError('No files found matching glob pattern')
        return fmuom__pbzlr
    qfnb__foetg = False
    if get_row_counts:
        qyqbk__ctnj = getfs(parallel=True)
        qfnb__foetg = bodo.parquet_validate_schema
    if bodo.get_rank() == 0:
        mbqpj__wmf = 1
        ilbm__lprf = os.cpu_count()
        if ilbm__lprf is not None and ilbm__lprf > 1:
            mbqpj__wmf = ilbm__lprf // 2
        try:
            if get_row_counts:
                nmbw__hzw = tracing.Event('pq.ParquetDataset', is_parallel=
                    False)
                if tracing.is_tracing():
                    nmbw__hzw.add_attribute('g_dnf_filter', str(dnf_filters))
            fydk__dmzen = pa.io_thread_count()
            pa.set_io_thread_count(mbqpj__wmf)
            prefix = ''
            if protocol == 's3':
                prefix = 's3://'
            elif protocol in {'hdfs', 'abfs', 'abfss'}:
                prefix = f'{protocol}://{kos__ejq.netloc}'
            if prefix:
                if isinstance(fpath, list):
                    btnrj__pku = [tmkm__tinhg[len(prefix):] for tmkm__tinhg in
                        fpath]
                else:
                    btnrj__pku = fpath[len(prefix):]
            else:
                btnrj__pku = fpath
            if isinstance(btnrj__pku, list):
                mnk__ekq = []
                for uox__fpyvo in btnrj__pku:
                    if has_magic(uox__fpyvo):
                        mnk__ekq += glob(protocol, getfs(), uox__fpyvo)
                    else:
                        mnk__ekq.append(uox__fpyvo)
                btnrj__pku = mnk__ekq
            elif has_magic(btnrj__pku):
                btnrj__pku = glob(protocol, getfs(), btnrj__pku)
            sdhe__icxpn = pq.ParquetDataset(btnrj__pku, filesystem=getfs(),
                filters=None, use_legacy_dataset=False, partitioning=
                partitioning)
            if dnf_filters is not None:
                sdhe__icxpn._filters = dnf_filters
                sdhe__icxpn._filter_expression = pq._filters_to_expression(
                    dnf_filters)
            gin__fommz = len(sdhe__icxpn.files)
            sdhe__icxpn = ParquetDataset(sdhe__icxpn, prefix)
            pa.set_io_thread_count(fydk__dmzen)
            if typing_pa_schema:
                sdhe__icxpn.schema = typing_pa_schema
            if get_row_counts:
                if dnf_filters is not None:
                    nmbw__hzw.add_attribute('num_pieces_before_filter',
                        gin__fommz)
                    nmbw__hzw.add_attribute('num_pieces_after_filter', len(
                        sdhe__icxpn.pieces))
                nmbw__hzw.finalize()
        except Exception as ogkvy__uhu:
            if isinstance(ogkvy__uhu, IsADirectoryError):
                ogkvy__uhu = BodoError(list_of_files_error_msg)
            elif isinstance(fpath, list) and isinstance(ogkvy__uhu, (
                OSError, FileNotFoundError)):
                ogkvy__uhu = BodoError(str(ogkvy__uhu) +
                    list_of_files_error_msg)
            else:
                ogkvy__uhu = BodoError(
                    f"""error from pyarrow: {type(ogkvy__uhu).__name__}: {str(ogkvy__uhu)}
"""
                    )
            glcbj__wxhr.bcast(ogkvy__uhu)
            raise ogkvy__uhu
        if get_row_counts:
            hdcp__ici = tracing.Event('bcast dataset')
        sdhe__icxpn = glcbj__wxhr.bcast(sdhe__icxpn)
    else:
        if get_row_counts:
            hdcp__ici = tracing.Event('bcast dataset')
        sdhe__icxpn = glcbj__wxhr.bcast(None)
        if isinstance(sdhe__icxpn, Exception):
            zkpq__oagto = sdhe__icxpn
            raise zkpq__oagto
    sdhe__icxpn.set_fs(getfs())
    if get_row_counts:
        hdcp__ici.finalize()
    if get_row_counts and tot_rows_to_read == 0:
        get_row_counts = qfnb__foetg = False
    if get_row_counts or qfnb__foetg:
        if get_row_counts and tracing.is_tracing():
            jxb__gom = tracing.Event('get_row_counts')
            jxb__gom.add_attribute('g_num_pieces', len(sdhe__icxpn.pieces))
            jxb__gom.add_attribute('g_expr_filters', str(expr_filters))
        negm__msuz = 0.0
        num_pieces = len(sdhe__icxpn.pieces)
        start = get_start(num_pieces, bodo.get_size(), bodo.get_rank())
        deqrf__zrhz = get_end(num_pieces, bodo.get_size(), bodo.get_rank())
        hmbmv__saoe = 0
        aqrcl__oepn = 0
        occ__qgto = 0
        ttarf__efgd = True
        if expr_filters is not None:
            import random
            random.seed(37)
            vao__hgwuk = random.sample(sdhe__icxpn.pieces, k=len(
                sdhe__icxpn.pieces))
        else:
            vao__hgwuk = sdhe__icxpn.pieces
        fpaths = [uox__fpyvo.path for uox__fpyvo in vao__hgwuk[start:
            deqrf__zrhz]]
        mbqpj__wmf = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)), 4)
        pa.set_io_thread_count(mbqpj__wmf)
        pa.set_cpu_count(mbqpj__wmf)
        zkpq__oagto = None
        try:
            xxqs__vfz = ds.dataset(fpaths, filesystem=sdhe__icxpn.
                filesystem, partitioning=sdhe__icxpn.partitioning)
            for lzlq__bkhd, frag in zip(vao__hgwuk[start:deqrf__zrhz],
                xxqs__vfz.get_fragments()):
                if qfnb__foetg:
                    dctd__qxsq = frag.metadata.schema.to_arrow_schema()
                    djjo__yqi = set(dctd__qxsq.names)
                    dmd__udqz = set(sdhe__icxpn.schema.names) - set(sdhe__icxpn
                        .partition_names)
                    if dmd__udqz != djjo__yqi:
                        iio__usu = djjo__yqi - dmd__udqz
                        xmhea__epvc = dmd__udqz - djjo__yqi
                        wcvq__gdazq = (
                            f'Schema in {lzlq__bkhd} was different.\n')
                        if typing_pa_schema is not None:
                            if iio__usu:
                                wcvq__gdazq += f"""File contains column(s) {iio__usu} not found in other files in the dataset.
"""
                                raise BodoError(wcvq__gdazq)
                        else:
                            if iio__usu:
                                wcvq__gdazq += f"""File contains column(s) {iio__usu} not found in other files in the dataset.
"""
                            if xmhea__epvc:
                                wcvq__gdazq += f"""File missing column(s) {xmhea__epvc} found in other files in the dataset.
"""
                            raise BodoError(wcvq__gdazq)
                    try:
                        sdhe__icxpn.schema = unify_schemas([sdhe__icxpn.
                            schema, dctd__qxsq])
                    except Exception as ogkvy__uhu:
                        wcvq__gdazq = (
                            f'Schema in {lzlq__bkhd} was different.\n' +
                            str(ogkvy__uhu))
                        raise BodoError(wcvq__gdazq)
                udib__xggz = time.time()
                qsubg__vtvui = frag.scanner(schema=xxqs__vfz.schema, filter
                    =expr_filters, use_threads=True).count_rows()
                negm__msuz += time.time() - udib__xggz
                lzlq__bkhd._bodo_num_rows = qsubg__vtvui
                hmbmv__saoe += qsubg__vtvui
                aqrcl__oepn += frag.num_row_groups
                occ__qgto += sum(jng__pvtz.total_byte_size for jng__pvtz in
                    frag.row_groups)
        except Exception as ogkvy__uhu:
            zkpq__oagto = ogkvy__uhu
        if glcbj__wxhr.allreduce(zkpq__oagto is not None, op=MPI.LOR):
            for zkpq__oagto in glcbj__wxhr.allgather(zkpq__oagto):
                if zkpq__oagto:
                    if isinstance(fpath, list) and isinstance(zkpq__oagto,
                        (OSError, FileNotFoundError)):
                        raise BodoError(str(zkpq__oagto) +
                            list_of_files_error_msg)
                    raise zkpq__oagto
        if qfnb__foetg:
            ttarf__efgd = glcbj__wxhr.allreduce(ttarf__efgd, op=MPI.LAND)
            if not ttarf__efgd:
                raise BodoError("Schema in parquet files don't match")
        if get_row_counts:
            sdhe__icxpn._bodo_total_rows = glcbj__wxhr.allreduce(hmbmv__saoe,
                op=MPI.SUM)
            hrcvy__ihk = glcbj__wxhr.allreduce(aqrcl__oepn, op=MPI.SUM)
            mfxk__qlwvd = glcbj__wxhr.allreduce(occ__qgto, op=MPI.SUM)
            oskj__lfp = np.array([uox__fpyvo._bodo_num_rows for uox__fpyvo in
                sdhe__icxpn.pieces])
            oskj__lfp = glcbj__wxhr.allreduce(oskj__lfp, op=MPI.SUM)
            for uox__fpyvo, jpng__fcofd in zip(sdhe__icxpn.pieces, oskj__lfp):
                uox__fpyvo._bodo_num_rows = jpng__fcofd
            if is_parallel and bodo.get_rank(
                ) == 0 and hrcvy__ihk < bodo.get_size() and hrcvy__ihk != 0:
                warnings.warn(BodoWarning(
                    f"""Total number of row groups in parquet dataset {fpath} ({hrcvy__ihk}) is too small for effective IO parallelization.
For best performance the number of row groups should be greater than the number of workers ({bodo.get_size()}). For more details, refer to
https://docs.bodo.ai/latest/file_io/#parquet-section.
"""
                    ))
            if hrcvy__ihk == 0:
                inkf__rifq = 0
            else:
                inkf__rifq = mfxk__qlwvd // hrcvy__ihk
            if (bodo.get_rank() == 0 and mfxk__qlwvd >= 20 * 1048576 and 
                inkf__rifq < 1048576 and protocol in REMOTE_FILESYSTEMS):
                warnings.warn(BodoWarning(
                    f'Parquet average row group size is small ({inkf__rifq} bytes) and can have negative impact on performance when reading from remote sources'
                    ))
            if tracing.is_tracing():
                jxb__gom.add_attribute('g_total_num_row_groups', hrcvy__ihk)
                jxb__gom.add_attribute('total_scan_time', negm__msuz)
                pon__avjsv = np.array([uox__fpyvo._bodo_num_rows for
                    uox__fpyvo in sdhe__icxpn.pieces])
                jclb__qjluw = np.percentile(pon__avjsv, [25, 50, 75])
                jxb__gom.add_attribute('g_row_counts_min', pon__avjsv.min())
                jxb__gom.add_attribute('g_row_counts_Q1', jclb__qjluw[0])
                jxb__gom.add_attribute('g_row_counts_median', jclb__qjluw[1])
                jxb__gom.add_attribute('g_row_counts_Q3', jclb__qjluw[2])
                jxb__gom.add_attribute('g_row_counts_max', pon__avjsv.max())
                jxb__gom.add_attribute('g_row_counts_mean', pon__avjsv.mean())
                jxb__gom.add_attribute('g_row_counts_std', pon__avjsv.std())
                jxb__gom.add_attribute('g_row_counts_sum', pon__avjsv.sum())
                jxb__gom.finalize()
    if read_categories:
        _add_categories_to_pq_dataset(sdhe__icxpn)
    if get_row_counts:
        cvw__sfa.finalize()
    if qfnb__foetg:
        if tracing.is_tracing():
            tima__wswpk = tracing.Event('unify_schemas_across_ranks')
        zkpq__oagto = None
        try:
            sdhe__icxpn.schema = glcbj__wxhr.allreduce(sdhe__icxpn.schema,
                bodo.io.helpers.pa_schema_unify_mpi_op)
        except Exception as ogkvy__uhu:
            zkpq__oagto = ogkvy__uhu
        if tracing.is_tracing():
            tima__wswpk.finalize()
        if glcbj__wxhr.allreduce(zkpq__oagto is not None, op=MPI.LOR):
            for zkpq__oagto in glcbj__wxhr.allgather(zkpq__oagto):
                if zkpq__oagto:
                    wcvq__gdazq = (
                        f'Schema in some files were different.\n' + str(
                        zkpq__oagto))
                    raise BodoError(wcvq__gdazq)
    return sdhe__icxpn


def get_scanner_batches(fpaths, expr_filters, selected_fields,
    avg_num_pieces, is_parallel, filesystem, str_as_dict_cols, start_offset,
    rows_to_read, partitioning, schema):
    import pyarrow as pa
    ilbm__lprf = os.cpu_count()
    if ilbm__lprf is None or ilbm__lprf == 0:
        ilbm__lprf = 2
    hjpud__ayaay = min(int(os.environ.get('BODO_MIN_IO_THREADS', 4)),
        ilbm__lprf)
    qfak__ieu = min(int(os.environ.get('BODO_MAX_IO_THREADS', 16)), ilbm__lprf)
    if is_parallel and len(fpaths) > qfak__ieu and len(fpaths
        ) / avg_num_pieces >= 2.0:
        pa.set_io_thread_count(qfak__ieu)
        pa.set_cpu_count(qfak__ieu)
    else:
        pa.set_io_thread_count(hjpud__ayaay)
        pa.set_cpu_count(hjpud__ayaay)
    nainn__nfc = ds.ParquetFileFormat(dictionary_columns=str_as_dict_cols)
    uik__slscw = set(str_as_dict_cols)
    for iiyev__zuj, name in enumerate(schema.names):
        if name in uik__slscw:
            cvtap__iro = schema.field(iiyev__zuj)
            dtr__zqm = pa.field(name, pa.dictionary(pa.int32(), cvtap__iro.
                type), cvtap__iro.nullable)
            schema = schema.remove(iiyev__zuj).insert(iiyev__zuj, dtr__zqm)
    sdhe__icxpn = ds.dataset(fpaths, filesystem=filesystem, partitioning=
        partitioning, schema=schema, format=nainn__nfc)
    mbxh__jeg = sdhe__icxpn.schema.names
    hmwxo__adixw = [mbxh__jeg[kpocs__qzj] for kpocs__qzj in selected_fields]
    myjr__bqg = len(fpaths) <= 3 or start_offset > 0 and len(fpaths) <= 10
    if myjr__bqg and expr_filters is None:
        mlmkg__wcx = []
        efcq__jubda = 0
        kmniq__puupg = 0
        for frag in sdhe__icxpn.get_fragments():
            kgoi__wrc = []
            for jng__pvtz in frag.row_groups:
                nsk__clb = jng__pvtz.num_rows
                if start_offset < efcq__jubda + nsk__clb:
                    if kmniq__puupg == 0:
                        xgj__vppnm = start_offset - efcq__jubda
                        nazr__tml = min(nsk__clb - xgj__vppnm, rows_to_read)
                    else:
                        nazr__tml = min(nsk__clb, rows_to_read - kmniq__puupg)
                    kmniq__puupg += nazr__tml
                    kgoi__wrc.append(jng__pvtz.id)
                efcq__jubda += nsk__clb
                if kmniq__puupg == rows_to_read:
                    break
            mlmkg__wcx.append(frag.subset(row_group_ids=kgoi__wrc))
            if kmniq__puupg == rows_to_read:
                break
        sdhe__icxpn = ds.FileSystemDataset(mlmkg__wcx, sdhe__icxpn.schema,
            nainn__nfc, filesystem=sdhe__icxpn.filesystem)
        start_offset = xgj__vppnm
    rphp__pbg = sdhe__icxpn.scanner(columns=hmwxo__adixw, filter=
        expr_filters, use_threads=True).to_reader()
    return sdhe__icxpn, rphp__pbg, start_offset


def _add_categories_to_pq_dataset(pq_dataset):
    import pyarrow as pa
    from mpi4py import MPI
    if len(pq_dataset.pieces) < 1:
        raise BodoError(
            'No pieces found in Parquet dataset. Cannot get read categorical values'
            )
    pa_schema = pq_dataset.schema
    zvxc__kix = [c for c in pa_schema.names if isinstance(pa_schema.field(c
        ).type, pa.DictionaryType) and c not in pq_dataset.partition_names]
    if len(zvxc__kix) == 0:
        pq_dataset._category_info = {}
        return
    glcbj__wxhr = MPI.COMM_WORLD
    if bodo.get_rank() == 0:
        try:
            dit__hvp = pq_dataset.pieces[0].frag.head(100, columns=zvxc__kix)
            psks__xcu = {c: tuple(dit__hvp.column(c).chunk(0).dictionary.
                to_pylist()) for c in zvxc__kix}
            del dit__hvp
        except Exception as ogkvy__uhu:
            glcbj__wxhr.bcast(ogkvy__uhu)
            raise ogkvy__uhu
        glcbj__wxhr.bcast(psks__xcu)
    else:
        psks__xcu = glcbj__wxhr.bcast(None)
        if isinstance(psks__xcu, Exception):
            zkpq__oagto = psks__xcu
            raise zkpq__oagto
    pq_dataset._category_info = psks__xcu


def get_pandas_metadata(schema, num_pieces):
    joj__mdrg = None
    ekm__zbnu = defaultdict(lambda : None)
    tzxnv__gumf = b'pandas'
    if schema.metadata is not None and tzxnv__gumf in schema.metadata:
        import json
        kdb__ceik = json.loads(schema.metadata[tzxnv__gumf].decode('utf8'))
        qjrgg__gxivu = len(kdb__ceik['index_columns'])
        if qjrgg__gxivu > 1:
            raise BodoError('read_parquet: MultiIndex not supported yet')
        joj__mdrg = kdb__ceik['index_columns'][0] if qjrgg__gxivu else None
        if not isinstance(joj__mdrg, str) and not isinstance(joj__mdrg, dict):
            joj__mdrg = None
        for sdq__gqm in kdb__ceik['columns']:
            sgd__qdlfr = sdq__gqm['name']
            kyc__ndla = sdq__gqm['pandas_type']
            if (kyc__ndla.startswith('int') or kyc__ndla.startswith('float')
                ) and sgd__qdlfr is not None:
                nmjz__srcfa = sdq__gqm['numpy_type']
                if nmjz__srcfa.startswith('Int') or nmjz__srcfa.startswith(
                    'Float'):
                    ekm__zbnu[sgd__qdlfr] = True
                else:
                    ekm__zbnu[sgd__qdlfr] = False
    return joj__mdrg, ekm__zbnu


def get_str_columns_from_pa_schema(pa_schema):
    str_columns = []
    for sgd__qdlfr in pa_schema.names:
        mhcw__gpr = pa_schema.field(sgd__qdlfr)
        if mhcw__gpr.type in (pa.string(), pa.large_string()):
            str_columns.append(sgd__qdlfr)
    return str_columns


def _pa_schemas_match(pa_schema1, pa_schema2):
    if pa_schema1.names != pa_schema2.names:
        return False
    try:
        unify_schemas([pa_schema1, pa_schema2])
    except:
        return False
    return True


def _get_sample_pq_pieces(pq_dataset, pa_schema, is_iceberg):
    vao__hgwuk = pq_dataset.pieces
    if len(vao__hgwuk) > bodo.get_size():
        import random
        random.seed(37)
        vao__hgwuk = random.sample(vao__hgwuk, bodo.get_size())
    else:
        vao__hgwuk = vao__hgwuk
    if is_iceberg:
        vao__hgwuk = [uox__fpyvo for uox__fpyvo in vao__hgwuk if
            _pa_schemas_match(uox__fpyvo.metadata.schema.to_arrow_schema(),
            pa_schema)]
    return vao__hgwuk


def determine_str_as_dict_columns(pq_dataset, pa_schema, str_columns: list,
    is_iceberg: bool=False) ->set:
    from mpi4py import MPI
    glcbj__wxhr = MPI.COMM_WORLD
    if len(str_columns) == 0:
        return set()
    vao__hgwuk = _get_sample_pq_pieces(pq_dataset, pa_schema, is_iceberg)
    str_columns = sorted(str_columns)
    ydh__acni = np.zeros(len(str_columns), dtype=np.int64)
    bjwd__xwadl = np.zeros(len(str_columns), dtype=np.int64)
    if bodo.get_rank() < len(vao__hgwuk):
        lzlq__bkhd = vao__hgwuk[bodo.get_rank()]
        try:
            metadata = lzlq__bkhd.metadata
            for iiyev__zuj in range(lzlq__bkhd.num_row_groups):
                for aeqtk__bmli, sgd__qdlfr in enumerate(str_columns):
                    frw__wtve = pa_schema.get_field_index(sgd__qdlfr)
                    ydh__acni[aeqtk__bmli] += metadata.row_group(iiyev__zuj
                        ).column(frw__wtve).total_uncompressed_size
            vyzoo__nqdx = metadata.num_rows
        except Exception as ogkvy__uhu:
            if isinstance(ogkvy__uhu, (OSError, FileNotFoundError)):
                vyzoo__nqdx = 0
            else:
                raise
    else:
        vyzoo__nqdx = 0
    pvdbz__ldn = glcbj__wxhr.allreduce(vyzoo__nqdx, op=MPI.SUM)
    if pvdbz__ldn == 0:
        return set()
    glcbj__wxhr.Allreduce(ydh__acni, bjwd__xwadl, op=MPI.SUM)
    dnd__ybop = bjwd__xwadl / pvdbz__ldn
    dhepb__qntyz = set()
    for iiyev__zuj, ofm__brt in enumerate(dnd__ybop):
        if ofm__brt < READ_STR_AS_DICT_THRESHOLD:
            sgd__qdlfr = str_columns[iiyev__zuj]
            dhepb__qntyz.add(sgd__qdlfr)
    return dhepb__qntyz


def parquet_file_schema(file_name, selected_columns, storage_options=None,
    input_file_name_col=None, read_as_dict_cols=None, use_hive=True
    ) ->FileSchema:
    mbxh__jeg = []
    rag__eqvye = []
    pq_dataset = get_parquet_dataset(file_name, get_row_counts=False,
        storage_options=storage_options, read_categories=True, use_hive=
        use_hive)
    partition_names = pq_dataset.partition_names
    pa_schema = pq_dataset.schema
    num_pieces = len(pq_dataset.pieces)
    str_columns = get_str_columns_from_pa_schema(pa_schema)
    lpz__ktanh = set(str_columns)
    if read_as_dict_cols is None:
        read_as_dict_cols = []
    read_as_dict_cols = set(read_as_dict_cols)
    rtwkp__hmh = read_as_dict_cols - lpz__ktanh
    if len(rtwkp__hmh) > 0:
        if bodo.get_rank() == 0:
            warnings.warn(
                f'The following columns are not of datatype string and hence cannot be read with dictionary encoding: {rtwkp__hmh}'
                , bodo.utils.typing.BodoWarning)
    read_as_dict_cols.intersection_update(lpz__ktanh)
    lpz__ktanh = lpz__ktanh - read_as_dict_cols
    str_columns = [ajn__eftv for ajn__eftv in str_columns if ajn__eftv in
        lpz__ktanh]
    dhepb__qntyz = determine_str_as_dict_columns(pq_dataset, pa_schema,
        str_columns)
    dhepb__qntyz.update(read_as_dict_cols)
    mbxh__jeg = pa_schema.names
    joj__mdrg, ekm__zbnu = get_pandas_metadata(pa_schema, num_pieces)
    brfu__mxr = []
    bnvv__emrmu = []
    ytyh__itac = []
    for iiyev__zuj, c in enumerate(mbxh__jeg):
        if c in partition_names:
            continue
        mhcw__gpr = pa_schema.field(c)
        pgzy__rkl, psk__curn = _get_numba_typ_from_pa_typ(mhcw__gpr, c ==
            joj__mdrg, ekm__zbnu[c], pq_dataset._category_info, str_as_dict
            =c in dhepb__qntyz)
        brfu__mxr.append(pgzy__rkl)
        bnvv__emrmu.append(psk__curn)
        ytyh__itac.append(mhcw__gpr.type)
    if partition_names:
        brfu__mxr += [_get_partition_cat_dtype(pq_dataset.
            partitioning_dictionaries[iiyev__zuj]) for iiyev__zuj in range(
            len(partition_names))]
        bnvv__emrmu.extend([True] * len(partition_names))
        ytyh__itac.extend([None] * len(partition_names))
    if input_file_name_col is not None:
        mbxh__jeg += [input_file_name_col]
        brfu__mxr += [dict_str_arr_type]
        bnvv__emrmu.append(True)
        ytyh__itac.append(None)
    gxdkg__lmhvs = {c: iiyev__zuj for iiyev__zuj, c in enumerate(mbxh__jeg)}
    if selected_columns is None:
        selected_columns = mbxh__jeg
    for c in selected_columns:
        if c not in gxdkg__lmhvs:
            raise BodoError(f'Selected column {c} not in Parquet file schema')
    if joj__mdrg and not isinstance(joj__mdrg, dict
        ) and joj__mdrg not in selected_columns:
        selected_columns.append(joj__mdrg)
    mbxh__jeg = selected_columns
    laxyt__ofyq = []
    rag__eqvye = []
    hfpp__vmmo = []
    ykinv__klvu = []
    for iiyev__zuj, c in enumerate(mbxh__jeg):
        uptht__iqrzj = gxdkg__lmhvs[c]
        laxyt__ofyq.append(uptht__iqrzj)
        rag__eqvye.append(brfu__mxr[uptht__iqrzj])
        if not bnvv__emrmu[uptht__iqrzj]:
            hfpp__vmmo.append(iiyev__zuj)
            ykinv__klvu.append(ytyh__itac[uptht__iqrzj])
    return (mbxh__jeg, rag__eqvye, joj__mdrg, laxyt__ofyq, partition_names,
        hfpp__vmmo, ykinv__klvu, pa_schema)


def _get_partition_cat_dtype(dictionary):
    assert dictionary is not None
    fjsm__umvvr = dictionary.to_pandas()
    him__pdff = bodo.typeof(fjsm__umvvr).dtype
    if isinstance(him__pdff, types.Integer):
        kij__qub = PDCategoricalDtype(tuple(fjsm__umvvr), him__pdff, False,
            int_type=him__pdff)
    else:
        kij__qub = PDCategoricalDtype(tuple(fjsm__umvvr), him__pdff, False)
    return CategoricalArrayType(kij__qub)


from llvmlite import ir as lir
from numba.core import cgutils
if bodo.utils.utils.has_pyarrow():
    from bodo.io import arrow_cpp
    ll.add_symbol('pq_write', arrow_cpp.pq_write)
    ll.add_symbol('pq_write_partitioned', arrow_cpp.pq_write_partitioned)


@intrinsic
def parquet_write_table_cpp(typingctx, filename_t, table_t, col_names_t,
    index_t, write_index, metadata_t, compression_t, is_parallel_t,
    write_range_index, start, stop, step, name, bucket_region,
    row_group_size, file_prefix, convert_timedelta_to_int64, timestamp_tz,
    downcast_time_ns_to_us):

    def codegen(context, builder, sig, args):
        wxo__omkh = lir.FunctionType(lir.IntType(64), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(32), lir.IntType(32),
            lir.IntType(32), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(1), lir.IntType(8).as_pointer(), lir.IntType(1)])
        mmuql__gjone = cgutils.get_or_insert_function(builder.module,
            wxo__omkh, name='pq_write')
        kdci__gct = builder.call(mmuql__gjone, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return kdci__gct
    return types.int64(types.voidptr, table_t, col_names_t, index_t, types.
        boolean, types.voidptr, types.voidptr, types.boolean, types.boolean,
        types.int32, types.int32, types.int32, types.voidptr, types.voidptr,
        types.int64, types.voidptr, types.boolean, types.voidptr, types.boolean
        ), codegen


@intrinsic
def parquet_write_table_partitioned_cpp(typingctx, filename_t, data_table_t,
    col_names_t, col_names_no_partitions_t, cat_table_t, part_col_idxs_t,
    num_part_col_t, compression_t, is_parallel_t, bucket_region,
    row_group_size, file_prefix, timestamp_tz):

    def codegen(context, builder, sig, args):
        wxo__omkh = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32), lir
            .IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        mmuql__gjone = cgutils.get_or_insert_function(builder.module,
            wxo__omkh, name='pq_write_partitioned')
        builder.call(mmuql__gjone, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
    return types.void(types.voidptr, data_table_t, col_names_t,
        col_names_no_partitions_t, cat_table_t, types.voidptr, types.int32,
        types.voidptr, types.boolean, types.voidptr, types.int64, types.
        voidptr, types.voidptr), codegen
