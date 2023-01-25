import sys


def ll1111ll111lll11Il1l1(l1l1ll1ll1lllll1Il1l1, ll11l1l11ll11l11Il1l1):
    from pathlib import Path
    from multiprocessing import util, spawn
    from multiprocessing.context import reduction, set_spawning_popen
    import io
    import os

    def l11111l11l1l11l1Il1l1(*l1l111l1l1ll1111Il1l1):

        for ll1lllll1ll1l111Il1l1 in l1l111l1l1ll1111Il1l1:
            os.close(ll1lllll1ll1l111Il1l1)

    if (sys.version_info > (3, 8, )):
        from multiprocessing import resource_tracker as tracker 
    else:
        from multiprocessing import semaphore_tracker as tracker 

    llll1l11l1111111Il1l1 = tracker.getfd()
    l1l1ll1ll1lllll1Il1l1._fds.append(llll1l11l1111111Il1l1)
    llll111ll1ll1ll1Il1l1 = spawn.get_preparation_data(ll11l1l11ll11l11Il1l1._name)
    llll1ll1l1ll1l11Il1l1 = io.BytesIO()
    set_spawning_popen(l1l1ll1ll1lllll1Il1l1)

    try:
        reduction.dump(llll111ll1ll1ll1Il1l1, llll1ll1l1ll1l11Il1l1)
        reduction.dump(ll11l1l11ll11l11Il1l1, llll1ll1l1ll1l11Il1l1)
    finally:
        set_spawning_popen(None)

    l1lll1l111111ll1Il1l1l1l1l1llllll11llIl1l1ll11ll1lllll11llIl1l1lll11lll1l1ll111Il1l1 = None
    try:
        (l1lll1l111111ll1Il1l1, l1l1l1llllll11llIl1l1, ) = os.pipe()
        (ll11ll1lllll11llIl1l1, lll11lll1l1ll111Il1l1, ) = os.pipe()
        lll1l11l11l11l11Il1l1 = spawn.get_command_line(tracker_fd=llll1l11l1111111Il1l1, pipe_handle=ll11ll1lllll11llIl1l1)


        llll111l11ll11llIl1l1 = str(Path(llll111ll1ll1ll1Il1l1['sys_argv'][0]).absolute())
        lll1l11l11l11l11Il1l1 = [lll1l11l11l11l11Il1l1[0], '-B', '-m', 'reloadium', 'spawn_process', str(llll1l11l1111111Il1l1), 
str(ll11ll1lllll11llIl1l1), llll111l11ll11llIl1l1]
        l1l1ll1ll1lllll1Il1l1._fds.extend([ll11ll1lllll11llIl1l1, l1l1l1llllll11llIl1l1])
        l1l1ll1ll1lllll1Il1l1.pid = util.spawnv_passfds(spawn.get_executable(), 
lll1l11l11l11l11Il1l1, l1l1ll1ll1lllll1Il1l1._fds)
        l1l1ll1ll1lllll1Il1l1.sentinel = l1lll1l111111ll1Il1l1
        with open(lll11lll1l1ll111Il1l1, 'wb', closefd=False) as l11ll11ll1llll11Il1l1:
            l11ll11ll1llll11Il1l1.write(llll1ll1l1ll1l11Il1l1.getbuffer())
    finally:
        ll1l1l1l1ll1l11lIl1l1 = []
        for ll1lllll1ll1l111Il1l1 in (l1lll1l111111ll1Il1l1, lll11lll1l1ll111Il1l1, ):
            if (ll1lllll1ll1l111Il1l1 is not None):
                ll1l1l1l1ll1l11lIl1l1.append(ll1lllll1ll1l111Il1l1)
        l1l1ll1ll1lllll1Il1l1.finalizer = util.Finalize(l1l1ll1ll1lllll1Il1l1, l11111l11l1l11l1Il1l1, ll1l1l1l1ll1l11lIl1l1)

        for ll1lllll1ll1l111Il1l1 in (ll11ll1lllll11llIl1l1, l1l1l1llllll11llIl1l1, ):
            if (ll1lllll1ll1l111Il1l1 is not None):
                os.close(ll1lllll1ll1l111Il1l1)


def __init__(l1l1ll1ll1lllll1Il1l1, ll11l1l11ll11l11Il1l1):
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

    llll111ll1ll1ll1Il1l1 = spawn.get_preparation_data(ll11l1l11ll11l11Il1l1._name)







    (l1111l1l1lllllllIl1l1, l1111111111ll1l1Il1l1, ) = _winapi.CreatePipe(None, 0)
    l11111l1ll1lllllIl1l1 = msvcrt.open_osfhandle(l1111111111ll1l1Il1l1, 0)
    ll1ll1lll11l1l11Il1l1 = spawn.get_executable()
    llll111l11ll11llIl1l1 = str(Path(llll111ll1ll1ll1Il1l1['sys_argv'][0]).absolute())
    lll1l11l11l11l11Il1l1 = ' '.join([ll1ll1lll11l1l11Il1l1, '-B', '-m', 'reloadium', 'spawn_process', str(os.getpid()), 
str(l1111l1l1lllllllIl1l1), llll111l11ll11llIl1l1])



    if ((WINENV and _path_eq(ll1ll1lll11l1l11Il1l1, sys.executable))):
        ll1ll1lll11l1l11Il1l1 = sys._base_executable
        ll1ll11l11ll111lIl1l1 = os.environ.copy()
        ll1ll11l11ll111lIl1l1['__PYVENV_LAUNCHER__'] = sys.executable
    else:
        ll1ll11l11ll111lIl1l1 = None

    with open(l11111l1ll1lllllIl1l1, 'wb', closefd=True) as ll11l1l111lll1l1Il1l1:

        try:
            (l11l1l11l11llll1Il1l1, ll1lll1l1l11111lIl1l1, ll11111lll1l11l1Il1l1, ll1111l11ll11111Il1l1, ) = _winapi.CreateProcess(ll1ll1lll11l1l11Il1l1, lll1l11l11l11l11Il1l1, None, None, False, 0, ll1ll11l11ll111lIl1l1, None, None)


            _winapi.CloseHandle(ll1lll1l1l11111lIl1l1)
        except :
            _winapi.CloseHandle(l1111l1l1lllllllIl1l1)
            raise 


        l1l1ll1ll1lllll1Il1l1.pid = ll11111lll1l11l1Il1l1
        l1l1ll1ll1lllll1Il1l1.returncode = None
        l1l1ll1ll1lllll1Il1l1._handle = l11l1l11l11llll1Il1l1
        l1l1ll1ll1lllll1Il1l1.sentinel = int(l11l1l11l11llll1Il1l1)
        if (sys.version_info > (3, 8, )):
            l1l1ll1ll1lllll1Il1l1.finalizer = util.Finalize(l1l1ll1ll1lllll1Il1l1, _close_handles, (l1l1ll1ll1lllll1Il1l1.sentinel, int(l1111l1l1lllllllIl1l1), 
))
        else:
            l1l1ll1ll1lllll1Il1l1.finalizer = util.Finalize(l1l1ll1ll1lllll1Il1l1, _close_handles, (l1l1ll1ll1lllll1Il1l1.sentinel, ))



        set_spawning_popen(l1l1ll1ll1lllll1Il1l1)
        try:
            reduction.dump(llll111ll1ll1ll1Il1l1, ll11l1l111lll1l1Il1l1)
            reduction.dump(ll11l1l11ll11l11Il1l1, ll11l1l111lll1l1Il1l1)
        finally:
            set_spawning_popen(None)
