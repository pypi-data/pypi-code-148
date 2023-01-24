"""
S3 & Hadoop file system supports, and file system dependent calls
"""
import glob
import os
import warnings
from urllib.parse import urlparse
import llvmlite.binding as ll
import numba
import numpy as np
from fsspec.implementations.arrow import ArrowFile, ArrowFSWrapper, wrap_exceptions
from numba.core import types
from numba.extending import NativeValue, models, overload, register_model, unbox
import bodo
from bodo.io import csv_cpp
from bodo.libs.distributed_api import Reduce_Type
from bodo.libs.str_ext import unicode_to_utf8, unicode_to_utf8_and_len
from bodo.utils.typing import BodoError, BodoWarning, get_overload_constant_dict
from bodo.utils.utils import check_java_installation


def fsspec_arrowfswrapper__open(self, path, mode='rb', block_size=None, **
    kwargs):
    if mode == 'rb':
        try:
            clo__gejxa = self.fs.open_input_file(path)
        except:
            clo__gejxa = self.fs.open_input_stream(path)
    elif mode == 'wb':
        clo__gejxa = self.fs.open_output_stream(path)
    else:
        raise ValueError(f'unsupported mode for Arrow filesystem: {mode!r}')
    return ArrowFile(self, clo__gejxa, path, mode, block_size, **kwargs)


ArrowFSWrapper._open = wrap_exceptions(fsspec_arrowfswrapper__open)
_csv_write = types.ExternalFunction('csv_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.voidptr,
    types.voidptr))
ll.add_symbol('csv_write', csv_cpp.csv_write)
bodo_error_msg = """
    Some possible causes:
        (1) Incorrect path: Specified file/directory doesn't exist or is unreachable.
        (2) Missing credentials: You haven't provided S3 credentials, neither through 
            environment variables, nor through a local AWS setup 
            that makes the credentials available at ~/.aws/credentials.
        (3) Incorrect credentials: Your S3 credentials are incorrect or do not have
            the correct permissions.
        (4) Wrong bucket region is used. Set AWS_DEFAULT_REGION variable with correct bucket region.
    """


def get_proxy_uri_from_env_vars():
    return os.environ.get('http_proxy', None) or os.environ.get('https_proxy',
        None) or os.environ.get('HTTP_PROXY', None) or os.environ.get(
        'HTTPS_PROXY', None)


def get_s3_fs(region=None, storage_options=None):
    from pyarrow.fs import S3FileSystem
    wzs__utsn = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    mjhx__mnl = False
    fsb__xxmo = get_proxy_uri_from_env_vars()
    if storage_options:
        mjhx__mnl = storage_options.get('anon', False)
    return S3FileSystem(anonymous=mjhx__mnl, region=region,
        endpoint_override=wzs__utsn, proxy_options=fsb__xxmo)


def get_s3_subtree_fs(bucket_name, region=None, storage_options=None):
    from pyarrow._fs import SubTreeFileSystem
    from pyarrow._s3fs import S3FileSystem
    wzs__utsn = os.environ.get('AWS_S3_ENDPOINT', None)
    if not region:
        region = os.environ.get('AWS_DEFAULT_REGION', None)
    mjhx__mnl = False
    fsb__xxmo = get_proxy_uri_from_env_vars()
    if storage_options:
        mjhx__mnl = storage_options.get('anon', False)
    fs = S3FileSystem(region=region, endpoint_override=wzs__utsn, anonymous
        =mjhx__mnl, proxy_options=fsb__xxmo)
    return SubTreeFileSystem(bucket_name, fs)


def get_s3_fs_from_path(path, parallel=False, storage_options=None):
    region = get_s3_bucket_region_njit(path, parallel=parallel)
    if region == '':
        region = None
    return get_s3_fs(region, storage_options)


def get_hdfs_fs(path):
    from pyarrow.fs import HadoopFileSystem as HdFS
    wfgsm__cmsd = urlparse(path)
    if wfgsm__cmsd.scheme in ('abfs', 'abfss'):
        wts__jtily = path
        if wfgsm__cmsd.port is None:
            axn__opln = 0
        else:
            axn__opln = wfgsm__cmsd.port
        wxhs__sdtn = None
    else:
        wts__jtily = wfgsm__cmsd.hostname
        axn__opln = wfgsm__cmsd.port
        wxhs__sdtn = wfgsm__cmsd.username
    try:
        fs = HdFS(host=wts__jtily, port=axn__opln, user=wxhs__sdtn)
    except Exception as gte__idpc:
        raise BodoError('Hadoop file system cannot be created: {}'.format(
            gte__idpc))
    return fs


def gcs_is_directory(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    try:
        kwed__zfqdv = fs.isdir(path)
    except gcsfs.utils.HttpError as gte__idpc:
        raise BodoError(
            f'{gte__idpc}. Make sure your google cloud credentials are set!')
    return kwed__zfqdv


def gcs_list_dir_fnames(path):
    import gcsfs
    fs = gcsfs.GCSFileSystem(token=None)
    return [vmren__yhze.split('/')[-1] for vmren__yhze in fs.ls(path)]


def s3_is_directory(fs, path):
    from pyarrow import fs as pa_fs
    try:
        wfgsm__cmsd = urlparse(path)
        fhjx__jsz = (wfgsm__cmsd.netloc + wfgsm__cmsd.path).rstrip('/')
        sxvoi__vho = fs.get_file_info(fhjx__jsz)
        if sxvoi__vho.type in (pa_fs.FileType.NotFound, pa_fs.FileType.Unknown
            ):
            raise FileNotFoundError('{} is a non-existing or unreachable file'
                .format(path))
        if not sxvoi__vho.size and sxvoi__vho.type == pa_fs.FileType.Directory:
            return True
        return False
    except (FileNotFoundError, OSError) as gte__idpc:
        raise
    except BodoError as itpey__mxam:
        raise
    except Exception as gte__idpc:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(gte__idpc).__name__}: {str(gte__idpc)}
{bodo_error_msg}"""
            )


def s3_list_dir_fnames(fs, path):
    from pyarrow import fs as pa_fs
    ycy__vox = None
    try:
        if s3_is_directory(fs, path):
            wfgsm__cmsd = urlparse(path)
            fhjx__jsz = (wfgsm__cmsd.netloc + wfgsm__cmsd.path).rstrip('/')
            enb__zwpkn = pa_fs.FileSelector(fhjx__jsz, recursive=False)
            zefb__dxr = fs.get_file_info(enb__zwpkn)
            if zefb__dxr and zefb__dxr[0].path in [fhjx__jsz, f'{fhjx__jsz}/'
                ] and int(zefb__dxr[0].size or 0) == 0:
                zefb__dxr = zefb__dxr[1:]
            ycy__vox = [iih__oomen.base_name for iih__oomen in zefb__dxr]
    except BodoError as itpey__mxam:
        raise
    except Exception as gte__idpc:
        raise BodoError(
            f"""error from pyarrow S3FileSystem: {type(gte__idpc).__name__}: {str(gte__idpc)}
{bodo_error_msg}"""
            )
    return ycy__vox


def hdfs_is_directory(path):
    from pyarrow.fs import FileType, HadoopFileSystem
    check_java_installation(path)
    wfgsm__cmsd = urlparse(path)
    qchyo__xuf = wfgsm__cmsd.path
    try:
        pxy__stvm = HadoopFileSystem.from_uri(path)
    except Exception as gte__idpc:
        raise BodoError(' Hadoop file system cannot be created: {}'.format(
            gte__idpc))
    vrqe__jeev = pxy__stvm.get_file_info([qchyo__xuf])
    if vrqe__jeev[0].type in (FileType.NotFound, FileType.Unknown):
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if not vrqe__jeev[0].size and vrqe__jeev[0].type == FileType.Directory:
        return pxy__stvm, True
    return pxy__stvm, False


def hdfs_list_dir_fnames(path):
    from pyarrow.fs import FileSelector
    ycy__vox = None
    pxy__stvm, kwed__zfqdv = hdfs_is_directory(path)
    if kwed__zfqdv:
        wfgsm__cmsd = urlparse(path)
        qchyo__xuf = wfgsm__cmsd.path
        enb__zwpkn = FileSelector(qchyo__xuf, recursive=True)
        try:
            zefb__dxr = pxy__stvm.get_file_info(enb__zwpkn)
        except Exception as gte__idpc:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(qchyo__xuf, gte__idpc))
        ycy__vox = [iih__oomen.base_name for iih__oomen in zefb__dxr]
    return pxy__stvm, ycy__vox


def abfs_is_directory(path):
    pxy__stvm = get_hdfs_fs(path)
    try:
        vrqe__jeev = pxy__stvm.info(path)
    except OSError as itpey__mxam:
        raise BodoError('{} is a non-existing or unreachable file'.format(path)
            )
    if vrqe__jeev['size'] == 0 and vrqe__jeev['kind'].lower() == 'directory':
        return pxy__stvm, True
    return pxy__stvm, False


def abfs_list_dir_fnames(path):
    ycy__vox = None
    pxy__stvm, kwed__zfqdv = abfs_is_directory(path)
    if kwed__zfqdv:
        wfgsm__cmsd = urlparse(path)
        qchyo__xuf = wfgsm__cmsd.path
        try:
            qxnqs__bmxid = pxy__stvm.ls(qchyo__xuf)
        except Exception as gte__idpc:
            raise BodoError('Exception on getting directory info of {}: {}'
                .format(qchyo__xuf, gte__idpc))
        ycy__vox = [fname[fname.rindex('/') + 1:] for fname in qxnqs__bmxid]
    return pxy__stvm, ycy__vox


def directory_of_files_common_filter(fname):
    return not (fname.endswith('.crc') or fname.endswith('_$folder$') or
        fname.startswith('.') or fname.startswith('_') and fname !=
        '_delta_log')


def find_file_name_or_handler(path, ftype, storage_options=None):
    from urllib.parse import urlparse
    hbhm__czyvs = urlparse(path)
    fname = path
    fs = None
    djcdn__jgyv = 'read_json' if ftype == 'json' else 'read_csv'
    ptg__euj = (
        f'pd.{djcdn__jgyv}(): there is no {ftype} file in directory: {fname}')
    lhz__bqiwt = directory_of_files_common_filter
    if hbhm__czyvs.scheme == 's3':
        nxeju__lsy = True
        fs = get_s3_fs_from_path(path, storage_options=storage_options)
        trls__gqxn = s3_list_dir_fnames(fs, path)
        fhjx__jsz = (hbhm__czyvs.netloc + hbhm__czyvs.path).rstrip('/')
        fname = fhjx__jsz
        if trls__gqxn:
            trls__gqxn = [(fhjx__jsz + '/' + vmren__yhze) for vmren__yhze in
                sorted(filter(lhz__bqiwt, trls__gqxn))]
            gfoy__mmo = [vmren__yhze for vmren__yhze in trls__gqxn if int(
                fs.get_file_info(vmren__yhze).size or 0) > 0]
            if len(gfoy__mmo) == 0:
                raise BodoError(ptg__euj)
            fname = gfoy__mmo[0]
        zme__ktjkj = int(fs.get_file_info(fname).size or 0)
        fs = ArrowFSWrapper(fs)
        idye__hsls = fs._open(fname)
    elif hbhm__czyvs.scheme == 'hdfs':
        nxeju__lsy = True
        fs, trls__gqxn = hdfs_list_dir_fnames(path)
        zme__ktjkj = fs.get_file_info([hbhm__czyvs.path])[0].size
        if trls__gqxn:
            path = path.rstrip('/')
            trls__gqxn = [(path + '/' + vmren__yhze) for vmren__yhze in
                sorted(filter(lhz__bqiwt, trls__gqxn))]
            gfoy__mmo = [vmren__yhze for vmren__yhze in trls__gqxn if fs.
                get_file_info([urlparse(vmren__yhze).path])[0].size > 0]
            if len(gfoy__mmo) == 0:
                raise BodoError(ptg__euj)
            fname = gfoy__mmo[0]
            fname = urlparse(fname).path
            zme__ktjkj = fs.get_file_info([fname])[0].size
        idye__hsls = fs.open_input_file(fname)
    elif hbhm__czyvs.scheme in ('abfs', 'abfss'):
        nxeju__lsy = True
        fs, trls__gqxn = abfs_list_dir_fnames(path)
        zme__ktjkj = fs.info(fname)['size']
        if trls__gqxn:
            path = path.rstrip('/')
            trls__gqxn = [(path + '/' + vmren__yhze) for vmren__yhze in
                sorted(filter(lhz__bqiwt, trls__gqxn))]
            gfoy__mmo = [vmren__yhze for vmren__yhze in trls__gqxn if fs.
                info(vmren__yhze)['size'] > 0]
            if len(gfoy__mmo) == 0:
                raise BodoError(ptg__euj)
            fname = gfoy__mmo[0]
            zme__ktjkj = fs.info(fname)['size']
            fname = urlparse(fname).path
        idye__hsls = fs.open(fname, 'rb')
    else:
        if hbhm__czyvs.scheme != '':
            raise BodoError(
                f'Unrecognized scheme {hbhm__czyvs.scheme}. Please refer to https://docs.bodo.ai/latest/file_io/.'
                )
        nxeju__lsy = False
        if os.path.isdir(path):
            qxnqs__bmxid = filter(lhz__bqiwt, glob.glob(os.path.join(os.
                path.abspath(path), '*')))
            gfoy__mmo = [vmren__yhze for vmren__yhze in sorted(qxnqs__bmxid
                ) if os.path.getsize(vmren__yhze) > 0]
            if len(gfoy__mmo) == 0:
                raise BodoError(ptg__euj)
            fname = gfoy__mmo[0]
        zme__ktjkj = os.path.getsize(fname)
        idye__hsls = fname
    return nxeju__lsy, idye__hsls, zme__ktjkj, fs


def get_s3_bucket_region(s3_filepath, parallel):
    try:
        from pyarrow import fs as pa_fs
    except:
        raise BodoError('Reading from s3 requires pyarrow currently.')
    from mpi4py import MPI
    seb__wtrcb = MPI.COMM_WORLD
    bucket_loc = None
    if parallel and bodo.get_rank() == 0 or not parallel:
        try:
            wjmo__zqt, lvc__ureg = pa_fs.S3FileSystem.from_uri(s3_filepath)
            bucket_loc = wjmo__zqt.region
        except Exception as gte__idpc:
            if os.environ.get('AWS_DEFAULT_REGION', '') == '':
                warnings.warn(BodoWarning(
                    f"""Unable to get S3 Bucket Region.
{gte__idpc}.
Value not defined in the AWS_DEFAULT_REGION environment variable either. Region defaults to us-east-1 currently."""
                    ))
            bucket_loc = ''
    if parallel:
        bucket_loc = seb__wtrcb.bcast(bucket_loc)
    return bucket_loc


@numba.njit()
def get_s3_bucket_region_njit(s3_filepath, parallel):
    with numba.objmode(bucket_loc='unicode_type'):
        bucket_loc = ''
        if isinstance(s3_filepath, list):
            s3_filepath = s3_filepath[0]
        if s3_filepath.startswith('s3://'):
            bucket_loc = get_s3_bucket_region(s3_filepath, parallel)
    return bucket_loc


def csv_write(path_or_buf, D, filename_prefix, is_parallel=False):
    return None


@overload(csv_write, no_unliteral=True)
def csv_write_overload(path_or_buf, D, filename_prefix, is_parallel=False):

    def impl(path_or_buf, D, filename_prefix, is_parallel=False):
        eueq__lgc = get_s3_bucket_region_njit(path_or_buf, parallel=is_parallel
            )
        mkhkm__wkq, mxnid__del = unicode_to_utf8_and_len(D)
        tndap__bjif = 0
        if is_parallel:
            tndap__bjif = bodo.libs.distributed_api.dist_exscan(mxnid__del,
                np.int32(Reduce_Type.Sum.value))
        _csv_write(unicode_to_utf8(path_or_buf), mkhkm__wkq, tndap__bjif,
            mxnid__del, is_parallel, unicode_to_utf8(eueq__lgc),
            unicode_to_utf8(filename_prefix))
        bodo.utils.utils.check_and_propagate_cpp_exception()
    return impl


class StorageOptionsDictType(types.Opaque):

    def __init__(self):
        super(StorageOptionsDictType, self).__init__(name=
            'StorageOptionsDictType')


storage_options_dict_type = StorageOptionsDictType()
types.storage_options_dict_type = storage_options_dict_type
register_model(StorageOptionsDictType)(models.OpaqueModel)


@unbox(StorageOptionsDictType)
def unbox_storage_options_dict_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


def get_storage_options_pyobject(storage_options):
    pass


@overload(get_storage_options_pyobject, no_unliteral=True)
def overload_get_storage_options_pyobject(storage_options):
    jxwt__rvfy = get_overload_constant_dict(storage_options)
    bwzrm__thjfj = 'def impl(storage_options):\n'
    bwzrm__thjfj += (
        "  with numba.objmode(storage_options_py='storage_options_dict_type'):\n"
        )
    bwzrm__thjfj += f'    storage_options_py = {str(jxwt__rvfy)}\n'
    bwzrm__thjfj += '  return storage_options_py\n'
    zfp__szkh = {}
    exec(bwzrm__thjfj, globals(), zfp__szkh)
    return zfp__szkh['impl']
