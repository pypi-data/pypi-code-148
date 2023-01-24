import sys


def lll111l1llll11l1Il1l1(l1lllll11lll11llIl1l1, l11l1111l1lll111Il1l1):
    from pathlib import Path
    from multiprocessing import util, spawn
    from multiprocessing.context import reduction, set_spawning_popen
    import io
    import os

    def llll1lllll1l11l1Il1l1(*lllll11111l111llIl1l1):

        for llll111l11111l11Il1l1 in lllll11111l111llIl1l1:
            os.close(llll111l11111l11Il1l1)

    if (sys.version_info > (3, 8, )):
        from multiprocessing import resource_tracker as tracker 
    else:
        from multiprocessing import semaphore_tracker as tracker 

    l1111l111111ll1lIl1l1 = tracker.getfd()
    l1lllll11lll11llIl1l1._fds.append(l1111l111111ll1lIl1l1)
    ll1llll1ll1l11llIl1l1 = spawn.get_preparation_data(l11l1111l1lll111Il1l1._name)
    l1l1ll111111l1llIl1l1 = io.BytesIO()
    set_spawning_popen(l1lllll11lll11llIl1l1)

    try:
        reduction.dump(ll1llll1ll1l11llIl1l1, l1l1ll111111l1llIl1l1)
        reduction.dump(l11l1111l1lll111Il1l1, l1l1ll111111l1llIl1l1)
    finally:
        set_spawning_popen(None)

    lll11l11111111llIl1l1l111lll1l1111111Il1l1l1ll111111l1111lIl1l1ll11111l11l11l1lIl1l1 = None
    try:
        (lll11l11111111llIl1l1, l111lll1l1111111Il1l1, ) = os.pipe()
        (l1ll111111l1111lIl1l1, ll11111l11l11l1lIl1l1, ) = os.pipe()
        l1l11lll1l11ll1lIl1l1 = spawn.get_command_line(tracker_fd=l1111l111111ll1lIl1l1, pipe_handle=l1ll111111l1111lIl1l1)


        ll1lll1ll11ll111Il1l1 = str(Path(ll1llll1ll1l11llIl1l1['sys_argv'][0]).absolute())
        l1l11lll1l11ll1lIl1l1 = [l1l11lll1l11ll1lIl1l1[0], '-B', '-m', 'reloadium', 'spawn_process', str(l1111l111111ll1lIl1l1), 
str(l1ll111111l1111lIl1l1), ll1lll1ll11ll111Il1l1]
        l1lllll11lll11llIl1l1._fds.extend([l1ll111111l1111lIl1l1, l111lll1l1111111Il1l1])
        l1lllll11lll11llIl1l1.pid = util.spawnv_passfds(spawn.get_executable(), 
l1l11lll1l11ll1lIl1l1, l1lllll11lll11llIl1l1._fds)
        l1lllll11lll11llIl1l1.sentinel = lll11l11111111llIl1l1
        with open(ll11111l11l11l1lIl1l1, 'wb', closefd=False) as l1111lll11llll1lIl1l1:
            l1111lll11llll1lIl1l1.write(l1l1ll111111l1llIl1l1.getbuffer())
    finally:
        l111111l1llll11lIl1l1 = []
        for llll111l11111l11Il1l1 in (lll11l11111111llIl1l1, ll11111l11l11l1lIl1l1, ):
            if (llll111l11111l11Il1l1 is not None):
                l111111l1llll11lIl1l1.append(llll111l11111l11Il1l1)
        l1lllll11lll11llIl1l1.finalizer = util.Finalize(l1lllll11lll11llIl1l1, llll1lllll1l11l1Il1l1, l111111l1llll11lIl1l1)

        for llll111l11111l11Il1l1 in (l1ll111111l1111lIl1l1, l111lll1l1111111Il1l1, ):
            if (llll111l11111l11Il1l1 is not None):
                os.close(llll111l11111l11Il1l1)


def __init__(l1lllll11lll11llIl1l1, l11l1111l1lll111Il1l1):
    from multiprocessing import util, spawn
    from multiprocessing.context import reduction, set_spawning_popen
    from multiprocessing.popen_spawn_win32 import TERMINATE, WINEXE, WINSERVICE, WINENV, _path_eq
    from pathlib import Path
    import os
    import msvcrt
    import sys
    import _winapi

    if (sys.version_info > (3, 8, )):
        from multiprocessing import resource_tracker as tracker 
        from multiprocessing.popen_spawn_win32 import _close_handles
    else:
        from multiprocessing import semaphore_tracker as tracker 
        _close_handles = _winapi.CloseHandle

    ll1llll1ll1l11llIl1l1 = spawn.get_preparation_data(l11l1111l1lll111Il1l1._name)







    (l11l1l11l11l1l11Il1l1, l111l1l1l1lll11lIl1l1, ) = _winapi.CreatePipe(None, 0)
    ll111ll1111ll1llIl1l1 = msvcrt.open_osfhandle(l111l1l1l1lll11lIl1l1, 0)
    l111l11llll1111lIl1l1 = spawn.get_executable()
    ll1lll1ll11ll111Il1l1 = str(Path(ll1llll1ll1l11llIl1l1['sys_argv'][0]).absolute())
    l1l11lll1l11ll1lIl1l1 = ' '.join([l111l11llll1111lIl1l1, '-B', '-m', 'reloadium', 'spawn_process', str(os.getpid()), 
str(l11l1l11l11l1l11Il1l1), ll1lll1ll11ll111Il1l1])



    if ((WINENV and _path_eq(l111l11llll1111lIl1l1, sys.executable))):
        l111l11llll1111lIl1l1 = sys._base_executable
        l111llll1111111lIl1l1 = os.environ.copy()
        l111llll1111111lIl1l1['__PYVENV_LAUNCHER__'] = sys.executable
    else:
        l111llll1111111lIl1l1 = None

    with open(ll111ll1111ll1llIl1l1, 'wb', closefd=True) as ll111111l1l111llIl1l1:

        try:
            (ll1lll1llllll1llIl1l1, l111ll11111l111lIl1l1, ll1lllll1ll1l11lIl1l1, lll111111l11llllIl1l1, ) = _winapi.CreateProcess(l111l11llll1111lIl1l1, l1l11lll1l11ll1lIl1l1, None, None, False, 0, l111llll1111111lIl1l1, None, None)


            _winapi.CloseHandle(l111ll11111l111lIl1l1)
        except :
            _winapi.CloseHandle(l11l1l11l11l1l11Il1l1)
            raise 


        l1lllll11lll11llIl1l1.pid = ll1lllll1ll1l11lIl1l1
        l1lllll11lll11llIl1l1.returncode = None
        l1lllll11lll11llIl1l1._handle = ll1lll1llllll1llIl1l1
        l1lllll11lll11llIl1l1.sentinel = int(ll1lll1llllll1llIl1l1)
        if (sys.version_info > (3, 8, )):
            l1lllll11lll11llIl1l1.finalizer = util.Finalize(l1lllll11lll11llIl1l1, _close_handles, (l1lllll11lll11llIl1l1.sentinel, int(l11l1l11l11l1l11Il1l1), 
))
        else:
            l1lllll11lll11llIl1l1.finalizer = util.Finalize(l1lllll11lll11llIl1l1, _close_handles, (l1lllll11lll11llIl1l1.sentinel, ))



        set_spawning_popen(l1lllll11lll11llIl1l1)
        try:
            reduction.dump(ll1llll1ll1l11llIl1l1, ll111111l1l111llIl1l1)
            reduction.dump(l11l1111l1lll111Il1l1, ll111111l1l111llIl1l1)
        finally:
            set_spawning_popen(None)
