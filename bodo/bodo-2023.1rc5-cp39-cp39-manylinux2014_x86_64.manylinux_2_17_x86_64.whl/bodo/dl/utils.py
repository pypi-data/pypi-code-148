"""Support distributed deep learning with Horovod
"""
import time
import numba
import numpy as np
from mpi4py import MPI
import bodo
from bodo.libs.distributed_api import create_subcomm_mpi4py, get_host_ranks, get_nodes_first_ranks
dl_status = None


def assert_dl_initialized():
    assert dl_status is not None, 'Horovod has not been initialized. Call bodo.dl.start() first'


class DLStatus(object):

    def __init__(self, framework, gpu_ranks):
        self.framework = framework
        self.gpu_ranks = gpu_ranks


def get_num_gpus(framework):
    if framework == 'torch':
        import torch
        return torch.cuda.device_count()
    elif framework == 'tensorflow':
        import tensorflow as tf
        return len(tf.config.experimental.list_physical_devices('GPU'))
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))


def get_gpu_ranks(framework):
    opqj__nzkn = MPI.COMM_WORLD
    wgln__umu = opqj__nzkn.Get_rank()
    umyh__tkw = get_host_ranks()
    zpdn__wkgfp = get_nodes_first_ranks()
    if wgln__umu in zpdn__wkgfp:
        try:
            sdv__rvtun = get_num_gpus(framework)
        except Exception as jgjzl__hyr:
            sdv__rvtun = jgjzl__hyr
        ufrbz__eku = create_subcomm_mpi4py(zpdn__wkgfp)
        ien__qhhey = ufrbz__eku.gather(sdv__rvtun)
        if wgln__umu == 0:
            gpu_ranks = []
            mwh__rvacr = None
            for tbjki__bwwoa, nsdkf__dop in enumerate(umyh__tkw.values()):
                ltx__dvep = ien__qhhey[tbjki__bwwoa]
                if isinstance(ltx__dvep, Exception):
                    mwh__rvacr = ltx__dvep
                    break
                if ltx__dvep == 0:
                    continue
                hiks__aqb = len(nsdkf__dop) // ltx__dvep
                for vexy__vumpo, bzle__trs in enumerate(nsdkf__dop):
                    if vexy__vumpo % hiks__aqb == 0:
                        pzpzx__mur = vexy__vumpo / hiks__aqb
                        if pzpzx__mur < ltx__dvep:
                            gpu_ranks.append(bzle__trs)
            if mwh__rvacr:
                opqj__nzkn.bcast(mwh__rvacr)
                raise mwh__rvacr
            else:
                opqj__nzkn.bcast(gpu_ranks)
    if wgln__umu != 0:
        gpu_ranks = opqj__nzkn.bcast(None)
        if isinstance(gpu_ranks, Exception):
            jgjzl__hyr = gpu_ranks
            raise jgjzl__hyr
    return gpu_ranks


def is_cuda_available():
    assert_dl_initialized()
    return len(dl_status.gpu_ranks) > 0


def initialize_horovod(framework):
    global dl_status
    if dl_status is not None:
        assert dl_status.framework == framework, 'Attempted to initialize Horovod with different DL frameworks'
        return np.array(dl_status.gpu_ranks, dtype=np.int32)
    gpu_ranks = get_gpu_ranks(framework)
    if framework == 'torch':
        import horovod.torch as hvd
        import torch
        torch.set_num_threads(1)
    elif framework == 'tensorflow':
        import horovod.tensorflow as hvd
        import tensorflow as tf
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))
    ytlq__jfi = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        ufrbz__eku = MPI.COMM_WORLD.Split(color=0 if ytlq__jfi in gpu_ranks
             else MPI.UNDEFINED, key=ytlq__jfi)
        if ufrbz__eku != MPI.COMM_NULL:
            hvd.init(comm=ufrbz__eku)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                lyxo__ghk = tf.config.experimental.list_physical_devices('GPU')
                for mjzd__uopl in lyxo__ghk:
                    tf.config.experimental.set_memory_growth(mjzd__uopl, True)
                tf.config.experimental.set_visible_devices(lyxo__ghk[hvd.
                    local_rank()], 'GPU')
    else:
        if ytlq__jfi == 0:
            print('[BODO-DL]: No GPUs found in cluster. Using CPUs')
        hvd.init()
    dl_status = DLStatus(framework, np.array(gpu_ranks, dtype=np.int32))


@numba.njit
def start(framework):
    with numba.objmode:
        initialize_horovod(framework)


@numba.njit
def end():
    with numba.objmode:
        end_py()


def end_py():
    if is_cuda_available():
        mpo__xte = 17
        opqj__nzkn = MPI.COMM_WORLD
        diylh__knuj = MPI.Get_processor_name()
        suja__hsde = get_host_ranks()[diylh__knuj]
        assert_dl_initialized()
        if bodo.get_rank() == suja__hsde[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for wgln__umu in suja__hsde[1:]:
                opqj__nzkn.isend(1, dest=wgln__umu, tag=mpo__xte)
        else:
            while True:
                mmhg__ptiv = MPI.Status()
                mdoj__euga = opqj__nzkn.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    mmhg__ptiv)
                if mdoj__euga:
                    assert mmhg__ptiv.source == suja__hsde[0]
                    assert mmhg__ptiv.tag == mpo__xte
                    opqj__nzkn.recv(source=0, tag=mpo__xte)
                    break
                time.sleep(1.0)
    else:
        bodo.barrier()


def _prepare_data_get_gpu_ranks():
    assert_dl_initialized()
    return dl_status.gpu_ranks


@numba.njit
def prepare_data(data):
    with numba.objmode(gpu_ranks='int32[:]'):
        gpu_ranks = _prepare_data_get_gpu_ranks()
    if len(gpu_ranks) > 0:
        data = bodo.rebalance(data, dests=list(gpu_ranks), parallel=True)
    else:
        data = bodo.rebalance(data, parallel=True)
    return data
