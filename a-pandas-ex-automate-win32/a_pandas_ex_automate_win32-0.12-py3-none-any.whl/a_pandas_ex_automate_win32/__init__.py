import sys
from ctypes import py_object, WINFUNCTYPE
from ctypes.wintypes import BOOL, HWND, LPARAM


from collections import namedtuple, defaultdict
from ctypes import wintypes, byref
import ctypes
from ctypes import windll
import pandas as pd

from flatten_everything import flatten_everything
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions

pd_add_apply_ignore_exceptions()

childcounter = sys.modules[__name__]
childcounter.rightnow = None


def find_elements(pid_=0):

    user32 = ctypes.WinDLL("user32")
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    GetWindowRect = windll.user32.GetWindowRect
    GetClientRect = windll.user32.GetClientRect
    WindowInfoxx = namedtuple(
        "WindowInfoxx",
        "parent pid title windowtext hwnd length tid status coords_client dim_client coords_win dim_win class_name path",
    )

    def get_window_text(hWnd):
        length = windll.user32.GetWindowTextLengthW(hWnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        windll.user32.GetWindowTextW(hWnd, buf, length + 1)
        return buf.value

    class RECT(ctypes.Structure):
        _fields_ = [
            ("left", ctypes.c_long),
            ("top", ctypes.c_long),
            ("right", ctypes.c_long),
            ("bottom", ctypes.c_long),
        ]

    WNDENUMPROCA = ctypes.WINFUNCTYPE(
        BOOL,
        HWND,
        LPARAM,
    )

    def get_window_infos_all():
        """Return a sorted list of visible windows."""

        @WNDENUMPROCA
        def enum_proc(hWnd, lParam):
            status = "invisible"
            if user32.IsWindowVisible(hWnd):
                status = "visible"
            pid = wintypes.DWORD()
            tid = user32.GetWindowThreadProcessId(hWnd, ctypes.byref(pid))
            if pid_ == 0:
                pass
            else:
                if pid.value != pid_:
                    return True
            length = user32.GetWindowTextLengthW(hWnd) + 1
            title = ctypes.create_unicode_buffer(length)
            user32.GetWindowTextW(hWnd, title, length)
            rect = RECT()
            GetClientRect(hWnd, ctypes.byref(rect))
            left, right, top, bottom = rect.left, rect.right, rect.top, rect.bottom
            w, h = right - left, bottom - top
            coords_client = left, right, top, bottom
            dim_client = w, h
            rect = RECT()
            GetWindowRect(hWnd, ctypes.byref(rect))
            left, right, top, bottom = rect.left, rect.right, rect.top, rect.bottom
            w, h = right - left, bottom - top
            coords_win = left, right, top, bottom
            dim_win = w, h
            length_ = 257
            title = ctypes.create_unicode_buffer(length_)
            user32.GetClassNameW(hWnd, title, length_)
            classname = title.value
            try:
                windowtext = get_window_text(hWnd)
            except Exception:
                windowtext = ""
            try:
                coa = kernel32.OpenProcess(0x1000, 0, pid.value)
                path = (ctypes.c_wchar * 260)()
                size = ctypes.c_uint(260)
                kernel32.QueryFullProcessImageNameW(coa, 0, path, byref(size))
                filepath = path.value
                ctypes.windll.kernel32.CloseHandle(coa)
            except Exception as fe:
                filepath = ""
            if childcounter.rightnow is None:
                assc = -1
            else:
                assc = childcounter.rightnow
            result.append(
                (
                    WindowInfoxx(
                        assc,
                        pid.value,
                        title.value,
                        windowtext,
                        hWnd,
                        length,
                        tid,
                        status,
                        coords_client,
                        dim_client,
                        coords_win,
                        dim_win,
                        classname,
                        filepath,
                    )
                )
            )
            return True

        user32.EnumWindows(enum_proc, 0)
        return sorted(result)

    @WNDENUMPROCA
    def enum_proc2(hWnd, lParam):
        status = "invisible"
        if user32.IsWindowVisible(hWnd):
            status = "visible"
        pid = wintypes.DWORD()
        tid = user32.GetWindowThreadProcessId(hWnd, ctypes.byref(pid))
        if pid_ == 0:
            pass
        else:
            if pid.value != pid_:
                return True
        length = user32.GetWindowTextLengthW(hWnd) + 1
        title = ctypes.create_unicode_buffer(length)
        user32.GetWindowTextW(hWnd, title, length)
        rect = RECT()
        GetClientRect(hWnd, ctypes.byref(rect))
        left, right, top, bottom = rect.left, rect.right, rect.top, rect.bottom
        w, h = right - left, bottom - top
        coords_client = left, right, top, bottom
        dim_client = w, h
        rect = RECT()
        GetWindowRect(hWnd, ctypes.byref(rect))
        left, right, top, bottom = rect.left, rect.right, rect.top, rect.bottom
        w, h = right - left, bottom - top
        coords_win = left, right, top, bottom
        dim_win = w, h
        length_ = 257
        title = ctypes.create_unicode_buffer(length_)
        user32.GetClassNameW(hWnd, title, length_)
        classname = title.value
        try:
            windowtext = get_window_text(hWnd)
        except Exception:
            windowtext = ""
        try:
            coa = kernel32.OpenProcess(0x1000, 0, pid.value)
            path = (ctypes.c_wchar * 260)()
            size = ctypes.c_uint(260)
            kernel32.QueryFullProcessImageNameW(coa, 0, path, byref(size))
            filepath = path.value
            ctypes.windll.kernel32.CloseHandle(coa)
        except Exception as fe:
            filepath = ""
        if childcounter.rightnow is None:
            assc = -1
        else:
            assc = childcounter.rightnow
        result.append(
            (
                WindowInfoxx(
                    assc,
                    pid.value,
                    title.value,
                    windowtext,
                    hWnd,
                    length,
                    tid,
                    status,
                    coords_client,
                    dim_client,
                    coords_win,
                    dim_win,
                    classname,
                    filepath,
                )
            )
        )
        return True

    result2 = []

    def code(ara=None):
        def func(hwnd, param):
            result2.append(hwnd)
            param.append(hwnd)
            return True

        arr = []
        if isinstance(ara, type(None)):
            for x in range(1):
                WNDENUMPROC = WINFUNCTYPE(BOOL, HWND, py_object)
                windll.user32.EnumChildWindows.argtypes = [HWND, WNDENUMPROC, py_object]
                windll.user32.EnumChildWindows.restype = BOOL
                if ara is None:
                    windll.user32.EnumChildWindows(
                        windll.user32.GetDesktopWindow(), WNDENUMPROC(func), arr
                    )
                    for aszaz in arr:

                        yield aszaz
        else:
            if not isinstance(ara, list):
                ara = [ara]
            for oraz in ara:
                WNDENUMPROC = WINFUNCTYPE(BOOL, HWND, py_object)
                windll.user32.EnumChildWindows.argtypes = [HWND, WNDENUMPROC, py_object]
                windll.user32.EnumChildWindows.restype = BOOL
                windll.user32.EnumChildWindows(oraz, WNDENUMPROC(func), arr)
                for aszaz in arr:
                    yield aszaz

    def yieldstuff(u):
        baba = list(code(u))
        yield baba
        yield from code(baba)

    result = []
    allpr = []
    getta = list(
        set(list(flatten_everything(([x.hwnd for x in get_window_infos_all()]))))
    )
    while True:
        allpr = list(set(list(flatten_everything(allpr))))
        altla = len(allpr)
        for g in getta:
            allpr.append(g)
            childcounter.rightnow = g
            tempi = []
            for u in yieldstuff(g):
                try:
                    if u is None:
                        continue

                    tempi.append(u)
                except Exception as bh:
                    continue
            allpr.append(tempi.copy())
        allpr += result2.copy()
        allpr = list(set(list(flatten_everything(allpr))))
        getta = allpr.copy()
        if len(allpr) == altla:
            break

    while True:
        allpr = list(set(list(flatten_everything(allpr))))
        altla = len(allpr)
        tempi = []

        for alip in allpr:
            for u in yieldstuff(alip):
                try:
                    if u is None:
                        continue

                    tempi.append((u, alip))

                except Exception as bh:
                    continue
        allpr += tempi.copy()
        allpr += result2.copy()

        allpr = list(set(list(flatten_everything(allpr))))
        if len(allpr) == altla:
            break

    allpr = list(set((flatten_everything(allpr))))
    daxs = defaultdict(list)
    for buda in allpr:
        childcounter.rightnow = buda

        for u in yieldstuff(buda):

            try:
                if not u:
                    continue
                if not isinstance(u, list):
                    u = [u]

                    for _i in u:
                        try:
                            enum_proc2(_i, 0)
                            daxs[buda].append(_i)
                        except Exception:
                            continue

            except Exception as bh:
                # raise bh
                continue

    df = (
        pd.DataFrame(result)
        .drop_duplicates()
        .sort_values(by=["pid", "coords_win"], ascending=[True, False])
        .reset_index(drop=True)
    ).copy()
    df["all_children"] = pd.NA
    df["all_children"] = df["all_children"].astype("object")
    for key, item in daxs.items():
        baxa = df.loc[(df.hwnd == key)]
        newwar = [tuple(flatten_everything(item))]
        for i in baxa.index:
            df.at[i, "all_children"] = newwar

    df["all_children"] = df["all_children"].ds_apply_ignore(
        pd.NA, lambda x: tuple(set(x[0]))
    )
    return df.copy()


def pd_add_automate_win32():
    pd.Q_get_automate32_df = find_elements
