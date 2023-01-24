import gc
import inspect
import sys
import types as pytypes
import bodo
master_mode_on = False
MASTER_RANK = 0


class MasterModeDispatcher(object):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def __call__(self, *args, **kwargs):
        assert bodo.get_rank() == MASTER_RANK
        return master_wrapper(self.dispatcher, *args, **kwargs)

    def __getstate__(self):
        assert bodo.get_rank() == MASTER_RANK
        return self.dispatcher.py_func

    def __setstate__(self, state):
        assert bodo.get_rank() != MASTER_RANK
        uzb__bloi = state
        nfj__kpfft = inspect.getsourcelines(uzb__bloi)[0][0]
        assert nfj__kpfft.startswith('@bodo.jit') or nfj__kpfft.startswith(
            '@jit')
        tksb__wori = eval(nfj__kpfft[1:])
        self.dispatcher = tksb__wori(uzb__bloi)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    nsmgy__atr = MPI.COMM_WORLD
    while True:
        nxp__cremq = nsmgy__atr.bcast(None, root=MASTER_RANK)
        if nxp__cremq[0] == 'exec':
            uzb__bloi = pickle.loads(nxp__cremq[1])
            for mijuj__xxv, bjxc__niac in list(uzb__bloi.__globals__.items()):
                if isinstance(bjxc__niac, MasterModeDispatcher):
                    uzb__bloi.__globals__[mijuj__xxv] = bjxc__niac.dispatcher
            if uzb__bloi.__module__ not in sys.modules:
                sys.modules[uzb__bloi.__module__] = pytypes.ModuleType(
                    uzb__bloi.__module__)
            nfj__kpfft = inspect.getsourcelines(uzb__bloi)[0][0]
            assert nfj__kpfft.startswith('@bodo.jit') or nfj__kpfft.startswith(
                '@jit')
            tksb__wori = eval(nfj__kpfft[1:])
            func = tksb__wori(uzb__bloi)
            bokth__ualf = nxp__cremq[2]
            rtoek__biyqs = nxp__cremq[3]
            rbh__oijsl = []
            for fik__wujp in bokth__ualf:
                if fik__wujp == 'scatter':
                    rbh__oijsl.append(bodo.scatterv(None))
                elif fik__wujp == 'bcast':
                    rbh__oijsl.append(nsmgy__atr.bcast(None, root=MASTER_RANK))
            kyi__bhiv = {}
            for argname, fik__wujp in rtoek__biyqs.items():
                if fik__wujp == 'scatter':
                    kyi__bhiv[argname] = bodo.scatterv(None)
                elif fik__wujp == 'bcast':
                    kyi__bhiv[argname] = nsmgy__atr.bcast(None, root=
                        MASTER_RANK)
            ppq__sjfe = func(*rbh__oijsl, **kyi__bhiv)
            if ppq__sjfe is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(ppq__sjfe)
            del (nxp__cremq, uzb__bloi, func, tksb__wori, bokth__ualf,
                rtoek__biyqs, rbh__oijsl, kyi__bhiv, ppq__sjfe)
            gc.collect()
        elif nxp__cremq[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    nsmgy__atr = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        bokth__ualf = ['scatter' for rqgb__iivou in range(len(args))]
        rtoek__biyqs = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        ckw__xik = func.py_func.__code__.co_varnames
        njgg__cjtxk = func.targetoptions

        def get_distribution(argname):
            if argname in njgg__cjtxk.get('distributed', []
                ) or argname in njgg__cjtxk.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        bokth__ualf = [get_distribution(argname) for argname in ckw__xik[:
            len(args)]]
        rtoek__biyqs = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    txb__txct = pickle.dumps(func.py_func)
    nsmgy__atr.bcast(['exec', txb__txct, bokth__ualf, rtoek__biyqs])
    rbh__oijsl = []
    for yag__xnfxq, fik__wujp in zip(args, bokth__ualf):
        if fik__wujp == 'scatter':
            rbh__oijsl.append(bodo.scatterv(yag__xnfxq))
        elif fik__wujp == 'bcast':
            nsmgy__atr.bcast(yag__xnfxq)
            rbh__oijsl.append(yag__xnfxq)
    kyi__bhiv = {}
    for argname, yag__xnfxq in kwargs.items():
        fik__wujp = rtoek__biyqs[argname]
        if fik__wujp == 'scatter':
            kyi__bhiv[argname] = bodo.scatterv(yag__xnfxq)
        elif fik__wujp == 'bcast':
            nsmgy__atr.bcast(yag__xnfxq)
            kyi__bhiv[argname] = yag__xnfxq
    rpqvw__ccvn = []
    for mijuj__xxv, bjxc__niac in list(func.py_func.__globals__.items()):
        if isinstance(bjxc__niac, MasterModeDispatcher):
            rpqvw__ccvn.append((func.py_func.__globals__, mijuj__xxv, func.
                py_func.__globals__[mijuj__xxv]))
            func.py_func.__globals__[mijuj__xxv] = bjxc__niac.dispatcher
    ppq__sjfe = func(*rbh__oijsl, **kyi__bhiv)
    for mor__qlri, mijuj__xxv, bjxc__niac in rpqvw__ccvn:
        mor__qlri[mijuj__xxv] = bjxc__niac
    if ppq__sjfe is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        ppq__sjfe = bodo.gatherv(ppq__sjfe)
    return ppq__sjfe


def init_master_mode():
    if bodo.get_size() == 1:
        return
    global master_mode_on
    assert master_mode_on is False, 'init_master_mode can only be called once on each process'
    master_mode_on = True
    assert sys.version_info[:2] >= (3, 8
        ), 'Python 3.8+ required for master mode'
    from bodo import jit
    globals()['jit'] = jit
    import cloudpickle
    from mpi4py import MPI
    globals()['pickle'] = cloudpickle
    globals()['MPI'] = MPI

    def master_exit():
        MPI.COMM_WORLD.bcast(['exit'])
    if bodo.get_rank() == MASTER_RANK:
        import atexit
        atexit.register(master_exit)
    else:
        worker_loop()
