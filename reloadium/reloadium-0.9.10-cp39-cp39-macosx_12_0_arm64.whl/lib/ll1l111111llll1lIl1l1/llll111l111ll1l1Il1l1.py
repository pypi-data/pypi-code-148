import sys


def lllll1lll1l1l111Il1l1(l1lll11lll1lllllIl1l1, ll1lll1ll111llllIl1l1):
    from pathlib import Path
    from multiprocessing import util, spawn
    from multiprocessing.context import reduction, set_spawning_popen
    import io
    import os

    def ll11111l1lll11l1Il1l1(*l11lll1l11l11l11Il1l1):

        for l1l1lll1lll1l11lIl1l1 in l11lll1l11l11l11Il1l1:
            os.close(l1l1lll1lll1l11lIl1l1)

    if (sys.version_info > (3, 8, )):
        from multiprocessing import resource_tracker as tracker 
    else:
        from multiprocessing import semaphore_tracker as tracker 

    lll111l11l1l1ll1Il1l1 = tracker.getfd()
    l1lll11lll1lllllIl1l1._fds.append(lll111l11l1l1ll1Il1l1)
    l1l1l1111ll1llllIl1l1 = spawn.get_preparation_data(ll1lll1ll111llllIl1l1._name)
    l11l1ll1lll111l1Il1l1 = io.BytesIO()
    set_spawning_popen(l1lll11lll1lllllIl1l1)

    try:
        reduction.dump(l1l1l1111ll1llllIl1l1, l11l1ll1lll111l1Il1l1)
        reduction.dump(ll1lll1ll111llllIl1l1, l11l1ll1lll111l1Il1l1)
    finally:
        set_spawning_popen(None)

    l1lll1l1lll11l11Il1l1lll1l1ll111ll1l1Il1l1ll11lll1l1l1ll1lIl1l1lll1llllll11l1llIl1l1 = None
    try:
        (l1lll1l1lll11l11Il1l1, lll1l1ll111ll1l1Il1l1, ) = os.pipe()
        (ll11lll1l1l1ll1lIl1l1, lll1llllll11l1llIl1l1, ) = os.pipe()
        ll1ll11lll1l1l11Il1l1 = spawn.get_command_line(tracker_fd=lll111l11l1l1ll1Il1l1, pipe_handle=ll11lll1l1l1ll1lIl1l1)


        llll111l111111l1Il1l1 = str(Path(l1l1l1111ll1llllIl1l1['sys_argv'][0]).absolute())
        ll1ll11lll1l1l11Il1l1 = [ll1ll11lll1l1l11Il1l1[0], '-B', '-m', 'reloadium', 'spawn_process', str(lll111l11l1l1ll1Il1l1), 
str(ll11lll1l1l1ll1lIl1l1), llll111l111111l1Il1l1]
        l1lll11lll1lllllIl1l1._fds.extend([ll11lll1l1l1ll1lIl1l1, lll1l1ll111ll1l1Il1l1])
        l1lll11lll1lllllIl1l1.pid = util.spawnv_passfds(spawn.get_executable(), 
ll1ll11lll1l1l11Il1l1, l1lll11lll1lllllIl1l1._fds)
        l1lll11lll1lllllIl1l1.sentinel = l1lll1l1lll11l11Il1l1
        with open(lll1llllll11l1llIl1l1, 'wb', closefd=False) as ll1lll1lll1ll11lIl1l1:
            ll1lll1lll1ll11lIl1l1.write(l11l1ll1lll111l1Il1l1.getbuffer())
    finally:
        l1l1111l1111l111Il1l1 = []
        for l1l1lll1lll1l11lIl1l1 in (l1lll1l1lll11l11Il1l1, lll1llllll11l1llIl1l1, ):
            if (l1l1lll1lll1l11lIl1l1 is not None):
                l1l1111l1111l111Il1l1.append(l1l1lll1lll1l11lIl1l1)
        l1lll11lll1lllllIl1l1.finalizer = util.Finalize(l1lll11lll1lllllIl1l1, ll11111l1lll11l1Il1l1, l1l1111l1111l111Il1l1)

        for l1l1lll1lll1l11lIl1l1 in (ll11lll1l1l1ll1lIl1l1, lll1l1ll111ll1l1Il1l1, ):
            if (l1l1lll1lll1l11lIl1l1 is not None):
                os.close(l1l1lll1lll1l11lIl1l1)


def __init__(l1lll11lll1lllllIl1l1, ll1lll1ll111llllIl1l1):
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

    l1l1l1111ll1llllIl1l1 = spawn.get_preparation_data(ll1lll1ll111llllIl1l1._name)







    (lll1111ll1111111Il1l1, ll1l1l11ll1ll11lIl1l1, ) = _winapi.CreatePipe(None, 0)
    lll1ll1ll111ll1lIl1l1 = msvcrt.open_osfhandle(ll1l1l11ll1ll11lIl1l1, 0)
    l1l1l1ll1111llllIl1l1 = spawn.get_executable()
    llll111l111111l1Il1l1 = str(Path(l1l1l1111ll1llllIl1l1['sys_argv'][0]).absolute())
    ll1ll11lll1l1l11Il1l1 = ' '.join([l1l1l1ll1111llllIl1l1, '-B', '-m', 'reloadium', 'spawn_process', str(os.getpid()), 
str(lll1111ll1111111Il1l1), llll111l111111l1Il1l1])



    if ((WINENV and _path_eq(l1l1l1ll1111llllIl1l1, sys.executable))):
        l1l1l1ll1111llllIl1l1 = sys._base_executable
        ll1ll1llllllll11Il1l1 = os.environ.copy()
        ll1ll1llllllll11Il1l1['__PYVENV_LAUNCHER__'] = sys.executable
    else:
        ll1ll1llllllll11Il1l1 = None

    with open(lll1ll1ll111ll1lIl1l1, 'wb', closefd=True) as l1l1lll1l11l1111Il1l1:

        try:
            (l11l1l111l1ll111Il1l1, l1l1l1lll11llll1Il1l1, l111ll11l1l1l1llIl1l1, l11l111l11l1l1llIl1l1, ) = _winapi.CreateProcess(l1l1l1ll1111llllIl1l1, ll1ll11lll1l1l11Il1l1, None, None, False, 0, ll1ll1llllllll11Il1l1, None, None)


            _winapi.CloseHandle(l1l1l1lll11llll1Il1l1)
        except :
            _winapi.CloseHandle(lll1111ll1111111Il1l1)
            raise 


        l1lll11lll1lllllIl1l1.pid = l111ll11l1l1l1llIl1l1
        l1lll11lll1lllllIl1l1.returncode = None
        l1lll11lll1lllllIl1l1._handle = l11l1l111l1ll111Il1l1
        l1lll11lll1lllllIl1l1.sentinel = int(l11l1l111l1ll111Il1l1)
        if (sys.version_info > (3, 8, )):
            l1lll11lll1lllllIl1l1.finalizer = util.Finalize(l1lll11lll1lllllIl1l1, _close_handles, (l1lll11lll1lllllIl1l1.sentinel, int(lll1111ll1111111Il1l1), 
))
        else:
            l1lll11lll1lllllIl1l1.finalizer = util.Finalize(l1lll11lll1lllllIl1l1, _close_handles, (l1lll11lll1lllllIl1l1.sentinel, ))



        set_spawning_popen(l1lll11lll1lllllIl1l1)
        try:
            reduction.dump(l1l1l1111ll1llllIl1l1, l1l1lll1l11l1111Il1l1)
            reduction.dump(ll1lll1ll111llllIl1l1, l1l1lll1l11l1111Il1l1)
        finally:
            set_spawning_popen(None)
