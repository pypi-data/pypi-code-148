"""
Function Help Scan/ScanFile.py

--[Mod]--
    --[hezhong_tzHEUR]-- => Try a heuristic scan and pass to the thread.
    --[jiance]-- => Heuristic scanning of dependent libraries.
    --[aikezi]-- => Heuristic scanning of dependent libraries.
    --[jiancefunc]-- => Heuristic scanning of dependent libraries.
    --[aidecide]-- => Heuristic main function. Passed to hezhong_tzHEUR Function
    --[get_md5_for_file] => Get file md5.
    --[main]-- => main.
--[File]--
    --[1.ini]-- => Config File. Don't move it!!!
    --[bd]--
        All files are databases. Don't move it!!!


--[Run]--
    Function:main(path)
    [path] => file path.
    Return:
        if False/None : Not detected
        if not False/None : This is the virus name
        if Error : try again.Feedback the Error? To https://bbs.flexible-world.com !


"""

import hashlib
import pefile
import threading as thre
from configparser import ConfigParser

def hezhong_tzHEUR(file, eng):
    global HEUR_ok
    global pe
    try:
        pe = pefile.PE(file)
    except Exception:
        HEUR_ok = 'Noj'
        return 'Noj'
    HEUR_ok = 'Noj'
    virusname = ''
    virusname, ensitivity = aidecide(file, eng)

    if virusname is not None:
        HEUR_ok = virusname + '({})'.format(ensitivity)
        return virusname + '({})'.format(ensitivity)
    else:
        HEUR_ok = 'Noj'
        return 'Noj'
    # print(jiancea('a',filebyte))
    # print(virusname)


def jiance(name, filebytes):
    if bytes(name, 'utf-8') in filebytes:
        return True
    elif bytes(name.lower(), 'utf-8') in filebytes:
        return True
    elif bytes(name.upper(), 'utf-8') in filebytes:
        return True
    else:
        return False


def aikezi(filebyte):
    if bytes("Pantikill", 'utf-8') in filebyte:
        return "Pantikill"
    elif bytes("vmp0", 'utf-8') in filebyte:
        return "VMP"
    elif bytes("PECompact", 'utf-8') in filebyte:
        return "PECompact"
    elif bytes("ex_cod", 'utf-8') in filebyte:
        return "eXPressor"
    elif bytes("FSG!", 'utf-8') in filebyte:
        return "FSG"
    elif bytes("MaskPE", 'utf-8') in filebyte:
        return "MaskPE"
    elif bytes("UPX", 'utf-8') in filebyte:
        return "UPX"
    elif bytes("T-VMP", 'utf-8') in filebyte:
        return "VMP"
    else:
        return -1


def jiancefunc(name):
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        for function in entry.imports:
            fucn = str(function.name)
            lena = len(fucn)
            if name == fucn[2:lena - 1]:
                return True
    return False


def aidecide(path, ensitivity):
    virusname = None
    tv = 0
    with open(path, 'rb') as fp:
        filebyte = fp.read()
    # 检测信任软件
    if jiance("Microsoft.Windows.Terminal.Win32Host", filebyte):
        return virusname, tv
    if jiance(r"\Microsoft\WindowsApps\Microsoft.WindowsNotepad_8wekyb3d8bbwe\notepad.exe", filebyte):
        return virusname, tv
    if jiance("CentBrowser", filebyte):
        return virusname, tv
    if jiance("browser_watcher", filebyte):
        return virusname, tv
    if jiance('video', filebyte):
        return virusname, tv
    if jiance('WAVEfmt', filebyte) and jiance('RIFFHXN', filebyte):
        return virusname, tv
    if jiance('ftypmp42', filebyte):
        return virusname, tv

    # 查壳

    if aikezi(filebyte) != -1:
        if aikezi(filebyte) == 'Pantikill':
            virusname = "Heur.Enclosure.Pantikill"
            return virusname, ensitivity
        if aikezi(filebyte) == 'VMP':
            virusname = "Heur.Enclosure.VMP"
            return virusname, ensitivity
        if aikezi(filebyte) == 'VMP':
            virusname = "Heur.Enclosure.VMP"
            return virusname, ensitivity
        if aikezi(filebyte) == 'PECompact':
            virusname = "Heur.Enclosure.PECompact"
            return virusname, ensitivity
        if aikezi(filebyte) == 'eXPressor':
            virusname = "Heur.Enclosure.eXPressor"
            return virusname, ensitivity
        if aikezi(filebyte) == 'FSG':
            virusname = "Heur.Enclosure.FSG"
            return virusname, ensitivity
        if aikezi(filebyte) == 'MaskPE':
            virusname = "Heur.Enclosure.MaskPE"
            return virusname, ensitivity
        if aikezi(filebyte) == 'UPX':
            tv += 15
        if jiancefunc('GetMappedFileNameW'):
            tv += 20
            if jiancefunc('VirtualQuery'):
                virusname = 'Heur.ProtectionShell.a'
                return virusname, ensitivity
    if jiancefunc('_CorExeMain'):
        tv += 30
    if jiancefunc('EnumSystemLocalesW') or jiancefunc('EnumTimeFormatsA') or jiancefunc('EnumWindows') or jiancefunc(
            'EnumDesktopWindows') or jiancefunc('EnumDateFormatsA') or jiancefunc('EnumChildWindows') or jiancefunc(
        'EnumThreadWindows') or jiancefunc('EnumSystemLocales') or jiancefunc('EnumSystemGeoID') or jiancefunc(
        'EnumSystemLanguageGroupsA') or jiancefunc('EnumUILanguagesA') or jiancefunc('EnumDesktopsW') or jiancefunc(
        'EnumSystemCodePagesW') or jiancefunc('EnumSystemCodePagesA'):
        tv += 25
        if jiancefunc('EnumSystemLocalesA'):
            virusname = 'Heur.Shellcode.a'
            return virusname, ensitivity
    if jiance("True Cloud Consulting Inc", filebyte):
        virusname = "Heur.Backdoor.Telegram.a"
        return virusname, ensitivity
    if jiance("亚洲诚信代码签名测试证书", filebyte):
        virusname = 'Suspicious.CERT.a'
        return virusname, ensitivity
    # 检测勒索
    if jiancefunc('NtCreateFile'):
        virusname = 'Heur.Ransom.LockMBR.a'
        return virusname, ensitivity
    if jiancefunc('NtWriteFile'):
        virusname = 'Heur.Ransom.LockMBR.c'
        return virusname, ensitivity
    if jiance(r"\\.\PhysicalDrive0", filebyte):
        if jiancefunc("lwrite") or jiancefunc("WriteFile"):
            virusname = "Heur.Jock.MEMZ.a"
            return virusname, ensitivity
        tv += 20
    if jiance("Password", filebyte) or jiance("QQ", filebyte):
        tv += 5
    if jiance("net user", filebyte) and jiancefunc("ShellExecuteA"):
        virusname = "Heur.Lock.a"
    if jiancefunc("Resources"):
        tv += 10
        if jiancefunc("VirtualProtect"):
            tv += 20
    # 检测后门

    if jiancefunc("RtlAdjustPrivilege"):
        virusname = "Heur.Backdoor.a"
        return virusname, ensitivity
    if jiancefunc("HideCurrentProcess"):
        virusname = "Heur.Backdoor.b"
        return virusname, ensitivity
    if jiancefunc("SetFileAttributes") or jiancefunc("SetFileAttributesW"):
        tv += 15
    if jiancefunc("CopyScreen") or jiancefunc("PrintWindow"):
        tv += 10
    if jiancefunc("FtpPutFile") or jiancefunc("WinHttpSendRequest") or jiancefunc("HttpSendRequestA") or jiancefunc(
            "WinHttpWriteData"):
        virusname = "Heur.Backdoor.ScreenSpy.a"
        return virusname, ensitivity
    if jiancefunc("GetAsyncKeyState"):
        tv += 15
        if jiancefunc("FtpPutFile") or jiancefunc("WinHttpSendRequest") or jiancefunc("HttpSendRequestA") or jiancefunc(
                "WinHttpWriteData"):
            virusname = "Heur.Backdoor.KeyboardSpy.a"
            return virusname, ensitivity
    if jiancefunc("GetRawInput") and jiancefunc("RegisterRawInputDevice") and jiancefunc(
            "GetRawInputDeviceList") and jiancefunc("GetRawInputDeviceInfo") and jiancefunc("GetRawInputData"):
        virusname = "Heur.Backdoor.KeyboardSpy.b"
        return virusname, ensitivity
    if jiancefunc("GetClipboardData"):
        if jiancefunc("FtpPutFile") or jiancefunc("WinHttpSendRequest") or jiancefunc("HttpSendRequestA") or jiancefunc(
                "WinHttpWriteData"):
            virusname = "Heur.Backdoor.ClipboardSpy.a"
            return virusname, ensitivity
        if jiancefunc("GetClipboardFormatName"):
            tv += 5
            if jiance("SetClipboardData"):
                tv += 15
    if jiancefunc("GetKeyState"):
        tv += 15
    if jiancefunc("keydb_event"):
        virusname = "Heur.Backdoor.Keydb.a"
        return virusname, ensitivity
    if jiancefunc("InternetGetCookieA"):
        if jiancefunc("FtpPutFile") or jiancefunc("WinHttpSendRequest") or jiancefunc("HttpSendRequestA") or jiancefunc(
                "WinHttpWriteData"):
            virusname = "Heur.Backdoor.CookieSpy.a"
            return virusname, ensitivity
        tv += 10
    if jiancefunc("ShellExecuteA"):
        tv += 10
    # 检测systemkiller
    if jiancefunc("GetSystemDirectory") or jiancefunc("GetWindowsDirectory"):
        if jiancefunc("DeleteFile") or jiancefunc("RemoveDirectory"):
            tv += 15
    if jiancefunc("NtRaiseHardError") or jiancefunc("ZwRaiseHardError"):
        virusname = "Heur.SystemKiller.c"
        return virusname, ensitivity
    if jiancefunc("SRRemoveRestorePoint"):
        virusname = "Heur.SystemKiller.d"
        return virusname, ensitivity
    if jiancefunc("SHFormatDrive"):
        virusname = "Heur.SystemKiller.f"
        return virusname, ensitivity
    if jiancefunc("DeleteVolumeMountPointW"):
        virusname = "Heur.SystemKiller.KillDick.a"
        return virusname, ensitivity
    if jiancefunc("ZwShutdownSystem"):
        virusname = "Heur.SystemKiller.s"
        return virusname, ensitivity
    if jiancefunc("GetWindowsDirectory") or jiancefunc("GetSystemDirectory"):
        if jiancefunc("LZRead") or jiancefunc("ReadFile"):
            if jiancefunc("lwrite") or jiancefunc("WriteFile"):
                tv += 15
    if jiancefunc("GetProfileStringA") or jiancefunc("GetPrivateProfileString") or jiancefunc(
            "GetProfileIntA") or jiancefunc("GetPrivateProfileInt"):
        if jiancefunc("WriteProfileStringA") or jiancefunc("WritePrivateProfileStringA"):
            tv += 15
    if jiancefunc("FlushFileBuffers"):
        tv += 15

    # 蠕虫检测
    if jiancefunc("CreateService"):
        tv += 15
        if jiancefunc("StartService"):
            if jiance("QQPCTray", filebyte) or jiance("QQPCRTP", filebyte) or jiance("HipsDaemon", filebyte) or jiance(
                    "HipsMain", filebyte) or jiance("HipsTray", filebyte) or jiance("360Tray", filebyte) or jiance(
                "360sd", filebyte) or jiance("360rp", filebyte) or jiance("ZhuDongFangYu", filebyte) or jiance(
                "kxetray", filebyte) or jiance("kxescore", filebyte) or jiance("rstray", filebyte) or jiance(
                "ravmond", filebyte) or jiance("NPFMntor", filebyte) or jiance("AVP", filebyte) or jiance("F-PROT",
                                                                                                          filebyte):
                virusname = "Heur.Rootkit.AntiAV.a"
                return virusname, ensitivity
            if jiancefunc("DeviceIoControl"):
                virusname = "Heur.Rootkit.b"
                return virusname, ensitivity
    if jiance("hao123.com", filebyte) or jiance("hao.360.cn", filebyte) or jiance("duba.com", filebyte) or jiance(
            "2345.com", filebyte) or jiance("daohang.qq.com", filebyte) or jiance("uc123.com", filebyte) or jiance(
        "jiegeng.com", filebyte):
        virusname = "Heur.Rootkit.StartPage.a"
        return virusname, ensitivity
    if jiance('sfbao.com', filebyte) or jiance('jjj.com', filebyte) or jiance('666sf.com.cn', filebyte) or jiance(
            '9hf.com', filebyte) or jiance('789ss.com', filebyte) or jiance('zsf.com', filebyte):
        virusname = "Heur.Rootkit.Sifu.a"
        return virusname, ensitivity
    if jiancefunc("SetWindowsHook") or jiancefunc("CallNextHookEx"):
        virusname = "Heur.WindowHook.a"
        return virusname, ensitivity

    # 检测QQ相关木马
    if jiance("://localhost.ptlogin2.qq.com", filebyte) or jiance("/pt_get_st?clientuin=", filebyte) or jiance(
            "&callback=ptui_getst_CB&r=", filebyte) or jiance("&pt_local_tk=", filebyte):
        if jiancefunc("FtpPutFile") or jiancefunc("WinHttpSendRequest") or jiancefunc("HttpSendRequestA") or jiancefunc(
                "WinHttpWriteData"):
            virusname = "Heur.QQSpy.a"
            return virusname, ensitivity
        virusname = "Heur.QQPass.a"
        return virusname, ensitivity

    # AVkiller
    if jiancefunc("ZwSuspendProcess") or jiancefunc("NtSuspendProcess"):
        virusname = "Heur/AntiAV.b"
        return virusname, ensitivity
    if jiance("QQPCTray", filebyte) or jiance("QQPCRTP", filebyte) or jiance("HipsDaemon", filebyte) or jiance(
            "HipsMain", filebyte) or jiance("HipsTray", filebyte) or jiance("360Tray", filebyte) or jiance("360sd",
                                                                                                           filebyte) or jiance(
        "360rp", filebyte) or jiance("ZhuDongFangYu", filebyte) or jiance("kxetray", filebyte) or jiance("kxescore",
                                                                                                         filebyte) or jiance(
        "rstray", filebyte) or jiance("ravmond", filebyte) or jiance("NPFMntor", filebyte) or jiance("AVP",
                                                                                                     filebyte) or jiance(
        "F-PROT", filebyte):
        tv += 15

    # 感染型检测

    # 可疑行为检测
    if jiancefunc("SetWindowPos") or jiancefunc("BringWindowToTop"):
        tv += 5
        if jiancefunc("EnumWindows") or jiancefunc("GetTopWindow"):
            tv += 15
    if jiancefunc("ZwClose"):
        tv += 15
        if jiancefunc("reateToolhelp32Snapshot"):
            tv += 15
    if jiancefunc("MessageBox") == False:
        tv += 10
    if jiancefunc("SetPriorityClass"):
        tv += 5
    if jiancefunc("ExitWindowsEx"):
        tv += 10
    if jiancefunc("TerminateProcess"):
        tv += 10
        if jiancefunc("CreateToolhelp32Snapshot"):
            tv += 10
    if jiancefunc("GetStartupInfo") or jiancefunc("IsProcessorFeaturePresent") or jiancefunc(
            "IsDebuggerPresent") or jiancefunc("QueryPerformanceCounter") or jiancefunc("nhandledExceptionFilter"):
        tv += 15
    if jiance("HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\services\Disk\Enum\Count", filebyte) != False:
        virusname = "Heur/VirMachine.Detection"
        return virusname, ensitivity
    if jiancefunc("VirtualAllocEx") and jiancefunc("CreateRemoteThread") and jiancefunc(
            "GetModuleHandleA") and jiancefunc("WaitForSingleObject"):
        tv += 30
    if jiance("NtAllocateVirtualMemory", filebyte):
        tv += 30
    if jiancefunc("GetSystemInfo"):
        tv += 20
    if jiancefunc("OpenPrinterA"):
        tv += 15
    if jiance("SetUnhandledExceptionFilter", filebyte):
        tv += 10
    if jiance("OutputDebugStringA", filebyte):
        tv += 10

    # 检测滑稽程序

    if jiancefunc("CorExitProcess"):
        if jiancefunc("MsiViewFetch"):
            virusname = "Heur.LikeTrojan.a"
            return virusname, ensitivity
    if jiance("shutdown", filebyte):
        tv += 10
    if jiancefunc("mouse_event"):
        if jiancefunc("SetCursorPos"):
            virusname = "Heur.Joke.m"
            return virusname, ensitivity
    if jiancefunc("ShowCursor"):
        virusname = "Heur.Joke.a"
        return virusname, ensitivity
    if jiancefunc("SwapMouseButton"):
        virusname = "Heur.Joke.b"
        return virusname, ensitivity
    if jiancefunc("mouse_event") or jiancefunc("SetCursorPos"):
        virusname = "Heur.Joke.c"
        return virusname, ensitivity
    if jiancefunc("StretchBlt"):
        virusname = "Heur.Joke.d"
        return virusname, ensitivity
    if jiancefunc("BitBlt"):
        virusname = "Heur.Joke.e"
    if jiancefunc("LoadIcon") or jiancefunc("LoadImage"):
        if jiancefunc("DrawIcon"):
            virusname = "Heur.Joke.f"
            return virusname, ensitivity
    if jiancefunc("BlockInput") or jiancefunc("EnableWindow"):
        tv += 15

    if jiancefunc('miniw'):
        virusname = 'Heur.Jock.MiniWorld.a'
        return virusname, ensitivity

    if jiancefunc('mini1'):
        virusname = 'Heur.Jock.MiniWorld.b'
        return virusname, ensitivity

    if jiancefunc('iworld'):
        virusname = 'Heur.Jock.MiniWorld.c'
        return virusname, ensitivity

    if tv >= 100 - ensitivity:
        virusname = "Trojan.Generic"
    return virusname, tv








def get_md5_for_file(filename):  # 获取MD5
    file_object = open(filename, 'rb')
    file_name = filename
    file_content = file_object.read()
    file_object.close()
    file_md5 = hashlib.md5(file_content)
    file_object.close()
    return file_md5.hexdigest()




def main(path):
    """

    :param path: File Path
    :return:         if False/None : Not detected
        if not False/None : This is the virus name
        if Error : try again.Feedback the Error? To https://bbs.flexible-world.com !
    """
    try:
        bd = get_md5_for_file(path)
    except Exception as err:
        bd = 'M'
    global HEUR_ok
    with open('bd/data1.vdb') as f:
        white_HEUR = f.read()
    with open('bd/ver.dll') as f:
        ver_log_print1 = f.read()
    with open('bd/ve.dll') as f:
        ver_log_print2 = f.read()
    conf = ConfigParser()  # 需要实例化一个ConfigParser对象
    conf.read('1.ini')  # 需要添加上config.ini的路径，不需要open打开，直接给文件路径就读取，也可以指定encoding='utf-8'
    t = conf['scan']['tz']  # 读取user段的name变量的值，字符串格式

    if t == 'N':
        open_hetz = False
    else:
        open_hetz = True


    with open('bd/bd.dll', 'r') as f:
        bdk = f.read()
    global bdfile  # 全局滑稽
    if bd in bdk:
        return 'Trojan.{}'.format(bd)
    else:
        if open_hetz:
            thred_1 = thre.Thread(target=hezhong_tzHEUR, args=(path, 40))
            thred_1.start()
            thred_1.join()
            if HEUR_ok == 'Noj' or HEUR_ok == None:
                return False
            else:
                if bd in white_HEUR:
                    return False
                else:
                    return HEUR_ok



        else:
            return False



